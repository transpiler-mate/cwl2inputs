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

# Generate an input template

Select the CWL process with a fragment and choose an output file:

```console
transpiler-mate cwl2inputs --output build/inputs.yaml 'workflow.cwl#main'
```

The fragment is required even for a single-process document. Use the workflow
or tool's `id`, not its display label. A missing or unknown fragment is an error.

Without `--output`, the plugin writes `inputs.yaml` in the current directory.
Relative output paths are resolved against that directory. Missing parents are
created and existing files are overwritten after generation succeeds.

The runtime loads the source and validates its Schema.org software metadata.
The plugin operates on that resolved graph. Remote schema references still
present in it may require network access during cwltool validation.

Replace directory/file paths and schema placeholders before running the workflow.
Optional named types can be set to `null` when no value is needed. Generating a
template does not execute the workflow or validate your eventual input values.
