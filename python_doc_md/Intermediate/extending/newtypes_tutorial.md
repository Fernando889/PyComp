# Defining Extension Types: Tutorial {#defining-new-types}

Python allows the writer of a C extension module to define new types that can be manipulated from Python code, much like the built-in `str`{.interpreted-text role="class"} and `list`{.interpreted-text role="class"} types. The code for all extension types follows a pattern, but there are some details that you need to understand before you can get started. This document is a gentle introduction to the topic.

## The Basics {#dnt-basics}

The `CPython`{.interpreted-text role="term"} runtime sees all Python objects as variables of type `PyObject*`{.interpreted-text role="c:expr"}, which serves as a \"base type\" for all Python objects. The `PyObject`{.interpreted-text role="c:type"} structure itself only contains the object\'s `reference count`{.interpreted-text role="term"} and a pointer to the object\'s \"type object\". This is where the action is; the type object determines which (C) functions get called by the interpreter when, for instance, an attribute gets looked up on an object, a method called, or it is multiplied by another object. These C functions are called \"type methods\".

So, if you want to define a new extension type, you need to create a new type object.

This sort of thing can only be explained by example, so here\'s a minimal, but complete, module that defines a new type named `!Custom`{.interpreted-text role="class"} inside a C extension module `!custom`{.interpreted-text role="mod"}:

:::: note
::: title
Note
:::

What we\'re showing here is the traditional way of defining *static* extension types. It should be adequate for most uses. The C API also allows defining heap-allocated extension types using the `PyType_FromSpec`{.interpreted-text role="c:func"} function, which isn\'t covered in this tutorial.
::::

::: literalinclude
../includes/newtypes/custom.c
:::

Now that\'s quite a bit to take in at once, but hopefully bits will seem familiar from the previous chapter. This file defines three things:

1.  What a `!Custom`{.interpreted-text role="class"} **object** contains: this is the `CustomObject` struct, which is allocated once for each `!Custom`{.interpreted-text role="class"} instance.
2.  How the `!Custom`{.interpreted-text role="class"} **type** behaves: this is the `CustomType` struct, which defines a set of flags and function pointers that the interpreter inspects when specific operations are requested.
3.  How to define and execute the `!custom`{.interpreted-text role="mod"} module: this is the `PyInit_custom` function and the associated `custom_module` struct for defining the module, and the `custom_module_exec` function to set up a fresh module object.

The first bit is:

``` c
typedef struct {
    PyObject_HEAD
} CustomObject;
```

This is what a Custom object will contain. `PyObject_HEAD` is mandatory at the start of each object struct and defines a field called `ob_base` of type `PyObject`{.interpreted-text role="c:type"}, containing a pointer to a type object and a reference count (these can be accessed using the macros `Py_TYPE`{.interpreted-text role="c:macro"} and `Py_REFCNT`{.interpreted-text role="c:macro"} respectively). The reason for the macro is to abstract away the layout and to enable additional fields in `debug builds
<debug-build>`{.interpreted-text role="ref"}.

:::: note
::: title
Note
:::

There is no semicolon above after the `PyObject_HEAD`{.interpreted-text role="c:macro"} macro. Be wary of adding one by accident: some compilers will complain.
::::

Of course, objects generally store additional data besides the standard `PyObject_HEAD` boilerplate; for example, here is the definition for standard Python floats:

``` c
typedef struct {
    PyObject_HEAD
    double ob_fval;
} PyFloatObject;
```

The second bit is the definition of the type object. :

``` c
static PyTypeObject CustomType = {
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "custom.Custom",
    .tp_doc = PyDoc_STR("Custom objects"),
    .tp_basicsize = sizeof(CustomObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
};
```

:::: note
::: title
Note
:::

We recommend using C99-style designated initializers as above, to avoid listing all the `PyTypeObject`{.interpreted-text role="c:type"} fields that you don\'t care about and also to avoid caring about the fields\' declaration order.
::::

The actual definition of `PyTypeObject`{.interpreted-text role="c:type"} in `object.h`{.interpreted-text role="file"} has many more `fields <type-structs>`{.interpreted-text role="ref"} than the definition above. The remaining fields will be filled with zeros by the C compiler, and it\'s common practice to not specify them explicitly unless you need them.

We\'re going to pick it apart, one field at a time:

``` c
.ob_base = PyVarObject_HEAD_INIT(NULL, 0)
```

This line is mandatory boilerplate to initialize the `ob_base` field mentioned above. :

``` c
.tp_name = "custom.Custom",
```

The name of our type. This will appear in the default textual representation of our objects and in some error messages, for example:

``` pycon
>>> "" + custom.Custom()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only concatenate str (not "custom.Custom") to str
```

Note that the name is a dotted name that includes both the module name and the name of the type within the module. The module in this case is `!custom`{.interpreted-text role="mod"} and the type is `!Custom`{.interpreted-text role="class"}, so we set the type name to `!custom.Custom`{.interpreted-text role="class"}. Using the real dotted import path is important to make your type compatible with the `pydoc`{.interpreted-text role="mod"} and `pickle`{.interpreted-text role="mod"} modules. :

``` c
.tp_basicsize = sizeof(CustomObject),
.tp_itemsize = 0,
```

This is so that Python knows how much memory to allocate when creating new `!Custom`{.interpreted-text role="class"} instances. `~PyTypeObject.tp_itemsize`{.interpreted-text role="c:member"} is only used for variable-sized objects and should otherwise be zero.

:::: note
::: title
Note
:::

If you want your type to be subclassable from Python, and your type has the same `~PyTypeObject.tp_basicsize`{.interpreted-text role="c:member"} as its base type, you may have problems with multiple inheritance. A Python subclass of your type will have to list your type first in its `~type.__bases__`{.interpreted-text role="attr"}, or else it will not be able to call your type\'s `~object.__new__`{.interpreted-text role="meth"} method without getting an error. You can avoid this problem by ensuring that your type has a larger value for `~PyTypeObject.tp_basicsize`{.interpreted-text role="c:member"} than its base type does. Most of the time, this will be true anyway, because either your base type will be `object`{.interpreted-text role="class"}, or else you will be adding data members to your base type, and therefore increasing its size.
::::

We set the class flags to `Py_TPFLAGS_DEFAULT`{.interpreted-text role="c:macro"}. :

``` c
.tp_flags = Py_TPFLAGS_DEFAULT,
```

All types should include this constant in their flags. It enables all of the members defined until at least Python 3.3. If you need further members, you will need to OR the corresponding flags.

We provide a doc string for the type in `~PyTypeObject.tp_doc`{.interpreted-text role="c:member"}. :

``` c
.tp_doc = PyDoc_STR("Custom objects"),
```

