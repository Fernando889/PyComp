# `!site`{.interpreted-text role="mod"} \-\-- Site-specific configuration hook

::: {.module synopsis="Module responsible for site-specific configuration."}
site
:::

**Source code:** `Lib/site.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

**This module is automatically imported during initialization.** The automatic import can be suppressed using the interpreter\'s `-S`{.interpreted-text role="option"} option.

::: index
triple: module; search; path
:::

Importing this module normally appends site-specific paths to the module search path and adds `callables <site-consts>`{.interpreted-text role="ref"}, including `help`{.interpreted-text role="func"} to the built-in namespace. However, Python startup option `-S`{.interpreted-text role="option"} blocks this and this module can be safely imported with no automatic modifications to the module search path or additions to the builtins. To explicitly trigger the usual site-specific additions, call the `main`{.interpreted-text role="func"} function.

::: versionchanged
3.3 Importing the module used to trigger paths manipulation even when using `-S`{.interpreted-text role="option"}.
:::

::: index
pair: site-packages; directory
:::

It starts by constructing up to four directories from a head and a tail part. For the head part, it uses `sys.prefix` and `sys.exec_prefix`; empty heads are skipped. For the tail part, it uses the empty string and then `lib/site-packages`{.interpreted-text role="file"} (on Windows) or `lib/python{X.Y[t]}/site-packages`{.interpreted-text role="file"} (on Unix and macOS). (The optional suffix \"t\" indicates the `free-threaded build`{.interpreted-text role="term"}, and is appended if `"t"` is present in the `sys.abiflags`{.interpreted-text role="data"} constant.) For each of the distinct head-tail combinations, it sees if it refers to an existing directory, and if so, adds it to `sys.path` and also inspects the newly added path for configuration files.

::: versionchanged
3.5 Support for the \"site-python\" directory has been removed.
:::

::: versionchanged
3.13 On Unix, `Free threading <free threading>`{.interpreted-text role="term"} Python installations are identified by the \"t\" suffix in the version-specific directory name, such as `lib/python3.13t/`{.interpreted-text role="file"}.
:::

::: versionchanged
3.14

`!site`{.interpreted-text role="mod"} is no longer responsible for updating `sys.prefix`{.interpreted-text role="data"} and `sys.exec_prefix`{.interpreted-text role="data"} on `sys-path-init-virtual-environments`{.interpreted-text role="ref"}. This is now done during the `path initialization <sys-path-init>`{.interpreted-text role="ref"}. As a result, under `sys-path-init-virtual-environments`{.interpreted-text role="ref"}, `sys.prefix`{.interpreted-text role="data"} and `sys.exec_prefix`{.interpreted-text role="data"} no longer depend on the `!site`{.interpreted-text role="mod"} initialization, and are therefore unaffected by `-S`{.interpreted-text role="option"}.
:::

::: {#site-virtual-environments-configuration}
When running under a `virtual environment <sys-path-init-virtual-environments>`{.interpreted-text role="ref"}, the `pyvenv.cfg` file in `sys.prefix`{.interpreted-text role="data"} is checked for site-specific configurations. If the `include-system-site-packages` key exists and is set to `true` (case-insensitive), the system-level prefixes will be searched for site-packages, otherwise they won\'t.
:::

::: index
single: \# (hash); comment pair: statement; import
:::

A path configuration file is a file whose name has the form `{name}.pth`{.interpreted-text role="file"} and exists in one of the four directories mentioned above; its contents are additional items (one per line) to be added to `sys.path`. Non-existing items are never added to `sys.path`, and no check is made that the item refers to a directory rather than a file. No item is added to `sys.path` more than once. Blank lines and lines beginning with `#` are skipped. Lines starting with `import` (followed by space or tab) are executed.

:::: note
::: title
Note
:::

An executable line in a `.pth`{.interpreted-text role="file"} file is run at every Python startup, regardless of whether a particular module is actually going to be used. Its impact should thus be kept to a minimum. The primary intended purpose of executable lines is to make the corresponding module(s) importable (load 3rd-party import hooks, adjust `PATH`{.interpreted-text role="envvar"} etc). Any other initialization is supposed to be done upon a module\'s actual import, if and when it happens. Limiting a code chunk to a single line is a deliberate measure to discourage putting anything more complex here.
::::

::: versionchanged
3.13 The `.pth`{.interpreted-text role="file"} files are now decoded by UTF-8 at first and then by the `locale encoding`{.interpreted-text role="term"} if it fails.
:::

