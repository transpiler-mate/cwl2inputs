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

"""Generate a YAML input template for the runtime-selected CWL process."""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from cwl_utils.parser import save
from cwltool.context import LoadingContext
from cwltool.load_tool import load_tool
from cwltool.main import make_template
from cwltool.workflow import default_make_tool
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field
from transpiler_mate.api import PluginExecutionError, transpiler_plugin

if TYPE_CHECKING:
    from transpiler_mate.api import TranspilerContext


class CWL2InputsOptions(BaseModel):
    """Output options for input template generation."""

    model_config = ConfigDict(extra="forbid")

    output: Path = Field(
        default=Path("inputs.yaml"), description="The output YAML file path"
    )


def _remove_anonymous_enum_names(value: Any) -> None:
    """Undo cwl-utils' generated enum names so cwltool keeps its placeholders."""
    if isinstance(value, dict):
        if value.get("type") == "enum" and str(value.get("name", "")).startswith("_:"):
            value.pop("name")
        for child in value.values():
            _remove_anonymous_enum_names(child)
    elif isinstance(value, list):
        for child in value:
            _remove_anonymous_enum_names(child)


def generate_template(context: TranspilerContext) -> str:
    """Render cwltool's template from the resolved graph and selected process.

    An explicit source fragment is required, following the runtime's
    ``resolved_process`` contract. No workflow or container is executed.
    """
    process = context.resolved_process
    document = save(list(context.processes), relative_uris=False)
    _remove_anonymous_enum_names(document)
    with TemporaryDirectory(prefix="cwl2inputs-") as directory:
        source = Path(directory) / "workflow.cwl"
        source.write_text(json.dumps(document), encoding="utf-8")
        loading_context = LoadingContext()
        loading_context.construct_tool_object = default_make_tool
        tool = load_tool(
            f"{source.as_uri()}#{quote(process.id, safe='/')}", loading_context
        )
        output = StringIO()
        make_template(tool, output)
        return output.getvalue()


@transpiler_plugin(
    name="cwl2inputs",
    description="Generate a CWL inputs YAML template using cwltool.",
    options_model=CWL2InputsOptions,
)
def cwl2inputs(context: TranspilerContext, options: CWL2InputsOptions) -> None:
    """Write a template, preserving cwltool's defaults and placeholder comments."""
    try:
        template = generate_template(context)
        options.output.parent.mkdir(parents=True, exist_ok=True)
        options.output.write_text(template, encoding="utf-8")
        logger.success(f"Input template written to {options.output.absolute()}")
    except PluginExecutionError:
        raise
    except Exception as exc:
        raise PluginExecutionError(
            f"Unable to generate input template at {options.output.absolute()}: {exc}"
        ) from exc
