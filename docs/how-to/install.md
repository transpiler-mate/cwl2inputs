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

# Install

Use Python 3.10 or newer. Clone the repository and install it alongside the runtime:

```console
git clone https://github.com/Transpiler-Mate/cwl2inputs.git
cd cwl2inputs
python -m pip install . transpiler-mate-runtime
transpiler-mate cwl2inputs --help
```

For development, use `python -m pip install -e . transpiler-mate-runtime`.
Install the runtime and plugin in the same environment so entry-point discovery
can find `cwl2inputs`.