::: index
single: package triple: path; configuration; file
:::

For example, suppose `sys.prefix` and `sys.exec_prefix` are set to `/usr/local`{.interpreted-text role="file"}. The Python X.Y library is then installed in `/usr/local/lib/python{X.Y}`{.interpreted-text role="file"}. Suppose this has a subdirectory `/usr/local/lib/python{X.Y}/site-packages`{.interpreted-text role="file"} with three subsubdirectories, `foo`{.interpreted-text role="file"}, `bar`{.interpreted-text role="file"} and `spam`{.interpreted-text role="file"}, and two path configuration files, `foo.pth`{.interpreted-text role="file"} and `bar.pth`{.interpreted-text role="file"}. Assume `foo.pth`{.interpreted-text role="file"} contains the following:

``` none
# foo package configuration

foo
bar
bletch
```

and `bar.pth`{.interpreted-text role="file"} contains:

``` none
# bar package configuration

bar
```

Then the following version-specific directories are added to `sys.path`, in this order:

``` none
/usr/local/lib/pythonX.Y/site-packages/bar
/usr/local/lib/pythonX.Y/site-packages/foo
```

Note that `bletch`{.interpreted-text role="file"} is omitted because it doesn\'t exist; the `bar`{.interpreted-text role="file"} directory precedes the `foo`{.interpreted-text role="file"} directory because `bar.pth`{.interpreted-text role="file"} comes alphabetically before `foo.pth`{.interpreted-text role="file"}; and `spam`{.interpreted-text role="file"} is omitted because it is not mentioned in either path configuration file.

## `!sitecustomize`{.interpreted-text role="mod"}

::: module
sitecustomize
:::

After these path manipulations, an attempt is made to import a module named `!sitecustomize`{.interpreted-text role="mod"}, which can perform arbitrary site-specific customizations. It is typically created by a system administrator in the site-packages directory. If this import fails with an `ImportError`{.interpreted-text role="exc"} or its subclass exception, and the exception\'s `~ImportError.name`{.interpreted-text role="attr"} attribute equals `'sitecustomize'`, it is silently ignored. If Python is started without output streams available, as with `pythonw.exe`{.interpreted-text role="file"} on Windows (which is used by default to start IDLE), attempted output from `!sitecustomize`{.interpreted-text role="mod"} is ignored. Any other exception causes a silent and perhaps mysterious failure of the process.

## `!usercustomize`{.interpreted-text role="mod"}

::: module
usercustomize
:::

After this, an attempt is made to import a module named `!usercustomize`{.interpreted-text role="mod"}, which can perform arbitrary user-specific customizations, if `~site.ENABLE_USER_SITE`{.interpreted-text role="data"} is true. This file is intended to be created in the user site-packages directory (see below), which is part of `sys.path` unless disabled by `-s`{.interpreted-text role="option"}. If this import fails with an `ImportError`{.interpreted-text role="exc"} or its subclass exception, and the exception\'s `~ImportError.name`{.interpreted-text role="attr"} attribute equals `'usercustomize'`, it is silently ignored.

Note that for some non-Unix systems, `sys.prefix` and `sys.exec_prefix` are empty, and the path manipulations are skipped; however the import of `sitecustomize`{.interpreted-text role="mod"} and `!usercustomize`{.interpreted-text role="mod"} is still attempted.

::: currentmodule
site
:::

## Readline configuration {#rlcompleter-config}

On systems that support `readline`{.interpreted-text role="mod"}, this module will also import and configure the `rlcompleter`{.interpreted-text role="mod"} module, if Python is started in `interactive mode <tut-interactive>`{.interpreted-text role="ref"} and without the `-S`{.interpreted-text role="option"} option. The default behavior is to enable tab completion and to use `~/.python_history`{.interpreted-text role="file"} as the history save file. To disable it, delete (or override) the `sys.__interactivehook__`{.interpreted-text role="data"} attribute in your `sitecustomize`{.interpreted-text role="mod"} or `usercustomize`{.interpreted-text role="mod"} module or your `PYTHONSTARTUP`{.interpreted-text role="envvar"} file.

::: versionchanged
3.4 Activation of rlcompleter and history was made automatic.
:::

## Module contents

::: data
PREFIXES

A list of prefixes for site-packages directories.
:::

::: data
ENABLE_USER_SITE

