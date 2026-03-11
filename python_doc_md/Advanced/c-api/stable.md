# C API and ABI Stability {#stable}

Unless documented otherwise, Python\'s C API is covered by the Backwards Compatibility Policy, `387`{.interpreted-text role="pep"}. Most changes to it are source-compatible (typically by only adding new API). Changing existing API or removing API is only done after a deprecation period or to fix serious issues.

CPython\'s Application Binary Interface (ABI) is forward- and backwards-compatible across a minor release (if these are compiled the same way; see `stable-abi-platform`{.interpreted-text role="ref"} below). So, code compiled for Python 3.10.0 will work on 3.10.8 and vice versa, but will need to be compiled separately for 3.9.x and 3.11.x.

There are two tiers of C API with different stability expectations:

- `Unstable API <unstable-c-api>`{.interpreted-text role="ref"}, may change in minor versions without a deprecation period. It is marked by the `PyUnstable` prefix in names.
- `Limited API <limited-c-api>`{.interpreted-text role="ref"}, is compatible across several minor releases. When `Py_LIMITED_API`{.interpreted-text role="c:macro"} is defined, only this subset is exposed from `Python.h`.

These are discussed in more detail below.

Names prefixed by an underscore, such as `_Py_InternalState`, are private API that can change without notice even in patch releases. If you need to use this API, consider reaching out to [CPython developers](https://discuss.python.org/c/core-dev/c-api/30) to discuss adding public API for your use case.

## Unstable C API

::: index
single: PyUnstable
:::

Any API named with the `PyUnstable` prefix exposes CPython implementation details, and may change in every minor release (e.g. from 3.9 to 3.10) without any deprecation warnings. However, it will not change in a bugfix release (e.g. from 3.10.0 to 3.10.1).

It is generally intended for specialized, low-level tools like debuggers.

Projects that use this API are expected to follow CPython development and spend extra effort adjusting to changes.

## Stable Application Binary Interface

For simplicity, this document talks about *extensions*, but the Limited API and Stable ABI work the same way for all uses of the API -- for example, embedding Python.

### Limited C API

Python 3.2 introduced the *Limited API*, a subset of Python\'s C API. Extensions that only use the Limited API can be compiled once and be loaded on multiple versions of Python. Contents of the Limited API are `listed below <limited-api-list>`{.interpreted-text role="ref"}.

> Define this macro before including `Python.h` to opt in to only use the Limited API, and to select the Limited API version.
>
> Define `Py_LIMITED_API` to the value of `PY_VERSION_HEX`{.interpreted-text role="c:macro"} corresponding to the lowest Python version your extension supports. The extension will be ABI-compatible with all Python 3 releases from the specified one onward, and can use Limited API introduced up to that version.
>
> Rather than using the `PY_VERSION_HEX` macro directly, hardcode a minimum minor version (e.g. `0x030A0000` for Python 3.10) for stability when compiling with future Python versions.
>
> You can also define `Py_LIMITED_API` to `3`. This works the same as `0x03020000` (Python 3.2, the version that introduced Limited API).

### Stable ABI

To enable this, Python provides a *Stable ABI*: a set of symbols that will remain ABI-compatible across Python 3.x versions.

:::: note
::: title
Note
:::

The Stable ABI prevents ABI issues, like linker errors due to missing symbols or data corruption due to changes in structure layouts or function signatures. However, other changes in Python can change the *behavior* of extensions. See Python\'s Backwards Compatibility Policy (`387`{.interpreted-text role="pep"}) for details.
::::

The Stable ABI contains symbols exposed in the `Limited API
<limited-c-api>`{.interpreted-text role="ref"}, but also other ones -- for example, functions necessary to support older versions of the Limited API.

On Windows, extensions that use the Stable ABI should be linked against `python3.dll` rather than a version-specific library such as `python39.dll`.

On some platforms, Python will look for and load shared library files named with the `abi3` tag (e.g. `mymodule.abi3.so`). It does not check if such extensions conform to a Stable ABI. The user (or their packaging tools) need to ensure that, for example, extensions built with the 3.10+ Limited API are not installed for lower versions of Python.

All functions in the Stable ABI are present as functions in Python\'s shared library, not solely as macros. This makes them usable from languages that don\'t use the C preprocessor.

### Limited API Scope and Performance

The goal for the Limited API is to allow everything that is possible with the full C API, but possibly with a performance penalty.

For example, while `PyList_GetItem`{.interpreted-text role="c:func"} is available, its "unsafe" macro variant `PyList_GET_ITEM`{.interpreted-text role="c:func"} is not. The macro can be faster because it can rely on version-specific implementation details of the list object.

Without `Py_LIMITED_API` defined, some C API functions are inlined or replaced by macros. Defining `Py_LIMITED_API` disables this inlining, allowing stability as Python\'s data structures are improved, but possibly reducing performance.

By leaving out the `Py_LIMITED_API` definition, it is possible to compile a Limited API extension with a version-specific ABI. This can improve performance for that Python version, but will limit compatibility. Compiling with `Py_LIMITED_API` will then yield an extension that can be distributed where a version-specific one is not available -- for example, for prereleases of an upcoming Python version.

### Limited API Caveats

Note that compiling with `Py_LIMITED_API` is *not* a complete guarantee that code conforms to the `Limited API <limited-c-api>`{.interpreted-text role="ref"} or the `Stable ABI
<stable-abi>`{.interpreted-text role="ref"}. `Py_LIMITED_API` only covers definitions, but an API also includes other issues, such as expected semantics.

One issue that `Py_LIMITED_API` does not guard against is calling a function with arguments that are invalid in a lower Python version. For example, consider a function that starts accepting `NULL` for an argument. In Python 3.9, `NULL` now selects a default behavior, but in Python 3.8, the argument will be used directly, causing a `NULL` dereference and crash. A similar argument works for fields of structs.

Another issue is that some struct fields are currently not hidden when `Py_LIMITED_API` is defined, even though they\'re part of the Limited API.

For these reasons, we recommend testing an extension with *all* minor Python versions it supports, and preferably to build with the *lowest* such version.

We also recommend reviewing documentation of all used API to check if it is explicitly part of the Limited API. Even with `Py_LIMITED_API` defined, a few private declarations are exposed for technical reasons (or even unintentionally, as bugs).

Also note that the Limited API is not necessarily stable: compiling with `Py_LIMITED_API` with Python 3.8 means that the extension will run with Python 3.12, but it will not necessarily *compile* with Python 3.12. In particular, parts of the Limited API may be deprecated and removed, provided that the Stable ABI stays stable.

## Platform Considerations {#stable-abi-platform}

ABI stability depends not only on Python, but also on the compiler used, lower-level libraries and compiler options. For the purposes of the `Stable ABI <stable-abi>`{.interpreted-text role="ref"}, these details define a "platform". They usually depend on the OS type and processor architecture

It is the responsibility of each particular distributor of Python to ensure that all Python versions on a particular platform are built in a way that does not break the Stable ABI. This is the case with Windows and macOS releases from `python.org` and many third-party distributors.

## ABI Checking

::: versionadded
3.15
:::

Python includes a rudimentary check for ABI compatibility.

This check is not comprehensive. It only guards against common cases of incompatible modules being installed for the wrong interpreter. It also does not take `platform incompatibilities <stable-abi-platform>`{.interpreted-text role="ref"} into account. It can only be done after an extension is successfully loaded.

Despite these limitations, it is recommended that extension modules use this mechanism, so that detectable incompatibilities raise exceptions rather than crash.

Most modules can use this check via the `Py_mod_abi`{.interpreted-text role="c:data"} slot and the `PyABIInfo_VAR`{.interpreted-text role="c:macro"} macro, for example like this:

``` c
PyABIInfo_VAR(abi_info);

static PyModuleDef_Slot mymodule_slots[] = {
   {Py_mod_abi, &abi_info},
   ...
};
```

The full API is described below for advanced use cases.

> Verify that the given *info* is compatible with the currently running interpreter.
>
> Return 0 on success. On failure, raise an exception and return -1.
>
> If the ABI is incompatible, the raised exception will be `ImportError`{.interpreted-text role="py:exc"}.
>
> The *module_name* argument can be `NULL`, or point to a NUL-terminated UTF-8-encoded string used for error messages.
>
> Note that if *info* describes the ABI that the current code uses (as defined by `PyABIInfo_VAR`{.interpreted-text role="c:macro"}, for example), using any other Python C API may lead to crashes. In particular, it is not safe to examine the raised exception.
>
> ::: versionadded
> 3.15
> :::

> Define a static `PyABIInfo`{.interpreted-text role="c:struct"} variable with the given *NAME* that describes the ABI that the current code will use. This macro expands to:
>
> ``` c
> static PyABIInfo NAME = {
>     1, 0,
>     PyABIInfo_DEFAULT_FLAGS,
>     PY_VERSION_HEX,
>     PyABIInfo_DEFAULT_ABI_VERSION
> }
> ```
>
> ::: versionadded
> 3.15
> :::

> > The major version of `PyABIInfo`{.interpreted-text role="c:struct"}. Can be set to:
> >
> > - `0` to skip all checking, or
> > - `1` to specify this version of `!PyABIInfo`{.interpreted-text role="c:struct"}.
>
> > The minor version of `PyABIInfo`{.interpreted-text role="c:struct"}. Must be set to `0`; larger values are reserved for backwards-compatible future versions of `!PyABIInfo`{.interpreted-text role="c:struct"}.
>
> > This field is usually set to the following macro:
> >
> > > Default flags, based on current values of macros such as `Py_LIMITED_API`{.interpreted-text role="c:macro"} and `Py_GIL_DISABLED`{.interpreted-text role="c:macro"}.
> >
> > Alternately, the field can be set to the following flags, combined by bitwise OR. Unused bits must be set to zero.
> >
> > ABI variant \-- one of:
> >
> > > > Specifies that the stable ABI is used.
> > >
> > > > Specifies ABI specific to a particular build of CPython. Internal use only.
> >
> > Free-threading compatibility \-- one of:
> >
> > > > Specifies ABI compatible with free-threading builds of CPython. (That is, ones compiled with `--disable-gil`{.interpreted-text role="option"}; with `t` in `sys.abiflags`{.interpreted-text role="py:data"})
> > >
> > > > Specifies ABI compatible with non-free-threading builds of CPython (ones compiled *without* `--disable-gil`{.interpreted-text role="option"}).
>
> > The version of the Python headers used to build the code, in the format used by `PY_VERSION_HEX`{.interpreted-text role="c:macro"}.
> >
> > This can be set to `0` to skip any checks related to this field. This option is meant mainly for projects that do not use the CPython headers directly, and do not emulate a specific version of them.
>
> > The ABI version.
> >
> > For the Stable ABI, this field should be the value of `Py_LIMITED_API`{.interpreted-text role="c:macro"} (except if `Py_LIMITED_API`{.interpreted-text role="c:macro"} is `3`; use `Py_PACK_VERSION(3, 2)`{.interpreted-text role="c:expr"} in that case).
> >
> > Otherwise, it should be set to `PY_VERSION_HEX`{.interpreted-text role="c:macro"}.
> >
> > It can also be set to `0` to skip any checks related to this field.
> >
> > > The value that should be used for this field, based on current values of macros such as `Py_LIMITED_API`{.interpreted-text role="c:macro"}, `PY_VERSION_HEX`{.interpreted-text role="c:macro"} and `Py_GIL_DISABLED`{.interpreted-text role="c:macro"}.
>
> ::: versionadded
> 3.15
> :::

## Contents of Limited API {#limited-api-list}

Currently, the `Limited API <limited-c-api>`{.interpreted-text role="ref"} includes the following items:

::: limited-api-list
:::
