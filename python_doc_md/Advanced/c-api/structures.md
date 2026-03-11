# Common Object Structures {#common-structs}

There are a large number of structures which are used in the definition of object types for Python. This section describes these structures and how they are used.

## Base object types and macros

All Python objects ultimately share a small number of fields at the beginning of the object\'s representation in memory. These are represented by the `PyObject`{.interpreted-text role="c:type"} and `PyVarObject`{.interpreted-text role="c:type"} types, which are defined, in turn, by the expansions of some macros also used, whether directly or indirectly, in the definition of all other Python objects. Additional macros can be found under `reference counting <countingrefs>`{.interpreted-text role="ref"}.

> All object types are extensions of this type. This is a type which contains the information Python needs to treat a pointer to an object as an object. In a normal \"release\" build, it contains only the object\'s reference count and a pointer to the corresponding type object. Nothing is actually declared to be a `PyObject`{.interpreted-text role="c:type"}, but every pointer to a Python object can be cast to a `PyObject*`{.interpreted-text role="c:expr"}.
>
> The members must not be accessed directly; instead use macros such as `Py_REFCNT`{.interpreted-text role="c:macro"} and `Py_TYPE`{.interpreted-text role="c:macro"}.
>
> > The object\'s reference count, as returned by `Py_REFCNT`{.interpreted-text role="c:macro"}. Do not use this field directly; instead use functions and macros such as `!Py_REFCNT`{.interpreted-text role="c:macro"}, `Py_INCREF`{.interpreted-text role="c:func"} and `Py_DecRef`{.interpreted-text role="c:func"}.
> >
> > The field type may be different from `Py_ssize_t`, depending on build configuration and platform.
>
> > The object\'s type. Do not use this field directly; use `Py_TYPE`{.interpreted-text role="c:macro"} and `Py_SET_TYPE`{.interpreted-text role="c:func"} instead.

> An extension of `PyObject`{.interpreted-text role="c:type"} that adds the `~PyVarObject.ob_size`{.interpreted-text role="c:member"} field. This is intended for objects that have some notion of *length*.
>
> As with `!PyObject`{.interpreted-text role="c:type"}, the members must not be accessed directly; instead use macros such as `Py_SIZE`{.interpreted-text role="c:macro"}, `Py_REFCNT`{.interpreted-text role="c:macro"} and `Py_TYPE`{.interpreted-text role="c:macro"}.
>
> > A size field, whose contents should be considered an object\'s internal implementation detail.
> >
> > Do not use this field directly; use `Py_SIZE`{.interpreted-text role="c:macro"} instead.
> >
> > Object creation functions such as `PyObject_NewVar`{.interpreted-text role="c:func"} will generally set this field to the requested size (number of items). After creation, arbitrary values can be stored in `!ob_size`{.interpreted-text role="c:member"} using `Py_SET_SIZE`{.interpreted-text role="c:macro"}.
> >
> > To get an object\'s publicly exposed length, as returned by the Python function `len`{.interpreted-text role="py:func"}, use `PyObject_Length`{.interpreted-text role="c:func"} instead.

> This is a macro used when declaring new types which represent objects without a varying length. The PyObject_HEAD macro expands to:
>
> ``` c
> PyObject ob_base;
> ```
>
> See documentation of `PyObject`{.interpreted-text role="c:type"} above.

> This is a macro used when declaring new types which represent objects with a length that varies from instance to instance. The PyObject_VAR_HEAD macro expands to:
>
> ``` c
> PyVarObject ob_base;
> ```
>
> See documentation of `PyVarObject`{.interpreted-text role="c:type"} above.

> The base class of all other objects, the same as `object`{.interpreted-text role="class"} in Python.

> Test if the *x* object is the *y* object, the same as `x is y` in Python.
>
> ::: versionadded
> 3.10
> :::

> Test if an object is the `None` singleton, the same as `x is None` in Python.
>
> ::: versionadded
> 3.10
> :::

> Test if an object is the `True` singleton, the same as `x is True` in Python.
>
> ::: versionadded
> 3.10
> :::

> Test if an object is the `False` singleton, the same as `x is False` in Python.
>
> ::: versionadded
> 3.10
> :::

