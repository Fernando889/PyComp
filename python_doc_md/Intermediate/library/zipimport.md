# `!zipimport`{.interpreted-text role="mod"} \-\-- Import modules from Zip archives

::: {.module synopsis="Support for importing Python modules from ZIP archives."}
zipimport
:::

**Source code:** `Lib/zipimport.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module adds the ability to import Python modules (`\*.py`{.interpreted-text role="file"}, `\*.pyc`{.interpreted-text role="file"}) and packages from ZIP-format archives. It is usually not needed to use the `!zipimport`{.interpreted-text role="mod"} module explicitly; it is automatically used by the built-in `import`{.interpreted-text role="keyword"} mechanism for `sys.path`{.interpreted-text role="data"} items that are paths to ZIP archives.

Typically, `sys.path`{.interpreted-text role="data"} is a list of directory names as strings. This module also allows an item of `sys.path`{.interpreted-text role="data"} to be a string naming a ZIP file archive. The ZIP archive can contain a subdirectory structure to support package imports, and a path within the archive can be specified to only import from a subdirectory. For example, the path `example.zip/lib/`{.interpreted-text role="file"} would only import from the `lib/`{.interpreted-text role="file"} subdirectory within the archive.

Any files may be present in the ZIP archive, but importers are only invoked for `.py`{.interpreted-text role="file"} and `.pyc`{.interpreted-text role="file"} files. ZIP import of dynamic modules (`.pyd`{.interpreted-text role="file"}, `.so`{.interpreted-text role="file"}) is disallowed. Note that if an archive only contains `.py`{.interpreted-text role="file"} files, Python will not attempt to modify the archive by adding the corresponding `.pyc`{.interpreted-text role="file"} file, meaning that if a ZIP archive doesn\'t contain `.pyc`{.interpreted-text role="file"} files, importing may be rather slow.

::: versionchanged
3.15 Zstandard (*zstd*) compressed zip file entries are supported.
:::

::: versionchanged
3.13 ZIP64 is supported
:::

::: versionchanged
3.8 Previously, ZIP archives with an archive comment were not supported.
:::

::: seealso

[PKZIP Application Note](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)

:   Documentation on the ZIP file format by Phil Katz, the creator of the format and algorithms used.

`273`{.interpreted-text role="pep"} - Import Modules from Zip Archives

:   Written by James C. Ahlstrom, who also provided an implementation. Python 2.3 follows the specification in `273`{.interpreted-text role="pep"}, but uses an implementation written by Just van Rossum that uses the import hooks described in `302`{.interpreted-text role="pep"}.

`importlib`{.interpreted-text role="mod"} - The implementation of the import machinery

:   Package providing the relevant protocols for all importers to implement.
:::

This module defines an exception:

::: exception
ZipImportError

Exception raised by zipimporter objects. It\'s a subclass of `ImportError`{.interpreted-text role="exc"}, so it can be caught as `ImportError`{.interpreted-text role="exc"}, too.
:::

## zipimporter Objects

`zipimporter`{.interpreted-text role="class"} is the class for importing ZIP files.

::::::::::::::::::::: zipimporter(archivepath)
Create a new zipimporter instance. *archivepath* must be a path to a ZIP file, or to a specific path within a ZIP file. For example, an *archivepath* of `foo/bar.zip/lib`{.interpreted-text role="file"} will look for modules in the `lib`{.interpreted-text role="file"} directory inside the ZIP file `foo/bar.zip`{.interpreted-text role="file"} (provided that it exists).

`ZipImportError`{.interpreted-text role="exc"} is raised if *archivepath* doesn\'t point to a valid ZIP archive.

::: versionchanged
3.12

Methods `find_loader()` and `find_module()`, deprecated in 3.10 are now removed. Use `find_spec`{.interpreted-text role="meth"} instead.
:::

:::: method
create_module(spec)

Implementation of `importlib.abc.Loader.create_module`{.interpreted-text role="meth"} that returns `None`{.interpreted-text role="const"} to explicitly request the default semantics.

::: versionadded
3.10
:::
::::

:::: method
exec_module(module)

Implementation of `importlib.abc.Loader.exec_module`{.interpreted-text role="meth"}.

::: versionadded
3.10
:::
::::

:::: method
find_spec(fullname, target=None)

An implementation of `importlib.abc.PathEntryFinder.find_spec`{.interpreted-text role="meth"}.

::: versionadded
3.10
:::
::::

::: method
get_code(fullname)

Return the code object for the specified module. Raise `ZipImportError`{.interpreted-text role="exc"} if the module couldn\'t be imported.
:::

:::: method
get_data(pathname)

Return the data associated with *pathname*. Raise `OSError`{.interpreted-text role="exc"} if the file wasn\'t found.

::: versionchanged
3.3 `IOError`{.interpreted-text role="exc"} used to be raised, it is now an alias of `OSError`{.interpreted-text role="exc"}.
:::
::::

:::: method
get_filename(fullname)

Return the value `__file__` would be set to if the specified module was imported. Raise `ZipImportError`{.interpreted-text role="exc"} if the module couldn\'t be imported.

::: versionadded
3.1
:::
::::

::: method
get_source(fullname)

Return the source code for the specified module. Raise `ZipImportError`{.interpreted-text role="exc"} if the module couldn\'t be found, return `None`{.interpreted-text role="const"} if the archive does contain the module, but has no source for it.
:::

::: method
is_package(fullname)

Return `True` if the module specified by *fullname* is a package. Raise `ZipImportError`{.interpreted-text role="exc"} if the module couldn\'t be found.
:::

:::: method
invalidate_caches()

Clear out the internal cache of information about files found within the ZIP archive.

::: versionadded
3.10
:::
::::

::: attribute
archive

The file name of the importer\'s associated ZIP file, without a possible subpath.
:::

::: attribute
prefix

The subpath within the ZIP file where modules are searched. This is the empty string for zipimporter objects which point to the root of the ZIP file.
:::

The `archive`{.interpreted-text role="attr"} and `prefix`{.interpreted-text role="attr"} attributes, when combined with a slash, equal the original *archivepath* argument given to the `zipimporter`{.interpreted-text role="class"} constructor.
:::::::::::::::::::::

## Examples {#zipimport-examples}

Here is an example that imports a module from a ZIP archive - note that the `!zipimport`{.interpreted-text role="mod"} module is not explicitly used.

``` shell-session
$ unzip -l example_archive.zip
Archive:  example_archive.zip
  Length     Date   Time    Name
 --------    ----   ----    ----
     8467  01-01-00 12:30   example.py
 --------                   -------
     8467                   1 file
```

``` pycon
>>> import sys
>>> # Add the archive to the front of the module search path
>>> sys.path.insert(0, 'example_archive.zip')
>>> import example
>>> example.__file__
'example_archive.zip/example.py'
```