To enable object creation, we have to provide a `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} handler. This is the equivalent of the Python method `~object.__new__`{.interpreted-text role="meth"}, but has to be specified explicitly. In this case, we can just use the default implementation provided by the API function `PyType_GenericNew`{.interpreted-text role="c:func"}. :

``` c
.tp_new = PyType_GenericNew,
```

Everything else in the file should be familiar, except for some code in `!custom_module_exec`{.interpreted-text role="c:func"}:

``` c
if (PyType_Ready(&CustomType) < 0) {
    return -1;
}
```

This initializes the `!Custom`{.interpreted-text role="class"} type, filling in a number of members to the appropriate default values, including `~PyObject.ob_type`{.interpreted-text role="c:member"} that we initially set to `NULL`. :

``` c
if (PyModule_AddObjectRef(m, "Custom", (PyObject *) &CustomType) < 0) {
    return -1;
}
```

This adds the type to the module dictionary. This allows us to create `!Custom`{.interpreted-text role="class"} instances by calling the `!Custom`{.interpreted-text role="class"} class:

``` pycon
>>> import custom
>>> mycustom = custom.Custom()
```

That\'s it! All that remains is to build it; put the above code in a file called `custom.c`{.interpreted-text role="file"},

::: literalinclude
../includes/newtypes/pyproject.toml
:::

in a file called `pyproject.toml`{.interpreted-text role="file"}, and

``` python
from setuptools import Extension, setup
setup(ext_modules=[Extension("custom", ["custom.c"])])
```

in a file called `setup.py`{.interpreted-text role="file"}; then typing

``` shell-session
$ python -m pip install .
```

in a shell should produce a file `custom.so`{.interpreted-text role="file"} in a subdirectory and install it; now fire up Python \-\-- you should be able to `import custom` and play around with `Custom` objects.

That wasn\'t so hard, was it?

Of course, the current Custom type is pretty uninteresting. It has no data and doesn\'t do anything. It can\'t even be subclassed.

## Adding data and methods to the Basic example

Let\'s extend the basic example to add some data and methods. Let\'s also make the type usable as a base class. We\'ll create a new module, `!custom2`{.interpreted-text role="mod"} that adds these capabilities:

::: literalinclude
../includes/newtypes/custom2.c
:::

This version of the module has a number of changes.

The `!Custom`{.interpreted-text role="class"} type now has three data attributes in its C struct, *first*, *last*, and *number*. The *first* and *last* variables are Python strings containing first and last names. The *number* attribute is a C integer.

The object structure is updated accordingly:

``` c
typedef struct {
    PyObject_HEAD
    PyObject *first; /* first name */
    PyObject *last;  /* last name */
    int number;
} CustomObject;
```

Because we now have data to manage, we have to be more careful about object allocation and deallocation. At a minimum, we need a deallocation method:

``` c
static void
Custom_dealloc(PyObject *op)
{
    CustomObject *self = (CustomObject *) op;
    Py_XDECREF(self->first);
    Py_XDECREF(self->last);
    Py_TYPE(self)->tp_free(self);
}
```

which is assigned to the `~PyTypeObject.tp_dealloc`{.interpreted-text role="c:member"} member:

``` c
.tp_dealloc = Custom_dealloc,
```

This method first clears the reference counts of the two Python attributes. `Py_XDECREF`{.interpreted-text role="c:func"} correctly handles the case where its argument is `NULL` (which might happen here if `tp_new` failed midway). It then calls the `~PyTypeObject.tp_free`{.interpreted-text role="c:member"} member of the object\'s type (computed by `Py_TYPE(self)`) to free the object\'s memory. Note that the object\'s type might not be `!CustomType`{.interpreted-text role="class"}, because the object may be an instance of a subclass.

:::: note
::: title
Note
:::

The explicit cast to `CustomObject *` above is needed because we defined `Custom_dealloc` to take a `PyObject *` argument, as the `tp_dealloc` function pointer expects to receive a `PyObject *` argument. By assigning to the `tp_dealloc` slot of a type, we declare that it can only be called with instances of our `CustomObject` class, so the cast to `(CustomObject *)` is safe. This is object-oriented polymorphism, in C!

In existing code, or in previous versions of this tutorial, you might see similar functions take a pointer to the subtype object structure (`CustomObject*`) directly, like this:

``` c
Custom_dealloc(CustomObject *self)
{
    Py_XDECREF(self->first);
    Py_XDECREF(self->last);
    Py_TYPE(self)->tp_free((PyObject *) self);
}
...
.tp_dealloc = (destructor) Custom_dealloc,
```

This does the same thing on all architectures that CPython supports, but according to the C standard, it invokes undefined behavior.
::::

We want to make sure that the first and last names are initialized to empty strings, so we provide a `tp_new` implementation:

``` c
static PyObject *
Custom_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    CustomObject *self;
    self = (CustomObject *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->first = PyUnicode_FromString("");
        if (self->first == NULL) {
            Py_DECREF(self);
            return NULL;
        }
        self->last = PyUnicode_FromString("");
        if (self->last == NULL) {
            Py_DECREF(self);
            return NULL;
        }
        self->number = 0;
    }
    return (PyObject *) self;
}
```

and install it in the `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} member:

``` c
.tp_new = Custom_new,
```

The `tp_new` handler is responsible for creating (as opposed to initializing) objects of the type. It is exposed in Python as the `~object.__new__`{.interpreted-text role="meth"} method. It is not required to define a `tp_new` member, and indeed many extension types will simply reuse `PyType_GenericNew`{.interpreted-text role="c:func"} as done in the first version of the `!Custom`{.interpreted-text role="class"} type above. In this case, we use the `tp_new` handler to initialize the `first` and `last` attributes to non-`NULL` default values.

`tp_new` is passed the type being instantiated (not necessarily `CustomType`, if a subclass is instantiated) and any arguments passed when the type was called, and is expected to return the instance created. `tp_new` handlers always accept positional and keyword arguments, but they often ignore the arguments, leaving the argument handling to initializer (a.k.a. `tp_init` in C or `__init__` in Python) methods.

