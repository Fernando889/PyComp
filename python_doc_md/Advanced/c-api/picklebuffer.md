:::: {#picklebuffer-objects}
::: index
pair: object; PickleBuffer
:::
::::

# Pickle buffer objects

::: versionadded
3.8
:::

A `pickle.PickleBuffer`{.interpreted-text role="class"} object wraps a `buffer-providing object
<bufferobjects>`{.interpreted-text role="ref"} for out-of-band data transfer with the `pickle`{.interpreted-text role="mod"} module.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python pickle buffer type. This is the same object as `pickle.PickleBuffer`{.interpreted-text role="class"} in the Python layer.

> Return true if *op* is a pickle buffer instance. This function always succeeds.

> Create a pickle buffer from the object *obj*.
>
> This function will fail if *obj* doesn\'t support the `buffer protocol <bufferobjects>`{.interpreted-text role="ref"}.
>
> On success, return a new pickle buffer instance. On failure, set an exception and return `NULL`.
>
> Analogous to calling `pickle.PickleBuffer`{.interpreted-text role="class"} with *obj* in Python.

> Get a pointer to the underlying `Py_buffer`{.interpreted-text role="c:type"} that the pickle buffer wraps.
>
> The returned pointer is valid as long as *picklebuf* is alive and has not been released. The caller must not modify or free the returned `Py_buffer`{.interpreted-text role="c:type"}. If the pickle buffer has been released, raise `ValueError`{.interpreted-text role="exc"}.
>
> On success, return a pointer to the buffer view. On failure, set an exception and return `NULL`.

> Release the underlying buffer held by the pickle buffer.
>
> Return `0` on success. On failure, set an exception and return `-1`.
>
> Analogous to calling `pickle.PickleBuffer.release`{.interpreted-text role="meth"} in Python.
