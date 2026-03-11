# `!pkgutil`{.interpreted-text role="mod"} \-\-- Package extension utility

::: {.module synopsis="Utilities for the import system."}
pkgutil
:::

**Source code:** `Lib/pkgutil.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module provides utilities for the import system, in particular package support.

:::: {.ModuleInfo(module_finder, .name, .ispkg)}
A namedtuple that holds a brief summary of a module\'s info.

::: versionadded
3.6
:::
::::

::: function
extend_path(path, name)

Extend the search path for the modules which comprise a package. Intended use is to place the following code in a package\'s `__init__.py`{.interpreted-text role="file"}:

    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

For each directory on `sys.path`{.interpreted-text role="data"} that has a subdirectory that matches the package name, add the subdirectory to the package\'s `~module.__path__`{.interpreted-text role="attr"}. This is useful if one wants to distribute different parts of a single logical package as multiple directories.

It also looks for `\*.pkg`{.interpreted-text role="file"} files beginning where `*` matches the *name* argument. This feature is similar to `\*.pth`{.interpreted-text role="file"} files (see the `site`{.interpreted-text role="mod"} module for more information), except that it doesn\'t special-case lines starting with `import`. A `\*.pkg`{.interpreted-text role="file"} file is trusted at face value: apart from skipping blank lines and ignoring comments, all entries found in a `\*.pkg`{.interpreted-text role="file"} file are added to the path, regardless of whether they exist on the filesystem (this is a feature).

If the input path is not a list (as is the case for frozen packages) it is returned unchanged. The input path is not modified; an extended copy is returned. Items are only appended to the copy at the end.

It is assumed that `sys.path`{.interpreted-text role="data"} is a sequence. Items of `sys.path`{.interpreted-text role="data"} that are not strings referring to existing directories are ignored. Unicode items on `sys.path`{.interpreted-text role="data"} that cause errors when used as filenames may cause this function to raise an exception (in line with `os.path.isdir`{.interpreted-text role="func"} behavior).
:::

:::: function
get_importer(path_item)

Retrieve a `finder`{.interpreted-text role="term"} for the given *path_item*.

The returned finder is cached in `sys.path_importer_cache`{.interpreted-text role="data"} if it was newly created by a path hook.

The cache (or part of it) can be cleared manually if a rescan of `sys.path_hooks`{.interpreted-text role="data"} is necessary.

::: versionchanged
3.3 Updated to be based directly on `importlib`{.interpreted-text role="mod"} rather than relying on the package internal `302`{.interpreted-text role="pep"} import emulation.
:::
::::

:::: function
iter_importers(fullname=\'\')

Yield `finder`{.interpreted-text role="term"} objects for the given module name.

If *fullname* contains a `'.'`, the finders will be for the package containing *fullname*, otherwise they will be all registered top level finders (i.e. those on both `sys.meta_path`{.interpreted-text role="data"} and `sys.path_hooks`{.interpreted-text role="data"}).

If the named module is in a package, that package is imported as a side effect of invoking this function.

If no module name is specified, all top level finders are produced.

::: versionchanged
3.3 Updated to be based directly on `importlib`{.interpreted-text role="mod"} rather than relying on the package internal `302`{.interpreted-text role="pep"} import emulation.
:::
::::

:::::: function
iter_modules(path=None, prefix=\'\')

Yields `ModuleInfo`{.interpreted-text role="class"} for all submodules on *path*, or, if *path* is `None`, all top-level modules on `sys.path`{.interpreted-text role="data"}.

*path* should be either `None` or a list of paths to look for modules in.

*prefix* is a string to output on the front of every module name on output.

:::: note
::: title
Note
:::

Only works for a `finder`{.interpreted-text role="term"} which defines an `iter_modules()` method. This interface is non-standard, so the module also provides implementations for `importlib.machinery.FileFinder`{.interpreted-text role="class"} and `zipimport.zipimporter`{.interpreted-text role="class"}.
::::

::: versionchanged
3.3 Updated to be based directly on `importlib`{.interpreted-text role="mod"} rather than relying on the package internal `302`{.interpreted-text role="pep"} import emulation.
:::
::::::

:::::: function
walk_packages(path=None, prefix=\'\', onerror=None)

Yields `ModuleInfo`{.interpreted-text role="class"} for all modules recursively on *path*, or, if *path* is `None`, all accessible modules.

*path* should be either `None` or a list of paths to look for modules in.

*prefix* is a string to output on the front of every module name on output.

Note that this function must import all *packages* (*not* all modules!) on the given *path*, in order to access the `__path__` attribute to find submodules.

*onerror* is a function which gets called with one argument (the name of the package which was being imported) if any exception occurs while trying to import a package. If no *onerror* function is supplied, `ImportError`{.interpreted-text role="exc"}s are caught and ignored, while all other exceptions are propagated, terminating the search.

Examples:

    # list all modules python can access
    walk_packages()

    # list all submodules of ctypes
    walk_packages(ctypes.__path__, ctypes.__name__ + '.')

:::: note
::: title
Note
:::

Only works for a `finder`{.interpreted-text role="term"} which defines an `iter_modules()` method. This interface is non-standard, so the module also provides implementations for `importlib.machinery.FileFinder`{.interpreted-text role="class"} and `zipimport.zipimporter`{.interpreted-text role="class"}.
::::

::: versionchanged
3.3 Updated to be based directly on `importlib`{.interpreted-text role="mod"} rather than relying on the package internal `302`{.interpreted-text role="pep"} import emulation.
:::
::::::

::: function
get_data(package, resource)

Get a resource from a package.

This is a wrapper for the `loader`{.interpreted-text role="term"} `get_data <importlib.abc.ResourceLoader.get_data>`{.interpreted-text role="meth"} API. The *package* argument should be the name of a package, in standard module format (`foo.bar`). The *resource* argument should be in the form of a relative filename, using `/` as the path separator. The parent directory name `..` is not allowed, and nor is a rooted name (starting with a `/`).

The function returns a binary string that is the contents of the specified resource.

For packages located in the filesystem, which have already been imported, this is the rough equivalent of:

    d = os.path.dirname(sys.modules[package].__file__)
    data = open(os.path.join(d, resource), 'rb').read()

If the package cannot be located or loaded, or it uses a `loader`{.interpreted-text role="term"} which does not support `get_data <importlib.abc.ResourceLoader.get_data>`{.interpreted-text role="meth"}, then `None` is returned. In particular, the `loader`{.interpreted-text role="term"} for `namespace packages <namespace package>`{.interpreted-text role="term"} does not support `get_data <importlib.abc.ResourceLoader.get_data>`{.interpreted-text role="meth"}.
:::

:::: function
resolve_name(name)

Resolve a name to an object.

This functionality is used in numerous places in the standard library (see `12915`{.interpreted-text role="issue"}) - and equivalent functionality is also in widely used third-party packages such as setuptools, Django and Pyramid.

It is expected that *name* will be a string in one of the following formats, where W is shorthand for a valid Python identifier and dot stands for a literal period in these pseudo-regexes:

- `W(.W)*`
- `W(.W)*:(W(.W)*)?`

The first form is intended for backward compatibility only. It assumes that some part of the dotted name is a package, and the rest is an object somewhere within that package, possibly nested inside other objects. Because the place where the package stops and the object hierarchy starts can\'t be inferred by inspection, repeated attempts to import must be done with this form.

In the second form, the caller makes the division point clear through the provision of a single colon: the dotted name to the left of the colon is a package to be imported, and the dotted name to the right is the object hierarchy within that package. Only one import is needed in this form. If it ends with the colon, then a module object is returned.

The function will return an object (which might be a module), or raise one of the following exceptions:

`ValueError`{.interpreted-text role="exc"} \-- if *name* isn\'t in a recognised format.

`ImportError`{.interpreted-text role="exc"} \-- if an import failed when it shouldn\'t have.

`AttributeError`{.interpreted-text role="exc"} \-- If a failure occurred when traversing the object hierarchy within the imported package to get to the desired object.

::: versionadded
3.9
:::
::::