:::: note
::: title
Note
:::

`tp_new` shouldn\'t call `tp_init` explicitly, as the interpreter will do it itself.
::::

The `tp_new` implementation calls the `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} slot to allocate memory:

``` c
self = (CustomObject *) type->tp_alloc(type, 0);
```

Since memory allocation may fail, we must check the `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} result against `NULL` before proceeding.

:::: note
::: title
Note
:::

We didn\'t fill the `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} slot ourselves. Rather `PyType_Ready`{.interpreted-text role="c:func"} fills it for us by inheriting it from our base class, which is `object`{.interpreted-text role="class"} by default. Most types use the default allocation strategy.
::::

:::: note
::: title
Note
:::

If you are creating a co-operative `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} (one that calls a base type\'s `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} or `~object.__new__`{.interpreted-text role="meth"}), you must *not* try to determine what method to call using method resolution order at runtime. Always statically determine what type you are going to call, and call its `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} directly, or via `type->tp_base->tp_new`. If you do not do this, Python subclasses of your type that also inherit from other Python-defined classes may not work correctly. (Specifically, you may not be able to create instances of such subclasses without getting a `TypeError`{.interpreted-text role="exc"}.)
::::

We also define an initialization function which accepts arguments to provide initial values for our instance:

``` c
static int
Custom_init(PyObject *op, PyObject *args, PyObject *kwds)
{
    CustomObject *self = (CustomObject *) op;
    static char *kwlist[] = {"first", "last", "number", NULL};
    PyObject *first = NULL, *last = NULL, *tmp;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OOi", kwlist,
                                     &first, &last,
                                     &self->number))
        return -1;

    if (first) {
        tmp = self->first;
        Py_INCREF(first);
        self->first = first;
        Py_XDECREF(tmp);
    }
    if (last) {
        tmp = self->last;
        Py_INCREF(last);
        self->last = last;
        Py_XDECREF(tmp);
    }
    return 0;
}
```

by filling the `~PyTypeObject.tp_init`{.interpreted-text role="c:member"} slot. :

``` c
.tp_init = Custom_init,
```

The `~PyTypeObject.tp_init`{.interpreted-text role="c:member"} slot is exposed in Python as the `~object.__init__`{.interpreted-text role="meth"} method. It is used to initialize an object after it\'s created. Initializers always accept positional and keyword arguments, and they should return either `0` on success or `-1` on error.

Unlike the `tp_new` handler, there is no guarantee that `tp_init` is called at all (for example, the `pickle`{.interpreted-text role="mod"} module by default doesn\'t call `~object.__init__`{.interpreted-text role="meth"} on unpickled instances). It can also be called multiple times. Anyone can call the `!__init__`{.interpreted-text role="meth"} method on our objects. For this reason, we have to be extra careful when assigning the new attribute values. We might be tempted, for example to assign the `first` member like this:

``` c
if (first) {
    Py_XDECREF(self->first);
    Py_INCREF(first);
    self->first = first;
}
```

But this would be risky. Our type doesn\'t restrict the type of the `first` member, so it could be any kind of object. It could have a destructor that causes code to be executed that tries to access the `first` member; or that destructor could detach the `thread state <attached thread state>`{.interpreted-text role="term"} and let arbitrary code run in other threads that accesses and modifies our object.

To be paranoid and protect ourselves against this possibility, we almost always reassign members before decrementing their reference counts. When don\'t we have to do this?

- when we absolutely know that the reference count is greater than 1;
- when we know that deallocation of the object[^1] will neither detach the `thread state <attached thread state>`{.interpreted-text role="term"} nor cause any calls back into our type\'s code;
- when decrementing a reference count in a `~PyTypeObject.tp_dealloc`{.interpreted-text role="c:member"} handler on a type which doesn\'t support cyclic garbage collection[^2].

We want to expose our instance variables as attributes. There are a number of ways to do that. The simplest way is to define member definitions:

``` c
static PyMemberDef Custom_members[] = {
    {"first", Py_T_OBJECT_EX, offsetof(CustomObject, first), 0,
     "first name"},
    {"last", Py_T_OBJECT_EX, offsetof(CustomObject, last), 0,
     "last name"},
    {"number", Py_T_INT, offsetof(CustomObject, number), 0,
     "custom number"},
    {NULL}  /* Sentinel */
};
```

and put the definitions in the `~PyTypeObject.tp_members`{.interpreted-text role="c:member"} slot:

``` c
.tp_members = Custom_members,
```

Each member definition has a member name, type, offset, access flags and documentation string. See the `Generic-Attribute-Management`{.interpreted-text role="ref"} section below for details.

A disadvantage of this approach is that it doesn\'t provide a way to restrict the types of objects that can be assigned to the Python attributes. We expect the first and last names to be strings, but any Python objects can be assigned. Further, the attributes can be deleted, setting the C pointers to `NULL`. Even though we can make sure the members are initialized to non-`NULL` values, the members can be set to `NULL` if the attributes are deleted.

We define a single method, `!Custom.name`{.interpreted-text role="meth"}, that outputs the objects name as the concatenation of the first and last names. :

``` c
static PyObject *
Custom_name(PyObject *op, PyObject *Py_UNUSED(dummy))
{
    CustomObject *self = (CustomObject *) op;
    if (self->first == NULL) {
        PyErr_SetString(PyExc_AttributeError, "first");
        return NULL;
    }
    if (self->last == NULL) {
        PyErr_SetString(PyExc_AttributeError, "last");
        return NULL;
    }
    return PyUnicode_FromFormat("%S %S", self->first, self->last);
}
```

The method is implemented as a C function that takes a `!Custom`{.interpreted-text role="class"} (or `!Custom`{.interpreted-text role="class"} subclass) instance as the first argument. Methods always take an instance as the first argument. Methods often take positional and keyword arguments as well, but in this case we don\'t take any and don\'t need to accept a positional argument tuple or keyword argument dictionary. This method is equivalent to the Python method:

``` python
def name(self):
    return "%s %s" % (self.first, self.last)