> Get the type of the Python object *o*.
>
> The returned reference is `borrowed <borrowed reference>`{.interpreted-text role="term"} from *o*. Do not release it with `Py_DECREF`{.interpreted-text role="c:func"} or similar.
>
> ::: versionchanged
> 3.11 `Py_TYPE()`{.interpreted-text role="c:func"} is changed to an inline static function. The parameter type is no longer `const PyObject*`{.interpreted-text role="c:expr"}.
> :::

> Return non-zero if the object *o* type is *type*. Return zero otherwise. Equivalent to: `Py_TYPE(o) == type`.
>
> ::: versionadded
> 3.9
> :::

> Set the type of object *o* to *type*, without any checking or reference counting.
>
> This is a very low-level operation. Consider instead setting the Python attribute `~object.__class__`{.interpreted-text role="attr"} using `PyObject_SetAttrString`{.interpreted-text role="c:func"} or similar.
>
> Note that assigning an incompatible type can lead to undefined behavior.
>
> If *type* is a `heap type <heap-types>`{.interpreted-text role="ref"}, the caller must create a new reference to it. Similarly, if the old type of *o* is a heap type, the caller must release a reference to that type.
>
> ::: versionadded
> 3.9
> :::

> Get the `~PyVarObject.ob_size`{.interpreted-text role="c:member"} field of *o*.
>
> ::: versionchanged
> 3.11 `Py_SIZE()`{.interpreted-text role="c:func"} is changed to an inline static function. The parameter type is no longer `const PyVarObject*`{.interpreted-text role="c:expr"}.
> :::

> Set the `~PyVarObject.ob_size`{.interpreted-text role="c:member"} field of *o* to *size*.
>
> ::: versionadded
> 3.9
> :::

> This is a macro which expands to initialization values for a new `PyObject`{.interpreted-text role="c:type"} type. This macro expands to:
>
> ``` c
> _PyObject_EXTRA_INIT
> 1, type,
> ```

> This is a macro which expands to initialization values for a new `PyVarObject`{.interpreted-text role="c:type"} type, including the `~PyVarObject.ob_size`{.interpreted-text role="c:member"} field. This macro expands to:
>
> ``` c
> _PyObject_EXTRA_INIT
> 1, type, size,
> ```

## Implementing functions and methods

> Type of the functions used to implement most Python callables in C. Functions of this type take two `PyObject*`{.interpreted-text role="c:expr"} parameters and return one such value. If the return value is `NULL`, an exception shall have been set. If not `NULL`, the return value is interpreted as the return value of the function as exposed in Python. The function must return a new reference.
>
> The function signature is:
>
> ``` c
> PyObject *PyCFunction(PyObject *self,
>                       PyObject *args);
> ```

> Type of the functions used to implement Python callables in C with signature `METH_VARARGS | METH_KEYWORDS <METH_VARARGS-METH_KEYWORDS>`{.interpreted-text role="ref"}. The function signature is:
>
> ``` c
> PyObject *PyCFunctionWithKeywords(PyObject *self,
>                                   PyObject *args,
>                                   PyObject *kwargs);
> ```

> Type of the functions used to implement Python callables in C with signature `METH_FASTCALL`{.interpreted-text role="c:macro"}. The function signature is:
>
> ``` c
> PyObject *PyCFunctionFast(PyObject *self,
>                           PyObject *const *args,
>                           Py_ssize_t nargs);
> ```

> Type of the functions used to implement Python callables in C with signature `METH_FASTCALL | METH_KEYWORDS <METH_FASTCALL-METH_KEYWORDS>`{.interpreted-text role="ref"}. The function signature is:
>
> ``` c
> PyObject *PyCFunctionFastWithKeywords(PyObject *self,
>                                       PyObject *const *args,
>                                       Py_ssize_t nargs,
>                                       PyObject *kwnames);
> ```

> Type of the functions used to implement Python callables in C with signature `METH_METHOD | METH_FASTCALL | METH_KEYWORDS <METH_METHOD-METH_FASTCALL-METH_KEYWORDS>`{.interpreted-text role="ref"}. The function signature is:
>
> ``` c
> PyObject *PyCMethod(PyObject *self,
>                     PyTypeObject *defining_class,
>                     PyObject *const *args,
>                     Py_ssize_t nargs,
>                     PyObject *kwnames)
> ```
>
> ::: versionadded
> 3.9
> :::

