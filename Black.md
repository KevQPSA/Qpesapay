TITLE: Format Python Code with Black (Command Line)

DESCRIPTION: Formats a specified Python source file or an entire directory using the Black formatter from the command line. This is the primary way to use Black.

SOURCE: https://github.com/psf/black/blob/main/README.md#\_snippet\_3



LANGUAGE: Shell

CODE:

```

black {source\_file\_or\_directory}

```



----------------------------------------



TITLE: Basic File Formatting with Black

DESCRIPTION: Demonstrates the primary command-line usage of Black to reformat Python source files or entire directories in place with sensible defaults.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_0



LANGUAGE: sh

CODE:

```

black {source\_file\_or\_directory}

```



----------------------------------------



TITLE: Install Black with pip

DESCRIPTION: Installs the Black code formatter using pip, the standard Python package installer. Includes an option to install with Jupyter Notebook support.

SOURCE: https://github.com/psf/black/blob/main/docs/getting\_started.md#\_snippet\_0



LANGUAGE: sh

CODE:

```

pip install black

```



LANGUAGE: sh

CODE:

```

pip install "black\[jupyter]"

```



----------------------------------------



TITLE: Run Black as a Python Module

DESCRIPTION: Illustrates how to invoke Black using the Python interpreter's module execution, which can be an alternative if direct script execution is problematic.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_1



LANGUAGE: python

CODE:

```

python -m black {source\_file\_or\_directory}

```



----------------------------------------



TITLE: Verify Black Installation and Command Line Access

DESCRIPTION: This command verifies that Black is correctly installed and accessible from your system's command line by displaying its help message, confirming its readiness for use in scripts or direct execution.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_3



LANGUAGE: console

CODE:

```

$ black --help

```



----------------------------------------



TITLE: Format Python Code from String Input

DESCRIPTION: Shows how to use the `--code` command-line option to format a Python code snippet provided directly as a string argument, useful for quick tests or single-line formatting.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_2



LANGUAGE: console

CODE:

```

black --code "print ( 'hello, world' )"

```



----------------------------------------



TITLE: Illustrate Trailing Comma Behavior with Target Versions

DESCRIPTION: Provides examples demonstrating how Black's decision to add or remove a trailing comma after `\*args` in function calls is dependent on the specified target Python versions, specifically highlighting the change introduced in Python 3.5.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_5



LANGUAGE: console

CODE:

```

black --line-length=10 --target-version=py35 -c 'f(a, \*args)'

```



LANGUAGE: console

CODE:

```

black --line-length=10 --target-version=py34 -c 'f(a, \*args)'

```



LANGUAGE: console

CODE:

```

black --line-length=10 --target-version=py34 --target-version=py35 -c 'f(a, \*args)'

```



----------------------------------------



TITLE: Install Black Python Formatter via pip

DESCRIPTION: Installs the Black code formatter using pip, the Python package installer. This is the standard way to get Black. It requires Python 3.9+ to run.

SOURCE: https://github.com/psf/black/blob/main/README.md#\_snippet\_0



LANGUAGE: Shell

CODE:

```

pip install black

```



----------------------------------------



TITLE: Specify Target Python Versions via CLI

DESCRIPTION: Explains how to explicitly set multiple target Python versions using the `-t` or `--target-version` command-line option, ensuring Black formats code compatible with these versions.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_3



LANGUAGE: console

CODE:

```

black -t py311 -t py312 -t py313

```



----------------------------------------



TITLE: Black's Line Wrapping for Long Function Definitions

DESCRIPTION: Shows how Black formats long function definitions, placing each parameter on a new line with proper indentation, and adding a trailing comma. This minimizes diffs when parameters are added or removed and provides a clear visual structure.

SOURCE: https://github.com/psf/black/blob/main/docs/the\_black\_code\_style/current\_style.md#\_snippet\_2



LANGUAGE: python

CODE:

```

\# in:



def very\_important\_function(template: str, \*variables, file: os.PathLike, engine: str, header: bool = True, debug: bool = False):

&nbsp;   """Applies `variables` to the `template` and writes to `file`."""

&nbsp;   with open(file, 'w') as f:

&nbsp;       ...

```



LANGUAGE: python

CODE:

```

\# out:



def very\_important\_function(

&nbsp;   template: str,

&nbsp;   \*variables,

&nbsp;   file: os.PathLike,

&nbsp;   engine: str,

&nbsp;   header: bool = True,

&nbsp;   debug: bool = False,

):

&nbsp;   """Applies `variables` to the `template` and writes to `file`."""

&nbsp;   with open(file, "w") as f:

&nbsp;       ...

```



----------------------------------------



TITLE: Install Black with Jupyter Notebook Support

DESCRIPTION: Installs the Black formatter along with additional dependencies required for formatting Jupyter Notebooks. Use this if you need to format .ipynb files.

SOURCE: https://github.com/psf/black/blob/main/README.md#\_snippet\_1



LANGUAGE: Shell

CODE:

```

pip install "black\[jupyter]"

```



----------------------------------------



TITLE: Configure Target Python Versions in pyproject.toml

DESCRIPTION: Demonstrates the TOML syntax for specifying target Python versions within a `pyproject.toml` configuration file, allowing for project-wide formatting consistency.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_4



LANGUAGE: toml

CODE:

```

target-version = \["py311", "py312", "py313"]

```



----------------------------------------



TITLE: Black Formatting from Stdin Console Example

DESCRIPTION: Demonstrates piping code to Black via standard input for formatting, with the result printed to standard output. This is useful for integrating Black into workflows where code is not stored in files.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_16



LANGUAGE: console

CODE:

```

$ echo "print ( 'hello, world' )" | black -

print("hello, world")

reformatted -

All done! ✨ 🍰 ✨

1 file reformatted.

```



----------------------------------------



TITLE: Black CLI: Check Mode Exit Codes

DESCRIPTION: Demonstrates the behavior and exit codes of the `black --check` command when files are unchanged, would be reformatted, or an internal error occurs. This flag prevents writing changes and is useful for CI/CD pipelines.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_6



LANGUAGE: Shell

CODE:

```

$ black test.py --check

All done! ✨ 🍰 ✨

1 file would be left unchanged.

$ echo $?

0



$ black test.py --check

would reformat test.py

Oh no! 💥 💔 💥

1 file would be reformatted.

$ echo $?

1



$ black test.py --check

error: cannot format test.py: INTERNAL ERROR: Black produced code that is not equivalent to the source.  Please report a bug on https://github.com/psf/black/issues.  This diff might be helpful: /tmp/blk\_kjdr1oog.log

Oh no! 💥 💔 💥

1 file would fail to reformat.

$ echo $?

123

```



----------------------------------------



TITLE: Install Black from GitHub Source

DESCRIPTION: Installs the latest development version of Black directly from its GitHub repository. This is useful for getting the newest features or bug fixes before they are officially released.

SOURCE: https://github.com/psf/black/blob/main/README.md#\_snippet\_2



LANGUAGE: Shell

CODE:

```

pip install git+https://github.com/psf/black

```



----------------------------------------



TITLE: Vim Black Plugin Commands

DESCRIPTION: Overview of commands provided by the official Black Vim plugin for formatting, upgrading, and checking version.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_4



LANGUAGE: APIDOC

CODE:

```

:Black: Formats the entire file (ranges not supported).

&nbsp; Optional: target\_version=<version> (same values as command line).

:BlackUpgrade: Upgrades Black inside the virtualenv.

:BlackVersion: Gets the current version of Black in use.

```



----------------------------------------



TITLE: Black CLI: Format Specific Line Ranges

