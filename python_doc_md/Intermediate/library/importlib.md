# `!importlib`{.interpreted-text role="mod"} \-\-- The implementation of `!import`{.interpreted-text role="keyword"}

::: {.module synopsis="The implementation of the import machinery."}
importlib
:::

::: versionadded
3.1
:::

**Source code:** `Lib/importlib/__init__.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

## Introduction

The purpose of the `!importlib`{.interpreted-text role="mod"} package is three-fold.

One is to provide the implementation of the `import`{.interpreted-text role="keyword"} statement (and thus, by extension, the `__import__`{.interpreted-text role="func"} function) in Python source code. This provides an implementation of `!import`{.interpreted-text role="keyword"} which is portable to any Python interpreter. This also provides an implementation which is easier to comprehend than one implemented in a programming language other than Python.

Two, the components to implement `import`{.interpreted-text role="keyword"} are exposed in this package, making it easier for users to create their own custom objects (known generically as an `importer`{.interpreted-text role="term"}) to participate in the import process.

Three, the package contains modules exposing additional functionality for managing aspects of Python packages:

- `importlib.metadata`{.interpreted-text role="mod"} presents access to metadata from third-party distributions.
- `importlib.resources`{.interpreted-text role="mod"} provides routines for accessing non-code \"resources\" from Python packages.

::: seealso

`import`{.interpreted-text role="ref"}

:   The language reference for the `import`{.interpreted-text role="keyword"} statement.

[Packages specification](https://www.python.org/doc/essays/packages/)

:   Original specification of packages. Some semantics have changed since the writing of this document (e.g. redirecting based on `None` in `sys.modules`{.interpreted-text role="data"}).

The `.__import__`{.interpreted-text role="func"} function

:   The `import`{.interpreted-text role="keyword"} statement is syntactic sugar for this function.

`sys-path-init`{.interpreted-text role="ref"}

:   The initialization of `sys.path`{.interpreted-text role="data"}.

`235`{.interpreted-text role="pep"}

:   Import on Case-Insensitive Platforms

`263`{.interpreted-text role="pep"}

:   Defining Python Source Code Encodings

`302`{.interpreted-text role="pep"}

:   New Import Hooks

`328`{.interpreted-text role="pep"}

:   Imports: Multi-Line and Absolute/Relative

`366`{.interpreted-text role="pep"}

:   Main module explicit relative imports

`420`{.interpreted-text role="pep"}

:   Implicit namespace packages

`451`{.interpreted-text role="pep"}

:   A ModuleSpec Type for the Import System

`488`{.interpreted-text role="pep"}

:   Elimination of PYO files

`489`{.interpreted-text role="pep"}

:   Multi-phase extension module initialization

`552`{.interpreted-text role="pep"}

:   Deterministic pycs

`3120`{.interpreted-text role="pep"}

:   Using UTF-8 as the Default Source Encoding

`3147`{.interpreted-text role="pep"}

:   PYC Repository Directories
:::

## Functions

::::: function
\_\_import\_\_(name, globals=None, locals=None, fromlist=(), level=0)

An implementation of the built-in `__import__`{.interpreted-text role="func"} function.

:::: note
::: title
Note
:::

Programmatic importing of modules should use `import_module`{.interpreted-text role="func"} instead of this function.
::::
:::::

:::: function
import_module(name, package=None)

Import a module. The *name* argument specifies what module to import in absolute or relative terms (e.g. either `pkg.mod` or `..mod`). If the name is specified in relative terms, then the *package* argument must be set to the name of the package which is to act as the anchor for resolving the package name (e.g. `import_module('..mod', 'pkg.subpkg')` will import `pkg.mod`).

The `import_module`{.interpreted-text role="func"} function acts as a simplifying wrapper around `importlib.__import__`{.interpreted-text role="func"}. This means all semantics of the function are derived from `importlib.__import__`{.interpreted-text role="func"}. The most important difference between these two functions is that `import_module`{.interpreted-text role="func"} returns the specified package or module (e.g. `pkg.mod`), while `__import__`{.interpreted-text role="func"} returns the top-level package or module (e.g. `pkg`).

If you are dynamically importing a module that was created since the interpreter began execution (e.g., created a Python source file), you may need to call `invalidate_caches`{.interpreted-text role="func"} in order for the new module to be noticed by the import system.

If the module cannot be imported, `import_module`{.interpreted-text role="func"} will raise `ImportError`{.interpreted-text role="exc"} or an appropriate subclass like `ModuleNotFoundError`{.interpreted-text role="exc"}.

::: versionchanged
3.3 Parent packages are automatically imported.
:::
::::

::::: function
invalidate_caches()

Invalidate the internal caches of finders stored at `sys.meta_path`{.interpreted-text role="data"}. If a finder implements `invalidate_caches()` then it will be called to perform the invalidation. This function should be called if any modules are created/installed while your program is running to guarantee all finders will notice the new module\'s existence.

::: versionadded
3.3
:::

::: versionchanged
3.10 Namespace packages created/installed in a different `sys.path`{.interpreted-text role="data"} location after the same namespace was already imported are noticed.
:::
:::::

::::::: function
reload(module)

Reload a previously imported *module*. The argument must be a module object, so it must have been successfully imported before. This is useful if you have edited the module source file using an external editor and want to try out the new version without leaving the Python interpreter. The return value is the module object (which can be different if re-importing causes a different object to be placed in `sys.modules`{.interpreted-text role="data"}).

When `reload`{.interpreted-text role="func"} is executed:

- Python module\'s code is recompiled and the module-level code re-executed, defining a new set of objects which are bound to names in the module\'s dictionary by reusing the `loader`{.interpreted-text role="term"} which originally loaded the module. The `init` function of extension modules is not called a second time.
- As with all other objects in Python the old objects are only reclaimed after their reference counts drop to zero.
- The names in the module namespace are updated to point to any new or changed objects.
- Other references to the old objects (such as names external to the module) are not rebound to refer to the new objects and must be updated in each namespace where they occur if that is desired.

There are a number of other caveats:

When a module is reloaded, its dictionary (containing the module\'s global variables) is retained. Redefinitions of names will override the old definitions, so this is generally not a problem. If the new version of a module does not define a name that was defined by the old version, the old definition remains. This feature can be used to the module\'s advantage if it maintains a global table or cache of objects \-\-- with a `try`{.interpreted-text role="keyword"} statement it can test for the table\'s presence and skip its initialization if desired:

    try:
        cache
    except NameError:
        cache = {}

It is generally not very useful to reload built-in or dynamically loaded modules. Reloading `sys`{.interpreted-text role="mod"}, `__main__`{.interpreted-text role="mod"}, `builtins`{.interpreted-text role="mod"} and other key modules is not recommended. In many cases extension modules are not designed to be initialized more than once, and may fail in arbitrary ways when reloaded.

If a module imports objects from another module using `from`{.interpreted-text role="keyword"} \... `import`{.interpreted-text role="keyword"} \..., calling `reload`{.interpreted-text role="func"} for the other module does not redefine the objects imported from it \-\-- one way around this is to re-execute the `!from`{.interpreted-text role="keyword"} statement, another is to use `!import`{.interpreted-text role="keyword"} and qualified names (*module.name*) instead.

If a module instantiates instances of a class, reloading the module that defines the class does not affect the method definitions of the instances \-\-- they continue to use the old class definition. The same is true for derived classes.

::: versionadded
3.4
:::

::: versionchanged
3.7 `ModuleNotFoundError`{.interpreted-text role="exc"} is raised when the module being reloaded lacks a `~importlib.machinery.ModuleSpec`{.interpreted-text role="class"}.
:::

:::: warning
::: title
Warning
:::

This function is not thread-safe. Calling it from multiple threads can result in unexpected behavior. It\'s recommended to use the `threading.Lock`{.interpreted-text role="class"} or other synchronization primitives for thread-safe module reloading.
::::
:::::::

## `!importlib.abc`{.interpreted-text role="mod"} \-- Abstract base classes related to import

::: {.module synopsis="Abstract base classes related to import"}
importlib.abc
:::

**Source code:** `Lib/importlib/abc.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!importlib.abc`{.interpreted-text role="mod"} module contains all of the core abstract base classes used by `import`{.interpreted-text role="keyword"}. Some subclasses of the core abstract base classes are also provided to help in implementing the core ABCs.

ABC hierarchy:

    object
     +-- MetaPathFinder
     +-- PathEntryFinder
     +-- Loader
          +-- ResourceLoader --------+
          +-- InspectLoader          |
               +-- ExecutionLoader --+
                                     +-- FileLoader
                                     +-- SourceLoader

::::::::::::: MetaPathFinder
An abstract base class representing a `meta path finder`{.interpreted-text role="term"}.

::: versionadded
3.3
:::

::: versionchanged
3.10 No longer a subclass of `!Finder`{.interpreted-text role="class"}.
:::

:::: method
find_spec(fullname, path, target=None)

An abstract method for finding a `spec <module spec>`{.interpreted-text role="term"} for the specified module. If this is a top-level import, *path* will be `None`. Otherwise, this is a search for a subpackage or module and *path* will be the value of `~module.__path__`{.interpreted-text role="attr"} from the parent package. If a spec cannot be found, `None` is returned. When passed in, `target` is a module object that the finder may use to make a more educated guess about what spec to return. `importlib.util.spec_from_loader`{.interpreted-text role="func"} may be useful for implementing concrete `MetaPathFinders`.

::: versionadded
3.4
:::
::::

:::: method
invalidate_caches()

An optional method which, when called, should invalidate any internal cache used by the finder. Used by `importlib.invalidate_caches`{.interpreted-text role="func"} when invalidating the caches of all finders on `sys.meta_path`{.interpreted-text role="data"}.

::: versionchanged
3.4 Returns `None` when called instead of `NotImplemented`{.interpreted-text role="data"}.
:::
::::

:::::: method
discover(parent=None)

An optional method which searches for possible specs with given *parent* module spec. If *parent* is *None*, `MetaPathFinder.discover`{.interpreted-text role="meth"} will search for top-level modules.

Returns an iterable of possible specs.

Raises `ValueError`{.interpreted-text role="exc"} if *parent* is not a package module.

:::: warning
::: title
Warning
:::

This method can potentially yield a very large number of objects, and it may carry out IO operations when computing these values.

Because of this, it will generaly be desirable to compute the result values on-the-fly, as they are needed. As such, the returned object is only guaranteed to be an `iterable <collections.abc.Iterable>`{.interpreted-text role="class"}, instead of a `list`{.interpreted-text role="class"} or other `collection <collections.abc.Collection>`{.interpreted-text role="class"} type.
::::

::: versionadded
next
:::
::::::
:::::::::::::

:::::::::::: PathEntryFinder
An abstract base class representing a `path entry finder`{.interpreted-text role="term"}. Though it bears some similarities to `MetaPathFinder`{.interpreted-text role="class"}, `PathEntryFinder` is meant for use only within the path-based import subsystem provided by `importlib.machinery.PathFinder`{.interpreted-text role="class"}.

::: versionadded
3.3
:::

::: versionchanged
3.10 No longer a subclass of `!Finder`{.interpreted-text role="class"}.
:::

:::: method
find_spec(fullname, target=None)

An abstract method for finding a `spec <module spec>`{.interpreted-text role="term"} for the specified module. The finder will search for the module only within the `path entry`{.interpreted-text role="term"} to which it is assigned. If a spec cannot be found, `None` is returned. When passed in, `target` is a module object that the finder may use to make a more educated guess about what spec to return. `importlib.util.spec_from_loader`{.interpreted-text role="func"} may be useful for implementing concrete `PathEntryFinders`.

::: versionadded
3.4
:::
::::

::: method
invalidate_caches()

An optional method which, when called, should invalidate any internal cache used by the finder. Used by `importlib.machinery.PathFinder.invalidate_caches`{.interpreted-text role="meth"} when invalidating the caches of all cached finders.
:::

:::::: method
discover(parent=None)

An optional method which searches for possible specs with given *parent* module spec. If *parent* is *None*, `PathEntryFinder.discover`{.interpreted-text role="meth"} will search for top-level modules.

Returns an iterable of possible specs.

Raises `ValueError`{.interpreted-text role="exc"} if *parent* is not a package module.

:::: warning
::: title
Warning
:::

This method can potentially yield a very large number of objects, and it may carry out IO operations when computing these values.

Because of this, it will generaly be desirable to compute the result values on-the-fly, as they are needed. As such, the returned object is only guaranteed to be an `iterable <collections.abc.Iterable>`{.interpreted-text role="class"}, instead of a `list`{.interpreted-text role="class"} or other `collection <collections.abc.Collection>`{.interpreted-text role="class"} type.
::::

::: versionadded
next
:::
::::::
::::::::::::

::::::::::: Loader
An abstract base class for a `loader`{.interpreted-text role="term"}. See `302`{.interpreted-text role="pep"} for the exact definition for a loader.

Loaders that wish to support resource reading should implement a `get_resource_reader`{.interpreted-text role="meth"} method as specified by `importlib.resources.abc.ResourceReader`{.interpreted-text role="class"}.

::: versionchanged
3.7 Introduced the optional `get_resource_reader`{.interpreted-text role="meth"} method.
:::

::: versionchanged
3.15 Removed the `load_module()` method.
:::

::::: method
create_module(spec)

A method that returns the module object to use when importing a module. This method may return `None`, indicating that default module creation semantics should take place.

::: versionadded
3.4
:::

::: versionchanged
3.6 This method is no longer optional when `exec_module`{.interpreted-text role="meth"} is defined.
:::
:::::

::::: method
exec_module(module)

An abstract method that executes the module in its own namespace when a module is imported or reloaded. The module should already be initialized when `exec_module`{.interpreted-text role="meth"} is called. When this method exists, `create_module`{.interpreted-text role="meth"} must be defined.

::: versionadded
3.4
:::

::: versionchanged
3.6 `create_module`{.interpreted-text role="meth"} must also be defined.
:::
:::::
:::::::::::

::: ResourceLoader
*Superseded by TraversableResources*

> An abstract base class for a `loader`{.interpreted-text role="term"} which implements the optional `302`{.interpreted-text role="pep"} protocol for loading arbitrary resources from the storage back-end.
>
> ::: deprecated
> 3.7 This ABC is deprecated in favour of supporting resource loading through `importlib.resources.abc.TraversableResources`{.interpreted-text role="class"}. This class exists for backwards compatibility only with other ABCs in this module.
> :::
>
> :::: {.method abstractmethod=""}
> get_data(path)
>
> An abstract method to return the bytes for the data located at *path*. Loaders that have a file-like storage back-end that allows storing arbitrary data can implement this abstract method to give direct access to the data stored. `OSError`{.interpreted-text role="exc"} is to be raised if the *path* cannot be found. The *path* is expected to be constructed using a module\'s `~module.__file__`{.interpreted-text role="attr"} attribute or an item from a package\'s `~module.__path__`{.interpreted-text role="attr"}.
>
> ::: versionchanged
> 3.4 Raises `OSError`{.interpreted-text role="exc"} instead of `NotImplementedError`{.interpreted-text role="exc"}.
> :::
> ::::
:::

:::::::::::::::::: InspectLoader
An abstract base class for a `loader`{.interpreted-text role="term"} which implements the optional `302`{.interpreted-text role="pep"} protocol for loaders that inspect modules.

::::::: method
get_code(fullname)

Return the code object for a module, or `None` if the module does not have a code object (as would be the case, for example, for a built-in module). Raise an `ImportError`{.interpreted-text role="exc"} if loader cannot find the requested module.

:::: note
::: title
Note
:::

While the method has a default implementation, it is suggested that it be overridden if possible for performance.
::::

::: index
single: universal newlines; importlib.abc.InspectLoader.get_source method
:::

::: versionchanged
3.4 No longer abstract and a concrete implementation is provided.
:::
:::::::

:::: {.method abstractmethod=""}
get_source(fullname)

An abstract method to return the source of a module. It is returned as a text string using `universal newlines`{.interpreted-text role="term"}, translating all recognized line separators into `'\n'` characters. Returns `None` if no source is available (e.g. a built-in module). Raises `ImportError`{.interpreted-text role="exc"} if the loader cannot find the module specified.

::: versionchanged
3.4 Raises `ImportError`{.interpreted-text role="exc"} instead of `NotImplementedError`{.interpreted-text role="exc"}.
:::
::::

:::: method
is_package(fullname)

An optional method to return a true value if the module is a package, a false value otherwise. `ImportError`{.interpreted-text role="exc"} is raised if the `loader`{.interpreted-text role="term"} cannot find the module.

::: versionchanged
3.4 Raises `ImportError`{.interpreted-text role="exc"} instead of `NotImplementedError`{.interpreted-text role="exc"}.
:::
::::

:::::: staticmethod
source_to_code(data, path=\'\<string\>\', fullname=None)

Create a code object from Python source.

The *data* argument can be whatever the `compile`{.interpreted-text role="func"} function supports (i.e. string or bytes). The *path* argument should be the \"path\" to where the source code originated from, which can be an abstract concept (e.g. location in a zip file).

With the subsequent code object one can execute it in a module by running `exec(code, module.__dict__)`.

The optional argument *fullname* specifies the module name. It is needed to unambiguous `filter <warning-filter>`{.interpreted-text role="ref"} syntax warnings by module name.

::: versionadded
3.4
:::

::: versionchanged
3.5 Made the method static.
:::

::: versionadded
3.15 Added the *fullname* parameter.
:::
::::::

:::: method
exec_module(module)

Implementation of `Loader.exec_module`{.interpreted-text role="meth"}.

::: versionadded
3.4
:::
::::
::::::::::::::::::

::::: ExecutionLoader
An abstract base class which inherits from `InspectLoader`{.interpreted-text role="class"} that, when implemented, helps a module to be executed as a script. The ABC represents an optional `302`{.interpreted-text role="pep"} protocol.

:::: {.method abstractmethod=""}
get_filename(fullname)

An abstract method that is to return the value of `~module.__file__`{.interpreted-text role="attr"} for the specified module. If no path is available, `ImportError`{.interpreted-text role="exc"} is raised.

If source code is available, then the method should return the path to the source file, regardless of whether a bytecode was used to load the module.

::: versionchanged
3.4 Raises `ImportError`{.interpreted-text role="exc"} instead of `NotImplementedError`{.interpreted-text role="exc"}.
:::
::::
:::::

::::::::: {.FileLoader(fullname, .path)}
An abstract base class which inherits from `ResourceLoader`{.interpreted-text role="class"} and `ExecutionLoader`{.interpreted-text role="class"}, providing concrete implementations of `ResourceLoader.get_data`{.interpreted-text role="meth"} and `ExecutionLoader.get_filename`{.interpreted-text role="meth"}.

The *fullname* argument is a fully resolved name of the module the loader is to handle. The *path* argument is the path to the file for the module.

::: versionadded
3.3
:::

::: versionchanged
3.15 Removed the `load_module()` method.
:::

::: attribute
name

The name of the module the loader can handle.
:::

::: attribute
path

Path to the file of the module.
:::

::: {.method abstractmethod=""}
get_filename(fullname)

Returns `path`{.interpreted-text role="attr"}.
:::

::: {.method abstractmethod=""}
get_data(path)

Reads *path* as a binary file and returns the bytes from it.
:::
:::::::::

::::::::::::::::: SourceLoader
An abstract base class for implementing source (and optionally bytecode) file loading. The class inherits from both `ResourceLoader`{.interpreted-text role="class"} and `ExecutionLoader`{.interpreted-text role="class"}, requiring the implementation of:

- `ResourceLoader.get_data`{.interpreted-text role="meth"}

- 

  `ExecutionLoader.get_filename`{.interpreted-text role="meth"}

  :   Should only return the path to the source file; sourceless loading is not supported.

The abstract methods defined by this class are to add optional bytecode file support. Not implementing these optional methods (or causing them to raise `NotImplementedError`{.interpreted-text role="exc"}) causes the loader to only work with source code. Implementing the methods allows the loader to work with source *and* bytecode files; it does not allow for *sourceless* loading where only bytecode is provided. Bytecode files are an optimization to speed up loading by removing the parsing step of Python\'s compiler, and so no bytecode-specific API is exposed.

::: versionchanged
3.15 Removed the `load_module()` method.
:::

::::: method
path_stats(path)

Optional abstract method which returns a `dict`{.interpreted-text role="class"} containing metadata about the specified path. Supported dictionary keys are:

- `'mtime'` (mandatory): an integer or floating-point number representing the modification time of the source code;
- `'size'` (optional): the size in bytes of the source code.

Any other keys in the dictionary are ignored, to allow for future extensions. If the path cannot be handled, `OSError`{.interpreted-text role="exc"} is raised.

::: versionadded
3.3
:::

::: versionchanged
3.4 Raise `OSError`{.interpreted-text role="exc"} instead of `NotImplementedError`{.interpreted-text role="exc"}.
:::
:::::

::::: method
path_mtime(path)

Optional abstract method which returns the modification time for the specified path.

::: deprecated
3.3 This method is deprecated in favour of `path_stats`{.interpreted-text role="meth"}. You don\'t have to implement it, but it is still available for compatibility purposes. Raise `OSError`{.interpreted-text role="exc"} if the path cannot be handled.
:::

::: versionchanged
3.4 Raise `OSError`{.interpreted-text role="exc"} instead of `NotImplementedError`{.interpreted-text role="exc"}.
:::
:::::

:::: method
set_data(path, data)

Optional abstract method which writes the specified bytes to a file path. Any intermediate directories which do not exist are to be created automatically.

When writing to the path fails because the path is read-only (`errno.EACCES`{.interpreted-text role="const"}/`PermissionError`{.interpreted-text role="exc"}), do not propagate the exception.

::: versionchanged
3.4 No longer raises `NotImplementedError`{.interpreted-text role="exc"} when called.
:::
::::

::: method
get_code(fullname)

Concrete implementation of `InspectLoader.get_code`{.interpreted-text role="meth"}.
:::

:::: method
exec_module(module)

Concrete implementation of `Loader.exec_module`{.interpreted-text role="meth"}.

::: versionadded
3.4
:::
::::

::: method
get_source(fullname)

Concrete implementation of `InspectLoader.get_source`{.interpreted-text role="meth"}.
:::

::: method
is_package(fullname)

Concrete implementation of `InspectLoader.is_package`{.interpreted-text role="meth"}. A module is determined to be a package if its file path (as provided by `ExecutionLoader.get_filename`{.interpreted-text role="meth"}) is a file named `__init__` when the file extension is removed **and** the module name itself does not end in `__init__`.
:::
:::::::::::::::::

## `!importlib.machinery`{.interpreted-text role="mod"} \-- Importers and path hooks

::: {.module synopsis="Importers and path hooks"}
importlib.machinery
:::

**Source code:** `Lib/importlib/machinery.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module contains the various objects that help `import`{.interpreted-text role="keyword"} find and load modules.

