TITLE: Create a Simple Hello World JavaScript Action
DESCRIPTION: This snippet demonstrates the basic structure of a JavaScript action. It shows how to retrieve an input value using `core.getInput` and print a greeting to the console. This is a fundamental example for getting started with JavaScript-based GitHub Actions.
SOURCE: https://github.com/actions/toolkit/blob/main/README.md#_snippet_10

LANGUAGE: javascript
CODE:
```
...\n  const nameToGreet = core.getInput('who-to-greet');\n  console.log(`Hello ${nameToGreet}!`);\n...
```

----------------------------------------

TITLE: Walkthrough for a Comprehensive JavaScript Action
DESCRIPTION: This walkthrough provides a template for building a complete JavaScript Action, including setup for tests, linting, workflow integration, publishing, and versioning. It illustrates how to get input values and perform asynchronous operations. The snippet also includes example test output, demonstrating successful execution of unit tests for the action.
SOURCE: https://github.com/actions/toolkit/blob/main/README.md#_snippet_11

LANGUAGE: javascript
CODE:
```
async function run() {\n  try {\n    const ms = core.getInput('milliseconds');\n    console.log(`Waiting ${ms} milliseconds ...`)\n    ...
```

LANGUAGE: javascript
CODE:
```
PASS ./index.test.js\n  ✓ throws invalid number\n  ✓ wait 500 ms\n  ✓ test runs\n\nTest Suites: 1 passed, 1 total\nTests:       3 passed, 3 total
```

----------------------------------------

TITLE: Handling Inputs and Outputs in GitHub Actions
DESCRIPTION: This code shows how to retrieve various types of inputs (string, boolean, multiline) using `getInput`, `getBooleanInput`, and `getMultilineInput`. It also demonstrates how to set an action's output using `setOutput`, making values accessible to subsequent actions.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/core/README.md#_snippet_1

LANGUAGE: javascript
CODE:
```
const myInput = core.getInput('inputName', { required: true });
const myBooleanInput = core.getBooleanInput('booleanInputName', { required: true });
const myMultilineInput = core.getMultilineInput('multilineInputName', { required: true });
core.setOutput('outputKey', 'outputVal');
```

----------------------------------------

TITLE: Registering Secrets in GitHub Actions Logs
DESCRIPTION: This code demonstrates how to use `setSecret` to register a sensitive value with the runner. Once registered, the secret will be automatically masked in the action's logs, preventing accidental exposure.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/core/README.md#_snippet_3

LANGUAGE: javascript
CODE:
```
core.setSecret('myPassword');
```

----------------------------------------

TITLE: Set Step Output in GitHub Actions
DESCRIPTION: This command sets an output variable for the current step, making it accessible to subsequent steps in the workflow. It's useful for passing data between different parts of a job. The output can be accessed via `steps.[step-id].outputs.[output-name]` in YAML.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/commands.md#_snippet_0

LANGUAGE: sh
CODE:
```
echo "::set-output name=FOO::BAR"
```

LANGUAGE: yaml
CODE:
```
steps:
  - name: Set the value
    id: step_one
    run: echo "::set-output name=FOO::BAR"
  - name: Use it
    run: echo ${{ steps.step_one.outputs.FOO }}
```

LANGUAGE: APIDOC
CODE:
```
setOutput(name: string, value: string): void
  name: The name of the output variable.
  value: The value to set for the output variable.
```

----------------------------------------

TITLE: Logging Utilities in GitHub Actions
DESCRIPTION: This comprehensive example showcases various logging functions provided by `@actions/core`, including `debug`, `warning`, `info`, and `error`. It also demonstrates how to check if debug logging is enabled using `isDebug()` and how to emit annotations with `notice`.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/core/README.md#_snippet_6

LANGUAGE: javascript
CODE:
```
const core = require('@actions/core');

const myInput = core.getInput('input');
try {
  core.debug('Inside try block');
  
  if (!myInput) {
    core.warning('myInput was not set');
  }
  
  if (core.isDebug()) {
    // curl -v https://github.com
  } else {
    // curl https://github.com
  }

  // Do stuff
  core.info('Output to the actions build log')

  core.notice('This is a message that will also emit an annotation')
}
catch (err) {
  core.error(`Error ${err}, action may still succeed though`);
}
```

----------------------------------------

TITLE: Complete GitHub Action Logic with Context Access (TypeScript)
DESCRIPTION: The final `src/main.ts` implementation, showing how to retrieve inputs, access GitHub context data (issue details and event action), and conditionally execute logic based on whether an issue or pull request was newly opened.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/github-package.md#_snippet_3

LANGUAGE: typescript
CODE:
```
import * as core from '@actions/core';
import * as github from '@actions/github';

export async function run() {
    try {
    const welcomeMessage: string = core.getInput('welcome-message', {required: true});
    const repoToken: string = core.getInput('repo-token', {required: true});
    const issue: {owner: string; repo: string; number: number} = github.context.issue;

    if (github.context.payload.action !== 'opened') {
      console.log('No issue or pull request was opened, skipping');
      return;
    }

    // TODO - make request to the GitHub API to comment on the issue 
    }
    catch (error) {
      core.setFailed(error.message);
      throw error;
    }
}

run();
```

----------------------------------------

TITLE: Mock GitHub Context in Jest Test (TypeScript)
DESCRIPTION: Demonstrates how to mock the GitHub context for a Jest unit test. It sets `process.env['GITHUB_REPOSITORY']` and `process.env['GITHUB_EVENT_PATH']` to simulate the repository and event payload, enabling comprehensive testing of action logic dependent on the GitHub context.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/github-package.md#_snippet_8

LANGUAGE: ts
CODE:
```
const nock = require('nock');
const path = require('path');

describe('action test suite', () => {
  it('It posts a comment on an opened issue', async () => {
    const welcomeMessage = 'hello';
    const repoToken = 'token';
    process.env['INPUT_WELCOME-MESSAGE'] = welcomeMessage;
    process.env['INPUT_REPO-TOKEN'] = repoToken;

    process.env['GITHUB_REPOSITORY'] = 'foo/bar';
    process.env['GITHUB_EVENT_PATH'] = path.join(__dirname, 'payload.json');

    // TODO
  });
});
```

----------------------------------------

TITLE: Authenticate and make REST API calls with Octokit in JavaScript
DESCRIPTION: This snippet demonstrates how to obtain an authenticated Octokit client using a GitHub token. It then shows an example of making a REST API call to fetch a pull request, highlighting the client's adherence to machine proxy settings and GHES base URL configuration.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/github/README.md#_snippet_0