DESCRIPTION: Shows how to use the `--line-ranges` option to apply Black's formatting only to specified line ranges within a file. This option can be specified multiple times and is primarily intended for editor integrations like 'Format Selection'.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_8



LANGUAGE: Shell

CODE:

```

black --line-ranges=1-10 --line-ranges=21-30 test.py

```



----------------------------------------



TITLE: Format Python Code with Black (Python Module)

DESCRIPTION: Formats a specified Python source file or directory by running Black as a Python module. This method can be used if running Black directly as a script doesn't work due to PATH issues or other environment configurations.

SOURCE: https://github.com/psf/black/blob/main/README.md#\_snippet\_4



LANGUAGE: Shell

CODE:

```

python -m black {source\_file\_or\_directory}

```



----------------------------------------



TITLE: Install Black Vim Plugin with vim-plug

DESCRIPTION: Instructions for installing the Black Vim plugin using vim-plug, including options for tracking stable branches or specific versions.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_6



LANGUAGE: VimScript

CODE:

```

Plug 'psf/black', { 'branch': 'stable' }

```



LANGUAGE: VimScript

CODE:

```

Plug 'psf/black', { 'tag': '\*.\*.\*' }

```



LANGUAGE: VimScript

CODE:

```

Plug 'psf/black', { 'tag': '22.\*.\*' }

```



----------------------------------------



TITLE: Display Black Code Style Badge in Markdown

DESCRIPTION: Shows how to embed the Black code style badge in a project's README.md file using standard Markdown syntax. This badge visually indicates that the project adheres to Black's formatting and links to the Black GitHub repository.

SOURCE: https://github.com/psf/black/blob/main/README.md#\_snippet\_5



LANGUAGE: md

CODE:

```

\[!\[Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

```



----------------------------------------



TITLE: Black CLI: Enforce Required Version

DESCRIPTION: Demonstrates how to use `--required-version` to ensure a specific Black version is running before formatting. This helps maintain consistent formatting across different development environments and can accept either a full version or just the major version.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_9



LANGUAGE: Shell

CODE:

```

$ black --version

black, 25.1.0 (compiled: yes)

$ black --required-version 25.1.0 -c "format = 'this'"

format = "this"

$ black --required-version 31.5b2 -c "still = 'beta?!'"

Oh no! 💥 💔 💥 The required version does not match the running version!



$ black --required-version 22 -c "format = 'this'"

format = "this"

$ black --required-version 31 -c "still = 'beta?!'"

Oh no! 💥 💔 💥 The required version does not match the running version!

```



----------------------------------------



TITLE: Basic GitHub Actions Workflow for Black Linting

DESCRIPTION: This YAML snippet defines a foundational GitHub Actions workflow. It triggers on push and pull\_request events, checks out the repository code, and then utilizes the `psf/black@stable` action to automatically lint the codebase, ensuring adherence to Black's code style. This provides a simple yet effective way to integrate Black into your CI/CD process.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/github\_actions.md#\_snippet\_0



LANGUAGE: yaml

CODE:

```

name: Lint



on: \[push, pull\_request]



jobs:

&nbsp; lint:

&nbsp;   runs-on: ubuntu-latest

&nbsp;   steps:

&nbsp;     - uses: actions/checkout@v4

&nbsp;     - uses: psf/black@stable

```



----------------------------------------



TITLE: Black Command-Line Exclusion and Inclusion Options

DESCRIPTION: Documentation for Black's command-line options related to file and directory exclusion and inclusion during recursive searches.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_10



LANGUAGE: APIDOC

CODE:

```

Option: --exclude

&nbsp; Description: A regular expression that matches files and directories that should be excluded on recursive searches. An empty value means no paths are excluded. Use forward slashes for directories on all platforms (Windows, too). By default, Black also ignores all paths listed in .gitignore. Changing this value will override all default exclusions.

&nbsp; Default Exclusions: \['.direnv', '.eggs', '.git', '.hg', '.ipynb\_checkpoints', '.mypy\_cache', '.nox', '.pytest\_cache', '.ruff\_cache', '.tox', '.svn', '.venv', '.vscode', '\_\_pypackages\_\_', '\_build', 'buck-out', 'build', 'dist', 'venv']

&nbsp; Notes: If the regular expression contains newlines, it is treated as a verbose regular expression, useful in pyproject.toml.

```



LANGUAGE: APIDOC

CODE:

```

Option: --extend-exclude

&nbsp; Description: Like --exclude, but adds additional files and directories on top of the default values instead of overriding them.

```



LANGUAGE: APIDOC

CODE:

```

Option: --force-exclude

&nbsp; Description: Like --exclude, but files and directories matching this regex will be excluded even when they are passed explicitly as arguments. Useful for programmatic invocation (e.g., pre-commit hooks).

```



LANGUAGE: APIDOC

CODE:

```

Option: --stdin-filename

&nbsp; Description: The name of the file when passing it through stdin. Useful to ensure Black respects --force-exclude when using stdin.

```



LANGUAGE: APIDOC

CODE:

```

Option: --include

&nbsp; Description: A regular expression that matches files and directories that should be included on recursive searches. An empty value means all files are included regardless of the name. Use forward slashes for directories on all platforms (Windows, too). Overrides all exclusions, including from .gitignore and command line options.

&nbsp; Default Inclusions: \['.pyi', '.ipynb']

```



----------------------------------------



TITLE: Install Black Python Formatter

DESCRIPTION: This command installs the core Black Python code formatter using pip, making it available for general use in your development environment.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_0



LANGUAGE: console

CODE:

```

$ pip install black

```



----------------------------------------



TITLE: isort Default Grid Wrap Incompatible with Black

DESCRIPTION: Illustrates isort's default 'Grid' wrapping style for imports when they exceed the line length. This style is incompatible with Black's formatting approach, which prefers a different multi-line import structure.

SOURCE: https://github.com/psf/black/blob/main/docs/guides/using\_black\_with\_other\_tools.md#\_snippet\_2



LANGUAGE: python

CODE:

```

from third\_party import (lib1, lib2, lib3,

&nbsp;                        lib4, lib5, ...)

```



----------------------------------------



TITLE: Black Command-Line Performance and Output Options

DESCRIPTION: Documentation for Black's command-line options controlling parallel processing, output verbosity, and configuration file usage.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_11



LANGUAGE: APIDOC

CODE:

```

Option: -W, --workers

&nbsp; Description: Controls the number of parallel workers Black uses when formatting multiple files. Can also be specified via the BLACK\_NUM\_WORKERS environment variable.

&nbsp; Default: Number of CPUs in the system.

```



LANGUAGE: APIDOC

CODE:

```

Option: -q, --quiet

&nbsp; Description: Stops emitting all non-critical output. Error messages will still be emitted.

```



LANGUAGE: APIDOC

CODE:

```

Option: -v, --verbose

&nbsp; Description: Emits messages about files that were not changed or were ignored due to exclusion patterns. Also details which configuration file is being used.

```



LANGUAGE: APIDOC

CODE:

```

Option: --version

&nbsp; Description: Displays the installed version of Black.

```



LANGUAGE: APIDOC

CODE:

```

Option: --config

&nbsp; Description: Specifies a configuration file to read options from.

```



----------------------------------------



TITLE: Install Black with 'd' Extra for blackd Server

DESCRIPTION: This command installs Black along with the 'd' extra, which includes dependencies necessary for running Black as a local server (blackd). This setup is often used for faster formatting in IDEs like PyCharm by avoiding startup costs on subsequent formats.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_1



LANGUAGE: console

CODE:

```

$ pip install 'black\[d]'

```



----------------------------------------



TITLE: Flake8 Minimal Configuration for Black Compatibility

