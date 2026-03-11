# Defining extension modules {#extension-modules}

A C extension for CPython is a shared library (for example, a `.so` file on Linux, `.pyd` DLL on Windows), which is loadable into the Python process (for example, it is compiled with compatible compiler settings), and which exports an `export hook`{.interpreted-text role="dfn"} function (or an old-style `initialization function <extension-pyinit>`{.interpreted-text role="ref"}).

To be importable by default (that is, by `importlib.machinery.ExtensionFileLoader`{.interpreted-text role="py:class"}), the shared library must be available on `sys.path`{.interpreted-text role="py:attr"}, and must be named after the module name plus an extension listed in `importlib.machinery.EXTENSION_SUFFIXES`{.interpreted-text role="py:attr"}.

:::: note
::: title
Note
:::

Building, packaging and distributing extension modules is best done with third-party tools, and is out of scope of this document. One suitable tool is Setuptools, whose documentation can be found at <https://setuptools.pypa.io/en/latest/setuptools.html>.
::::

## Extension export hook

::: versionadded
3.15

Support for the `PyModExport_{<name>}`{.interpreted-text role="samp"} export hook was added in Python 3.15. The older way of defining modules is still available: consult either the `extension-pyinit`{.interpreted-text role="ref"} section or earlier versions of this documentation if you plan to support earlier Python versions.
:::

The export hook must be an exported function with the following signature:

For modules with ASCII-only names, the `export hook <extension-export-hook>`{.interpreted-text role="ref"} must be named `PyModExport_{<name>}`{.interpreted-text role="samp"}, with `<name>` replaced by the module\'s name.

For non-ASCII module names, the export hook must instead be named `PyModExportU_{<name>}`{.interpreted-text role="samp"} (note the `U`), with `<name>` encoded using Python\'s *punycode* encoding with hyphens replaced by underscores. In Python:

``` python
def hook_name(name):
    try:
        suffix = b'_' + name.encode('ascii')
    except UnicodeEncodeError:
        suffix = b'U_' + name.encode('punycode').replace(b'-', b'_')
    return b'PyModExport' + suffix
```

The export hook returns an array of `PyModuleDef_Slot`{.interpreted-text role="c:type"} entries, terminated by an entry with a slot ID of `0`. These slots describe how the module should be created and initialized.

This array must remain valid and constant until interpreter shutdown. Typically, it should use `static` storage. Prefer using the `Py_mod_create`{.interpreted-text role="c:macro"} and `Py_mod_exec`{.interpreted-text role="c:macro"} slots for any dynamic behavior.

The export hook may return `NULL` with an exception set to signal failure.

It is recommended to define the export hook function using a helper macro:

> Declare an extension module export hook. This macro:
>
> - specifies the `PyModuleDef_Slot*`{.interpreted-text role="c:expr"} return type,
> - adds any special linkage declarations required by the platform, and
> - for C++, declares the function as `extern "C"`.

For example, a module called `spam` would be defined like this:

``` c
PyABIInfo_VAR(abi_info);

static PyModuleDef_Slot spam_slots[] = {
    {Py_mod_abi, &abi_info},
    {Py_mod_name, "spam"},
    {Py_mod_init, spam_init_function},
    ...
    {0, NULL},
};

PyMODEXPORT_FUNC
PyModExport_spam(void)
{
    return spam_slots;
}
```

The export hook is typically the only non-`static` item defined in the module\'s C source.

The hook should be kept short \-- ideally, one line as above. If you do need to use Python C API in this function, it is recommended to call `PyABIInfo_Check(&abi_info, "modulename")` first to raise an exception, rather than crash, in common cases of ABI mismatch.

:::: note
::: title
Note
:::

It is possible to export multiple modules from a single shared library by defining multiple export hooks. However, importing them requires a custom importer or suitably named copies/links of the extension file, because Python\'s import machinery only finds the function corresponding to the filename. See the [Multiple modules in one library](https://peps.python.org/pep-0489/#multiple-modules-in-one-library) section in `489`{.interpreted-text role="pep"} for details.
::::

