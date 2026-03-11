:::: {#memoryview-objects}
::: index
pair: object; memoryview
:::
::::

# MemoryView objects

A `memoryview`{.interpreted-text role="class"} object exposes the C level `buffer interface
<bufferobjects>`{.interpreted-text role="ref"} as a Python object which can then be passed around like any other object.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python memoryview type. This is the same object as `memoryview`{.interpreted-text role="class"} in the Python layer.

> Create a memoryview object from an object that provides the buffer interface. If *obj* supports writable buffer exports, the memoryview object will be read/write, otherwise it may be either read-only or read/write at the discretion of the exporter.

> Flag to request a readonly buffer.

> Flag to request a writable buffer.

> Create a memoryview object using *mem* as the underlying buffer. *flags* can be one of `PyBUF_READ`{.interpreted-text role="c:macro"} or `PyBUF_WRITE`{.interpreted-text role="c:macro"}.
>
> ::: versionadded
> 3.3
> :::

> Create a memoryview object wrapping the given buffer structure *view*. For simple byte buffers, `PyMemoryView_FromMemory`{.interpreted-text role="c:func"} is the preferred function.

> Create a memoryview object to a `contiguous`{.interpreted-text role="term"} chunk of memory (in either \'C\' or \'F\'ortran *order*) from an object that defines the buffer interface. If memory is contiguous, the memoryview object points to the original memory. Otherwise, a copy is made and the memoryview points to a new bytes object.
>
> *buffertype* can be one of `PyBUF_READ`{.interpreted-text role="c:macro"} or `PyBUF_WRITE`{.interpreted-text role="c:macro"}.

> Return true if the object *obj* is a memoryview object. It is not currently allowed to create subclasses of `memoryview`{.interpreted-text role="class"}. This function always succeeds.

> Return a pointer to the memoryview\'s private copy of the exporter\'s buffer. *mview* **must** be a memoryview instance; this macro doesn\'t check its type, you must do it yourself or you will risk crashes.

> Return either a pointer to the exporting object that the memoryview is based on or `NULL` if the memoryview has been created by one of the functions `PyMemoryView_FromMemory`{.interpreted-text role="c:func"} or `PyMemoryView_FromBuffer`{.interpreted-text role="c:func"}. *mview* **must** be a memoryview instance.