DESCRIPTION: A minimal Flake8 configuration for compatibility with Black, setting the maximum line length to 88 and ignoring E203 and E701 warnings. This can be used in `.flake8`, `setup.cfg`, or `tox.ini`.

SOURCE: https://github.com/psf/black/blob/main/docs/guides/using\_black\_with\_other\_tools.md#\_snippet\_8



LANGUAGE: ini

CODE:

```

\[flake8]

max-line-length = 88

extend-ignore = E203,E701

```



----------------------------------------



TITLE: Locate Black Executable Path

DESCRIPTION: These commands help in finding the installation path of the Black executable on different operating systems (macOS/Linux/BSD and Windows). Knowing the executable's path is crucial for configuring Black as an external tool or file watcher in IDEs.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_2



LANGUAGE: console

CODE:

```

$ which black

/usr/local/bin/black  # possible location

```



LANGUAGE: console

CODE:

```

$ where black

%LocalAppData%\\Programs\\Python\\Python36-32\\Scripts\\black.exe  # possible location

```



----------------------------------------



TITLE: Black Quiet Mode Console Example

DESCRIPTION: Demonstrates using the `--quiet` flag to suppress non-critical output during Black's formatting process, showing only error messages.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_13



LANGUAGE: console

CODE:

```

$ black src/ -q

error: cannot format src/black\_primer/cli.py: Cannot parse: 5:6: mport asyncio

```



----------------------------------------



TITLE: Pycodestyle/Flake8 Basic Configuration

DESCRIPTION: Configures pycodestyle or Flake8 to set the maximum line length to 88 characters and ignore specific warnings (E203, E701) that conflict with Black's formatting style. This configuration is suitable for `setup.cfg`, `.pycodestyle`, or `tox.ini` files.

SOURCE: https://github.com/psf/black/blob/main/docs/guides/using\_black\_with\_other\_tools.md#\_snippet\_6



LANGUAGE: ini

CODE:

```

\[pycodestyle]

max-line-length = 88

ignore = E203,E701

```



----------------------------------------



TITLE: Black Verbose Mode Console Example

DESCRIPTION: Illustrates using the `--verbose` flag to get detailed output, including configuration file usage, file modification status, and a summary of changes.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_14



LANGUAGE: console

CODE:

```

$ black src/ -v

Using configuration from /tmp/pyproject.toml.

src/blib2to3 ignored: matches the --extend-exclude regular expression

src/\_black\_version.py wasn't modified on disk since last run.

src/black/\_\_main\_\_.py wasn't modified on disk since last run.

error: cannot format src/black\_primer/cli.py: Cannot parse: 5:6: mport asyncio

reformatted src/black\_primer/lib.py

reformatted src/blackd/\_\_init\_\_.py

reformatted src/black/\_\_init\_\_.py

Oh no! 💥 💔 💥

3 files reformatted, 2 files left unchanged, 1 file failed to reformat

```



----------------------------------------



TITLE: Vim Black Plugin Configuration Variables

DESCRIPTION: Configurable variables for the Black Vim plugin, controlling behavior like line length, virtual environment usage, and preview mode.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_5



LANGUAGE: APIDOC

CODE:

```

g:black\_fast (defaults to 0)

g:black\_linelength (defaults to 88)

g:black\_skip\_string\_normalization (defaults to 0)

g:black\_skip\_magic\_trailing\_comma (defaults to 0)

g:black\_virtualenv (defaults to ~/.vim/black or ~/.local/share/nvim/black)

g:black\_use\_virtualenv (defaults to 1)

g:black\_target\_version (defaults to "")

g:black\_quiet (defaults to 0)

g:black\_preview (defaults to 0)

```



----------------------------------------



TITLE: Black Preview Style: Dict Parentheses Management - Before

DESCRIPTION: This Python code snippet shows a dictionary literal with a long value that is not yet wrapped in parentheses, and a short value unnecessarily wrapped. It represents the code \*before\* Black's `--preview` style is applied for improved parentheses management in dictionaries.

SOURCE: https://github.com/psf/black/blob/main/docs/the\_black\_code\_style/future\_style.md#\_snippet\_0



LANGUAGE: python

CODE:

```

my\_dict = {

&nbsp;   "a key in my dict": a\_very\_long\_variable

&nbsp;   \* and\_a\_very\_long\_function\_call()

&nbsp;   / 100000.0,

&nbsp;   "another key": (short\_value),

}

```



----------------------------------------



TITLE: Install Black Vim Plugin with Vundle

DESCRIPTION: Steps to install the Black Vim plugin using Vundle, including cloning the stable branch.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_7



LANGUAGE: VimScript

CODE:

```

Plugin 'psf/black'

```



LANGUAGE: Shell

CODE:

```

cd ~/.vim/bundle/black

git checkout origin/stable -b stable

```



----------------------------------------



TITLE: Black Version Check Console Example

DESCRIPTION: Shows how to check the installed version of Black using the `--version` command-line flag.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_15



LANGUAGE: console

CODE:

```

$ black --version

black, 25.1.0

```



----------------------------------------



TITLE: Black Preview Style: Dict Parentheses Management - After

DESCRIPTION: This Python code snippet demonstrates how Black's `--preview` style reformats the dictionary from the previous example. It wraps the long dictionary value in parentheses for better readability and removes unnecessary parentheses from the short value.

SOURCE: https://github.com/psf/black/blob/main/docs/the\_black\_code\_style/future\_style.md#\_snippet\_1



LANGUAGE: python

CODE:

```

my\_dict = {

&nbsp;   "a key in my dict": (

&nbsp;       a\_very\_long\_variable \* and\_a\_very\_long\_function\_call() / 100000.0

&nbsp;   ),

&nbsp;   "another key": short\_value,

}

```



----------------------------------------



TITLE: Black Writeback and Reporting Options

DESCRIPTION: Documentation for Black's command-line options that control whether files are rewritten and how changes are reported, including `--check` and `--diff` modes.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_17



LANGUAGE: APIDOC

CODE:

```

Option: --check

&nbsp; Description: Enables a dry-run mode where Black checks if any file would be reformatted. Exits with code 1 if any file would be changed, otherwise 0.

```



LANGUAGE: APIDOC

CODE:

```

Option: --diff

&nbsp; Description: Enables a dry-run mode where Black prints a diff of changes that would be applied instead of reformatting files in place.

```



----------------------------------------



TITLE: Disable Black Vim Plugin Virtualenv

DESCRIPTION: Configuration to prevent the Black Vim plugin from using its own virtual environment, opting for a system-wide Black installation instead.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_9



LANGUAGE: VimScript

CODE:

```

let g:black\_use\_virtualenv = 0

```



----------------------------------------



TITLE: Black Preview Style: Multiline List/Dict Indentation - Before

DESCRIPTION: This Python code snippet shows a function call with a multiline list parameter and a nested multiline list, both with traditional indentation where opening parentheses/brackets are on a new line. This represents the code \*before\* Black's `--preview` style is applied for more compact formatting.

SOURCE: https://github.com/psf/black/blob/main/docs/the\_black\_code\_style/future\_style.md#\_snippet\_2



LANGUAGE: python

CODE:

```

foo(

&nbsp;   \[

&nbsp;       1,

&nbsp;       2,

&nbsp;       3,

&nbsp;   ]

)



nested\_array = \[

&nbsp;   \[

&nbsp;       1,

&nbsp;       2,

&nbsp;       3,

&nbsp;   ]

]

```



----------------------------------------



TITLE: Configure Black to Run on File Save in Vim

DESCRIPTION: Vim autocmd configuration to automatically run Black on Python files before they are saved.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_10



LANGUAGE: VimScript

CODE:

