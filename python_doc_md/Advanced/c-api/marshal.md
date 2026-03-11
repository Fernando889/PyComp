# Data marshalling support {#marshalling-utils}

These routines allow C code to work with serialized objects using the same data format as the `marshal`{.interpreted-text role="mod"} module. There are functions to write data into the serialization format, and additional functions that can be used to read the data back. Files used to store marshalled data must be opened in binary mode.

Numeric values are stored with the least significant byte first.

The module supports several versions of the data format; see the `Python module documentation <marshal>`{.interpreted-text role="py:mod"} for details.

> The current format version. See `marshal.version`{.interpreted-text role="py:data"}.

> Marshal a `long`{.interpreted-text role="c:expr"} integer, *value*, to *file*. This will only write the least-significant 32 bits of *value*; regardless of the size of the native `long`{.interpreted-text role="c:expr"} type. *version* indicates the file format.
>
> This function can fail, in which case it sets the error indicator. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to check for that.

> Marshal a Python object, *value*, to *file*. *version* indicates the file format.
>
> This function can fail, in which case it sets the error indicator. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to check for that.

> Return a bytes object containing the marshalled representation of *value*. *version* indicates the file format.

The following functions allow marshalled values to be read back in.

> Return a C `long`{.interpreted-text role="c:expr"} from the data stream in a `FILE*`{.interpreted-text role="c:expr"} opened for reading. Only a 32-bit value can be read in using this function, regardless of the native size of `long`{.interpreted-text role="c:expr"}.
>
> On error, sets the appropriate exception (`EOFError`{.interpreted-text role="exc"}) and returns `-1`.

> Return a C `short`{.interpreted-text role="c:expr"} from the data stream in a `FILE*`{.interpreted-text role="c:expr"} opened for reading. Only a 16-bit value can be read in using this function, regardless of the native size of `short`{.interpreted-text role="c:expr"}.
>
> On error, sets the appropriate exception (`EOFError`{.interpreted-text role="exc"}) and returns `-1`.

> Return a Python object from the data stream in a `FILE*`{.interpreted-text role="c:expr"} opened for reading.
>
> On error, sets the appropriate exception (`EOFError`{.interpreted-text role="exc"}, `ValueError`{.interpreted-text role="exc"} or `TypeError`{.interpreted-text role="exc"}) and returns `NULL`.

> Return a Python object from the data stream in a `FILE*`{.interpreted-text role="c:expr"} opened for reading. Unlike `PyMarshal_ReadObjectFromFile`{.interpreted-text role="c:func"}, this function assumes that no further objects will be read from the file, allowing it to aggressively load file data into memory so that the de-serialization can operate from data in memory rather than reading a byte at a time from the file. Only use this variant if you are certain that you won\'t be reading anything else from the file.
>
> On error, sets the appropriate exception (`EOFError`{.interpreted-text role="exc"}, `ValueError`{.interpreted-text role="exc"} or `TypeError`{.interpreted-text role="exc"}) and returns `NULL`.

> Return a Python object from the data stream in a byte buffer containing *len* bytes pointed to by *data*.
>
> On error, sets the appropriate exception (`EOFError`{.interpreted-text role="exc"}, `ValueError`{.interpreted-text role="exc"} or `TypeError`{.interpreted-text role="exc"}) and returns `NULL`.
