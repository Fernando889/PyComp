# The import system {#importsystem}

::: index
single: import machinery
:::

Python code in one `module`{.interpreted-text role="term"} gains access to the code in another module by the process of `importing`{.interpreted-text role="term"} it. The `import`{.interpreted-text role="keyword"} statement is the most common way of invoking the import machinery, but it is not the only way. Functions such as `importlib.import_module`{.interpreted-text role="func"} and built-in `__import__`{.interpreted-text role="func"} can also be used to invoke the import machinery.

The `import`{.interpreted-text role="keyword"} statement combines two operations; it searches for the named module, then it binds the results of that search to a name in the local scope. The search operation of the `!import`{.interpreted-text role="keyword"} statement is defined as a call to the `__import__`{.interpreted-text role="func"} function, with the appropriate arguments. The return value of `__import__`{.interpreted-text role="func"} is used to perform the name binding operation of the `!import`{.interpreted-text role="keyword"} statement. See the `!import`{.interpreted-text role="keyword"} statement for the exact details of that name binding operation.

A direct call to `__import__`{.interpreted-text role="func"} performs only the module search and, if found, the module creation operation. While certain side-effects may occur, such as the importing of parent packages, and the updating of various caches (including `sys.modules`{.interpreted-text role="data"}), only the `import`{.interpreted-text role="keyword"} statement performs a name binding operation.

When an `import`{.interpreted-text role="keyword"} statement is executed, the standard builtin `__import__`{.interpreted-text role="func"} function is called. Other mechanisms for invoking the import system (such as `importlib.import_module`{.interpreted-text role="func"}) may choose to bypass `__import__`{.interpreted-text role="func"} and use their own solutions to implement import semantics.

When a module is first imported, Python searches for the module and if found, it creates a module object[^1], initializing it. If the named module cannot be found, a `ModuleNotFoundError`{.interpreted-text role="exc"} is raised. Python implements various strategies to search for the named module when the import machinery is invoked. These strategies can be modified and extended by using various hooks described in the sections below.

::: versionchanged
3.3 The import system has been updated to fully implement the second phase of `302`{.interpreted-text role="pep"}. There is no longer any implicit import machinery - the full import system is exposed through `sys.meta_path`{.interpreted-text role="data"}. In addition, native namespace package support has been implemented (see `420`{.interpreted-text role="pep"}).
:::

## `importlib`{.interpreted-text role="mod"}

The `importlib`{.interpreted-text role="mod"} module provides a rich API for interacting with the import system. For example `importlib.import_module`{.interpreted-text role="func"} provides a recommended, simpler API than built-in `__import__`{.interpreted-text role="func"} for invoking the import machinery. Refer to the `importlib`{.interpreted-text role="mod"} library documentation for additional detail.

## Packages

::: index
single: package
:::

Python has only one type of module object, and all modules are of this type, regardless of whether the module is implemented in Python, C, or something else. To help organize modules and provide a naming hierarchy, Python has a concept of `packages <package>`{.interpreted-text role="term"}.

You can think of packages as the directories on a file system and modules as files within directories, but don\'t take this analogy too literally since packages and modules need not originate from the file system. For the purposes of this documentation, we\'ll use this convenient analogy of directories and files. Like file system directories, packages are organized hierarchically, and packages may themselves contain subpackages, as well as regular modules.

It\'s important to keep in mind that all packages are modules, but not all modules are packages. Or put another way, packages are just a special kind of module. Specifically, any module that contains a `__path__` attribute is considered a package.

All modules have a name. Subpackage names are separated from their parent package name by a dot, akin to Python\'s standard attribute access syntax. Thus you might have a package called `email`{.interpreted-text role="mod"}, which in turn has a subpackage called `email.mime`{.interpreted-text role="mod"} and a module within that subpackage called `email.mime.text`{.interpreted-text role="mod"}.

### Regular packages

::: index
pair: package; regular
:::

Python defines two types of packages, `regular packages <regular
package>`{.interpreted-text role="term"} and `namespace packages <namespace package>`{.interpreted-text role="term"}. Regular packages are traditional packages as they existed in Python 3.2 and earlier. A regular package is typically implemented as a directory containing an `__init__.py` file. When a regular package is imported, this `__init__.py` file is implicitly executed, and the objects it defines are bound to names in the package\'s namespace. The `__init__.py` file can contain the same Python code that any other module can contain, and Python will add some additional attributes to the module when it is imported.

For example, the following file system layout defines a top level `parent` package with three subpackages:

    parent/
        __init__.py
        one/
            __init__.py
        two/
            __init__.py
        three/
            __init__.py

Importing `parent.one` will implicitly execute `parent/__init__.py` and `parent/one/__init__.py`. Subsequent imports of `parent.two` or `parent.three` will execute `parent/two/__init__.py` and `parent/three/__init__.py` respectively.

### Namespace packages {#reference-namespace-package}

::: index
pair: package; namespace pair: package; portion
:::