```

augroup black\_on\_save

&nbsp; autocmd!

&nbsp; autocmd BufWritePre \*.py Black

augroup end

```



----------------------------------------



TITLE: Black Formatter Console Output Example

DESCRIPTION: This snippet demonstrates the typical console output from Black when formatting files. It shows messages for successful reformatting, errors for unparseable files, and a summary of the operation, illustrating Black's default verbosity.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_18



LANGUAGE: console

CODE:

```

$ black src/

error: cannot format src/black\_primer/cli.py: Cannot parse: 5:6: mport asyncio

reformatted src/black\_primer/lib.py

reformatted src/blackd/\_\_init\_\_.py

reformatted src/black/\_\_init\_\_.py

Oh no! 💥 💔 💥

3 files reformatted, 2 files left unchanged, 1 file failed to reformat.

```



----------------------------------------



TITLE: Black Preview Style: Multiline List/Dict Indentation - After

DESCRIPTION: This Python code snippet demonstrates how Black's `--preview` style reformats the multiline list/dictionary indentation from the previous example. It pairs opening parentheses/brackets with their respective braces/square brackets on the same line for a more compact and readable format.

SOURCE: https://github.com/psf/black/blob/main/docs/the\_black\_code\_style/future\_style.md#\_snippet\_3



LANGUAGE: python

CODE:

```

foo(\[

&nbsp;   1,

&nbsp;   2,

&nbsp;   3,

])



nested\_array = \[\[

&nbsp;   1,

&nbsp;   2,

&nbsp;   3,

]]

```



----------------------------------------



TITLE: Example pyproject.toml Configuration for Black

DESCRIPTION: This TOML snippet illustrates how to configure Black's behavior within a `pyproject.toml` file. It showcases common options such as `line-length`, `target-version`, `include` patterns, and `extend-exclude` for specific files or directories, including the use of regular expressions and multi-line strings for complex patterns.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_19



LANGUAGE: toml

CODE:

```

\[tool.black]

line-length = 88

target-version = \['py37']

include = '\\.pyi?$'

\# 'extend-exclude' excludes files or directories in addition to the defaults

extend-exclude = '''

\# A regex preceded with ^/ will apply only to files and directories

\# in the root of the project.

(

&nbsp; ^/foo.py    # exclude a file named foo.py in the root of the project

&nbsp; | .\*\_pb2.py  # exclude autogenerated Protocol Buffer files anywhere in the project

)

'''

```



----------------------------------------



TITLE: Map Black Formatting to a Key Press in Vim

DESCRIPTION: Vim key mapping to execute the Black formatting command on a specific key press, e.g., F9.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_11



LANGUAGE: VimScript

CODE:

```

nnoremap <F9> :Black<CR>

```



----------------------------------------



TITLE: Black Preview Style: List/Dict Unpacking Indentation - Before

DESCRIPTION: This Python code snippet illustrates a function call with unpacked list comprehension, where the opening bracket is on a new line. This shows the code \*before\* Black's `--preview` style applies its compacting behavior for improved multiline indentation.

SOURCE: https://github.com/psf/black/blob/main/docs/the\_black\_code\_style/future\_style.md#\_snippet\_4



LANGUAGE: python

CODE:

```

foo(

&nbsp;   \*\[

&nbsp;       a\_long\_function\_name(a\_long\_variable\_name)

&nbsp;       for a\_long\_variable\_name in some\_generator

&nbsp;   ]

)

```



----------------------------------------



TITLE: Configure Black Formatting Hook in Kakoune

DESCRIPTION: This Kakoune configuration snippet adds a global hook that automatically sets the `formatcmd` option for Python files. When a Python file is opened, this hook ensures that the `black -q -` command is used for formatting, which can then be triggered by the `:format` command. This integrates Black directly into Kakoune's formatting workflow for Python source code.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_15



LANGUAGE: kakoune

CODE:

```

hook global WinSetOption filetype=python %{

&nbsp;   set-option window formatcmd 'black -q  -'

}

```



----------------------------------------



TITLE: Black Preview Style: List/Dict Unpacking Indentation - After

DESCRIPTION: This Python code snippet demonstrates how Black's `--preview` style reformats the unpacked list comprehension from the previous example. It moves the opening bracket to the same line as the asterisk, resulting in a more compact format.

SOURCE: https://github.com/psf/black/blob/main/docs/the\_black\_code\_style/future\_style.md#\_snippet\_5



LANGUAGE: python

CODE:

```

foo(\*\[

&nbsp;   a\_long\_function\_name(a\_long\_variable\_name)

&nbsp;   for a\_long\_variable\_name in some\_generator

])

```



----------------------------------------



TITLE: Configure Black Action with Specific Options and Version

DESCRIPTION: This YAML snippet demonstrates how to customize the `psf/black` GitHub Action's behavior. It sets specific `options` for Black (e.g., `--check --verbose`), defines the `src` directory to be linted, enables `jupyter` notebook support, and explicitly pins the `version` of Black to use. This allows for precise control over how Black operates within your workflow.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/github\_actions.md#\_snippet\_1



LANGUAGE: yaml

CODE:

```

\- uses: psf/black@stable

&nbsp; with:

&nbsp;   options: "--check --verbose"

&nbsp;   src: "./src"

&nbsp;   jupyter: true

&nbsp;   version: "21.5b1"

```



----------------------------------------



TITLE: Black Reformats Multiline String with `.replace()`

DESCRIPTION: Demonstrates Black's reformatting of a multiline string assigned to a variable and then modified with `.replace()`, showing the string being inlined from a multiline definition to a single line.

SOURCE: https://github.com/psf/black/blob/main/docs/the\_black\_code\_style/future\_style.md#\_snippet\_8



LANGUAGE: Python

CODE:

```

MULTILINE = """

foobar

""".replace(

&nbsp;   "\\n", ""

)

```



LANGUAGE: Python

CODE:

```

MULTILINE = """

foobar

""".replace("\\n", "")

```



----------------------------------------



TITLE: Configure Black Action with Compatible Version Specifier

DESCRIPTION: This YAML snippet illustrates how to configure the `psf/black` GitHub Action to use a version of Black that is compatible with a specified major release, leveraging the `~=` operator. This approach ensures that the action uses a Black version that aligns with its stability policy, offering flexibility while maintaining compatibility. It also includes custom `options` and `src` path for the linting process.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/github\_actions.md#\_snippet\_2



LANGUAGE: yaml

CODE:

```

\- uses: psf/black@stable

&nbsp; with:

&nbsp;   options: "--check --verbose"

&nbsp;   src: "./src"

&nbsp;   version: "~= 22.0"

```



----------------------------------------



TITLE: Install Black Development Dependencies

DESCRIPTION: Steps to set up a Python virtual environment and install necessary development and test dependencies for the Black project, including pre-commit hooks for linting.

SOURCE: https://github.com/psf/black/blob/main/docs/contributing/the\_basics.md#\_snippet\_1



LANGUAGE: console

CODE:

```

python3 -m venv .venv

source .venv/bin/activate # activation for linux and mac

.venv\\Scripts\\activate # activation for windows



(.venv)$ pip install -r test\_requirements.txt

(.venv)$ pip install -e ".\[d]"

(.venv)$ pre-commit install

```



----------------------------------------



TITLE: Configure Black Action to Read Version from pyproject.toml

DESCRIPTION: This YAML snippet shows how to configure the `psf/black` GitHub Action to automatically read the Black version from your project's `pyproject.toml` file. It first sets up a specific Python version (3.13) using `actions/setup-python`, which is a prerequisite for `use\_pyproject: true`. This method ensures that the Black version used in your CI/CD pipeline is consistent with your project's declared dependencies.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/github\_actions.md#\_snippet\_3