:::: data
SOURCE_SUFFIXES

A list of strings representing the recognized file suffixes for source modules.

::: versionadded
3.3
:::
::::

::::: data
DEBUG_BYTECODE_SUFFIXES

A list of strings representing the file suffixes for non-optimized bytecode modules.

::: versionadded
3.3
:::

::: deprecated
3.5 Use `BYTECODE_SUFFIXES`{.interpreted-text role="const"} instead.
:::
:::::

::::: data
OPTIMIZED_BYTECODE_SUFFIXES

A list of strings representing the file suffixes for optimized bytecode modules.

::: versionadded
3.3
:::

::: deprecated
3.5 Use `BYTECODE_SUFFIXES`{.interpreted-text role="const"} instead.
:::
:::::

::::: data
BYTECODE_SUFFIXES

A list of strings representing the recognized file suffixes for bytecode modules (including the leading dot).

::: versionadded
3.3
:::

::: versionchanged
3.5 The value is no longer dependent on `__debug__`.
:::
:::::

:::: data
EXTENSION_SUFFIXES

A list of strings representing the recognized file suffixes for extension modules.

::: versionadded
3.3
:::
::::

:::: function
all_suffixes()

Returns a combined list of strings representing all file suffixes for modules recognized by the standard import machinery. This is a helper for code which simply needs to know if a filesystem path potentially refers to a module without needing any details on the kind of module (for example, `inspect.getmodulename`{.interpreted-text role="func"}).

