::: index
single: buffer protocol single: buffer interface; (see buffer protocol) single: buffer object; (see buffer protocol)
:::

# Buffer Protocol {#bufferobjects}

Certain objects available in Python wrap access to an underlying memory array or *buffer*. Such objects include the built-in `bytes`{.interpreted-text role="class"} and `bytearray`{.interpreted-text role="class"}, and some extension types like `array.array`{.interpreted-text role="class"}. Third-party libraries may define their own types for special purposes, such as image processing or numeric analysis.

While each of these types have their own semantics, they share the common characteristic of being backed by a possibly large memory buffer. It is then desirable, in some situations, to access that buffer directly and without intermediate copying.

Python provides such a facility at the C and Python level in the form of the `buffer protocol <bufferobjects>`{.interpreted-text role="ref"}. This protocol has two sides:

::: index
single: PyBufferProcs (C type)
:::

- on the producer side, a type can export a \"buffer interface\" which allows objects of that type to expose information about their underlying buffer. This interface is described in the section `buffer-structs`{.interpreted-text role="ref"}; for Python see `python-buffer-protocol`{.interpreted-text role="ref"}.
- on the consumer side, several means are available to obtain a pointer to the raw underlying data of an object (for example a method parameter). For Python see `memoryview`{.interpreted-text role="class"}.

Simple objects such as `bytes`{.interpreted-text role="class"} and `bytearray`{.interpreted-text role="class"} expose their underlying buffer in byte-oriented form. Other forms are possible; for example, the elements exposed by an `array.array`{.interpreted-text role="class"} can be multi-byte values.

An example consumer of the buffer interface is the `~io.BufferedIOBase.write`{.interpreted-text role="meth"} method of file objects: any object that can export a series of bytes through the buffer interface can be written to a file. While `!write`{.interpreted-text role="meth"} only needs read-only access to the internal contents of the object passed to it, other methods such as `~io.BufferedIOBase.readinto`{.interpreted-text role="meth"} need write access to the contents of their argument. The buffer interface allows objects to selectively allow or reject exporting of read-write and read-only buffers.

There are two ways for a consumer of the buffer interface to acquire a buffer over a target object:

- call `PyObject_GetBuffer`{.interpreted-text role="c:func"} with the right parameters;
- call `PyArg_ParseTuple`{.interpreted-text role="c:func"} (or one of its siblings) with one of the `y*`, `w*` or `s*` `format codes <arg-parsing>`{.interpreted-text role="ref"}.

In both cases, `PyBuffer_Release`{.interpreted-text role="c:func"} must be called when the buffer isn\'t needed anymore. Failure to do so could lead to various issues such as resource leaks.

::: versionadded
3.12

The buffer protocol is now accessible in Python, see `python-buffer-protocol`{.interpreted-text role="ref"} and `memoryview`{.interpreted-text role="class"}.
:::

## Buffer structure

