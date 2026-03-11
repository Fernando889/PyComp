# Allocating Objects on the Heap {#allocating-objects}

> Initialize a newly allocated object *op* with its type and initial reference. Returns the initialized object. Other fields of the object are not initialized. Despite its name, this function is unrelated to the object\'s `~object.__init__`{.interpreted-text role="meth"} method (`~PyTypeObject.tp_init`{.interpreted-text role="c:member"} slot). Specifically, this function does **not** call the object\'s `!__init__`{.interpreted-text role="meth"} method.
>
> In general, consider this function to be a low-level routine. Use `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} where possible. For implementing `!tp_alloc`{.interpreted-text role="c:member"} for your type, prefer `PyType_GenericAlloc`{.interpreted-text role="c:func"} or `PyObject_New`{.interpreted-text role="c:func"}.
>
> :::: note
> ::: title
> Note
> :::
>
> This function only initializes the object\'s memory corresponding to the initial `PyObject`{.interpreted-text role="c:type"} structure. It does not zero the rest.
> ::::

> This does everything `PyObject_Init`{.interpreted-text role="c:func"} does, and also initializes the length information for a variable-size object.
>
> :::: note
> ::: title
> Note
> :::
>
> This function only initializes some of the object\'s memory. It does not zero the rest.
> ::::

> Allocates a new Python object using the C structure type *TYPE* and the Python type object *typeobj* (`PyTypeObject*`) by calling `PyObject_Malloc`{.interpreted-text role="c:func"} to allocate memory and initializing it like `PyObject_Init`{.interpreted-text role="c:func"}. The caller will own the only reference to the object (i.e. its reference count will be one).
>
> Avoid calling this directly to allocate memory for an object; call the type\'s `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} slot instead.
>
> When populating a type\'s `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} slot, `PyType_GenericAlloc`{.interpreted-text role="c:func"} is preferred over a custom function that simply calls this macro.
>
> This macro does not call `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"}, `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} (`~object.__new__`{.interpreted-text role="meth"}), or `~PyTypeObject.tp_init`{.interpreted-text role="c:member"} (`~object.__init__`{.interpreted-text role="meth"}).
>
> This cannot be used for objects with `Py_TPFLAGS_HAVE_GC`{.interpreted-text role="c:macro"} set in `~PyTypeObject.tp_flags`{.interpreted-text role="c:member"}; use `PyObject_GC_New`{.interpreted-text role="c:macro"} instead.
>
> Memory allocated by this macro must be freed with `PyObject_Free`{.interpreted-text role="c:func"} (usually called via the object\'s `~PyTypeObject.tp_free`{.interpreted-text role="c:member"} slot).
>
> :::: note
> ::: title
> Note
> :::
>
> The returned memory is not guaranteed to have been completely zeroed before it was initialized.
> ::::
>
> :::: note
> ::: title
> Note
> :::
>
> This macro does not construct a fully initialized object of the given type; it merely allocates memory and prepares it for further initialization by `~PyTypeObject.tp_init`{.interpreted-text role="c:member"}. To construct a fully initialized object, call *typeobj* instead. For example:
>
> ``` c
> PyObject *foo = PyObject_CallNoArgs((PyObject *)&PyFoo_Type);
> ```
> ::::
>
> ::: seealso
> - `PyObject_Free`{.interpreted-text role="c:func"}
> - `PyObject_GC_New`{.interpreted-text role="c:macro"}
> - `PyType_GenericAlloc`{.interpreted-text role="c:func"}
> - `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"}
> :::

> Like `PyObject_New`{.interpreted-text role="c:macro"} except:
>
> - It allocates enough memory for the *TYPE* structure plus *size* (`Py_ssize_t`) fields of the size given by the `~PyTypeObject.tp_itemsize`{.interpreted-text role="c:member"} field of *typeobj*.
> - The memory is initialized like `PyObject_InitVar`{.interpreted-text role="c:func"}.
>
> This is useful for implementing objects like tuples, which are able to determine their size at construction time. Embedding the array of fields into the same allocation decreases the number of allocations, improving the memory management efficiency.
>
> Avoid calling this directly to allocate memory for an object; call the type\'s `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} slot instead.
>
> When populating a type\'s `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} slot, `PyType_GenericAlloc`{.interpreted-text role="c:func"} is preferred over a custom function that simply calls this macro.
>
> This cannot be used for objects with `Py_TPFLAGS_HAVE_GC`{.interpreted-text role="c:macro"} set in `~PyTypeObject.tp_flags`{.interpreted-text role="c:member"}; use `PyObject_GC_NewVar`{.interpreted-text role="c:macro"} instead.
>
> Memory allocated by this function must be freed with `PyObject_Free`{.interpreted-text role="c:func"} (usually called via the object\'s `~PyTypeObject.tp_free`{.interpreted-text role="c:member"} slot).
>
> :::: note
> ::: title
> Note
> :::
>
> The returned memory is not guaranteed to have been completely zeroed before it was initialized.
> ::::
>
> :::: note
> ::: title
> Note
> :::
>
> This macro does not construct a fully initialized object of the given type; it merely allocates memory and prepares it for further initialization by `~PyTypeObject.tp_init`{.interpreted-text role="c:member"}. To construct a fully initialized object, call *typeobj* instead. For example:
>
> ``` c
> PyObject *list_instance = PyObject_CallNoArgs((PyObject *)&PyList_Type);
> ```
> ::::
>
> ::: seealso
> - `PyObject_Free`{.interpreted-text role="c:func"}
> - `PyObject_GC_NewVar`{.interpreted-text role="c:macro"}
> - `PyType_GenericAlloc`{.interpreted-text role="c:func"}
> - `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"}
> :::

> Object which is visible in Python as `None`. This should only be accessed using the `Py_None`{.interpreted-text role="c:macro"} macro, which evaluates to a pointer to this object.

::: seealso

`moduleobjects`{.interpreted-text role="ref"}

:   To allocate and create extension modules.
:::

## Deprecated aliases

These are `soft deprecated`{.interpreted-text role="term"} aliases to existing functions and macros. They exist solely for backwards compatibility.

  Deprecated alias   Function
  ------------------ -----------------------------------------------------
                     `PyObject_New`{.interpreted-text role="c:macro"}
                     `PyObject_NewVar`{.interpreted-text role="c:macro"}
                     `PyObject_Init`{.interpreted-text role="c:func"}
                     `PyObject_InitVar`{.interpreted-text role="c:func"}
                     `PyObject_Malloc`{.interpreted-text role="c:func"}
                     `PyObject_Realloc`{.interpreted-text role="c:func"}
                     `PyObject_Free`{.interpreted-text role="c:func"}
                     `PyObject_Free`{.interpreted-text role="c:func"}
                     `PyObject_Free`{.interpreted-text role="c:func"}
