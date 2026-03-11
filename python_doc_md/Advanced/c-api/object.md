# Object Protocol {#object}

> Get a `strong reference`{.interpreted-text role="term"} to a constant.
>
> Set an exception and return `NULL` if *constant_id* is invalid.
>
> *constant_id* must be one of these constant identifiers:
>
>   Constant Identifier   Value   Returned object
>   --------------------- ------- ----------------------------------------------------
>                         `0`     `None`{.interpreted-text role="py:data"}
>                         `1`     `False`{.interpreted-text role="py:data"}
>                         `2`     `True`{.interpreted-text role="py:data"}
>                         `3`     `Ellipsis`{.interpreted-text role="py:data"}
>                         `4`     `NotImplemented`{.interpreted-text role="py:data"}
>                         `5`     `0`
>                         `6`     `1`
>                         `7`     `''`
>                         `8`     `b''`
>                         `9`     `()`
>
> Numeric values are only given for projects which cannot use the constant identifiers.
>
> ::: versionadded
> 3.13
> :::
>
> ::: impl-detail
> In CPython, all of these constants are `immortal`{.interpreted-text role="term"}.
> :::

> Similar to `Py_GetConstant`{.interpreted-text role="c:func"}, but return a `borrowed
> reference`{.interpreted-text role="term"}.
>
> This function is primarily intended for backwards compatibility: using `Py_GetConstant`{.interpreted-text role="c:func"} is recommended for new code.
>
> The reference is borrowed from the interpreter, and is valid until the interpreter finalization.
>
> ::: versionadded
> 3.13
> :::

> The `NotImplemented` singleton, used to signal that an operation is not implemented for the given type combination.

> Properly handle returning `Py_NotImplemented`{.interpreted-text role="c:data"} from within a C function (that is, create a new `strong reference`{.interpreted-text role="term"} to `NotImplemented`{.interpreted-text role="const"} and return it).

> Flag to be used with multiple functions that print the object (like `PyObject_Print`{.interpreted-text role="c:func"} and `PyFile_WriteObject`{.interpreted-text role="c:func"}). If passed, these functions use the `str`{.interpreted-text role="func"} of the object instead of the `repr`{.interpreted-text role="func"}.

> Print an object *o*, on file *fp*. Returns `-1` on error. The flags argument is used to enable certain printing options. The only option currently supported is `Py_PRINT_RAW`{.interpreted-text role="c:macro"}; if given, the `str`{.interpreted-text role="func"} of the object is written instead of the `repr`{.interpreted-text role="func"}.

> Dump an object *op* to `stderr`. This should only be used for debugging.
>
> The output is intended to try dumping objects even after memory corruption:
>
> - Information is written starting with fields that are the least likely to crash when accessed.
> - This function can be called without an `attached thread state`{.interpreted-text role="term"}, but it\'s not recommended to do so: it can cause deadlocks.
> - An object that does not belong to the current interpreter may be dumped, but this may also cause crashes or unintended behavior.
> - Implement a heuristic to detect if the object memory has been freed. Don\'t display the object contents in this case, only its memory address.
> - The output format may change at any time.
>
> Example of output:
>
> ``` output
> object address  : 0x7f80124702c0
> object refcount : 2
> object type     : 0x9902e0
> object type name: str
> object repr     : 'abcdef'
> ```
>
> ::: versionadded
> 3.15
> :::

> Returns `1` if *o* has the attribute *attr_name*, and `0` otherwise. This is equivalent to the Python expression `hasattr(o, attr_name)`. On failure, return `-1`.
>
> ::: versionadded
> 3.13
> :::

> This is the same as `PyObject_HasAttrWithError`{.interpreted-text role="c:func"}, but *attr_name* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> ::: versionadded
> 3.13
> :::