::: versionadded
3.3
:::
::::

:::: BuiltinImporter
An `importer`{.interpreted-text role="term"} for built-in modules. All known built-in modules are listed in `sys.builtin_module_names`{.interpreted-text role="data"}. This class implements the `importlib.abc.MetaPathFinder`{.interpreted-text role="class"} and `importlib.abc.InspectLoader`{.interpreted-text role="class"} ABCs.

Only class methods are defined by this class to alleviate the need for instantiation.

::: versionchanged
3.5 As part of `489`{.interpreted-text role="pep"}, the builtin importer now implements `Loader.create_module`{.interpreted-text role="meth"} and `Loader.exec_module`{.interpreted-text role="meth"}
:::
::::

:::: FrozenImporter
An `importer`{.interpreted-text role="term"} for frozen modules. This class implements the `importlib.abc.MetaPathFinder`{.interpreted-text role="class"} and `importlib.abc.InspectLoader`{.interpreted-text role="class"} ABCs.

Only class methods are defined by this class to alleviate the need for instantiation.

::: versionchanged
3.4 Gained `~Loader.create_module`{.interpreted-text role="meth"} and `~Loader.exec_module`{.interpreted-text role="meth"} methods.
:::
::::

::::: WindowsRegistryFinder
`Finder <finder>`{.interpreted-text role="term"} for modules declared in the Windows registry. This class implements the `importlib.abc.MetaPathFinder`{.interpreted-text role="class"} ABC.