LANGUAGE: js
CODE:
```
const github = require('@actions/github');
const core = require('@actions/core');

async function run() {
    // This should be a token with access to your repository scoped in as a secret.
    // The YML workflow will need to set myToken with the GitHub Secret Token
    // myToken: ${{ secrets.GITHUB_TOKEN }}
    // https://help.github.com/en/actions/automating-your-workflow-with-github-actions/authenticating-with-the-github_token#about-the-github_token-secret
    const myToken = core.getInput('myToken');

    const octokit = github.getOctokit(myToken)

    // You can also pass in additional options as a second parameter to getOctokit
    // const octokit = github.getOctokit(myToken, {userAgent: "MyActionVersion1"});

    const { data: pullRequest } = await octokit.rest.pulls.get({
        owner: 'octokit',
        repo: 'rest.js',
        pull_number: 123,
        mediaType: {
          format: 'diff'
        }
    });

    console.log(pullRequest);
}

run();
```

----------------------------------------

TITLE: Access GitHub Action context and create issues in JavaScript
DESCRIPTION: This code shows how to retrieve the current GitHub Action's context, which contains information about the repository and event. It then uses this context along with the Octokit client to create a new GitHub issue programmatically.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/github/README.md#_snippet_2

LANGUAGE: js
CODE:
```
const github = require('@actions/github');

const context = github.context;

const newIssue = await octokit.rest.issues.create({
  ...context.repo,
  title: 'New issue!',
  body: 'Hello Universe!'
});
```

----------------------------------------

TITLE: Setting Action Exit Codes for Success/Failure
DESCRIPTION: This example demonstrates how to handle errors and set a failing exit code for a GitHub Action using `core.setFailed`. Wrapping action logic in a try-catch block ensures that any unhandled exceptions are caught, logging the error message and signaling a failure to the runner.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/core/README.md#_snippet_5

LANGUAGE: javascript
CODE:
```
const core = require('@actions/core');

try {
  // Do stuff
}
catch (err) {
  // setFailed logs the message and sets a failing exit code
  core.setFailed(`Action failed with error ${err}`);
}
```

----------------------------------------

TITLE: Mock GitHub Action Inputs in Jest Test (TypeScript)
DESCRIPTION: Illustrates how to mock GitHub Action inputs within a Jest unit test. It sets `process.env['INPUT_WELCOME-MESSAGE']` and `process.env['INPUT_REPO-TOKEN']` to simulate input values, allowing the action to be tested without actual GitHub input.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/github-package.md#_snippet_7

LANGUAGE: ts
CODE:
```
const nock = require('nock');
const path = require('path');

describe('action test suite', () => {
  it('It posts a comment on an opened issue', async () => {
    const welcomeMessage = 'hello';
    const repoToken = 'token';
    process.env['INPUT_WELCOME-MESSAGE'] = welcomeMessage;
    process.env['INPUT_REPO-TOKEN'] = repoToken;

    // TODO
  });
});
```

----------------------------------------

TITLE: Referencing GitHub Actions in Workflows
DESCRIPTION: Shows various methods to reference a GitHub Action in a workflow, including using a major version tag (recommended), a specific semantic version, or an immutable SHA1 hash. This allows control over the action's stability and update behavior.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/action-versioning.md#_snippet_0

LANGUAGE: yaml
CODE:
```
steps:
    - uses: actions/javascript-action@v1        # recommended. starter workflows use this
    - uses: actions/javascript-action@v1.0.0    # if an action offers specific releases 
    - uses: actions/javascript-action@41775a4da8ffae865553a738ab8ac1cd5a3c0044 # sha
```

----------------------------------------

TITLE: Initial GitHub Action Logic in src/main.ts
DESCRIPTION: The foundational TypeScript structure for `src/main.ts`, including imports for `@actions/core` and `@actions/github`, and an asynchronous `run` function with basic error handling, ready for core logic.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/github-package.md#_snippet_2

LANGUAGE: typescript
CODE:
```
import * as core from '@actions/core';
import * as github from '@actions/github';

export async function run() {
    try {
    const welcomeMessage: string = core.getInput('welcome-message');
    // TODO - Get context data

    // TODO - make request to the GitHub API to comment on the issue 
    }
    catch (error) {
      core.setFailed(error.message);
      throw error;
    }
}

run();
```

----------------------------------------

TITLE: Install GitHub Actions Toolkit Dependencies
DESCRIPTION: Instructions to install the necessary `@actions/core` and `@actions/github` packages using npm, which are essential for developing GitHub Actions.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/github-package.md#_snippet_0

LANGUAGE: bash
CODE:
```
npm install @actions/core && npm install @actions/github
```

----------------------------------------

TITLE: Interact with GitHub OIDC Provider
DESCRIPTION: Documents the `getIDToken()` method for obtaining a JWT ID token from the GitHub OIDC provider. This token can be used to acquire access tokens from third-party cloud providers. It details the method's optional `audience` input and its JWT output.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/core/README.md#_snippet_12

LANGUAGE: APIDOC
CODE:
```
Method Name: getIDToken()
Inputs:
  audience : optional
Outputs:
  A JWT ID Token
```

LANGUAGE: JavaScript
CODE:
```
const core = require('@actions/core');
async function getIDTokenAction(): Promise<void> {
  
   const audience = core.getInput('audience', {required: false})
   
   const id_token1 = await core.getIDToken()            // ID Token with default audience
   const id_token2 = await core.getIDToken(audience)    // ID token with custom audience
   
   // this id_token can be used to get access token from third party cloud providers
}
getIDTokenAction()
```

LANGUAGE: YAML
CODE:
```
name: 'GetIDToken'
description: 'Get ID token from Github OIDC provider'
inputs:
  audience:  
    description: 'Audience for which the ID token is intended for'
    required: false
outputs:
  id_token1: 
    description: 'ID token obtained from OIDC provider'
  id_token2: 
    description: 'ID token obtained from OIDC provider'
runs:
  using: 'node12'
  main: 'dist/index.js'
```

----------------------------------------

TITLE: Save Cache using @actions/cache
DESCRIPTION: This snippet demonstrates how to save a cache containing specified files using a unique key with the `@actions/cache` package. Files are compressed using zstandard or gzip. The function returns the cache ID upon successful saving and throws an error if the upload fails.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/cache/README.md#_snippet_0

LANGUAGE: javascript
CODE:
```
const cache = require('@actions/cache');
const paths = [
    'node_modules',
    'packages/*/node_modules/'
]
const key = 'npm-foobar-d5ea0750'
const cacheId = await cache.saveCache(paths, key)
```

----------------------------------------