A namespace package is a composite of various `portions <portion>`{.interpreted-text role="term"}, where each portion contributes a subpackage to the parent package. Portions may reside in different locations on the file system. Portions may also be found in zip files, on the network, or anywhere else that Python searches during import. Namespace packages may or may not correspond directly to objects on the file system; they may be virtual modules that have no concrete representation.

Namespace packages do not use an ordinary list for their `__path__` attribute. They instead use a custom iterable type which will automatically perform a new search for package portions on the next import attempt within that package if the path of their parent package (or `sys.path`{.interpreted-text role="data"} for a top level package) changes.

With namespace packages, there is no `parent/__init__.py` file. In fact, there may be multiple `parent` directories found during import search, where each one is provided by a different portion. Thus `parent/one` may not be physically located next to `parent/two`. In this case, Python will create a namespace package for the top-level `parent` package whenever it or one of its subpackages is imported.

See also `420`{.interpreted-text role="pep"} for the namespace package specification.

## Searching

To begin the search, Python needs the `fully qualified <qualified name>`{.interpreted-text role="term"} name of the module (or package, but for the purposes of this discussion, the difference is immaterial) being imported. This name may come from various arguments to the `import`{.interpreted-text role="keyword"} statement, or from the parameters to the `importlib.import_module`{.interpreted-text role="func"} or `__import__`{.interpreted-text role="func"} functions.

This name will be used in various phases of the import search, and it may be the dotted path to a submodule, e.g. `foo.bar.baz`. In this case, Python first tries to import `foo`, then `foo.bar`, and finally `foo.bar.baz`. If any of the intermediate imports fail, a `ModuleNotFoundError`{.interpreted-text role="exc"} is raised.

### The module cache

::: index
single: sys.modules
:::

The first place checked during import search is `sys.modules`{.interpreted-text role="data"}. This mapping serves as a cache of all modules that have been previously imported, including the intermediate paths. So if `foo.bar.baz` was previously imported, `sys.modules`{.interpreted-text role="data"} will contain entries for `foo`, `foo.bar`, and `foo.bar.baz`. Each key will have as its value the corresponding module object.

During import, the module name is looked up in `sys.modules`{.interpreted-text role="data"} and if present, the associated value is the module satisfying the import, and the process completes. However, if the value is `None`, then a `ModuleNotFoundError`{.interpreted-text role="exc"} is raised. If the module name is missing, Python will continue searching for the module.

`sys.modules`{.interpreted-text role="data"} is writable. Deleting a key may not destroy the associated module (as other modules may hold references to it), but it will invalidate the cache entry for the named module, causing Python to search anew for the named module upon its next import. The key can also be assigned to `None`, forcing the next import of the module to result in a `ModuleNotFoundError`{.interpreted-text role="exc"}.

Beware though, as if you keep a reference to the module object, invalidate its cache entry in `sys.modules`{.interpreted-text role="data"}, and then re-import the named module, the two module objects will *not* be the same. By contrast, `importlib.reload`{.interpreted-text role="func"} will reuse the *same* module object, and simply reinitialise the module contents by rerunning the module\'s code.

### Finders and loaders

::: index
single: finder single: loader single: module spec
:::

If the named module is not found in `sys.modules`{.interpreted-text role="data"}, then Python\'s import protocol is invoked to find and load the module. This protocol consists of two conceptual objects, `finders <finder>`{.interpreted-text role="term"} and `loaders <loader>`{.interpreted-text role="term"}. A finder\'s job is to determine whether it can find the named module using whatever strategy it knows about. Objects that implement both of these interfaces are referred to as `importers <importer>`{.interpreted-text role="term"} - they return themselves when they find that they can load the requested module.

Python includes a number of default finders and importers. The first one knows how to locate built-in modules, and the second knows how to locate frozen modules. A third default finder searches an `import path`{.interpreted-text role="term"} for modules. The `import path`{.interpreted-text role="term"} is a list of locations that may name file system paths or zip files. It can also be extended to search for any locatable resource, such as those identified by URLs.

The import machinery is extensible, so new finders can be added to extend the range and scope of module searching.

Finders do not actually load modules. If they can find the named module, they return a `module spec`{.interpreted-text role="dfn"}, an encapsulation of the module\'s import-related information, which the import machinery then uses when loading the module.

The following sections describe the protocol for finders and loaders in more detail, including how you can create and register new ones to extend the import machinery.

::: versionchanged
3.4 In previous versions of Python, finders returned `loaders <loader>`{.interpreted-text role="term"} directly, whereas now they return module specs which *contain* loaders. Loaders are still used during import but have fewer responsibilities.
:::

### Import hooks

::: index
single: import hooks single: meta hooks single: path hooks pair: hooks; import pair: hooks; meta pair: hooks; path
:::

The import machinery is designed to be extensible; the primary mechanism for this are the *import hooks*. There are two types of import hooks: *meta hooks* and *import path hooks*.