> Returns `1` if *o* has the attribute *attr_name*, and `0` otherwise. This function always succeeds.
>
> :::: note
> ::: title
> Note
> :::
>
> Exceptions that occur when this calls `~object.__getattr__`{.interpreted-text role="meth"} and `~object.__getattribute__`{.interpreted-text role="meth"} methods aren\'t propagated, but instead given to `sys.unraisablehook`{.interpreted-text role="func"}. For proper error handling, use `PyObject_HasAttrWithError`{.interpreted-text role="c:func"}, `PyObject_GetOptionalAttr`{.interpreted-text role="c:func"} or `PyObject_GetAttr`{.interpreted-text role="c:func"} instead.
> ::::

> This is the same as `PyObject_HasAttr`{.interpreted-text role="c:func"}, but *attr_name* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> :::: note
> ::: title
> Note
> :::
>
> Exceptions that occur when this calls `~object.__getattr__`{.interpreted-text role="meth"} and `~object.__getattribute__`{.interpreted-text role="meth"} methods or while creating the temporary `str`{.interpreted-text role="class"} object are silently ignored. For proper error handling, use `PyObject_HasAttrStringWithError`{.interpreted-text role="c:func"}, `PyObject_GetOptionalAttrString`{.interpreted-text role="c:func"} or `PyObject_GetAttrString`{.interpreted-text role="c:func"} instead.
> ::::

> Retrieve an attribute named *attr_name* from object *o*. Returns the attribute value on success, or `NULL` on failure. This is the equivalent of the Python expression `o.attr_name`.
>
> If the missing attribute should not be treated as a failure, you can use `PyObject_GetOptionalAttr`{.interpreted-text role="c:func"} instead.

> This is the same as `PyObject_GetAttr`{.interpreted-text role="c:func"}, but *attr_name* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> If the missing attribute should not be treated as a failure, you can use `PyObject_GetOptionalAttrString`{.interpreted-text role="c:func"} instead.

> Variant of `PyObject_GetAttr`{.interpreted-text role="c:func"} which doesn\'t raise `AttributeError`{.interpreted-text role="exc"} if the attribute is not found.
>
> If the attribute is found, return `1` and set *\*result* to a new `strong reference`{.interpreted-text role="term"} to the attribute. If the attribute is not found, return `0` and set *\*result* to `NULL`; the `AttributeError`{.interpreted-text role="exc"} is silenced. If an error other than `AttributeError`{.interpreted-text role="exc"} is raised, return `-1` and set *\*result* to `NULL`.
>
> ::: versionadded
> 3.13
> :::

> This is the same as `PyObject_GetOptionalAttr`{.interpreted-text role="c:func"}, but *attr_name* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> ::: versionadded
> 3.13
> :::

> Generic attribute getter function that is meant to be put into a type object\'s `tp_getattro` slot. It looks for a descriptor in the dictionary of classes in the object\'s MRO as well as an attribute in the object\'s `~object.__dict__`{.interpreted-text role="attr"} (if present). As outlined in `descriptors`{.interpreted-text role="ref"}, data descriptors take preference over instance attributes, while non-data descriptors don\'t. Otherwise, an `AttributeError`{.interpreted-text role="exc"} is raised.

> Set the value of the attribute named *attr_name*, for object *o*, to the value *v*. Raise an exception and return `-1` on failure; return `0` on success. This is the equivalent of the Python statement `o.attr_name = v`.
>
> If *v* is `NULL`, the attribute is deleted. This behaviour is deprecated in favour of using `PyObject_DelAttr`{.interpreted-text role="c:func"}, but there are currently no plans to remove it.
>
> The function must not be called with a `NULL` *v* and an exception set. This case can arise from forgetting `NULL` checks and would delete the attribute.
>
> ::: versionchanged
> 3.15 Must not be called with NULL value if an exception is set.
> :::

> This is the same as `PyObject_SetAttr`{.interpreted-text role="c:func"}, but *attr_name* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> If *v* is `NULL`, the attribute is deleted, but this feature is deprecated in favour of using `PyObject_DelAttrString`{.interpreted-text role="c:func"}.
>
> The function must not be called with a `NULL` *v* and an exception set. This case can arise from forgetting `NULL` checks and would delete the attribute.
>
> The number of different attribute names passed to this function should be kept small, usually by using a statically allocated string as *attr_name*. For attribute names that aren\'t known at compile time, prefer calling `PyUnicode_FromString`{.interpreted-text role="c:func"} and `PyObject_SetAttr`{.interpreted-text role="c:func"} directly. For more details, see `PyUnicode_InternFromString`{.interpreted-text role="c:func"}, which may be used internally to create a key object.
>
> ::: versionchanged
> 3.15 Must not be called with NULL value if an exception is set.
> :::

