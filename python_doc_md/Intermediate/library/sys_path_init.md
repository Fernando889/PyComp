# The initialization of the `sys.path`{.interpreted-text role="data"} module search path {#sys-path-init}

A module search path is initialized when Python starts. This module search path may be accessed at `sys.path`{.interpreted-text role="data"}.

The first entry in the module search path is the directory that contains the input script, if there is one. Otherwise, the first entry is the current directory, which is the case when executing the interactive shell, a `-c`{.interpreted-text role="option"} command, or `-m`{.interpreted-text role="option"} module.

The `PYTHONPATH`{.interpreted-text role="envvar"} environment variable is often used to add directories to the search path. If this environment variable is found then the contents are added to the module search path.

:::: note
::: title
Note
:::

`PYTHONPATH`{.interpreted-text role="envvar"} will affect all installed Python versions/environments. Be wary of setting this in your shell profile or global environment variables. The `site`{.interpreted-text role="mod"} module offers more nuanced techniques as mentioned below.
::::

The next items added are the directories containing standard Python modules as well as any `extension module`{.interpreted-text role="term"}s that these modules depend on. Extension modules are `.pyd` files on Windows and `.so` files on other platforms. The directory with the platform-independent Python modules is called `prefix`. The directory with the extension modules is called `exec_prefix`.

The `PYTHONHOME`{.interpreted-text role="envvar"} environment variable may be used to set the `prefix` and `exec_prefix` locations. Otherwise these directories are found by using the Python executable as a starting point and then looking for various \'landmark\' files and directories. Note that any symbolic links are followed so the real Python executable location is used as the search starting point. The Python executable location is called `home`.

Once `home` is determined, the `prefix` directory is found by first looking for `python{majorversion}{minorversion}.zip`{.interpreted-text role="file"} (`python311.zip`). On Windows the zip archive is searched for in `home` and on Unix the archive is expected to be in `lib`{.interpreted-text role="file"}. Note that the expected zip archive location is added to the module search path even if the archive does not exist. If no archive was found, Python on Windows will continue the search for `prefix` by looking for `Lib\\os.py`{.interpreted-text role="file"}. Python on Unix will look for `lib/python{majorversion}.{minorversion}/os.py`{.interpreted-text role="file"} (`lib/python3.11/os.py`). On Windows `prefix` and `exec_prefix` are the same, however on other platforms `lib/python{majorversion}.{minorversion}/lib-dynload`{.interpreted-text role="file"} (`lib/python3.11/lib-dynload`) is searched for and used as an anchor for `exec_prefix`. On some platforms `lib`{.interpreted-text role="file"} may be `lib64`{.interpreted-text role="file"} or another value, see `sys.platlibdir`{.interpreted-text role="data"} and `PYTHONPLATLIBDIR`{.interpreted-text role="envvar"}.

Once found, `prefix` and `exec_prefix` are available at `sys.base_prefix`{.interpreted-text role="data"} and `sys.base_exec_prefix`{.interpreted-text role="data"} respectively.

If `PYTHONHOME`{.interpreted-text role="envvar"} is not set, and a `pyvenv.cfg` file is found alongside the main executable, or in its parent directory, `sys.prefix`{.interpreted-text role="data"} and `sys.exec_prefix`{.interpreted-text role="data"} get set to the directory containing `pyvenv.cfg`, otherwise they are set to the same value as `sys.base_prefix`{.interpreted-text role="data"} and `sys.base_exec_prefix`{.interpreted-text role="data"}, respectively. This is used by `sys-path-init-virtual-environments`{.interpreted-text role="ref"}.

Finally, the `site`{.interpreted-text role="mod"} module is processed and `site-packages`{.interpreted-text role="file"} directories are added to the module search path. A common way to customize the search path is to create `sitecustomize`{.interpreted-text role="mod"} or `usercustomize`{.interpreted-text role="mod"} modules as described in the `site`{.interpreted-text role="mod"} module documentation.

:::: note
::: title
Note
:::

Certain command line options may further affect path calculations. See `-E`{.interpreted-text role="option"}, `-I`{.interpreted-text role="option"}, `-s`{.interpreted-text role="option"} and `-S`{.interpreted-text role="option"} for further details.
::::

::: versionchanged
3.14

`sys.prefix`{.interpreted-text role="data"} and `sys.exec_prefix`{.interpreted-text role="data"} are now set to the `pyvenv.cfg` directory during the path initialization. This was previously done by `site`{.interpreted-text role="mod"}, therefore affected by `-S`{.interpreted-text role="option"}.
:::

## Virtual Environments {#sys-path-init-virtual-environments}

Virtual environments place a `pyvenv.cfg` file in their prefix, which causes `sys.prefix`{.interpreted-text role="data"} and `sys.exec_prefix`{.interpreted-text role="data"} to point to them, instead of the base installation.

The `prefix` and `exec_prefix` values of the base installation are available at `sys.base_prefix`{.interpreted-text role="data"} and `sys.base_exec_prefix`{.interpreted-text role="data"}.

As well as being used as a marker to identify virtual environments, `pyvenv.cfg` may also be used to configure the `site`{.interpreted-text role="mod"} initialization. Please refer to `site`{.interpreted-text role="mod"}\'s `virtual environments documentation <site-virtual-environments-configuration>`{.interpreted-text role="ref"}.

:::: note
::: title
Note
:::

`PYTHONHOME`{.interpreted-text role="envvar"} overrides the `pyvenv.cfg` detection.
::::

:::: note
::: title
Note
:::

There are other ways how \"virtual environments\" could be implemented, this documentation refers implementations based on the `pyvenv.cfg` mechanism, such as `venv`{.interpreted-text role="mod"}. Most virtual environment implementations follow the model set by `venv`{.interpreted-text role="mod"}, but there may be exotic implementations that diverge from it.
::::

## [pth]{#pth} files

To completely override `sys.path`{.interpreted-text role="data"} create a `._pth` file with the same name as the shared library or executable (`python._pth` or `python311._pth`). The shared library path is always known on Windows, however it may not be available on other platforms. In the `._pth` file specify one line for each path to add to `sys.path`{.interpreted-text role="data"}. The file based on the shared library name overrides the one based on the executable, which allows paths to be restricted for any program loading the runtime if desired.

When the file exists, all registry and environment variables are ignored, isolated mode is enabled, and `site`{.interpreted-text role="mod"} is not imported unless one line in the file specifies `import site`. Blank paths and lines starting with `#` are ignored. Each path may be absolute or relative to the location of the file. Import statements other than to `site` are not permitted, and arbitrary code cannot be specified.

Note that `.pth` files (without leading underscore) will be processed normally by the `site`{.interpreted-text role="mod"} module when `import site` has been specified.

## Embedded Python

If Python is embedded within another application `Py_InitializeFromConfig`{.interpreted-text role="c:func"} and the `PyConfig`{.interpreted-text role="c:type"} structure can be used to initialize Python. The path specific details are described at `init-path-config`{.interpreted-text role="ref"}.

::: seealso
- `windows_finding_modules`{.interpreted-text role="ref"} for detailed Windows notes.
- `using-on-unix`{.interpreted-text role="ref"} for Unix details.
:::