Meta hooks are called at the start of import processing, before any other import processing has occurred, other than `sys.modules`{.interpreted-text role="data"} cache look up. This allows meta hooks to override `sys.path`{.interpreted-text role="data"} processing, frozen modules, or even built-in modules. Meta hooks are registered by adding new finder objects to `sys.meta_path`{.interpreted-text role="data"}, as described below.

Import path hooks are called as part of `sys.path`{.interpreted-text role="data"} (or `package.__path__`) processing, at the point where their associated path item is encountered. Import path hooks are registered by adding new callables to `sys.path_hooks`{.interpreted-text role="data"} as described below.

### The meta path

::: index
single: sys.meta_path pair: finder; find_spec
:::

When the named module is not found in `sys.modules`{.interpreted-text role="data"}, Python next searches `sys.meta_path`{.interpreted-text role="data"}, which contains a list of meta path finder objects. These finders are queried in order to see if they know how to handle the named module. Meta path finders must implement a method called `~importlib.abc.MetaPathFinder.find_spec`{.interpreted-text role="meth"} which takes three arguments: a name, an import path, and (optionally) a target module. The meta path finder can use any strategy it wants to determine whether it can handle the named module or not.

If the meta path finder knows how to handle the named module, it returns a spec object. If it cannot handle the named module, it returns `None`. If `sys.meta_path`{.interpreted-text role="data"} processing reaches the end of its list without returning a spec, then a `ModuleNotFoundError`{.interpreted-text role="exc"} is raised. Any other exceptions raised are simply propagated up, aborting the import process.

The `~importlib.abc.MetaPathFinder.find_spec`{.interpreted-text role="meth"} method of meta path finders is called with two or three arguments. The first is the fully qualified name of the module being imported, for example `foo.bar.baz`. The second argument is the path entries to use for the module search. For top-level modules, the second argument is `None`, but for submodules or subpackages, the second argument is the value of the parent package\'s `__path__` attribute. If the appropriate `__path__` attribute cannot be accessed, a `ModuleNotFoundError`{.interpreted-text role="exc"} is raised. The third argument is an existing module object that will be the target of loading later. The import system passes in a target module only during reload.

The meta path may be traversed multiple times for a single import request. For example, assuming none of the modules involved has already been cached, importing `foo.bar.baz` will first perform a top level import, calling `mpf.find_spec("foo", None, None)` on each meta path finder (`mpf`). After `foo` has been imported, `foo.bar` will be imported by traversing the meta path a second time, calling `mpf.find_spec("foo.bar", foo.__path__, None)`. Once `foo.bar` has been imported, the final traversal will call `mpf.find_spec("foo.bar.baz", foo.bar.__path__, None)`.

Some meta path finders only support top level imports. These importers will always return `None` when anything other than `None` is passed as the second argument.

Python\'s default `sys.meta_path`{.interpreted-text role="data"} has three meta path finders, one that knows how to import built-in modules, one that knows how to import frozen modules, and one that knows how to import modules from an `import path`{.interpreted-text role="term"} (i.e. the `path based finder`{.interpreted-text role="term"}).

::: versionchanged
3.4 The `~importlib.abc.MetaPathFinder.find_spec`{.interpreted-text role="meth"} method of meta path finders replaced `!find_module`{.interpreted-text role="meth"}, which is now deprecated. While it will continue to work without change, the import machinery will try it only if the finder does not implement `~importlib.abc.MetaPathFinder.find_spec`{.interpreted-text role="meth"}.
:::

::: versionchanged
3.10 Use of `!find_module`{.interpreted-text role="meth"} by the import system now raises `ImportWarning`{.interpreted-text role="exc"}.
:::

::: versionchanged
3.12 `!find_module`{.interpreted-text role="meth"} has been removed. Use `~importlib.abc.MetaPathFinder.find_spec`{.interpreted-text role="meth"} instead.
:::

## Loading

If and when a module spec is found, the import machinery will use it (and the loader it contains) when loading the module. Here is an approximation of what happens during the loading portion of import:

    module = None
    if spec.loader is not None and hasattr(spec.loader, 'create_module'):
        # It is assumed 'exec_module' will also be defined on the loader.
        module = spec.loader.create_module(spec)
    if module is None:
        module = ModuleType(spec.name)
    # The import-related module attributes get set here:
    _init_module_attrs(spec, module)

    if spec.loader is None:
        # unsupported
        raise ImportError

    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        try:
            del sys.modules[spec.name]
        except KeyError:
            pass
        raise
    return sys.modules[spec.name]

Note the following details:

