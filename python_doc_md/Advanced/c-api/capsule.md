# Capsules

::: index
pair: object; Capsule
:::

Refer to `using-capsules`{.interpreted-text role="ref"} for more information on using these objects.

::: versionadded
3.1
:::

> This subtype of `PyObject`{.interpreted-text role="c:type"} represents an opaque value, useful for C extension modules which need to pass an opaque value (as a `void*`{.interpreted-text role="c:expr"} pointer) through Python code to other C code. It is often used to make a C function pointer defined in one module available to other modules, so the regular import mechanism can be used to access C APIs defined in dynamically loaded modules.

> The type object corresponding to capsule objects. This is the same object as `types.CapsuleType`{.interpreted-text role="class"} in the Python layer.

> The type of a destructor callback for a capsule. Defined as:
>
> ``` c
> typedef void (*PyCapsule_Destructor)(PyObject *);
> ```
>
> See `PyCapsule_New`{.interpreted-text role="c:func"} for the semantics of PyCapsule_Destructor callbacks.

> Return true if its argument is a `PyCapsule`{.interpreted-text role="c:type"}. This function always succeeds.

> Create a `PyCapsule`{.interpreted-text role="c:type"} encapsulating the *pointer*. The *pointer* argument may not be `NULL`.
>
> On failure, set an exception and return `NULL`.
>
> The *name* string may either be `NULL` or a pointer to a valid C string. If non-`NULL`, this string must outlive the capsule. (Though it is permitted to free it inside the *destructor*.)
>
> If the *destructor* argument is not `NULL`, it will be called with the capsule as its argument when it is destroyed.
>
> If this capsule will be stored as an attribute of a module, the *name* should be specified as `modulename.attributename`. This will enable other modules to import the capsule using `PyCapsule_Import`{.interpreted-text role="c:func"}.

> Retrieve the *pointer* stored in the capsule. On failure, set an exception and return `NULL`.
>
> The *name* parameter must compare exactly to the name stored in the capsule. If the name stored in the capsule is `NULL`, the *name* passed in must also be `NULL`. Python uses the C function `!strcmp`{.interpreted-text role="c:func"} to compare capsule names.

> Return the current destructor stored in the capsule. On failure, set an exception and return `NULL`.
>
> It is legal for a capsule to have a `NULL` destructor. This makes a `NULL` return code somewhat ambiguous; use `PyCapsule_IsValid`{.interpreted-text role="c:func"} or `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.

> Return the current context stored in the capsule. On failure, set an exception and return `NULL`.
>
> It is legal for a capsule to have a `NULL` context. This makes a `NULL` return code somewhat ambiguous; use `PyCapsule_IsValid`{.interpreted-text role="c:func"} or `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.

> Return the current name stored in the capsule. On failure, set an exception and return `NULL`.
>
> It is legal for a capsule to have a `NULL` name. This makes a `NULL` return code somewhat ambiguous; use `PyCapsule_IsValid`{.interpreted-text role="c:func"} or `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.

> Import a pointer to a C object from a capsule attribute in a module. The *name* parameter should specify the full name to the attribute, as in `module.attribute`. The *name* stored in the capsule must match this string exactly.
>
> This function splits *name* on the `.` character, and imports the first element. It then processes further elements using attribute lookups.
>
> Return the capsule\'s internal *pointer* on success. On failure, set an exception and return `NULL`.
>
> :::: note
> ::: title
> Note
> :::
>
> If *name* points to an attribute of some submodule or subpackage, this submodule or subpackage must be previously imported using other means (for example, by using `PyImport_ImportModule`{.interpreted-text role="c:func"}) for the attribute lookups to succeed.
> ::::
>
> ::: versionchanged
> 3.3 *no_block* has no effect anymore.
> :::

> Determines whether or not *capsule* is a valid capsule. A valid capsule is non-`NULL`, passes `PyCapsule_CheckExact`{.interpreted-text role="c:func"}, has a non-`NULL` pointer stored in it, and its internal name matches the *name* parameter. (See `PyCapsule_GetPointer`{.interpreted-text role="c:func"} for information on how capsule names are compared.)
>
> In other words, if `PyCapsule_IsValid`{.interpreted-text role="c:func"} returns a true value, calls to any of the accessors (any function starting with `PyCapsule_Get`) are guaranteed to succeed.
>
> Return a nonzero value if the object is valid and matches the name passed in. Return `0` otherwise. This function will not fail.

> Set the context pointer inside *capsule* to *context*.
>
> Return `0` on success. Return nonzero and set an exception on failure.

> Set the destructor inside *capsule* to *destructor*.
>
> Return `0` on success. Return nonzero and set an exception on failure.

> Set the name inside *capsule* to *name*. If non-`NULL`, the name must outlive the capsule. If the previous *name* stored in the capsule was not `NULL`, no attempt is made to free it.
>
> Return `0` on success. Return nonzero and set an exception on failure.

> Set the void pointer inside *capsule* to *pointer*. The pointer may not be `NULL`.
>
> Return `0` on success. Return nonzero and set an exception on failure.
