<!--
Copyright 2026 Transpiler-Mate

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

# Contributing to CWL 2 Inputs

This project was generated from `transpiler-mate-plugin-project-template` with
Copier (`project_name="CWL 2 Inputs"`, `project_slug="cwl2inputs"`,
`python_package="cwl2inputs"`).

Install Hatch, then run:

```console
hatch run test:test
hatch run dev:typecheck
hatch run dev:lint
hatch run dev:check
hatch run dev:security
hatch build
```

`dev:lint` formats files and `dev:check` applies lint fixes. To check without
changing files, use `hatch run dev:ruff format --check src tests` and
`hatch run dev:ruff check src tests`.

Build the documentation with:

```console
python -m pip install -r requirements-docs.txt
mkdocs build --strict
```

Tests exercise cwltool's actual Python APIs, template values, process selection,
entry-point registration, and failure handling. The default suite uses local
fixtures and requires neither Docker nor remote CWL schemas.
