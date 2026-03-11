# `!pickle`{.interpreted-text role="mod"} \-\-- Python object serialization

::: {.module synopsis="Convert Python objects to streams of bytes and back."}
pickle
:::

**Source code:** `Lib/pickle.py`{.interpreted-text role="source"}

::: index
single: persistence pair: persistent; objects pair: serializing; objects pair: marshalling; objects pair: flattening; objects pair: pickling; objects
:::

------------------------------------------------------------------------

The `!pickle`{.interpreted-text role="mod"} module implements binary protocols for serializing and de-serializing a Python object structure. *\"Pickling\"* is the process whereby a Python object hierarchy is converted into a byte stream, and *\"unpickling\"* is the inverse operation, whereby a byte stream (from a `binary file`{.interpreted-text role="term"} or `bytes-like object`{.interpreted-text role="term"}) is converted back into an object hierarchy. Pickling (and unpickling) is alternatively known as \"serialization\", \"marshalling,\"[^1] or \"flattening\"; however, to avoid confusion, the terms used here are \"pickling\" and \"unpickling\".

:::: warning
::: title
Warning
:::

The `pickle` module **is not secure**. Only unpickle data you trust.

It is possible to construct malicious pickle data which will **execute arbitrary code during unpickling**. Never unpickle data that could have come from an untrusted source, or that could have been tampered with.

Consider signing data with `hmac`{.interpreted-text role="mod"} if you need to ensure that it has not been tampered with.

Safer serialization formats such as `json`{.interpreted-text role="mod"} may be more appropriate if you are processing untrusted data. See `comparison-with-json`{.interpreted-text role="ref"}.
::::

## Relationship to other Python modules

### Comparison with `marshal`

Python has a more primitive serialization module called `marshal`{.interpreted-text role="mod"}, but in general `!pickle`{.interpreted-text role="mod"} should always be the preferred way to serialize Python objects. `marshal`{.interpreted-text role="mod"} exists primarily to support Python\'s `.pyc`{.interpreted-text role="file"} files.

The `!pickle`{.interpreted-text role="mod"} module differs from `marshal`{.interpreted-text role="mod"} in several significant ways:

- `marshal`{.interpreted-text role="mod"} cannot be used to serialize user-defined classes and their instances. `!pickle`{.interpreted-text role="mod"} can save and restore class instances transparently, however the class definition must be importable and live in the same module as when the object was stored.
- The `marshal`{.interpreted-text role="mod"} serialization format is not guaranteed to be portable across Python versions. Because its primary job in life is to support `.pyc`{.interpreted-text role="file"} files, the Python implementers reserve the right to change the serialization format in non-backwards compatible ways should the need arise. The `!pickle`{.interpreted-text role="mod"} serialization format is guaranteed to be backwards compatible across Python releases provided a compatible pickle protocol is chosen and pickling and unpickling code deals with Python 2 to Python 3 type differences if your data is crossing that unique breaking change language boundary.

### Comparison with `json`

