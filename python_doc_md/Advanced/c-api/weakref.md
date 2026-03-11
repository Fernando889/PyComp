# Weak Reference Objects {#weakrefobjects}

Python supports *weak references* as first-class objects. There are two specific object types which directly implement weak references. The first is a simple reference object, and the second acts as a proxy for the original object as much as it can.

> Return non-zero if *ob* is either a reference or proxy object. This function always succeeds.

> Return non-zero if *ob* is a reference object or a subclass of the reference type. This function always succeeds.

> Return non-zero if *ob* is a reference object, but not a subclass of the reference type. This function always succeeds.

> Return non-zero if *ob* is a proxy object. This function always succeeds.

> Return a weak reference object for the object *ob*. This will always return a new reference, but is not guaranteed to create a new object; an existing reference object may be returned. The second parameter, *callback*, can be a callable object that receives notification when *ob* is garbage collected; it should accept a single parameter, which will be the weak reference object itself. *callback* may also be `None` or `NULL`. If *ob* is not a weakly referenceable object, or if *callback* is not callable, `None`, or `NULL`, this will return `NULL` and raise `TypeError`{.interpreted-text role="exc"}.
>
> ::: seealso
> `PyType_SUPPORTS_WEAKREFS`{.interpreted-text role="c:func"} for checking if *ob* is weakly referenceable.
> :::

> Return a weak reference proxy object for the object *ob*. This will always return a new reference, but is not guaranteed to create a new object; an existing proxy object may be returned. The second parameter, *callback*, can be a callable object that receives notification when *ob* is garbage collected; it should accept a single parameter, which will be the weak reference object itself. *callback* may also be `None` or `NULL`. If *ob* is not a weakly referenceable object, or if *callback* is not callable, `None`, or `NULL`, this will return `NULL` and raise `TypeError`{.interpreted-text role="exc"}.
>
> ::: seealso
> `PyType_SUPPORTS_WEAKREFS`{.interpreted-text role="c:func"} for checking if *ob* is weakly referenceable.
> :::

> Get a `strong reference`{.interpreted-text role="term"} to the referenced object from a weak reference, *ref*, into *\*pobj*.
>
> - On success, set *\*pobj* to a new `strong reference`{.interpreted-text role="term"} to the referenced object and return 1.
> - If the reference is dead, set *\*pobj* to `NULL` and return 0.
> - On error, raise an exception and return -1.
>
> ::: versionadded
> 3.13
> :::

> Test if the weak reference *ref* is dead. Returns 1 if the reference is dead, 0 if it is alive, and -1 with an error set if *ref* is not a weak reference object.
>
> ::: versionadded
> 3.14
> :::

> This function is called by the `~PyTypeObject.tp_dealloc`{.interpreted-text role="c:member"} handler to clear weak references.
>
> This iterates through the weak references for *object* and calls callbacks for those references which have one. It returns when all callbacks have been attempted.

> Clears the weakrefs for *object* without calling the callbacks.
>
> This function is called by the `~PyTypeObject.tp_dealloc`{.interpreted-text role="c:member"} handler for types with finalizers (i.e., `~object.__del__`{.interpreted-text role="meth"}). The handler for those objects first calls `PyObject_ClearWeakRefs`{.interpreted-text role="c:func"} to clear weakrefs and call their callbacks, then the finalizer, and finally this function to clear any weakrefs that may have been created by the finalizer.
>
> In most circumstances, it\'s more appropriate to use `PyObject_ClearWeakRefs`{.interpreted-text role="c:func"} to clear weakrefs instead of this function.
>
> ::: versionadded
> 3.13
> :::