> Structure used to describe a method of an extension type. This structure has four fields:
>
> > Name of the method.
> >
> > A `NULL` *ml_name* marks the end of a `!PyMethodDef`{.interpreted-text role="c:type"} array.
>
> > Pointer to the C implementation.
>
> > Flags bits indicating how the call should be constructed.
>
> > Points to the contents of the docstring.

The `~PyMethodDef.ml_meth`{.interpreted-text role="c:member"} is a C function pointer. The functions may be of different types, but they always return `PyObject*`{.interpreted-text role="c:expr"}. If the function is not of the `PyCFunction`{.interpreted-text role="c:type"}, the compiler will require a cast in the method table. Even though `PyCFunction`{.interpreted-text role="c:type"} defines the first parameter as `PyObject*`{.interpreted-text role="c:expr"}, it is common that the method implementation uses the specific C type of the *self* object.

The `~PyMethodDef.ml_flags`{.interpreted-text role="c:member"} field is a bitfield which can include the following flags. The individual flags indicate either a calling convention or a binding convention.

There are these calling conventions:

> This is the typical calling convention, where the methods have the type `PyCFunction`{.interpreted-text role="c:type"}. The function expects two `PyObject*`{.interpreted-text role="c:expr"} values. The first one is the *self* object for methods; for module functions, it is the module object. The second parameter (often called *args*) is a tuple object representing all arguments. This parameter is typically processed using `PyArg_ParseTuple`{.interpreted-text role="c:func"} or `PyArg_UnpackTuple`{.interpreted-text role="c:func"}.

> Can only be used in certain combinations with other flags: `METH_VARARGS | METH_KEYWORDS <METH_VARARGS-METH_KEYWORDS>`{.interpreted-text role="ref"}, `METH_FASTCALL | METH_KEYWORDS <METH_FASTCALL-METH_KEYWORDS>`{.interpreted-text role="ref"} and `METH_METHOD | METH_FASTCALL | METH_KEYWORDS <METH_METHOD-METH_FASTCALL-METH_KEYWORDS>`{.interpreted-text role="ref"}.