LANGUAGE: yaml

CODE:

```

\- uses: actions/setup-python@v5

&nbsp; with:

&nbsp;   python-version: "3.13"

\- uses: psf/black@stable

&nbsp; with:

&nbsp;   options: "--check --verbose"

&nbsp;   src: "./src"

&nbsp;   use\_pyproject: true

```



----------------------------------------



TITLE: Run Black Lints and Tests

DESCRIPTION: Commands to execute pre-commit checks for linting, run unit tests using tox, and optionally perform fuzz testing or self-format Black itself before submitting pull requests.

SOURCE: https://github.com/psf/black/blob/main/docs/contributing/the\_basics.md#\_snippet\_2



LANGUAGE: console

CODE:

```

\# Linting

(.venv)$ pre-commit run -a



\# Unit tests

(.venv)$ tox -e py



\# Optional Fuzz testing

(.venv)$ tox -e fuzz



\# Format Black itself

(.venv)$ tox -e run\_self

```



----------------------------------------



TITLE: Configure pre-commit hook for Black Python formatter

DESCRIPTION: This YAML configuration adds a pre-commit hook to automatically format Python code using Black. It leverages a faster mirror for improved performance and allows specifying the Python version for the hook.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/source\_version\_control.md#\_snippet\_0



LANGUAGE: YAML

CODE:

```

repos:

&nbsp; # Using this mirror lets us use mypyc-compiled black, which is about 2x faster

&nbsp; - repo: https://github.com/psf/black-pre-commit-mirror

&nbsp;   rev: 25.1.0

&nbsp;   hooks:

&nbsp;     - id: black

&nbsp;       # It is recommended to specify the latest version of Python

&nbsp;       # supported by your project here, or alternatively use

&nbsp;       # pre-commit's default\_language\_version, see

&nbsp;       # https://pre-commit.com/#top\_level-default\_language\_version

&nbsp;       language\_version: python3.11

```



----------------------------------------



TITLE: Add New Changelog Template for Next Black Release

DESCRIPTION: Runs the `release.py` script to append an empty template for the next release's changelog entries to `CHANGES.md`. This command is typically executed after a release has been successfully cut, preparing the repository for future development cycles. The optional `--debug` flag provides more verbose output.

SOURCE: https://github.com/psf/black/blob/main/docs/contributing/release\_process.md#\_snippet\_2



LANGUAGE: Shell

CODE:

```

python3 scripts/release.py --add-changes-template|-a \[--debug]

```



----------------------------------------



TITLE: Configure pre-commit hook for Black Jupyter Notebook formatter

DESCRIPTION: This YAML configuration extends the Black pre-commit hook to include Jupyter Notebooks. By replacing the hook ID with 'black-jupyter', it ensures that both Python code and .ipynb files are automatically formatted.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/source\_version\_control.md#\_snippet\_1



LANGUAGE: YAML

CODE:

```

repos:

&nbsp; # Using this mirror lets us use mypyc-compiled black, which is about 2x faster

&nbsp; - repo: https://github.com/psf/black-pre-commit-mirror

&nbsp;   rev: 25.1.0

&nbsp;   hooks:

&nbsp;     - id: black-jupyter

&nbsp;       # It is recommended to specify the latest version of Python

&nbsp;       # supported by your project here, or alternatively use

&nbsp;       # pre-commit's default\_language\_version, see

&nbsp;       # https://pre-commit.com/#top\_level-default\_language\_version

&nbsp;       language\_version: python3.11

```



----------------------------------------



TITLE: `blackd` Server API and Behavior

DESCRIPTION: This section outlines specific API interactions and behavioral characteristics of the `blackd` server, Black's daemon mode. It details how `blackd` preserves Windows-style newlines (CRLF) and supports enabling the preview style through a dedicated HTTP header.

SOURCE: https://github.com/psf/black/blob/main/CHANGES.md#\_snippet\_3



LANGUAGE: APIDOC

CODE:

```

CRLF Newlines:

&nbsp; - Windows style (CRLF) newlines will be preserved.

X-Preview Header:

&nbsp; - Supports enabling the preview style via this HTTP header.

```



----------------------------------------



TITLE: Configure isort Profile for Black in pyproject.toml

DESCRIPTION: Example configuration for isort version 5.0.0 and newer to use the 'black' profile. This setting ensures that isort's import sorting and formatting align with Black's style, specifically within a `pyproject.toml` file.

SOURCE: https://github.com/psf/black/blob/main/docs/guides/using\_black\_with\_other\_tools.md#\_snippet\_0



LANGUAGE: toml

CODE:

```

\[tool.isort]

profile = "black"

```



----------------------------------------



TITLE: Black Integrations: Vim Plugin and GitHub Action Options

DESCRIPTION: This snippet details configuration options and enhancements for Black's integrations with popular development tools. It covers a flag for the Vim plugin to control preview style and options for the GitHub Action to support Jupyter Notebooks and specific Black versions.

SOURCE: https://github.com/psf/black/blob/main/CHANGES.md#\_snippet\_4



LANGUAGE: APIDOC

CODE:

```

Vim Plugin:

&nbsp; g:black\_preview:

&nbsp;   - Flag to enable/disable the preview style.

&nbsp;   - Messages prefixed with 'Black: '.

GitHub Action:

&nbsp; jupyter option:

&nbsp;   - Supports formatting of Jupyter Notebook files.

&nbsp; version specifiers (e.g., <23):

&nbsp;   - Supports use of version specifiers for Black version.

```



----------------------------------------



TITLE: Custom isort Configuration for Black Compatibility

DESCRIPTION: Detailed configuration for isort, suitable for versions older than 5.0.0 or for custom setups, to achieve compatibility with Black. This snippet for `.isort.cfg` sets specific options like multi-line output, trailing commas, parentheses, and line length to match Black's formatting rules.

SOURCE: https://github.com/psf/black/blob/main/docs/guides/using\_black\_with\_other\_tools.md#\_snippet\_1



LANGUAGE: ini

CODE:

```

multi\_line\_output = 3

include\_trailing\_comma = True

force\_grid\_wrap = 0

use\_parentheses = True

ensure\_newline\_before\_comments = True

line\_length = 88

```



----------------------------------------



TITLE: Black Support for Modern Python Syntax (PEPs)

DESCRIPTION: This section highlights Black's compatibility with and ability to format new syntax features introduced in recent Python Enhancement Proposals (PEPs). It specifically mentions support for structured exception groups (PEP 654) and type parameter syntax (PEP 646), ensuring Black can handle contemporary Python code.

SOURCE: https://github.com/psf/black/blob/main/CHANGES.md#\_snippet\_5



LANGUAGE: APIDOC

CODE:

```

PEP 654 Syntax:

&nbsp; - Supported (e.g., except \*ExceptionGroup:).

PEP 646 Syntax:

&nbsp; - Supported (e.g., Array\[Batch, \*Shape] or def fn(\*args: \*T) -> None).

```



----------------------------------------



TITLE: isort Vertical Hanging Indent Compatible with Black

DESCRIPTION: Demonstrates the 'Vertical Hanging Indent' style for imports, which is fully compatible with Black's formatting. This style is achieved in isort by setting `multi-line-output = 3` and ensures consistent import wrapping.

SOURCE: https://github.com/psf/black/blob/main/docs/guides/using\_black\_with\_other\_tools.md#\_snippet\_3



LANGUAGE: python

CODE:

```

from third\_party import (

&nbsp;   lib1,

&nbsp;   lib2,

&nbsp;   lib3,

&nbsp;   lib4,

)

```



----------------------------------------



TITLE: Black Parser Support for Starred Expressions in For Loops

