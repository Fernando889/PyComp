# Defining Extension Types: Assorted Topics {#new-types-topics}

::: {#dnt-type-methods}
This section aims to give a quick fly-by on the various type methods you can implement and what they do.
:::

Here is the definition of `PyTypeObject`{.interpreted-text role="c:type"}, with some fields only used in `debug builds <debug-build>`{.interpreted-text role="ref"} omitted:

::: literalinclude
../includes/typestruct.h
:::

Now that\'s a *lot* of methods. Don\'t worry too much though \-- if you have a type you want to define, the chances are very good that you will only implement a handful of these.

As you probably expect by now, we\'re going to go over this and give more information about the various handlers. We won\'t go in the order they are defined in the structure, because there is a lot of historical baggage that impacts the ordering of the fields. It\'s often easiest to find an example that includes the fields you need and then change the values to suit your new type. :

``` c
const char *tp_name; /* For printing */
```

The name of the type \-- as mentioned in the previous chapter, this will appear in various places, almost entirely for diagnostic purposes. Try to choose something that will be helpful in such a situation! :

``` c
Py_ssize_t tp_basicsize, tp_itemsize; /* For allocation */
```

These fields tell the runtime how much memory to allocate when new objects of this type are created. Python has some built-in support for variable length structures (think: strings, tuples) which is where the `~PyTypeObject.tp_itemsize`{.interpreted-text role="c:member"} field comes in. This will be dealt with later. :

``` c
const char *tp_doc;
```

Here you can put a string (or its address) that you want returned when the Python script references `obj.__doc__` to retrieve the doc string.

Now we come to the basic type methods \-- the ones most extension types will implement.

## Finalization and De-allocation

::: index
single: object; deallocation single: deallocation, object single: object; finalization single: finalization, of objects
:::

``` c
destructor tp_dealloc;
```

This function is called when the reference count of the instance of your type is reduced to zero and the Python interpreter wants to reclaim it. If your type has memory to free or other clean-up to perform, you can put it here. The object itself needs to be freed here as well. Here is an example of this function:

``` c
static void
newdatatype_dealloc(PyObject *op)
{
    newdatatypeobject *self = (newdatatypeobject *) op;
    free(self->obj_UnderlyingDatatypePtr);
    Py_TYPE(self)->tp_free(self);
}
```

If your type supports garbage collection, the destructor should call `PyObject_GC_UnTrack`{.interpreted-text role="c:func"} before clearing any member fields:

``` c
static void
newdatatype_dealloc(PyObject *op)
{
    newdatatypeobject *self = (newdatatypeobject *) op;
    PyObject_GC_UnTrack(op);
    Py_CLEAR(self->other_obj);
    ...
    Py_TYPE(self)->tp_free(self);
}
```

::: index
single: PyErr_Fetch (C function) single: PyErr_Restore (C function)
:::

One important requirement of the deallocator function is that it leaves any pending exceptions alone. This is important since deallocators are frequently called as the interpreter unwinds the Python stack; when the stack is unwound due to an exception (rather than normal returns), nothing is done to protect the deallocators from seeing that an exception has already been set. Any actions which a deallocator performs which may cause additional Python code to be executed may detect that an exception has been set. This can lead to misleading errors from the interpreter. The proper way to protect against this is to save a pending exception before performing the unsafe action, and restoring it when done. This can be done using the `PyErr_Fetch`{.interpreted-text role="c:func"} and `PyErr_Restore`{.interpreted-text role="c:func"} functions:

``` c
static void
my_dealloc(PyObject *obj)
{
    MyObject *self = (MyObject *) obj;
    PyObject *cbresult;

    if (self->my_callback != NULL) {
        PyObject *err_type, *err_value, *err_traceback;

        /* This saves the current exception state */
        PyErr_Fetch(&err_type, &err_value, &err_traceback);

        cbresult = PyObject_CallNoArgs(self->my_callback);
        if (cbresult == NULL) {
           PyErr_WriteUnraisable(self->my_callback);
        }
        else {
            Py_DECREF(cbresult);
        }

        /* This restores the saved exception state */
        PyErr_Restore(err_type, err_value, err_traceback);

        Py_DECREF(self->my_callback);
    }
    Py_TYPE(self)->tp_free(self);
}
```

::::: note
::: title
Note
:::

There are limitations to what you can safely do in a deallocator function. First, if your type supports garbage collection (using `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} and/or `~PyTypeObject.tp_clear`{.interpreted-text role="c:member"}), some of the object\'s members can have been cleared or finalized by the time `~PyTypeObject.tp_dealloc`{.interpreted-text role="c:member"} is called. Second, in `~PyTypeObject.tp_dealloc`{.interpreted-text role="c:member"}, your object is in an unstable state: its reference count is equal to zero. Any call to a non-trivial object or API (as in the example above) might end up calling `~PyTypeObject.tp_dealloc`{.interpreted-text role="c:member"} again, causing a double free and a crash.

Starting with Python 3.4, it is recommended not to put any complex finalization code in `~PyTypeObject.tp_dealloc`{.interpreted-text role="c:member"}, and instead use the new `~PyTypeObject.tp_finalize`{.interpreted-text role="c:member"} type method.

::: seealso
`442`{.interpreted-text role="pep"} explains the new finalization scheme.
:::
:::::

::: index
single: string; object representation pair: built-in function; repr
:::

## Object Presentation

In Python, there are two ways to generate a textual representation of an object: the `repr`{.interpreted-text role="func"} function, and the `str`{.interpreted-text role="func"} function. (The `print`{.interpreted-text role="func"} function just calls `str`{.interpreted-text role="func"}.) These handlers are both optional.

``` c
reprfunc tp_repr;
reprfunc tp_str;
```

The `~PyTypeObject.tp_repr`{.interpreted-text role="c:member"} handler should return a string object containing a representation of the instance for which it is called. Here is a simple example:

``` c
static PyObject *
newdatatype_repr(PyObject *op)
{
    newdatatypeobject *self = (newdatatypeobject *) op;
    return PyUnicode_FromFormat("Repr-ified_newdatatype{{size:%d}}",
                                self->obj_UnderlyingDatatypePtr->size);
}
```

If no `~PyTypeObject.tp_repr`{.interpreted-text role="c:member"} handler is specified, the interpreter will supply a representation that uses the type\'s `~PyTypeObject.tp_name`{.interpreted-text role="c:member"} and a uniquely identifying value for the object.

The `~PyTypeObject.tp_str`{.interpreted-text role="c:member"} handler is to `str`{.interpreted-text role="func"} what the `~PyTypeObject.tp_repr`{.interpreted-text role="c:member"} handler described above is to `repr`{.interpreted-text role="func"}; that is, it is called when Python code calls `str`{.interpreted-text role="func"} on an instance of your object. Its implementation is very similar to the `~PyTypeObject.tp_repr`{.interpreted-text role="c:member"} function, but the resulting string is intended for human consumption. If `~PyTypeObject.tp_str`{.interpreted-text role="c:member"} is not specified, the `~PyTypeObject.tp_repr`{.interpreted-text role="c:member"} handler is used instead.

Here is a simple example:

``` c
static PyObject *
newdatatype_str(PyObject *op)
{
    newdatatypeobject *self = (newdatatypeobject *) op;
    return PyUnicode_FromFormat("Stringified_newdatatype{{size:%d}}",
                                self->obj_UnderlyingDatatypePtr->size);
}
```

## Attribute Management

For every object which can support attributes, the corresponding type must provide the functions that control how the attributes are resolved. There needs to be a function which can retrieve attributes (if any are defined), and another to set attributes (if setting attributes is allowed). Removing an attribute is a special case, for which the new value passed to the handler is `NULL`.

Python supports two pairs of attribute handlers; a type that supports attributes only needs to implement the functions for one pair. The difference is that one pair takes the name of the attribute as a `char\*`{.interpreted-text role="c:expr"}, while the other accepts a `PyObject*`{.interpreted-text role="c:expr"}. Each type can use whichever pair makes more sense for the implementation\'s convenience. :

``` c
getattrfunc  tp_getattr;        /* char * version */
setattrfunc  tp_setattr;
/* ... */
getattrofunc tp_getattro;       /* PyObject * version */
setattrofunc tp_setattro;
```

If accessing attributes of an object is always a simple operation (this will be explained shortly), there are generic implementations which can be used to provide the `PyObject*`{.interpreted-text role="c:expr"} version of the attribute management functions. The actual need for type-specific attribute handlers almost completely disappeared starting with Python 2.2, though there are many examples which have not been updated to use some of the new generic mechanism that is available.

### Generic Attribute Management

Most extension types only use *simple* attributes. So, what makes the attributes simple? There are only a couple of conditions that must be met:

1.  The name of the attributes must be known when `PyType_Ready`{.interpreted-text role="c:func"} is called.
2.  No special processing is needed to record that an attribute was looked up or set, nor do actions need to be taken based on the value.

Note that this list does not place any restrictions on the values of the attributes, when the values are computed, or how relevant data is stored.

When `PyType_Ready`{.interpreted-text role="c:func"} is called, it uses three tables referenced by the type object to create `descriptor`{.interpreted-text role="term"}s which are placed in the dictionary of the type object. Each descriptor controls access to one attribute of the instance object. Each of the tables is optional; if all three are `NULL`, instances of the type will only have attributes that are inherited from their base type, and should leave the `~PyTypeObject.tp_getattro`{.interpreted-text role="c:member"} and `~PyTypeObject.tp_setattro`{.interpreted-text role="c:member"} fields `NULL` as well, allowing the base type to handle attributes.

The tables are declared as three fields of the type object:

``` c
struct PyMethodDef *tp_methods;
struct PyMemberDef *tp_members;
struct PyGetSetDef *tp_getset;
```

If `~PyTypeObject.tp_methods`{.interpreted-text role="c:member"} is not `NULL`, it must refer to an array of `PyMethodDef`{.interpreted-text role="c:type"} structures. Each entry in the table is an instance of this structure:

``` c
typedef struct PyMethodDef {
    const char  *ml_name;       /* method name */
    PyCFunction  ml_meth;       /* implementation function */
    int          ml_flags;      /* flags */
    const char  *ml_doc;        /* docstring */
} PyMethodDef;
```

One entry should be defined for each method provided by the type; no entries are needed for methods inherited from a base type. One additional entry is needed at the end; it is a sentinel that marks the end of the array. The `~PyMethodDef.ml_name`{.interpreted-text role="c:member"} field of the sentinel must be `NULL`.

The second table is used to define attributes which map directly to data stored in the instance. A variety of primitive C types are supported, and access may be read-only or read-write. The structures in the table are defined as:

``` c
typedef struct PyMemberDef {
    const char *name;
    int         type;
    int         offset;
    int         flags;
    const char *doc;
} PyMemberDef;
```

For each entry in the table, a `descriptor`{.interpreted-text role="term"} will be constructed and added to the type which will be able to extract a value from the instance structure. The `~PyMemberDef.type`{.interpreted-text role="c:member"} field should contain a type code like `Py_T_INT`{.interpreted-text role="c:macro"} or `Py_T_DOUBLE`{.interpreted-text role="c:macro"}; the value will be used to determine how to convert Python values to and from C values. The `~PyMemberDef.flags`{.interpreted-text role="c:member"} field is used to store flags which control how the attribute can be accessed: you can set it to `Py_READONLY`{.interpreted-text role="c:macro"} to prevent Python code from setting it.

An interesting advantage of using the `~PyTypeObject.tp_members`{.interpreted-text role="c:member"} table to build descriptors that are used at runtime is that any attribute defined this way can have an associated doc string simply by providing the text in the table. An application can use the introspection API to retrieve the descriptor from the class object, and get the doc string using its `~type.__doc__`{.interpreted-text role="attr"} attribute.

As with the `~PyTypeObject.tp_methods`{.interpreted-text role="c:member"} table, a sentinel entry with a `~PyMethodDef.ml_name`{.interpreted-text role="c:member"} value of `NULL` is required.

> Descriptor objects have two handler functions which correspond to the member{tp_getattro} and member{tp_setattro} handlers. The method{\_\_get\_\_()} handler is a function which is passed the descriptor, instance, and type objects, and returns the value of the attribute, or it returns NULL{} and sets an exception. The method{\_\_set\_\_()} handler is passed the descriptor, instance, type, and new value;

### Type-specific Attribute Management

For simplicity, only the `char\*`{.interpreted-text role="c:expr"} version will be demonstrated here; the type of the name parameter is the only difference between the `char\*`{.interpreted-text role="c:expr"} and `PyObject*`{.interpreted-text role="c:expr"} flavors of the interface. This example effectively does the same thing as the generic example above, but does not use the generic support added in Python 2.2. It explains how the handler functions are called, so that if you do need to extend their functionality, you\'ll understand what needs to be done.

The `~PyTypeObject.tp_getattr`{.interpreted-text role="c:member"} handler is called when the object requires an attribute look-up. It is called in the same situations where the `~object.__getattr__`{.interpreted-text role="meth"} method of a class would be called.

Here is an example:

``` c
static PyObject *
newdatatype_getattr(PyObject *op, char *name)
{
    newdatatypeobject *self = (newdatatypeobject *) op;
    if (strcmp(name, "data") == 0) {
        return PyLong_FromLong(self->data);
    }

    PyErr_Format(PyExc_AttributeError,
                 "'%.100s' object has no attribute '%.400s'",
                 Py_TYPE(self)->tp_name, name);
    return NULL;
}
```

The `~PyTypeObject.tp_setattr`{.interpreted-text role="c:member"} handler is called when the `~object.__setattr__`{.interpreted-text role="meth"} or `~object.__delattr__`{.interpreted-text role="meth"} method of a class instance would be called. When an attribute should be deleted, the third parameter will be `NULL`. Here is an example that simply raises an exception; if this were really all you wanted, the `~PyTypeObject.tp_setattr`{.interpreted-text role="c:member"} handler should be set to `NULL`. :

``` c
static int
newdatatype_setattr(PyObject *op, char *name, PyObject *v)
{
    PyErr_Format(PyExc_RuntimeError, "Read-only attribute: %s", name);
    return -1;
}
```

## Object Comparison

``` c
richcmpfunc tp_richcompare;
```

The `~PyTypeObject.tp_richcompare`{.interpreted-text role="c:member"} handler is called when comparisons are needed. It is analogous to the `rich comparison methods <richcmpfuncs>`{.interpreted-text role="ref"}, like `!__lt__`{.interpreted-text role="meth"}, and also called by `PyObject_RichCompare`{.interpreted-text role="c:func"} and `PyObject_RichCompareBool`{.interpreted-text role="c:func"}.

This function is called with two Python objects and the operator as arguments, where the operator is one of `Py_EQ`, `Py_NE`, `Py_LE`, `Py_GE`, `Py_LT` or `Py_GT`. It should compare the two objects with respect to the specified operator and return `Py_True` or `Py_False` if the comparison is successful, `Py_NotImplemented` to indicate that comparison is not implemented and the other object\'s comparison method should be tried, or `NULL` if an exception was set.

Here is a sample implementation, for a datatype that is considered equal if the size of an internal pointer is equal:

``` c
static PyObject *
newdatatype_richcmp(PyObject *lhs, PyObject *rhs, int op)
{
    newdatatypeobject *obj1 = (newdatatypeobject *) lhs;
    newdatatypeobject *obj2 = (newdatatypeobject *) rhs;
    PyObject *result;
    int c, size1, size2;

    /* code to make sure that both arguments are of type
       newdatatype omitted */

    size1 = obj1->obj_UnderlyingDatatypePtr->size;
    size2 = obj2->obj_UnderlyingDatatypePtr->size;

    switch (op) {
    case Py_LT: c = size1 <  size2; break;
    case Py_LE: c = size1 <= size2; break;
    case Py_EQ: c = size1 == size2; break;
    case Py_NE: c = size1 != size2; break;
    case Py_GT: c = size1 >  size2; break;
    case Py_GE: c = size1 >= size2; break;
    }
    result = c ? Py_True : Py_False;
    return Py_NewRef(result);
 }
```

## Abstract Protocol Support

Python supports a variety of *abstract* \'protocols;\' the specific interfaces provided to use these interfaces are documented in `abstract`{.interpreted-text role="ref"}.

A number of these abstract interfaces were defined early in the development of the Python implementation. In particular, the number, mapping, and sequence protocols have been part of Python since the beginning. Other protocols have been added over time. For protocols which depend on several handler routines from the type implementation, the older protocols have been defined as optional blocks of handlers referenced by the type object. For newer protocols there are additional slots in the main type object, with a flag bit being set to indicate that the slots are present and should be checked by the interpreter. (The flag bit does not indicate that the slot values are non-`NULL`. The flag may be set to indicate the presence of a slot, but a slot may still be unfilled.) :

``` c
PyNumberMethods   *tp_as_number;
PySequenceMethods *tp_as_sequence;
PyMappingMethods  *tp_as_mapping;
```

If you wish your object to be able to act like a number, a sequence, or a mapping object, then you place the address of a structure that implements the C type `PyNumberMethods`{.interpreted-text role="c:type"}, `PySequenceMethods`{.interpreted-text role="c:type"}, or `PyMappingMethods`{.interpreted-text role="c:type"}, respectively. It is up to you to fill in this structure with appropriate values. You can find examples of the use of each of these in the `Objects`{.interpreted-text role="file"} directory of the Python source distribution. :

``` c
hashfunc tp_hash;
```

This function, if you choose to provide it, should return a hash number for an instance of your data type. Here is a simple example:

``` c
static Py_hash_t
newdatatype_hash(PyObject *op)
{
    newdatatypeobject *self = (newdatatypeobject *) op;
    Py_hash_t result;
    result = self->some_size + 32767 * self->some_number;
    if (result == -1) {
        result = -2;
    }
    return result;
}
```

`Py_hash_t`{.interpreted-text role="c:type"} is a signed integer type with a platform-varying width. Returning `-1` from `~PyTypeObject.tp_hash`{.interpreted-text role="c:member"} indicates an error, which is why you should be careful to avoid returning it when hash computation is successful, as seen above.

``` c
ternaryfunc tp_call;
```

This function is called when an instance of your data type is \"called\", for example, if `obj1` is an instance of your data type and the Python script contains `obj1('hello')`, the `~PyTypeObject.tp_call`{.interpreted-text role="c:member"} handler is invoked.

This function takes three arguments:

1.  *self* is the instance of the data type which is the subject of the call. If the call is `obj1('hello')`, then *self* is `obj1`.
2.  *args* is a tuple containing the arguments to the call. You can use `PyArg_ParseTuple`{.interpreted-text role="c:func"} to extract the arguments.
3.  *kwds* is a dictionary of keyword arguments that were passed. If this is non-`NULL` and you support keyword arguments, use `PyArg_ParseTupleAndKeywords`{.interpreted-text role="c:func"} to extract the arguments. If you do not want to support keyword arguments and this is non-`NULL`, raise a `TypeError`{.interpreted-text role="exc"} with a message saying that keyword arguments are not supported.

Here is a toy `tp_call` implementation:

``` c
static PyObject *
newdatatype_call(PyObject *op, PyObject *args, PyObject *kwds)
{
    newdatatypeobject *self = (newdatatypeobject *) op;
    PyObject *result;
    const char *arg1;
    const char *arg2;
    const char *arg3;

    if (!PyArg_ParseTuple(args, "sss:call", &arg1, &arg2, &arg3)) {
        return NULL;
    }
    result = PyUnicode_FromFormat(
        "Returning -- value: [%d] arg1: [%s] arg2: [%s] arg3: [%s]\n",
        self->obj_UnderlyingDatatypePtr->size,
        arg1, arg2, arg3);
    return result;
}
```

``` c
/* Iterators */
getiterfunc tp_iter;
iternextfunc tp_iternext;
```

These functions provide support for the iterator protocol. Both handlers take exactly one parameter, the instance for which they are being called, and return a new reference. In the case of an error, they should set an exception and return `NULL`. `~PyTypeObject.tp_iter`{.interpreted-text role="c:member"} corresponds to the Python `~object.__iter__`{.interpreted-text role="meth"} method, while `~PyTypeObject.tp_iternext`{.interpreted-text role="c:member"} corresponds to the Python `~iterator.__next__`{.interpreted-text role="meth"} method.

Any `iterable`{.interpreted-text role="term"} object must implement the `~PyTypeObject.tp_iter`{.interpreted-text role="c:member"} handler, which must return an `iterator`{.interpreted-text role="term"} object. Here the same guidelines apply as for Python classes:

- For collections (such as lists and tuples) which can support multiple independent iterators, a new iterator should be created and returned by each call to `~PyTypeObject.tp_iter`{.interpreted-text role="c:member"}.
- Objects which can only be iterated over once (usually due to side effects of iteration, such as file objects) can implement `~PyTypeObject.tp_iter`{.interpreted-text role="c:member"} by returning a new reference to themselves \-- and should also therefore implement the `~PyTypeObject.tp_iternext`{.interpreted-text role="c:member"} handler.

Any `iterator`{.interpreted-text role="term"} object should implement both `~PyTypeObject.tp_iter`{.interpreted-text role="c:member"} and `~PyTypeObject.tp_iternext`{.interpreted-text role="c:member"}. An iterator\'s `~PyTypeObject.tp_iter`{.interpreted-text role="c:member"} handler should return a new reference to the iterator. Its `~PyTypeObject.tp_iternext`{.interpreted-text role="c:member"} handler should return a new reference to the next object in the iteration, if there is one. If the iteration has reached the end, `~PyTypeObject.tp_iternext`{.interpreted-text role="c:member"} may return `NULL` without setting an exception, or it may set `StopIteration`{.interpreted-text role="exc"} *in addition* to returning `NULL`; avoiding the exception can yield slightly better performance. If an actual error occurs, `~PyTypeObject.tp_iternext`{.interpreted-text role="c:member"} should always set an exception and return `NULL`.

## Weak Reference Support {#weakref-support}

One of the goals of Python\'s weak reference implementation is to allow any type to participate in the weak reference mechanism without incurring the overhead on performance-critical objects (such as numbers).

::: seealso
Documentation for the `weakref`{.interpreted-text role="mod"} module.
:::

For an object to be weakly referenceable, the extension type must set the `Py_TPFLAGS_MANAGED_WEAKREF` bit of the `~PyTypeObject.tp_flags`{.interpreted-text role="c:member"} field. The legacy `~PyTypeObject.tp_weaklistoffset`{.interpreted-text role="c:member"} field should be left as zero.

If this flag is set, `Py_TPFLAGS_HAVE_GC`{.interpreted-text role="c:macro"} should also be set.

Concretely, here is how the statically declared type object would look:

``` c
static PyTypeObject TrivialType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    /* ... other members omitted for brevity ... */
    .tp_flags = Py_TPFLAGS_MANAGED_WEAKREF | ...,
};
```

The only further addition is that `tp_dealloc` needs to clear any weak references (by calling `PyObject_ClearWeakRefs`{.interpreted-text role="c:func"}):

``` c
static void
Trivial_dealloc(PyObject *op)
{
    /* Clear weakrefs first before calling any destructors */
    PyObject_ClearWeakRefs(op);
    /* ... remainder of destruction code omitted for brevity ... */
    Py_TYPE(op)->tp_free(op);
}
```

## More Suggestions

In order to learn how to implement any specific method for your new data type, get the `CPython`{.interpreted-text role="term"} source code. Go to the `Objects`{.interpreted-text role="file"} directory, then search the C source files for `tp_` plus the function you want (for example, `tp_richcompare`). You will find examples of the function you want to implement.

When you need to verify that an object is a concrete instance of the type you are implementing, use the `PyObject_TypeCheck`{.interpreted-text role="c:func"} function. A sample of its use might be something like the following:

``` c
if (!PyObject_TypeCheck(some_object, &MyType)) {
    PyErr_SetString(PyExc_TypeError, "arg #1 not a mything");
    return NULL;
}
```

::: seealso
Download CPython source releases. <https://www.python.org/downloads/source/>

The CPython project on GitHub, where the CPython source code is developed.

:   <https://github.com/python/cpython>
:::