::: {#METH_VARARGS-METH_KEYWORDS}

`METH_VARARGS | METH_KEYWORDS`{.interpreted-text role="c:expr"}

:   Methods with these flags must be of type `PyCFunctionWithKeywords`{.interpreted-text role="c:type"}. The function expects three parameters: *self*, *args*, *kwargs* where *kwargs* is a dictionary of all the keyword arguments or possibly `NULL` if there are no keyword arguments. The parameters are typically processed using `PyArg_ParseTupleAndKeywords`{.interpreted-text role="c:func"}.
:::

> Fast calling convention supporting only positional arguments. The methods have the type `PyCFunctionFast`{.interpreted-text role="c:type"}. The first parameter is *self*, the second parameter is a C array of `PyObject*`{.interpreted-text role="c:expr"} values indicating the arguments and the third parameter is the number of arguments (the length of the array).
>
> ::: versionadded
> 3.7
> :::
>
> ::: versionchanged
> 3.10
>
> `METH_FASTCALL` is now part of the `stable ABI <stable-abi>`{.interpreted-text role="ref"}.
> :::

::: {#METH_FASTCALL-METH_KEYWORDS}

`METH_FASTCALL | METH_KEYWORDS`{.interpreted-text role="c:expr"}

:   Extension of `METH_FASTCALL`{.interpreted-text role="c:macro"} supporting also keyword arguments, with methods of type `PyCFunctionFastWithKeywords`{.interpreted-text role="c:type"}. Keyword arguments are passed the same way as in the `vectorcall protocol <vectorcall>`{.interpreted-text role="ref"}: there is an additional fourth `PyObject*`{.interpreted-text role="c:expr"} parameter which is a tuple representing the names of the keyword arguments (which are guaranteed to be strings) or possibly `NULL` if there are no keywords. The values of the keyword arguments are stored in the *args* array, after the positional arguments.

    ::: versionadded
    3.7
    :::
:::

> Can only be used in the combination with other flags: `METH_METHOD | METH_FASTCALL | METH_KEYWORDS <METH_METHOD-METH_FASTCALL-METH_KEYWORDS>`{.interpreted-text role="ref"}.

::: {#METH_METHOD-METH_FASTCALL-METH_KEYWORDS}

`METH_METHOD | METH_FASTCALL | METH_KEYWORDS`{.interpreted-text role="c:expr"}

:   Extension of `METH_FASTCALL | METH_KEYWORDS <METH_FASTCALL-METH_KEYWORDS>`{.interpreted-text role="ref"} supporting the *defining class*, that is, the class that contains the method in question. The defining class might be a superclass of `Py_TYPE(self)`.

    The method needs to be of type `PyCMethod`{.interpreted-text role="c:type"}, the same as for `METH_FASTCALL | METH_KEYWORDS` with `defining_class` argument added after `self`.

    ::: versionadded
    3.9
    :::
:::

> Methods without parameters don\'t need to check whether arguments are given if they are listed with the `METH_NOARGS`{.interpreted-text role="c:macro"} flag. They need to be of type `PyCFunction`{.interpreted-text role="c:type"}. The first parameter is typically named *self* and will hold a reference to the module or object instance. In all cases the second parameter will be `NULL`.
>
> The function must have 2 parameters. Since the second parameter is unused, `Py_UNUSED`{.interpreted-text role="c:macro"} can be used to prevent a compiler warning.

> Methods with a single object argument can be listed with the `METH_O`{.interpreted-text role="c:macro"} flag, instead of invoking `PyArg_ParseTuple`{.interpreted-text role="c:func"} with a `"O"` argument. They have the type `PyCFunction`{.interpreted-text role="c:type"}, with the *self* parameter, and a `PyObject*`{.interpreted-text role="c:expr"} parameter representing the single argument.

These two constants are not used to indicate the calling convention but the binding when used with methods of classes. These may not be used for functions defined for modules. At most one of these flags may be set for any given method.

> ::: index
> pair: built-in function; classmethod
> :::
>
> The method will be passed the type object as the first parameter rather than an instance of the type. This is used to create *class methods*, similar to what is created when using the `classmethod`{.interpreted-text role="func"} built-in function.

> ::: index
> pair: built-in function; staticmethod
> :::
>
> The method will be passed `NULL` as the first parameter rather than an instance of the type. This is used to create *static methods*, similar to what is created when using the `staticmethod`{.interpreted-text role="func"} built-in function.

One other constant controls whether a method is loaded in place of another definition with the same method name.

> The method will be loaded in place of existing definitions. Without *METH_COEXIST*, the default is to skip repeated definitions. Since slot wrappers are loaded before the method table, the existence of a *sq_contains* slot, for example, would generate a wrapped method named `~object.__contains__`{.interpreted-text role="meth"} and preclude the loading of a corresponding PyCFunction with the same name. With the flag defined, the PyCFunction will be loaded in place of the wrapper object and will co-exist with the slot. This is helpful because calls to PyCFunctions are optimized more than wrapper object calls.

> The type object corresponding to Python C method objects. This is available as `types.BuiltinMethodType`{.interpreted-text role="class"} in the Python layer.

> Return true if *op* is an instance of the `PyCMethod_Type`{.interpreted-text role="c:type"} type or a subtype of it. This function always succeeds.

> This is the same as `PyCMethod_Check`{.interpreted-text role="c:func"}, but does not account for subtypes.

> Turn *ml* into a Python `callable`{.interpreted-text role="term"} object. The caller must ensure that *ml* outlives the `callable`{.interpreted-text role="term"}. Typically, *ml* is defined as a static variable.
>
> The *self* parameter will be passed as the *self* argument to the C function in `ml->ml_meth` when invoked. *self* can be `NULL`.
>
> The `callable`{.interpreted-text role="term"} object\'s `__module__` attribute can be set from the given *module* argument. *module* should be a Python string, which will be used as name of the module the function is defined in. If unavailable, it can be set to `None`{.interpreted-text role="const"} or `NULL`.
>
> ::: seealso
> `function.__module__`{.interpreted-text role="attr"}
> :::
>
> The *cls* parameter will be passed as the *defining_class* argument to the C function. Must be set if `METH_METHOD`{.interpreted-text role="c:macro"} is set on `ml->ml_flags`.
>
> ::: versionadded
> 3.9
> :::

> The type object corresponding to Python C function objects. This is available as `types.BuiltinFunctionType`{.interpreted-text role="class"} in the Python layer.

> Return true if *op* is an instance of the `PyCFunction_Type`{.interpreted-text role="c:type"} type or a subtype of it. This function always succeeds.

> This is the same as `PyCFunction_Check`{.interpreted-text role="c:func"}, but does not account for subtypes.

> Equivalent to `PyCMethod_New(ml, self, module, NULL)`.

> Equivalent to `PyCMethod_New(ml, self, NULL, NULL)`.

> Get the function\'s flags on *func* as they were passed to `~PyMethodDef.ml_flags`{.interpreted-text role="c:member"}.
>
> If *func* is not a C function object, this fails with an exception. *func* must not be `NULL`.
>
> This function returns the function\'s flags on success, and `-1` with an exception set on failure.

> This is the same as `PyCFunction_GetFlags`{.interpreted-text role="c:func"}, but without error or type checking.

> Get the function pointer on *func* as it was passed to `~PyMethodDef.ml_meth`{.interpreted-text role="c:member"}.
>
> If *func* is not a C function object, this fails with an exception. *func* must not be `NULL`.
>
> This function returns the function pointer on success, and `NULL` with an exception set on failure.

> This is the same as `PyCFunction_GetFunction`{.interpreted-text role="c:func"}, but without error or type checking.

> Get the \"self\" object on *func*. This is the object that would be passed to the first argument of a `PyCFunction`{.interpreted-text role="c:type"}. For C function objects created through a `PyMethodDef`{.interpreted-text role="c:type"} on a `PyModuleDef`{.interpreted-text role="c:type"}, this is the resulting module object.
>
> If *func* is not a C function object, this fails with an exception. *func* must not be `NULL`.
>
> This function returns a `borrowed reference`{.interpreted-text role="term"} to the \"self\" object on success, and `NULL` with an exception set on failure.

> This is the same as `PyCFunction_GetSelf`{.interpreted-text role="c:func"}, but without error or type checking.

## Accessing attributes of extension types

> Structure which describes an attribute of a type which corresponds to a C struct member. When defining a class, put a NULL-terminated array of these structures in the `~PyTypeObject.tp_members`{.interpreted-text role="c:member"} slot.
>
> Its fields are, in order:
>
> > Name of the member. A NULL value marks the end of a `PyMemberDef[]` array.
> >
> > The string should be static, no copy is made of it.
>
> > The type of the member in the C struct. See `PyMemberDef-types`{.interpreted-text role="ref"} for the possible values.
>
> > The offset in bytes that the member is located on the type's object struct.
>
> > Zero or more of the `PyMemberDef-flags`{.interpreted-text role="ref"}, combined using bitwise OR.
>
> > The docstring, or NULL. The string should be static, no copy is made of it. Typically, it is defined using `PyDoc_STR`{.interpreted-text role="c:macro"}.
>
> By default (when `~PyMemberDef.flags`{.interpreted-text role="c:member"} is `0`), members allow both read and write access. Use the `Py_READONLY`{.interpreted-text role="c:macro"} flag for read-only access. Certain types, like `Py_T_STRING`{.interpreted-text role="c:macro"}, imply `Py_READONLY`{.interpreted-text role="c:macro"}. Only `Py_T_OBJECT_EX`{.interpreted-text role="c:macro"} (and legacy `T_OBJECT`{.interpreted-text role="c:macro"}) members can be deleted.
>
> ::: {#pymemberdef-offsets}
> For heap-allocated types (created using `PyType_FromSpec`{.interpreted-text role="c:func"} or similar), `PyMemberDef` may contain a definition for the special member `"__vectorcalloffset__"`, corresponding to `~PyTypeObject.tp_vectorcall_offset`{.interpreted-text role="c:member"} in type objects. This member must be defined with `Py_T_PYSSIZET`, and either `Py_READONLY` or `Py_READONLY | Py_RELATIVE_OFFSET`. For example:
>
> ``` c
> static PyMemberDef spam_type_members[] = {
>     {"__vectorcalloffset__", Py_T_PYSSIZET,
>      offsetof(Spam_object, vectorcall), Py_READONLY},
>     {NULL}  /* Sentinel */
> };
> ```
> :::
>
> (You may need to `#include <stddef.h>` for `!offsetof`{.interpreted-text role="c:func"}.)
>
> The legacy offsets `~PyTypeObject.tp_dictoffset`{.interpreted-text role="c:member"} and `~PyTypeObject.tp_weaklistoffset`{.interpreted-text role="c:member"} can be defined similarly using `"__dictoffset__"` and `"__weaklistoffset__"` members, but extensions are strongly encouraged to use `Py_TPFLAGS_MANAGED_DICT`{.interpreted-text role="c:macro"} and `Py_TPFLAGS_MANAGED_WEAKREF`{.interpreted-text role="c:macro"} instead.
>
> ::: versionchanged
> 3.12
>
> `PyMemberDef` is always available. Previously, it required including `"structmember.h"`.
> :::
>
> ::: versionchanged
> 3.14
>
> `Py_RELATIVE_OFFSET`{.interpreted-text role="c:macro"} is now allowed for `"__vectorcalloffset__"`, `"__dictoffset__"` and `"__weaklistoffset__"`.
> :::

> Get an attribute belonging to the object at address *obj_addr*. The attribute is described by `PyMemberDef` *m*. Returns `NULL` on error.
>
> ::: versionchanged
> 3.12
>
> `PyMember_GetOne` is always available. Previously, it required including `"structmember.h"`.
> :::

> Set an attribute belonging to the object at address *obj_addr* to object *o*. The attribute to set is described by `PyMemberDef` *m*. Returns `0` if successful and a negative value on failure.
>
> ::: versionchanged
> 3.12
>
> `PyMember_SetOne` is always available. Previously, it required including `"structmember.h"`.
> :::

### Member flags {#PyMemberDef-flags}

The following flags can be used with `PyMemberDef.flags`{.interpreted-text role="c:member"}:

> Not writable.

> Emit an `object.__getattr__` `audit event <audit-events>`{.interpreted-text role="ref"} before reading.

> Indicates that the `~PyMemberDef.offset`{.interpreted-text role="c:member"} of this `PyMemberDef` entry indicates an offset from the subclass-specific data, rather than from `PyObject`.
>
> Can only be used as part of the `Py_tp_members`{.interpreted-text role="c:data"} `slot <PyType_Slot>`{.interpreted-text role="c:type"} when creating a class using negative `~PyType_Spec.basicsize`{.interpreted-text role="c:member"}. It is mandatory in that case. When setting `~PyTypeObject.tp_members`{.interpreted-text role="c:member"} from the slot during class creation, Python clears the flag and sets `PyMemberDef.offset`{.interpreted-text role="c:member"} to the offset from the `PyObject` struct.

::: index
single: READ_RESTRICTED (C macro) single: WRITE_RESTRICTED (C macro) single: RESTRICTED (C macro)
:::

::: versionchanged
3.10

The `!RESTRICTED`{.interpreted-text role="c:macro"}, `!READ_RESTRICTED`{.interpreted-text role="c:macro"} and `!WRITE_RESTRICTED`{.interpreted-text role="c:macro"} macros available with `#include "structmember.h"` are deprecated. `!READ_RESTRICTED`{.interpreted-text role="c:macro"} and `!RESTRICTED`{.interpreted-text role="c:macro"} are equivalent to `Py_AUDIT_READ`{.interpreted-text role="c:macro"}; `!WRITE_RESTRICTED`{.interpreted-text role="c:macro"} does nothing.
:::

::: index
single: READONLY (C macro)
:::

::: versionchanged
3.12

The `!READONLY`{.interpreted-text role="c:macro"} macro was renamed to `Py_READONLY`{.interpreted-text role="c:macro"}. The `!PY_AUDIT_READ`{.interpreted-text role="c:macro"} macro was renamed with the `Py_` prefix. The new names are now always available. Previously, these required `#include "structmember.h"`. The header is still available and it provides the old names.
:::

### Member types {#PyMemberDef-types}

`PyMemberDef.type`{.interpreted-text role="c:member"} can be one of the following macros corresponding to various C types. When the member is accessed in Python, it will be converted to the equivalent Python type. When it is set from Python, it will be converted back to the C type. If that is not possible, an exception such as `TypeError`{.interpreted-text role="exc"} or `ValueError`{.interpreted-text role="exc"} is raised.

Unless marked (D), attributes defined this way cannot be deleted using e.g. `del`{.interpreted-text role="keyword"} or `delattr`{.interpreted-text role="py:func"}.

  Macro name   C type                                                        Python type
  ------------ ------------------------------------------------------------- -------------------------------------------------
               `char`{.interpreted-text role="c:expr"}                       `int`{.interpreted-text role="py:class"}
               `short`{.interpreted-text role="c:expr"}                      `int`{.interpreted-text role="py:class"}
               `int`{.interpreted-text role="c:expr"}                        `int`{.interpreted-text role="py:class"}
               `long`{.interpreted-text role="c:expr"}                       `int`{.interpreted-text role="py:class"}
               `long long`{.interpreted-text role="c:expr"}                  `int`{.interpreted-text role="py:class"}
               `unsigned char`{.interpreted-text role="c:expr"}              `int`{.interpreted-text role="py:class"}
               `unsigned int`{.interpreted-text role="c:expr"}               `int`{.interpreted-text role="py:class"}
               `unsigned short`{.interpreted-text role="c:expr"}             `int`{.interpreted-text role="py:class"}
               `unsigned long`{.interpreted-text role="c:expr"}              `int`{.interpreted-text role="py:class"}
               `unsigned long long`{.interpreted-text role="c:expr"}         `int`{.interpreted-text role="py:class"}
               `Py_ssize_t`{.interpreted-text role="c:expr"}                 `int`{.interpreted-text role="py:class"}
               `float`{.interpreted-text role="c:expr"}                      `float`{.interpreted-text role="py:class"}
               `double`{.interpreted-text role="c:expr"}                     `float`{.interpreted-text role="py:class"}
               `char`{.interpreted-text role="c:expr"} (written as 0 or 1)   `bool`{.interpreted-text role="py:class"}
               `const char *`{.interpreted-text role="c:expr"} (\*)          `str`{.interpreted-text role="py:class"} (RO)
               `const char[]`{.interpreted-text role="c:expr"} (\*)          `str`{.interpreted-text role="py:class"} (RO)
               `char`{.interpreted-text role="c:expr"} (0-127)               `str`{.interpreted-text role="py:class"} (\*\*)
               `PyObject *`{.interpreted-text role="c:expr"}                 `object`{.interpreted-text role="py:class"} (D)

> (\*): Zero-terminated, UTF8-encoded C string. With `!Py_T_STRING`{.interpreted-text role="c:macro"} the C representation is a pointer; with `!Py_T_STRING_INPLACE`{.interpreted-text role="c:macro"} the string is stored directly in the structure.
>
> (\*\*): String of length 1. Only ASCII is accepted.
>
> (RO): Implies `Py_READONLY`{.interpreted-text role="c:macro"}.
>
> (D): Can be deleted, in which case the pointer is set to `NULL`. Reading a `NULL` pointer raises `AttributeError`{.interpreted-text role="py:exc"}.

::: index
single: T_BYTE (C macro) single: T_SHORT (C macro) single: T_INT (C macro) single: T_LONG (C macro) single: T_LONGLONG (C macro) single: T_UBYTE (C macro) single: T_USHORT (C macro) single: T_UINT (C macro) single: T_ULONG (C macro) single: T_ULONGULONG (C macro) single: T_PYSSIZET (C macro) single: T_FLOAT (C macro) single: T_DOUBLE (C macro) single: T_BOOL (C macro) single: T_CHAR (C macro) single: T_STRING (C macro) single: T_STRING_INPLACE (C macro) single: T_OBJECT_EX (C macro) single: structmember.h
:::

::: versionadded
3.12

In previous versions, the macros were only available with `#include "structmember.h"` and were named without the `Py_` prefix (e.g. as `T_INT`). The header is still available and contains the old names, along with the following deprecated types:

> Like `Py_T_OBJECT_EX`, but `NULL` is converted to `None`. This results in surprising behavior in Python: deleting the attribute effectively sets it to `None`.

> Always `None`. Must be used with `Py_READONLY`{.interpreted-text role="c:macro"}.
:::

### Defining Getters and Setters

> Structure to define property-like access for a type. See also description of the `PyTypeObject.tp_getset`{.interpreted-text role="c:member"} slot.
>
> > attribute name
>
> > C function to get the attribute.
>
> > Optional C function to set or delete the attribute. If `NULL`, the attribute is read-only.
>
> > optional docstring
>
> > Optional user data pointer, providing additional data for getter and setter.

> The `get` function takes one `PyObject*`{.interpreted-text role="c:expr"} parameter (the instance) and a user data pointer (the associated `closure`):
>
> It should return a new reference on success or `NULL` with a set exception on failure.

> `set` functions take two `PyObject*`{.interpreted-text role="c:expr"} parameters (the instance and the value to be set) and a user data pointer (the associated `closure`):
>
> In case the attribute should be deleted the second parameter is `NULL`. Should return `0` on success or `-1` with a set exception on failure.
