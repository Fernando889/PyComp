# `!marshal`{.interpreted-text role="mod"} \-\-- Internal Python object serialization

::: {.module synopsis="Convert Python objects to streams of bytes and back (with different
constraints)."}
marshal
:::

------------------------------------------------------------------------

This module contains functions that can read and write Python values in a binary format. The format is specific to Python, but independent of machine architecture issues (e.g., you can write a Python value to a file on a PC, transport the file to a Mac, and read it back there). Details of the format are undocumented on purpose; it may change between Python versions (although it rarely does).[^1]

::: index
pair: module; pickle pair: module; shelve
:::

This is not a general \"persistence\" module. For general persistence and transfer of Python objects through RPC calls, see the modules `pickle`{.interpreted-text role="mod"} and `shelve`{.interpreted-text role="mod"}. The `!marshal`{.interpreted-text role="mod"} module exists mainly to support reading and writing the \"pseudo-compiled\" code for Python modules of `.pyc`{.interpreted-text role="file"} files. Therefore, the Python maintainers reserve the right to modify the marshal format in backward incompatible ways should the need arise. The format of code objects is not compatible between Python versions, even if the version of the format is the same. De-serializing a code object in the incorrect Python version has undefined behavior. If you\'re serializing and de-serializing Python objects, use the `pickle`{.interpreted-text role="mod"} module instead \-- the performance is comparable, version independence is guaranteed, and pickle supports a substantially wider range of objects than marshal.

:::: warning
::: title
Warning
:::

The `!marshal`{.interpreted-text role="mod"} module is not intended to be secure against erroneous or maliciously constructed data. Never unmarshal data received from an untrusted or unauthenticated source.
::::

There are functions that read/write files as well as functions operating on bytes-like objects.

::: index
object; code, code object
:::

Not all Python object types are supported; in general, only objects whose value is independent from a particular invocation of Python can be written and read by this module. The following types are supported:

- Numeric types: `int`{.interpreted-text role="class"}, `bool`{.interpreted-text role="class"}, `float`{.interpreted-text role="class"}, `complex`{.interpreted-text role="class"}.
- Strings (`str`{.interpreted-text role="class"}) and `bytes`{.interpreted-text role="class"}. `Bytes-like objects <bytes-like object>`{.interpreted-text role="term"} like `bytearray`{.interpreted-text role="class"} are marshalled as `!bytes`{.interpreted-text role="class"}.
- Containers: `tuple`{.interpreted-text role="class"}, `list`{.interpreted-text role="class"}, `set`{.interpreted-text role="class"}, `frozenset`{.interpreted-text role="class"}, and (since `version`{.interpreted-text role="data"} 5), `slice`{.interpreted-text role="class"}. It should be understood that these are supported only if the values contained therein are themselves supported. Recursive containers are supported since `version`{.interpreted-text role="data"} 3.
- The singletons `None`{.interpreted-text role="const"}, `Ellipsis`{.interpreted-text role="const"} and `StopIteration`{.interpreted-text role="exc"}.
- `code`{.interpreted-text role="class"} objects, if *allow_code* is true. See note above about version dependence.

::: versionchanged
3.4

- Added format version 3, which supports marshalling recursive lists, sets and dictionaries.
- Added format version 4, which supports efficient representations of short strings.
:::

::: versionchanged
3.14

Added format version 5, which allows marshalling slices.
:::

The module defines these functions:

::::: function
dump(value, file, version=version, /, \*, allow_code=True)

Write the value on the open file. The value must be a supported type. The file must be a writeable `binary file`{.interpreted-text role="term"}.

If the value has (or contains an object that has) an unsupported type, a `ValueError`{.interpreted-text role="exc"} exception is raised \-\-- but garbage data will also be written to the file. The object will not be properly read back by `load`{.interpreted-text role="func"}. `Code objects <code-objects>`{.interpreted-text role="ref"} are only supported if *allow_code* is true.

The *version* argument indicates the data format that `dump` should use (see below).

::: audit-event
marshal.dumps value,version marshal.dump
:::

::: versionchanged
3.13 Added the *allow_code* parameter.
:::
:::::

:::::::: function
load(file, /, \*, allow_code=True)

Read one value from the open file and return it. If no valid value is read (e.g. because the data has a different Python version\'s incompatible marshal format), raise `EOFError`{.interpreted-text role="exc"}, `ValueError`{.interpreted-text role="exc"} or `TypeError`{.interpreted-text role="exc"}. `Code objects <code-objects>`{.interpreted-text role="ref"} are only supported if *allow_code* is true. The file must be a readable `binary file`{.interpreted-text role="term"}.

::: audit-event
marshal.load \"\" marshal.load
:::

:::: note
::: title
Note
:::

If an object containing an unsupported type was marshalled with `dump`{.interpreted-text role="func"}, `load`{.interpreted-text role="func"} will substitute `None` for the unmarshallable type.
::::

::: versionchanged
3.10

This call used to raise a `code.__new__` audit event for each code object. Now it raises a single `marshal.load` event for the entire load operation.
:::

::: versionchanged
3.13 Added the *allow_code* parameter.
:::
::::::::

::::: function
dumps(value, version=version, /, \*, allow_code=True)

Return the bytes object that would be written to a file by `dump(value, file)`. The value must be a supported type. Raise a `ValueError`{.interpreted-text role="exc"} exception if value has (or contains an object that has) an unsupported type. `Code objects <code-objects>`{.interpreted-text role="ref"} are only supported if *allow_code* is true.

The *version* argument indicates the data format that `dumps` should use (see below).

::: audit-event
marshal.dumps value,version marshal.dump
:::

::: versionchanged
3.13 Added the *allow_code* parameter.
:::
:::::

:::::: function
loads(bytes, /, \*, allow_code=True)

Convert the `bytes-like object`{.interpreted-text role="term"} to a value. If no valid value is found, raise `EOFError`{.interpreted-text role="exc"}, `ValueError`{.interpreted-text role="exc"} or `TypeError`{.interpreted-text role="exc"}. `Code objects <code-objects>`{.interpreted-text role="ref"} are only supported if *allow_code* is true. Extra bytes in the input are ignored.

::: audit-event
marshal.loads bytes marshal.load
:::

::: versionchanged
3.10

This call used to raise a `code.__new__` audit event for each code object. Now it raises a single `marshal.loads` event for the entire load operation.
:::

::: versionchanged
3.13 Added the *allow_code* parameter.
:::
::::::

In addition, the following constants are defined:

::: data
version

Indicates the format that the module uses. Version 0 is the historical first version; subsequent versions add new features. Generally, a new version becomes the default when it is introduced.

  Version   Available since   New features
  --------- ----------------- -------------------------------------------------------------
  1         Python 2.4        Sharing interned strings
  2         Python 2.5        Binary representation of floats
  3         Python 3.4        Support for object instancing and recursion
  4         Python 3.4        Efficient representation of short strings
  5         Python 3.14       Support for `slice`{.interpreted-text role="class"} objects
:::

**Footnotes**

[^1]: The name of this module stems from a bit of terminology used by the designers of Modula-3 (amongst others), who use the term \"marshalling\" for shipping of data around in a self-contained form. Strictly speaking, \"to marshal\" means to convert some data from internal to external form (in an RPC buffer for instance) and \"unmarshalling\" for the reverse process.
