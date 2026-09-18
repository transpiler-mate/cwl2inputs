# Copyright 2026 Transpiler-Mate
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from importlib.metadata import entry_points
from io import StringIO
from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner
from cwl_loader import load_cwl_from_location, load_cwl_from_string_content
from cwl_loader.utils import to_index
from cwltool.context import LoadingContext
from cwltool.load_tool import load_tool
from cwltool.main import make_template
from cwltool.workflow import default_make_tool
from pydantic import ValidationError
from ruamel.yaml import YAML
from transpiler_mate.api import (
    PluginExecutionError,
    SoftwareApplication,
    TranspilerContext,
)
from transpiler_mate.runtime.cli import main

from cwl2inputs.plugin import CWL2InputsOptions, cwl2inputs, generate_template

DOCUMENT = """
cwlVersion: v1.2
$graph:
  - class: Workflow
    id: main
    inputs:
      pre_event: Directory
      post_event: Directory
      count:
        type: int
        default: 7
      optional: string?
      choices:
        type:
          type: enum
          symbols: [red, blue]
      files: File[]
      settings:
        type:
          type: record
          name: Settings
          fields:
            enabled: boolean
    outputs: []
    steps: []
  - class: CommandLineTool
    id: other
    baseCommand: echo
    inputs:
      message:
        type: string
        default: hello
    outputs: []
"""


def make_context(
    document: str = DOCUMENT, process_id: str | None = "main"
) -> TranspilerContext:
    loaded = load_cwl_from_string_content(document)
    processes = loaded if isinstance(loaded, list) else [loaded]
    return TranspilerContext.model_construct(
        source="file:///unavailable/original.cwl",
        process_id=process_id,
        document=to_index(processes),
        metadata=SoftwareApplication.model_construct(),
    )


def test_template_matches_cwltool(tmp_path: Path) -> None:
    source = tmp_path / "original.cwl"
    source.write_text(DOCUMENT)
    loading = LoadingContext()
    loading.construct_tool_object = default_make_tool
    expected = StringIO()
    make_template(load_tool(f"{source.as_uri()}#main", loading), expected)
    loaded = load_cwl_from_location(str(source))
    context = make_context().model_copy(
        update={"document": to_index(loaded if isinstance(loaded, list) else [loaded])}
    )
    output = tmp_path / "nested" / "inputs.yaml"
    cwl2inputs.execute(context, CWL2InputsOptions(output=output))
    assert YAML(typ="safe").load(output.read_text()) == YAML(typ="safe").load(
        expected.getvalue()
    )
    template = YAML(typ="safe").load(output.read_text())
    assert template["count"] == 7
    assert template["pre_event"]["class"] == "Directory"
    assert template["files"][0]["class"] == "File"
    assert template["settings"]["enabled"] is False
    assert "#" in output.read_text()


def test_selected_tool_only() -> None:
    template = YAML(typ="safe").load(
        generate_template(make_context(process_id="other"))
    )
    assert template == {"message": "hello"}


@pytest.mark.parametrize("process_id", [None, "missing"])
def test_invalid_selection_preserves_output(
    tmp_path: Path, process_id: str | None
) -> None:
    output = tmp_path / "inputs.yaml"
    output.write_text("existing")
    with pytest.raises(PluginExecutionError):
        cwl2inputs.execute(
            make_context(process_id=process_id), CWL2InputsOptions(output=output)
        )
    assert output.read_text() == "existing"


def test_write_failure_is_plugin_error(tmp_path: Path) -> None:
    with pytest.raises(PluginExecutionError, match="Unable to generate") as error:
        cwl2inputs.execute(make_context(), CWL2InputsOptions(output=tmp_path))
    assert isinstance(error.value.__cause__, OSError)


def test_generation_failure_preserves_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(*args: Any, **kwargs: Any) -> None:
        raise ValueError("invalid CWL")

    monkeypatch.setattr("cwl2inputs.plugin.load_tool", fail)
    output = tmp_path / "inputs.yaml"
    output.write_text("existing")
    with pytest.raises(PluginExecutionError, match="invalid CWL"):
        cwl2inputs.execute(make_context(), CWL2InputsOptions(output=output))
    assert output.read_text() == "existing"


def test_options_and_registration() -> None:
    assert CWL2InputsOptions().output == Path("inputs.yaml")
    with pytest.raises(ValidationError):
        CWL2InputsOptions.model_validate({"unknown": True})
    registration = next(
        iter(entry_points(group="transpiler_mate.plugins", name="cwl2inputs"))
    ).load()
    assert registration is cwl2inputs


def test_runtime_cli(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = Path(__file__).parent / "fixtures" / "hello.cwl"
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(main, ["cwl2inputs", f"{source.resolve()}#hello"])
    assert result.exit_code == 0, result.output
    assert YAML(typ="safe").load((tmp_path / "inputs.yaml").read_text()) == {
        "message": "Hello world"
    }


def test_no_context_mutation() -> None:
    from cwl_utils.parser import save

    context = make_context()
    before = save(list(context.processes), relative_uris=False)
    first = generate_template(context)
    assert save(list(context.processes), relative_uris=False) == before
    assert generate_template(context) == first