```

Note that we have to check for the possibility that our `!first`{.interpreted-text role="attr"} and `!last`{.interpreted-text role="attr"} members are `NULL`. This is because they can be deleted, in which case they are set to `NULL`. It would be better to prevent deletion of these attributes and to restrict the attribute values to be strings. We\'ll see how to do that in the next section.

Now that we\'ve defined the method, we need to create an array of method definitions:

``` c
static PyMethodDef Custom_methods[] = {
    {"name", Custom_name, METH_NOARGS,
     "Return the name, combining the first and last name"
    },
    {NULL}  /* Sentinel */
};
```

(note that we used the `METH_NOARGS`{.interpreted-text role="c:macro"} flag to indicate that the method is expecting no arguments other than *self*)

and assign it to the `~PyTypeObject.tp_methods`{.interpreted-text role="c:member"} slot:

``` c
.tp_methods = Custom_methods,
```

Finally, we\'ll make our type usable as a base class for subclassing. We\'ve written our methods carefully so far so that they don\'t make any assumptions about the type of the object being created or used, so all we need to do is to add the `Py_TPFLAGS_BASETYPE`{.interpreted-text role="c:macro"} to our class flag definition:

``` c
.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
```

We rename `!PyInit_custom`{.interpreted-text role="c:func"} to `!PyInit_custom2`{.interpreted-text role="c:func"}, update the module name in the `PyModuleDef`{.interpreted-text role="c:type"} struct, and update the full class name in the `PyTypeObject`{.interpreted-text role="c:type"} struct.

Finally, we update our `setup.py`{.interpreted-text role="file"} file to include the new module,

``` python
from setuptools import Extension, setup
setup(ext_modules=[
    Extension("custom", ["custom.c"]),
    Extension("custom2", ["custom2.c"]),
])
```

and then we re-install so that we can `import custom2`:

``` shell-session
$ python -m pip install .
```

## Providing finer control over data attributes

In this section, we\'ll provide finer control over how the `!first`{.interpreted-text role="attr"} and `!last`{.interpreted-text role="attr"} attributes are set in the `!Custom`{.interpreted-text role="class"} example. In the previous version of our module, the instance variables `!first`{.interpreted-text role="attr"} and `!last`{.interpreted-text role="attr"} could be set to non-string values or even deleted. We want to make sure that these attributes always contain strings.

::: literalinclude
../includes/newtypes/custom3.c
:::

To provide greater control, over the `!first`{.interpreted-text role="attr"} and `!last`{.interpreted-text role="attr"} attributes, we\'ll use custom getter and setter functions. Here are the functions for getting and setting the `!first`{.interpreted-text role="attr"} attribute:

``` c
static PyObject *
Custom_getfirst(PyObject *op, void *closure)
{
    CustomObject *self = (CustomObject *) op;
    Py_INCREF(self->first);
    return self->first;
}