> Generic attribute setter and deleter function that is meant to be put into a type object\'s `~PyTypeObject.tp_setattro`{.interpreted-text role="c:member"} slot. It looks for a data descriptor in the dictionary of classes in the object\'s MRO, and if found it takes preference over setting or deleting the attribute in the instance dictionary. Otherwise, the attribute is set or deleted in the object\'s `~object.__dict__`{.interpreted-text role="attr"} (if present). On success, `0` is returned, otherwise an `AttributeError`{.interpreted-text role="exc"} is raised and `-1` is returned.

> Delete attribute named *attr_name*, for object *o*. Returns `-1` on failure. This is the equivalent of the Python statement `del o.attr_name`.

> This is the same as `PyObject_DelAttr`{.interpreted-text role="c:func"}, but *attr_name* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> The number of different attribute names passed to this function should be kept small, usually by using a statically allocated string as *attr_name*. For attribute names that aren\'t known at compile time, prefer calling `PyUnicode_FromString`{.interpreted-text role="c:func"} and `PyObject_DelAttr`{.interpreted-text role="c:func"} directly. For more details, see `PyUnicode_InternFromString`{.interpreted-text role="c:func"}, which may be used internally to create a key object for lookup.

> A generic implementation for the getter of a `__dict__` descriptor. It creates the dictionary if necessary.
>
> This function may also be called to get the `~object.__dict__`{.interpreted-text role="py:attr"} of the object *o*. Pass `NULL` for *context* when calling it. Since this function may need to allocate memory for the dictionary, it may be more efficient to call `PyObject_GetAttr`{.interpreted-text role="c:func"} when accessing an attribute on the object.
>
> On failure, returns `NULL` with an exception set.
>
> ::: versionadded
> 3.3
> :::

> A generic implementation for the setter of a `__dict__` descriptor. This implementation does not allow the dictionary to be deleted.
>
> ::: versionadded
> 3.3
> :::

> Return a pointer to `~object.__dict__`{.interpreted-text role="py:attr"} of the object *obj*. If there is no `__dict__`, return `NULL` without setting an exception.
>
> This function may need to allocate memory for the dictionary, so it may be more efficient to call `PyObject_GetAttr`{.interpreted-text role="c:func"} when accessing an attribute on the object.

> Compare the values of *o1* and *o2* using the operation specified by *opid*, which must be one of `Py_LT`{.interpreted-text role="c:macro"}, `Py_LE`{.interpreted-text role="c:macro"}, `Py_EQ`{.interpreted-text role="c:macro"}, `Py_NE`{.interpreted-text role="c:macro"}, `Py_GT`{.interpreted-text role="c:macro"}, or `Py_GE`{.interpreted-text role="c:macro"}, corresponding to `<`, `<=`, `==`, `!=`, `>`, or `>=` respectively. This is the equivalent of the Python expression `o1 op o2`, where `op` is the operator corresponding to *opid*. Returns the value of the comparison on success, or `NULL` on failure.

> Compare the values of *o1* and *o2* using the operation specified by *opid*, like `PyObject_RichCompare`{.interpreted-text role="c:func"}, but returns `-1` on error, `0` if the result is false, `1` otherwise.

:::: note
::: title
Note
:::

If *o1* and *o2* are the same object, `PyObject_RichCompareBool`{.interpreted-text role="c:func"} will always return `1` for `Py_EQ`{.interpreted-text role="c:macro"} and `0` for `Py_NE`{.interpreted-text role="c:macro"}.
::::