There are fundamental differences between the pickle protocols and [JSON (JavaScript Object Notation)](https://json.org):

- JSON is a text serialization format (it outputs unicode text, although most of the time it is then encoded to `utf-8`), while pickle is a binary serialization format;
- JSON is human-readable, while pickle is not;
- JSON is interoperable and widely used outside of the Python ecosystem, while pickle is Python-specific;
- JSON, by default, can only represent a subset of the Python built-in types, and no custom classes; pickle can represent an extremely large number of Python types (many of them automatically, by clever usage of Python\'s introspection facilities; complex cases can be tackled by implementing `specific object APIs <pickle-inst>`{.interpreted-text role="ref"});
- Unlike pickle, deserializing untrusted JSON does not in itself create an arbitrary code execution vulnerability.

::: seealso
The `json`{.interpreted-text role="mod"} module: a standard library module allowing JSON serialization and deserialization.
:::

## Data stream format {#pickle-protocols}

::: index
single: External Data Representation
:::

The data format used by `!pickle`{.interpreted-text role="mod"} is Python-specific. This has the advantage that there are no restrictions imposed by external standards such as JSON (which can\'t represent pointer sharing); however it means that non-Python programs may not be able to reconstruct pickled Python objects.

By default, the `!pickle`{.interpreted-text role="mod"} data format uses a relatively compact binary representation. If you need optimal size characteristics, you can efficiently `compress <archiving>`{.interpreted-text role="doc"} pickled data.

The module `pickletools`{.interpreted-text role="mod"} contains tools for analyzing data streams generated by `!pickle`{.interpreted-text role="mod"}. `pickletools`{.interpreted-text role="mod"} source code has extensive comments about opcodes used by pickle protocols.

There are currently 6 different protocols which can be used for pickling. The higher the protocol used, the more recent the version of Python needed to read the pickle produced.

- Protocol version 0 is the original \"human-readable\" protocol and is backwards compatible with earlier versions of Python.
- Protocol version 1 is an old binary format which is also compatible with earlier versions of Python.
- Protocol version 2 was introduced in Python 2.3. It provides much more efficient pickling of `new-style classes <new-style class>`{.interpreted-text role="term"}. Refer to `307`{.interpreted-text role="pep"} for information about improvements brought by protocol 2.
- Protocol version 3 was added in Python 3.0. It has explicit support for `bytes`{.interpreted-text role="class"} objects and cannot be unpickled by Python 2.x. This was the default protocol in Python 3.0\--3.7.
- Protocol version 4 was added in Python 3.4. It adds support for very large objects, pickling more kinds of objects, and some data format optimizations. This was the default protocol in Python 3.8\--3.13. Refer to `3154`{.interpreted-text role="pep"} for information about improvements brought by protocol 4.
- Protocol version 5 was added in Python 3.8. It adds support for out-of-band data and speedup for in-band data. It is the default protocol starting with Python 3.14. Refer to `574`{.interpreted-text role="pep"} for information about improvements brought by protocol 5.

:::: note
::: title
Note
:::

Serialization is a more primitive notion than persistence; although `!pickle`{.interpreted-text role="mod"} reads and writes file objects, it does not handle the issue of naming persistent objects, nor the (even more complicated) issue of concurrent access to persistent objects. The `!pickle`{.interpreted-text role="mod"} module can transform a complex object into a byte stream and it can transform the byte stream into an object with the same internal structure. Perhaps the most obvious thing to do with these byte streams is to write them onto a file, but it is also conceivable to send them across a network or store them in a database. The `shelve`{.interpreted-text role="mod"} module provides a simple interface to pickle and unpickle objects on DBM-style database files.
::::

## Module Interface

To serialize an object hierarchy, you simply call the `dumps`{.interpreted-text role="func"} function. Similarly, to de-serialize a data stream, you call the `loads`{.interpreted-text role="func"} function. However, if you want more control over serialization and de-serialization, you can create a `Pickler`{.interpreted-text role="class"} or an `Unpickler`{.interpreted-text role="class"} object, respectively.

The `!pickle`{.interpreted-text role="mod"} module provides the following constants:

::: data
HIGHEST_PROTOCOL

An integer, the highest `protocol version <pickle-protocols>`{.interpreted-text role="ref"} available. This value can be passed as a *protocol* value to functions `dump`{.interpreted-text role="func"} and `dumps`{.interpreted-text role="func"} as well as the `Pickler`{.interpreted-text role="class"} constructor.
:::

:::::: data
DEFAULT_PROTOCOL

An integer, the default `protocol version <pickle-protocols>`{.interpreted-text role="ref"} used for pickling. May be less than `HIGHEST_PROTOCOL`{.interpreted-text role="data"}. Currently the default protocol is 5, introduced in Python 3.8 and incompatible with previous versions. This version introduces support for out-of-band buffers, where `3118`{.interpreted-text role="pep"}-compatible data can be transmitted separately from the main pickle stream.

::: versionchanged
3.0

The default protocol is 3.
:::

::: versionchanged
3.8

The default protocol is 4.
:::

::: versionchanged
3.14

The default protocol is 5.
:::
::::::

The `!pickle`{.interpreted-text role="mod"} module provides the following functions to make the pickling process more convenient:

:::: function
dump(obj, file, protocol=None, \*, fix_imports=True, buffer_callback=None)

Write the pickled representation of the object *obj* to the open `file object`{.interpreted-text role="term"} *file*. This is equivalent to `Pickler(file, protocol).dump(obj)`.

Arguments *file*, *protocol*, *fix_imports* and *buffer_callback* have the same meaning as in the `Pickler`{.interpreted-text role="class"} constructor.

::: versionchanged
3.8 The *buffer_callback* argument was added.
:::
::::

:::: function
dumps(obj, protocol=None, \*, fix_imports=True, buffer_callback=None)

Return the pickled representation of the object *obj* as a `bytes`{.interpreted-text role="class"} object, instead of writing it to a file.

Arguments *protocol*, *fix_imports* and *buffer_callback* have the same meaning as in the `Pickler`{.interpreted-text role="class"} constructor.

::: versionchanged
3.8 The *buffer_callback* argument was added.
:::
::::

:::: function
load(file, \*, fix_imports=True, encoding=\"ASCII\", errors=\"strict\", buffers=None)

Read the pickled representation of an object from the open `file object`{.interpreted-text role="term"} *file* and return the reconstituted object hierarchy specified therein. This is equivalent to `Unpickler(file).load()`.

The protocol version of the pickle is detected automatically, so no protocol argument is needed. Bytes past the pickled representation of the object are ignored.

Arguments *file*, *fix_imports*, *encoding*, *errors*, *strict* and *buffers* have the same meaning as in the `Unpickler`{.interpreted-text role="class"} constructor.

::: versionchanged
3.8 The *buffers* argument was added.
:::
::::

:::: function
loads(data, /, \*, fix_imports=True, encoding=\"ASCII\", errors=\"strict\", buffers=None)

Return the reconstituted object hierarchy of the pickled representation *data* of an object. *data* must be a `bytes-like object`{.interpreted-text role="term"}.

The protocol version of the pickle is detected automatically, so no protocol argument is needed. Bytes past the pickled representation of the object are ignored.

Arguments *fix_imports*, *encoding*, *errors*, *strict* and *buffers* have the same meaning as in the `Unpickler`{.interpreted-text role="class"} constructor.

::: versionchanged
3.8 The *buffers* argument was added.
:::
::::

The `!pickle`{.interpreted-text role="mod"} module defines three exceptions:

::: exception
PickleError

Common base class for the other pickling exceptions. It inherits from `Exception`{.interpreted-text role="exc"}.
:::

::: exception
PicklingError

Error raised when an unpicklable object is encountered by `Pickler`{.interpreted-text role="class"}. It inherits from `PickleError`{.interpreted-text role="exc"}.

Refer to `pickle-picklable`{.interpreted-text role="ref"} to learn what kinds of objects can be pickled.
:::

::: exception
UnpicklingError

Error raised when there is a problem unpickling an object, such as a data corruption or a security violation. It inherits from `PickleError`{.interpreted-text role="exc"}.

Note that other exceptions may also be raised during unpickling, including (but not necessarily limited to) AttributeError, EOFError, ImportError, and IndexError.
:::

The `!pickle`{.interpreted-text role="mod"} module exports three classes, `Pickler`{.interpreted-text role="class"}, `Unpickler`{.interpreted-text role="class"} and `PickleBuffer`{.interpreted-text role="class"}:

::::::::::::: {.Pickler(file, .protocol=None, .*, .fix_imports=True, .buffer_callback=None)}
This takes a binary file for writing a pickle data stream.

The optional *protocol* argument, an integer, tells the pickler to use the given protocol; supported protocols are 0 to `HIGHEST_PROTOCOL`{.interpreted-text role="data"}. If not specified, the default is `DEFAULT_PROTOCOL`{.interpreted-text role="data"}. If a negative number is specified, `HIGHEST_PROTOCOL`{.interpreted-text role="data"} is selected.

The *file* argument must have a write() method that accepts a single bytes argument. It can thus be an on-disk file opened for binary writing, an `io.BytesIO`{.interpreted-text role="class"} instance, or any other custom object that meets this interface.

If *fix_imports* is true and *protocol* is less than 3, pickle will try to map the new Python 3 names to the old module names used in Python 2, so that the pickle data stream is readable with Python 2.

If *buffer_callback* is `None` (the default), buffer views are serialized into *file* as part of the pickle stream.

If *buffer_callback* is not `None`, then it can be called any number of times with a buffer view. If the callback returns a false value (such as `None`), the given buffer is `out-of-band <pickle-oob>`{.interpreted-text role="ref"}; otherwise the buffer is serialized in-band, i.e. inside the pickle stream.

It is an error if *buffer_callback* is not `None` and *protocol* is `None` or smaller than 5.

::: versionchanged
3.8 The *buffer_callback* argument was added.
:::

::: method
dump(obj)

Write the pickled representation of *obj* to the open file object given in the constructor.
:::

:::: method
persistent_id(obj)

Do nothing by default. This exists so a subclass can override it.

If `persistent_id`{.interpreted-text role="meth"} returns `None`, *obj* is pickled as usual. Any other value causes `Pickler`{.interpreted-text role="class"} to emit the returned value as a persistent ID for *obj*. The meaning of this persistent ID should be defined by `Unpickler.persistent_load`{.interpreted-text role="meth"}. Note that the value returned by `persistent_id`{.interpreted-text role="meth"} cannot itself have a persistent ID.

See `pickle-persistent`{.interpreted-text role="ref"} for details and examples of uses.

::: versionchanged
3.13 Add the default implementation of this method in the C implementation of `!Pickler`{.interpreted-text role="class"}.
:::
::::

:::: attribute
dispatch_table

A pickler object\'s dispatch table is a registry of *reduction functions* of the kind which can be declared using `copyreg.pickle`{.interpreted-text role="func"}. It is a mapping whose keys are classes and whose values are reduction functions. A reduction function takes a single argument of the associated class and should conform to the same interface as a `~object.__reduce__`{.interpreted-text role="meth"} method.

By default, a pickler object will not have a `dispatch_table`{.interpreted-text role="attr"} attribute, and it will instead use the global dispatch table managed by the `copyreg`{.interpreted-text role="mod"} module. However, to customize the pickling for a specific pickler object one can set the `dispatch_table`{.interpreted-text role="attr"} attribute to a dict-like object. Alternatively, if a subclass of `Pickler`{.interpreted-text role="class"} has a `dispatch_table`{.interpreted-text role="attr"} attribute then this will be used as the default dispatch table for instances of that class.

See `pickle-dispatch`{.interpreted-text role="ref"} for usage examples.

::: versionadded
3.3
:::
::::

:::: method
reducer_override(obj)

Special reducer that can be defined in `Pickler`{.interpreted-text role="class"} subclasses. This method has priority over any reducer in the `dispatch_table`{.interpreted-text role="attr"}. It should conform to the same interface as a `~object.__reduce__`{.interpreted-text role="meth"} method, and can optionally return `NotImplemented`{.interpreted-text role="data"} to fallback on `dispatch_table`{.interpreted-text role="attr"}-registered reducers to pickle `obj`.

For a detailed example, see `reducer_override`{.interpreted-text role="ref"}.

::: versionadded
3.8
:::
::::

::: attribute
fast

Deprecated. Enable fast mode if set to a true value. The fast mode disables the usage of memo, therefore speeding the pickling process by not generating superfluous PUT opcodes. It should not be used with self-referential objects, doing otherwise will cause `Pickler`{.interpreted-text role="class"} to recurse infinitely.

Use `pickletools.optimize`{.interpreted-text role="func"} if you need more compact pickles.
:::

::: method
clear_memo()

Clears the pickler\'s \"memo\".

The memo is the data structure that remembers which objects the pickler has already seen, so that shared or recursive objects are pickled by reference and not by value. This method is useful when re-using picklers.
:::
:::::::::::::

::::::::: {.Unpickler(file, .*, .fix_imports=True, .encoding=\"ASCII\", .errors=\"strict\", .buffers=None)}
This takes a binary file for reading a pickle data stream.

The protocol version of the pickle is detected automatically, so no protocol argument is needed.

The argument *file* must have three methods, a read() method that takes an integer argument, a readinto() method that takes a buffer argument and a readline() method that requires no arguments, as in the `io.BufferedIOBase`{.interpreted-text role="class"} interface. Thus *file* can be an on-disk file opened for binary reading, an `io.BytesIO`{.interpreted-text role="class"} object, or any other custom object that meets this interface.

The optional arguments *fix_imports*, *encoding* and *errors* are used to control compatibility support for pickle stream generated by Python 2. If *fix_imports* is true, pickle will try to map the old Python 2 names to the new names used in Python 3. The *encoding* and *errors* tell pickle how to decode 8-bit string instances pickled by Python 2; these default to \'ASCII\' and \'strict\', respectively. The *encoding* can be \'bytes\' to read these 8-bit string instances as bytes objects. Using `encoding='latin1'` is required for unpickling NumPy arrays and instances of `~datetime.datetime`{.interpreted-text role="class"}, `~datetime.date`{.interpreted-text role="class"} and `~datetime.time`{.interpreted-text role="class"} pickled by Python 2.

If *buffers* is `None` (the default), then all data necessary for deserialization must be contained in the pickle stream. This means that the *buffer_callback* argument was `None` when a `Pickler`{.interpreted-text role="class"} was instantiated (or when `dump`{.interpreted-text role="func"} or `dumps`{.interpreted-text role="func"} was called).

If *buffers* is not `None`, it should be an iterable of buffer-enabled objects that is consumed each time the pickle stream references an `out-of-band <pickle-oob>`{.interpreted-text role="ref"} buffer view. Such buffers have been given in order to the *buffer_callback* of a Pickler object.

::: versionchanged
3.8 The *buffers* argument was added.
:::

::: method
load()

Read the pickled representation of an object from the open file object given in the constructor, and return the reconstituted object hierarchy specified therein. Bytes past the pickled representation of the object are ignored.
:::

:::: method
persistent_load(pid)

Raise an `UnpicklingError`{.interpreted-text role="exc"} by default.

If defined, `persistent_load`{.interpreted-text role="meth"} should return the object specified by the persistent ID *pid*. If an invalid persistent ID is encountered, an `UnpicklingError`{.interpreted-text role="exc"} should be raised.

See `pickle-persistent`{.interpreted-text role="ref"} for details and examples of uses.

::: versionchanged
3.13 Add the default implementation of this method in the C implementation of `!Unpickler`{.interpreted-text role="class"}.
:::
::::

:::: method
find_class(module, name)

Import *module* if necessary and return the object called *name* from it, where the *module* and *name* arguments are `str`{.interpreted-text role="class"} objects. Note, unlike its name suggests, `find_class`{.interpreted-text role="meth"} is also used for finding functions.

Subclasses may override this to gain control over what type of objects and how they can be loaded, potentially reducing security risks. Refer to `pickle-restrict`{.interpreted-text role="ref"} for details.

::: audit-event
pickle.find_class module,name pickle.Unpickler.find_class
:::
::::
:::::::::

:::::: PickleBuffer(buffer)
A wrapper for a buffer representing picklable data. *buffer* must be a `buffer-providing <bufferobjects>`{.interpreted-text role="ref"} object, such as a `bytes-like object`{.interpreted-text role="term"} or a N-dimensional array.

`PickleBuffer`{.interpreted-text role="class"} is itself a buffer provider, therefore it is possible to pass it to other APIs expecting a buffer-providing object, such as `memoryview`{.interpreted-text role="class"}.

`PickleBuffer`{.interpreted-text role="class"} objects can only be serialized using pickle protocol 5 or higher. They are eligible for `out-of-band serialization <pickle-oob>`{.interpreted-text role="ref"}.

::: versionadded
3.8
:::

::: method
raw()

Return a `memoryview`{.interpreted-text role="class"} of the memory area underlying this buffer. The returned object is a one-dimensional, C-contiguous memoryview with format `B` (unsigned bytes). `BufferError`{.interpreted-text role="exc"} is raised if the buffer is neither C- nor Fortran-contiguous.
:::

::: method
release()

Release the underlying buffer exposed by the PickleBuffer object.
:::
::::::

## What can be pickled and unpickled? {#pickle-picklable}

The following types can be pickled:

- built-in constants (`None`, `True`, `False`, `Ellipsis`, and `NotImplemented`{.interpreted-text role="data"});
- integers, floating-point numbers, complex numbers;
- strings, bytes, bytearrays;
- tuples, lists, sets, and dictionaries containing only picklable objects;
- functions (built-in and user-defined) accessible from the top level of a module (using `def`{.interpreted-text role="keyword"}, not `lambda`{.interpreted-text role="keyword"});
- classes accessible from the top level of a module;
- instances of such classes for which the result of calling `~object.__getstate__`{.interpreted-text role="meth"} is picklable (see section `pickle-inst`{.interpreted-text role="ref"} for details).

Attempts to pickle unpicklable objects will raise the `PicklingError`{.interpreted-text role="exc"} exception; when this happens, an unspecified number of bytes may have already been written to the underlying file. Trying to pickle a highly recursive data structure may exceed the maximum recursion depth, a `RecursionError`{.interpreted-text role="exc"} will be raised in this case. You can carefully raise this limit with `sys.setrecursionlimit`{.interpreted-text role="func"}.

Note that functions (built-in and user-defined) are pickled by fully `qualified name`{.interpreted-text role="term"}, not by value.[^2] This means that only the function name is pickled, along with the name of the containing module and classes. Neither the function\'s code, nor any of its function attributes are pickled. Thus the defining module must be importable in the unpickling environment, and the module must contain the named object, otherwise an exception will be raised.[^3]

Similarly, classes are pickled by fully qualified name, so the same restrictions in the unpickling environment apply. Note that none of the class\'s code or data is pickled, so in the following example the class attribute `attr` is not restored in the unpickling environment:

    class Foo:
        attr = 'A class attribute'

    picklestring = pickle.dumps(Foo)

These restrictions are why picklable functions and classes must be defined at the top level of a module.

Similarly, when class instances are pickled, their class\'s code and data are not pickled along with them. Only the instance data are pickled. This is done on purpose, so you can fix bugs in a class or add methods to the class and still load objects that were created with an earlier version of the class. If you plan to have long-lived objects that will see many versions of a class, it may be worthwhile to put a version number in the objects so that suitable conversions can be made by the class\'s `~object.__setstate__`{.interpreted-text role="meth"} method.

## Pickling Class Instances {#pickle-inst}

::: currentmodule
None
:::

In this section, we describe the general mechanisms available to you to define, customize, and control how class instances are pickled and unpickled.

In most cases, no additional code is needed to make instances picklable. By default, pickle will retrieve the class and the attributes of an instance via introspection. When a class instance is unpickled, its `~object.__init__`{.interpreted-text role="meth"} method is usually *not* invoked. The default behaviour first creates an uninitialized instance and then restores the saved attributes. The following code shows an implementation of this behaviour:

    def save(obj):
        return (obj.__class__, obj.__dict__)

    def restore(cls, attributes):
        obj = cls.__new__(cls)
        obj.__dict__.update(attributes)
        return obj

Classes can alter the default behaviour by providing one or several special methods:

:::: method
object.\_\_getnewargs_ex\_\_()

In protocols 2 and newer, classes that implement the `__getnewargs_ex__`{.interpreted-text role="meth"} method can dictate the values passed to the `__new__`{.interpreted-text role="meth"} method upon unpickling. The method must return a pair `(args, kwargs)` where *args* is a tuple of positional arguments and *kwargs* a dictionary of named arguments for constructing the object. Those will be passed to the `__new__`{.interpreted-text role="meth"} method upon unpickling.

You should implement this method if the `__new__`{.interpreted-text role="meth"} method of your class requires keyword-only arguments. Otherwise, it is recommended for compatibility to implement `__getnewargs__`{.interpreted-text role="meth"}.

::: versionchanged
3.6 `__getnewargs_ex__`{.interpreted-text role="meth"} is now used in protocols 2 and 3.
:::
::::

:::: method
object.\_\_getnewargs\_\_()

This method serves a similar purpose as `__getnewargs_ex__`{.interpreted-text role="meth"}, but supports only positional arguments. It must return a tuple of arguments `args` which will be passed to the `__new__`{.interpreted-text role="meth"} method upon unpickling.

`__getnewargs__`{.interpreted-text role="meth"} will not be called if `__getnewargs_ex__`{.interpreted-text role="meth"} is defined.

::: versionchanged
3.6 Before Python 3.6, `__getnewargs__`{.interpreted-text role="meth"} was called instead of `__getnewargs_ex__`{.interpreted-text role="meth"} in protocols 2 and 3.
:::
::::

:::: method
object.\_\_getstate\_\_()

Classes can further influence how their instances are pickled by overriding the method `__getstate__`{.interpreted-text role="meth"}. It is called and the returned object is pickled as the contents for the instance, instead of a default state. There are several cases:

- For a class that has no instance `~object.__dict__`{.interpreted-text role="attr"} and no `~object.__slots__`{.interpreted-text role="attr"}, the default state is `None`.
- For a class that has an instance `~object.__dict__`{.interpreted-text role="attr"} and no `~object.__slots__`{.interpreted-text role="attr"}, the default state is `self.__dict__`.
- For a class that has an instance `~object.__dict__`{.interpreted-text role="attr"} and `~object.__slots__`{.interpreted-text role="attr"}, the default state is a tuple consisting of two dictionaries: `self.__dict__`, and a dictionary mapping slot names to slot values. Only slots that have a value are included in the latter.
- For a class that has `~object.__slots__`{.interpreted-text role="attr"} and no instance `~object.__dict__`{.interpreted-text role="attr"}, the default state is a tuple whose first item is `None` and whose second item is a dictionary mapping slot names to slot values described in the previous bullet.

::: versionchanged
3.11 Added the default implementation of the `__getstate__()` method in the `object`{.interpreted-text role="class"} class.
:::
::::

::::: method
object.\_\_setstate\_\_(state)

Upon unpickling, if the class defines `__setstate__`{.interpreted-text role="meth"}, it is called with the unpickled state. In that case, there is no requirement for the state object to be a dictionary. Otherwise, the pickled state must be a dictionary and its items are assigned to the new instance\'s dictionary.

:::: note
::: title
Note
:::

If `__reduce__`{.interpreted-text role="meth"} returns a state with value `None` at pickling, the `__setstate__`{.interpreted-text role="meth"} method will not be called upon unpickling.
::::
:::::

Refer to the section `pickle-state`{.interpreted-text role="ref"} for more information about how to use the methods `~object.__getstate__`{.interpreted-text role="meth"} and `~object.__setstate__`{.interpreted-text role="meth"}.

:::: note
::: title
Note
:::

At unpickling time, some methods like `~object.__getattr__`{.interpreted-text role="meth"}, `~object.__getattribute__`{.interpreted-text role="meth"}, or `~object.__setattr__`{.interpreted-text role="meth"} may be called upon the instance. In case those methods rely on some internal invariant being true, the type should implement `~object.__new__`{.interpreted-text role="meth"} to establish such an invariant, as `~object.__init__`{.interpreted-text role="meth"} is not called when unpickling an instance.
::::

::: index
pair: copy; protocol
:::

As we shall see, pickle does not use directly the methods described above. In fact, these methods are part of the copy protocol which implements the `~object.__reduce__`{.interpreted-text role="meth"} special method. The copy protocol provides a unified interface for retrieving the data necessary for pickling and copying objects.[^4]

Although powerful, implementing `~object.__reduce__`{.interpreted-text role="meth"} directly in your classes is error prone. For this reason, class designers should use the high-level interface (i.e., `~object.__getnewargs_ex__`{.interpreted-text role="meth"}, `~object.__getstate__`{.interpreted-text role="meth"} and `~object.__setstate__`{.interpreted-text role="meth"}) whenever possible. We will show, however, cases where using `!__reduce__`{.interpreted-text role="meth"} is the only option or leads to more efficient pickling or both.

::: method
object.\_\_reduce\_\_()

The interface is currently defined as follows. The `__reduce__`{.interpreted-text role="meth"} method takes no argument and shall return either a string or preferably a tuple (the returned object is often referred to as the \"reduce value\").

If a string is returned, the string should be interpreted as the name of a global variable. It should be the object\'s local name relative to its module; the pickle module searches the module namespace to determine the object\'s module. This behaviour is typically useful for singletons.

When a tuple is returned, it must be between two and six items long. Optional items can either be omitted, or `None` can be provided as their value. The semantics of each item are in order:

- A callable object that will be called to create the initial version of the object.

- A tuple of arguments for the callable object. An empty tuple must be given if the callable does not accept any argument.

- Optionally, the object\'s state, which will be passed to the object\'s `__setstate__`{.interpreted-text role="meth"} method as previously described. If the object has no such method then, the value must be a dictionary and it will be added to the object\'s `~object.__dict__`{.interpreted-text role="attr"} attribute.

- Optionally, an iterator (and not a sequence) yielding successive items. These items will be appended to the object either using `obj.append(item)` or, in batch, using `obj.extend(list_of_items)`. This is primarily used for list subclasses, but may be used by other classes as long as they have `~sequence.append`{.interpreted-text role="meth"} and `~sequence.extend`{.interpreted-text role="meth"} methods with the appropriate signature. (Whether `!append`{.interpreted-text role="meth"} or `!extend`{.interpreted-text role="meth"} is used depends on which pickle protocol version is used as well as the number of items to append, so both must be supported.)

- Optionally, an iterator (not a sequence) yielding successive key-value pairs. These items will be stored to the object using `obj[key] = value`. This is primarily used for dictionary subclasses, but may be used by other classes as long as they implement `__setitem__`{.interpreted-text role="meth"}.

- Optionally, a callable with a `(obj, state)` signature. This callable allows the user to programmatically control the state-updating behavior of a specific object, instead of using `obj`\'s static `__setstate__`{.interpreted-text role="meth"} method. If not `None`, this callable will have priority over `obj`\'s `__setstate__`{.interpreted-text role="meth"}.

  ::: versionadded
  3.8 The optional sixth tuple item, `(obj, state)`, was added.
  :::
:::

::: method
object.\_\_reduce_ex\_\_(protocol)

Alternatively, a `__reduce_ex__`{.interpreted-text role="meth"} method may be defined. The only difference is this method should take a single integer argument, the protocol version. When defined, pickle will prefer it over the `__reduce__`{.interpreted-text role="meth"} method. In addition, `__reduce__`{.interpreted-text role="meth"} automatically becomes a synonym for the extended version. The main use for this method is to provide backwards-compatible reduce values for older Python releases.
:::

::: currentmodule
pickle
:::

### Persistence of External Objects {#pickle-persistent}

::: index
single: persistent_id (pickle protocol) single: persistent_load (pickle protocol)
:::

For the benefit of object persistence, the `!pickle`{.interpreted-text role="mod"} module supports the notion of a reference to an object outside the pickled data stream. Such objects are referenced by a persistent ID, which should be either a string of alphanumeric characters (for protocol 0)[^5] or just an arbitrary object (for any newer protocol).

The resolution of such persistent IDs is not defined by the `!pickle`{.interpreted-text role="mod"} module; it will delegate this resolution to the user-defined methods on the pickler and unpickler, `~Pickler.persistent_id`{.interpreted-text role="meth"} and `~Unpickler.persistent_load`{.interpreted-text role="meth"} respectively.

To pickle objects that have an external persistent ID, the pickler must have a custom `~Pickler.persistent_id`{.interpreted-text role="meth"} method that takes an object as an argument and returns either `None` or the persistent ID for that object. When `None` is returned, the pickler simply pickles the object as normal. When a persistent ID string is returned, the pickler will pickle that object, along with a marker so that the unpickler will recognize it as a persistent ID.

To unpickle external objects, the unpickler must have a custom `~Unpickler.persistent_load`{.interpreted-text role="meth"} method that takes a persistent ID object and returns the referenced object.

Here is a comprehensive example presenting how persistent ID can be used to pickle external objects by reference.

::: literalinclude
../includes/dbpickle.py
:::

### Dispatch Tables {#pickle-dispatch}

If one wants to customize pickling of some classes without disturbing any other code which depends on pickling, then one can create a pickler with a private dispatch table.

The global dispatch table managed by the `copyreg`{.interpreted-text role="mod"} module is available as `!copyreg.dispatch_table`{.interpreted-text role="data"}. Therefore, one may choose to use a modified copy of `!copyreg.dispatch_table`{.interpreted-text role="data"} as a private dispatch table.

For example :

    f = io.BytesIO()
    p = pickle.Pickler(f)
    p.dispatch_table = copyreg.dispatch_table.copy()
    p.dispatch_table[SomeClass] = reduce_SomeClass

creates an instance of `pickle.Pickler`{.interpreted-text role="class"} with a private dispatch table which handles the `SomeClass` class specially. Alternatively, the code :

    class MyPickler(pickle.Pickler):
        dispatch_table = copyreg.dispatch_table.copy()
        dispatch_table[SomeClass] = reduce_SomeClass
    f = io.BytesIO()
    p = MyPickler(f)

does the same but all instances of `MyPickler` will by default share the private dispatch table. On the other hand, the code :

    copyreg.pickle(SomeClass, reduce_SomeClass)
    f = io.BytesIO()
    p = pickle.Pickler(f)

modifies the global dispatch table shared by all users of the `copyreg`{.interpreted-text role="mod"} module.

### Handling Stateful Objects {#pickle-state}

::: index
single: \_\_getstate\_\_() (copy protocol) single: \_\_setstate\_\_() (copy protocol)
:::

Here\'s an example that shows how to modify pickling behavior for a class. The `!TextReader`{.interpreted-text role="class"} class below opens a text file, and returns the line number and line contents each time its `!readline`{.interpreted-text role="meth"} method is called. If a `!TextReader`{.interpreted-text role="class"} instance is pickled, all attributes *except* the file object member are saved. When the instance is unpickled, the file is reopened, and reading resumes from the last location. The `!__setstate__`{.interpreted-text role="meth"} and `!__getstate__`{.interpreted-text role="meth"} methods are used to implement this behavior. :

    class TextReader:
        """Print and number lines in a text file."""

        def __init__(self, filename):
            self.filename = filename
            self.file = open(filename)
            self.lineno = 0

        def readline(self):
            self.lineno += 1
            line = self.file.readline()
            if not line:
                return None
            if line.endswith('\n'):
                line = line[:-1]
            return "%i: %s" % (self.lineno, line)

        def __getstate__(self):
            # Copy the object's state from self.__dict__ which contains
            # all our instance attributes. Always use the dict.copy()
            # method to avoid modifying the original state.
            state = self.__dict__.copy()
            # Remove the unpicklable entries.
            del state['file']
            return state

        def __setstate__(self, state):
            # Restore instance attributes (i.e., filename and lineno).
            self.__dict__.update(state)
            # Restore the previously opened file's state. To do so, we need to
            # reopen it and read from it until the line count is restored.
            file = open(self.filename)
            for _ in range(self.lineno):
                file.readline()
            # Finally, save the file.
            self.file = file

A sample usage might be something like this:

    >>> reader = TextReader("hello.txt")
    >>> reader.readline()
    '1: Hello world!'
    >>> reader.readline()
    '2: I am line number two.'
    >>> new_reader = pickle.loads(pickle.dumps(reader))
    >>> new_reader.readline()
    '3: Goodbye!'

## Custom Reduction for Types, Functions, and Other Objects {#reducer_override}

::: versionadded
3.8
:::

Sometimes, `~Pickler.dispatch_table`{.interpreted-text role="attr"} may not be flexible enough. In particular we may want to customize pickling based on another criterion than the object\'s type, or we may want to customize the pickling of functions and classes.

For those cases, it is possible to subclass from the `Pickler`{.interpreted-text role="class"} class and implement a `~Pickler.reducer_override`{.interpreted-text role="meth"} method. This method can return an arbitrary reduction tuple (see `~object.__reduce__`{.interpreted-text role="meth"}). It can alternatively return `NotImplemented`{.interpreted-text role="data"} to fallback to the traditional behavior.

If both the `~Pickler.dispatch_table`{.interpreted-text role="attr"} and `~Pickler.reducer_override`{.interpreted-text role="meth"} are defined, then `~Pickler.reducer_override`{.interpreted-text role="meth"} method takes priority.

:::: note
::: title
Note
:::

For performance reasons, `~Pickler.reducer_override`{.interpreted-text role="meth"} may not be called for the following objects: `None`, `True`, `False`, and exact instances of `int`{.interpreted-text role="class"}, `float`{.interpreted-text role="class"}, `bytes`{.interpreted-text role="class"}, `str`{.interpreted-text role="class"}, `dict`{.interpreted-text role="class"}, `set`{.interpreted-text role="class"}, `frozenset`{.interpreted-text role="class"}, `list`{.interpreted-text role="class"} and `tuple`{.interpreted-text role="class"}.
::::

Here is a simple example where we allow pickling and reconstructing a given class:

    import io
    import pickle

    class MyClass:
        my_attribute = 1

    class MyPickler(pickle.Pickler):
        def reducer_override(self, obj):
            """Custom reducer for MyClass."""
            if getattr(obj, "__name__", None) == "MyClass":
                return type, (obj.__name__, obj.__bases__,
                              {'my_attribute': obj.my_attribute})
            else:
                # For any other object, fallback to usual reduction
                return NotImplemented

    f = io.BytesIO()
    p = MyPickler(f)
    p.dump(MyClass)

    del MyClass

    unpickled_class = pickle.loads(f.getvalue())

    assert isinstance(unpickled_class, type)
    assert unpickled_class.__name__ == "MyClass"
    assert unpickled_class.my_attribute == 1

## Out-of-band Buffers {#pickle-oob}

::: versionadded
3.8
:::

In some contexts, the `!pickle`{.interpreted-text role="mod"} module is used to transfer massive amounts of data. Therefore, it can be important to minimize the number of memory copies, to preserve performance and resource consumption. However, normal operation of the `!pickle`{.interpreted-text role="mod"} module, as it transforms a graph-like structure of objects into a sequential stream of bytes, intrinsically involves copying data to and from the pickle stream.

This constraint can be eschewed if both the *provider* (the implementation of the object types to be transferred) and the *consumer* (the implementation of the communications system) support the out-of-band transfer facilities provided by pickle protocol 5 and higher.

### Provider API

The large data objects to be pickled must implement a `~object.__reduce_ex__`{.interpreted-text role="meth"} method specialized for protocol 5 and higher, which returns a `PickleBuffer`{.interpreted-text role="class"} instance (instead of e.g. a `bytes`{.interpreted-text role="class"} object) for any large data.

A `PickleBuffer`{.interpreted-text role="class"} object *signals* that the underlying buffer is eligible for out-of-band data transfer. Those objects remain compatible with normal usage of the `!pickle`{.interpreted-text role="mod"} module. However, consumers can also opt-in to tell `!pickle`{.interpreted-text role="mod"} that they will handle those buffers by themselves.

### Consumer API

A communications system can enable custom handling of the `PickleBuffer`{.interpreted-text role="class"} objects generated when serializing an object graph.

On the sending side, it needs to pass a *buffer_callback* argument to `Pickler`{.interpreted-text role="class"} (or to the `dump`{.interpreted-text role="func"} or `dumps`{.interpreted-text role="func"} function), which will be called with each `PickleBuffer`{.interpreted-text role="class"} generated while pickling the object graph. Buffers accumulated by the *buffer_callback* will not see their data copied into the pickle stream, only a cheap marker will be inserted.

On the receiving side, it needs to pass a *buffers* argument to `Unpickler`{.interpreted-text role="class"} (or to the `load`{.interpreted-text role="func"} or `loads`{.interpreted-text role="func"} function), which is an iterable of the buffers which were passed to *buffer_callback*. That iterable should produce buffers in the same order as they were passed to *buffer_callback*. Those buffers will provide the data expected by the reconstructors of the objects whose pickling produced the original `PickleBuffer`{.interpreted-text role="class"} objects.

Between the sending side and the receiving side, the communications system is free to implement its own transfer mechanism for out-of-band buffers. Potential optimizations include the use of shared memory or datatype-dependent compression.

### Example

Here is a trivial example where we implement a `bytearray`{.interpreted-text role="class"} subclass able to participate in out-of-band buffer pickling:

    class ZeroCopyByteArray(bytearray):

        def __reduce_ex__(self, protocol):
            if protocol >= 5:
                return type(self)._reconstruct, (PickleBuffer(self),), None
            else:
                # PickleBuffer is forbidden with pickle protocols <= 4.
                return type(self)._reconstruct, (bytearray(self),)

        @classmethod
        def _reconstruct(cls, obj):
            with memoryview(obj) as m:
                # Get a handle over the original buffer object
                obj = m.obj
                if type(obj) is cls:
                    # Original buffer object is a ZeroCopyByteArray, return it
                    # as-is.
                    return obj
                else:
                    return cls(obj)

The reconstructor (the `_reconstruct` class method) returns the buffer\'s providing object if it has the right type. This is an easy way to simulate zero-copy behaviour on this toy example.

On the consumer side, we can pickle those objects the usual way, which when unserialized will give us a copy of the original object:

    b = ZeroCopyByteArray(b"abc")
    data = pickle.dumps(b, protocol=5)
    new_b = pickle.loads(data)
    print(b == new_b)  # True
    print(b is new_b)  # False: a copy was made

But if we pass a *buffer_callback* and then give back the accumulated buffers when unserializing, we are able to get back the original object:

    b = ZeroCopyByteArray(b"abc")
    buffers = []
    data = pickle.dumps(b, protocol=5, buffer_callback=buffers.append)
    new_b = pickle.loads(data, buffers=buffers)
    print(b == new_b)  # True
    print(b is new_b)  # True: no copy was made

This example is limited by the fact that `bytearray`{.interpreted-text role="class"} allocates its own memory: you cannot create a `bytearray`{.interpreted-text role="class"} instance that is backed by another object\'s memory. However, third-party datatypes such as NumPy arrays do not have this limitation, and allow use of zero-copy pickling (or making as few copies as possible) when transferring between distinct processes or systems.

::: seealso
`574`{.interpreted-text role="pep"} \-- Pickle protocol 5 with out-of-band data
:::

## Restricting Globals {#pickle-restrict}

::: index
single: find_class() (pickle protocol)
:::

By default, unpickling will import any class or function that it finds in the pickle data. For many applications, this behaviour is unacceptable as it permits the unpickler to import and invoke arbitrary code. Just consider what this hand-crafted pickle data stream does when loaded:

    >>> import pickle
    >>> pickle.loads(b"cos\nsystem\n(S'echo hello world'\ntR.")
    hello world
    0

In this example, the unpickler imports the `os.system`{.interpreted-text role="func"} function and then apply the string argument \"echo hello world\". Although this example is inoffensive, it is not difficult to imagine one that could damage your system.

For this reason, you may want to control what gets unpickled by customizing `Unpickler.find_class`{.interpreted-text role="meth"}. Unlike its name suggests, `Unpickler.find_class`{.interpreted-text role="meth"} is called whenever a global (i.e., a class or a function) is requested. Thus it is possible to either completely forbid globals or restrict them to a safe subset.

Here is an example of an unpickler allowing only few safe classes from the `builtins`{.interpreted-text role="mod"} module to be loaded:

    import builtins
    import io
    import pickle

    safe_builtins = {
        'range',
        'complex',
        'set',
        'frozenset',
        'slice',
    }

    class RestrictedUnpickler(pickle.Unpickler):

        def find_class(self, module, name):
            # Only allow safe classes from builtins.
            if module == "builtins" and name in safe_builtins:
                return getattr(builtins, name)
            # Forbid everything else.
            raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                         (module, name))

    def restricted_loads(s):
        """Helper function analogous to pickle.loads()."""
        return RestrictedUnpickler(io.BytesIO(s)).load()

A sample usage of our unpickler working as intended:

    >>> restricted_loads(pickle.dumps([1, 2, range(15)]))
    [1, 2, range(0, 15)]
    >>> restricted_loads(b"cos\nsystem\n(S'echo hello world'\ntR.")
    Traceback (most recent call last):
      ...
    pickle.UnpicklingError: global 'os.system' is forbidden
    >>> restricted_loads(b'cbuiltins\neval\n'
    ...                  b'(S\'getattr(__import__("os"), "system")'
    ...                  b'("echo hello world")\'\ntR.')
    Traceback (most recent call last):
      ...
    pickle.UnpicklingError: global 'builtins.eval' is forbidden

As our examples shows, you have to be careful with what you allow to be unpickled. Therefore if security is a concern, you may want to consider alternatives such as the marshalling API in `xmlrpc.client`{.interpreted-text role="mod"} or third-party solutions.

## Performance

Recent versions of the pickle protocol (from protocol 2 and upwards) feature efficient binary encodings for several common features and built-in types. Also, the `!pickle`{.interpreted-text role="mod"} module has a transparent optimizer written in C.

## Examples {#pickle-example}

For the simplest code, use the `dump`{.interpreted-text role="func"} and `load`{.interpreted-text role="func"} functions. :

    import pickle

    # An arbitrary collection of objects supported by pickle.
    data = {
        'a': [1, 2.0, 3+4j],
        'b': ("character string", b"byte string"),
        'c': {None, True, False}
    }

    with open('data.pickle', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

The following example reads the resulting pickled data. :

    import pickle

    with open('data.pickle', 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        data = pickle.load(f)

## Command-line interface {#pickle-cli}

The `!pickle`{.interpreted-text role="mod"} module can be invoked as a script from the command line, it will display contents of the pickle files. However, when the pickle file that you want to examine comes from an untrusted source, `-m pickletools` is a safer option because it does not execute pickle bytecode, see `pickletools CLI usage <pickletools-cli>`{.interpreted-text role="ref"}.

``` bash
python -m pickle pickle_file [pickle_file ...]
```

The following option is accepted:

::: program
pickle
:::

::: option
pickle_file

A pickle file to read, or `-` to indicate reading from standard input.
:::

::: seealso

Module `copyreg`{.interpreted-text role="mod"}

:   Pickle interface constructor registration for extension types.

Module `pickletools`{.interpreted-text role="mod"}

:   Tools for working with and analyzing pickled data.

Module `shelve`{.interpreted-text role="mod"}

:   Indexed databases of objects; uses `!pickle`{.interpreted-text role="mod"}.

Module `copy`{.interpreted-text role="mod"}

:   Shallow and deep object copying.

Module `marshal`{.interpreted-text role="mod"}

:   High-performance serialization of built-in types.
:::

**Footnotes**

[^1]: Don\'t confuse this with the `marshal`{.interpreted-text role="mod"} module

[^2]: This is why `lambda`{.interpreted-text role="keyword"} functions cannot be pickled: all `!lambda`{.interpreted-text role="keyword"} functions share the same name: `<lambda>`.

[^3]: The exception raised will likely be an `ImportError`{.interpreted-text role="exc"} or an `AttributeError`{.interpreted-text role="exc"} but it could be something else.

[^4]: The `copy`{.interpreted-text role="mod"} module uses this protocol for shallow and deep copying operations.

[^5]: The limitation on alphanumeric characters is due to the fact that persistent IDs in protocol 0 are delimited by the newline character. Therefore if any kind of newline characters occurs in persistent IDs, the resulting pickled data will become unreadable.
