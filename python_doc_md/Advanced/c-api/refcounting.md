# Reference Counting {#countingrefs}

The functions and macros in this section are used for managing reference counts of Python objects.

> Get the reference count of the Python object *o*.
>
> Note that the returned value may not actually reflect how many references to the object are actually held. For example, some objects are `immortal`{.interpreted-text role="term"} and have a very high refcount that does not reflect the actual number of references. Consequently, do not rely on the returned value to be accurate, other than a value of 0 or 1.
>
> Use the `Py_SET_REFCNT()`{.interpreted-text role="c:func"} function to set an object reference count.
>
> :::: note
> ::: title
> Note
> :::
>
> On `free-threaded builds <free-threaded build>`{.interpreted-text role="term"} of Python, returning 1 isn\'t sufficient to determine if it\'s safe to treat *o* as having no access by other threads. Use `PyUnstable_Object_IsUniquelyReferenced`{.interpreted-text role="c:func"} for that instead.
>
> See also the function `PyUnstable_Object_IsUniqueReferencedTemporary()`{.interpreted-text role="c:func"}.
> ::::
>
> ::: versionchanged
> 3.10 `Py_REFCNT()`{.interpreted-text role="c:func"} is changed to the inline static function.
> :::
>
> ::: versionchanged
> 3.11 The parameter type is no longer `const PyObject*`{.interpreted-text role="c:expr"}.
> :::

> Set the object *o* reference counter to *refcnt*.
>
> On `Python build with Free Threading <free-threading-build>`{.interpreted-text role="ref"}, if *refcnt* is larger than `UINT32_MAX`, the object is made `immortal`{.interpreted-text role="term"}.
>
> This function has no effect on `immortal`{.interpreted-text role="term"} objects.
>
> ::: versionadded
> 3.9
> :::
>
> ::: versionchanged
> 3.12 Immortal objects are not modified.
> :::

> Indicate taking a new `strong reference`{.interpreted-text role="term"} to object *o*, indicating it is in use and should not be destroyed.
>
> This function has no effect on `immortal`{.interpreted-text role="term"} objects.
>
> This function is usually used to convert a `borrowed reference`{.interpreted-text role="term"} to a `strong reference`{.interpreted-text role="term"} in-place. The `Py_NewRef`{.interpreted-text role="c:func"} function can be used to create a new `strong reference`{.interpreted-text role="term"}.
>
> When done using the object, release is by calling `Py_DECREF`{.interpreted-text role="c:func"}.
>
> The object must not be `NULL`; if you aren\'t sure that it isn\'t `NULL`, use `Py_XINCREF`{.interpreted-text role="c:func"}.
>
> Do not expect this function to actually modify *o* in any way. For at least `some objects <0683>`{.interpreted-text role="pep"}, this function has no effect.
>
> ::: versionchanged
> 3.12 Immortal objects are not modified.
> :::

> Similar to `Py_INCREF`{.interpreted-text role="c:func"}, but the object *o* can be `NULL`, in which case this has no effect.
>
> See also `Py_XNewRef`{.interpreted-text role="c:func"}.

> Create a new `strong reference`{.interpreted-text role="term"} to an object: call `Py_INCREF`{.interpreted-text role="c:func"} on *o* and return the object *o*.
>
> When the `strong reference`{.interpreted-text role="term"} is no longer needed, `Py_DECREF`{.interpreted-text role="c:func"} should be called on it to release the reference.
>
> The object *o* must not be `NULL`; use `Py_XNewRef`{.interpreted-text role="c:func"} if *o* can be `NULL`.
>
> For example:
>
> ``` c
> Py_INCREF(obj);
> self->attr = obj;
> ```
>
> can be written as:
>
> ``` c
> self->attr = Py_NewRef(obj);
> ```
>
> See also `Py_INCREF`{.interpreted-text role="c:func"}.
>
> ::: versionadded
> 3.10
> :::

> Similar to `Py_NewRef`{.interpreted-text role="c:func"}, but the object *o* can be NULL.
>
> If the object *o* is `NULL`, the function just returns `NULL`.
>
> ::: versionadded
> 3.10
> :::

