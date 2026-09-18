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

# Architecture

Transpiler-Mate owns source resolution, metadata validation, and process selection.
The plugin depends on `transpiler-mate-api`, not the runtime implementation.

The plugin serializes the context's complete resolved graph with `cwl_utils.parser.save`
to a temporary CWL document. Keeping the graph preserves subworkflow references.
It removes generated blank-node names on anonymous enums so cwltool retains its
usual enum placeholders. The context itself is not mutated.

It then uses cwltool's `load_tool` with `default_make_tool` to load the selected
process, and [`make_template`](https://cwltool.readthedocs.io/en/latest/autoapi/cwltool/main/index.html#cwltool.main.make_template)
to render YAML into memory. The temporary document is cleaned up automatically.
No subprocess, workflow execution, or container launch is involved.

The original source is not fetched again by the plugin. Schema references that
remain external can still require network access. Runtime normalization can
change input ordering and schema identifiers compared with the original source.
Placeholder generation follows the installed cwltool version, including its
limitations for optional named schema types.

Only after rendering succeeds does the plugin create parent directories and
write the destination. This protects existing output from loading or rendering
failures; the final filesystem write is not atomic.