Only class methods are defined by this class to alleviate the need for instantiation.

::: versionadded
3.3
:::

::: deprecated
3.6 Use `site`{.interpreted-text role="mod"} configuration instead. Future versions of Python may not enable this finder by default.
:::
:::::

::::::::: PathFinder
A `Finder <finder>`{.interpreted-text role="term"} for `sys.path`{.interpreted-text role="data"} and package `__path__` attributes. This class implements the `importlib.abc.MetaPathFinder`{.interpreted-text role="class"} ABC.

Only class methods are defined by this class to alleviate the need for instantiation.

::::: classmethod
find_spec(fullname, path=None, target=None)

Class method that attempts to find a `spec <module spec>`{.interpreted-text role="term"} for the module specified by *fullname* on `sys.path`{.interpreted-text role="data"} or, if defined, on *path*. For each path entry that is searched, `sys.path_importer_cache`{.interpreted-text role="data"} is checked. If a non-false object is found then it is used as the `path entry finder`{.interpreted-text role="term"} to look for the module being searched for. If no entry is found in `sys.path_importer_cache`{.interpreted-text role="data"}, then `sys.path_hooks`{.interpreted-text role="data"} is searched for a finder for the path entry and, if found, is stored in `sys.path_importer_cache`{.interpreted-text role="data"} along with being queried about the module. If no finder is ever found then `None` is both stored in the cache and returned.

