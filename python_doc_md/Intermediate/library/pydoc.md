# `!pydoc`{.interpreted-text role="mod"} \-\-- Documentation generator and online help system

::: {.module synopsis="Documentation generator and online help system."}
pydoc
:::

**Source code:** `Lib/pydoc.py`{.interpreted-text role="source"}

::: index
single: documentation; generation single: documentation; online single: help; online
:::

------------------------------------------------------------------------

The `!pydoc`{.interpreted-text role="mod"} module automatically generates documentation from Python modules. The documentation can be presented as pages of text on the console, served to a web browser, or saved to HTML files.

For modules, classes, functions and methods, the displayed documentation is derived from the docstring (i.e. the `~definition.__doc__`{.interpreted-text role="attr"} attribute) of the object, and recursively of its documentable members. If there is no docstring, `!pydoc`{.interpreted-text role="mod"} tries to obtain a description from the block of comment lines just above the definition of the class, function or method in the source file, or at the top of the module (see `inspect.getcomments`{.interpreted-text role="func"}).

The built-in function `help`{.interpreted-text role="func"} invokes the online help system in the interactive interpreter, which uses `!pydoc`{.interpreted-text role="mod"} to generate its documentation as text on the console. The same text documentation can also be viewed from outside the Python interpreter by running `pydoc`{.interpreted-text role="program"} as a script at the operating system\'s command prompt. For example, running :

    python -m pydoc sys

at a shell prompt will display documentation on the `sys`{.interpreted-text role="mod"} module, in a style similar to the manual pages shown by the Unix `man`{.interpreted-text role="program"} command. The argument to `pydoc`{.interpreted-text role="program"} can be the name of a function, module, or package, or a dotted reference to a class, method, or function within a module or module in a package. If the argument to `pydoc`{.interpreted-text role="program"} looks like a path (that is, it contains the path separator for your operating system, such as a slash in Unix), and refers to an existing Python source file, then documentation is produced for that file.

:::: note
::: title
Note
:::

In order to find objects and their documentation, `!pydoc`{.interpreted-text role="mod"} imports the module(s) to be documented. Therefore, any code on module level will be executed on that occasion. Use an `if __name__ == '__main__':` guard to only execute code when a file is invoked as a script and not just imported.
::::

When printing output to the console, `pydoc`{.interpreted-text role="program"} attempts to paginate the output for easier reading. If either the `MANPAGER`{.interpreted-text role="envvar"} or the `PAGER`{.interpreted-text role="envvar"} environment variable is set, `pydoc`{.interpreted-text role="program"} will use its value as a pagination program. When both are set, `MANPAGER`{.interpreted-text role="envvar"} is used.

Specifying a `-w` flag before the argument will cause HTML documentation to be written out to a file in the current directory, instead of displaying text on the console.

Specifying a `-k` flag before the argument will search the synopsis lines of all available modules for the keyword given as the argument, again in a manner similar to the Unix `man`{.interpreted-text role="program"} command. The synopsis line of a module is the first line of its documentation string.

You can also use `pydoc`{.interpreted-text role="program"} to start an HTTP server on the local machine that will serve documentation to visiting web browsers. `python -m pydoc -p 1234`{.interpreted-text role="program"} will start a HTTP server on port 1234, allowing you to browse the documentation at `http://localhost:1234/` in your preferred web browser. Specifying `0` as the port number will select an arbitrary unused port.

`python -m pydoc -n <hostname>`{.interpreted-text role="program"} will start the server listening at the given hostname. By default the hostname is \'localhost\' but if you want the server to be reached from other machines, you may want to change the host name that the server responds to. During development this is especially useful if you want to run pydoc from within a container.

`python -m pydoc -b`{.interpreted-text role="program"} will start the server and additionally open a web browser to a module index page. Each served page has a navigation bar at the top where you can *Get* help on an individual item, *Search* all modules with a keyword in their synopsis line, and go to the *Module index*, *Topics* and *Keywords* pages.

When `pydoc`{.interpreted-text role="program"} generates documentation, it uses the current environment and path to locate modules. Thus, invoking `pydoc spam`{.interpreted-text role="program"} documents precisely the version of the module you would get if you started the Python interpreter and typed `import spam`.

Module docs for core modules are assumed to reside in `https://docs.python.org/X.Y/library/` where `X` and `Y` are the major and minor version numbers of the Python interpreter. This can be overridden by setting the `!PYTHONDOCS`{.interpreted-text role="envvar"} environment variable to a different URL or to a local directory containing the Library Reference Manual pages.

::: versionchanged
3.2 Added the `-b` option.
:::

::: versionchanged
3.3 The `-g` command line option was removed.
:::

::: versionchanged
3.4 `!pydoc`{.interpreted-text role="mod"} now uses `inspect.signature`{.interpreted-text role="func"} rather than `inspect.getfullargspec`{.interpreted-text role="func"} to extract signature information from callables.
:::

::: versionchanged
3.7 Added the `-n` option.
:::