## Multi-phase initialization

The process of creating an extension module follows several phases:

- Python finds and calls the export hook to get information on how to create the module.
- Before any substantial code is executed, Python can determine which capabilities the module supports, and it can adjust the environment or refuse loading an incompatible extension. Slots like `Py_mod_abi`{.interpreted-text role="c:data"}, `Py_mod_gil`{.interpreted-text role="c:data"} and `Py_mod_multiple_interpreters`{.interpreted-text role="c:data"} influence this step.
- By default, Python itself then creates the module object \-- that is, it does the equivalent of calling `~object.__new__`{.interpreted-text role="py:meth"} when creating an object. This step can be overridden using the `Py_mod_create`{.interpreted-text role="c:data"} slot.
- Python sets initial module attributes like `~module.__package__`{.interpreted-text role="attr"} and `~module.__loader__`{.interpreted-text role="attr"}, and inserts the module object into `sys.modules`{.interpreted-text role="py:attr"}.
- Afterwards, the module object is initialized in an extension-specific way \-- the equivalent of `~object.__init__`{.interpreted-text role="py:meth"} when creating an object, or of executing top-level code in a Python-language module. The behavior is specified using the `Py_mod_exec`{.interpreted-text role="c:data"} slot.

This is called *multi-phase initialization* to distinguish it from the legacy (but still supported) `single-phase initialization <single-phase-initialization>`{.interpreted-text role="ref"}, where an initialization function returns a fully constructed module.

::: versionchanged
3.5

Added support for multi-phase initialization (`489`{.interpreted-text role="pep"}).
:::

## Multiple module instances

By default, extension modules are not singletons. For example, if the `sys.modules`{.interpreted-text role="py:attr"} entry is removed and the module is re-imported, a new module object is created and, typically, populated with fresh method and type objects. The old module is subject to normal garbage collection. This mirrors the behavior of pure-Python modules.

Additional module instances may be created in `sub-interpreters <sub-interpreter-support>`{.interpreted-text role="ref"} or after Python runtime reinitialization (`Py_Finalize`{.interpreted-text role="c:func"} and `Py_Initialize`{.interpreted-text role="c:func"}). In these cases, sharing Python objects between module instances would likely cause crashes or undefined behavior.

To avoid such issues, each instance of an extension module should be *isolated*: changes to one instance should not implicitly affect the others, and all state owned by the module, including references to Python objects, should be specific to a particular module instance. See `isolating-extensions-howto`{.interpreted-text role="ref"} for more details and a practical guide.

A simpler way to avoid these issues is `raising an error on repeated initialization <isolating-extensions-optout>`{.interpreted-text role="ref"}.

All modules are expected to support `sub-interpreters <sub-interpreter-support>`{.interpreted-text role="ref"}, or otherwise explicitly signal a lack of support. This is usually achieved by isolation or blocking repeated initialization, as above. A module may also be limited to the main interpreter using the `Py_mod_multiple_interpreters`{.interpreted-text role="c:data"} slot.

## `PyInit` function {#extension-pyinit}

::: deprecated
3.15

This functionality is `soft deprecated`{.interpreted-text role="term"}. It will not get new features, but there are no plans to remove it.
:::

Instead of `PyModExport_modulename`{.interpreted-text role="c:func"}, an extension module can define an older-style `initialization function`{.interpreted-text role="dfn"} with the signature:

Its name should be `PyInit_{<name>}`{.interpreted-text role="samp"}, with `<name>` replaced by the name of the module. For non-ASCII module names, use `PyInitU_{<name>}`{.interpreted-text role="samp"} instead, with `<name>` encoded in the same way as for the `export hook <extension-export-hook>`{.interpreted-text role="ref"} (that is, using Punycode with underscores).

If a module exports both `PyInit_{<name>}`{.interpreted-text role="samp"} and `PyModExport_{<name>}`{.interpreted-text role="samp"}, the `PyInit_{<name>}`{.interpreted-text role="samp"} function is ignored.

