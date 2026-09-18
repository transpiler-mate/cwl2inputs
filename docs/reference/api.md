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

# API reference

The installed entry point is `cwl2inputs.plugin:cwl2inputs` in the
`transpiler_mate.plugins` group.

| Option | Type | Default | Meaning |
| --- | --- | --- | --- |
| `output` / `--output` | `Path` | `inputs.yaml` | Destination YAML file. |

Unknown options are rejected. `generate_template(context)` returns YAML text;
`cwl2inputs.execute(context, options)` writes it. Both require a selected process.
The plugin wraps generation and output failures as `PluginExecutionError` with
the original exception as its cause. Selection errors use the runtime's message.

::: cwl2inputs.plugin