Buffer structures (or simply \"buffers\") are useful as a way to expose the binary data from another object to the Python programmer. They can also be used as a zero-copy slicing mechanism. Using their ability to reference a block of memory, it is possible to expose any data to the Python programmer quite easily. The memory could be a large, constant array in a C extension, it could be a raw block of memory for manipulation before passing to an operating system library, or it could be used to pass around structured data in its native, in-memory format.

Contrary to most data types exposed by the Python interpreter, buffers are not `PyObject`{.interpreted-text role="c:type"} pointers but rather simple C structures. This allows them to be created and copied very simply. When a generic wrapper around a buffer is needed, a `memoryview <memoryview-objects>`{.interpreted-text role="ref"} object can be created.

For short instructions how to write an exporting object, see `Buffer Object Structures <buffer-structs>`{.interpreted-text role="ref"}. For obtaining a buffer, see `PyObject_GetBuffer`{.interpreted-text role="c:func"}.

> > A pointer to the start of the logical structure described by the buffer fields. This can be any location within the underlying physical memory block of the exporter. For example, with negative `~Py_buffer.strides`{.interpreted-text role="c:member"} the value may point to the end of the memory block.
> >
> > For `contiguous`{.interpreted-text role="term"} arrays, the value points to the beginning of the memory block.
>
> > A new reference to the exporting object. The reference is owned by the consumer and automatically released (i.e. reference count decremented) and set to `NULL` by `PyBuffer_Release`{.interpreted-text role="c:func"}. The field is the equivalent of the return value of any standard C-API function.
> >
> > As a special case, for *temporary* buffers that are wrapped by `PyMemoryView_FromBuffer`{.interpreted-text role="c:func"} or `PyBuffer_FillInfo`{.interpreted-text role="c:func"} this field is `NULL`. In general, exporting objects MUST NOT use this scheme.
>
> > `product(shape) * itemsize`. For contiguous arrays, this is the length of the underlying memory block. For non-contiguous arrays, it is the length that the logical structure would have if it were copied to a contiguous representation.
> >
> > Accessing `((char *)buf)[0] up to ((char *)buf)[len-1]` is only valid if the buffer has been obtained by a request that guarantees contiguity. In most cases such a request will be `PyBUF_SIMPLE`{.interpreted-text role="c:macro"} or `PyBUF_WRITABLE`{.interpreted-text role="c:macro"}.
>
> > An indicator of whether the buffer is read-only. This field is controlled by the `PyBUF_WRITABLE`{.interpreted-text role="c:macro"} flag.
>
> > Item size in bytes of a single element. Same as the value of `struct.calcsize`{.interpreted-text role="func"} called on non-`NULL` `~Py_buffer.format`{.interpreted-text role="c:member"} values.
> >
> > Important exception: If a consumer requests a buffer without the `PyBUF_FORMAT`{.interpreted-text role="c:macro"} flag, `~Py_buffer.format`{.interpreted-text role="c:member"} will be set to `NULL`, but `~Py_buffer.itemsize`{.interpreted-text role="c:member"} still has the value for the original format.
> >
> > If `~Py_buffer.shape`{.interpreted-text role="c:member"} is present, the equality `product(shape) * itemsize == len` still holds and the consumer can use `~Py_buffer.itemsize`{.interpreted-text role="c:member"} to navigate the buffer.
> >
> > If `~Py_buffer.shape`{.interpreted-text role="c:member"} is `NULL` as a result of a `PyBUF_SIMPLE`{.interpreted-text role="c:macro"} or a `PyBUF_WRITABLE`{.interpreted-text role="c:macro"} request, the consumer must disregard `~Py_buffer.itemsize`{.interpreted-text role="c:member"} and assume `itemsize == 1`.
>
> > A *NULL* terminated string in `struct`{.interpreted-text role="mod"} module style syntax describing the contents of a single item. If this is `NULL`, `"B"` (unsigned bytes) is assumed.
> >
> > This field is controlled by the `PyBUF_FORMAT`{.interpreted-text role="c:macro"} flag.
>
> > The number of dimensions the memory represents as an n-dimensional array. If it is `0`, `~Py_buffer.buf`{.interpreted-text role="c:member"} points to a single item representing a scalar. In this case, `~Py_buffer.shape`{.interpreted-text role="c:member"}, `~Py_buffer.strides`{.interpreted-text role="c:member"} and `~Py_buffer.suboffsets`{.interpreted-text role="c:member"} MUST be `NULL`. The maximum number of dimensions is given by `PyBUF_MAX_NDIM`{.interpreted-text role="c:macro"}.
>
> > An array of `Py_ssize_t`{.interpreted-text role="c:type"} of length `~Py_buffer.ndim`{.interpreted-text role="c:member"} indicating the shape of the memory as an n-dimensional array. Note that `shape[0] * ... * shape[ndim-1] * itemsize` MUST be equal to `~Py_buffer.len`{.interpreted-text role="c:member"}.
> >
> > Shape values are restricted to `shape[n] >= 0`. The case `shape[n] == 0` requires special attention. See [complex arrays](#complex-arrays) for further information.
> >
> > The shape array is read-only for the consumer.
>
> > An array of `Py_ssize_t`{.interpreted-text role="c:type"} of length `~Py_buffer.ndim`{.interpreted-text role="c:member"} giving the number of bytes to skip to get to a new element in each dimension.
> >
> > Stride values can be any integer. For regular arrays, strides are usually positive, but a consumer MUST be able to handle the case `strides[n] <= 0`. See [complex arrays](#complex-arrays) for further information.
> >
> > The strides array is read-only for the consumer.
>
> > An array of `Py_ssize_t`{.interpreted-text role="c:type"} of length `~Py_buffer.ndim`{.interpreted-text role="c:member"}. If `suboffsets[n] >= 0`, the values stored along the nth dimension are pointers and the suboffset value dictates how many bytes to add to each pointer after de-referencing. A suboffset value that is negative indicates that no de-referencing should occur (striding in a contiguous memory block).
> >
> > If all suboffsets are negative (i.e. no de-referencing is needed), then this field must be `NULL` (the default value).
> >
> > This type of array representation is used by the Python Imaging Library (PIL). See [complex arrays](#complex-arrays) for further information how to access elements of such an array.
> >
> > The suboffsets array is read-only for the consumer.
>
> > This is for use internally by the exporting object. For example, this might be re-cast as an integer by the exporter and used to store flags about whether or not the shape, strides, and suboffsets arrays must be freed when the buffer is released. The consumer MUST NOT alter this value.

Constants:

> The maximum number of dimensions the memory represents. Exporters MUST respect this limit, consumers of multi-dimensional buffers SHOULD be able to handle up to `!PyBUF_MAX_NDIM`{.interpreted-text role="c:macro"} dimensions. Currently set to 64.

## Buffer request types

Buffers are usually obtained by sending a buffer request to an exporting object via `PyObject_GetBuffer`{.interpreted-text role="c:func"}. Since the complexity of the logical structure of the memory can vary drastically, the consumer uses the *flags* argument to specify the exact buffer type it can handle.

All `Py_buffer`{.interpreted-text role="c:type"} fields are unambiguously defined by the request type.

### request-independent fields

The following fields are not influenced by *flags* and must always be filled in with the correct values: `~Py_buffer.obj`{.interpreted-text role="c:member"}, `~Py_buffer.buf`{.interpreted-text role="c:member"}, `~Py_buffer.len`{.interpreted-text role="c:member"}, `~Py_buffer.itemsize`{.interpreted-text role="c:member"}, `~Py_buffer.ndim`{.interpreted-text role="c:member"}.

### readonly, format

> > Controls the `~Py_buffer.readonly`{.interpreted-text role="c:member"} field. If set, the exporter MUST provide a writable buffer or else report failure. Otherwise, the exporter MAY provide either a read-only or writable buffer, but the choice MUST be consistent for all consumers. For example, `PyBUF_SIMPLE | PyBUF_WRITABLE`{.interpreted-text role="c:expr"} can be used to request a simple writable buffer.
>
> > This is a `soft deprecated`{.interpreted-text role="term"} alias to `PyBUF_WRITABLE`{.interpreted-text role="c:macro"}.
>
> > Controls the `~Py_buffer.format`{.interpreted-text role="c:member"} field. If set, this field MUST be filled in correctly. Otherwise, this field MUST be `NULL`.

`PyBUF_WRITABLE`{.interpreted-text role="c:macro"} can be \|\'d to any of the flags in the next section. Since `PyBUF_SIMPLE`{.interpreted-text role="c:macro"} is defined as 0, `PyBUF_WRITABLE`{.interpreted-text role="c:macro"} can be used as a stand-alone flag to request a simple writable buffer.

`PyBUF_FORMAT`{.interpreted-text role="c:macro"} must be \|\'d to any of the flags except `PyBUF_SIMPLE`{.interpreted-text role="c:macro"}, because the latter already implies format `B` (unsigned bytes). `!PyBUF_FORMAT`{.interpreted-text role="c:macro"} cannot be used on its own.

### shape, strides, suboffsets

The flags that control the logical structure of the memory are listed in decreasing order of complexity. Note that each flag contains all bits of the flags below it.

::: tabularcolumns
[\|p{0.35\\linewidth}\|](##SUBST##|p{0.35\linewidth}|)l[\|l\|](##SUBST##|l|)l\|
:::

+-----------------------------+--------+---------+------------+
| > Request                   | shape  | strides | suboffsets |
+=============================+========+=========+============+
|                             | > yes  | > yes   | if needed  |
+-----------------------------+--------+---------+------------+
|                             | > yes  | > yes   | > NULL     |
+-----------------------------+--------+---------+------------+
|                             | > yes  | > NULL  | > NULL     |
+-----------------------------+--------+---------+------------+
|                             | > NULL | > NULL  | > NULL     |
+-----------------------------+--------+---------+------------+

::: index
contiguous, C-contiguous, Fortran contiguous
:::

### contiguity requests

C or Fortran `contiguity <contiguous>`{.interpreted-text role="term"} can be explicitly requested, with and without stride information. Without stride information, the buffer must be C-contiguous.

::: tabularcolumns
[\|p{0.35\\linewidth}\|](##SUBST##|p{0.35\linewidth}|)l[\|l\|](##SUBST##|l|)l[\|l\|](##SUBST##|l|)
:::

+----------------------------------------------+-------+---------+------------+--------+
| > Request                                    | shape | strides | suboffsets | contig |
+==============================================+=======+=========+============+========+
|                                              | > yes | > yes   | > NULL     | > C    |
+----------------------------------------------+-------+---------+------------+--------+
|                                              | > yes | > yes   | > NULL     | > F    |
+----------------------------------------------+-------+---------+------------+--------+
|                                              | > yes | > yes   | > NULL     | C or F |
+----------------------------------------------+-------+---------+------------+--------+
| `PyBUF_ND`{.interpreted-text role="c:macro"} | > yes | > NULL  | > NULL     | > C    |
+----------------------------------------------+-------+---------+------------+--------+

### compound requests

All possible requests are fully defined by some combination of the flags in the previous section. For convenience, the buffer protocol provides frequently used combinations as single flags.

In the following table *U* stands for undefined contiguity. The consumer would have to call `PyBuffer_IsContiguous`{.interpreted-text role="c:func"} to determine contiguity.

::: tabularcolumns
[\|p{0.35\\linewidth}\|](##SUBST##|p{0.35\linewidth}|)l[\|l\|](##SUBST##|l|)l[\|l\|](##SUBST##|l|)l[\|l\|](##SUBST##|l|)
:::

+----------------------+-------+---------+------------+--------+----------+--------+
| > Request            | shape | strides | suboffsets | contig | readonly | format |
+======================+=======+=========+============+========+==========+========+
|                      | > yes | > yes   | if needed  | > U    | > 0      | > yes  |
+----------------------+-------+---------+------------+--------+----------+--------+
|                      | > yes | > yes   | if needed  | > U    | > 1 or 0 | > yes  |
+----------------------+-------+---------+------------+--------+----------+--------+
|                      | > yes | > yes   | > NULL     | > U    | > 0      | > yes  |
+----------------------+-------+---------+------------+--------+----------+--------+
|                      | > yes | > yes   | > NULL     | > U    | > 1 or 0 | > yes  |
+----------------------+-------+---------+------------+--------+----------+--------+
|                      | > yes | > yes   | > NULL     | > U    | > 0      | > NULL |
+----------------------+-------+---------+------------+--------+----------+--------+
|                      | > yes | > yes   | > NULL     | > U    | > 1 or 0 | > NULL |
+----------------------+-------+---------+------------+--------+----------+--------+
|                      | > yes | > NULL  | > NULL     | > C    | > 0      | > NULL |
+----------------------+-------+---------+------------+--------+----------+--------+
|                      | > yes | > NULL  | > NULL     | > C    | > 1 or 0 | > NULL |
+----------------------+-------+---------+------------+--------+----------+--------+

## Complex arrays

### NumPy-style: shape and strides

The logical structure of NumPy-style arrays is defined by `~Py_buffer.itemsize`{.interpreted-text role="c:member"}, `~Py_buffer.ndim`{.interpreted-text role="c:member"}, `~Py_buffer.shape`{.interpreted-text role="c:member"} and `~Py_buffer.strides`{.interpreted-text role="c:member"}.

If `ndim == 0`, the memory location pointed to by `~Py_buffer.buf`{.interpreted-text role="c:member"} is interpreted as a scalar of size `~Py_buffer.itemsize`{.interpreted-text role="c:member"}. In that case, both `~Py_buffer.shape`{.interpreted-text role="c:member"} and `~Py_buffer.strides`{.interpreted-text role="c:member"} are `NULL`.

If `~Py_buffer.strides`{.interpreted-text role="c:member"} is `NULL`, the array is interpreted as a standard n-dimensional C-array. Otherwise, the consumer must access an n-dimensional array as follows:

``` c
ptr = (char *)buf + indices[0] * strides[0] + ... + indices[n-1] * strides[n-1];
item = *((typeof(item) *)ptr);
```

As noted above, `~Py_buffer.buf`{.interpreted-text role="c:member"} can point to any location within the actual memory block. An exporter can check the validity of a buffer with this function:

``` python
def verify_structure(memlen, itemsize, ndim, shape, strides, offset):
    """Verify that the parameters represent a valid array within
       the bounds of the allocated memory:
           char *mem: start of the physical memory block
           memlen: length of the physical memory block
           offset: (char *)buf - mem
    """
    if offset % itemsize:
        return False
    if offset < 0 or offset+itemsize > memlen:
        return False
    if any(v % itemsize for v in strides):
        return False

    if ndim <= 0:
        return ndim == 0 and not shape and not strides
    if 0 in shape:
        return True

    imin = sum(strides[j]*(shape[j]-1) for j in range(ndim)
               if strides[j] <= 0)
    imax = sum(strides[j]*(shape[j]-1) for j in range(ndim)
               if strides[j] > 0)

    return 0 <= offset+imin and offset+imax+itemsize <= memlen
```

### PIL-style: shape, strides and suboffsets

In addition to the regular items, PIL-style arrays can contain pointers that must be followed in order to get to the next element in a dimension. For example, the regular three-dimensional C-array `char v[2][2][3]` can also be viewed as an array of 2 pointers to 2 two-dimensional arrays: `char (*v[2])[2][3]`. In suboffsets representation, those two pointers can be embedded at the start of `~Py_buffer.buf`{.interpreted-text role="c:member"}, pointing to two `char x[2][3]` arrays that can be located anywhere in memory.

Here is a function that returns a pointer to the element in an N-D array pointed to by an N-dimensional index when there are both non-`NULL` strides and suboffsets:

``` c
void *get_item_pointer(int ndim, void *buf, Py_ssize_t *strides,
                       Py_ssize_t *suboffsets, Py_ssize_t *indices) {
    char *pointer = (char*)buf;
    int i;
    for (i = 0; i < ndim; i++) {
        pointer += strides[i] * indices[i];
        if (suboffsets[i] >=0 ) {
            pointer = *((char**)pointer) + suboffsets[i];
        }
    }
    return (void*)pointer;
}
```

## Buffer-related functions

> Return `1` if *obj* supports the buffer interface otherwise `0`. When `1` is returned, it doesn\'t guarantee that `PyObject_GetBuffer`{.interpreted-text role="c:func"} will succeed. This function always succeeds.

> Send a request to *exporter* to fill in *view* as specified by *flags*. If the exporter cannot provide a buffer of the exact type, it MUST raise `BufferError`{.interpreted-text role="exc"}, set `view->obj` to `NULL` and return `-1`.
>
> On success, fill in *view*, set `view->obj` to a new reference to *exporter* and return 0. In the case of chained buffer providers that redirect requests to a single object, `view->obj` MAY refer to this object instead of *exporter* (See `Buffer Object Structures <buffer-structs>`{.interpreted-text role="ref"}).
>
> Successful calls to `PyObject_GetBuffer`{.interpreted-text role="c:func"} must be paired with calls to `PyBuffer_Release`{.interpreted-text role="c:func"}, similar to `malloc`{.interpreted-text role="c:func"} and `free`{.interpreted-text role="c:func"}. Thus, after the consumer is done with the buffer, `PyBuffer_Release`{.interpreted-text role="c:func"} must be called exactly once.

> Release the buffer *view* and release the `strong reference`{.interpreted-text role="term"} (i.e. decrement the reference count) to the view\'s supporting object, `view->obj`. This function MUST be called when the buffer is no longer being used, otherwise reference leaks may occur.
>
> It is an error to call this function on a buffer that was not obtained via `PyObject_GetBuffer`{.interpreted-text role="c:func"}.

> Return the implied `~Py_buffer.itemsize`{.interpreted-text role="c:member"} from `~Py_buffer.format`{.interpreted-text role="c:member"}. On error, raise an exception and return -1.
>
> ::: versionadded
> 3.9
> :::

> Return `1` if the memory defined by the *view* is C-style (*order* is `'C'`) or Fortran-style (*order* is `'F'`) `contiguous`{.interpreted-text role="term"} or either one (*order* is `'A'`). Return `0` otherwise. This function always succeeds.

> Get the memory area pointed to by the *indices* inside the given *view*. *indices* must point to an array of `view->ndim` indices.

> Copy contiguous *len* bytes from *buf* to *view*. *fort* can be `'C'` or `'F'` (for C-style or Fortran-style ordering). `0` is returned on success, `-1` on error.

> Copy *len* bytes from *src* to its contiguous representation in *buf*. *order* can be `'C'` or `'F'` or `'A'` (for C-style or Fortran-style ordering or either one). `0` is returned on success, `-1` on error.
>
> This function fails if *len* != *src-\>len*.

> Copy data from *src* to *dest* buffer. Can convert between C-style and or Fortran-style buffers.
>
> `0` is returned on success, `-1` on error.

> Fill the *strides* array with byte-strides of a `contiguous`{.interpreted-text role="term"} (C-style if *order* is `'C'` or Fortran-style if *order* is `'F'`) array of the given shape with the given number of bytes per element.

> Handle buffer requests for an exporter that wants to expose *buf* of size *len* with writability set according to *readonly*. *buf* is interpreted as a sequence of unsigned bytes.
>
> The *flags* argument indicates the request type. This function always fills in *view* as specified by flags, unless *buf* has been designated as read-only and `PyBUF_WRITABLE`{.interpreted-text role="c:macro"} is set in *flags*.
>
> On success, set `view->obj` to a new reference to *exporter* and return 0. Otherwise, raise `BufferError`{.interpreted-text role="exc"}, set `view->obj` to `NULL` and return `-1`;
>
> If this function is used as part of a `getbufferproc <buffer-structs>`{.interpreted-text role="ref"}, *exporter* MUST be set to the exporting object and *flags* must be passed unmodified. Otherwise, *exporter* MUST be `NULL`.