> Format *obj* using *format_spec*. This is equivalent to the Python expression `format(obj, format_spec)`.
>
> *format_spec* may be `NULL`. In this case the call is equivalent to `format(obj)`. Returns the formatted string on success, `NULL` on failure.

> ::: index
> pair: built-in function; repr
> :::
>
> Compute a string representation of object *o*. Returns the string representation on success, `NULL` on failure. This is the equivalent of the Python expression `repr(o)`. Called by the `repr`{.interpreted-text role="func"} built-in function.
>
> ::: versionchanged
> 3.4 This function now includes a debug assertion to help ensure that it does not silently discard an active exception.
> :::

> ::: index
> pair: built-in function; ascii
> :::
>
> As `PyObject_Repr`{.interpreted-text role="c:func"}, compute a string representation of object *o*, but escape the non-ASCII characters in the string returned by `PyObject_Repr`{.interpreted-text role="c:func"} with `\x`, `\u` or `\U` escapes. This generates a string similar to that returned by `PyObject_Repr`{.interpreted-text role="c:func"} in Python 2. Called by the `ascii`{.interpreted-text role="func"} built-in function.
>
> ::: index
> string; PyObject_Str (C function)
> :::

> Compute a string representation of object *o*. Returns the string representation on success, `NULL` on failure. This is the equivalent of the Python expression `str(o)`. Called by the `str`{.interpreted-text role="func"} built-in function and, therefore, by the `print`{.interpreted-text role="func"} function.
>
> ::: versionchanged
> 3.4 This function now includes a debug assertion to help ensure that it does not silently discard an active exception.
> :::

> ::: index
> pair: built-in function; bytes
> :::
>
> Compute a bytes representation of object *o*. `NULL` is returned on failure and a bytes object on success. This is equivalent to the Python expression `bytes(o)`, when *o* is not an integer. Unlike `bytes(o)`, a TypeError is raised when *o* is an integer instead of a zero-initialized bytes object.

> Return `1` if the class *derived* is identical to or derived from the class *cls*, otherwise return `0`. In case of an error, return `-1`.
>
> If *cls* is a tuple, the check will be done against every entry in *cls*. The result will be `1` when at least one of the checks returns `1`, otherwise it will be `0`.
>
> If *cls* has a `~type.__subclasscheck__`{.interpreted-text role="meth"} method, it will be called to determine the subclass status as described in `3119`{.interpreted-text role="pep"}. Otherwise, *derived* is a subclass of *cls* if it is a direct or indirect subclass, i.e. contained in `cls.__mro__ <type.__mro__>`{.interpreted-text role="attr"}.
>
> Normally only class objects, i.e. instances of `type`{.interpreted-text role="class"} or a derived class, are considered classes. However, objects can override this by having a `~type.__bases__`{.interpreted-text role="attr"} attribute (which must be a tuple of base classes).

> Return `1` if *inst* is an instance of the class *cls* or a subclass of *cls*, or `0` if not. On error, returns `-1` and sets an exception.
>
> If *cls* is a tuple, the check will be done against every entry in *cls*. The result will be `1` when at least one of the checks returns `1`, otherwise it will be `0`.
>
> If *cls* has a `~type.__instancecheck__`{.interpreted-text role="meth"} method, it will be called to determine the subclass status as described in `3119`{.interpreted-text role="pep"}. Otherwise, *inst* is an instance of *cls* if its class is a subclass of *cls*.
>
> An instance *inst* can override what is considered its class by having a `~object.__class__`{.interpreted-text role="attr"} attribute.
>
> An object *cls* can override if it is considered a class, and what its base classes are, by having a `~type.__bases__`{.interpreted-text role="attr"} attribute (which must be a tuple of base classes).

> ::: index
> pair: built-in function; hash
> :::
>
> Compute and return the hash value of an object *o*. On failure, return `-1`. This is the equivalent of the Python expression `hash(o)`.
>
> ::: versionchanged
> 3.2 The return type is now Py_hash_t. This is a signed integer the same size as `Py_ssize_t`{.interpreted-text role="c:type"}.
> :::