::: versionadded
3.4
:::

::: versionchanged
3.5 If the current working directory \-- represented by an empty string \-- is no longer valid then `None` is returned but no value is cached in `sys.path_importer_cache`{.interpreted-text role="data"}.
:::
:::::

:::: classmethod
invalidate_caches()

Calls `importlib.abc.PathEntryFinder.invalidate_caches`{.interpreted-text role="meth"} on all finders stored in `sys.path_importer_cache`{.interpreted-text role="data"} that define the method. Otherwise entries in `sys.path_importer_cache`{.interpreted-text role="data"} set to `None` are deleted.

::: versionchanged
3.7 Entries of `None` in `sys.path_importer_cache`{.interpreted-text role="data"} are deleted.
:::
::::

::: versionchanged
3.4 Calls objects in `sys.path_hooks`{.interpreted-text role="data"} with the current working directory for `''` (i.e. the empty string).
:::
:::::::::

::::::::: {.FileFinder(path, .*loader_details)}
A concrete implementation of `importlib.abc.PathEntryFinder`{.interpreted-text role="class"} which caches results from the file system.

The *path* argument is the directory for which the finder is in charge of searching.

The *loader_details* argument is a variable number of 2-item tuples each containing a loader and a sequence of file suffixes the loader recognizes. The loaders are expected to be callables which accept two arguments of the module\'s name and the path to the file found.

The finder will cache the directory contents as necessary, making stat calls for each module search to verify the cache is not outdated. Because cache staleness relies upon the granularity of the operating system\'s state information of the file system, there is a potential race condition of searching for a module, creating a new file, and then searching for the module the new file represents. If the operations happen fast enough to fit within the granularity of stat calls, then the module search will fail. To prevent this from happening, when you create a module dynamically, make sure to call `importlib.invalidate_caches`{.interpreted-text role="func"}.

::: versionadded
3.3
:::

::: attribute
path

The path the finder will search in.
:::

:::: method
find_spec(fullname, target=None)

Attempt to find the spec to handle *fullname* within `path`{.interpreted-text role="attr"}.

::: versionadded
3.4
:::
::::

::: method
invalidate_caches()

Clear out the internal cache.
:::

::: classmethod
path_hook(\*loader_details)

A class method which returns a closure for use on `sys.path_hooks`{.interpreted-text role="data"}. An instance of `FileFinder`{.interpreted-text role="class"} is returned by the closure using the path argument given to the closure directly and *loader_details* indirectly.

If the argument to the closure is not an existing directory, `ImportError`{.interpreted-text role="exc"} is raised.
:::
:::::::::

:::::: {.NamespacePath(name, .path, .path_finder)}
Represents a `namespace package`{.interpreted-text role="term"}\'s path (`module.__path__`{.interpreted-text role="attr"}).

When its `__path__` value is accessed it will be recomputed if necessary. This keeps it in-sync with the global state (`sys.modules`{.interpreted-text role="attr"}).

The *name* argument is the name of the namespace module.

The *path* argument is the initial path value.

The *path_finder* argument is the callable used to recompute the path value. The callable has the same signature as `importlib.abc.MetaPathFinder.find_spec`{.interpreted-text role="meth"}.

When the parent\'s `module.__path__`{.interpreted-text role="attr"} attribute is updated, the path value is recomputed.

If the parent module is missing from `sys.modules`{.interpreted-text role="data"}, then `ModuleNotFoundError`{.interpreted-text role="exc"} will be raised.

For top-level modules, the parent module\'s path is `sys.path`{.interpreted-text role="data"}.

:::: note
::: title
Note
:::

`PathFinder.invalidate_caches`{.interpreted-text role="meth"} invalidates `NamespacePath`{.interpreted-text role="class"}, forcing the path value to be recomputed next time it is accessed.
::::

::: versionadded
3.15
:::
::::::

:::::::::: {.SourceFileLoader(fullname, .path)}
A concrete implementation of `importlib.abc.SourceLoader`{.interpreted-text role="class"} by subclassing `importlib.abc.FileLoader`{.interpreted-text role="class"} and providing some concrete implementations of other methods.

::: versionadded
3.3
:::

::: versionchanged
3.15 Removed the `load_module()` method.
:::

::: attribute
name

The name of the module that this loader will handle.
:::

::: attribute
path

The path to the source file.
:::

::: method
is_package(fullname)

Return `True` if `path`{.interpreted-text role="attr"} appears to be for a package.
:::

::: method
path_stats(path)

Concrete implementation of `importlib.abc.SourceLoader.path_stats`{.interpreted-text role="meth"}.
:::

::: method
set_data(path, data)

Concrete implementation of `importlib.abc.SourceLoader.set_data`{.interpreted-text role="meth"}.
:::
::::::::::

:::::::::: {.SourcelessFileLoader(fullname, .path)}
A concrete implementation of `importlib.abc.FileLoader`{.interpreted-text role="class"} which can import bytecode files (i.e. no source code files exist).

Please note that direct use of bytecode files (and thus not source code files) inhibits your modules from being usable by all Python implementations or new versions of Python which change the bytecode format.

::: versionadded
3.3
:::

::: versionchanged
3.15 Removed the `load_module()` method.
:::

::: attribute
name

The name of the module the loader will handle.
:::

::: attribute
path

The path to the bytecode file.
:::

::: method
is_package(fullname)

Determines if the module is a package based on `path`{.interpreted-text role="attr"}.
:::

::: method
get_code(fullname)

Returns the code object for `name`{.interpreted-text role="attr"} created from `path`{.interpreted-text role="attr"}.
:::

::: method
get_source(fullname)

Returns `None` as bytecode files have no source when this loader is used.
:::
::::::::::

:::::::::::::::: {.ExtensionFileLoader(fullname, .path)}
A concrete implementation of `importlib.abc.ExecutionLoader`{.interpreted-text role="class"} for extension modules.

The *fullname* argument specifies the name of the module the loader is to support. The *path* argument is the path to the extension module\'s file.

Note that, by default, importing an extension module will fail in subinterpreters if it doesn\'t implement multi-phase init (see `489`{.interpreted-text role="pep"}), even if it would otherwise import successfully.

::: versionadded
3.3
:::

::: versionchanged
3.12 Multi-phase init is now required for use in subinterpreters.
:::

::: attribute
name

Name of the module the loader supports.
:::

::: attribute
path

Path to the extension module.
:::

:::: method
create_module(spec)

Creates the module object from the given specification in accordance with `489`{.interpreted-text role="pep"}.

::: versionadded
3.5
:::
::::

:::: method
exec_module(module)

Initializes the given module object in accordance with `489`{.interpreted-text role="pep"}.

::: versionadded
3.5
:::
::::

::: method
is_package(fullname)