Like with `PyMODEXPORT_FUNC`{.interpreted-text role="c:macro"}, it is recommended to define the initialization function using a helper macro:

> Declare an extension module initialization function. This macro:
>
> - specifies the `PyObject*`{.interpreted-text role="c:expr"} return type,
> - adds any special linkage declarations required by the platform, and
> - for C++, declares the function as `extern "C"`.

Normally, the initialization function (`PyInit_modulename`) returns a `PyModuleDef`{.interpreted-text role="c:type"} instance with non-`NULL` `~PyModuleDef.m_slots`{.interpreted-text role="c:member"}. This allows Python to use `multi-phase initialization <multi-phase-initialization>`{.interpreted-text role="ref"}.

Before it is returned, the `PyModuleDef` instance must be initialized using the following function:

> Ensure a module definition is a properly initialized Python object that correctly reports its type and a reference count.
>
> Return *def* cast to `PyObject*`, or `NULL` if an error occurred.
>
> Calling this function is required before returning a `PyModuleDef`{.interpreted-text role="c:type"} from a module initialization function. It should not be used in other contexts.
>
> Note that Python assumes that `PyModuleDef` structures are statically allocated. This function may return either a new reference or a borrowed one; this reference must not be released.
>
> ::: versionadded
> 3.5
> :::

For example, a module called `spam` would be defined like this:

``` c
static struct PyModuleDef spam_module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "spam",
    ...
};

PyMODINIT_FUNC
PyInit_spam(void)
{
    return PyModuleDef_Init(&spam_module);
}
```

### Legacy single-phase initialization {#single-phase-initialization}

::: deprecated
3.15

Single-phase initialization is `soft deprecated`{.interpreted-text role="term"}. It is a legacy mechanism to initialize extension modules, with known drawbacks and design flaws. Extension module authors are encouraged to use multi-phase initialization instead.

However, there are no plans to remove support for it.
:::

In single-phase initialization, the old-style `initialization function <extension-pyinit>`{.interpreted-text role="ref"} (`PyInit_modulename`) should create, populate and return a module object. This is typically done using `PyModule_Create`{.interpreted-text role="c:func"} and functions like `PyModule_AddObjectRef`{.interpreted-text role="c:func"}.

Single-phase initialization differs from the `default <multi-phase-initialization>`{.interpreted-text role="ref"} in the following ways:

- Single-phase modules are, or rather *contain*, "singletons".

  When the module is first initialized, Python saves the contents of the module\'s `__dict__` (that is, typically, the module\'s functions and types).

  For subsequent imports, Python does not call the initialization function again. Instead, it creates a new module object with a new `__dict__`, and copies the saved contents to it. For example, given a single-phase module `_testsinglephase` [^1] that defines a function `sum` and an exception class `error`:

  ``` python
  >>> import sys
  >>> import _testsinglephase as one
  >>> del sys.modules['_testsinglephase']
  >>> import _testsinglephase as two
  >>> one is two
  False
  >>> one.__dict__ is two.__dict__
  False
  >>> one.sum is two.sum
  True
  >>> one.error is two.error
  True
  ```

  The exact behavior should be considered a CPython implementation detail.

- To work around the fact that `PyInit_modulename` does not take a *spec* argument, some state of the import machinery is saved and applied to the first suitable module created during the `PyInit_modulename` call. Specifically, when a sub-module is imported, this mechanism prepends the parent package name to the name of the module.

  A single-phase `PyInit_modulename` function should create "its" module object as soon as possible, before any other module objects can be created.

- Non-ASCII module names (`PyInitU_modulename`) are not supported.

- Single-phase modules support module lookup functions like `PyState_FindModule`{.interpreted-text role="c:func"}.

- The module\'s `PyModuleDef.m_slots`{.interpreted-text role="c:member"} must be NULL.

[^1]: `_testsinglephase` is an internal module used in CPython\'s self-test suite; your installation may or may not include it.