> Set a `TypeError`{.interpreted-text role="exc"} indicating that `type(o)` is not `hashable`{.interpreted-text role="term"} and return `-1`. This function receives special treatment when stored in a `tp_hash` slot, allowing a type to explicitly indicate to the interpreter that it is not hashable.

> Returns `1` if the object *o* is considered to be true, and `0` otherwise. This is equivalent to the Python expression `not not o`. On failure, return `-1`.

> Returns `0` if the object *o* is considered to be true, and `1` otherwise. This is equivalent to the Python expression `not o`. On failure, return `-1`.

> ::: index
> pair: built-in function; type
> :::
>
> When *o* is non-`NULL`, returns a type object corresponding to the object type of object *o*. On failure, raises `SystemError`{.interpreted-text role="exc"} and returns `NULL`. This is equivalent to the Python expression `type(o)`. This function creates a new `strong reference`{.interpreted-text role="term"} to the return value. There\'s really no reason to use this function instead of the `Py_TYPE()`{.interpreted-text role="c:func"} function, which returns a pointer of type `PyTypeObject*`{.interpreted-text role="c:expr"}, except when a new `strong reference`{.interpreted-text role="term"} is needed.

> Return non-zero if the object *o* is of type *type* or a subtype of *type*, and `0` otherwise. Both parameters must be non-`NULL`.

> Return an estimated length for the object *o*. First try to return its actual length, then an estimate using `~object.__length_hint__`{.interpreted-text role="meth"}, and finally return the default value. On error return `-1`. This is the equivalent to the Python expression `operator.length_hint(o, defaultvalue)`.
>
> ::: versionadded
> 3.4
> :::

> Return element of *o* corresponding to the object *key* or `NULL` on failure. This is the equivalent of the Python expression `o[key]`.

> Map the object *key* to the value *v*. Raise an exception and return `-1` on failure; return `0` on success. This is the equivalent of the Python statement `o[key] = v`. This function *does not* steal a reference to *v*.

> Remove the mapping for the object *key* from the object *o*. Return `-1` on failure. This is equivalent to the Python statement `del o[key]`.

> This is the same as `PyObject_DelItem`{.interpreted-text role="c:func"}, but *key* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.

> This is equivalent to the Python expression `dir(o)`, returning a (possibly empty) list of strings appropriate for the object argument, or `NULL` if there was an error. If the argument is `NULL`, this is like the Python `dir()`, returning the names of the current locals; in this case, if no execution frame is active then `NULL` is returned but `PyErr_Occurred`{.interpreted-text role="c:func"} will return false.

> This is equivalent to the Python expression `iter(o)`. It returns a new iterator for the object argument, or the object itself if the object is already an iterator. Raises `TypeError`{.interpreted-text role="exc"} and returns `NULL` if the object cannot be iterated.

> This is equivalent to the Python `__iter__(self): return self` method. It is intended for `iterator`{.interpreted-text role="term"} types, to be used in the `PyTypeObject.tp_iter`{.interpreted-text role="c:member"} slot.

> This is the equivalent to the Python expression `aiter(o)`. Takes an `AsyncIterable`{.interpreted-text role="class"} object and returns an `AsyncIterator`{.interpreted-text role="class"} for it. This is typically a new iterator but if the argument is an `AsyncIterator`{.interpreted-text role="class"}, this returns itself. Raises `TypeError`{.interpreted-text role="exc"} and returns `NULL` if the object cannot be iterated.
>
> ::: versionadded
> 3.10
> :::

> Get a pointer to subclass-specific data reserved for *cls*.
>
> The object *o* must be an instance of *cls*, and *cls* must have been created using negative `PyType_Spec.basicsize`{.interpreted-text role="c:member"}. Python does not check this.
>
> On error, set an exception and return `NULL`.
>
> ::: versionadded
> 3.12
> :::

