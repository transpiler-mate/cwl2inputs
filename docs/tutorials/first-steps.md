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

# First steps

Install the plugin and runtime from the repository:

```console
python -m pip install . transpiler-mate-runtime
```

Save this document as `hello.cwl`. The Schema.org metadata is required by the
Transpiler-Mate runtime:

```yaml
cwlVersion: v1.2
class: CommandLineTool
id: hello
baseCommand: echo
inputs:
  message:
    type: string
    default: Hello world
    inputBinding:
      position: 1
outputs: []
$namespaces:
  s: https://schema.org/
s:name: Hello
s:description: A minimal template-generation example.
s:dateCreated: '2026-09-18'
s:license: https://spdx.org/licenses/Apache-2.0
s:softwareVersion: '0.1.0'
s:softwareHelp:
  s:name: User guide
  s:url: https://example.org/hello
s:publisher:
  s:name: Example Organization
s:author:
  s:givenName: Example
  s:familyName: Author
  s:email: author@example.org
  s:affiliation:
    s:name: Example Organization
```

Generate a template for the `hello` entrypoint:

```console
transpiler-mate cwl2inputs --output inputs.yaml 'hello.cwl#hello'
```

The generated YAML contains the input default:

```yaml
message: Hello world  # default value of type 'string'.
```

Edit `message` as needed. Template generation only inspects the workflow; it
does not run `echo`. For a larger document, select another `#<process-id>` to
produce a template for that process alone.
