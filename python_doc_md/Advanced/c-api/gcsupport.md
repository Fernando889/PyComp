# Supporting Cyclic Garbage Collection {#supporting-cycle-detection}

Python\'s support for detecting and collecting garbage which involves circular references requires support from object types which are \"containers\" for other objects which may also be containers. Types which do not store references to other objects, or which only store references to atomic types (such as numbers or strings), do not need to provide any explicit support for garbage collection.

To create a container type, the `~PyTypeObject.tp_flags`{.interpreted-text role="c:member"} field of the type object must include the `Py_TPFLAGS_HAVE_GC`{.interpreted-text role="c:macro"} and provide an implementation of the `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} handler. If instances of the type are mutable, a `~PyTypeObject.tp_clear`{.interpreted-text role="c:member"} implementation must also be provided.

`Py_TPFLAGS_HAVE_GC`{.interpreted-text role="c:macro"}

:   Objects with a type with this flag set must conform with the rules documented here. For convenience these objects will be referred to as container objects.

Constructors for container types must conform to two rules:

1.  The memory for the object must be allocated using `PyObject_GC_New`{.interpreted-text role="c:macro"} or `PyObject_GC_NewVar`{.interpreted-text role="c:macro"}.
2.  Once all the fields which may contain references to other containers are initialized, it must call `PyObject_GC_Track`{.interpreted-text role="c:func"}.

Similarly, the deallocator for the object must conform to a similar pair of rules:

1.  Before fields which refer to other containers are invalidated, `PyObject_GC_UnTrack`{.interpreted-text role="c:func"} must be called.

2.  The object\'s memory must be deallocated using `PyObject_GC_Del`{.interpreted-text role="c:func"}.

    :::: warning
    ::: title
    Warning
    :::

    If a type adds the Py_TPFLAGS_HAVE_GC, then it *must* implement at least a `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} handler or explicitly use one from its subclass or subclasses.

    When calling `PyType_Ready`{.interpreted-text role="c:func"} or some of the APIs that indirectly call it like `PyType_FromSpecWithBases`{.interpreted-text role="c:func"} or `PyType_FromSpec`{.interpreted-text role="c:func"} the interpreter will automatically populate the `~PyTypeObject.tp_flags`{.interpreted-text role="c:member"}, `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} and `~PyTypeObject.tp_clear`{.interpreted-text role="c:member"} fields if the type inherits from a class that implements the garbage collector protocol and the child class does *not* include the `Py_TPFLAGS_HAVE_GC`{.interpreted-text role="c:macro"} flag.
    ::::

> Analogous to `PyObject_New`{.interpreted-text role="c:macro"} but for container objects with the `Py_TPFLAGS_HAVE_GC`{.interpreted-text role="c:macro"} flag set.
>
> Do not call this directly to allocate memory for an object; call the type\'s `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} slot instead.
>
> When populating a type\'s `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} slot, `PyType_GenericAlloc`{.interpreted-text role="c:func"} is preferred over a custom function that simply calls this macro.
>
> Memory allocated by this macro must be freed with `PyObject_GC_Del`{.interpreted-text role="c:func"} (usually called via the object\'s `~PyTypeObject.tp_free`{.interpreted-text role="c:member"} slot).
>
> ::: seealso
> - `PyObject_GC_Del`{.interpreted-text role="c:func"}
> - `PyObject_New`{.interpreted-text role="c:macro"}
> - `PyType_GenericAlloc`{.interpreted-text role="c:func"}
> - `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"}
> :::

> Analogous to `PyObject_NewVar`{.interpreted-text role="c:macro"} but for container objects with the `Py_TPFLAGS_HAVE_GC`{.interpreted-text role="c:macro"} flag set.
>
> Do not call this directly to allocate memory for an object; call the type\'s `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} slot instead.
>
> When populating a type\'s `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} slot, `PyType_GenericAlloc`{.interpreted-text role="c:func"} is preferred over a custom function that simply calls this macro.
>
> Memory allocated by this macro must be freed with `PyObject_GC_Del`{.interpreted-text role="c:func"} (usually called via the object\'s `~PyTypeObject.tp_free`{.interpreted-text role="c:member"} slot).
>
> ::: seealso
> - `PyObject_GC_Del`{.interpreted-text role="c:func"}
> - `PyObject_NewVar`{.interpreted-text role="c:macro"}
> - `PyType_GenericAlloc`{.interpreted-text role="c:func"}
> - `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"}
> :::

> Analogous to `PyObject_GC_New`{.interpreted-text role="c:macro"} but allocates *extra_size* bytes at the end of the object (at offset `~PyTypeObject.tp_basicsize`{.interpreted-text role="c:member"}). The allocated memory is initialized to zeros, except for the `Python object header <PyObject>`{.interpreted-text role="c:type"}.
>
> The extra data will be deallocated with the object, but otherwise it is not managed by Python.
>
> Memory allocated by this function must be freed with `PyObject_GC_Del`{.interpreted-text role="c:func"} (usually called via the object\'s `~PyTypeObject.tp_free`{.interpreted-text role="c:member"} slot).
>
> :::: warning
> ::: title
> Warning
> :::
>
> The function is marked as unstable because the final mechanism for reserving extra data after an instance is not yet decided. For allocating a variable number of fields, prefer using `PyVarObject`{.interpreted-text role="c:type"} and `~PyTypeObject.tp_itemsize`{.interpreted-text role="c:member"} instead.
> ::::
>
> ::: versionadded
> 3.12
> :::

> Resize an object allocated by `PyObject_NewVar`{.interpreted-text role="c:macro"}. Returns the resized object of type `TYPE*` (refers to any C type) or `NULL` on failure.
>
> *op* must be of type `PyVarObject *`{.interpreted-text role="c:expr"} and must not be tracked by the collector yet. *newsize* must be of type `Py_ssize_t`{.interpreted-text role="c:type"}.

> Adds the object *op* to the set of container objects tracked by the collector. The collector can run at unexpected times so objects must be valid while being tracked. This should be called once all the fields followed by the `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} handler become valid, usually near the end of the constructor.