static int
Custom_setfirst(PyObject *op, PyObject *value, void *closure)
{
    CustomObject *self = (CustomObject *) op;
    PyObject *tmp;
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the first attribute");
        return -1;
    }
    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The first attribute value must be a string");
        return -1;
    }
    tmp = self->first;
    Py_INCREF(value);
    self->first = value;
    Py_DECREF(tmp);
    return 0;
}
```

The getter function is passed a `!Custom`{.interpreted-text role="class"} object and a \"closure\", which is a void pointer. In this case, the closure is ignored. (The closure supports an advanced usage in which definition data is passed to the getter and setter. This could, for example, be used to allow a single set of getter and setter functions that decide the attribute to get or set based on data in the closure.)

The setter function is passed the `!Custom`{.interpreted-text role="class"} object, the new value, and the closure. The new value may be `NULL`, in which case the attribute is being deleted. In our setter, we raise an error if the attribute is deleted or if its new value is not a string.

We create an array of `PyGetSetDef`{.interpreted-text role="c:type"} structures:

``` c
static PyGetSetDef Custom_getsetters[] = {
    {"first", Custom_getfirst, Custom_setfirst,
     "first name", NULL},
    {"last", Custom_getlast, Custom_setlast,
     "last name", NULL},
    {NULL}  /* Sentinel */
};
```

and register it in the `~PyTypeObject.tp_getset`{.interpreted-text role="c:member"} slot:

``` c
.tp_getset = Custom_getsetters,
```

The last item in a `PyGetSetDef`{.interpreted-text role="c:type"} structure is the \"closure\" mentioned above. In this case, we aren\'t using a closure, so we just pass `NULL`.

We also remove the member definitions for these attributes:

``` c
static PyMemberDef Custom_members[] = {
    {"number", Py_T_INT, offsetof(CustomObject, number), 0,
     "custom number"},
    {NULL}  /* Sentinel */
};
```

We also need to update the `~PyTypeObject.tp_init`{.interpreted-text role="c:member"} handler to only allow strings[^3] to be passed:

``` c
static int
Custom_init(PyObject *op, PyObject *args, PyObject *kwds)
{
    CustomObject *self = (CustomObject *) op;
    static char *kwlist[] = {"first", "last", "number", NULL};
    PyObject *first = NULL, *last = NULL, *tmp;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|UUi", kwlist,
                                     &first, &last,
                                     &self->number))
        return -1;

    if (first) {
        tmp = self->first;
        Py_INCREF(first);
        self->first = first;
        Py_DECREF(tmp);
    }
    if (last) {
        tmp = self->last;
        Py_INCREF(last);
        self->last = last;
        Py_DECREF(tmp);
    }
    return 0;
}
```

With these changes, we can assure that the `first` and `last` members are never `NULL` so we can remove checks for `NULL` values in almost all cases. This means that most of the `Py_XDECREF`{.interpreted-text role="c:func"} calls can be converted to `Py_DECREF`{.interpreted-text role="c:func"} calls. The only place we can\'t change these calls is in the `tp_dealloc` implementation, where there is the possibility that the initialization of these members failed in `tp_new`.

We also rename the module initialization function and module name in the initialization function, as we did before, and we add an extra definition to the `setup.py`{.interpreted-text role="file"} file.

## Supporting cyclic garbage collection

Python has a `cyclic garbage collector (GC) <garbage collection>`{.interpreted-text role="term"} that can identify unneeded objects even when their reference counts are not zero. This can happen when objects are involved in cycles. For example, consider:

``` pycon
>>> l = []
>>> l.append(l)
>>> del l
```

In this example, we create a list that contains itself. When we delete it, it still has a reference from itself. Its reference count doesn\'t drop to zero. Fortunately, Python\'s cyclic garbage collector will eventually figure out that the list is garbage and free it.

In the second version of the `!Custom`{.interpreted-text role="class"} example, we allowed any kind of object to be stored in the `!first`{.interpreted-text role="attr"} or `!last`{.interpreted-text role="attr"} attributes[^4]. Besides, in the second and third versions, we allowed subclassing `!Custom`{.interpreted-text role="class"}, and subclasses may add arbitrary attributes. For any of those two reasons, `!Custom`{.interpreted-text role="class"} objects can participate in cycles:

``` pycon
>>> import custom3
>>> class Derived(custom3.Custom): pass
...
>>> n = Derived()
>>> n.some_attribute = n
```

To allow a `!Custom`{.interpreted-text role="class"} instance participating in a reference cycle to be properly detected and collected by the cyclic GC, our `!Custom`{.interpreted-text role="class"} type needs to fill two additional slots and to enable a flag that enables these slots:

::: literalinclude
../includes/newtypes/custom4.c
:::

First, the traversal method lets the cyclic GC know about subobjects that could participate in cycles:

``` c
static int
Custom_traverse(PyObject *op, visitproc visit, void *arg)
{
    CustomObject *self = (CustomObject *) op;
    int vret;
    if (self->first) {
        vret = visit(self->first, arg);
        if (vret != 0)
            return vret;
    }
    if (self->last) {
        vret = visit(self->last, arg);
        if (vret != 0)
            return vret;
    }
    return 0;
}
```

For each subobject that can participate in cycles, we need to call the `!visit`{.interpreted-text role="c:func"} function, which is passed to the traversal method. The `!visit`{.interpreted-text role="c:func"} function takes as arguments the subobject and the extra argument *arg* passed to the traversal method. It returns an integer value that must be returned if it is non-zero.

Python provides a `Py_VISIT`{.interpreted-text role="c:func"} macro that automates calling visit functions. With `Py_VISIT`{.interpreted-text role="c:func"}, we can minimize the amount of boilerplate in `Custom_traverse`:

``` c
static int
Custom_traverse(PyObject *op, visitproc visit, void *arg)
{
    CustomObject *self = (CustomObject *) op;
    Py_VISIT(self->first);
    Py_VISIT(self->last);
    return 0;
}
```

:::: note
::: title
Note
:::

The `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} implementation must name its arguments exactly *visit* and *arg* in order to use `Py_VISIT`{.interpreted-text role="c:func"}.
::::