Flag showing the status of the user site-packages directory. `True` means that it is enabled and was added to `sys.path`. `False` means that it was disabled by user request (with `-s`{.interpreted-text role="option"} or `PYTHONNOUSERSITE`{.interpreted-text role="envvar"}). `None` means it was disabled for security reasons (mismatch between user or group id and effective id) or by an administrator.
:::

::: data
USER_SITE

Path to the user site-packages for the running Python. Can be `None` if `getusersitepackages`{.interpreted-text role="func"} hasn\'t been called yet. Default value is `~/.local/lib/python{X.Y}[t]/site-packages`{.interpreted-text role="file"} for UNIX and non-framework macOS builds, `~/Library/Python/{X.Y}/lib/python/site-packages`{.interpreted-text role="file"} for macOS framework builds, and `{%APPDATA%}\\Python\\Python{XY}\\site-packages`{.interpreted-text role="file"} on Windows. The optional \"t\" indicates the free-threaded build. This directory is a site directory, which means that `.pth`{.interpreted-text role="file"} files in it will be processed.
:::

::: data
USER_BASE

Path to the base directory for the user site-packages. Can be `None` if `getuserbase`{.interpreted-text role="func"} hasn\'t been called yet. Default value is `~/.local`{.interpreted-text role="file"} for UNIX and macOS non-framework builds, `~/Library/Python/{X.Y}`{.interpreted-text role="file"} for macOS framework builds, and `{%APPDATA%}\\Python`{.interpreted-text role="file"} for Windows. This value is used to compute the installation directories for scripts, data files, Python modules, etc. for the `user installation scheme <sysconfig-user-scheme>`{.interpreted-text role="ref"}. See also `PYTHONUSERBASE`{.interpreted-text role="envvar"}.
:::

:::: function
main()

Adds all the standard site-specific directories to the module search path. This function is called automatically when this module is imported, unless the Python interpreter was started with the `-S`{.interpreted-text role="option"} flag.

::: versionchanged
3.3 This function used to be called unconditionally.
:::
::::

::: function
addsitedir(sitedir, known_paths=None)

Add a directory to sys.path and process its `.pth`{.interpreted-text role="file"} files. Typically used in `sitecustomize`{.interpreted-text role="mod"} or `usercustomize`{.interpreted-text role="mod"} (see above).
:::

:::: function
getsitepackages()

Return a list containing all global site-packages directories.

::: versionadded
3.2
:::
::::

:::: function
getuserbase()

Return the path of the user base directory, `USER_BASE`{.interpreted-text role="data"}. If it is not initialized yet, this function will also set it, respecting `PYTHONUSERBASE`{.interpreted-text role="envvar"}.

::: versionadded
3.2
:::
::::

:::: function
getusersitepackages()

Return the path of the user-specific site-packages directory, `USER_SITE`{.interpreted-text role="data"}. If it is not initialized yet, this function will also set it, respecting `USER_BASE`{.interpreted-text role="data"}. To determine if the user-specific site-packages was added to `sys.path` `ENABLE_USER_SITE`{.interpreted-text role="data"} should be used.

::: versionadded
3.2
:::
::::

## Command-line interface {#site-commandline}

::: program
site
:::

The `!site`{.interpreted-text role="mod"} module also provides a way to get the user directories from the command line:

``` shell-session
$ python -m site --user-site
/home/user/.local/lib/python3.11/site-packages
```

If it is called without arguments, it will print the contents of `sys.path`{.interpreted-text role="data"} on the standard output, followed by the value of `USER_BASE`{.interpreted-text role="data"} and whether the directory exists, then the same thing for `USER_SITE`{.interpreted-text role="data"}, and finally the value of `ENABLE_USER_SITE`{.interpreted-text role="data"}.

::: option

`--user-base`

:   

Print the path to the user base directory.
:::

::: option

`--user-site`

:   

Print the path to the user site-packages directory.
:::

If both options are given, user base and user site will be printed (always in this order), separated by `os.pathsep`{.interpreted-text role="data"}.

If any option is given, the script will exit with one of these values: `0` if the user site-packages directory is enabled, `1` if it was disabled by the user, `2` if it is disabled for security reasons or by an administrator, and a value greater than 2 if there is an error.

::: seealso
- `370`{.interpreted-text role="pep"} \-- Per user site-packages directory
- `sys-path-init`{.interpreted-text role="ref"} \-- The initialization of `sys.path`{.interpreted-text role="data"}.
:::