Returns `True` if the file path points to a package\'s `__init__` module based on `EXTENSION_SUFFIXES`{.interpreted-text role="const"}.
:::

::: method
get_code(fullname)

Returns `None` as extension modules lack a code object.
:::

::: method
get_source(fullname)

Returns `None` as extension modules do not have source code.
:::

:::: method
get_filename(fullname)

Returns `path`{.interpreted-text role="attr"}.

::: versionadded
3.4
:::
::::
::::::::::::::::

:::: {.NamespaceLoader(name, .path, .path_finder)}
A concrete implementation of `importlib.abc.InspectLoader`{.interpreted-text role="class"} for namespace packages. This is an alias for a private class and is only made public for introspecting the `__loader__` attribute on namespace packages:

    >>> from importlib.machinery import NamespaceLoader
    >>> import my_namespace
    >>> isinstance(my_namespace.__loader__, NamespaceLoader)
    True
    >>> import importlib.abc
    >>> isinstance(my_namespace.__loader__, importlib.abc.Loader)
    True

::: versionadded
3.11
:::
::::

:::::::::::: {.ModuleSpec(name, .loader, .*, .origin=None, .loader_state=None, .is_package=None)}
A specification for a module\'s import-system-related state. This is typically exposed as the module\'s `~module.__spec__`{.interpreted-text role="attr"} attribute. Many of these attributes are also available directly on a module: for example, `module.__spec__.origin == module.__file__`. Note, however, that while the *values* are usually equivalent, they can differ since there is no synchronization between the two objects. For example, it is possible to update the module\'s `~module.__file__`{.interpreted-text role="attr"} at runtime and this will not be automatically reflected in the module\'s `__spec__.origin <ModuleSpec.origin>`{.interpreted-text role="attr"}, and vice versa.

::: versionadded
3.4
:::

::: attribute
name

The module\'s fully qualified name (see `module.__name__`{.interpreted-text role="attr"}). The `finder`{.interpreted-text role="term"} should always set this attribute to a non-empty string.
:::

::: attribute
loader

The `loader`{.interpreted-text role="term"} used to load the module (see `module.__loader__`{.interpreted-text role="attr"}). The `finder`{.interpreted-text role="term"} should always set this attribute.
:::

::: attribute
origin

The location the `loader`{.interpreted-text role="term"} should use to load the module (see `module.__file__`{.interpreted-text role="attr"}). For example, for modules loaded from a `.py` file this is the filename. The `finder`{.interpreted-text role="term"} should always set this attribute to a meaningful value for the `loader`{.interpreted-text role="term"} to use. In the uncommon case that there is not one (like for namespace packages), it should be set to `None`.
:::

::: attribute
submodule_search_locations

A (possibly empty) `sequence`{.interpreted-text role="term"} of strings enumerating the locations in which a package\'s submodules will be found (see `module.__path__`{.interpreted-text role="attr"}). Most of the time there will only be a single directory in this list.

The `finder`{.interpreted-text role="term"} should set this attribute to a sequence, even an empty one, to indicate to the import system that the module is a package. It should be set to `None` for non-package modules. It is set automatically later to a special object for namespace packages.
:::

::: attribute
loader_state

The `finder`{.interpreted-text role="term"} may set this attribute to an object containing additional, module-specific data to use when loading the module. Otherwise it should be set to `None`.
:::

::: attribute
cached

The filename of a compiled version of the module\'s code. The `finder`{.interpreted-text role="term"} should always set this attribute but it may be `None` for modules that do not need compiled code stored.
:::

::: attribute
parent

(Read-only) The fully qualified name of the package the module is in (or the empty string for a top-level module). See `module.__package__`{.interpreted-text role="attr"}. If the module is a package then this is the same as `name`{.interpreted-text role="attr"}.
:::

::: attribute
has_location

`True` if the spec\'s `origin`{.interpreted-text role="attr"} refers to a loadable location, `False` otherwise. This value impacts how `!origin`{.interpreted-text role="attr"} is interpreted and how the module\'s `~module.__file__`{.interpreted-text role="attr"} is populated.
:::
::::::::::::

::::::: {.AppleFrameworkLoader(name, .path)}
A specialization of `importlib.machinery.ExtensionFileLoader`{.interpreted-text role="class"} that is able to load extension modules in Framework format.

For compatibility with the iOS App Store, *all* binary modules in an iOS app must be dynamic libraries, contained in a framework with appropriate metadata, stored in the `Frameworks` folder of the packaged app. There can be only a single binary per framework, and there can be no executable binary material outside the Frameworks folder.

To accommodate this requirement, when running on iOS, extension module binaries are *not* packaged as `.so` files on `sys.path`, but as individual standalone frameworks. To discover those frameworks, this loader is registered against the `.fwork` file extension, with a `.fwork` file acting as a placeholder in the original location of the binary on `sys.path`. The `.fwork` file contains the path of the actual binary in the `Frameworks` folder, relative to the app bundle. To allow for resolving a framework-packaged binary back to the original location, the framework is expected to contain a `.origin` file that contains the location of the `.fwork` file, relative to the app bundle.

For example, consider the case of an import `from foo.bar import _whiz`, where `_whiz` is implemented with the binary module `sources/foo/bar/_whiz.abi3.so`, with `sources` being the location registered on `sys.path`, relative to the application bundle. This module *must* be distributed as `Frameworks/foo.bar._whiz.framework/foo.bar._whiz` (creating the framework name from the full import path of the module), with an `Info.plist` file in the `.framework` directory identifying the binary as a framework. The `foo.bar._whiz` module would be represented in the original location with a `sources/foo/bar/_whiz.abi3.fwork` marker file, containing the path `Frameworks/foo.bar._whiz/foo.bar._whiz`. The framework would also contain `Frameworks/foo.bar._whiz.framework/foo.bar._whiz.origin`, containing the path to the `.fwork` file.

When a module is loaded with this loader, the `__file__` for the module will report as the location of the `.fwork` file. This allows code to use the `__file__` of a module as an anchor for file system traversal. However, the spec origin will reference the location of the *actual* binary in the `.framework` folder.

The Xcode project building the app is responsible for converting any `.so` files from wherever they exist in the `PYTHONPATH` into frameworks in the `Frameworks` folder (including stripping extensions from the module file, the addition of framework metadata, and signing the resulting framework), and creating the `.fwork` and `.origin` files. This will usually be done with a build step in the Xcode project; see the iOS documentation for details on how to construct this build step.

::: versionadded
3.13
:::

::: availability
iOS.
:::

::: attribute
name

Name of the module the loader supports.
:::

::: attribute
path

Path to the `.fwork` file for the extension module.
:::
:::::::

## `!importlib.util`{.interpreted-text role="mod"} \-- Utility code for importers

::: {.module synopsis="Utility code for importers"}
importlib.util
:::