TITLE: Docker Action Entrypoint Script
DESCRIPTION: This Bash script serves as the entry point for a Docker action. It demonstrates how to access an input argument passed to the action, printing a 'hello' message followed by the first argument.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/container-action.md#_snippet_2

LANGUAGE: bash
CODE:
```
#!/bin/sh -l

echo "hello $1"
```

----------------------------------------

TITLE: GitHub Actions Workflow for Multi-Environment Node.js Testing
DESCRIPTION: This YAML workflow demonstrates how to test a Node.js library across multiple Node.js versions and operating systems using a JavaScript action. It utilizes a matrix strategy to run jobs on different environments, sets up Node.js using 'actions/setup-node', and then executes npm commands and a custom action.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/action-types.md#_snippet_0

LANGUAGE: yaml
CODE:
```
on: push

jobs:
  build:
    strategy: 
      matrix:
        node: [8.x, 10.x]
        os: [ubuntu-16.04, windows-2019]
    runs-on: ${{matrix.os}}
    actions:
    - uses: actions/setup-node@v4
      with:
        version: ${{matrix.node}}
    - run: |
        npm install
    - run: |
        npm test
    - uses: actions/custom-action@v1
```

----------------------------------------

TITLE: Updating Major Version Tag for GitHub Actions
DESCRIPTION: Provides Git commands to update a major version tag (e.g., `v1`) to point to the latest stable release's reference. This ensures that users who bind to the major version tag automatically receive the most recent stable minor and patch updates, maintaining compatibility.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/action-versioning.md#_snippet_2

LANGUAGE: bash
CODE:
```
git tag -fa v1 -m "Update v1 tag"
git push origin v1 --force
```

----------------------------------------

TITLE: Walkthrough for a Comprehensive TypeScript Action
DESCRIPTION: This walkthrough guides through creating a TypeScript Action, covering compilation, testing, linting, workflow integration, publishing, and versioning. It demonstrates importing core toolkit functionalities and handling action inputs. The included test output confirms the successful execution of the action's unit tests.
SOURCE: https://github.com/actions/toolkit/blob/main/README.md#_snippet_12

LANGUAGE: javascript
CODE:
```
import * as core from '@actions/core';\n\nasync function run() {\n  try {\n    const ms = core.getInput('milliseconds');\n    console.log(`Waiting ${ms} milliseconds ...`)\n    ...
```

LANGUAGE: javascript
CODE:
```
PASS ./index.test.js\n  ✓ throws invalid number\n  ✓ wait 500 ms\n  ✓ test runs\n\nTest Suites: 1 passed, 1 total\nTests:       3 passed, 3 total
```

----------------------------------------

TITLE: Upload and Download GitHub Actions Artifact with Retention
DESCRIPTION: Illustrates the complete process of uploading files to a named artifact, specifying retention days, and subsequently downloading the artifact by its ID to a specified path. This example highlights basic artifact management.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/artifact/README.md#_snippet_3