- If there is an existing module object with the given name in `sys.modules`{.interpreted-text role="data"}, import will have already returned it.
- The module will exist in `sys.modules`{.interpreted-text role="data"} before the loader executes the module code. This is crucial because the module code may (directly or indirectly) import itself; adding it to `sys.modules`{.interpreted-text role="data"} beforehand prevents unbounded recursion in the worst case and multiple loading in the best.
- If loading fails, the failing module \-- and only the failing module \-- gets removed from `sys.modules`{.interpreted-text role="data"}. Any module already in the `sys.modules`{.interpreted-text role="data"} cache, and any module that was successfully loaded as a side-effect, must remain in the cache. This contrasts with reloading where even the failing module is left in `sys.modules`{.interpreted-text role="data"}.
- After the module is created but before execution, the import machinery sets the import-related module attributes (\"\_init_module_attrs\" in the pseudo-code example above), as summarized in a `later section <import-mod-attrs>`{.interpreted-text role="ref"}.
- Module execution is the key moment of loading in which the module\'s namespace gets populated. Execution is entirely delegated to the loader, which gets to decide what gets populated and how.
- The module created during loading and passed to exec_module() may not be the one returned at the end of import[^2].

::: versionchanged
3.4 The import system has taken over the boilerplate responsibilities of loaders. These were previously performed by the `importlib.abc.Loader.load_module` method.
:::

::: versionchanged
3.15 The `load_module` method is no longer used.
:::

### Loaders

Module loaders provide the critical function of loading: module execution. The import machinery calls the `importlib.abc.Loader.exec_module`{.interpreted-text role="meth"} method with a single argument, the module object to execute. Any value returned from `~importlib.abc.Loader.exec_module`{.interpreted-text role="meth"} is ignored.

Loaders must satisfy the following requirements:

- If the module is a Python module (as opposed to a built-in module or a dynamically loaded extension), the loader should execute the module\'s code in the module\'s global name space (`module.__dict__`).
- If the loader cannot execute the module, it should raise an `ImportError`{.interpreted-text role="exc"}, although any other exception raised during `~importlib.abc.Loader.exec_module`{.interpreted-text role="meth"} will be propagated.

In many cases, the finder and loader can be the same object; in such cases the `~importlib.abc.MetaPathFinder.find_spec`{.interpreted-text role="meth"} method would just return a spec with the loader set to `self`.

Module loaders may opt in to creating the module object during loading by implementing a `~importlib.abc.Loader.create_module`{.interpreted-text role="meth"} method. It takes one argument, the module spec, and returns the new module object to use during loading. `create_module()` does not need to set any attributes on the module object. If the method returns `None`, the import machinery will create the new module itself.

::: versionadded
3.4 The `~importlib.abc.Loader.create_module`{.interpreted-text role="meth"} method of loaders.
:::

::: versionchanged
3.4 The `importlib.abc.Loader.load_module` method was replaced by `~importlib.abc.Loader.exec_module`{.interpreted-text role="meth"} and the import machinery assumed all the boilerplate responsibilities of loading.

For compatibility with existing loaders, the import machinery will use the `load_module()` method of loaders if it exists and the loader does not also implement `exec_module()`. However, `load_module()` has been deprecated and loaders should implement `exec_module()` instead.

The `load_module()` method must implement all the boilerplate loading functionality described above in addition to executing the module. All the same constraints apply, with some additional clarification:

- If there is an existing module object with the given name in `sys.modules`{.interpreted-text role="data"}, the loader must use that existing module. (Otherwise, `importlib.reload`{.interpreted-text role="func"} will not work correctly.) If the named module does not exist in `sys.modules`{.interpreted-text role="data"}, the loader must create a new module object and add it to `sys.modules`{.interpreted-text role="data"}.
- The module *must* exist in `sys.modules`{.interpreted-text role="data"} before the loader executes the module code, to prevent unbounded recursion or multiple loading.
- If loading fails, the loader must remove any modules it has inserted into `sys.modules`{.interpreted-text role="data"}, but it must remove **only** the failing module(s), and only if the loader itself has loaded the module(s) explicitly.
:::

::: versionchanged
3.5 A `DeprecationWarning`{.interpreted-text role="exc"} is raised when `exec_module()` is defined but `create_module()` is not.
:::

::: versionchanged
3.6 An `ImportError`{.interpreted-text role="exc"} is raised when `exec_module()` is defined but `create_module()` is not.
:::

::: versionchanged
3.10 Use of `load_module()` will raise `ImportWarning`{.interpreted-text role="exc"}.
:::

### Submodules

When a submodule is loaded using any mechanism (e.g. `importlib` APIs, the `import` or `import-from` statements, or built-in `__import__()`) a binding is placed in the parent module\'s namespace to the submodule object. For example, if package `spam` has a submodule `foo`, after importing `spam.foo`, `spam` will have an attribute `foo` which is bound to the submodule. Let\'s say you have the following directory structure:

    spam/
        __init__.py
        foo.py

and `spam/__init__.py` has the following line in it:

    from .foo import Foo

then executing the following puts name bindings for `foo` and `Foo` in the `spam` module:

    >>> import spam
    >>> spam.foo
    <module 'spam.foo' from '/tmp/imports/spam/foo.py'>
    >>> spam.Foo
    <class 'spam.foo.Foo'>

Given Python\'s familiar name binding rules this might seem surprising, but it\'s actually a fundamental feature of the import system. The invariant holding is that if you have `sys.modules['spam']` and `sys.modules['spam.foo']` (as you would after the above import), the latter must appear as the `foo` attribute of the former.

### Module specs

The import machinery uses a variety of information about each module during import, especially before loading. Most of the information is common to all modules. The purpose of a module\'s spec is to encapsulate this import-related information on a per-module basis.

Using a spec during import allows state to be transferred between import system components, e.g. between the finder that creates the module spec and the loader that executes it. Most importantly, it allows the import machinery to perform the boilerplate operations of loading, whereas without a module spec the loader had that responsibility.

The module\'s spec is exposed as `module.__spec__`{.interpreted-text role="attr"}. Setting `!__spec__`{.interpreted-text role="attr"} appropriately applies equally to `modules initialized during interpreter startup <programs>`{.interpreted-text role="ref"}. The one exception is `__main__`, where `!__spec__`{.interpreted-text role="attr"} is `set to None in some cases <main_spec>`{.interpreted-text role="ref"}.

See `~importlib.machinery.ModuleSpec`{.interpreted-text role="class"} for details on the contents of the module spec.

::: versionadded
3.4
:::

### \_\_path\_\_ attributes on modules {#package-path-rules}

The `~module.__path__`{.interpreted-text role="attr"} attribute should be a (possibly empty) `sequence`{.interpreted-text role="term"} of strings enumerating the locations where the package\'s submodules will be found. By definition, if a module has a `!__path__`{.interpreted-text role="attr"} attribute, it is a `package`{.interpreted-text role="term"}.

A package\'s `~module.__path__`{.interpreted-text role="attr"} attribute is used during imports of its subpackages. Within the import machinery, it functions much the same as `sys.path`{.interpreted-text role="data"}, i.e. providing a list of locations to search for modules during import. However, `!__path__`{.interpreted-text role="attr"} is typically much more constrained than `!sys.path`{.interpreted-text role="data"}.

The same rules used for `sys.path`{.interpreted-text role="data"} also apply to a package\'s `!__path__`{.interpreted-text role="attr"}. `sys.path_hooks`{.interpreted-text role="data"} (described below) are consulted when traversing a package\'s `!__path__`{.interpreted-text role="attr"}.

A package\'s `__init__.py` file may set or alter the package\'s `~module.__path__`{.interpreted-text role="attr"} attribute, and this was typically the way namespace packages were implemented prior to `420`{.interpreted-text role="pep"}. With the adoption of `420`{.interpreted-text role="pep"}, namespace packages no longer need to supply `__init__.py` files containing only `!__path__`{.interpreted-text role="attr"} manipulation code; the import machinery automatically sets `!__path__`{.interpreted-text role="attr"} correctly for the namespace package.

### Module reprs

By default, all modules have a usable repr, however depending on the attributes set above, and in the module\'s spec, you can more explicitly control the repr of module objects.

If the module has a spec (`__spec__`), the import machinery will try to generate a repr from it. If that fails or there is no spec, the import system will craft a default repr using whatever information is available on the module. It will try to use the `module.__name__`, `module.__file__`, and `module.__loader__` as input into the repr, with defaults for whatever information is missing.

Here are the exact rules used:

- If the module has a `__spec__` attribute, the information in the spec is used to generate the repr. The \"name\", \"loader\", \"origin\", and \"has_location\" attributes are consulted.
- If the module has a `__file__` attribute, this is used as part of the module\'s repr.
- If the module has no `__file__` but does have a `__loader__` that is not `None`, then the loader\'s repr is used as part of the module\'s repr.
- Otherwise, just use the module\'s `__name__` in the repr.

::: versionchanged
3.12 Use of `!module_repr`{.interpreted-text role="meth"}, having been deprecated since Python 3.4, was removed in Python 3.12 and is no longer called during the resolution of a module\'s repr.
:::

### Cached bytecode invalidation {#pyc-invalidation}

Before Python loads cached bytecode from a `.pyc` file, it checks whether the cache is up-to-date with the source `.py` file. By default, Python does this by storing the source\'s last-modified timestamp and size in the cache file when writing it. At runtime, the import system then validates the cache file by checking the stored metadata in the cache file against the source\'s metadata.

Python also supports \"hash-based\" cache files, which store a hash of the source file\'s contents rather than its metadata. There are two variants of hash-based `.pyc` files: checked and unchecked. For checked hash-based `.pyc` files, Python validates the cache file by hashing the source file and comparing the resulting hash with the hash in the cache file. If a checked hash-based cache file is found to be invalid, Python regenerates it and writes a new checked hash-based cache file. For unchecked hash-based `.pyc` files, Python simply assumes the cache file is valid if it exists. Hash-based `.pyc` files validation behavior may be overridden with the `--check-hash-based-pycs`{.interpreted-text role="option"} flag.

::: versionchanged
3.7 Added hash-based `.pyc` files. Previously, Python only supported timestamp-based invalidation of bytecode caches.
:::

## The Path Based Finder

::: index
single: path based finder
:::

As mentioned previously, Python comes with several default meta path finders. One of these, called the `path based finder`{.interpreted-text role="term"} (`~importlib.machinery.PathFinder`{.interpreted-text role="class"}), searches an `import path`{.interpreted-text role="term"}, which contains a list of `path entries <path entry>`{.interpreted-text role="term"}. Each path entry names a location to search for modules.

The path based finder itself doesn\'t know how to import anything. Instead, it traverses the individual path entries, associating each of them with a path entry finder that knows how to handle that particular kind of path.

The default set of path entry finders implement all the semantics for finding modules on the file system, handling special file types such as Python source code (`.py` files), Python byte code (`.pyc` files) and shared libraries (e.g. `.so` files). When supported by the `zipimport`{.interpreted-text role="mod"} module in the standard library, the default path entry finders also handle loading all of these file types (other than shared libraries) from zipfiles.

Path entries need not be limited to file system locations. They can refer to URLs, database queries, or any other location that can be specified as a string.

The path based finder provides additional hooks and protocols so that you can extend and customize the types of searchable path entries. For example, if you wanted to support path entries as network URLs, you could write a hook that implements HTTP semantics to find modules on the web. This hook (a callable) would return a `path entry finder`{.interpreted-text role="term"} supporting the protocol described below, which was then used to get a loader for the module from the web.

A word of warning: this section and the previous both use the term *finder*, distinguishing between them by using the terms `meta path finder`{.interpreted-text role="term"} and `path entry finder`{.interpreted-text role="term"}. These two types of finders are very similar, support similar protocols, and function in similar ways during the import process, but it\'s important to keep in mind that they are subtly different. In particular, meta path finders operate at the beginning of the import process, as keyed off the `sys.meta_path`{.interpreted-text role="data"} traversal.

By contrast, path entry finders are in a sense an implementation detail of the path based finder, and in fact, if the path based finder were to be removed from `sys.meta_path`{.interpreted-text role="data"}, none of the path entry finder semantics would be invoked.

### Path entry finders

::: index
single: sys.path single: sys.path_hooks single: sys.path_importer_cache single: PYTHONPATH
:::

The `path based finder`{.interpreted-text role="term"} is responsible for finding and loading Python modules and packages whose location is specified with a string `path entry`{.interpreted-text role="term"}. Most path entries name locations in the file system, but they need not be limited to this.

As a meta path finder, the `path based finder`{.interpreted-text role="term"} implements the `~importlib.abc.MetaPathFinder.find_spec`{.interpreted-text role="meth"} protocol previously described, however it exposes additional hooks that can be used to customize how modules are found and loaded from the `import path`{.interpreted-text role="term"}.

Three variables are used by the `path based finder`{.interpreted-text role="term"}, `sys.path`{.interpreted-text role="data"}, `sys.path_hooks`{.interpreted-text role="data"} and `sys.path_importer_cache`{.interpreted-text role="data"}. The `__path__` attributes on package objects are also used. These provide additional ways that the import machinery can be customized.

`sys.path`{.interpreted-text role="data"} contains a list of strings providing search locations for modules and packages. It is initialized from the `PYTHONPATH`{.interpreted-text role="envvar"} environment variable and various other installation- and implementation-specific defaults. Entries in `sys.path`{.interpreted-text role="data"} can name directories on the file system, zip files, and potentially other \"locations\" (see the `site`{.interpreted-text role="mod"} module) that should be searched for modules, such as URLs, or database queries. Only strings should be present on `sys.path`{.interpreted-text role="data"}; all other data types are ignored.

The `path based finder`{.interpreted-text role="term"} is a `meta path finder`{.interpreted-text role="term"}, so the import machinery begins the `import path`{.interpreted-text role="term"} search by calling the path based finder\'s `~importlib.machinery.PathFinder.find_spec`{.interpreted-text role="meth"} method as described previously. When the `path` argument to `~importlib.machinery.PathFinder.find_spec`{.interpreted-text role="meth"} is given, it will be a list of string paths to traverse - typically a package\'s `__path__` attribute for an import within that package. If the `path` argument is `None`, this indicates a top level import and `sys.path`{.interpreted-text role="data"} is used.

The path based finder iterates over every entry in the search path, and for each of these, looks for an appropriate `path entry finder`{.interpreted-text role="term"} (`~importlib.abc.PathEntryFinder`{.interpreted-text role="class"}) for the path entry. Because this can be an expensive operation (e.g. there may be `stat()` call overheads for this search), the path based finder maintains a cache mapping path entries to path entry finders. This cache is maintained in `sys.path_importer_cache`{.interpreted-text role="data"} (despite the name, this cache actually stores finder objects rather than being limited to `importer`{.interpreted-text role="term"} objects). In this way, the expensive search for a particular `path entry`{.interpreted-text role="term"} location\'s `path entry finder`{.interpreted-text role="term"} need only be done once. User code is free to remove cache entries from `sys.path_importer_cache`{.interpreted-text role="data"} forcing the path based finder to perform the path entry search again.

If the path entry is not present in the cache, the path based finder iterates over every callable in `sys.path_hooks`{.interpreted-text role="data"}. Each of the `path entry
hooks <path entry hook>`{.interpreted-text role="term"} in this list is called with a single argument, the path entry to be searched. This callable may either return a `path
entry finder`{.interpreted-text role="term"} that can handle the path entry, or it may raise `ImportError`{.interpreted-text role="exc"}. An `ImportError`{.interpreted-text role="exc"} is used by the path based finder to signal that the hook cannot find a `path entry finder`{.interpreted-text role="term"} for that `path entry`{.interpreted-text role="term"}. The exception is ignored and `import path`{.interpreted-text role="term"} iteration continues. The hook should expect either a string or bytes object; the encoding of bytes objects is up to the hook (e.g. it may be a file system encoding, UTF-8, or something else), and if the hook cannot decode the argument, it should raise `ImportError`{.interpreted-text role="exc"}.

If `sys.path_hooks`{.interpreted-text role="data"} iteration ends with no `path entry finder`{.interpreted-text role="term"} being returned, then the path based finder\'s `~importlib.machinery.PathFinder.find_spec`{.interpreted-text role="meth"} method will store `None` in `sys.path_importer_cache`{.interpreted-text role="data"} (to indicate that there is no finder for this path entry) and return `None`, indicating that this `meta path finder`{.interpreted-text role="term"} could not find the module.

If a `path entry finder`{.interpreted-text role="term"} *is* returned by one of the `path entry
hook`{.interpreted-text role="term"} callables on `sys.path_hooks`{.interpreted-text role="data"}, then the following protocol is used to ask the finder for a module spec, which is then used when loading the module.

The current working directory \-- denoted by an empty string \-- is handled slightly differently from other entries on `sys.path`{.interpreted-text role="data"}. First, if the current working directory cannot be determined or is found not to exist, no value is stored in `sys.path_importer_cache`{.interpreted-text role="data"}. Second, the value for the current working directory is looked up fresh for each module lookup. Third, the path used for `sys.path_importer_cache`{.interpreted-text role="data"} and returned by `importlib.machinery.PathFinder.find_spec`{.interpreted-text role="meth"} will be the actual current working directory and not the empty string.

### Path entry finder protocol

In order to support imports of modules and initialized packages and also to contribute portions to namespace packages, path entry finders must implement the `~importlib.abc.PathEntryFinder.find_spec`{.interpreted-text role="meth"} method.

`~importlib.abc.PathEntryFinder.find_spec`{.interpreted-text role="meth"} takes two arguments: the fully qualified name of the module being imported, and the (optional) target module. `find_spec()` returns a fully populated spec for the module. This spec will always have \"loader\" set (with one exception).

To indicate to the import machinery that the spec represents a namespace `portion`{.interpreted-text role="term"}, the path entry finder sets `submodule_search_locations` to a list containing the portion.

::: versionchanged
3.4 `~importlib.abc.PathEntryFinder.find_spec`{.interpreted-text role="meth"} replaced `!find_loader`{.interpreted-text role="meth"} and `!find_module`{.interpreted-text role="meth"}, both of which are now deprecated, but will be used if `find_spec()` is not defined.

Older path entry finders may implement one of these two deprecated methods instead of `find_spec()`. The methods are still respected for the sake of backward compatibility. However, if `find_spec()` is implemented on the path entry finder, the legacy methods are ignored.

`!find_loader`{.interpreted-text role="meth"} takes one argument, the fully qualified name of the module being imported. `find_loader()` returns a 2-tuple where the first item is the loader and the second item is a namespace `portion`{.interpreted-text role="term"}.

For backwards compatibility with other implementations of the import protocol, many path entry finders also support the same, traditional `find_module()` method that meta path finders support. However path entry finder `find_module()` methods are never called with a `path` argument (they are expected to record the appropriate path information from the initial call to the path hook).

The `find_module()` method on path entry finders is deprecated, as it does not allow the path entry finder to contribute portions to namespace packages. If both `find_loader()` and `find_module()` exist on a path entry finder, the import system will always call `find_loader()` in preference to `find_module()`.
:::

::: versionchanged
3.10 Calls to `!find_module`{.interpreted-text role="meth"} and `!find_loader`{.interpreted-text role="meth"} by the import system will raise `ImportWarning`{.interpreted-text role="exc"}.
:::

::: versionchanged
3.12 `find_module()` and `find_loader()` have been removed.
:::

## Replacing the standard import system

The most reliable mechanism for replacing the entire import system is to delete the default contents of `sys.meta_path`{.interpreted-text role="data"}, replacing them entirely with a custom meta path hook.

If it is acceptable to only alter the behaviour of import statements without affecting other APIs that access the import system, then replacing the builtin `__import__`{.interpreted-text role="func"} function may be sufficient.

To selectively prevent the import of some modules from a hook early on the meta path (rather than disabling the standard import system entirely), it is sufficient to raise `ModuleNotFoundError`{.interpreted-text role="exc"} directly from `~importlib.abc.MetaPathFinder.find_spec`{.interpreted-text role="meth"} instead of returning `None`. The latter indicates that the meta path search should continue, while raising an exception terminates it immediately.

## Package Relative Imports {#relativeimports}

Relative imports use leading dots. A single leading dot indicates a relative import, starting with the current package. Two or more leading dots indicate a relative import to the parent(s) of the current package, one level per dot after the first. For example, given the following package layout:

    package/
        __init__.py
        subpackage1/
            __init__.py
            moduleX.py
            moduleY.py
        subpackage2/
            __init__.py
            moduleZ.py
        moduleA.py

In either `subpackage1/moduleX.py` or `subpackage1/__init__.py`, the following are valid relative imports:

    from .moduleY import spam
    from .moduleY import spam as ham
    from . import moduleY
    from ..subpackage1 import moduleY
    from ..subpackage2.moduleZ import eggs
    from ..moduleA import foo

Absolute imports may use either the `import <>` or `from <> import <>` syntax, but relative imports may only use the second form; the reason for this is that:

    import XXX.YYY.ZZZ

should expose `XXX.YYY.ZZZ` as a usable expression, but .moduleY is not a valid expression.

## Special considerations for \_\_main\_\_ {#import-dunder-main}

The `__main__`{.interpreted-text role="mod"} module is a special case relative to Python\'s import system. As noted `elsewhere <programs>`{.interpreted-text role="ref"}, the `__main__` module is directly initialized at interpreter startup, much like `sys`{.interpreted-text role="mod"} and `builtins`{.interpreted-text role="mod"}. However, unlike those two, it doesn\'t strictly qualify as a built-in module. This is because the manner in which `__main__` is initialized depends on the flags and other options with which the interpreter is invoked.

### \_\_main\_\_.\_\_spec\_\_ {#main_spec}

Depending on how `__main__`{.interpreted-text role="mod"} is initialized, `__main__.__spec__` gets set appropriately or to `None`.

When Python is started with the `-m`{.interpreted-text role="option"} option, `__spec__` is set to the module spec of the corresponding module or package. `__spec__` is also populated when the `__main__` module is loaded as part of executing a directory, zipfile or other `sys.path`{.interpreted-text role="data"} entry.

In `the remaining cases <using-on-interface-options>`{.interpreted-text role="ref"} `__main__.__spec__` is set to `None`, as the code used to populate the `__main__`{.interpreted-text role="mod"} does not correspond directly with an importable module:

- interactive prompt
- `-c`{.interpreted-text role="option"} option
- running from stdin
- running directly from a source or bytecode file

Note that `__main__.__spec__` is always `None` in the last case, *even if* the file could technically be imported directly as a module instead. Use the `-m`{.interpreted-text role="option"} switch if valid module metadata is desired in `__main__`{.interpreted-text role="mod"}.

Note also that even when `__main__` corresponds with an importable module and `__main__.__spec__` is set accordingly, they\'re still considered *distinct* modules. This is due to the fact that blocks guarded by `if __name__ == "__main__":` checks only execute when the module is used to populate the `__main__` namespace, and not during normal import.

## References

The import machinery has evolved considerably since Python\'s early days. The original [specification for packages](https://www.python.org/doc/essays/packages/) is still available to read, although some details have changed since the writing of that document.

The original specification for `sys.meta_path`{.interpreted-text role="data"} was `302`{.interpreted-text role="pep"}, with subsequent extension in `420`{.interpreted-text role="pep"}.

`420`{.interpreted-text role="pep"} introduced `namespace packages <namespace package>`{.interpreted-text role="term"} for Python 3.3. `420`{.interpreted-text role="pep"} also introduced the `!find_loader`{.interpreted-text role="meth"} protocol as an alternative to `!find_module`{.interpreted-text role="meth"}.

`366`{.interpreted-text role="pep"} describes the addition of the `__package__` attribute for explicit relative imports in main modules.

`328`{.interpreted-text role="pep"} introduced absolute and explicit relative imports and initially proposed `__name__` for semantics `366`{.interpreted-text role="pep"} would eventually specify for `__package__`.

`338`{.interpreted-text role="pep"} defines executing modules as scripts.

`451`{.interpreted-text role="pep"} adds the encapsulation of per-module import state in spec objects. It also off-loads most of the boilerplate responsibilities of loaders back onto the import machinery. These changes allow the deprecation of several APIs in the import system and also addition of new methods to finders and loaders.

**Footnotes**

[^1]: See `types.ModuleType`{.interpreted-text role="class"}.

[^2]: The importlib implementation avoids using the return value directly. Instead, it gets the module object by looking the module name up in `sys.modules`{.interpreted-text role="data"}. The indirect effect of this is that an imported module may replace itself in `sys.modules`{.interpreted-text role="data"}. This is implementation-specific behavior that is not guaranteed to work in other Python implementations.
