<!--
Copyright 2026 Terradue

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# CWL 2 Inputs

[![PyPI - Version](https://img.shields.io/pypi/v/cwl2inputs.svg)](https://pypi.org/project/cwl2inputs)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cwl2inputs.svg)](https://pypi.org/project/cwl2inputs)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/transpiler-mate/cwl2inputs/package.yaml?branch=develop&event=push&label=build&logo=githubactions)](https://github.com/transpiler-mate/cwl2inputs/actions/workflows/package.yaml?query=branch%3Adevelop)
[![Code coverage](https://img.shields.io/codecov/c/github/transpiler-mate/cwl2inputs/develop?logo=codecov)](https://app.codecov.io/gh/transpiler-mate/cwl2inputs/tree/develop)

`cwl2inputs` is a Transpiler-Mate plugin that generates an `inputs.yaml` template
for a selected CWL workflow or tool using cwltool's Python APIs.

## Install from source

Use Python 3.10 or newer. From this repository:

```console
python -m pip install . transpiler-mate-runtime
```

The plugin registers in `transpiler_mate.plugins` and is invoked through the
runtime; there is no standalone `cwl2inputs` executable.

## Usage

```console
transpiler-mate cwl2inputs --output inputs.yaml 'workflow.cwl#main'
```

For the burned-area workflow, from the organization workspace:

```console
transpiler-mate cwl2inputs \
  --output tmp/build/burned-area-severity/inputs.yaml \
  'tmp/burned-area-severity.cwl#burned-area-severity'
```

`--output` defaults to `inputs.yaml`. Parent directories are created as needed;
an existing output file is replaced after successful template generation.
Always select the process with `#<process-id>`, including single-process documents.
The runtime requires document-level Schema.org `SoftwareApplication` metadata.

The plugin uses the already-resolved CWL graph and calls cwltool's `load_tool`
and `make_template` APIs. It does not execute workflows or containers.
Defaults, example values, and YAML comments come from cwltool. Input ordering
may differ from running cwltool on the original source because the runtime
normalizes the document.

Templates are starting points: replace file/directory paths and other
placeholders before execution. Named optional schemas may appear as schema URI
placeholders; replace them with a value matching the schema or `null`.

## Documentation and development

See the [first-steps tutorial](docs/tutorials/first-steps.md),
[CLI guide](docs/how-to/use-cli.md), and [API reference](docs/reference/api.md).
See [CONTRIBUTING.md](CONTRIBUTING.md) for checks and development setup.

Bootstrapped with [transpiler-mate-plugin-project-template](https://github.com/transpiler-mate/transpiler-mate-plugin-project-template)
using Copier.

## License

[![Apache License, Version 2.0](https://img.shields.io/badge/license-Apache%20License%202.0-blue)](https://www.apache.org/licenses/LICENSE-2.0)
