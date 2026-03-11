# Call Protocol {#call}

CPython supports two different calling protocols: *tp_call* and vectorcall.

## The *tp_call* Protocol

Instances of classes that set `~PyTypeObject.tp_call`{.interpreted-text role="c:member"} are callable. The signature of the slot is:

``` c
PyObject *tp_call(PyObject *callable, PyObject *args, PyObject *kwargs);
```

A call is made using a tuple for the positional arguments and a dict for the keyword arguments, similarly to `callable(*args, **kwargs)` in Python code. *args* must be non-NULL (use an empty tuple if there are no arguments) but *kwargs* may be *NULL* if there are no keyword arguments.

This convention is not only used by *tp_call*: `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} and `~PyTypeObject.tp_init`{.interpreted-text role="c:member"} also pass arguments this way.

To call an object, use `PyObject_Call`{.interpreted-text role="c:func"} or another `call API <capi-call>`{.interpreted-text role="ref"}.

## The Vectorcall Protocol {#vectorcall}

::: versionadded
3.9
:::

The vectorcall protocol was introduced in `590`{.interpreted-text role="pep"} as an additional protocol for making calls more efficient.

As rule of thumb, CPython will prefer the vectorcall for internal calls if the callable supports it. However, this is not a hard rule. Additionally, some third-party extensions use *tp_call* directly (rather than using `PyObject_Call`{.interpreted-text role="c:func"}). Therefore, a class supporting vectorcall must also implement `~PyTypeObject.tp_call`{.interpreted-text role="c:member"}. Moreover, the callable must behave the same regardless of which protocol is used. The recommended way to achieve this is by setting `~PyTypeObject.tp_call`{.interpreted-text role="c:member"} to `PyVectorcall_Call`{.interpreted-text role="c:func"}. This bears repeating:

:::: warning
::: title
Warning
:::

A class supporting vectorcall **must** also implement `~PyTypeObject.tp_call`{.interpreted-text role="c:member"} with the same semantics.
::::

::: versionchanged
3.12

The `Py_TPFLAGS_HAVE_VECTORCALL`{.interpreted-text role="c:macro"} flag is now removed from a class when the class\'s `~object.__call__`{.interpreted-text role="py:meth"} method is reassigned. (This internally sets `~PyTypeObject.tp_call`{.interpreted-text role="c:member"} only, and thus may make it behave differently than the vectorcall function.) In earlier Python versions, vectorcall should only be used with `immutable <Py_TPFLAGS_IMMUTABLETYPE>`{.interpreted-text role="c:macro"} or static types.
:::

A class should not implement vectorcall if that would be slower than *tp_call*. For example, if the callee needs to convert the arguments to an args tuple and kwargs dict anyway, then there is no point in implementing vectorcall.

Classes can implement the vectorcall protocol by enabling the `Py_TPFLAGS_HAVE_VECTORCALL`{.interpreted-text role="c:macro"} flag and setting `~PyTypeObject.tp_vectorcall_offset`{.interpreted-text role="c:member"} to the offset inside the object structure where a *vectorcallfunc* appears. This is a pointer to a function with the following signature:

- *callable* is the object being called.

- 

  *args* is a C array consisting of the positional arguments followed by the

  :   values of the keyword arguments. This can be *NULL* if there are no arguments.

- 

  *nargsf* is the number of positional arguments plus possibly the

  :   `PY_VECTORCALL_ARGUMENTS_OFFSET`{.interpreted-text role="c:macro"} flag. To get the actual number of positional arguments from *nargsf*, use `PyVectorcall_NARGS`{.interpreted-text role="c:func"}.

- 

  *kwnames* is a tuple containing the names of the keyword arguments;

  :   in other words, the keys of the kwargs dict. These names must be strings (instances of `str` or a subclass) and they must be unique. If there are no keyword arguments, then *kwnames* can instead be *NULL*.

> If this flag is set in a vectorcall *nargsf* argument, the callee is allowed to temporarily change `args[-1]`. In other words, *args* points to argument 1 (not 0) in the allocated vector. The callee must restore the value of `args[-1]` before returning.
>
> For `PyObject_VectorcallMethod`{.interpreted-text role="c:func"}, this flag means instead that `args[0]` may be changed.
>
> Whenever they can do so cheaply (without additional allocation), callers are encouraged to use `PY_VECTORCALL_ARGUMENTS_OFFSET`{.interpreted-text role="c:macro"}. Doing so will allow callables such as bound methods to make their onward calls (which include a prepended *self* argument) very efficiently.
>
> ::: versionadded
> 3.8
> :::

To call an object that implements vectorcall, use a `call API <capi-call>`{.interpreted-text role="ref"} function as with any other callable. `PyObject_Vectorcall`{.interpreted-text role="c:func"} will usually be most efficient.

### Recursion Control

When using *tp_call*, callees do not need to worry about `recursion <recursion>`{.interpreted-text role="ref"}: CPython uses `Py_EnterRecursiveCall`{.interpreted-text role="c:func"} and `Py_LeaveRecursiveCall`{.interpreted-text role="c:func"} for calls made using *tp_call*.

For efficiency, this is not the case for calls done using vectorcall: the callee should use *Py_EnterRecursiveCall* and *Py_LeaveRecursiveCall* if needed.

### Vectorcall Support API

> Given a vectorcall *nargsf* argument, return the actual number of arguments. Currently equivalent to:
>
> ``` c
> (Py_ssize_t)(nargsf & ~PY_VECTORCALL_ARGUMENTS_OFFSET)
> ```
>
> However, the function `PyVectorcall_NARGS` should be used to allow for future extensions.
>
> ::: versionadded
> 3.8
> :::

> If *op* does not support the vectorcall protocol (either because the type does not or because the specific instance does not), return *NULL*. Otherwise, return the vectorcall function pointer stored in *op*. This function never raises an exception.
>
> This is mostly useful to check whether or not *op* supports vectorcall, which can be done by checking `PyVectorcall_Function(op) != NULL`.
>
> ::: versionadded
> 3.9
> :::

> Call *callable*\'s `vectorcallfunc`{.interpreted-text role="c:type"} with positional and keyword arguments given in a tuple and dict, respectively.
>
> This is a specialized function, intended to be put in the `~PyTypeObject.tp_call`{.interpreted-text role="c:member"} slot or be used in an implementation of `tp_call`. It does not check the `Py_TPFLAGS_HAVE_VECTORCALL`{.interpreted-text role="c:macro"} flag and it does not fall back to `tp_call`.
>
> ::: versionadded
> 3.8
> :::

## Object Calling API {#capi-call}

Various functions are available for calling a Python object. Each converts its arguments to a convention supported by the called object -- either *tp_call* or vectorcall. In order to do as little conversion as possible, pick one that best fits the format of data you have available.

The following table summarizes the available functions; please see individual documentation for details.

  --------------------------------------------------------------------------------------------------------------
  Function                                                          callable        args           kwargs
  ----------------------------------------------------------------- --------------- -------------- -------------
  `PyObject_Call`{.interpreted-text role="c:func"}                  `PyObject *`    tuple          dict/`NULL`

  `PyObject_CallNoArgs`{.interpreted-text role="c:func"}            `PyObject *`    \-\--          \-\--

  `PyObject_CallOneArg`{.interpreted-text role="c:func"}            `PyObject *`    1 object       \-\--

  `PyObject_CallObject`{.interpreted-text role="c:func"}            `PyObject *`    tuple/`NULL`   \-\--

  `PyObject_CallFunction`{.interpreted-text role="c:func"}          `PyObject *`    format         \-\--

  `PyObject_CallMethod`{.interpreted-text role="c:func"}            obj + `char*`   format         \-\--

  `PyObject_CallFunctionObjArgs`{.interpreted-text role="c:func"}   `PyObject *`    variadic       \-\--

  `PyObject_CallMethodObjArgs`{.interpreted-text role="c:func"}     obj + name      variadic       \-\--

  `PyObject_CallMethodNoArgs`{.interpreted-text role="c:func"}      obj + name      \-\--          \-\--

  `PyObject_CallMethodOneArg`{.interpreted-text role="c:func"}      obj + name      1 object       \-\--

  `PyObject_Vectorcall`{.interpreted-text role="c:func"}            `PyObject *`    vectorcall     vectorcall

  `PyObject_VectorcallDict`{.interpreted-text role="c:func"}        `PyObject *`    vectorcall     dict/`NULL`

  `PyObject_VectorcallMethod`{.interpreted-text role="c:func"}      arg + name      vectorcall     vectorcall
  --------------------------------------------------------------------------------------------------------------

> Call a callable Python object *callable*, with arguments given by the tuple *args*, and named arguments given by the dictionary *kwargs*.
>
> *args* must not be *NULL*; use an empty tuple if no arguments are needed. If no named arguments are needed, *kwargs* can be *NULL*.
>
> Return the result of the call on success, or raise an exception and return *NULL* on failure.
>
> This is the equivalent of the Python expression: `callable(*args, **kwargs)`.

> Call a callable Python object *callable* without any arguments. It is the most efficient way to call a callable Python object without any argument.
>
> Return the result of the call on success, or raise an exception and return *NULL* on failure.
>
> ::: versionadded
> 3.9
> :::

> Call a callable Python object *callable* with exactly 1 positional argument *arg* and no keyword arguments.
>
> Return the result of the call on success, or raise an exception and return *NULL* on failure.
>
> ::: versionadded
> 3.9
> :::

> Call a callable Python object *callable*, with arguments given by the tuple *args*. If no arguments are needed, then *args* can be *NULL*.
>
> Return the result of the call on success, or raise an exception and return *NULL* on failure.
>
> This is the equivalent of the Python expression: `callable(*args)`.

> Call a callable Python object *callable*, with a variable number of C arguments. The C arguments are described using a `Py_BuildValue`{.interpreted-text role="c:func"} style format string. The format can be *NULL*, indicating that no arguments are provided.
>
> Return the result of the call on success, or raise an exception and return *NULL* on failure.
>
> This is the equivalent of the Python expression: `callable(*args)`.
>
> Note that if you only pass `PyObject *`{.interpreted-text role="c:expr"} args, `PyObject_CallFunctionObjArgs`{.interpreted-text role="c:func"} is a faster alternative.
>
> ::: versionchanged
> 3.4 The type of *format* was changed from `char *`.
> :::

> Call the method named *name* of object *obj* with a variable number of C arguments. The C arguments are described by a `Py_BuildValue`{.interpreted-text role="c:func"} format string that should produce a tuple.
>
> The format can be *NULL*, indicating that no arguments are provided.
>
> Return the result of the call on success, or raise an exception and return *NULL* on failure.
>
> This is the equivalent of the Python expression: `obj.name(arg1, arg2, ...)`.
>
> Note that if you only pass `PyObject *`{.interpreted-text role="c:expr"} args, `PyObject_CallMethodObjArgs`{.interpreted-text role="c:func"} is a faster alternative.
>
> ::: versionchanged
> 3.4 The types of *name* and *format* were changed from `char *`.
> :::

> Call a callable Python object *callable*, with a variable number of `PyObject *`{.interpreted-text role="c:expr"} arguments. The arguments are provided as a variable number of parameters followed by *NULL*.
>
> Return the result of the call on success, or raise an exception and return *NULL* on failure.
>
> This is the equivalent of the Python expression: `callable(arg1, arg2, ...)`.

> Call a method of the Python object *obj*, where the name of the method is given as a Python string object in *name*. It is called with a variable number of `PyObject *`{.interpreted-text role="c:expr"} arguments. The arguments are provided as a variable number of parameters followed by *NULL*.
>
> Return the result of the call on success, or raise an exception and return *NULL* on failure.

> Call a method of the Python object *obj* without arguments, where the name of the method is given as a Python string object in *name*.
>
> Return the result of the call on success, or raise an exception and return *NULL* on failure.
>
> ::: versionadded
> 3.9
> :::

> Call a method of the Python object *obj* with a single positional argument *arg*, where the name of the method is given as a Python string object in *name*.
>
> Return the result of the call on success, or raise an exception and return *NULL* on failure.
>
> ::: versionadded
> 3.9
> :::

> Call a callable Python object *callable*. The arguments are the same as for `vectorcallfunc`{.interpreted-text role="c:type"}. If *callable* supports [vectorcall](#vectorcall), this directly calls the vectorcall function stored in *callable*.
>
> Return the result of the call on success, or raise an exception and return *NULL* on failure.
>
> ::: versionadded
> 3.8 as `_PyObject_Vectorcall`
> :::
>
> ::: versionchanged
> 3.9
>
> Renamed to the current name, without the leading underscore. The old provisional name is `soft deprecated`{.interpreted-text role="term"}.
> :::

> Call *callable* with positional arguments passed exactly as in the [vectorcall](#vectorcall) protocol, but with keyword arguments passed as a dictionary *kwdict*. The *args* array contains only the positional arguments.
>
> Regardless of which protocol is used internally, a conversion of arguments needs to be done. Therefore, this function should only be used if the caller already has a dictionary ready to use for the keyword arguments, but not a tuple for the positional arguments.
>
> ::: versionadded
> 3.9
> :::

> Call a method using the vectorcall calling convention. The name of the method is given as a Python string *name*. The object whose method is called is *args\[0\]*, and the *args* array starting at *args\[1\]* represents the arguments of the call. There must be at least one positional argument. *nargsf* is the number of positional arguments including *args\[0\]*, plus `PY_VECTORCALL_ARGUMENTS_OFFSET`{.interpreted-text role="c:macro"} if the value of `args[0]` may temporarily be changed. Keyword arguments can be passed just like in `PyObject_Vectorcall`{.interpreted-text role="c:func"}.
>
> If the object has the `Py_TPFLAGS_METHOD_DESCRIPTOR`{.interpreted-text role="c:macro"} feature, this will call the unbound method object with the full *args* vector as arguments.
>
> Return the result of the call on success, or raise an exception and return *NULL* on failure.
>
> ::: versionadded
> 3.9
> :::

## Call Support API

> Determine if the object *o* is callable. Return `1` if the object is callable and `0` otherwise. This function always succeeds.