**Source code:** `Lib/importlib/util.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module contains the various objects that help in the construction of an `importer`{.interpreted-text role="term"}.

:::: data
MAGIC_NUMBER

The bytes which represent the bytecode version number. If you need help with loading/writing bytecode then consider `importlib.abc.SourceLoader`{.interpreted-text role="class"}.

::: versionadded
3.4
:::
::::

::::::: function
cache_from_source(path, \*, optimization=None)

Return the `3147`{.interpreted-text role="pep"}/`488`{.interpreted-text role="pep"} path to the byte-compiled file associated with the source *path*. For example, if *path* is `/foo/bar/baz.py` the return value would be `/foo/bar/__pycache__/baz.cpython-32.pyc` for Python 3.2. The `cpython-32` string comes from the current magic tag (see `get_tag`{.interpreted-text role="func"}; if `sys.implementation.cache_tag`{.interpreted-text role="attr"} is not defined then `NotImplementedError`{.interpreted-text role="exc"} will be raised).

The *optimization* parameter is used to specify the optimization level of the bytecode file. An empty string represents no optimization, so `/foo/bar/baz.py` with an *optimization* of `''` will result in a bytecode path of `/foo/bar/__pycache__/baz.cpython-32.pyc`. `None` causes the interpreter\'s optimization level to be used. Any other value\'s string representation is used, so `/foo/bar/baz.py` with an *optimization* of `2` will lead to the bytecode path of `/foo/bar/__pycache__/baz.cpython-32.opt-2.pyc`. The string representation of *optimization* can only be alphanumeric, else `ValueError`{.interpreted-text role="exc"} is raised.

::: versionadded
3.4
:::

::: versionchanged
3.5 The *optimization* parameter was added and the *debug_override* parameter was deprecated.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.15 The *debug_override* parameter was removed.
:::
:::::::

::::: function
source_from_cache(path)

Given the *path* to a `3147`{.interpreted-text role="pep"} file name, return the associated source code file path. For example, if *path* is `/foo/bar/__pycache__/baz.cpython-32.pyc` the returned path would be `/foo/bar/baz.py`. *path* need not exist, however if it does not conform to `3147`{.interpreted-text role="pep"} or `488`{.interpreted-text role="pep"} format, a `ValueError`{.interpreted-text role="exc"} is raised. If `sys.implementation.cache_tag`{.interpreted-text role="attr"} is not defined, `NotImplementedError`{.interpreted-text role="exc"} is raised.

::: versionadded
3.4
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
:::::

:::: function
decode_source(source_bytes)

Decode the given bytes representing source code and return it as a string with universal newlines (as required by `importlib.abc.InspectLoader.get_source`{.interpreted-text role="meth"}).

::: versionadded
3.4
:::
::::

::::: function
resolve_name(name, package)

Resolve a relative module name to an absolute one.

If **name** has no leading dots, then **name** is simply returned. This allows for usage such as `importlib.util.resolve_name('sys', __spec__.parent)` without doing a check to see if the **package** argument is needed.

`ImportError`{.interpreted-text role="exc"} is raised if **name** is a relative module name but **package** is a false value (e.g. `None` or the empty string). `ImportError`{.interpreted-text role="exc"} is also raised if a relative name would escape its containing package (e.g. requesting `..bacon` from within the `spam` package).

::: versionadded
3.3
:::

::: versionchanged
3.9 To improve consistency with import statements, raise `ImportError`{.interpreted-text role="exc"} instead of `ValueError`{.interpreted-text role="exc"} for invalid relative import attempts.
:::
:::::

::::: function
find_spec(name, package=None)

Find the `spec <module spec>`{.interpreted-text role="term"} for a module, optionally relative to the specified **package** name. If the module is in `sys.modules`{.interpreted-text role="data"}, then `sys.modules[name].__spec__` is returned (unless the spec would be `None` or is not set, in which case `ValueError`{.interpreted-text role="exc"} is raised). Otherwise a search using `sys.meta_path`{.interpreted-text role="data"} is done. `None` is returned if no spec is found.

If **name** is for a submodule (contains a dot), the parent module is automatically imported.

**name** and **package** work the same as for `import_module`{.interpreted-text role="func"}.

::: versionadded
3.4
:::

::: versionchanged
3.7 Raises `ModuleNotFoundError`{.interpreted-text role="exc"} instead of `AttributeError`{.interpreted-text role="exc"} if **package** is in fact not a package (i.e. lacks a `~module.__path__`{.interpreted-text role="attr"} attribute).
:::
:::::

:::: function
module_from_spec(spec)

Create a new module based on **spec** and `spec.loader.create_module <importlib.abc.Loader.create_module>`{.interpreted-text role="meth"}.

If `spec.loader.create_module <importlib.abc.Loader.create_module>`{.interpreted-text role="meth"} does not return `None`, then any pre-existing attributes will not be reset. Also, no `AttributeError`{.interpreted-text role="exc"} will be raised if triggered while accessing **spec** or setting an attribute on the module.

This function is preferred over using `types.ModuleType`{.interpreted-text role="class"} to create a new module as **spec** is used to set as many import-controlled attributes on the module as possible.

::: versionadded
3.5
:::
::::

:::: function
spec_from_loader(name, loader, \*, origin=None, is_package=None)

A factory function for creating a `~importlib.machinery.ModuleSpec`{.interpreted-text role="class"} instance based on a loader. The parameters have the same meaning as they do for ModuleSpec. The function uses available `loader`{.interpreted-text role="term"} APIs, such as `InspectLoader.is_package`{.interpreted-text role="meth"}, to fill in any missing information on the spec.

::: versionadded
3.4
:::
::::

::::: function
spec_from_file_location(name, location, \*, loader=None, submodule_search_locations=None)

A factory function for creating a `~importlib.machinery.ModuleSpec`{.interpreted-text role="class"} instance based on the path to a file. Missing information will be filled in on the spec by making use of loader APIs and by the implication that the module will be file-based.

::: versionadded
3.4
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
:::::

:::: function
source_hash(source_bytes)

Return the hash of *source_bytes* as bytes. A hash-based `.pyc` file embeds the `source_hash`{.interpreted-text role="func"} of the corresponding source file\'s contents in its header.

::: versionadded
3.7
:::
::::

:::::: function
[incompatible_extension_module_restrictions]{#incompatible_extension_module_restrictions}(\*, disable_check)

A context manager that can temporarily skip the compatibility check for extension modules. By default the check is enabled and will fail when a single-phase init module is imported in a subinterpreter. It will also fail for a multi-phase init module that doesn\'t explicitly support a per-interpreter GIL, when imported in an interpreter with its own GIL.

Note that this function is meant to accommodate an unusual case; one which is likely to eventually go away. There\'s is a pretty good chance this is not what you were looking for.

You can get the same effect as this function by implementing the basic interface of multi-phase init (`489`{.interpreted-text role="pep"}) and lying about support for multiple interpreters (or per-interpreter GIL).

:::: warning
::: title
Warning
:::

Using this function to disable the check can lead to unexpected behavior and even crashes. It should only be used during extension module development.
::::

::: versionadded
3.12
:::
::::::

:::::::: LazyLoader(loader)
A class which postpones the execution of the loader of a module until the module has an attribute accessed.

This class **only** works with loaders that define `~importlib.abc.Loader.exec_module`{.interpreted-text role="meth"} as control over what module type is used for the module is required. For those same reasons, the loader\'s `~importlib.abc.Loader.create_module`{.interpreted-text role="meth"} method must return `None` or a type for which its `__class__` attribute can be mutated along with not using `slots <__slots__>`{.interpreted-text role="term"}. Finally, modules which substitute the object placed into `sys.modules`{.interpreted-text role="data"} will not work as there is no way to properly replace the module references throughout the interpreter safely; `ValueError`{.interpreted-text role="exc"} is raised if such a substitution is detected.

:::: note
::: title
Note
:::

For projects where startup time is critical, this class allows for potentially minimizing the cost of loading a module if it is never used. For projects where startup time is not essential then use of this class is **heavily** discouraged due to error messages created during loading being postponed and thus occurring out of context.
::::

::: versionadded
3.5
:::

::: versionchanged
3.6 Began calling `~importlib.abc.Loader.create_module`{.interpreted-text role="meth"}, removing the compatibility warning for `importlib.machinery.BuiltinImporter`{.interpreted-text role="class"} and `importlib.machinery.ExtensionFileLoader`{.interpreted-text role="class"}.
:::

::: classmethod
factory(loader)

A class method which returns a callable that creates a lazy loader. This is meant to be used in situations where the loader is passed by class instead of by instance. :

    suffixes = importlib.machinery.SOURCE_SUFFIXES
    loader = importlib.machinery.SourceFileLoader
    lazy_loader = importlib.util.LazyLoader.factory(loader)
    finder = importlib.machinery.FileFinder(path, (lazy_loader, suffixes))
:::
::::::::

## Examples {#importlib-examples}

### Importing programmatically

To programmatically import a module, use `importlib.import_module`{.interpreted-text role="func"}. :

    import importlib

    itertools = importlib.import_module('itertools')

### Checking if a module can be imported

If you need to find out if a module can be imported without actually doing the import, then you should use `importlib.util.find_spec`{.interpreted-text role="func"}.

Note that if `name` is a submodule (contains a dot), `importlib.util.find_spec`{.interpreted-text role="func"} will import the parent module. :

    import importlib.util
    import sys

    # For illustrative purposes.
    name = 'itertools'

    if name in sys.modules:
        print(f"{name!r} already in sys.modules")
    elif (spec := importlib.util.find_spec(name)) is not None:
        # If you chose to perform the actual import ...
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        print(f"{name!r} has been imported")
    else:
        print(f"can't find the {name!r} module")

### Importing a source file directly

This recipe should be used with caution: it is an approximation of an import statement where the file path is specified directly, rather than `sys.path`{.interpreted-text role="data"} being searched. Alternatives should first be considered first, such as modifying `sys.path`{.interpreted-text role="data"} when a proper module is required, or using `runpy.run_path`{.interpreted-text role="func"} when the global namespace resulting from running a Python file is appropriate.

To import a Python source file directly from a path, use the following recipe:

    import importlib.util
    import sys


    def import_from_path(module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module


    # For illustrative purposes only (use of `json` is arbitrary).
    import json
    file_path = json.__file__
    module_name = json.__name__

    # Similar outcome as `import json`.
    json = import_from_path(module_name, file_path)

### Implementing lazy imports

The example below shows how to implement lazy imports:

    >>> import importlib.util
    >>> import sys
    >>> def lazy_import(name):
    ...     spec = importlib.util.find_spec(name)
    ...     loader = importlib.util.LazyLoader(spec.loader)
    ...     spec.loader = loader
    ...     module = importlib.util.module_from_spec(spec)
    ...     sys.modules[name] = module
    ...     loader.exec_module(module)
    ...     return module
    ...
    >>> lazy_typing = lazy_import("typing")
    >>> #lazy_typing is a real module object,
    >>> #but it is not loaded in memory yet.
    >>> lazy_typing.TYPE_CHECKING
    False

### Setting up an importer

For deep customizations of import, you typically want to implement an `importer`{.interpreted-text role="term"}. This means managing both the `finder`{.interpreted-text role="term"} and `loader`{.interpreted-text role="term"} side of things. For finders there are two flavours to choose from depending on your needs: a `meta path finder`{.interpreted-text role="term"} or a `path entry finder`{.interpreted-text role="term"}. The former is what you would put on `sys.meta_path`{.interpreted-text role="data"} while the latter is what you create using a `path entry hook`{.interpreted-text role="term"} on `sys.path_hooks`{.interpreted-text role="data"} which works with `sys.path`{.interpreted-text role="data"} entries to potentially create a finder. This example will show you how to register your own importers so that import will use them (for creating an importer for yourself, read the documentation for the appropriate classes defined within this package):

    import importlib.machinery
    import sys

    # For illustrative purposes only.
    SpamMetaPathFinder = importlib.machinery.PathFinder
    SpamPathEntryFinder = importlib.machinery.FileFinder
    loader_details = (importlib.machinery.SourceFileLoader,
                      importlib.machinery.SOURCE_SUFFIXES)

    # Setting up a meta path finder.
    # Make sure to put the finder in the proper location in the list in terms of
    # priority.
    sys.meta_path.append(SpamMetaPathFinder)

    # Setting up a path entry finder.
    # Make sure to put the path hook in the proper location in the list in terms
    # of priority.
    sys.path_hooks.append(SpamPathEntryFinder.path_hook(loader_details))

### Approximating `importlib.import_module`{.interpreted-text role="func"}

Import itself is implemented in Python code, making it possible to expose most of the import machinery through importlib. The following helps illustrate the various APIs that importlib exposes by providing an approximate implementation of `importlib.import_module`{.interpreted-text role="func"}:

    import importlib.util
    import sys

    def import_module(name, package=None):
        """An approximate implementation of import."""
        absolute_name = importlib.util.resolve_name(name, package)
        try:
            return sys.modules[absolute_name]
        except KeyError:
            pass

        path = None
        if '.' in absolute_name:
            parent_name, _, child_name = absolute_name.rpartition('.')
            parent_module = import_module(parent_name)
            path = parent_module.__spec__.submodule_search_locations
        for finder in sys.meta_path:
            spec = finder.find_spec(absolute_name, path)
            if spec is not None:
                break
        else:
            msg = f'No module named {absolute_name!r}'
            raise ModuleNotFoundError(msg, name=absolute_name)
        module = importlib.util.module_from_spec(spec)
        sys.modules[absolute_name] = module
        spec.loader.exec_module(module)
        if path is not None:
            setattr(parent_module, child_name, module)
        return module