Second, we need to provide a method for clearing any subobjects that can participate in cycles:

``` c
static int
Custom_clear(PyObject *op)
{
    CustomObject *self = (CustomObject *) op;
    Py_CLEAR(self->first);
    Py_CLEAR(self->last);
    return 0;
}
```

Notice the use of the `Py_CLEAR`{.interpreted-text role="c:func"} macro. It is the recommended and safe way to clear data attributes of arbitrary types while decrementing their reference counts. If you were to call `Py_XDECREF`{.interpreted-text role="c:func"} instead on the attribute before setting it to `NULL`, there is a possibility that the attribute\'s destructor would call back into code that reads the attribute again (*especially* if there is a reference cycle).

:::: note
::: title
Note
:::

You could emulate `Py_CLEAR`{.interpreted-text role="c:func"} by writing:

PyObject \*tmp; tmp = self-\>first; self-\>first = NULL; Py_XDECREF(tmp);

Nevertheless, it is much easier and less error-prone to always use `Py_CLEAR`{.interpreted-text role="c:func"} when deleting an attribute. Don\'t try to micro-optimize at the expense of robustness!
::::

The deallocator `Custom_dealloc` may call arbitrary code when clearing attributes. It means the circular GC can be triggered inside the function. Since the GC assumes reference count is not zero, we need to untrack the object from the GC by calling `PyObject_GC_UnTrack`{.interpreted-text role="c:func"} before clearing members. Here is our reimplemented deallocator using `PyObject_GC_UnTrack`{.interpreted-text role="c:func"} and `Custom_clear`:

``` c
static void
Custom_dealloc(PyObject *op)
{
    PyObject_GC_UnTrack(op);
    (void)Custom_clear(op);
    Py_TYPE(op)->tp_free(op);
}
```

Finally, we add the `Py_TPFLAGS_HAVE_GC`{.interpreted-text role="c:macro"} flag to the class flags:

``` c
.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
```