DESCRIPTION: Black now supports parsing starred expressions within the target of `for` and `async for` statements. This enhancement allows for more flexible iteration patterns and ensures correct formatting of such constructs.

SOURCE: https://github.com/psf/black/blob/main/CHANGES.md#\_snippet\_7



LANGUAGE: Python

CODE:

```

for item in \*items\_1, \*items\_2: pass

```



----------------------------------------



TITLE: isort Black Profile Configuration Across Various File Formats

DESCRIPTION: Examples of how to configure isort to use the 'black' profile across different common configuration file formats. This ensures consistent Black compatibility regardless of the project's chosen configuration file type.

SOURCE: https://github.com/psf/black/blob/main/docs/guides/using\_black\_with\_other\_tools.md#\_snippet\_4



LANGUAGE: ini

CODE:

```

\[settings]

profile = black

```



LANGUAGE: ini

CODE:

```

\[isort]

profile = black

```



LANGUAGE: toml

CODE:

```

\[tool.isort]

profile = 'black'

```



LANGUAGE: ini

CODE:

```

\[\*.py]

profile = black

```



----------------------------------------



TITLE: Black Parser Fix for Mapping Case As-Expressions

DESCRIPTION: This fix addresses issues with parsing mapping cases that include 'as-expressions', ensuring correct formatting for complex pattern matching constructs. It resolves previous parsing errors related to these patterns.

SOURCE: https://github.com/psf/black/blob/main/CHANGES.md#\_snippet\_8



LANGUAGE: Python

CODE:

```

case {"key": 1 | 2 as password}

```



----------------------------------------



TITLE: pycodestyle Configuration for Black Compatibility

DESCRIPTION: Configuration for pycodestyle to align its linting rules with Black's formatting. This snippet sets the maximum line length to 88 characters and disables specific warnings (E203, E701) that conflict with Black's stylistic choices, such as whitespace around slice operators.

SOURCE: https://github.com/psf/black/blob/main/docs/guides/using\_black\_with\_other\_tools.md#\_snippet\_5



LANGUAGE: ini

CODE:

```

max-line-length = 88

ignore = E203,E701

```



----------------------------------------



TITLE: Black Parser Fix for Multiple Top-Level As-Expressions

DESCRIPTION: Black's parser has been updated to correctly handle cases containing multiple top-level 'as-expressions' in pattern matching. This improvement ensures accurate parsing and formatting for more intricate match statements.

SOURCE: https://github.com/psf/black/blob/main/CHANGES.md#\_snippet\_9



LANGUAGE: Python

CODE:

```

case 1 as a, 2 as b

```



----------------------------------------



TITLE: Pylint Configuration in pylintrc

DESCRIPTION: Example configuration for Pylint in a `pylintrc` file, setting the maximum line length within the `\[format]` section to 88 characters.

SOURCE: https://github.com/psf/black/blob/main/docs/guides/using\_black\_with\_other\_tools.md#\_snippet\_10



LANGUAGE: ini

CODE:

```

\[format]

max-line-length = 88

```



----------------------------------------



TITLE: Configure Black as ALE Fixer in Vim

DESCRIPTION: This snippet configures the Asynchronous Linting Engine (ALE) plugin in Vim to use Black for automatic Python code formatting. It sets `g:ale\_fixers.python` to include 'black', enabling Black to fix Python files upon saving or on demand. Users need to have both ALE and Black installed for this configuration to function correctly.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_12



LANGUAGE: vim

CODE:

```

let g:ale\_fixers = {}

let g:ale\_fixers.python = \['black']

```



----------------------------------------



TITLE: Pylint Configuration in pyproject.toml

DESCRIPTION: Example configuration for Pylint in a `pyproject.toml` file, setting the maximum line length for the `format` tool to 88 characters.

SOURCE: https://github.com/psf/black/blob/main/docs/guides/using\_black\_with\_other\_tools.md#\_snippet\_12



LANGUAGE: toml

CODE:

```

\[tool.pylint.format]

max-line-length = "88"

```



----------------------------------------



TITLE: Open File with Gedit from Console

DESCRIPTION: This is a standard console command used to open a specified file (`<file\_name>`) directly with the Gedit text editor. It's a basic utility command for quick file access from the terminal. This command does not involve Black formatting directly but is a prerequisite step mentioned in the Gedit integration guide.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_13



LANGUAGE: console

CODE:

```

$ gedit <file\_name>

```



----------------------------------------



TITLE: Python Type Annotation Spacing Fix Example

DESCRIPTION: This code snippet illustrates a complex type annotation involving a type variable tuple (`\*tuple\[\*Ts, T]`) that required a fix in Black's preview style to ensure correct spacing. This addresses a specific issue related to how Black formats advanced type hints.

SOURCE: https://github.com/psf/black/blob/main/CHANGES.md#\_snippet\_0



LANGUAGE: Python

CODE:

```

def fn(\*args: \*tuple\[\*Ts, T]) -> None: pass

```



----------------------------------------



TITLE: Python Binary Operator Spacing Examples

DESCRIPTION: Demonstrates Black's rules for whitespace around binary operators, specifically focusing on the power operator (\*\*). It differentiates between simple operands (NAME, numeric CONSTANT, attribute access) which do not require surrounding whitespace, and complex operands (function calls, dictionary access) which do.

SOURCE: https://github.com/psf/black/blob/main/docs/the\_black\_code\_style/current\_style.md#\_snippet\_6



LANGUAGE: python

CODE:

```

\# For example, these won't be surrounded by whitespace

a = x\*\*y

b = config.base\*\*5.2

c = config.base\*\*runtime.config.exponent

d = 2\*\*5

e = 2\*\*~5



\# ... but these will be surrounded by whitespace

f = 2 \*\* get\_exponent()

g = get\_x() \*\* get\_y()

h = config\['base'] \*\* 2

```



----------------------------------------



TITLE: Create Gedit External Tool for Black Formatting

DESCRIPTION: This bash script is designed to be added as an 'External Tool' within Gedit, allowing users to format the currently open document using Black. It retrieves the current document's name and then executes the `black` command on it. This provides a convenient way to trigger Black formatting directly from Gedit's interface, potentially via a keyboard shortcut.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_14



LANGUAGE: bash

CODE:

```

\#!/bin/bash

Name=$GEDIT\_CURRENT\_DOCUMENT\_NAME

black $Name

```



----------------------------------------



TITLE: Black Command-Line and File Configuration Options

DESCRIPTION: This section details various command-line arguments and configuration behaviors for the Black formatter. It covers options to skip formatting specific parts of source code, control string normalization, manage trailing commas, and how Black interacts with .gitignore files for path exclusion.

SOURCE: https://github.com/psf/black/blob/main/CHANGES.md#\_snippet\_1



LANGUAGE: APIDOC

CODE:

```

.ipynb\_checkpoints:

&nbsp; - Excluded by default.

--skip-source-first-line / -x:

&nbsp; - Ignores the first line of source code while formatting.

--skip-string-normalization / -S:

&nbsp; - Prevents docstring prefixes from being normalized.

--skip-magic-trailing-comma / -C:

&nbsp; - Strips trailing commas from subscript expressions with more than 1 element.

--stdin-filename:

&nbsp; - Affects misdetection of project root and verbose logging.

.gitignore files:

&nbsp; - Immediate .gitignore files in source directories are respected.

--version:

&nbsp; - Outputs Python version and implementation.

```



----------------------------------------



TITLE: Manual Installation of Black Vim Plugin

DESCRIPTION: Commands to manually install the Black Vim plugin for Vim 8 native plugin management by downloading files.

SOURCE: https://github.com/psf/black/blob/main/docs/integrations/editors.md#\_snippet\_8



LANGUAGE: Shell