> Return the size of the instance memory space reserved for *cls*, i.e. the size of the memory `PyObject_GetTypeData`{.interpreted-text role="c:func"} returns.
>
> This may be larger than requested using `-PyType_Spec.basicsize <PyType_Spec.basicsize>`{.interpreted-text role="c:member"}; it is safe to use this larger size (e.g. with `!memset`{.interpreted-text role="c:func"}).
>
> The type *cls* **must** have been created using negative `PyType_Spec.basicsize`{.interpreted-text role="c:member"}. Python does not check this.
>
> On error, set an exception and return a negative value.
>
> ::: versionadded
> 3.12
> :::

> Get a pointer to per-item data for a class with `Py_TPFLAGS_ITEMS_AT_END`{.interpreted-text role="c:macro"}.
>
> On error, set an exception and return `NULL`. `TypeError`{.interpreted-text role="py:exc"} is raised if *o* does not have `Py_TPFLAGS_ITEMS_AT_END`{.interpreted-text role="c:macro"} set.
>
> ::: versionadded
> 3.12
> :::

> Visit the managed dictionary of *obj*.
>
> This function must only be called in a traverse function of the type which has the `Py_TPFLAGS_MANAGED_DICT`{.interpreted-text role="c:macro"} flag set.
>
> ::: versionadded
> 3.13
> :::

> Clear the managed dictionary of *obj*.
>
> This function must only be called in a clear function of the type which has the `Py_TPFLAGS_MANAGED_DICT`{.interpreted-text role="c:macro"} flag set.
>
> ::: versionadded
> 3.13
> :::