> Returns non-zero if the object implements the garbage collector protocol, otherwise returns 0.
>
> The object cannot be tracked by the garbage collector if this function returns 0.

> Returns 1 if the object type of *op* implements the GC protocol and *op* is being currently tracked by the garbage collector and 0 otherwise.
>
> This is analogous to the Python function `gc.is_tracked`{.interpreted-text role="func"}.
>
> ::: versionadded
> 3.9
> :::

> Returns 1 if the object type of *op* implements the GC protocol and *op* has been already finalized by the garbage collector and 0 otherwise.
>
> This is analogous to the Python function `gc.is_finalized`{.interpreted-text role="func"}.
>
> ::: versionadded
> 3.9
> :::

> Releases memory allocated to an object using `PyObject_GC_New`{.interpreted-text role="c:macro"} or `PyObject_GC_NewVar`{.interpreted-text role="c:macro"}.
>
> Do not call this directly to free an object\'s memory; call the type\'s `~PyTypeObject.tp_free`{.interpreted-text role="c:member"} slot instead.
>
> Do not use this for memory allocated by `PyObject_New`{.interpreted-text role="c:macro"}, `PyObject_NewVar`{.interpreted-text role="c:macro"}, or related allocation functions; use `PyObject_Free`{.interpreted-text role="c:func"} instead.
>
> ::: seealso
> - `PyObject_Free`{.interpreted-text role="c:func"} is the non-GC equivalent of this function.
> - `PyObject_GC_New`{.interpreted-text role="c:macro"}
> - `PyObject_GC_NewVar`{.interpreted-text role="c:macro"}
> - `PyType_GenericAlloc`{.interpreted-text role="c:func"}
> - `~PyTypeObject.tp_free`{.interpreted-text role="c:member"}
> :::

> Remove the object *op* from the set of container objects tracked by the collector. Note that `PyObject_GC_Track`{.interpreted-text role="c:func"} can be called again on this object to add it back to the set of tracked objects. The deallocator (`~PyTypeObject.tp_dealloc`{.interpreted-text role="c:member"} handler) should call this for the object before any of the fields used by the `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} handler become invalid.

::: versionchanged
3.8

The `!_PyObject_GC_TRACK`{.interpreted-text role="c:func"} and `!_PyObject_GC_UNTRACK`{.interpreted-text role="c:func"} macros have been removed from the public C API.
:::

The `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} handler accepts a function parameter of this type:

> Type of the visitor function passed to the `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} handler. The function should be called with an object to traverse as *object* and the third parameter to the `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} handler as *arg*. The Python core uses several visitor functions to implement cyclic garbage detection; it\'s not expected that users will need to write their own visitor functions.

The `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} handler must have the following type:

> Traversal function for a container object. Implementations must call the *visit* function for each object directly contained by *self*, with the parameters to *visit* being the contained object and the *arg* value passed to the handler. The *visit* function must not be called with a `NULL` object argument. If *visit* returns a non-zero value that value should be returned immediately.
>
> The traversal function must not have any side effects. Implementations may not modify the reference counts of any Python objects nor create or destroy any Python objects.

To simplify writing `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} handlers, a `Py_VISIT`{.interpreted-text role="c:func"} macro is provided. In order to use this macro, the `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} implementation must name its arguments exactly *visit* and *arg*:

> If the `PyObject *`{.interpreted-text role="c:expr"} *o* is not `NULL`, call the *visit* callback, with arguments *o* and *arg*. If *visit* returns a non-zero value, then return it. Using this macro, `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} handlers look like:
>
> ``` c
> static int
> my_traverse(Noddy *self, visitproc visit, void *arg)
> {
>     Py_VISIT(self->foo);
>     Py_VISIT(self->bar);
>     return 0;
> }
> ```

The `~PyTypeObject.tp_clear`{.interpreted-text role="c:member"} handler must be of the `inquiry`{.interpreted-text role="c:type"} type, or `NULL` if the object is immutable.

> Drop references that may have created reference cycles. Immutable objects do not have to define this method since they can never directly create reference cycles. Note that the object must still be valid after calling this method (don\'t just call `Py_DECREF`{.interpreted-text role="c:func"} on a reference). The collector will call this method if it detects that this object is involved in a reference cycle.

## Controlling the Garbage Collector State

The C-API provides the following functions for controlling garbage collection runs.

> Perform a full garbage collection, if the garbage collector is enabled. (Note that `gc.collect`{.interpreted-text role="func"} runs it unconditionally.)
>
> Returns the number of collected + unreachable objects which cannot be collected. If the garbage collector is disabled or already collecting, returns `0` immediately. Errors during garbage collection are passed to `sys.unraisablehook`{.interpreted-text role="data"}. This function does not raise exceptions.

> Enable the garbage collector: similar to `gc.enable`{.interpreted-text role="func"}. Returns the previous state, 0 for disabled and 1 for enabled.
>
> ::: versionadded
> 3.10
> :::

> Disable the garbage collector: similar to `gc.disable`{.interpreted-text role="func"}. Returns the previous state, 0 for disabled and 1 for enabled.
>
> ::: versionadded
> 3.10
> :::

> Query the state of the garbage collector: similar to `gc.isenabled`{.interpreted-text role="func"}. Returns the current state, 0 for disabled and 1 for enabled.
>
> ::: versionadded
> 3.10
> :::

## Querying Garbage Collector State

The C-API provides the following interface for querying information about the garbage collector.

> Run supplied *callback* on all live GC-capable objects. *arg* is passed through to all invocations of *callback*.
>
> :::: warning
> ::: title
> Warning
> :::
>
> If new objects are (de)allocated by the callback it is undefined if they will be visited.
>
> Garbage collection is disabled during operation. Explicitly running a collection in the callback may lead to undefined behaviour e.g. visiting the same objects multiple times or not at all.
> ::::
>
> ::: versionadded
> 3.12
> :::

> Type of the visitor function to be passed to `PyUnstable_GC_VisitObjects`{.interpreted-text role="c:func"}. *arg* is the same as the *arg* passed to `PyUnstable_GC_VisitObjects`. Return `1` to continue iteration, return `0` to stop iteration. Other return values are reserved for now so behavior on returning anything else is undefined.
>
> ::: versionadded
> 3.12
> :::