CODE:

```

mkdir -p ~/.vim/pack/python/start/black/plugin

mkdir -p ~/.vim/pack/python/start/black/autoload

curl https://raw.githubusercontent.com/psf/black/stable/plugin/black.vim -o ~/.vim/pack/python/start/black/plugin/black.vim

curl https://raw.githubusercontent.com/psf/black/stable/autoload/black.vim -o ~/.vim/pack/python/start/black/autoload/black.vim

```



----------------------------------------



TITLE: In-Code Formatting Directives for Black

DESCRIPTION: This snippet describes special comments that can be embedded directly within Python code to control Black's formatting behavior. These directives allow users to selectively enable, disable, or skip formatting for specific lines or blocks of code, providing fine-grained control over the output.

SOURCE: https://github.com/psf/black/blob/main/CHANGES.md#\_snippet\_2



LANGUAGE: APIDOC

CODE:

```

\# fmt: on/off:

&nbsp; - Controls formatting for a block of code.

&nbsp; - Fixes infinite loop when used in middle of expression/block.

\# fmt: skip:

&nbsp; - Skips formatting for the current line.

&nbsp; - Fixes incorrect handling on colon (:) lines.

&nbsp; - Comments are no longer deleted when spaces removed around power operators.

```



----------------------------------------



TITLE: Flake8 Configuration with Bugbear Plugin

DESCRIPTION: Recommended Flake8 configuration when using the flake8-bugbear plugin. It sets the line length to 80, enables Bugbear's B950 check (which aligns with Black's 10% rule), and extends ignored warnings to include E501, E203, and E701.

SOURCE: https://github.com/psf/black/blob/main/docs/guides/using\_black\_with\_other\_tools.md#\_snippet\_7



LANGUAGE: ini

CODE:

```

\[flake8]

max-line-length = 80

extend-select = B950

extend-ignore = E203,E501,E701

```



----------------------------------------



TITLE: Python Documentation Build Requirements

DESCRIPTION: This snippet lists the Python package dependencies with pinned versions, crucial for ensuring stable and reproducible documentation builds for the /psf/black project, especially when hosted on ReadTheDocs. Comments explain the purpose and specific version choices.

SOURCE: https://github.com/psf/black/blob/main/docs/requirements.txt#\_snippet\_0



LANGUAGE: Python

CODE:

```

\# Used by ReadTheDocs; pinned requirements for stability.



myst-parser==4.0.1

Sphinx==8.2.3

\# Older versions break Sphinx even though they're declared to be supported.

docutils==0.21.2

sphinxcontrib-programoutput==0.18

sphinx\_copybutton==0.5.2

furo==2024.8.6

```



----------------------------------------



TITLE: Black Standardizes Jupyter Code Cell Separators

DESCRIPTION: Black now standardizes Jupyter Notebook code cell separators from `#%%` to `# %%`, ensuring consistent formatting across notebooks. This change improves readability and adherence to a unified style.

SOURCE: https://github.com/psf/black/blob/main/CHANGES.md#\_snippet\_6



LANGUAGE: Python

CODE:

```

Before: #%%

After: # %%

```



----------------------------------------



TITLE: Pylint Line Length Configuration

DESCRIPTION: Configures Pylint to set the maximum line length to 88 characters, aligning with Black's formatting. This is a general setting that needs to be placed within the appropriate Pylint configuration file and section.

SOURCE: https://github.com/psf/black/blob/main/docs/guides/using\_black\_with\_other\_tools.md#\_snippet\_9



LANGUAGE: ini

CODE:

```

max-line-length = 88

```



----------------------------------------



TITLE: Black Parser Fix for Call Pattern As-Expressions with Keyword Arguments

DESCRIPTION: This update resolves parsing issues for call patterns that incorporate 'as-expressions' alongside keyword arguments. It improves compatibility with advanced pattern matching syntax and ensures consistent formatting.

SOURCE: https://github.com/psf/black/blob/main/CHANGES.md#\_snippet\_10



LANGUAGE: Python

CODE:

```

case Foo(bar=baz as quux)

```



----------------------------------------



TITLE: Black CLI: Generate Diff Output

DESCRIPTION: Illustrates how to use `black --diff` to preview formatting changes as a unified diff without modifying the original file. The output is printed to stdout, making it easy to capture or pipe.

SOURCE: https://github.com/psf/black/blob/main/docs/usage\_and\_configuration/the\_basics.md#\_snippet\_7



LANGUAGE: Shell

CODE:

```

$ black test.py --diff

--- test.py	2021-03-08 22:23:40.848954+00:00

+++ test.py	2021-03-08 22:23:47.126319+00:00

@@ -1 +1 @@

-print ( 'hello, world' )

+print("hello, world")

would reformat test.py

All done! ✨ 🍰 ✨

1 file would be reformatted.

```



----------------------------------------



TITLE: Pylint Configuration in setup.cfg

DESCRIPTION: Example configuration for Pylint in a `setup.cfg` file, setting the maximum line length within the `\[pylint]` section to 88 characters.

SOURCE: https://github.com/psf/black/blob/main/docs/guides/using\_black\_with\_other\_tools.md#\_snippet\_11



LANGUAGE: ini

CODE:

```

\[pylint]

max-line-length = 88

```



----------------------------------------



TITLE: Black Formatting for Unparenthesized Tuples in Annotated Assignments

DESCRIPTION: Black now correctly handles and implies Python 3.8+ for unparenthesized tuples used in annotated assignments. This ensures consistent formatting and proper interpretation of type hints in such contexts.

SOURCE: https://github.com/psf/black/blob/main/CHANGES.md#\_snippet\_11



LANGUAGE: Python

CODE:

```

values: Tuple\[int, ...] = 1, 2, 3

```



----------------------------------------



TITLE: Display Black Code Style Badge in Markdown

DESCRIPTION: This snippet provides the Markdown syntax to include a 'Code style: black' badge in a project's README.md file. The badge links to the Black GitHub repository, indicating that the project adheres to Black's formatting standards.

SOURCE: https://github.com/psf/black/blob/main/docs/index.md#\_snippet\_0



LANGUAGE: md

CODE:

```

\[!\[Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

```



----------------------------------------



TITLE: Black Parser Implication for Future Annotations Import

DESCRIPTION: The presence of `from \_\_future\_\_ import annotations` now implies Python 3.7+ for Black's parser. This affects how code is interpreted and formatted, aligning with the language's evolution.

SOURCE: https://github.com/psf/black/blob/main/CHANGES.md#\_snippet\_12



LANGUAGE: Python

CODE:

```

from \_\_future\_\_ import annotations

```



----------------------------------------



TITLE: Display Black Code Style Badge in reStructuredText

DESCRIPTION: Demonstrates how to include the Black code style badge in a project's README.rst file using reStructuredText syntax. The badge serves as a visual indicator of Black formatting compliance and links to the Black GitHub repository.

SOURCE: https://github.com/psf/black/blob/main/README.md#\_snippet\_6



LANGUAGE: rst

CODE:

```

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg

&nbsp;   :target: https://github.com/psf/black

```



----------------------------------------



TITLE: Black CLI Options Reference

DESCRIPTION: Documentation for the command-line interface options available in the Black Python code formatter, extracted from the provided release notes.

SOURCE: https://github.com/psf/black/blob/main/CHANGES.md#\_snippet\_13



LANGUAGE: APIDOC

CODE:

```

Black CLI Options:

&nbsp; --config <path>: Specify a path to a TOML configuration file.

&nbsp; -h, --help: Show help message and exit.

&nbsp; --include <regex>: A regular expression that matches files and directories to include.

&nbsp; --exclude <regex>: A regular expression that matches files and directories to exclude.

&nbsp; --skip-string-normalization: Don't normalize string quotes or prefixes.

&nbsp; --verbose: Enable verbose output.

&nbsp; --pyi: Format .pyi (typing stub) files.

&nbsp; --py36: Format code for Python 3.6+ features (e.g., f-strings).

&nbsp; -S: (Implied from context) Related to unmodified file caching.

```



----------------------------------------



TITLE: Execute Python Code with Timing

DESCRIPTION: This snippet demonstrates a basic Python print statement within a Jupyter/IPython environment, utilizing the `%%time` magic command to measure the execution time of the cell. The accompanying note 'This notebook should not be reformatted' indicates a specific requirement or constraint regarding the layout or structure of the notebook containing this code.

SOURCE: https://github.com/psf/black/blob/main/tests/data/jupyter/notebook\_without\_changes.ipynb#\_snippet\_0



LANGUAGE: python

CODE:

```

%%time



print("foo")

```



----------------------------------------



TITLE: Black's Line Wrapping for Simple Lists

DESCRIPTION: Demonstrates how Black unwraps a multi-line list into a single line if it fits the allotted line length, removing unnecessary vertical whitespace and ensuring compact formatting.

SOURCE: https://github.com/psf/black/blob/main/docs/the\_black\_code\_style/current\_style.md#\_snippet\_0



LANGUAGE: python

CODE:

```

\# in:



j = \[1,

&nbsp;    2,

&nbsp;    3

]

```



LANGUAGE: python

CODE:

```

\# out:



j = \[1, 2, 3]

```



----------------------------------------



TITLE: Execute Python Code with Time Measurement

DESCRIPTION: This snippet demonstrates a basic Python print statement and utilizes the `%%time` Jupyter magic command to measure its execution time. It's typically used in interactive environments like Jupyter notebooks for quick performance insights.

SOURCE: https://github.com/psf/black/blob/main/tests/data/jupyter/notebook\_empty\_metadata.ipynb#\_snippet\_0



LANGUAGE: python

CODE:

```

%%time



print('foo')

```



----------------------------------------



TITLE: Black's Line Wrapping for Long Function Calls

DESCRIPTION: Illustrates how Black wraps long function calls by placing arguments on separate indented lines if the entire call doesn't fit on one line, improving readability for complex expressions.

SOURCE: https://github.com/psf/black/blob/main/docs/the\_black\_code\_style/current\_style.md#\_snippet\_1



LANGUAGE: python

CODE:

```

\# in:



ImportantClass.important\_method(exc, limit, lookup\_lines, capture\_locals, extra\_argument)

```



LANGUAGE: python

CODE:

```

\# out:



ImportantClass.important\_method(

&nbsp;   exc, limit, lookup\_lines, capture\_locals, extra\_argument

)

```



----------------------------------------



TITLE: Execute Simple Python Print Statement with Time Measurement

DESCRIPTION: This snippet demonstrates a basic Python print function. It also includes the `%%time` IPython magic command, which measures the execution time of the entire cell in an IPython environment (like Jupyter notebooks). This is useful for quick performance profiling.

SOURCE: https://github.com/psf/black/blob/main/tests/data/jupyter/notebook\_trailing\_newline.ipynb#\_snippet\_0



LANGUAGE: python

CODE:

```

%%time



print('foo')

```



----------------------------------------



TITLE: Black's Removal of Backslashes for Short Conditions

DESCRIPTION: Demonstrates Black's preference for parentheses over backslashes. For short logical expressions that can fit on a single line, it removes backslashes and consolidates the expression.

SOURCE: https://github.com/psf/black/blob/main/docs/the\_black\_code\_style/current\_style.md#\_snippet\_3



LANGUAGE: python

CODE:

```

\# in:



if some\_short\_rule1 \\

&nbsp; and some\_short\_rule2:

&nbsp;     ...

```



LANGUAGE: python

CODE:

```

\# out:



if some\_short\_rule1 and some\_short\_rule2:

&nbsp; ...

```



----------------------------------------



TITLE: Python Grammar: Expanded Variable Argument List Definition

DESCRIPTION: Presents the complete, expanded grammar rule for `varargslist`, which describes the parsing of function arguments without type hints, covering positional-only, positional-or-keyword, variable positional, and keyword-only arguments.

SOURCE: https://github.com/psf/black/blob/main/src/blib2to3/Grammar.txt#\_snippet\_5



LANGUAGE: Python Grammar

CODE:

```

varargslist: vfpdef \['=' test ](',' vfpdef \['=' test])\* ',' '/' \[',' \[

&nbsp;                    ((vfpdef \['=' test] ',')\* ('\*' \[vname] (',' vname \['=' test])\*

&nbsp;                           \[',' \['\*\*' vname \[',']]] | '\*\*' vname \[','])

&nbsp;                           | vfpdef \['=' test] (',' vfpdef \['=' test])\* \[','])

&nbsp;                    ]] | ((vfpdef \['=' test] ',')\*

&nbsp;                    ('\*' \[vname] (',' vname \['=' test])\*  \[',' \['\*\*' vname \[',']]]| '\*\*' vname \[','])

&nbsp;                    | vfpdef \['=' test] (',' vfpdef \['=' test])\* \[','])

```



----------------------------------------



TITLE: Black's Removal of Backslashes for Long Conditions

DESCRIPTION: Illustrates how Black replaces backslashes with parentheses for long logical expressions, wrapping them across multiple lines. This improves readability and avoids the brittle nature of backslashes in Python's grammar.

SOURCE: https://github.com/psf/black/blob/main/docs/the\_black\_code\_style/current\_style.md#\_snippet\_4



LANGUAGE: python

CODE:

```

\# in:



if some\_long\_rule1 \\

&nbsp; and some\_long\_rule2:

&nbsp;   ...

```



LANGUAGE: python

CODE:

```

\# out:



if (

&nbsp;   some\_long\_rule1

&nbsp;   and some\_long\_rule2

):

&nbsp;   ...

```



----------------------------------------



TITLE: Python Grammar: Helper Rules for Variable Arguments

DESCRIPTION: Defines auxiliary grammar rules used within `varargslist` for parsing variable names (`vname`) and variable function parameter definitions (`vfpdef`, `vfplist`).

SOURCE: https://github.com/psf/black/blob/main/src/blib2to3/Grammar.txt#\_snippet\_6



LANGUAGE: Python Grammar

CODE:

```

vname: NAME

vfpdef: vname | '(' vfplist ')'

vfplist: vfpdef (',' vfpdef)\* \[',']

```



----------------------------------------



TITLE: Black Formatter: Empty Line Handling in Python Functions

DESCRIPTION: This example demonstrates how Black reformats Python code to manage empty lines. It shows that empty lines within parenthesized expressions are removed, while single empty lines inside functions are preserved. It also illustrates how Black enforces proper spacing between function definitions, ensuring consistency and adherence to PEP 8 guidelines.

SOURCE: https://github.com/psf/black/blob/main/docs/the\_black\_code\_style/current\_style.md#\_snippet\_5



LANGUAGE: python

CODE:

```

\# in:



def function(

&nbsp;   some\_argument: int,



&nbsp;   other\_argument: int = 5,

) -> EmptyLineInParenWillBeDeleted:







&nbsp;   print("One empty line above me will be kept!")



def this\_is\_okay\_too():

&nbsp;   print("No empty line here")

\# out:



def function(

&nbsp;   some\_argument: int,

&nbsp;   other\_argument: int = 5,

) -> EmptyLineInParenWillBeDeleted:



&nbsp;   print("One empty line above me will be kept!")





def this\_is\_okay\_too():

&nbsp;   print("No empty line here")

```