> Release a `strong reference`{.interpreted-text role="term"} to object *o*, indicating the reference is no longer used.
>
> This function has no effect on `immortal`{.interpreted-text role="term"} objects.
>
> Once the last `strong reference`{.interpreted-text role="term"} is released (i.e. the object\'s reference count reaches 0), the object\'s type\'s deallocation function (which must not be `NULL`) is invoked.
>
> This function is usually used to delete a `strong reference`{.interpreted-text role="term"} before exiting its scope.
>
> The object must not be `NULL`; if you aren\'t sure that it isn\'t `NULL`, use `Py_XDECREF`{.interpreted-text role="c:func"}.
>
> Do not expect this function to actually modify *o* in any way. For at least `some objects <683>`{.interpreted-text role="pep"}, this function has no effect.
>
> :::: warning
> ::: title
> Warning
> :::
>
> The deallocation function can cause arbitrary Python code to be invoked (e.g. when a class instance with a `~object.__del__`{.interpreted-text role="meth"} method is deallocated). While exceptions in such code are not propagated, the executed code has free access to all Python global variables. This means that any object that is reachable from a global variable should be in a consistent state before `Py_DECREF`{.interpreted-text role="c:func"} is invoked. For example, code to delete an object from a list should copy a reference to the deleted object in a temporary variable, update the list data structure, and then call `Py_DECREF`{.interpreted-text role="c:func"} for the temporary variable.
> ::::
>
> ::: versionchanged
> 3.12 Immortal objects are not modified.
> :::

> Similar to `Py_DECREF`{.interpreted-text role="c:func"}, but the object *o* can be `NULL`, in which case this has no effect. The same warning from `Py_DECREF`{.interpreted-text role="c:func"} applies here as well.

> Release a `strong reference`{.interpreted-text role="term"} for object *o*. The object may be `NULL`, in which case the macro has no effect; otherwise the effect is the same as for `Py_DECREF`{.interpreted-text role="c:func"}, except that the argument is also set to `NULL`. The warning for `Py_DECREF`{.interpreted-text role="c:func"} does not apply with respect to the object passed because the macro carefully uses a temporary variable and sets the argument to `NULL` before releasing the reference.
>
> It is a good idea to use this macro whenever releasing a reference to an object that might be traversed during garbage collection.
>
> ::: versionchanged
> 3.12 The macro argument is now only evaluated once. If the argument has side effects, these are no longer duplicated.
> :::

> Indicate taking a new `strong reference`{.interpreted-text role="term"} to object *o*. A function version of `Py_XINCREF`{.interpreted-text role="c:func"}. It can be used for runtime dynamic embedding of Python.

> Release a `strong reference`{.interpreted-text role="term"} to object *o*. A function version of `Py_XDECREF`{.interpreted-text role="c:func"}. It can be used for runtime dynamic embedding of Python.

> Macro safely releasing a `strong reference`{.interpreted-text role="term"} to object *dst* and setting *dst* to *src*.
>
> As in case of `Py_CLEAR`{.interpreted-text role="c:func"}, \"the obvious\" code can be deadly:
>
> ``` c
> Py_DECREF(dst);
> dst = src;
> ```
>
> The safe way is:
>
> ``` c
> Py_SETREF(dst, src);
> ```
>
> That arranges to set *dst* to *src* *before* releasing the reference to the old value of *dst*, so that any code triggered as a side-effect of *dst* getting torn down no longer believes *dst* points to a valid object.
>
> ::: versionadded
> 3.6
> :::
>
> ::: versionchanged
> 3.12 The macro arguments are now only evaluated once. If an argument has side effects, these are no longer duplicated.
> :::

> Variant of `Py_SETREF`{.interpreted-text role="c:macro"} macro that uses `Py_XDECREF`{.interpreted-text role="c:func"} instead of `Py_DECREF`{.interpreted-text role="c:func"}.
>
> ::: versionadded
> 3.6
> :::
>
> ::: versionchanged
> 3.12 The macro arguments are now only evaluated once. If an argument has side effects, these are no longer duplicated.
> :::