> Enable [deferred reference counting](https://peps.python.org/pep-0703/#deferred-reference-counting) on *obj*, if supported by the runtime. In the `free-threaded <free threading>`{.interpreted-text role="term"} build, this allows the interpreter to avoid reference count adjustments to *obj*, which may improve multi-threaded performance. The tradeoff is that *obj* will only be deallocated by the tracing garbage collector, and not when the interpreter no longer has any references to it.
>
> This function returns `1` if deferred reference counting is enabled on *obj*, and `0` if deferred reference counting is not supported or if the hint was ignored by the interpreter, such as when deferred reference counting is already enabled on *obj*. This function is thread-safe, and cannot fail.
>
> This function does nothing on builds with the `GIL`{.interpreted-text role="term"} enabled, which do not support deferred reference counting. This also does nothing if *obj* is not an object tracked by the garbage collector (see `gc.is_tracked`{.interpreted-text role="func"} and `PyObject_GC_IsTracked`{.interpreted-text role="c:func"}).
>
> This function is intended to be used soon after *obj* is created, by the code that creates it, such as in the object\'s `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} slot.
>
> ::: versionadded
> 3.14
> :::

> Check if *obj* is a unique temporary object. Returns `1` if *obj* is known to be a unique temporary object, and `0` otherwise. This function cannot fail, but the check is conservative, and may return `0` in some cases even if *obj* is a unique temporary object.
>
> If an object is a unique temporary, it is guaranteed that the current code has the only reference to the object. For arguments to C functions, this should be used instead of checking if the reference count is `1`. Starting with Python 3.14, the interpreter internally avoids some reference count modifications when loading objects onto the operands stack by `borrowing <borrowed reference>`{.interpreted-text role="term"} references when possible, which means that a reference count of `1` by itself does not guarantee that a function argument uniquely referenced.
>
> In the example below, `my_func` is called with a unique temporary object as its argument:
>
> ``` c
> my_func([1, 2, 3])
> ```
>
> In the example below, `my_func` is **not** called with a unique temporary object as its argument, even if its refcount is `1`:
>
> ``` c
> my_list = [1, 2, 3]
> my_func(my_list)
> ```
>
> See also the function `Py_REFCNT`{.interpreted-text role="c:func"}.
>
> ::: versionadded
> 3.14
> :::

> This function returns non-zero if *obj* is `immortal`{.interpreted-text role="term"}, and zero otherwise. This function cannot fail.
>
> :::: note
> ::: title
> Note
> :::
>
> Objects that are immortal in one CPython version are not guaranteed to be immortal in another.
> ::::
>
> ::: versionadded
> 3.14
> :::

> Increments the reference count of *obj* if it is not zero. Returns `1` if the object\'s reference count was successfully incremented. Otherwise, this function returns `0`.
>
> `PyUnstable_EnableTryIncRef`{.interpreted-text role="c:func"} must have been called earlier on *obj* or this function may spuriously return `0` in the `free-threaded build`{.interpreted-text role="term"}.
>
> This function is logically equivalent to the following C code, except that it behaves atomically in the `free-threaded build`{.interpreted-text role="term"}:
>
> ``` c
> if (Py_REFCNT(op) > 0) {
>    Py_INCREF(op);
>    return 1;
> }
> return 0;
> ```
>
> This is intended as a building block for managing weak references without the overhead of a Python `weak reference object <weakrefobjects>`{.interpreted-text role="ref"}.
>
> Typically, correct use of this function requires support from *obj*\'s deallocator (`~PyTypeObject.tp_dealloc`{.interpreted-text role="c:member"}). For example, the following sketch could be adapted to implement a \"weakmap\" that works like a `~weakref.WeakValueDictionary`{.interpreted-text role="py:class"} for a specific type:
>
> ``` c
> PyMutex mutex;
>
> PyObject *
> add_entry(weakmap_key_type *key, PyObject *value)
> {
>     PyUnstable_EnableTryIncRef(value);
>     weakmap_type weakmap = ...;
>     PyMutex_Lock(&mutex);
>     weakmap_add_entry(weakmap, key, value);
>     PyMutex_Unlock(&mutex);
>     Py_RETURN_NONE;
> }
>
> PyObject *
> get_value(weakmap_key_type *key)
> {
>     weakmap_type weakmap = ...;
>     PyMutex_Lock(&mutex);
>     PyObject *result = weakmap_find(weakmap, key);
>     if (PyUnstable_TryIncRef(result)) {
>         // `result` is safe to use
>         PyMutex_Unlock(&mutex);
>         return result;
>     }
>     // if we get here, `result` is starting to be garbage-collected,
>     // but has not been removed from the weakmap yet
>     PyMutex_Unlock(&mutex);
>     return NULL;
> }
>
> // tp_dealloc function for weakmap values
> void
> value_dealloc(PyObject *value)
> {
>     weakmap_type weakmap = ...;
>     PyMutex_Lock(&mutex);
>     weakmap_remove_value(weakmap, value);
>
>     ...
>     PyMutex_Unlock(&mutex);
> }
> ```
>
> ::: versionadded
> 3.14
> :::

> Enables subsequent uses of `PyUnstable_TryIncRef`{.interpreted-text role="c:func"} on *obj*. The caller must hold a `strong reference`{.interpreted-text role="term"} to *obj* when calling this.
>
> ::: versionadded
> 3.14
> :::

> Determine if *op* only has one reference.
>
> On GIL-enabled builds, this function is equivalent to `Py_REFCNT(op) == 1`{.interpreted-text role="c:expr"}.
>
> On a `free-threaded build`{.interpreted-text role="term"}, this checks if *op*\'s `reference count`{.interpreted-text role="term"} is equal to one and additionally checks if *op* is only used by this thread. `Py_REFCNT(op) == 1`{.interpreted-text role="c:expr"} is **not** thread-safe on free-threaded builds; prefer this function.
>
> The caller must hold an `attached thread state`{.interpreted-text role="term"}, despite the fact that this function doesn\'t call into the Python interpreter. This function cannot fail.
>
> ::: versionadded
> 3.14
> :::

> Marks the object *op* `immortal`{.interpreted-text role="term"}. The argument should be uniquely referenced by the calling thread. This is intended to be used for reducing reference counting contention in the `free-threaded build`{.interpreted-text role="term"} for objects which are shared across threads.
>
> This is a one-way process: objects can only be made immortal; they cannot be made mortal once again. Immortal objects do not participate in reference counting and will never be garbage collected. If the object is GC-tracked, it is untracked.
>
> This function is intended to be used soon after *op* is created, by the code that creates it, such as in the object\'s `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} slot. Returns 1 if the object was made immortal and returns 0 if it was not. This function cannot fail.
>
> ::: versionadded
> next
> :::