LANGUAGE: js
CODE:
```
const {id, size} = await artifact.uploadArtifact(
  // name of the artifact
  'my-artifact',
  // files to include (supports absolute and relative paths)
  ['/absolute/path/file1.txt', './relative/file2.txt'],
  {
    // optional: how long to retain the artifact
    // if unspecified, defaults to repository/org retention settings (the limit of this value)
    retentionDays: 10
  }
)

console.log(`Created artifact with id: ${id} (bytes: ${size}`)

const {downloadPath} = await artifact.downloadArtifact(id, {
  // optional: download destination path. otherwise defaults to $GITHUB_WORKSPACE
  path: '/tmp/dst/path',
})

console.log(`Downloaded artifact ${id} to: ${downloadPath}`)
```

----------------------------------------

TITLE: Define GitHub Action Inputs in action.yml
DESCRIPTION: YAML configuration for `action.yml` that defines the action's name, description, author, and two inputs: `welcome-message` (with a default) and `repo-token` (required).
SOURCE: https://github.com/actions/toolkit/blob/main/docs/github-package.md#_snippet_1

LANGUAGE: yaml
CODE:
```
name: "Welcome"
description: "A basic welcome action"
author: "GitHub"
inputs:
  welcome-message:
    description: "Message to display when a user opens an issue or PR"
    default: "Thanks for opening an issue! Make sure you've followed CONTRIBUTING.md"
  repo-token:
    description: "Token for the repo. Can be passed in using {{ secrets.GITHUB_TOKEN }}"
    required: true
runs:
  using: "node12"
  main: "lib/main.js"
```

----------------------------------------

TITLE: Basic command execution with @actions/exec
DESCRIPTION: Demonstrates the fundamental usage of `@actions/exec` to run a simple command, providing cross-platform compatibility.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/exec/README.md#_snippet_0

LANGUAGE: javascript
CODE:
```
const exec = require('@actions/exec');

await exec.exec('node index.js');
```

----------------------------------------

TITLE: Emitting Annotations in GitHub Actions
DESCRIPTION: This snippet demonstrates how to use `core.error`, `core.warning`, and `core.notice` to create annotations that surface in the GitHub Actions UI and Pull Requests. These annotations provide visual cues for different severity levels of messages.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/core/README.md#_snippet_8

LANGUAGE: javascript
CODE:
```
core.error('This is a bad error, action may still succeed though.')

core.warning('Something went wrong, but it\'s not bad enough to fail the build.')

core.notice('Something happened that you might want to know about.')
```

----------------------------------------

TITLE: Restore Cache using @actions/cache
DESCRIPTION: This snippet illustrates how to restore a cache based on a primary key and optional fallback keys to specified paths using the `@actions/cache` package. The function returns the exact cache key if a cache hit is found, otherwise it returns undefined if no matching cache is located.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/cache/README.md#_snippet_1

LANGUAGE: javascript
CODE:
```
const cache = require('@actions/cache');
const paths = [
    'node_modules',
    'packages/*/node_modules/'
]
const key = 'npm-foobar-d5ea0750'
const restoreKeys = [
    'npm-foobar-',
    'npm-'
]
const cacheKey = await cache.restoreCache(paths, key, restoreKeys)
```

----------------------------------------

TITLE: Exporting Environment Variables for GitHub Actions
DESCRIPTION: This snippet illustrates how to use `exportVariable` to add a variable to the environment block of the current and future steps within a GitHub Actions job. This ensures that the variable is accessible across different processes.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/core/README.md#_snippet_2

LANGUAGE: javascript
CODE:
```
core.exportVariable('envVar', 'Val');
```

----------------------------------------

TITLE: Upload Workflow Artifact API
DESCRIPTION: This function uploads an artifact to the current workflow run. It requires the artifact's name, a list of file paths to upload, and the root directory from which the file paths are relative. Optional parameters allow for further customization of the upload process.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/artifact/docs/generated/classes/DefaultArtifactClient.md#_snippet_6

LANGUAGE: APIDOC
CODE:
```
uploadArtifact(name, files, rootDirectory, options?): Promise<UploadArtifactResponse>

Parameters:
  name: string
    Description: The name of the artifact, required
  files: string[]
    Description: A list of absolute or relative paths that denote what files should be uploaded
  rootDirectory: string
    Description: An absolute or relative file path that denotes the root parent directory of the files being uploaded
  options?: UploadArtifactOptions
    Description: Extra options for customizing the upload behavior

Returns:
  Promise<UploadArtifactResponse>
    Description: single UploadArtifactResponse object

Implementation of: ArtifactClient.uploadArtifact
Defined in: src/internal/client.ts:113
```

----------------------------------------

TITLE: Emit Log Messages at Different Levels
DESCRIPTION: These commands allow you to emit messages to the workflow logs with specific severity levels: debug, notice, warning, and error. This helps categorize log output and can trigger different UI treatments in GitHub Actions. Additional syntax options are available for more detailed messages.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/commands.md#_snippet_5

LANGUAGE: sh
CODE:
```
echo "::debug::My debug message"
```

LANGUAGE: sh
CODE:
```
echo "::notice::My notice message"
```

LANGUAGE: sh
CODE:
```
echo "::warning::My warning message"
```

LANGUAGE: sh
CODE:
```
echo "::error::My error message"
```

----------------------------------------

TITLE: Complete GitHub Action to Welcome New Issues/PRs (TypeScript)
DESCRIPTION: Provides the full TypeScript code for a GitHub Action that welcomes new issues or pull requests. It retrieves a welcome message and repository token from inputs, checks if an issue/PR was opened, and then uses Octokit to post a welcome comment. Includes error handling.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/github-package.md#_snippet_5

LANGUAGE: ts
CODE:
```
import * as core from '@actions/core';
import * as github from '@actions/github';

export async function run() {
    try {
    const welcomeMessage: string = core.getInput('welcome-message', {required: true});
    const repoToken: string = core.getInput('repo-token', {required: true});
    const issue: {owner: string; repo: string; number: number} = github.context.issue;

    if (github.context.payload.action !== 'opened') {
      console.log('No issue or pull request was opened, skipping');
      return;
    }

    const client: github.GitHub = new github.GitHub(repoToken);
    await client.issues.createComment({
      owner: issue.owner,
      repo: issue.repo,
      issue_number: issue.number,
      body: welcomeMessage
    });
    }
    catch (error) {
      core.setFailed(error.message);
      throw error;
    }
}

run();
```

----------------------------------------

TITLE: Populating Job Summary with core.summary Content Methods
DESCRIPTION: Demonstrates various `core.summary` methods for adding different types of content to the GitHub Actions job summary buffer, including raw text, end-of-line markers, code blocks, lists, collapsible details, images, headings, separators, line breaks, quotes, and links. All methods, except `addRaw()`, internally use `addRaw()` followed by `addEOL()`.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/core/README.md#_snippet_15

LANGUAGE: typescript
CODE:
```
// Write raw text, optionally add an EOL after the content, defaults to false
core.summary.addRaw('Some content here :speech_balloon:', true)
// Output: Some content here :speech_balloon:\n
// Add an operating system-specific end-of-line marker
core.summary.addEOL()
// Output (POSIX): \n
// Output (Windows): \r\n
// Add a codeblock with an optional language for syntax highlighting
core.summary.addCodeBlock('console.log(\'hello world\')', 'javascript')
// Output: <pre lang="javascript"><code>console.log('hello world')</code></pre>

// Add a list, second parameter indicates if list is ordered, defaults to false
core.summary.addList(['item1','item2','item3'], true)
// Output: <ol><li>item1</li><li>item2</li><li>item3</li></ol>

// Add a collapsible HTML details element
core.summary.addDetails('Label', 'Some detail that will be collapsed')
// Output: <details><summary>Label</summary>Some detail that will be collapsed</details>

// Add an image, image options parameter is optional, you can supply one of or both width and height in pixels
core.summary.addImage('example.png', 'alt description of img', {width: '100', height: '100'})
// Output: <img src="example.png" alt="alt description of img" width="100" height="100">

// Add an HTML section heading element, optionally pass a level that translates to 'hX' ie. h2. Defaults to h1
core.summary.addHeading('My Heading', '2')
// Output: <h2>My Heading</h2>

// Add an HTML thematic break <hr>
core.summary.addSeparator()
// Output: <hr>

// Add an HTML line break <br>
core.summary.addBreak()
// Output: <br>

// Add an HTML blockquote with an optional citation
core.summary.addQuote('To be or not to be', 'Shakespeare')
// Output: <blockquote cite="Shakespeare">To be or not to be</blockquote>

// Add an HTML anchor tag
core.summary.addLink('click here', 'https://github.com')
// Output: <a href="https://github.com">click here</a>
```

----------------------------------------

TITLE: Set Environment Variable in Shell
DESCRIPTION: This example shows how to set a simple environment variable `FOO` to `BAR` for subsequent steps in a workflow. The value is appended to the file specified by the `GITHUB_ENV` environment variable, making it available to future out-of-process steps.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/commands.md#_snippet_8

LANGUAGE: sh
CODE:
```
echo "FOO=BAR" >> $GITHUB_ENV
```

----------------------------------------

TITLE: Send Comment to GitHub Issue/PR using Octokit (TypeScript)
DESCRIPTION: Demonstrates how to use the Octokit REST client in TypeScript to create a comment on a GitHub issue or pull request. It requires an authenticated `repoToken` and the `owner`, `repo`, `issue_number`, and `body` of the comment.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/github-package.md#_snippet_4

LANGUAGE: ts
CODE:
```
const client: github.GitHub = new github.GitHub(repoToken);
await client.issues.createComment({
  owner: issue.owner,
  repo: issue.repo,
  issue_number: issue.number,
  body: welcomeMessage
});
```

----------------------------------------

TITLE: Group and Ungroup Log Lines in GitHub Actions
DESCRIPTION: These commands allow you to create collapsible regions in the workflow logs, improving readability for large outputs. `::group::` starts a new collapsible section with a given title, and `::endgroup::` closes the most recently opened group.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/commands.md#_snippet_2

LANGUAGE: bash
CODE:
```
echo "::group::my title"   
echo "::endgroup::"
```

LANGUAGE: APIDOC
CODE:
```
startGroup(name: string): void
  name: The title of the log group.
endGroup(): void
```

----------------------------------------

TITLE: Install @actions/core package
DESCRIPTION: Installs the `@actions/core` package, which provides essential functions for handling inputs, outputs, results, logging, secrets, and variables within GitHub Actions.
SOURCE: https://github.com/actions/toolkit/blob/main/README.md#_snippet_0

LANGUAGE: bash
CODE:
```
npm install @actions/core
```

----------------------------------------

TITLE: Reference Docker Action in Workflow
DESCRIPTION: This snippet demonstrates how users reference a Docker action in their GitHub Actions workflow file using the 'using' keyword, pointing to the action's repository and version.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/container-action.md#_snippet_0

LANGUAGE: yaml
CODE:
```
steps:
    using: actions/setup-node@v4
```

----------------------------------------

TITLE: Importing @actions/core Package
DESCRIPTION: This snippet demonstrates how to import the `@actions/core` package in both JavaScript and TypeScript environments, making its core functionalities available for use within a GitHub Action.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/core/README.md#_snippet_0

LANGUAGE: javascript
CODE:
```
const core = require('@actions/core');
```

LANGUAGE: typescript
CODE:
```
import * as core from '@actions/core';
```

----------------------------------------

TITLE: Perform GraphQL queries with Octokit in JavaScript
DESCRIPTION: This example illustrates how to execute GraphQL queries using the authenticated Octokit client. It provides a concise demonstration of passing a query and variables to the `octokit.graphql` method.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/github/README.md#_snippet_1

LANGUAGE: js
CODE:
```
const result = await octokit.graphql(query, variables);
```

----------------------------------------

TITLE: Define Multi-Line Problem Matcher for ESLint Stylish Output
DESCRIPTION: Defines a JSON problem matcher configuration for multi-line ESLint stylish output. It uses a two-pattern approach: the first pattern captures the file name, and the second pattern, utilizing `loop: true`, iteratively captures multiple error/warning lines associated with that file, enabling multiple annotations from a single file header.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/problem-matchers.md#_snippet_2

LANGUAGE: json
CODE:
```
{
    "problemMatcher": [
        {
            "owner": "eslint-stylish",
            "pattern": [
                {
                    "regexp": "^([^\s].*)$",
                    "file": 1
                },
                {
                    "regexp": "^\s+(\d+):(\d+)\s+(error|warning|info)\s+(.*)\s\s+(.*)$",
                    "line": 1,
                    "column": 2,
                    "severity": 3,
                    "message": 4,
                    "code": 5,
                    "loop": true
                }
            ]
        }
    ]
}
```

----------------------------------------

TITLE: Convert Filesystem Paths Across OS
DESCRIPTION: Provides examples for `toPosixPath`, `toWin32Path`, and `toPlatformPath` functions, which facilitate converting file paths between Posix (Linux) and Windows styles, and adapting paths to the runner's native operating system.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/core/README.md#_snippet_13

LANGUAGE: JavaScript
CODE:
```
toPosixPath('\\foo\\bar') // => /foo/bar
toWin32Path('/foo/bar') // => \\foo\\bar
```

LANGUAGE: JavaScript
CODE:
```
// On a Windows runner.
toPlatformPath('/foo/bar') // => \\foo\\bar

// On a Linux runner.
toPlatformPath('\\foo\\bar') // => /foo/bar
```

----------------------------------------

TITLE: Capturing output and configuring options with @actions/exec
DESCRIPTION: Shows how to capture standard output and error streams, and set various execution options like the current working directory, using listeners and an options object with `@actions/exec`.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/exec/README.md#_snippet_2

LANGUAGE: javascript
CODE:
```
const exec = require('@actions/exec');

let myOutput = '';
let myError = '';

const options = {};
options.listeners = {
  stdout: (data) => {
    myOutput += data.toString();
  },
  stderr: (data) => {
    myError += data.toString();
  }
};
options.cwd = './lib';

await exec.exec('node', ['index.js', 'foo=bar'], options);
```

----------------------------------------

TITLE: Type GitHub webhook payloads using `@octokit/webhooks-definitions` in TypeScript
DESCRIPTION: This snippet demonstrates how to enhance type safety for GitHub webhook payloads by using the `@octokit/webhooks-definitions` npm module. It shows how to install the module and assert the payload type based on the `eventName` for specific event structures like `PushEvent`.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/github/README.md#_snippet_3

LANGUAGE: ts
CODE:
```
import * as core from '@actions/core'
import * as github from '@actions/github'
import {PushEvent} from '@octokit/webhooks-definitions/schema'

if (github.context.eventName === 'push') {
  const pushPayload = github.context.payload as PushEvent
  core.info(`The head commit is: ${pushPayload.head_commit}`)
}
```

----------------------------------------

TITLE: Generate SLSA Provenance Attestation with `attestProvenance` (JavaScript)
DESCRIPTION: Illustrates how to use the `attestProvenance` function to create a build provenance attestation for an artifact. It automatically populates a SLSA provenance predicate with metadata from the GitHub Actions run. A GitHub token and the artifact's name and digest are required.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/attest/README.md#_snippet_3

LANGUAGE: javascript
CODE:
```
const { attestProvenance } = require('@actions/attest');
const core = require('@actions/core');

async function run() {
    // In order to persist attestations to the repo, this should be a token with
    // repository write permissions.
    const ghToken = core.getInput('gh-token');

    const attestation = await attestProvenance({
        subjectName: 'my-artifact-name',
        subjectDigest: { 'sha256': '36ab4667...'},
        token: ghToken
    });

    console.log(attestation);
}

run();
```

----------------------------------------

TITLE: Mask Secrets in GitHub Actions Logs
DESCRIPTION: This command registers a value as a secret with the runner, causing it to be masked (replaced with asterisks) in all subsequent log output. This prevents sensitive information from being exposed in build logs. It supports single-line or escaped multi-line secrets.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/commands.md#_snippet_1

LANGUAGE: sh
CODE:
```
echo "::add-mask::mysecretvalue"
```

LANGUAGE: APIDOC
CODE:
```
setSecret(secret: string): void
  secret: The string value to mask in the logs.
```

LANGUAGE: sh
CODE:
```
echo "::add-mask::first%0Asecond%0D%0Athird"
```

----------------------------------------

TITLE: Specify GitHub Actions Artifact Versions in Workflow
DESCRIPTION: This YAML snippet demonstrates how to specify the version of the `actions/upload-artifact` and `actions/download-artifact` actions within a GitHub Actions workflow file. It is crucial to use matching versions of these actions to ensure compatibility and proper functionality.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/artifact/docs/faq.md#_snippet_0

LANGUAGE: yaml
CODE:
```
  uses: actions/upload-artifact@v4
  # ...
  uses: actions/download-artifact@v4
  # ...
```

----------------------------------------

TITLE: Prepend to PATH in Shell
DESCRIPTION: This command demonstrates how to prepend a new directory path (`/Users/test/.nvm/versions/node/v12.18.3/bin`) to the system's `PATH` environment variable. By appending the path to the file specified by `GITHUB_PATH`, the directory becomes accessible for command execution in subsequent workflow steps.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/commands.md#_snippet_12

LANGUAGE: sh
CODE:
```
echo "/Users/test/.nvm/versions/node/v12.18.3/bin" >> $GITHUB_PATH
```

----------------------------------------

TITLE: Discouraged: Referencing `main` Branch for GitHub Actions
DESCRIPTION: Illustrates the anti-pattern of referencing the `main` branch for a GitHub Action. This practice is strongly discouraged because the `main` branch contains the latest, potentially unstable, and breaking changes, which can lead to unexpected workflow failures.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/action-versioning.md#_snippet_1

LANGUAGE: yaml
CODE:
```
steps:
    - uses: actions/javascript-action@main  # do not do this
```

----------------------------------------

TITLE: Retrieve GitHub Actions Endpoints for Firewall Configuration
DESCRIPTION: Provides a `curl` command to fetch the list of GitHub Actions domain endpoints from the GitHub Meta API, essential for configuring firewall rules for self-hosted runners.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/artifact/README.md#_snippet_4

LANGUAGE: bash
CODE:
```
curl https://api.github.com/meta | jq .domains.actions
```

----------------------------------------

TITLE: Adding HTML Tables to Job Summary with core.summary.addTable()
DESCRIPTION: Illustrates how to use the `core.summary.addTable()` method to add an HTML table to the job summary. This example demonstrates structuring table data using the `SummaryTableRow` and `SummaryTableCell` types, including header cells.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/core/README.md#_snippet_17

LANGUAGE: typescript
CODE:
```
const tableData = [
  {data: 'Header1', header: true},
  {data: 'Header2', header: true},
  {data: 'Header3', header: true},
  {data: 'MyData1'},
  {data: 'MyData2'},
  {data: 'MyData3'}
]

// Add an HTML table
core.summary.addTable([tableData])
// Output: <table><tr><th>Header1</th><th>Header2</th><th>Header3</th></tr><tr></tr><td>MyData1</td><td>MyData2</td><td>MyData3</td></tr></table>
```

----------------------------------------

TITLE: Create a Docker Container Action Using Octokit
DESCRIPTION: This example demonstrates building a Docker container action that leverages the GitHub Actions Toolkit and Octokit. The Dockerfile sets up a Node.js environment for the action. The JavaScript code within the container shows how to access action inputs and retrieve GitHub context data, such as repository information, using the Octokit client.
SOURCE: https://github.com/actions/toolkit/blob/main/README.md#_snippet_14

LANGUAGE: docker
CODE:
```
FROM node:slim\nCOPY . .\nRUN npm install --production\nENTRYPOINT ["node", "/lib/main.js"]
```

LANGUAGE: javascript
CODE:
```
const myInput = core.getInput('myInput');\ncore.debug(`Hello ${myInput} from inside a container`);\n\nconst context = github.context;\nconsole.log(`We can even get context data, like the repo: ${context.repo.repo}`)
```

----------------------------------------

TITLE: GitHub Actions Core: exportVariable API
DESCRIPTION: Documents the `exportVariable` function from the `@actions/core` library. This function is used to set an environment variable, making it available not only for future out-of-process steps but also updating it for the current step's process.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/commands.md#_snippet_11

LANGUAGE: APIDOC
CODE:
```
export function exportVariable(name: string, val: string): void {}
```

----------------------------------------

TITLE: Core Library API Specifications
DESCRIPTION: Defines core functions for interacting with the GitHub Actions runner and environment, including logging, environment variable management, path manipulation, input retrieval, and action status setting.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/specs/package-specs.md#_snippet_0

LANGUAGE: APIDOC
CODE:
```
Core Library API:
  Functions:
    debug(message: string): void
      Description: Logging function.
    warning(message: string): void
      Description: Logging function.
    error(message: string): void
      Description: Logging function.
    exportVariable(name: string, val: string): void
      Description: Sets an environment variable for the current and future actions in the job.
      Parameters:
        name: The name of the variable to set.
        val: The value of the variable.
    exportSecret(name: string, val: string): void
      Description: Exports a variable and registers it as a secret, masking it from logs.
      Parameters:
        name: The name of the variable to set.
        val: Value of the secret.
    addPath(inputPath: string): void
      Description: Prepends inputPath to the system's PATH environment variable.
      Parameters:
        inputPath: The path to add.
    getInput(name: string, options?: InputOptions): string | undefined
      Description: Gets the value of an input, which is also trimmed.
      Parameters:
        name: Name of the input to get.
        options: Optional. See InputOptions.
      Returns: string | undefined
    setNeutral(message: string): void
      Description: Sets the status of the action to neutral.
      Parameters:
        message: The status message.
    setFailed(message: string): void
      Description: Sets the status of the action to failed.
      Parameters:
        message: The status message.
  Interfaces:
    InputOptions:
      Description: Options for getInput.
      Properties:
        required?: bool
          Description: Optional. Whether the input is required. If required and not present, will throw. Defaults to false.
```

----------------------------------------

TITLE: GitHub Actions Core: addPath API
DESCRIPTION: Documents the `addPath` function from the `@actions/core` library. This function provides a programmatic way to prepend a given `inputPath` to the system's `PATH` environment variable, similar to writing directly to `GITHUB_PATH`.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/commands.md#_snippet_13

LANGUAGE: APIDOC
CODE:
```
export function addPath(inputPath: string): void {}
```

----------------------------------------

TITLE: Define Single-Line Problem Matcher for ESLint Compact Output
DESCRIPTION: Defines a JSON problem matcher configuration to detect and parse single-line ESLint compact output. It uses a regular expression to extract file, line, column, severity, message, and error code from the log entry, creating annotations in the GitHub Actions UI.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/problem-matchers.md#_snippet_0

LANGUAGE: json
CODE:
```
{
    "problemMatcher": [
        {
            "owner": "eslint-compact",
            "pattern": [
                {
                    "regexp": "^(.+):\sline\s(\d+),\scol\s(\d+),\s(Error|Warning|Info)\s-\s(.+)\s\((.+)\)$",
                    "file": 1,
                    "line": 2,
                    "column": 3,
                    "severity": 4,
                    "message": 5,
                    "code": 6
                }
            ]
        }
    ]
}
```

----------------------------------------

TITLE: Managing Job Summary Buffer with core.summary Utility Functions
DESCRIPTION: Provides examples of utility functions available in `core.summary` for managing the job summary buffer. These methods allow clearing the buffer and file, retrieving buffer content as a string, checking if the buffer is empty, resetting the buffer without writing, and writing the buffer content to the summary file with an optional overwrite.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/core/README.md#_snippet_18

LANGUAGE: typescript
CODE:
```
// Empties the summary buffer AND wipes the summary file on disk
core.summary.clear()

// Returns the current summary buffer as a string
core.summary.stringify()

// If the summary buffer is empty
core.summary.isEmptyBuffer()

// Resets the summary buffer without writing to the summary file on disk
core.summary.emptyBuffer()

// Writes text in the buffer to the summary buffer file and empties the buffer, optionally overwriting all existing content in the summary file with buffer contents. Defaults to false.
core.summary.write({overwrite: true})
```

----------------------------------------

TITLE: Generic Heredoc Syntax for Environment Variables
DESCRIPTION: This snippet outlines the general heredoc syntax for defining multiline environment variables within GitHub Actions workflows. It specifies the structure for wrapping a variable's value between a chosen delimiter, which is then written to the `GITHUB_ENV` file.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/commands.md#_snippet_10

LANGUAGE: text
CODE:
```
{VARIABLE_NAME}<<{DELIMETER}
{VARIABLE_VALUE}
{DELIMETER}
```

----------------------------------------

TITLE: Mocking Octokit Client with Nock and Running a Test
DESCRIPTION: Illustrates how to use `nock` to mock an HTTP POST request to the GitHub API for creating an issue comment. This snippet also includes a full test suite setup for a GitHub Action, demonstrating environment variable setup and asynchronous test execution.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/github-package.md#_snippet_11

LANGUAGE: javascript
CODE:
```
const nock = require('nock');
const path = require('path');

describe('action test suite', () => {
  it('It posts a comment on an opened issue', async () => {
    const welcomeMessage = 'hello';
    const repoToken = 'token';
    process.env['INPUT_WELCOME-MESSAGE'] = welcomeMessage;
    process.env['INPUT_REPO-TOKEN'] = repoToken;

    process.env['GITHUB_REPOSITORY'] = 'foo/bar';
    process.env['GITHUB_EVENT_PATH'] = path.join(__dirname, 'payload.json');

    nock('https://api.github.com')
      .persist()
      .post('/repos/foo/bar/issues/10/comments', '{\"body\":\"hello\"}')
      .reply(200);
      
    const main = require('../src/main');

    await main.run();
  });
});
```

----------------------------------------

TITLE: Copy and Move Files/Folders with @actions/io
DESCRIPTION: Illustrates how to copy or move files and folders using `io.cp` and `io.mv`. The `cp` function supports options like `recursive` for directories and `force` for overwriting, similar to standard Unix `cp` and `mv` commands. It's essential for managing file locations within a project.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/io/README.md#_snippet_1

LANGUAGE: js
CODE:
```
const io = require('@actions/io');

// Recursive must be true for directories
const options = { recursive: true, force: false }

await io.cp('path/to/directory', 'path/to/dest', options);
await io.mv('path/to/file', 'path/to/dest');
```

----------------------------------------

TITLE: Optimize Large Artifact Uploads with Compression Level
DESCRIPTION: Provides guidance on speeding up uploads of large files or uncompressible file types by adjusting the artifact archive's compression level. This is a trade-off between upload time and stored data size, with options ranging from no compression to best compression.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/artifact/README.md#_snippet_8

LANGUAGE: ts
CODE:
```
await artifact.uploadArtifact('my-massive-artifact', ['big_file.bin'], {
  // The level of compression for Zlib to be applied to the artifact archive.
  // - 0: No compression
  // - 1: Best speed
  // - 6: Default compression (same as GNU Gzip)
  // - 9: Best compression
  compressionLevel: 0
})

```

----------------------------------------

TITLE: Passing arguments to commands with @actions/exec
DESCRIPTION: Illustrates how to provide an array of arguments to a command executed using `@actions/exec`, allowing for flexible command line interactions.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/exec/README.md#_snippet_1

LANGUAGE: javascript
CODE:
```
const exec = require('@actions/exec');

await exec.exec('node', ['index.js', 'foo=bar']);
```

----------------------------------------

TITLE: Example Octokit Client Call for Creating a Comment
DESCRIPTION: Demonstrates a typical Octokit client call to create a comment on a GitHub issue. This call is the target for mocking in a test environment.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/github-package.md#_snippet_10

LANGUAGE: typescript
CODE:
```
client.issues.createComment({
  owner: 'foo',
  repo: 'bar',
  issue_number: 10,
  body: 'you posted your first issue'
});
```

----------------------------------------

TITLE: Save and Retrieve State in GitHub Actions
DESCRIPTION: Illustrates how to use `core.saveState` and `core.getState` to persist and retrieve information between different steps or jobs within a GitHub Action, specifically between the `main` and `post` (cleanup) phases of a wrapper action.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/core/README.md#_snippet_11

LANGUAGE: YAML
CODE:
```
name: 'Wrapper action sample'
inputs:
  name:
    default: 'GitHub'
runs:
  using: 'node12'
  main: 'main.js'
  post: 'cleanup.js'
```

LANGUAGE: JavaScript
CODE:
```
const core = require('@actions/core');

core.saveState("pidToKill", 12345);
```

LANGUAGE: JavaScript
CODE:
```
const core = require('@actions/core');

var pid = core.getState("pidToKill");

process.kill(pid);
```

----------------------------------------

TITLE: Download Tool using @actions/tool-cache
DESCRIPTION: Demonstrates how to download a file from a URL using `tc.downloadTool`. This function fetches the content and saves it to a temporary location.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/tool-cache/README.md#_snippet_0

LANGUAGE: js
CODE:
```
const tc = require('@actions/tool-cache');

const node12Path = await tc.downloadTool('https://nodejs.org/dist/v12.7.0/node-v12.7.0-linux-x64.tar.gz');
```

----------------------------------------

TITLE: Instantiate DefaultArtifactClient for Artifact Operations
DESCRIPTION: Initializes a new instance of `DefaultArtifactClient` to perform artifact upload, download, and deletion operations within GitHub Actions workflows.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/artifact/README.md#_snippet_2

LANGUAGE: js
CODE:
```
const artifact = new DefaultArtifactClient()
```

----------------------------------------

TITLE: Iterate Glob Search Results (JavaScript)
DESCRIPTION: Illustrates how to use `globGenerator()` to iterate over a large number of search results asynchronously, processing files one by one.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/glob/README.md#_snippet_2

LANGUAGE: js
CODE:
```
const glob = require('@actions/glob');

const globber = await glob.create('**')
for await (const file of globber.globGenerator()) {
  console.log(file)
}
```

----------------------------------------

TITLE: Save State for GitHub Actions Pre/Post Actions
DESCRIPTION: This command saves a key-value pair as state, making it available as an environment variable (`STATE_[NAME]`) to subsequent `main` or `post` actions within the same job. This is useful for persisting data across different phases of an action's execution.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/commands.md#_snippet_4

LANGUAGE: bash
CODE:
```
echo "::save-state name=FOO::foovalue"
```

----------------------------------------

TITLE: Create a Basic Docker Container Action
DESCRIPTION: This snippet illustrates how to create a GitHub Action delivered as a Docker container. It defines a simple Dockerfile that copies necessary files and sets the entrypoint for the action. This approach allows actions to run in an isolated environment using Docker.
SOURCE: https://github.com/actions/toolkit/blob/main/README.md#_snippet_13

LANGUAGE: docker
CODE:
```
FROM alpine:3.10\nCOPY LICENSE README.md /\nCOPY entrypoint.sh /entrypoint.sh\nENTRYPOINT ["/entrypoint.sh"]
```

----------------------------------------

TITLE: Locate Tool Path with @actions/io
DESCRIPTION: Demonstrates how to find the full path to an executable tool using `io.which`. This function resolves the tool's location via system paths, similar to the `which` command, and can be used to ensure a tool is available or to execute it with its absolute path.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/io/README.md#_snippet_3

LANGUAGE: js
CODE:
```
const exec = require('@actions/exec');
const io = require('@actions/io');

const pythonPath: string = await io.which('python', true)

await exec.exec(`"${pythonPath}"`, ['main.py']);
```

----------------------------------------

TITLE: Set Multiline Environment Variable with Heredoc in Workflow
DESCRIPTION: This workflow step illustrates how to set a multiline environment variable, `JSON_RESPONSE`, using a heredoc-style syntax. The content of a `curl` request to `https://httpbin.org/json` is captured and written to `GITHUB_ENV` between `EOF` delimiters, making the full JSON response available as an environment variable.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/commands.md#_snippet_9

LANGUAGE: sh
CODE:
```
echo 'JSON_RESPONSE<<EOF' >> $GITHUB_ENV
curl https://httpbin.org/json >> $GITHUB_ENV
echo 'EOF' >> $GITHUB_ENV
```

----------------------------------------

TITLE: Download and List Artifacts from Other Workflow Runs or Repositories
DESCRIPTION: Explains how to download or list artifacts from different workflow runs or repositories. This requires elevating permissions by providing a GitHub token with `actions:read` permissions and specifying `findBy` options for `downloadArtifact`, `getArtifact`, and `listArtifacts`.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/artifact/README.md#_snippet_7

LANGUAGE: ts
CODE:
```
const findBy = {
  // must have actions:read permission on target repository
  token: process.env['GITHUB_TOKEN'],
  workflowRunId: 123,
  repositoryOwner: 'actions',
  repositoryName: 'toolkit'
}

await artifact.downloadArtifact(1337, {
  findBy
})

// can also be used in other methods

await artifact.getArtifact('my-artifact', {
  findBy
})

await artifact.listArtifacts({
  findBy
})

```

----------------------------------------

TITLE: Cache Extracted Directory and Add to System Path
DESCRIPTION: Illustrates how to cache an extracted directory using `tc.cacheDir` for reuse across runs or for self-hosted runners. It also shows how to add the cached path to the system's PATH environment variable using `@actions/core.addPath`.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/tool-cache/README.md#_snippet_2

LANGUAGE: js
CODE:
```
const tc = require('@actions/tool-cache');
const core = require('@actions/core');

const node12Path = await tc.downloadTool('https://nodejs.org/dist/v12.7.0/node-v12.7.0-linux-x64.tar.gz');
const node12ExtractedFolder = await tc.extractTar(node12Path, 'path/to/extract/to');

const cachedPath = await tc.cacheDir(node12ExtractedFolder, 'node', '12.7.0');
core.addPath(cachedPath);
```

----------------------------------------

TITLE: Find Cached Tool Directory and Add to Path
DESCRIPTION: Shows how to locate a previously cached tool directory using `tc.find` by specifying the tool name, version, and architecture. The found directory can then be added to the system's PATH.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/tool-cache/README.md#_snippet_4

LANGUAGE: js
CODE:
```
const tc = require('@actions/tool-cache');
const core = require('@actions/core');

const nodeDirectory = tc.find('node', '12.x', 'x64');
core.addPath(nodeDirectory);
```

----------------------------------------

TITLE: Build Project
DESCRIPTION: Executes the build script defined in `package.json` to compile or transpile the project's source code, preparing it for distribution or use.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/http-client/README.md#_snippet_3

LANGUAGE: shell
CODE:
```
npm run build
```

----------------------------------------

TITLE: Set Output Variable in CMD
DESCRIPTION: This snippet demonstrates how to set an output variable named `FOO` with the value `BAR` using the `::set-output` command in a Windows Command Prompt (CMD) environment. Note that `"` characters should be removed for correct processing in CMD.
SOURCE: https://github.com/actions/toolkit/blob/main/docs/commands.md#_snippet_7

LANGUAGE: cmd
CODE:
```
echo ::set-output name=FOO::BAR
```

----------------------------------------

TITLE: Glob Pattern Syntax and Behavior (APIDOC)
DESCRIPTION: Detailed documentation on the supported glob pattern syntax, including special characters (`*`, `?`, `[...]`, `**`), tilde expansion, comments, exclude patterns, and escaping rules.
SOURCE: https://github.com/actions/toolkit/blob/main/packages/glob/README.md#_snippet_5

LANGUAGE: APIDOC
CODE:
```
Glob behavior:
- Patterns: *, ?, [...], ** (globstar)
- File names starting with . may be included.
- Case insensitive on Windows.
- Directory separators / and \ both supported on Windows.

Tilde expansion:
- Supports basic tilde expansion for current user HOME replacement only.
- Example: ~ expands to /Users/johndoe; ~/foo expands to /Users/johndoe/foo.

Comments:
- Patterns beginning with # are treated as comments.

Exclude patterns:
- Leading ! changes meaning to exclude.
- Multiple leading ! flips the meaning.

Escaping:
- Wrapping special characters in [] escapes literal glob characters (e.g., hello[[]a-z] for hello[a-z]).
- On Linux/macOS, \ is also treated as an escape character.
```