That\'s pretty much it. If we had written custom `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} or `~PyTypeObject.tp_free`{.interpreted-text role="c:member"} handlers, we\'d need to modify them for cyclic garbage collection. Most extensions will use the versions automatically provided.

## Subclassing other types

It is possible to create new extension types that are derived from existing types. It is easiest to inherit from the built in types, since an extension can easily use the `PyTypeObject`{.interpreted-text role="c:type"} it needs. It can be difficult to share these `PyTypeObject`{.interpreted-text role="c:type"} structures between extension modules.

In this example we will create a `!SubList`{.interpreted-text role="class"} type that inherits from the built-in `list`{.interpreted-text role="class"} type. The new type will be completely compatible with regular lists, but will have an additional `!increment`{.interpreted-text role="meth"} method that increases an internal counter:

``` pycon
>>> import sublist
>>> s = sublist.SubList(range(3))
>>> s.extend(s)
>>> print(len(s))
6
>>> print(s.increment())
1
>>> print(s.increment())
2
```

::: literalinclude
../includes/newtypes/sublist.c
:::

As you can see, the source code closely resembles the `!Custom`{.interpreted-text role="class"} examples in previous sections. We will break down the main differences between them. :

``` c
typedef struct {
    PyListObject list;
    int state;
} SubListObject;
```

The primary difference for derived type objects is that the base type\'s object structure must be the first value. The base type will already include the `PyObject_HEAD`{.interpreted-text role="c:func"} at the beginning of its structure.

When a Python object is a `!SubList`{.interpreted-text role="class"} instance, its `PyObject *` pointer can be safely cast to both `PyListObject *` and `SubListObject *`:

``` c
static int
SubList_init(PyObject *op, PyObject *args, PyObject *kwds)
{
    SubListObject *self = (SubListObject *) op;
    if (PyList_Type.tp_init(op, args, kwds) < 0)
        return -1;
    self->state = 0;
    return 0;
}
```

We see above how to call through to the `~object.__init__`{.interpreted-text role="meth"} method of the base type.

This pattern is important when writing a type with custom `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} and `~PyTypeObject.tp_dealloc`{.interpreted-text role="c:member"} members. The `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} handler should not actually create the memory for the object with its `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"}, but let the base class handle it by calling its own `~PyTypeObject.tp_new`{.interpreted-text role="c:member"}.

The `PyTypeObject`{.interpreted-text role="c:type"} struct supports a `~PyTypeObject.tp_base`{.interpreted-text role="c:member"} specifying the type\'s concrete base class. Due to cross-platform compiler issues, you can\'t fill that field directly with a reference to `PyList_Type`{.interpreted-text role="c:type"}; it should be done in the `Py_mod_exec`{.interpreted-text role="c:data"} function:

``` c
static int
sublist_module_exec(PyObject *m)
{
    SubListType.tp_base = &PyList_Type;
    if (PyType_Ready(&SubListType) < 0) {
        return -1;
    }

    if (PyModule_AddObjectRef(m, "SubList", (PyObject *) &SubListType) < 0) {
        return -1;
    }

    return 0;
}
```

Before calling `PyType_Ready`{.interpreted-text role="c:func"}, the type structure must have the `~PyTypeObject.tp_base`{.interpreted-text role="c:member"} slot filled in. When we are deriving an existing type, it is not necessary to fill out the `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} slot with `PyType_GenericNew`{.interpreted-text role="c:func"} \-- the allocation function from the base type will be inherited.

After that, calling `PyType_Ready`{.interpreted-text role="c:func"} and adding the type object to the module is the same as with the basic `!Custom`{.interpreted-text role="class"} examples.

**Footnotes**

[^1]: This is true when we know that the object is a basic type, like a string or a float.

[^2]: We relied on this in the `~PyTypeObject.tp_dealloc`{.interpreted-text role="c:member"} handler in this example, because our type doesn\'t support garbage collection.

[^3]: We now know that the first and last members are strings, so perhaps we could be less careful about decrementing their reference counts, however, we accept instances of string subclasses. Even though deallocating normal strings won\'t call back into our objects, we can\'t guarantee that deallocating an instance of a string subclass won\'t call back into our objects.

[^4]: Also, even with our attributes restricted to strings instances, the user could pass arbitrary `str`{.interpreted-text role="class"} subclasses and therefore still create reference cycles.
