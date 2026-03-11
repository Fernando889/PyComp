# Data model {#datamodel}

## Objects, values and types {#objects}

::: index
single: object single: data
:::

`Objects`{.interpreted-text role="dfn"} are Python\'s abstraction for data. All data in a Python program is represented by objects or by relations between objects. Even code is represented by objects.

::: index
pair: built-in function; id pair: built-in function; type single: identity of an object single: value of an object single: type of an object single: mutable object single: immutable object
:::

Every object has an identity, a type and a value. An object\'s *identity* never changes once it has been created; you may think of it as the object\'s address in memory. The `is`{.interpreted-text role="keyword"} operator compares the identity of two objects; the `id`{.interpreted-text role="func"} function returns an integer representing its identity.

::: impl-detail
For CPython, `id(x)` is the memory address where `x` is stored.
:::

An object\'s type determines the operations that the object supports (e.g., \"does it have a length?\") and also defines the possible values for objects of that type. The `type`{.interpreted-text role="func"} function returns an object\'s type (which is an object itself). Like its identity, an object\'s `type`{.interpreted-text role="dfn"} is also unchangeable. [^1]

The *value* of some objects can change. Objects whose value can change are said to be *mutable*; objects whose value is unchangeable once they are created are called *immutable*. (The value of an immutable container object that contains a reference to a mutable object can change when the latter\'s value is changed; however the container is still considered immutable, because the collection of objects it contains cannot be changed. So, immutability is not strictly the same as having an unchangeable value, it is more subtle.) An object\'s mutability is determined by its type; for instance, numbers, strings and tuples are immutable, while dictionaries and lists are mutable.

::: index
single: garbage collection single: reference counting single: unreachable object
:::

Objects are never explicitly destroyed; however, when they become unreachable they may be garbage-collected. An implementation is allowed to postpone garbage collection or omit it altogether \-\-- it is a matter of implementation quality how garbage collection is implemented, as long as no objects are collected that are still reachable.

::: impl-detail
CPython currently uses a reference-counting scheme with (optional) delayed detection of cyclically linked garbage, which collects most objects as soon as they become unreachable, but is not guaranteed to collect garbage containing circular references. See the documentation of the `gc`{.interpreted-text role="mod"} module for information on controlling the collection of cyclic garbage. Other implementations act differently and CPython may change. Do not depend on immediate finalization of objects when they become unreachable (so you should always close files explicitly).
:::

Note that the use of the implementation\'s tracing or debugging facilities may keep objects alive that would normally be collectable. Also note that catching an exception with a `try`{.interpreted-text role="keyword"}\...`except`{.interpreted-text role="keyword"} statement may keep objects alive.

Some objects contain references to \"external\" resources such as open files or windows. It is understood that these resources are freed when the object is garbage-collected, but since garbage collection is not guaranteed to happen, such objects also provide an explicit way to release the external resource, usually a `!close`{.interpreted-text role="meth"} method. Programs are strongly recommended to explicitly close such objects. The `try`{.interpreted-text role="keyword"}\...`finally`{.interpreted-text role="keyword"} statement and the `with`{.interpreted-text role="keyword"} statement provide convenient ways to do this.

::: index
single: container
:::

Some objects contain references to other objects; these are called *containers*. Examples of containers are tuples, lists and dictionaries. The references are part of a container\'s value. In most cases, when we talk about the value of a container, we imply the values, not the identities of the contained objects; however, when we talk about the mutability of a container, only the identities of the immediately contained objects are implied. So, if an immutable container (like a tuple) contains a reference to a mutable object, its value changes if that mutable object is changed.

Types affect almost all aspects of object behavior. Even the importance of object identity is affected in some sense: for immutable types, operations that compute new values may actually return a reference to any existing object with the same type and value, while for mutable objects this is not allowed. For example, after `a = 1; b = 1`, *a* and *b* may or may not refer to the same object with the value one, depending on the implementation. This is because `int`{.interpreted-text role="class"} is an immutable type, so the reference to `1` can be reused. This behaviour depends on the implementation used, so should not be relied upon, but is something to be aware of when making use of object identity tests. However, after `c = []; d = []`, *c* and *d* are guaranteed to refer to two different, unique, newly created empty lists. (Note that `e = f = []` assigns the *same* object to both *e* and *f*.)

## The standard type hierarchy {#types}

::: index
single: type pair: data; type pair: type; hierarchy pair: extension; module pair: C; language
:::

Below is a list of the types that are built into Python. Extension modules (written in C, Java, or other languages, depending on the implementation) can define additional types. Future versions of Python may add types to the type hierarchy (e.g., rational numbers, efficiently stored arrays of integers, etc.), although such additions will often be provided via the standard library instead.

::: index
single: attribute pair: special; attribute triple: generic; special; attribute
:::

Some of the type descriptions below contain a paragraph listing \'special attributes.\' These are attributes that provide access to the implementation and are not intended for general use. Their definition may change in the future.

### None

::: index
pair: object; None
:::

This type has a single value. There is a single object with this value. This object is accessed through the built-in name `None`. It is used to signify the absence of a value in many situations, e.g., it is returned from functions that don\'t explicitly return anything. Its truth value is false.

### NotImplemented

::: index
pair: object; NotImplemented
:::

This type has a single value. There is a single object with this value. This object is accessed through the built-in name `NotImplemented`{.interpreted-text role="data"}. Numeric methods and rich comparison methods should return this value if they do not implement the operation for the operands provided. (The interpreter will then try the reflected operation, or some other fallback, depending on the operator.) It should not be evaluated in a boolean context.

See `implementing-the-arithmetic-operations`{.interpreted-text role="ref"} for more details.

::: versionchanged
3.9 Evaluating `NotImplemented`{.interpreted-text role="data"} in a boolean context was deprecated.
:::

::: versionchanged
3.14 Evaluating `NotImplemented`{.interpreted-text role="data"} in a boolean context now raises a `TypeError`{.interpreted-text role="exc"}. It previously evaluated to `True`{.interpreted-text role="const"} and emitted a `DeprecationWarning`{.interpreted-text role="exc"} since Python 3.9.
:::

### Ellipsis

::: index
pair: object; Ellipsis single: \...; ellipsis literal
:::

This type has a single value. There is a single object with this value. This object is accessed through the literal `...` or the built-in name `Ellipsis`. Its truth value is true.

### `numbers.Number`{.interpreted-text role="class"}

::: index
pair: object; numeric
:::

These are created by numeric literals and returned as results by arithmetic operators and arithmetic built-in functions. Numeric objects are immutable; once created their value never changes. Python numbers are of course strongly related to mathematical numbers, but subject to the limitations of numerical representation in computers.

The string representations of the numeric classes, computed by `~object.__repr__`{.interpreted-text role="meth"} and `~object.__str__`{.interpreted-text role="meth"}, have the following properties:

- They are valid numeric literals which, when passed to their class constructor, produce an object having the value of the original numeric.
- The representation is in base 10, when possible.
- Leading zeros, possibly excepting a single zero before a decimal point, are not shown.
- Trailing zeros, possibly excepting a single zero after a decimal point, are not shown.
- A sign is shown only when the number is negative.

Python distinguishes between integers, floating-point numbers, and complex numbers:

#### `numbers.Integral`{.interpreted-text role="class"}

::: index
pair: object; integer
:::

These represent elements from the mathematical set of integers (positive and negative).

:::: note
::: title
Note
:::

.. index:: pair: integer; representation

The rules for integer representation are intended to give the most meaningful interpretation of shift and mask operations involving negative integers.
::::

There are two types of integers:

Integers (`int`{.interpreted-text role="class"})

:   These represent numbers in an unlimited range, subject to available (virtual) memory only. For the purpose of shift and mask operations, a binary representation is assumed, and negative numbers are represented in a variant of 2\'s complement which gives the illusion of an infinite string of sign bits extending to the left.

Booleans (`bool`{.interpreted-text role="class"})

:   ::: index
    pair: object; Boolean single: False single: True
    :::

    These represent the truth values False and True. The two objects representing the values `False` and `True` are the only Boolean objects. The Boolean type is a subtype of the integer type, and Boolean values behave like the values 0 and 1, respectively, in almost all contexts, the exception being that when converted to a string, the strings `"False"` or `"True"` are returned, respectively.

#### `numbers.Real`{.interpreted-text role="class"} (`float`{.interpreted-text role="class"}) {#datamodel-float}

::: index
pair: object; floating-point pair: floating-point; number pair: C; language pair: Java; language
:::

These represent machine-level double precision floating-point numbers. You are at the mercy of the underlying machine architecture (and C or Java implementation) for the accepted range and handling of overflow. Python does not support single-precision floating-point numbers; the savings in processor and memory usage that are usually the reason for using these are dwarfed by the overhead of using objects in Python, so there is no reason to complicate the language with two kinds of floating-point numbers.

#### `numbers.Complex`{.interpreted-text role="class"} (`complex`{.interpreted-text role="class"})

::: index
pair: object; complex pair: complex; number
:::

These represent complex numbers as a pair of machine-level double precision floating-point numbers. The same caveats apply as for floating-point numbers. The real and imaginary parts of a complex number `z` can be retrieved through the read-only attributes `z.real` and `z.imag`.

### Sequences {#datamodel-sequences}

::: index
pair: built-in function; len pair: object; sequence single: index operation single: item selection single: subscription
:::

These represent finite ordered sets indexed by non-negative numbers. The built-in function `len`{.interpreted-text role="func"} returns the number of items of a sequence. When the length of a sequence is *n*, the index set contains the numbers 0, 1, \..., *n*-1. Item *i* of sequence *a* is selected by `a[i]`. Some sequences, including built-in sequences, interpret negative subscripts by adding the sequence length. For example, `a[-2]` equals `a[n-2]`, the second to last item of sequence a with length `n`.

The resulting value must be a nonnegative integer less than the number of items in the sequence. If it is not, an `IndexError`{.interpreted-text role="exc"} is raised.

::: index
single: slicing single: start (slice object attribute) single: stop (slice object attribute) single: step (slice object attribute)
:::

Sequences also support slicing: `a[start:stop]` selects all items with index *k* such that *start* `<=` *k* `<` *stop*. When used as an expression, a slice is a sequence of the same type. The comment above about negative subscripts also applies to negative slice positions. Note that no error is raised if a slice position is less than zero or larger than the length of the sequence.

If *start* is missing or `None`{.interpreted-text role="data"}, slicing behaves as if *start* was zero. If *stop* is missing or `None`, slicing behaves as if *stop* was equal to the length of the sequence.

Some sequences also support \"extended slicing\" with a third \"step\" parameter: `a[i:j:k]` selects all items of *a* with index *x* where `x = i + n*k`, *n* `>=` `0` and *i* `<=` *x* `<` *j*.

Sequences are distinguished according to their mutability:

#### Immutable sequences

::: index
pair: object; immutable sequence pair: object; immutable
:::

An object of an immutable sequence type cannot change once it is created. (If the object contains references to other objects, these other objects may be mutable and may be changed; however, the collection of objects directly referenced by an immutable object cannot change.)

The following types are immutable sequences:

::: index
single: string; immutable sequences
:::

Strings

:   ::: index
    pair: built-in function; chr pair: built-in function; ord single: character pair: string; item single: Unicode
    :::

    A string (`str`{.interpreted-text role="class"}) is a sequence of values that represent `characters`{.interpreted-text role="dfn"}, or more formally, *Unicode code points*. All the code points in the range `0` to `0x10FFFF` can be represented in a string.

    Python doesn\'t have a dedicated *character* type. Instead, every code point in the string is represented as a string object with length `1`.

    The built-in function `ord`{.interpreted-text role="func"} converts a code point from its string form to an integer in the range `0` to `0x10FFFF`; `chr`{.interpreted-text role="func"} converts an integer in the range `0` to `0x10FFFF` to the corresponding length `1` string object. `str.encode`{.interpreted-text role="meth"} can be used to convert a `str`{.interpreted-text role="class"} to `bytes`{.interpreted-text role="class"} using the given text encoding, and `bytes.decode`{.interpreted-text role="meth"} can be used to achieve the opposite.

Tuples

:   ::: index
    pair: object; tuple pair: singleton; tuple pair: empty; tuple
    :::

    The items of a `tuple`{.interpreted-text role="class"} are arbitrary Python objects. Tuples of two or more items are formed by comma-separated lists of expressions. A tuple of one item (a \'singleton\') can be formed by affixing a comma to an expression (an expression by itself does not create a tuple, since parentheses must be usable for grouping of expressions). An empty tuple can be formed by an empty pair of parentheses.

Bytes

:   ::: index
    bytes, byte
    :::

    A `bytes`{.interpreted-text role="class"} object is an immutable array. The items are 8-bit bytes, represented by integers in the range 0 \<= x \< 256. Bytes literals (like `b'abc'`) and the built-in `bytes`{.interpreted-text role="func"} constructor can be used to create bytes objects. Also, bytes objects can be decoded to strings via the `~bytes.decode`{.interpreted-text role="meth"} method.

#### Mutable sequences

::: index
pair: object; mutable sequence pair: object; mutable pair: assignment; statement single: subscription single: slicing
:::

Mutable sequences can be changed after they are created. The subscription and slicing notations can be used as the target of assignment and `del`{.interpreted-text role="keyword"} (delete) statements.

:::: note
::: title
Note
:::

.. index:: pair: module; array .. index:: pair: module; collections

The `collections`{.interpreted-text role="mod"} and `array`{.interpreted-text role="mod"} module provide additional examples of mutable sequence types.
::::

There are currently two intrinsic mutable sequence types:

Lists

:   ::: index
    pair: object; list
    :::

    The items of a list are arbitrary Python objects. Lists are formed by placing a comma-separated list of expressions in square brackets. (Note that there are no special cases needed to form lists of length 0 or 1.)

Byte Arrays

:   ::: index
    bytearray
    :::

    A bytearray object is a mutable array. They are created by the built-in `bytearray`{.interpreted-text role="func"} constructor. Aside from being mutable (and hence unhashable), byte arrays otherwise provide the same interface and functionality as immutable `bytes`{.interpreted-text role="class"} objects.

### Set types

::: index
pair: built-in function; len pair: object; set type
:::

These represent unordered, finite sets of unique, immutable objects. As such, they cannot be indexed by any subscript. However, they can be iterated over, and the built-in function `len`{.interpreted-text role="func"} returns the number of items in a set. Common uses for sets are fast membership testing, removing duplicates from a sequence, and computing mathematical operations such as intersection, union, difference, and symmetric difference.

For set elements, the same immutability rules apply as for dictionary keys. Note that numeric types obey the normal rules for numeric comparison: if two numbers compare equal (e.g., `1` and `1.0`), only one of them can be contained in a set.

There are currently two intrinsic set types:

Sets

:   ::: index
    pair: object; set
    :::

    These represent a mutable set. They are created by the built-in `set`{.interpreted-text role="func"} constructor and can be modified afterwards by several methods, such as `~set.add`{.interpreted-text role="meth"}.

Frozen sets

:   ::: index
    pair: object; frozenset
    :::

    These represent an immutable set. They are created by the built-in `frozenset`{.interpreted-text role="func"} constructor. As a frozenset is immutable and `hashable`{.interpreted-text role="term"}, it can be used again as an element of another set, or as a dictionary key.

### Mappings {#datamodel-mappings}

::: index
pair: built-in function; len single: subscription pair: object; mapping
:::

These represent finite sets of objects indexed by arbitrary index sets. The subscript notation `a[k]` selects the item indexed by `k` from the mapping `a`; this can be used in expressions and as the target of assignments or `del`{.interpreted-text role="keyword"} statements. The built-in function `len`{.interpreted-text role="func"} returns the number of items in a mapping.

There is currently a single intrinsic mapping type:

#### Dictionaries

::: index
pair: object; dictionary
:::

These represent finite sets of objects indexed by nearly arbitrary values. The only types of values not acceptable as keys are values containing lists or dictionaries or other mutable types that are compared by value rather than by object identity, the reason being that the efficient implementation of dictionaries requires a key\'s hash value to remain constant. Numeric types used for keys obey the normal rules for numeric comparison: if two numbers compare equal (e.g., `1` and `1.0`) then they can be used interchangeably to index the same dictionary entry.

Dictionaries preserve insertion order, meaning that keys will be produced in the same order they were added sequentially over the dictionary. Replacing an existing key does not change the order, however removing a key and re-inserting it will add it to the end instead of keeping its old place.

Dictionaries are mutable; they can be created by the `{}` notation (see section `dict`{.interpreted-text role="ref"}).

::: index
pair: module; dbm.ndbm pair: module; dbm.gnu
:::

The extension modules `dbm.ndbm`{.interpreted-text role="mod"} and `dbm.gnu`{.interpreted-text role="mod"} provide additional examples of mapping types, as does the `collections`{.interpreted-text role="mod"} module.

::: versionchanged
3.7 Dictionaries did not preserve insertion order in versions of Python before 3.6. In CPython 3.6, insertion order was preserved, but it was considered an implementation detail at that time rather than a language guarantee.
:::

### Callable types

::: index
pair: object; callable pair: function; call single: invocation pair: function; argument
:::

These are the types to which the function call operation (see section `calls`{.interpreted-text role="ref"}) can be applied:

#### User-defined functions {#user-defined-funcs}

::: index
pair: user-defined; function pair: object; function pair: object; user-defined function
:::

A user-defined function object is created by a function definition (see section `function`{.interpreted-text role="ref"}). It should be called with an argument list containing the same number of items as the function\'s formal parameter list.

##### Special read-only attributes

::: index
single: \_\_builtins\_\_ (function attribute) single: \_\_closure\_\_ (function attribute) single: \_\_globals\_\_ (function attribute) pair: global; namespace
:::

+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Attribute                 | Meaning                                                                                                                                                                                                                                                                   |
+===========================+===========================================================================================================================================================================================================================================================================+
| ::: attribute             | A reference to the `dictionary <dict>`{.interpreted-text role="class"} that holds the function\'s builtins namespace.                                                                                                                                                     |
| function.\_\_builtins\_\_ |                                                                                                                                                                                                                                                                           |
| :::                       | ::: versionadded                                                                                                                                                                                                                                                          |
|                           | 3.10                                                                                                                                                                                                                                                                      |
|                           | :::                                                                                                                                                                                                                                                                       |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute             | A reference to the `dictionary <dict>`{.interpreted-text role="class"} that holds the function\'s `global variables <naming>`{.interpreted-text role="ref"} \-- the global namespace of the module in which the function was defined.                                     |
| function.\_\_globals\_\_  |                                                                                                                                                                                                                                                                           |
| :::                       |                                                                                                                                                                                                                                                                           |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute             | `None` or a `tuple`{.interpreted-text role="class"} of cells that contain bindings for the names specified in the `~codeobject.co_freevars`{.interpreted-text role="attr"} attribute of the function\'s `code object <function.__code__>`{.interpreted-text role="attr"}. |
| function.\_\_closure\_\_  |                                                                                                                                                                                                                                                                           |
| :::                       | A cell object has the attribute `cell_contents`. This can be used to get the value of the cell, as well as set the value.                                                                                                                                                 |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

##### Special writable attributes

::: index
single: \_\_doc\_\_ (function attribute) single: \_\_name\_\_ (function attribute) single: \_\_module\_\_ (function attribute) single: \_\_dict\_\_ (function attribute) single: \_\_defaults\_\_ (function attribute) single: \_\_code\_\_ (function attribute) single: \_\_annotations\_\_ (function attribute) single: \_\_annotate\_\_ (function attribute) single: \_\_kwdefaults\_\_ (function attribute) single: \_\_type_params\_\_ (function attribute)
:::

Most of these attributes check the type of the assigned value:

+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Attribute                    | Meaning                                                                                                                                                                                                                                                                                                                |
+==============================+========================================================================================================================================================================================================================================================================================================================+
| ::: attribute                | The function\'s documentation string, or `None` if unavailable.                                                                                                                                                                                                                                                        |
| function.\_\_doc\_\_         |                                                                                                                                                                                                                                                                                                                        |
| :::                          |                                                                                                                                                                                                                                                                                                                        |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | The function\'s name. See also: `__name__ attributes <definition.__name__>`{.interpreted-text role="attr"}.                                                                                                                                                                                                            |
| function.\_\_name\_\_        |                                                                                                                                                                                                                                                                                                                        |
| :::                          |                                                                                                                                                                                                                                                                                                                        |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | The function\'s `qualified name`{.interpreted-text role="term"}. See also: `__qualname__ attributes <definition.__qualname__>`{.interpreted-text role="attr"}.                                                                                                                                                         |
| function.\_\_qualname\_\_    |                                                                                                                                                                                                                                                                                                                        |
| :::                          | ::: versionadded                                                                                                                                                                                                                                                                                                       |
|                              | 3.3                                                                                                                                                                                                                                                                                                                    |
|                              | :::                                                                                                                                                                                                                                                                                                                    |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | The name of the module the function was defined in, or `None` if unavailable.                                                                                                                                                                                                                                          |
| function.\_\_module\_\_      |                                                                                                                                                                                                                                                                                                                        |
| :::                          |                                                                                                                                                                                                                                                                                                                        |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | A `tuple`{.interpreted-text role="class"} containing default `parameter`{.interpreted-text role="term"} values for those parameters that have defaults, or `None` if no parameters have a default value.                                                                                                               |
| function.\_\_defaults\_\_    |                                                                                                                                                                                                                                                                                                                        |
| :::                          |                                                                                                                                                                                                                                                                                                                        |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | The `code object <code-objects>`{.interpreted-text role="ref"} representing the compiled function body.                                                                                                                                                                                                                |
| function.\_\_code\_\_        |                                                                                                                                                                                                                                                                                                                        |
| :::                          |                                                                                                                                                                                                                                                                                                                        |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | The namespace supporting arbitrary function attributes. See also: `__dict__ attributes <object.__dict__>`{.interpreted-text role="attr"}.                                                                                                                                                                              |
| function.\_\_dict\_\_        |                                                                                                                                                                                                                                                                                                                        |
| :::                          |                                                                                                                                                                                                                                                                                                                        |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | A `dictionary <dict>`{.interpreted-text role="class"} containing annotations of `parameters <parameter>`{.interpreted-text role="term"}. The keys of the dictionary are the parameter names, and `'return'` for the return annotation, if provided. See also: `object.__annotations__`{.interpreted-text role="attr"}. |
| function.\_\_annotations\_\_ |                                                                                                                                                                                                                                                                                                                        |
| :::                          | ::: versionchanged                                                                                                                                                                                                                                                                                                     |
|                              | 3.14 Annotations are now `lazily evaluated <lazy-evaluation>`{.interpreted-text role="ref"}. See `649`{.interpreted-text role="pep"}.                                                                                                                                                                                  |
|                              | :::                                                                                                                                                                                                                                                                                                                    |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | The `annotate function`{.interpreted-text role="term"} for this function, or `None` if the function has no annotations. See `object.__annotate__`{.interpreted-text role="attr"}.                                                                                                                                      |
| function.\_\_annotate\_\_    |                                                                                                                                                                                                                                                                                                                        |
| :::                          | ::: versionadded                                                                                                                                                                                                                                                                                                       |
|                              | 3.14                                                                                                                                                                                                                                                                                                                   |
|                              | :::                                                                                                                                                                                                                                                                                                                    |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | A `dictionary <dict>`{.interpreted-text role="class"} containing defaults for keyword-only `parameters <parameter>`{.interpreted-text role="term"}.                                                                                                                                                                    |
| function.\_\_kwdefaults\_\_  |                                                                                                                                                                                                                                                                                                                        |
| :::                          |                                                                                                                                                                                                                                                                                                                        |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | A `tuple`{.interpreted-text role="class"} containing the `type parameters <type-params>`{.interpreted-text role="ref"} of a `generic function <generic-functions>`{.interpreted-text role="ref"}.                                                                                                                      |
| function.\_\_type_params\_\_ |                                                                                                                                                                                                                                                                                                                        |
| :::                          | ::: versionadded                                                                                                                                                                                                                                                                                                       |
|                              | 3.12                                                                                                                                                                                                                                                                                                                   |
|                              | :::                                                                                                                                                                                                                                                                                                                    |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Function objects also support getting and setting arbitrary attributes, which can be used, for example, to attach metadata to functions. Regular attribute dot-notation is used to get and set such attributes.

::: impl-detail
CPython\'s current implementation only supports function attributes on user-defined functions. Function attributes on `built-in functions <builtin-functions>`{.interpreted-text role="ref"} may be supported in the future.
:::

Additional information about a function\'s definition can be retrieved from its `code object <code-objects>`{.interpreted-text role="ref"} (accessible via the `~function.__code__`{.interpreted-text role="attr"} attribute).

#### Instance methods

::: index
pair: object; method pair: object; user-defined method pair: user-defined; method
:::

An instance method object combines a class, a class instance and any callable object (normally a user-defined function).

::: index
single: \_\_func\_\_ (method attribute) single: \_\_self\_\_ (method attribute) single: \_\_doc\_\_ (method attribute) single: \_\_name\_\_ (method attribute) single: \_\_module\_\_ (method attribute)
:::

Special read-only attributes:

+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | Refers to the class instance object to which the method is `bound <method-binding>`{.interpreted-text role="ref"}                                                                                                          |
| method.\_\_self\_\_   |                                                                                                                                                                                                                            |
| :::                   |                                                                                                                                                                                                                            |
+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | Refers to the original `function object <user-defined-funcs>`{.interpreted-text role="ref"}                                                                                                                                |
| method.\_\_func\_\_   |                                                                                                                                                                                                                            |
| :::                   |                                                                                                                                                                                                                            |
+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | The method\'s documentation (same as `method.__func__.__doc__ <function.__doc__>`{.interpreted-text role="attr"}). A `string <str>`{.interpreted-text role="class"} if the original function had a docstring, else `None`. |
| method.\_\_doc\_\_    |                                                                                                                                                                                                                            |
| :::                   |                                                                                                                                                                                                                            |
+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | The name of the method (same as `method.__func__.__name__ <function.__name__>`{.interpreted-text role="attr"})                                                                                                             |
| method.\_\_name\_\_   |                                                                                                                                                                                                                            |
| :::                   |                                                                                                                                                                                                                            |
+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | The name of the module the method was defined in, or `None` if unavailable.                                                                                                                                                |
| method.\_\_module\_\_ |                                                                                                                                                                                                                            |
| :::                   |                                                                                                                                                                                                                            |
+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Methods also support accessing (but not setting) the arbitrary function attributes on the underlying `function object <user-defined-funcs>`{.interpreted-text role="ref"}.

User-defined method objects may be created when getting an attribute of a class (perhaps via an instance of that class), if that attribute is a user-defined `function object <user-defined-funcs>`{.interpreted-text role="ref"} or a `classmethod`{.interpreted-text role="class"} object.

::: {#method-binding}
When an instance method object is created by retrieving a user-defined `function object <user-defined-funcs>`{.interpreted-text role="ref"} from a class via one of its instances, its `~method.__self__`{.interpreted-text role="attr"} attribute is the instance, and the method object is said to be *bound*. The new method\'s `~method.__func__`{.interpreted-text role="attr"} attribute is the original function object.
:::

When an instance method object is created by retrieving a `classmethod`{.interpreted-text role="class"} object from a class or instance, its `~method.__self__`{.interpreted-text role="attr"} attribute is the class itself, and its `~method.__func__`{.interpreted-text role="attr"} attribute is the function object underlying the class method.

When an instance method object is called, the underlying function (`~method.__func__`{.interpreted-text role="attr"}) is called, inserting the class instance (`~method.__self__`{.interpreted-text role="attr"}) in front of the argument list. For instance, when `!C`{.interpreted-text role="class"} is a class which contains a definition for a function `!f`{.interpreted-text role="meth"}, and `x` is an instance of `!C`{.interpreted-text role="class"}, calling `x.f(1)` is equivalent to calling `C.f(x, 1)`.

When an instance method object is derived from a `classmethod`{.interpreted-text role="class"} object, the \"class instance\" stored in `~method.__self__`{.interpreted-text role="attr"} will actually be the class itself, so that calling either `x.f(1)` or `C.f(1)` is equivalent to calling `f(C,1)` where `f` is the underlying function.

It is important to note that user-defined functions which are attributes of a class instance are not converted to bound methods; this *only* happens when the function is an attribute of the class.

#### Generator functions

::: index
single: generator; function single: generator; iterator
:::

A function or method which uses the `yield`{.interpreted-text role="keyword"} statement (see section `yield`{.interpreted-text role="ref"}) is called a `generator function`{.interpreted-text role="dfn"}. Such a function, when called, always returns an `iterator`{.interpreted-text role="term"} object which can be used to execute the body of the function: calling the iterator\'s `iterator.__next__`{.interpreted-text role="meth"} method will cause the function to execute until it provides a value using the `!yield`{.interpreted-text role="keyword"} statement. When the function executes a `return`{.interpreted-text role="keyword"} statement or falls off the end, a `StopIteration`{.interpreted-text role="exc"} exception is raised and the iterator will have reached the end of the set of values to be returned.

#### Coroutine functions

::: index
single: coroutine; function
:::

A function or method which is defined using `async def`{.interpreted-text role="keyword"} is called a `coroutine function`{.interpreted-text role="dfn"}. Such a function, when called, returns a `coroutine`{.interpreted-text role="term"} object. It may contain `await`{.interpreted-text role="keyword"} expressions, as well as `async with`{.interpreted-text role="keyword"} and `async for`{.interpreted-text role="keyword"} statements. See also the `coroutine-objects`{.interpreted-text role="ref"} section.

#### Asynchronous generator functions

::: index
single: asynchronous generator; function single: asynchronous generator; asynchronous iterator
:::

A function or method which is defined using `async def`{.interpreted-text role="keyword"} and which uses the `yield`{.interpreted-text role="keyword"} statement is called a `asynchronous generator function`{.interpreted-text role="dfn"}. Such a function, when called, returns an `asynchronous iterator`{.interpreted-text role="term"} object which can be used in an `async for`{.interpreted-text role="keyword"} statement to execute the body of the function.

Calling the asynchronous iterator\'s `aiterator.__anext__ <object.__anext__>`{.interpreted-text role="meth"} method will return an `awaitable`{.interpreted-text role="term"} which when awaited will execute until it provides a value using the `yield`{.interpreted-text role="keyword"} expression. When the function executes an empty `return`{.interpreted-text role="keyword"} statement or falls off the end, a `StopAsyncIteration`{.interpreted-text role="exc"} exception is raised and the asynchronous iterator will have reached the end of the set of values to be yielded.

#### Built-in functions {#builtin-functions}

::: index
pair: object; built-in function pair: object; function pair: C; language
:::

A built-in function object is a wrapper around a C function. Examples of built-in functions are `len`{.interpreted-text role="func"} and `math.sin`{.interpreted-text role="func"} (`math`{.interpreted-text role="mod"} is a standard built-in module). The number and type of the arguments are determined by the C function. Special read-only attributes:

- `!__doc__`{.interpreted-text role="attr"} is the function\'s documentation string, or `None` if unavailable. See `function.__doc__`{.interpreted-text role="attr"}.
- `!__name__`{.interpreted-text role="attr"} is the function\'s name. See `function.__name__`{.interpreted-text role="attr"}.
- `!__self__`{.interpreted-text role="attr"} is set to `None` (but see the next item).
- `!__module__`{.interpreted-text role="attr"} is the name of the module the function was defined in or `None` if unavailable. See `function.__module__`{.interpreted-text role="attr"}.

#### Built-in methods {#builtin-methods}

::: index
pair: object; built-in method pair: object; method pair: built-in; method
:::

This is really a different disguise of a built-in function, this time containing an object passed to the C function as an implicit extra argument. An example of a built-in method is `alist.append()`, assuming *alist* is a list object. In this case, the special read-only attribute `!__self__`{.interpreted-text role="attr"} is set to the object denoted by *alist*. (The attribute has the same semantics as it does with `other instance methods <method.__self__>`{.interpreted-text role="attr"}.)

#### Classes

Classes are callable. These objects normally act as factories for new instances of themselves, but variations are possible for class types that override `~object.__new__`{.interpreted-text role="meth"}. The arguments of the call are passed to `!__new__`{.interpreted-text role="meth"} and, in the typical case, to `~object.__init__`{.interpreted-text role="meth"} to initialize the new instance.

#### Class Instances

Instances of arbitrary classes can be made callable by defining a `~object.__call__`{.interpreted-text role="meth"} method in their class.

### Modules {#module-objects}

::: index
pair: statement; import pair: object; module
:::

Modules are a basic organizational unit of Python code, and are created by the `import system <importsystem>`{.interpreted-text role="ref"} as invoked either by the `import`{.interpreted-text role="keyword"} statement, or by calling functions such as `importlib.import_module`{.interpreted-text role="func"} and built-in `__import__`{.interpreted-text role="func"}. A module object has a namespace implemented by a `dictionary <dict>`{.interpreted-text role="class"} object (this is the dictionary referenced by the `~function.__globals__`{.interpreted-text role="attr"} attribute of functions defined in the module). Attribute references are translated to lookups in this dictionary, e.g., `m.x` is equivalent to `m.__dict__["x"]`. A module object does not contain the code object used to initialize the module (since it isn\'t needed once the initialization is done).

Attribute assignment updates the module\'s namespace dictionary, e.g., `m.x = 1` is equivalent to `m.__dict__["x"] = 1`.

::: index
single: \_\_name\_\_ (module attribute) single: \_\_spec\_\_ (module attribute) single: \_\_package\_\_ (module attribute) single: \_\_loader\_\_ (module attribute) single: \_\_path\_\_ (module attribute) single: \_\_file\_\_ (module attribute) single: \_\_doc\_\_ (module attribute) single: \_\_annotations\_\_ (module attribute) single: \_\_annotate\_\_ (module attribute) pair: module; namespace
:::

#### Import-related attributes on module objects {#import-mod-attrs}

Module objects have the following attributes that relate to the `import system <importsystem>`{.interpreted-text role="ref"}. When a module is created using the machinery associated with the import system, these attributes are filled in based on the module\'s `spec <module spec>`{.interpreted-text role="term"}, before the `loader`{.interpreted-text role="term"} executes and loads the module.

To create a module dynamically rather than using the import system, it\'s recommended to use `importlib.util.module_from_spec`{.interpreted-text role="func"}, which will set the various import-controlled attributes to appropriate values. It\'s also possible to use the `types.ModuleType`{.interpreted-text role="class"} constructor to create modules directly, but this technique is more error-prone, as most attributes must be manually set on the module object after it has been created when using this approach.

::::: caution
::: title
Caution
:::

With the exception of `~module.__name__`{.interpreted-text role="attr"}, it is **strongly** recommended that you rely on `~module.__spec__`{.interpreted-text role="attr"} and its attributes instead of any of the other individual attributes listed in this subsection. Note that updating an attribute on `!__spec__`{.interpreted-text role="attr"} will not update the corresponding attribute on the module itself:

::: doctest
\>\>\> import typing \>\>\> typing.\_\_name\_\_, typing.\_\_spec\_\_.name (\'typing\', \'typing\') \>\>\> typing.\_\_spec\_\_.name = \'spelling\' \>\>\> typing.\_\_name\_\_, typing.\_\_spec\_\_.name (\'typing\', \'spelling\') \>\>\> typing.\_\_name\_\_ = \'keyboard_smashing\' \>\>\> typing.\_\_name\_\_, typing.\_\_spec\_\_.name (\'keyboard_smashing\', \'spelling\')
:::
:::::

::: attribute
module.\_\_name\_\_

The name used to uniquely identify the module in the import system. For a directly executed module, this will be set to `"__main__"`.

This attribute must be set to the fully qualified name of the module. It is expected to match the value of `module.__spec__.name <importlib.machinery.ModuleSpec.name>`{.interpreted-text role="attr"}.
:::

:::: attribute
module.\_\_spec\_\_

A record of the module\'s import-system-related state.

Set to the `module spec <importlib.machinery.ModuleSpec>`{.interpreted-text role="class"} that was used when importing the module. See `module-specs`{.interpreted-text role="ref"} for more details.

::: versionadded
3.4
:::
::::

:::::::: attribute
module.\_\_package\_\_

The `package`{.interpreted-text role="term"} a module belongs to.

If the module is top-level (that is, not a part of any specific package) then the attribute should be set to `''` (the empty string). Otherwise, it should be set to the name of the module\'s package (which can be equal to `module.__name__`{.interpreted-text role="attr"} if the module itself is a package). See `366`{.interpreted-text role="pep"} for further details.

This attribute is used instead of `~module.__name__`{.interpreted-text role="attr"} to calculate explicit relative imports for main modules. It defaults to `None` for modules created dynamically using the `types.ModuleType`{.interpreted-text role="class"} constructor; use `importlib.util.module_from_spec`{.interpreted-text role="func"} instead to ensure the attribute is set to a `str`{.interpreted-text role="class"}.

It is **strongly** recommended that you use `module.__spec__.parent <importlib.machinery.ModuleSpec.parent>`{.interpreted-text role="attr"} instead of `!module.__package__`{.interpreted-text role="attr"}. `__package__`{.interpreted-text role="attr"} is now only used as a fallback if `!__spec__.parent`{.interpreted-text role="attr"} is not set, and this fallback path is deprecated.

::: versionchanged
3.4 This attribute now defaults to `None` for modules created dynamically using the `types.ModuleType`{.interpreted-text role="class"} constructor. Previously the attribute was optional.
:::

::: versionchanged
3.6 The value of `!__package__`{.interpreted-text role="attr"} is expected to be the same as `__spec__.parent <importlib.machinery.ModuleSpec.parent>`{.interpreted-text role="attr"}. `__package__`{.interpreted-text role="attr"} is now only used as a fallback during import resolution if `!__spec__.parent`{.interpreted-text role="attr"} is not defined.
:::

::: versionchanged
3.10 `ImportWarning`{.interpreted-text role="exc"} is raised if an import resolution falls back to `!__package__`{.interpreted-text role="attr"} instead of `__spec__.parent <importlib.machinery.ModuleSpec.parent>`{.interpreted-text role="attr"}.
:::

::: versionchanged
3.12 Raise `DeprecationWarning`{.interpreted-text role="exc"} instead of `ImportWarning`{.interpreted-text role="exc"} when falling back to `!__package__`{.interpreted-text role="attr"} during import resolution.
:::

::: deprecated-removed
3.13 3.15 `!__package__`{.interpreted-text role="attr"} will cease to be set or taken into consideration by the import system or standard library.
:::
::::::::

::::: attribute
module.\_\_loader\_\_

The `loader`{.interpreted-text role="term"} object that the import machinery used to load the module.

This attribute is mostly useful for introspection, but can be used for additional loader-specific functionality, for example getting data associated with a loader.

`!__loader__`{.interpreted-text role="attr"} defaults to `None` for modules created dynamically using the `types.ModuleType`{.interpreted-text role="class"} constructor; use `importlib.util.module_from_spec`{.interpreted-text role="func"} instead to ensure the attribute is set to a `loader`{.interpreted-text role="term"} object.

It is **strongly** recommended that you use `module.__spec__.loader <importlib.machinery.ModuleSpec.loader>`{.interpreted-text role="attr"} instead of `!module.__loader__`{.interpreted-text role="attr"}.

::: versionchanged
3.4 This attribute now defaults to `None` for modules created dynamically using the `types.ModuleType`{.interpreted-text role="class"} constructor. Previously the attribute was optional.
:::

::: deprecated-removed
3.12 3.16 Setting `!__loader__`{.interpreted-text role="attr"} on a module while failing to set `!__spec__.loader`{.interpreted-text role="attr"} is deprecated. In Python 3.16, `!__loader__`{.interpreted-text role="attr"} will cease to be set or taken into consideration by the import system or the standard library.
:::
:::::

::: attribute
module.\_\_path\_\_

A (possibly empty) `sequence`{.interpreted-text role="term"} of strings enumerating the locations where the package\'s submodules will be found. Non-package modules should not have a `!__path__`{.interpreted-text role="attr"} attribute. See `package-path-rules`{.interpreted-text role="ref"} for more details.

It is **strongly** recommended that you use `module.__spec__.submodule_search_locations <importlib.machinery.ModuleSpec.submodule_search_locations>`{.interpreted-text role="attr"} instead of `!module.__path__`{.interpreted-text role="attr"}.
:::

::::: attribute
module.\_\_file\_\_

`!__file__`{.interpreted-text role="attr"} is an optional attribute that may or may not be set. Both attributes should be a `str`{.interpreted-text role="class"} when they are available.

An optional attribute, `!__file__`{.interpreted-text role="attr"} indicates the pathname of the file from which the module was loaded (if loaded from a file), or the pathname of the shared library file for extension modules loaded dynamically from a shared library. It might be missing for certain types of modules, such as C modules that are statically linked into the interpreter, and the `import system <importsystem>`{.interpreted-text role="ref"} may opt to leave it unset if it has no semantic meaning (for example, a module loaded from a database).

::: deprecated-removed
3.13 3.15 Setting `__cached__` on a module while failing to set `!__spec__.cached`{.interpreted-text role="attr"} is deprecated. In Python 3.15, `__cached__` will cease to be set or taken into consideration by the import system or standard library.
:::

::: versionchanged
3.15 `__cached__` is no longer set.
:::
:::::

#### Other writable attributes on module objects

As well as the import-related attributes listed above, module objects also have the following writable attributes:

::: attribute
module.\_\_doc\_\_

The module\'s documentation string, or `None` if unavailable. See also: `__doc__ attributes <definition.__doc__>`{.interpreted-text role="attr"}.
:::

:::: attribute
module.\_\_annotations\_\_

A dictionary containing `variable annotations <variable annotation>`{.interpreted-text role="term"} collected during module body execution. For best practices on working with `!__annotations__`{.interpreted-text role="attr"}, see `annotationlib`{.interpreted-text role="mod"}.

::: versionchanged
3.14 Annotations are now `lazily evaluated <lazy-evaluation>`{.interpreted-text role="ref"}. See `649`{.interpreted-text role="pep"}.
:::
::::

:::: attribute
module.\_\_annotate\_\_

The `annotate function`{.interpreted-text role="term"} for this module, or `None` if the module has no annotations. See also: `~object.__annotate__`{.interpreted-text role="attr"} attributes.

::: versionadded
3.14
:::
::::

#### Module dictionaries

Module objects also have the following special read-only attribute:

::: index
single: \_\_dict\_\_ (module attribute)
:::

:::: attribute
module.\_\_dict\_\_

The module\'s namespace as a dictionary object. Uniquely among the attributes listed here, `!__dict__`{.interpreted-text role="attr"} cannot be accessed as a global variable from within a module; it can only be accessed as an attribute on module objects.

::: impl-detail
Because of the way CPython clears module dictionaries, the module dictionary will be cleared when the module falls out of scope even if the dictionary still has live references. To avoid this, copy the dictionary or keep the module around while using its dictionary directly.
:::
::::

### Custom classes {#class-attrs-and-methods}

Custom class types are typically created by class definitions (see section `class`{.interpreted-text role="ref"}). A class has a namespace implemented by a dictionary object. Class attribute references are translated to lookups in this dictionary, e.g., `C.x` is translated to `C.__dict__["x"]` (although there are a number of hooks which allow for other means of locating attributes). When the attribute name is not found there, the attribute search continues in the base classes. This search of the base classes uses the C3 method resolution order which behaves correctly even in the presence of \'diamond\' inheritance structures where there are multiple inheritance paths leading back to a common ancestor. Additional details on the C3 MRO used by Python can be found at `python_2.3_mro`{.interpreted-text role="ref"}.

::: index
pair: object; class pair: object; class instance pair: object; instance pair: class object; call single: container pair: object; dictionary pair: class; attribute
:::

When a class attribute reference (for class `!C`{.interpreted-text role="class"}, say) would yield a class method object, it is transformed into an instance method object whose `~method.__self__`{.interpreted-text role="attr"} attribute is `!C`{.interpreted-text role="class"}. When it would yield a `staticmethod`{.interpreted-text role="class"} object, it is transformed into the object wrapped by the static method object. See section `descriptors`{.interpreted-text role="ref"} for another way in which attributes retrieved from a class may differ from those actually contained in its `~object.__dict__`{.interpreted-text role="attr"}.

::: index
triple: class; attribute; assignment
:::

Class attribute assignments update the class\'s dictionary, never the dictionary of a base class.

::: index
pair: class object; call
:::

A class object can be called (see above) to yield a class instance (see below).

#### Special attributes

::: index
single: \_\_name\_\_ (class attribute) single: \_\_module\_\_ (class attribute) single: \_\_dict\_\_ (class attribute) single: \_\_bases\_\_ (class attribute) single: \_\_base\_\_ (class attribute) single: \_\_doc\_\_ (class attribute) single: \_\_annotations\_\_ (class attribute) single: \_\_annotate\_\_ (class attribute) single: \_\_type_params\_\_ (class attribute) single: \_\_static_attributes\_\_ (class attribute) single: \_\_firstlineno\_\_ (class attribute)
:::

+--------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Attribute                      | Meaning                                                                                                                                                                                                                                                                                                                                                             |
+================================+=====================================================================================================================================================================================================================================================================================================================================================================+
| ::: attribute                  | The class\'s name. See also: `__name__ attributes <definition.__name__>`{.interpreted-text role="attr"}.                                                                                                                                                                                                                                                            |
| type.\_\_name\_\_              |                                                                                                                                                                                                                                                                                                                                                                     |
| :::                            |                                                                                                                                                                                                                                                                                                                                                                     |
+--------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                  | The class\'s `qualified name`{.interpreted-text role="term"}. See also: `__qualname__ attributes <definition.__qualname__>`{.interpreted-text role="attr"}.                                                                                                                                                                                                         |
| type.\_\_qualname\_\_          |                                                                                                                                                                                                                                                                                                                                                                     |
| :::                            |                                                                                                                                                                                                                                                                                                                                                                     |
+--------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                  | The name of the module in which the class was defined.                                                                                                                                                                                                                                                                                                              |
| type.\_\_module\_\_            |                                                                                                                                                                                                                                                                                                                                                                     |
| :::                            |                                                                                                                                                                                                                                                                                                                                                                     |
+--------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                  | A `mapping proxy <types.MappingProxyType>`{.interpreted-text role="class"} providing a read-only view of the class\'s namespace. See also: `__dict__ attributes <object.__dict__>`{.interpreted-text role="attr"}.                                                                                                                                                  |
| type.\_\_dict\_\_              |                                                                                                                                                                                                                                                                                                                                                                     |
| :::                            |                                                                                                                                                                                                                                                                                                                                                                     |
+--------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                  | A `tuple`{.interpreted-text role="class"} containing the class\'s bases. In most cases, for a class defined as `class X(A, B, C)`, `X.__bases__` will be exactly equal to `(A, B, C)`.                                                                                                                                                                              |
| type.\_\_bases\_\_             |                                                                                                                                                                                                                                                                                                                                                                     |
| :::                            |                                                                                                                                                                                                                                                                                                                                                                     |
+--------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                  | ::: impl-detail                                                                                                                                                                                                                                                                                                                                                     |
| type.\_\_base\_\_              | The single base class in the inheritance chain that is responsible for the memory layout of instances. This attribute corresponds to `~PyTypeObject.tp_base`{.interpreted-text role="c:member"} at the C level.                                                                                                                                                     |
| :::                            | :::                                                                                                                                                                                                                                                                                                                                                                 |
+--------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                  | The class\'s documentation string, or `None` if undefined. Not inherited by subclasses.                                                                                                                                                                                                                                                                             |
| type.\_\_doc\_\_               |                                                                                                                                                                                                                                                                                                                                                                     |
| :::                            |                                                                                                                                                                                                                                                                                                                                                                     |
+--------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                  | A dictionary containing `variable annotations <variable annotation>`{.interpreted-text role="term"} collected during class body execution. See also: `__annotations__ attributes <object.__annotations__>`{.interpreted-text role="attr"}.                                                                                                                          |
| type.\_\_annotations\_\_       |                                                                                                                                                                                                                                                                                                                                                                     |
| :::                            | For best practices on working with `~object.__annotations__`{.interpreted-text role="attr"}, please see `annotationlib`{.interpreted-text role="mod"}. Use `annotationlib.get_annotations`{.interpreted-text role="func"} instead of accessing this attribute directly.                                                                                             |
|                                |                                                                                                                                                                                                                                                                                                                                                                     |
|                                | :::: warning                                                                                                                                                                                                                                                                                                                                                        |
|                                | ::: title                                                                                                                                                                                                                                                                                                                                                           |
|                                | Warning                                                                                                                                                                                                                                                                                                                                                             |
|                                | :::                                                                                                                                                                                                                                                                                                                                                                 |
|                                |                                                                                                                                                                                                                                                                                                                                                                     |
|                                | Accessing the `!__annotations__`{.interpreted-text role="attr"} attribute directly on a class object may return annotations for the wrong class, specifically in certain cases where the class, its base class, or a metaclass is defined under `from __future__ import annotations`. See `749 <749#pep749-metaclasses>`{.interpreted-text role="pep"} for details. |
|                                |                                                                                                                                                                                                                                                                                                                                                                     |
|                                | This attribute does not exist on certain builtin classes. On user-defined classes without `__annotations__`, it is an empty dictionary.                                                                                                                                                                                                                             |
|                                | ::::                                                                                                                                                                                                                                                                                                                                                                |
|                                |                                                                                                                                                                                                                                                                                                                                                                     |
|                                | ::: versionchanged                                                                                                                                                                                                                                                                                                                                                  |
|                                | 3.14 Annotations are now `lazily evaluated <lazy-evaluation>`{.interpreted-text role="ref"}. See `649`{.interpreted-text role="pep"}.                                                                                                                                                                                                                               |
|                                | :::                                                                                                                                                                                                                                                                                                                                                                 |
+--------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: method                     | The `annotate function`{.interpreted-text role="term"} for this class, or `None` if the class has no annotations. See also: `__annotate__ attributes <object.__annotate__>`{.interpreted-text role="attr"}.                                                                                                                                                         |
| type.\_\_annotate\_\_          |                                                                                                                                                                                                                                                                                                                                                                     |
| :::                            | ::: versionadded                                                                                                                                                                                                                                                                                                                                                    |
|                                | 3.14                                                                                                                                                                                                                                                                                                                                                                |
|                                | :::                                                                                                                                                                                                                                                                                                                                                                 |
+--------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                  | A `tuple`{.interpreted-text role="class"} containing the `type parameters <type-params>`{.interpreted-text role="ref"} of a `generic class <generic-classes>`{.interpreted-text role="ref"}.                                                                                                                                                                        |
| type.\_\_type_params\_\_       |                                                                                                                                                                                                                                                                                                                                                                     |
| :::                            | ::: versionadded                                                                                                                                                                                                                                                                                                                                                    |
|                                | 3.12                                                                                                                                                                                                                                                                                                                                                                |
|                                | :::                                                                                                                                                                                                                                                                                                                                                                 |
+--------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                  | A `tuple`{.interpreted-text role="class"} containing names of attributes of this class which are assigned through `self.X` from any function in its body.                                                                                                                                                                                                           |
| type.\_\_static_attributes\_\_ |                                                                                                                                                                                                                                                                                                                                                                     |
| :::                            | ::: versionadded                                                                                                                                                                                                                                                                                                                                                    |
|                                | 3.13                                                                                                                                                                                                                                                                                                                                                                |
|                                | :::                                                                                                                                                                                                                                                                                                                                                                 |
+--------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                  | The line number of the first line of the class definition, including decorators. Setting the `~type.__module__`{.interpreted-text role="attr"} attribute removes the `!__firstlineno__`{.interpreted-text role="attr"} item from the type\'s dictionary.                                                                                                            |
| type.\_\_firstlineno\_\_       |                                                                                                                                                                                                                                                                                                                                                                     |
| :::                            | ::: versionadded                                                                                                                                                                                                                                                                                                                                                    |
|                                | 3.13                                                                                                                                                                                                                                                                                                                                                                |
|                                | :::                                                                                                                                                                                                                                                                                                                                                                 |
+--------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                  | The `tuple`{.interpreted-text role="class"} of classes that are considered when looking for base classes during method resolution.                                                                                                                                                                                                                                  |
| type.\_\_mro\_\_               |                                                                                                                                                                                                                                                                                                                                                                     |
| :::                            |                                                                                                                                                                                                                                                                                                                                                                     |
+--------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

#### Special methods

In addition to the special attributes described above, all Python classes also have the following two methods available:

::: method
type.mro

This method can be overridden by a metaclass to customize the method resolution order for its instances. It is called at class instantiation, and its result is stored in `~type.__mro__`{.interpreted-text role="attr"}.
:::

:::: method
type.\_\_subclasses\_\_

Each class keeps a list of weak references to its immediate subclasses. This method returns a list of all those references still alive. The list is in definition order. Example:

::: doctest
\>\>\> class A: pass \>\>\> class B(A): pass \>\>\> A.\_\_subclasses\_\_() \[\<class \'B\'\>\]
:::
::::

### Class instances

::: index
pair: object; class instance pair: object; instance pair: class; instance pair: class instance; attribute
:::

A class instance is created by calling a class object (see above). A class instance has a namespace implemented as a dictionary which is the first place in which attribute references are searched. When an attribute is not found there, and the instance\'s class has an attribute by that name, the search continues with the class attributes. If a class attribute is found that is a user-defined function object, it is transformed into an instance method object whose `~method.__self__`{.interpreted-text role="attr"} attribute is the instance. Static method and class method objects are also transformed; see above under \"Classes\". See section `descriptors`{.interpreted-text role="ref"} for another way in which attributes of a class retrieved via its instances may differ from the objects actually stored in the class\'s `~object.__dict__`{.interpreted-text role="attr"}. If no class attribute is found, and the object\'s class has a `~object.__getattr__`{.interpreted-text role="meth"} method, that is called to satisfy the lookup.

::: index
triple: class instance; attribute; assignment
:::

Attribute assignments and deletions update the instance\'s dictionary, never a class\'s dictionary. If the class has a `~object.__setattr__`{.interpreted-text role="meth"} or `~object.__delattr__`{.interpreted-text role="meth"} method, this is called instead of updating the instance dictionary directly.

::: index
pair: object; numeric pair: object; sequence pair: object; mapping
:::

Class instances can pretend to be numbers, sequences, or mappings if they have methods with certain special names. See section `specialnames`{.interpreted-text role="ref"}.

#### Special attributes

::: index
single: \_\_dict\_\_ (instance attribute) single: \_\_class\_\_ (instance attribute)
:::

::: attribute
object.\_\_class\_\_

The class to which a class instance belongs.
:::

::: attribute
object.\_\_dict\_\_

A dictionary or other mapping object used to store an object\'s (writable) attributes. Not all instances have a `!__dict__`{.interpreted-text role="attr"} attribute; see the section on `slots`{.interpreted-text role="ref"} for more details.
:::

### I/O objects (also known as file objects)

::: index
pair: built-in function; open pair: module; io single: popen() (in module os) single: makefile() (socket method) single: sys.stdin single: sys.stdout single: sys.stderr single: stdio single: stdin (in module sys) single: stdout (in module sys) single: stderr (in module sys)
:::

A `file object`{.interpreted-text role="term"} represents an open file. Various shortcuts are available to create file objects: the `open`{.interpreted-text role="func"} built-in function, and also `os.popen`{.interpreted-text role="func"}, `os.fdopen`{.interpreted-text role="func"}, and the `~socket.socket.makefile`{.interpreted-text role="meth"} method of socket objects (and perhaps by other functions or methods provided by extension modules).

The objects `sys.stdin`, `sys.stdout` and `sys.stderr` are initialized to file objects corresponding to the interpreter\'s standard input, output and error streams; they are all open in text mode and therefore follow the interface defined by the `io.TextIOBase`{.interpreted-text role="class"} abstract class.

### Internal types

::: index
single: internal type single: types, internal
:::

A few types used internally by the interpreter are exposed to the user. Their definitions may change with future versions of the interpreter, but they are mentioned here for completeness.

#### Code objects

::: index
bytecode, object; code, code object
:::

Code objects represent *byte-compiled* executable Python code, or `bytecode`{.interpreted-text role="term"}. The difference between a code object and a function object is that the function object contains an explicit reference to the function\'s globals (the module in which it was defined), while a code object contains no context; also the default argument values are stored in the function object, not in the code object (because they represent values calculated at run-time). Unlike function objects, code objects are immutable and contain no references (directly or indirectly) to mutable objects.

::: index
single: co_argcount (code object attribute) single: co_posonlyargcount (code object attribute) single: co_kwonlyargcount (code object attribute) single: co_code (code object attribute) single: co_consts (code object attribute) single: co_filename (code object attribute) single: co_firstlineno (code object attribute) single: co_flags (code object attribute) single: co_lnotab (code object attribute) single: co_name (code object attribute) single: co_names (code object attribute) single: co_nlocals (code object attribute) single: co_stacksize (code object attribute) single: co_varnames (code object attribute) single: co_cellvars (code object attribute) single: co_freevars (code object attribute) single: co_qualname (code object attribute)
:::

##### Special read-only attributes

+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | The function name                                                                                                                                                                                                                                                                                 |
| codeobject.co_name            |                                                                                                                                                                                                                                                                                                   |
| :::                           |                                                                                                                                                                                                                                                                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | The fully qualified function name                                                                                                                                                                                                                                                                 |
| codeobject.co_qualname        |                                                                                                                                                                                                                                                                                                   |
| :::                           | ::: versionadded                                                                                                                                                                                                                                                                                  |
|                               | 3.11                                                                                                                                                                                                                                                                                              |
|                               | :::                                                                                                                                                                                                                                                                                               |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | The total number of positional `parameters <parameter>`{.interpreted-text role="term"} (including positional-only parameters and parameters with default values) that the function has                                                                                                            |
| codeobject.co_argcount        |                                                                                                                                                                                                                                                                                                   |
| :::                           |                                                                                                                                                                                                                                                                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | The number of positional-only `parameters <parameter>`{.interpreted-text role="term"} (including arguments with default values) that the function has                                                                                                                                             |
| codeobject.co_posonlyargcount |                                                                                                                                                                                                                                                                                                   |
| :::                           |                                                                                                                                                                                                                                                                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | The number of keyword-only `parameters <parameter>`{.interpreted-text role="term"} (including arguments with default values) that the function has                                                                                                                                                |
| codeobject.co_kwonlyargcount  |                                                                                                                                                                                                                                                                                                   |
| :::                           |                                                                                                                                                                                                                                                                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | The number of `local variables <naming>`{.interpreted-text role="ref"} used by the function (including parameters)                                                                                                                                                                                |
| codeobject.co_nlocals         |                                                                                                                                                                                                                                                                                                   |
| :::                           |                                                                                                                                                                                                                                                                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | A `tuple`{.interpreted-text role="class"} containing the names of the local variables in the function (starting with the parameter names)                                                                                                                                                         |
| codeobject.co_varnames        |                                                                                                                                                                                                                                                                                                   |
| :::                           |                                                                                                                                                                                                                                                                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | A `tuple`{.interpreted-text role="class"} containing the names of `local variables <naming>`{.interpreted-text role="ref"} that are referenced from at least one `nested scope`{.interpreted-text role="term"} inside the function                                                                |
| codeobject.co_cellvars        |                                                                                                                                                                                                                                                                                                   |
| :::                           |                                                                                                                                                                                                                                                                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | A `tuple`{.interpreted-text role="class"} containing the names of `free (closure) variables <closure variable>`{.interpreted-text role="term"} that a `nested scope`{.interpreted-text role="term"} references in an outer scope. See also `function.__closure__`{.interpreted-text role="attr"}. |
| codeobject.co_freevars        |                                                                                                                                                                                                                                                                                                   |
| :::                           | Note: references to global and builtin names are *not* included.                                                                                                                                                                                                                                  |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | A string representing the sequence of `bytecode`{.interpreted-text role="term"} instructions in the function                                                                                                                                                                                      |
| codeobject.co_code            |                                                                                                                                                                                                                                                                                                   |
| :::                           |                                                                                                                                                                                                                                                                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | A `tuple`{.interpreted-text role="class"} containing the literals used by the `bytecode`{.interpreted-text role="term"} in the function                                                                                                                                                           |
| codeobject.co_consts          |                                                                                                                                                                                                                                                                                                   |
| :::                           |                                                                                                                                                                                                                                                                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | A `tuple`{.interpreted-text role="class"} containing the names used by the `bytecode`{.interpreted-text role="term"} in the function                                                                                                                                                              |
| codeobject.co_names           |                                                                                                                                                                                                                                                                                                   |
| :::                           |                                                                                                                                                                                                                                                                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | The name of the file from which the code was compiled                                                                                                                                                                                                                                             |
| codeobject.co_filename        |                                                                                                                                                                                                                                                                                                   |
| :::                           |                                                                                                                                                                                                                                                                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | The line number of the first line of the function                                                                                                                                                                                                                                                 |
| codeobject.co_firstlineno     |                                                                                                                                                                                                                                                                                                   |
| :::                           |                                                                                                                                                                                                                                                                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | A string encoding the mapping from `bytecode`{.interpreted-text role="term"} offsets to line numbers. For details, see the source code of the interpreter.                                                                                                                                        |
| codeobject.co_lnotab          |                                                                                                                                                                                                                                                                                                   |
| :::                           | ::: deprecated                                                                                                                                                                                                                                                                                    |
|                               | 3.12 This attribute of code objects is deprecated, and may be removed in Python 3.15.                                                                                                                                                                                                             |
|                               | :::                                                                                                                                                                                                                                                                                               |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | The required stack size of the code object                                                                                                                                                                                                                                                        |
| codeobject.co_stacksize       |                                                                                                                                                                                                                                                                                                   |
| :::                           |                                                                                                                                                                                                                                                                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                 | An `integer <int>`{.interpreted-text role="class"} encoding a number of flags for the interpreter.                                                                                                                                                                                                |
| codeobject.co_flags           |                                                                                                                                                                                                                                                                                                   |
| :::                           |                                                                                                                                                                                                                                                                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

::: index
pair: object; generator
:::

The following flag bits are defined for `~codeobject.co_flags`{.interpreted-text role="attr"}: bit `0x04` is set if the function uses the `*arguments` syntax to accept an arbitrary number of positional arguments; bit `0x08` is set if the function uses the `**keywords` syntax to accept arbitrary keyword arguments; bit `0x20` is set if the function is a generator. See `inspect-module-co-flags`{.interpreted-text role="ref"} for details on the semantics of each flags that might be present.

Future feature declarations (for example, `from __future__ import division`) also use bits in `~codeobject.co_flags`{.interpreted-text role="attr"} to indicate whether a code object was compiled with a particular feature enabled. See `~__future__._Feature.compiler_flag`{.interpreted-text role="attr"}.

Other bits in `~codeobject.co_flags`{.interpreted-text role="attr"} are reserved for internal use.

::: index
single: documentation string
:::

If a code object represents a function and has a docstring, the `~inspect.CO_HAS_DOCSTRING`{.interpreted-text role="data"} bit is set in `~codeobject.co_flags`{.interpreted-text role="attr"} and the first item in `~codeobject.co_consts`{.interpreted-text role="attr"} is the docstring of the function.

##### Methods on code objects

:::::: method
codeobject.co_positions()

Returns an iterable over the source code positions of each `bytecode`{.interpreted-text role="term"} instruction in the code object.

The iterator returns `tuple`{.interpreted-text role="class"}s containing the `(start_line, end_line, start_column, end_column)`. The *i-th* tuple corresponds to the position of the source code that compiled to the *i-th* code unit. Column information is 0-indexed utf-8 byte offsets on the given source line.

This positional information can be missing. A non-exhaustive lists of cases where this may happen:

- Running the interpreter with `-X`{.interpreted-text role="option"} `no_debug_ranges`.
- Loading a pyc file compiled while using `-X`{.interpreted-text role="option"} `no_debug_ranges`.
- Position tuples corresponding to artificial instructions.
- Line and column numbers that can\'t be represented due to implementation specific limitations.

When this occurs, some or all of the tuple elements can be `None`{.interpreted-text role="const"}.

::: versionadded
3.11
:::

:::: note
::: title
Note
:::

This feature requires storing column positions in code objects which may result in a small increase of disk usage of compiled Python files or interpreter memory usage. To avoid storing the extra information and/or deactivate printing the extra traceback information, the `-X`{.interpreted-text role="option"} `no_debug_ranges` command line flag or the `PYTHONNODEBUGRANGES`{.interpreted-text role="envvar"} environment variable can be used.
::::
::::::

::::: method
codeobject.co_lines()

Returns an iterator that yields information about successive ranges of `bytecode`{.interpreted-text role="term"}s. Each item yielded is a `(start, end, lineno)` `tuple`{.interpreted-text role="class"}:

- `start` (an `int`{.interpreted-text role="class"}) represents the offset (inclusive) of the start of the `bytecode`{.interpreted-text role="term"} range
- `end` (an `int`{.interpreted-text role="class"}) represents the offset (exclusive) of the end of the `bytecode`{.interpreted-text role="term"} range
- `lineno` is an `int`{.interpreted-text role="class"} representing the line number of the `bytecode`{.interpreted-text role="term"} range, or `None` if the bytecodes in the given range have no line number

The items yielded will have the following properties:

- The first range yielded will have a `start` of 0.
- The `(start, end)` ranges will be non-decreasing and consecutive. That is, for any pair of `tuple`{.interpreted-text role="class"}s, the `start` of the second will be equal to the `end` of the first.
- No range will be backwards: `end >= start` for all triples.
- The last `tuple`{.interpreted-text role="class"} yielded will have `end` equal to the size of the `bytecode`{.interpreted-text role="term"}.

Zero-width ranges, where `start == end`, are allowed. Zero-width ranges are used for lines that are present in the source code, but have been eliminated by the `bytecode`{.interpreted-text role="term"} compiler.

::: versionadded
3.10
:::

::: seealso

`626`{.interpreted-text role="pep"} - Precise line numbers for debugging and other tools.

:   The PEP that introduced the `!co_lines`{.interpreted-text role="meth"} method.
:::
:::::

:::: method
codeobject.replace(\*\*kwargs)

Return a copy of the code object with new values for the specified fields.

Code objects are also supported by the generic function `copy.replace`{.interpreted-text role="func"}.

::: versionadded
3.8
:::
::::

#### Frame objects

::: index
pair: object; frame
:::

Frame objects represent execution frames. They may occur in `traceback objects <traceback-objects>`{.interpreted-text role="ref"}, and are also passed to registered trace functions.

::: index
single: f_back (frame attribute) single: f_code (frame attribute) single: f_globals (frame attribute) single: f_locals (frame attribute) single: f_lasti (frame attribute) single: f_builtins (frame attribute) single: f_generator (frame attribute)
:::

##### Special read-only attributes

+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute     | Points to the previous stack frame (towards the caller), or `None` if this is the bottom stack frame                                                                                                                                                |
| frame.f_back      |                                                                                                                                                                                                                                                     |
| :::               |                                                                                                                                                                                                                                                     |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute     | The `code object <code-objects>`{.interpreted-text role="ref"} being executed in this frame. Accessing this attribute raises an `auditing event <auditing>`{.interpreted-text role="ref"} `object.__getattr__` with arguments `obj` and `"f_code"`. |
| frame.f_code      |                                                                                                                                                                                                                                                     |
| :::               |                                                                                                                                                                                                                                                     |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute     | The mapping used by the frame to look up `local variables <naming>`{.interpreted-text role="ref"}. If the frame refers to an `optimized scope`{.interpreted-text role="term"}, this may return a write-through proxy object.                        |
| frame.f_locals    |                                                                                                                                                                                                                                                     |
| :::               | ::: versionchanged                                                                                                                                                                                                                                  |
|                   | 3.13 Return a proxy for optimized scopes.                                                                                                                                                                                                           |
|                   | :::                                                                                                                                                                                                                                                 |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute     | The dictionary used by the frame to look up `global variables <naming>`{.interpreted-text role="ref"}                                                                                                                                               |
| frame.f_globals   |                                                                                                                                                                                                                                                     |
| :::               |                                                                                                                                                                                                                                                     |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute     | The dictionary used by the frame to look up `built-in (intrinsic) names <naming>`{.interpreted-text role="ref"}                                                                                                                                     |
| frame.f_builtins  |                                                                                                                                                                                                                                                     |
| :::               |                                                                                                                                                                                                                                                     |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute     | The \"precise instruction\" of the frame object (this is an index into the `bytecode`{.interpreted-text role="term"} string of the `code object <code-objects>`{.interpreted-text role="ref"})                                                      |
| frame.f_lasti     |                                                                                                                                                                                                                                                     |
| :::               |                                                                                                                                                                                                                                                     |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute     | The `generator`{.interpreted-text role="term"} or `coroutine`{.interpreted-text role="term"} object that owns this frame, or `None` if the frame is a normal function.                                                                              |
| frame.f_generator |                                                                                                                                                                                                                                                     |
| :::               | ::: versionadded                                                                                                                                                                                                                                    |
|                   | 3.14                                                                                                                                                                                                                                                |
|                   | :::                                                                                                                                                                                                                                                 |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

::: index
single: f_trace (frame attribute) single: f_trace_lines (frame attribute) single: f_trace_opcodes (frame attribute) single: f_lineno (frame attribute)
:::

##### Special writable attributes

+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | If not `None`, this is a function called for various events during code execution (this is used by debuggers). Normally an event is triggered for each new source line (see `~frame.f_trace_lines`{.interpreted-text role="attr"}).                 |
| frame.f_trace         |                                                                                                                                                                                                                                                     |
| :::                   |                                                                                                                                                                                                                                                     |
+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | Set this attribute to `False`{.interpreted-text role="const"} to disable triggering a tracing event for each source line.                                                                                                                           |
| frame.f_trace_lines   |                                                                                                                                                                                                                                                     |
| :::                   |                                                                                                                                                                                                                                                     |
+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | Set this attribute to `True`{.interpreted-text role="const"} to allow per-opcode events to be requested. Note that this may lead to undefined interpreter behaviour if exceptions raised by the trace function escape to the function being traced. |
| frame.f_trace_opcodes |                                                                                                                                                                                                                                                     |
| :::                   |                                                                                                                                                                                                                                                     |
+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | The current line number of the frame \-- writing to this from within a trace function jumps to the given line (only for the bottom-most frame). A debugger can implement a Jump command (aka Set Next Statement) by writing to this attribute.      |
| frame.f_lineno        |                                                                                                                                                                                                                                                     |
| :::                   |                                                                                                                                                                                                                                                     |
+-----------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

##### Frame object methods

Frame objects support one method:

::::: method
frame.clear()

This method clears all references to `local variables <naming>`{.interpreted-text role="ref"} held by the frame. Also, if the frame belonged to a `generator`{.interpreted-text role="term"}, the generator is finalized. This helps break reference cycles involving frame objects (for example when catching an `exception <bltin-exceptions>`{.interpreted-text role="ref"} and storing its `traceback <traceback-objects>`{.interpreted-text role="ref"} for later use).

`RuntimeError`{.interpreted-text role="exc"} is raised if the frame is currently executing or suspended.

::: versionadded
3.4
:::

::: versionchanged
3.13 Attempting to clear a suspended frame raises `RuntimeError`{.interpreted-text role="exc"} (as has always been the case for executing frames).
:::
:::::

#### Traceback objects

::: index
pair: object; traceback pair: stack; trace pair: exception; handler pair: execution; stack single: exc_info (in module sys) single: last_traceback (in module sys) single: sys.exc_info single: sys.exception single: sys.last_traceback
:::

Traceback objects represent the stack trace of an `exception <tut-errors>`{.interpreted-text role="ref"}. A traceback object is implicitly created when an exception occurs, and may also be explicitly created by calling `types.TracebackType`{.interpreted-text role="class"}.

::: versionchanged
3.7 Traceback objects can now be explicitly instantiated from Python code.
:::

For implicitly created tracebacks, when the search for an exception handler unwinds the execution stack, at each unwound level a traceback object is inserted in front of the current traceback. When an exception handler is entered, the stack trace is made available to the program. (See section `try`{.interpreted-text role="ref"}.) It is accessible as the third item of the tuple returned by `sys.exc_info`{.interpreted-text role="func"}, and as the `~BaseException.__traceback__`{.interpreted-text role="attr"} attribute of the caught exception.

When the program contains no suitable handler, the stack trace is written (nicely formatted) to the standard error stream; if the interpreter is interactive, it is also made available to the user as `sys.last_traceback`{.interpreted-text role="data"}.

For explicitly created tracebacks, it is up to the creator of the traceback to determine how the `~traceback.tb_next`{.interpreted-text role="attr"} attributes should be linked to form a full stack trace.

::: index
single: tb_frame (traceback attribute) single: tb_lineno (traceback attribute) single: tb_lasti (traceback attribute) pair: statement; try
:::

Special read-only attributes:

+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute       | Points to the execution `frame <frame-objects>`{.interpreted-text role="ref"} of the current level.                                                      |
| traceback.tb_frame  |                                                                                                                                                          |
| :::                 | Accessing this attribute raises an `auditing event <auditing>`{.interpreted-text role="ref"} `object.__getattr__` with arguments `obj` and `"tb_frame"`. |
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute       | Gives the line number where the exception occurred                                                                                                       |
| traceback.tb_lineno |                                                                                                                                                          |
| :::                 |                                                                                                                                                          |
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute       | Indicates the \"precise instruction\".                                                                                                                   |
| traceback.tb_lasti  |                                                                                                                                                          |
| :::                 |                                                                                                                                                          |
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------+

The line number and last instruction in the traceback may differ from the line number of its `frame object <frame-objects>`{.interpreted-text role="ref"} if the exception occurred in a `try`{.interpreted-text role="keyword"} statement with no matching except clause or with a `finally`{.interpreted-text role="keyword"} clause.

::: index
single: tb_next (traceback attribute)
:::

:::: attribute
traceback.tb_next

The special writable attribute `!tb_next`{.interpreted-text role="attr"} is the next level in the stack trace (towards the frame where the exception occurred), or `None` if there is no next level.

::: versionchanged
3.7 This attribute is now writable
:::
::::

#### Slice objects

::: index
pair: built-in function; slice
:::

Slice objects are used to represent slices for `~object.__getitem__`{.interpreted-text role="meth"} methods. They are also created by the built-in `slice`{.interpreted-text role="func"} function.

::: versionadded
3.15

The `slice`{.interpreted-text role="func"} type now supports `subscription <subscriptions>`{.interpreted-text role="ref"}. For example, `slice[float]` may be used in type annotations to indicate a slice containing `float`{.interpreted-text role="type"} objects.
:::

::: index
single: start (slice object attribute) single: stop (slice object attribute) single: step (slice object attribute)
:::

Special read-only attributes: `~slice.start`{.interpreted-text role="attr"} is the lower bound; `~slice.stop`{.interpreted-text role="attr"} is the upper bound; `~slice.step`{.interpreted-text role="attr"} is the step value; each is `None` if omitted. These attributes can have any type.

Slice objects support one method:

::: method
slice.indices(self, length)

This method takes a single integer argument *length* and computes information about the slice that the slice object would describe if applied to a sequence of *length* items. It returns a tuple of three integers; respectively these are the *start* and *stop* indices and the *step* or stride length of the slice. Missing or out-of-bounds indices are handled in a manner consistent with regular slices.
:::

#### Static method objects

Static method objects provide a way of defeating the transformation of function objects to method objects described above. A static method object is a wrapper around any other object, usually a user-defined method object. When a static method object is retrieved from a class or a class instance, the object actually returned is the wrapped object, which is not subject to any further transformation. Static method objects are also callable. Static method objects are created by the built-in `staticmethod`{.interpreted-text role="func"} constructor.

#### Class method objects

A class method object, like a static method object, is a wrapper around another object that alters the way in which that object is retrieved from classes and class instances. The behaviour of class method objects upon such retrieval is described above, under `"instance methods" <instance-methods>`{.interpreted-text role="ref"}. Class method objects are created by the built-in `classmethod`{.interpreted-text role="func"} constructor.

## Special method names {#specialnames}

::: index
pair: operator; overloading single: \_\_getitem\_\_() (mapping object method)
:::

A class can implement certain operations that are invoked by special syntax (such as arithmetic operations or subscripting and slicing) by defining methods with special names. This is Python\'s approach to `operator overloading`{.interpreted-text role="dfn"}, allowing classes to define their own behavior with respect to language operators. For instance, if a class defines a method named `~object.__getitem__`{.interpreted-text role="meth"}, and `x` is an instance of this class, then `x[i]` is roughly equivalent to `type(x).__getitem__(x, i)`. Except where mentioned, attempts to execute an operation raise an exception when no appropriate method is defined (typically `AttributeError`{.interpreted-text role="exc"} or `TypeError`{.interpreted-text role="exc"}).

Setting a special method to `None` indicates that the corresponding operation is not available. For example, if a class sets `~object.__iter__`{.interpreted-text role="meth"} to `None`, the class is not iterable, so calling `iter`{.interpreted-text role="func"} on its instances will raise a `TypeError`{.interpreted-text role="exc"} (without falling back to `~object.__getitem__`{.interpreted-text role="meth"}).[^2]

When implementing a class that emulates any built-in type, it is important that the emulation only be implemented to the degree that it makes sense for the object being modelled. For example, some sequences may work well with retrieval of individual elements, but extracting a slice may not make sense. (One example of this is the `NodeList <dom-nodelist-objects>`{.interpreted-text role="ref"} interface in the W3C\'s Document Object Model.)

### Basic customization {#customization}

:::: method
object.\_\_new\_\_(cls\[, \...\])

::: index
pair: subclassing; immutable types
:::

Called to create a new instance of class *cls*. `__new__`{.interpreted-text role="meth"} is a static method (special-cased so you need not declare it as such) that takes the class of which an instance was requested as its first argument. The remaining arguments are those passed to the object constructor expression (the call to the class). The return value of `__new__`{.interpreted-text role="meth"} should be the new object instance (usually an instance of *cls*).

Typical implementations create a new instance of the class by invoking the superclass\'s `__new__`{.interpreted-text role="meth"} method using `super().__new__(cls[, ...])` with appropriate arguments and then modifying the newly created instance as necessary before returning it.

If `__new__`{.interpreted-text role="meth"} is invoked during object construction and it returns an instance of *cls*, then the new instance's `__init__`{.interpreted-text role="meth"} method will be invoked like `__init__(self[, ...])`, where *self* is the new instance and the remaining arguments are the same as were passed to the object constructor.

If `__new__`{.interpreted-text role="meth"} does not return an instance of *cls*, then the new instance\'s `__init__`{.interpreted-text role="meth"} method will not be invoked.

`__new__`{.interpreted-text role="meth"} is intended mainly to allow subclasses of immutable types (like int, str, or tuple) to customize instance creation. It is also commonly overridden in custom metaclasses in order to customize class creation.
::::

:::: method
object.\_\_init\_\_(self\[, \...\])

::: index
pair: class; constructor
:::

Called after the instance has been created (by `__new__`{.interpreted-text role="meth"}), but before it is returned to the caller. The arguments are those passed to the class constructor expression. If a base class has an `__init__`{.interpreted-text role="meth"} method, the derived class\'s `__init__`{.interpreted-text role="meth"} method, if any, must explicitly call it to ensure proper initialization of the base class part of the instance; for example: `super().__init__([args...])`.

Because `__new__`{.interpreted-text role="meth"} and `__init__`{.interpreted-text role="meth"} work together in constructing objects (`__new__`{.interpreted-text role="meth"} to create it, and `__init__`{.interpreted-text role="meth"} to customize it), no non-`None` value may be returned by `__init__`{.interpreted-text role="meth"}; doing so will cause a `TypeError`{.interpreted-text role="exc"} to be raised at runtime.
::::

::::::::::: method
object.\_\_del\_\_(self)

::: index
single: destructor single: finalizer pair: statement; del
:::

Called when the instance is about to be destroyed. This is also called a finalizer or (improperly) a destructor. If a base class has a `__del__`{.interpreted-text role="meth"} method, the derived class\'s `__del__`{.interpreted-text role="meth"} method, if any, must explicitly call it to ensure proper deletion of the base class part of the instance.

It is possible (though not recommended!) for the `__del__`{.interpreted-text role="meth"} method to postpone destruction of the instance by creating a new reference to it. This is called object *resurrection*. It is implementation-dependent whether `__del__`{.interpreted-text role="meth"} is called a second time when a resurrected object is about to be destroyed; the current `CPython`{.interpreted-text role="term"} implementation only calls it once.

It is not guaranteed that `__del__`{.interpreted-text role="meth"} methods are called for objects that still exist when the interpreter exits. `weakref.finalize`{.interpreted-text role="class"} provides a straightforward way to register a cleanup function to be called when an object is garbage collected.

:::: note
::: title
Note
:::

`del x` doesn\'t directly call `x.__del__()` \-\-- the former decrements the reference count for `x` by one, and the latter is only called when `x`\'s reference count reaches zero.
::::

:::: impl-detail
It is possible for a reference cycle to prevent the reference count of an object from going to zero. In this case, the cycle will be later detected and deleted by the `cyclic garbage collector
<garbage collection>`{.interpreted-text role="term"}. A common cause of reference cycles is when an exception has been caught in a local variable. The frame\'s locals then reference the exception, which references its own traceback, which references the locals of all frames caught in the traceback.

::: seealso
Documentation for the `gc`{.interpreted-text role="mod"} module.
:::
::::

:::: warning
::: title
Warning
:::

Due to the precarious circumstances under which `__del__`{.interpreted-text role="meth"} methods are invoked, exceptions that occur during their execution are ignored, and a warning is printed to `sys.stderr` instead. In particular:

- `__del__`{.interpreted-text role="meth"} can be invoked when arbitrary code is being executed, including from any arbitrary thread. If `__del__`{.interpreted-text role="meth"} needs to take a lock or invoke any other blocking resource, it may deadlock as the resource may already be taken by the code that gets interrupted to execute `__del__`{.interpreted-text role="meth"}.
- `__del__`{.interpreted-text role="meth"} can be executed during interpreter shutdown. As a consequence, the global variables it needs to access (including other modules) may already have been deleted or set to `None`. Python guarantees that globals whose name begins with a single underscore are deleted from their module before other globals are deleted; if no other references to such globals exist, this may help in assuring that imported modules are still available at the time when the `__del__`{.interpreted-text role="meth"} method is called.
::::

::: index
single: repr() (built-in function); \_\_repr\_\_() (object method)
:::
:::::::::::

:::: method
object.\_\_repr\_\_(self)

Called by the `repr`{.interpreted-text role="func"} built-in function to compute the \"official\" string representation of an object. If at all possible, this should look like a valid Python expression that could be used to recreate an object with the same value (given an appropriate environment). If this is not possible, a string of the form `<...some useful description...>` should be returned. The return value must be a string object. If a class defines `__repr__`{.interpreted-text role="meth"} but not `__str__`{.interpreted-text role="meth"}, then `__repr__`{.interpreted-text role="meth"} is also used when an \"informal\" string representation of instances of that class is required.

This is typically used for debugging, so it is important that the representation is information-rich and unambiguous. A default implementation is provided by the `object`{.interpreted-text role="class"} class itself.

::: index
single: string; \_\_str\_\_() (object method) single: format() (built-in function); \_\_str\_\_() (object method) single: print() (built-in function); \_\_str\_\_() (object method)
:::
::::

::: method
object.\_\_str\_\_(self)

Called by `str(object) <str>`{.interpreted-text role="func"}, the default `__format__`{.interpreted-text role="meth"} implementation, and the built-in function `print`{.interpreted-text role="func"}, to compute the \"informal\" or nicely printable string representation of an object. The return value must be a `str <textseq>`{.interpreted-text role="ref"} object.

This method differs from `object.__repr__`{.interpreted-text role="meth"} in that there is no expectation that `__str__`{.interpreted-text role="meth"} return a valid Python expression: a more convenient or concise representation can be used.

The default implementation defined by the built-in type `object`{.interpreted-text role="class"} calls `object.__repr__`{.interpreted-text role="meth"}.
:::

::::: method
object.\_\_bytes\_\_(self)

::: index
pair: built-in function; bytes
:::

Called by `bytes <func-bytes>`{.interpreted-text role="ref"} to compute a byte-string representation of an object. This should return a `bytes`{.interpreted-text role="class"} object. The `object`{.interpreted-text role="class"} class itself does not provide this method.

::: index
single: string; \_\_format\_\_() (object method) pair: string; conversion pair: built-in function; print
:::
:::::

::::: method
object.\_\_format\_\_(self, format_spec)

Called by the `format`{.interpreted-text role="func"} built-in function, and by extension, evaluation of `formatted string literals
<f-strings>`{.interpreted-text role="ref"} and the `str.format`{.interpreted-text role="meth"} method, to produce a \"formatted\" string representation of an object. The *format_spec* argument is a string that contains a description of the formatting options desired. The interpretation of the *format_spec* argument is up to the type implementing `__format__`{.interpreted-text role="meth"}, however most classes will either delegate formatting to one of the built-in types, or use a similar formatting option syntax.

See `formatspec`{.interpreted-text role="ref"} for a description of the standard formatting syntax.

The return value must be a string object.

The default implementation by the `object`{.interpreted-text role="class"} class should be given an empty *format_spec* string. It delegates to `__str__`{.interpreted-text role="meth"}.

::: versionchanged
3.4 The \_\_format\_\_ method of `object` itself raises a `TypeError`{.interpreted-text role="exc"} if passed any non-empty string.
:::

::: versionchanged
3.7 `object.__format__(x, '')` is now equivalent to `str(x)` rather than `format(str(x), '')`.
:::
:::::

> ::: index
> single: comparisons
> :::
>
> These are the so-called \"rich comparison\" methods. The correspondence between operator symbols and method names is as follows: `x<y` calls `x.__lt__(y)`, `x<=y` calls `x.__le__(y)`, `x==y` calls `x.__eq__(y)`, `x!=y` calls `x.__ne__(y)`, `x>y` calls `x.__gt__(y)`, and `x>=y` calls `x.__ge__(y)`.
>
> A rich comparison method may return the singleton `NotImplemented`{.interpreted-text role="data"} if it does not implement the operation for a given pair of arguments. By convention, `False` and `True` are returned for a successful comparison. However, these methods can return any value, so if the comparison operator is used in a Boolean context (e.g., in the condition of an `if` statement), Python will call `bool`{.interpreted-text role="func"} on the value to determine if the result is true or false.
>
> By default, `object` implements `__eq__`{.interpreted-text role="meth"} by using `is`, returning `NotImplemented`{.interpreted-text role="data"} in the case of a false comparison: `True if x is y else NotImplemented`. For `__ne__`{.interpreted-text role="meth"}, by default it delegates to `__eq__`{.interpreted-text role="meth"} and inverts the result unless it is `!NotImplemented`{.interpreted-text role="data"}. There are no other implied relationships among the comparison operators or default implementations; for example, the truth of `(x<y or x==y)` does not imply `x<=y`. To automatically generate ordering operations from a single root operation, see `functools.total_ordering`{.interpreted-text role="func"}.
>
> By default, the `object`{.interpreted-text role="class"} class provides implementations consistent with `expressions-value-comparisons`{.interpreted-text role="ref"}: equality compares according to object identity, and order comparisons raise `TypeError`{.interpreted-text role="exc"}. Each default method may generate these results directly, but may also return `NotImplemented`{.interpreted-text role="data"}.
>
> See the paragraph on `__hash__`{.interpreted-text role="meth"} for some important notes on creating `hashable`{.interpreted-text role="term"} objects which support custom comparison operations and are usable as dictionary keys.
>
> There are no swapped-argument versions of these methods (to be used when the left argument does not support the operation but the right argument does); rather, `__lt__`{.interpreted-text role="meth"} and `__gt__`{.interpreted-text role="meth"} are each other\'s reflection, `__le__`{.interpreted-text role="meth"} and `__ge__`{.interpreted-text role="meth"} are each other\'s reflection, and `__eq__`{.interpreted-text role="meth"} and `__ne__`{.interpreted-text role="meth"} are their own reflection. If the operands are of different types, and the right operand\'s type is a direct or indirect subclass of the left operand\'s type, the reflected method of the right operand has priority, otherwise the left operand\'s method has priority. Virtual subclassing is not considered.
>
> When no appropriate method returns any value other than `NotImplemented`{.interpreted-text role="data"}, the `==` and `!=` operators will fall back to `is` and `is not`, respectively.

::::::::: method
object.\_\_hash\_\_(self)

::: index
pair: object; dictionary pair: built-in function; hash
:::

Called by built-in function `hash`{.interpreted-text role="func"} and for operations on members of hashed collections including `set`{.interpreted-text role="class"}, `frozenset`{.interpreted-text role="class"}, and `dict`{.interpreted-text role="class"}. The `__hash__()` method should return an integer. The only required property is that objects which compare equal have the same hash value; it is advised to mix together the hash values of the components of the object that also play a part in comparison of objects by packing them into a tuple and hashing the tuple. Example:

    def __hash__(self):
        return hash((self.name, self.nick, self.color))

:::: note
::: title
Note
:::

`hash`{.interpreted-text role="func"} truncates the value returned from an object\'s custom `__hash__`{.interpreted-text role="meth"} method to the size of a `Py_ssize_t`{.interpreted-text role="c:type"}. This is typically 8 bytes on 64-bit builds and 4 bytes on 32-bit builds. If an object\'s `__hash__`{.interpreted-text role="meth"} must interoperate on builds of different bit sizes, be sure to check the width on all supported builds. An easy way to do this is with `python -c "import sys; print(sys.hash_info.width)"`.
::::

If a class does not define an `__eq__`{.interpreted-text role="meth"} method it should not define a `__hash__`{.interpreted-text role="meth"} operation either; if it defines `__eq__`{.interpreted-text role="meth"} but not `__hash__`{.interpreted-text role="meth"}, its instances will not be usable as items in hashable collections. If a class defines mutable objects and implements an `__eq__`{.interpreted-text role="meth"} method, it should not implement `__hash__`{.interpreted-text role="meth"}, since the implementation of `hashable`{.interpreted-text role="term"} collections requires that a key\'s hash value is immutable (if the object\'s hash value changes, it will be in the wrong hash bucket).

User-defined classes have `__eq__`{.interpreted-text role="meth"} and `__hash__`{.interpreted-text role="meth"} methods by default (inherited from the `object`{.interpreted-text role="class"} class); with them, all objects compare unequal (except with themselves) and `x.__hash__()` returns an appropriate value such that `x == y` implies both that `x is y` and `hash(x) == hash(y)`.

A class that overrides `__eq__`{.interpreted-text role="meth"} and does not define `__hash__`{.interpreted-text role="meth"} will have its `__hash__`{.interpreted-text role="meth"} implicitly set to `None`. When the `__hash__`{.interpreted-text role="meth"} method of a class is `None`, instances of the class will raise an appropriate `TypeError`{.interpreted-text role="exc"} when a program attempts to retrieve their hash value, and will also be correctly identified as unhashable when checking `isinstance(obj, collections.abc.Hashable)`.

If a class that overrides `__eq__`{.interpreted-text role="meth"} needs to retain the implementation of `__hash__`{.interpreted-text role="meth"} from a parent class, the interpreter must be told this explicitly by setting `__hash__ = <ParentClass>.__hash__`.

If a class that does not override `__eq__`{.interpreted-text role="meth"} wishes to suppress hash support, it should include `__hash__ = None` in the class definition. A class which defines its own `__hash__`{.interpreted-text role="meth"} that explicitly raises a `TypeError`{.interpreted-text role="exc"} would be incorrectly identified as hashable by an `isinstance(obj, collections.abc.Hashable)` call.

:::: note
::: title
Note
:::

By default, the `__hash__`{.interpreted-text role="meth"} values of str and bytes objects are \"salted\" with an unpredictable random value. Although they remain constant within an individual Python process, they are not predictable between repeated invocations of Python.

This is intended to provide protection against a denial-of-service caused by carefully chosen inputs that exploit the worst case performance of a dict insertion, *O*(*n*^2^) complexity. See <http://ocert.org/advisories/ocert-2011-003.html> for details.

Changing hash values affects the iteration order of sets. Python has never made guarantees about this ordering (and it typically varies between 32-bit and 64-bit builds).

See also `PYTHONHASHSEED`{.interpreted-text role="envvar"}.
::::

::: versionchanged
3.3 Hash randomization is enabled by default.
:::
:::::::::

:::: method
object.\_\_bool\_\_(self)

::: index
single: \_\_len\_\_() (mapping object method)
:::

Called to implement truth value testing and the built-in operation `bool()`; should return `False` or `True`. When this method is not defined, `~object.__len__`{.interpreted-text role="meth"} is called, if it is defined, and the object is considered true if its result is nonzero. If a class defines neither `!__len__`{.interpreted-text role="meth"} nor `!__bool__`{.interpreted-text role="meth"} (which is true of the `object`{.interpreted-text role="class"} class itself), all its instances are considered true.
::::

### Customizing attribute access {#attribute-access}

The following methods can be defined to customize the meaning of attribute access (use of, assignment to, or deletion of `x.name`) for class instances.

::: method
object.\_\_getattr\_\_(self, name)

Called when the default attribute access fails with an `AttributeError`{.interpreted-text role="exc"} (either `__getattribute__`{.interpreted-text role="meth"} raises an `AttributeError`{.interpreted-text role="exc"} because *name* is not an instance attribute or an attribute in the class tree for `self`; or `__get__`{.interpreted-text role="meth"} of a *name* property raises `AttributeError`{.interpreted-text role="exc"}). This method should either return the (computed) attribute value or raise an `AttributeError`{.interpreted-text role="exc"} exception. The `object`{.interpreted-text role="class"} class itself does not provide this method.

Note that if the attribute is found through the normal mechanism, `__getattr__`{.interpreted-text role="meth"} is not called. (This is an intentional asymmetry between `__getattr__`{.interpreted-text role="meth"} and `__setattr__`{.interpreted-text role="meth"}.) This is done both for efficiency reasons and because otherwise `__getattr__`{.interpreted-text role="meth"} would have no way to access other attributes of the instance. Note that at least for instance variables, you can take total control by not inserting any values in the instance attribute dictionary (but instead inserting them in another object). See the `__getattribute__`{.interpreted-text role="meth"} method below for a way to actually get total control over attribute access.
:::

:::::: method
object.\_\_getattribute\_\_(self, name)

Called unconditionally to implement attribute accesses for instances of the class. If the class also defines `__getattr__`{.interpreted-text role="meth"}, the latter will not be called unless `__getattribute__`{.interpreted-text role="meth"} either calls it explicitly or raises an `AttributeError`{.interpreted-text role="exc"}. This method should return the (computed) attribute value or raise an `AttributeError`{.interpreted-text role="exc"} exception. In order to avoid infinite recursion in this method, its implementation should always call the base class method with the same name to access any attributes it needs, for example, `object.__getattribute__(self, name)`.

:::: note
::: title
Note
:::

This method may still be bypassed when looking up special methods as the result of implicit invocation via language syntax or `built-in functions <builtin-functions>`{.interpreted-text role="ref"}. See `special-lookup`{.interpreted-text role="ref"}.
::::

::: audit-event
object.\_\_getattr\_\_ obj,name object.\_\_getattribute\_\_

For certain sensitive attribute accesses, raises an `auditing event <auditing>`{.interpreted-text role="ref"} `object.__getattr__` with arguments `obj` and `name`.
:::
::::::

:::: method
object.\_\_setattr\_\_(self, name, value)

Called when an attribute assignment is attempted. This is called instead of the normal mechanism (i.e. store the value in the instance dictionary). *name* is the attribute name, *value* is the value to be assigned to it.

If `__setattr__`{.interpreted-text role="meth"} wants to assign to an instance attribute, it should call the base class method with the same name, for example, `object.__setattr__(self, name, value)`.

::: audit-event
object.\_\_setattr\_\_ obj,name,value object.\_\_setattr\_\_

For certain sensitive attribute assignments, raises an `auditing event <auditing>`{.interpreted-text role="ref"} `object.__setattr__` with arguments `obj`, `name`, `value`.
:::
::::

:::: method
object.\_\_delattr\_\_(self, name)

Like `__setattr__`{.interpreted-text role="meth"} but for attribute deletion instead of assignment. This should only be implemented if `del obj.name` is meaningful for the object.

::: audit-event
object.\_\_delattr\_\_ obj,name object.\_\_delattr\_\_

For certain sensitive attribute deletions, raises an `auditing event <auditing>`{.interpreted-text role="ref"} `object.__delattr__` with arguments `obj` and `name`.
:::
::::

::: method
object.\_\_dir\_\_(self)

Called when `dir`{.interpreted-text role="func"} is called on the object. An iterable must be returned. `dir`{.interpreted-text role="func"} converts the returned iterable to a list and sorts it.
:::

#### Customizing module attribute access

::: index
single: \_\_getattr\_\_ (module attribute) single: \_\_dir\_\_ (module attribute) single: \_\_class\_\_ (module attribute)
:::

::: method
module.\_\_getattr\_\_ module.\_\_dir\_\_
:::

Special names `__getattr__` and `__dir__` can be also used to customize access to module attributes. The `__getattr__` function at the module level should accept one argument which is the name of an attribute and return the computed value or raise an `AttributeError`{.interpreted-text role="exc"}. If an attribute is not found on a module object through the normal lookup, i.e. `object.__getattribute__`{.interpreted-text role="meth"}, then `__getattr__` is searched in the module `__dict__` before raising an `AttributeError`{.interpreted-text role="exc"}. If found, it is called with the attribute name and the result is returned.

The `__dir__` function should accept no arguments, and return an iterable of strings that represents the names accessible on module. If present, this function overrides the standard `dir`{.interpreted-text role="func"} search on a module.

::: attribute
module.\_\_class\_\_
:::

For a more fine grained customization of the module behavior (setting attributes, properties, etc.), one can set the `__class__` attribute of a module object to a subclass of `types.ModuleType`{.interpreted-text role="class"}. For example:

    import sys
    from types import ModuleType

    class VerboseModule(ModuleType):
        def __repr__(self):
            return f'Verbose {self.__name__}'

        def __setattr__(self, attr, value):
            print(f'Setting {attr}...')
            super().__setattr__(attr, value)

    sys.modules[__name__].__class__ = VerboseModule

:::: note
::: title
Note
:::

Defining module `__getattr__` and setting module `__class__` only affect lookups made using the attribute access syntax \-- directly accessing the module globals (whether by code within the module, or via a reference to the module\'s globals dictionary) is unaffected.
::::

::: versionchanged
3.5 `__class__` module attribute is now writable.
:::

::: versionadded
3.7 `__getattr__` and `__dir__` module attributes.
:::

::: seealso

`562`{.interpreted-text role="pep"} - Module \_\_getattr\_\_ and \_\_dir\_\_

:   Describes the `__getattr__` and `__dir__` functions on modules.
:::

#### Implementing Descriptors {#descriptors}

The following methods only apply when an instance of the class containing the method (a so-called *descriptor* class) appears in an *owner* class (the descriptor must be in either the owner\'s class dictionary or in the class dictionary for one of its parents). In the examples below, \"the attribute\" refers to the attribute whose name is the key of the property in the owner class\' `~object.__dict__`{.interpreted-text role="attr"}. The `object`{.interpreted-text role="class"} class itself does not implement any of these protocols.

::: method
object.\_\_get\_\_(self, instance, owner=None)

Called to get the attribute of the owner class (class attribute access) or of an instance of that class (instance attribute access). The optional *owner* argument is the owner class, while *instance* is the instance that the attribute was accessed through, or `None` when the attribute is accessed through the *owner*.

This method should return the computed attribute value or raise an `AttributeError`{.interpreted-text role="exc"} exception.

[PEP 252](http://www.python.org/dev/peps/pep-0252/ "PEP 252") specifies that `__get__`{.interpreted-text role="meth"} is callable with one or two arguments. Python\'s own built-in descriptors support this specification; however, it is likely that some third-party tools have descriptors that require both arguments. Python\'s own `__getattribute__`{.interpreted-text role="meth"} implementation always passes in both arguments whether they are required or not.
:::

::: method
object.\_\_set\_\_(self, instance, value)

Called to set the attribute on an instance *instance* of the owner class to a new value, *value*.

Note, adding `__set__`{.interpreted-text role="meth"} or `__delete__`{.interpreted-text role="meth"} changes the kind of descriptor to a \"data descriptor\". See `descriptor-invocation`{.interpreted-text role="ref"} for more details.
:::

::: method
object.\_\_delete\_\_(self, instance)

Called to delete the attribute on an instance *instance* of the owner class.
:::

Instances of descriptors may also have the `!__objclass__`{.interpreted-text role="attr"} attribute present:

::: attribute
object.\_\_objclass\_\_

The attribute `!__objclass__`{.interpreted-text role="attr"} is interpreted by the `inspect`{.interpreted-text role="mod"} module as specifying the class where this object was defined (setting this appropriately can assist in runtime introspection of dynamic class attributes). For callables, it may indicate that an instance of the given type (or a subclass) is expected or required as the first positional argument (for example, CPython sets this attribute for unbound methods that are implemented in C).
:::

#### Invoking Descriptors {#descriptor-invocation}

In general, a descriptor is an object attribute with \"binding behavior\", one whose attribute access has been overridden by methods in the descriptor protocol: `~object.__get__`{.interpreted-text role="meth"}, `~object.__set__`{.interpreted-text role="meth"}, and `~object.__delete__`{.interpreted-text role="meth"}. If any of those methods are defined for an object, it is said to be a descriptor.

The default behavior for attribute access is to get, set, or delete the attribute from an object\'s dictionary. For instance, `a.x` has a lookup chain starting with `a.__dict__['x']`, then `type(a).__dict__['x']`, and continuing through the base classes of `type(a)` excluding metaclasses.

However, if the looked-up value is an object defining one of the descriptor methods, then Python may override the default behavior and invoke the descriptor method instead. Where this occurs in the precedence chain depends on which descriptor methods were defined and how they were called.

The starting point for descriptor invocation is a binding, `a.x`. How the arguments are assembled depends on `a`:

Direct Call

:   The simplest and least common call is when user code directly invokes a descriptor method: `x.__get__(a)`.

Instance Binding

:   If binding to an object instance, `a.x` is transformed into the call: `type(a).__dict__['x'].__get__(a, type(a))`.

Class Binding

:   If binding to a class, `A.x` is transformed into the call: `A.__dict__['x'].__get__(None, A)`.

Super Binding

:   A dotted lookup such as `super(A, a).x` searches `a.__class__.__mro__` for a base class `B` following `A` and then returns `B.__dict__['x'].__get__(a, A)`. If not a descriptor, `x` is returned unchanged.

::: {.testcode hide=""}

class Desc:

:   

    def \_\_get\_\_(\*args):

    :   return args

class B:

> x = Desc()

class A(B):

> x = 999
>
> def m(self):
>
> :   \'Demonstrate these two descriptor invocations are equivalent\' result1 = super(A, self).x result2 = B.\_\_dict\_\_\[\'x\'\].\_\_get\_\_(self, A) return result1 == result2
:::

::: {.doctest hide=""}
\>\>\> a = A() \>\>\> a.\_\_class\_\_.\_\_mro\_\_.index(B) \> a.\_\_class\_\_.\_\_mro\_\_.index(A) True \>\>\> super(A, a).x == B.\_\_dict\_\_\[\'x\'\].\_\_get\_\_(a, A) True \>\>\> a.m() True
:::

For instance bindings, the precedence of descriptor invocation depends on which descriptor methods are defined. A descriptor can define any combination of `~object.__get__`{.interpreted-text role="meth"}, `~object.__set__`{.interpreted-text role="meth"} and `~object.__delete__`{.interpreted-text role="meth"}. If it does not define `!__get__`{.interpreted-text role="meth"}, then accessing the attribute will return the descriptor object itself unless there is a value in the object\'s instance dictionary. If the descriptor defines `!__set__`{.interpreted-text role="meth"} and/or `!__delete__`{.interpreted-text role="meth"}, it is a data descriptor; if it defines neither, it is a non-data descriptor. Normally, data descriptors define both `!__get__`{.interpreted-text role="meth"} and `!__set__`{.interpreted-text role="meth"}, while non-data descriptors have just the `!__get__`{.interpreted-text role="meth"} method. Data descriptors with `!__get__`{.interpreted-text role="meth"} and `!__set__`{.interpreted-text role="meth"} (and/or `!__delete__`{.interpreted-text role="meth"}) defined always override a redefinition in an instance dictionary. In contrast, non-data descriptors can be overridden by instances.

Python methods (including those decorated with `staticmethod`{.interpreted-text role="deco"} and `classmethod`{.interpreted-text role="deco"}) are implemented as non-data descriptors. Accordingly, instances can redefine and override methods. This allows individual instances to acquire behaviors that differ from other instances of the same class.

The `property`{.interpreted-text role="func"} function is implemented as a data descriptor. Accordingly, instances cannot override the behavior of a property.

#### \_\_slots\_\_ {#slots}

*\_\_slots\_\_* allow us to explicitly declare data members (like properties) and deny the creation of `~object.__dict__`{.interpreted-text role="attr"} and *\_\_weakref\_\_* (unless explicitly declared in *\_\_slots\_\_* or available in a parent.)

The space saved over using `~object.__dict__`{.interpreted-text role="attr"} can be significant. Attribute lookup speed can be significantly improved as well.

::: data
object.\_\_slots\_\_

This class variable can be assigned a string, iterable, or sequence of strings with variable names used by instances. *\_\_slots\_\_* reserves space for the declared variables and prevents the automatic creation of `~object.__dict__`{.interpreted-text role="attr"} and *\_\_weakref\_\_* for each instance.
:::

::: {#datamodel-note-slots}
Notes on using *\_\_slots\_\_*:
:::

- When inheriting from a class without *\_\_slots\_\_*, the `~object.__dict__`{.interpreted-text role="attr"} and *\_\_weakref\_\_* attribute of the instances will always be accessible.
- Without a `~object.__dict__`{.interpreted-text role="attr"} variable, instances cannot be assigned new variables not listed in the *\_\_slots\_\_* definition. Attempts to assign to an unlisted variable name raises `AttributeError`{.interpreted-text role="exc"}. If dynamic assignment of new variables is desired, then add `'__dict__'` to the sequence of strings in the *\_\_slots\_\_* declaration.
- Without a *\_\_weakref\_\_* variable for each instance, classes defining *\_\_slots\_\_* do not support `weak references <weakref>`{.interpreted-text role="mod"} to its instances. If weak reference support is needed, then add `'__weakref__'` to the sequence of strings in the *\_\_slots\_\_* declaration.
- *\_\_slots\_\_* are implemented at the class level by creating `descriptors <descriptors>`{.interpreted-text role="ref"} for each variable name. As a result, class attributes cannot be used to set default values for instance variables defined by *\_\_slots\_\_*; otherwise, the class attribute would overwrite the descriptor assignment.
- The action of a *\_\_slots\_\_* declaration is not limited to the class where it is defined. *\_\_slots\_\_* declared in parents are available in child classes. However, instances of a child subclass will get a `~object.__dict__`{.interpreted-text role="attr"} and *\_\_weakref\_\_* unless the subclass also defines *\_\_slots\_\_* (which should only contain names of any *additional* slots).
- If a class defines a slot also defined in a base class, the instance variable defined by the base class slot is inaccessible (except by retrieving its descriptor directly from the base class). This renders the meaning of the program undefined. In the future, a check may be added to prevent this.
- `TypeError`{.interpreted-text role="exc"} will be raised if *\_\_slots\_\_* other than *\_\_dict\_\_* and *\_\_weakref\_\_* are defined for a class derived from a `"variable-length" built-in type <PyTypeObject.tp_itemsize>`{.interpreted-text role="c:member"} such as `int`{.interpreted-text role="class"}, `bytes`{.interpreted-text role="class"}, and `type`{.interpreted-text role="class"}, except `tuple`{.interpreted-text role="class"}.
- Any non-string `iterable`{.interpreted-text role="term"} may be assigned to *\_\_slots\_\_*.
- If a `dictionary <dict>`{.interpreted-text role="class"} is used to assign *\_\_slots\_\_*, the dictionary keys will be used as the slot names. The values of the dictionary can be used to provide per-attribute docstrings that will be recognised by `inspect.getdoc`{.interpreted-text role="func"} and displayed in the output of `help`{.interpreted-text role="func"}.
- `~object.__class__`{.interpreted-text role="attr"} assignment works only if both classes have the same *\_\_slots\_\_*.
- `Multiple inheritance <multiple-inheritance>`{.interpreted-text role="ref"} with multiple slotted parent classes can be used, but only one parent is allowed to have attributes created by slots (the other bases must have empty slot layouts) - violations raise `TypeError`{.interpreted-text role="exc"}.
- If an `iterator`{.interpreted-text role="term"} is used for *\_\_slots\_\_* then a `descriptor`{.interpreted-text role="term"} is created for each of the iterator\'s values. However, the *\_\_slots\_\_* attribute will be an empty iterator.

::: versionchanged
3.15 Allowed defining the *\_\_dict\_\_* and *\_\_weakref\_\_* *\_\_slots\_\_* for any class. Allowed defining any *\_\_slots\_\_* for a class derived from `tuple`{.interpreted-text role="class"}.
:::

### Customizing class creation {#class-customization}

Whenever a class inherits from another class, `~object.__init_subclass__`{.interpreted-text role="meth"} is called on the parent class. This way, it is possible to write classes which change the behavior of subclasses. This is closely related to class decorators, but where class decorators only affect the specific class they\'re applied to, `__init_subclass__` solely applies to future subclasses of the class defining the method.

:::::: classmethod
object.\_\_init_subclass\_\_(cls)

This method is called whenever the containing class is subclassed. *cls* is then the new subclass. If defined as a normal instance method, this method is implicitly converted to a class method.

Keyword arguments which are given to a new class are passed to the parent class\'s `__init_subclass__`. For compatibility with other classes using `__init_subclass__`, one should take out the needed keyword arguments and pass the others over to the base class, as in:

    class Philosopher:
        def __init_subclass__(cls, /, default_name, **kwargs):
            super().__init_subclass__(**kwargs)
            cls.default_name = default_name

    class AustralianPhilosopher(Philosopher, default_name="Bruce"):
        pass

The default implementation `object.__init_subclass__` does nothing, but raises an error if it is called with any arguments.

:::: note
::: title
Note
:::

The metaclass hint `metaclass` is consumed by the rest of the type machinery, and is never passed to `__init_subclass__` implementations. The actual metaclass (rather than the explicit hint) can be accessed as `type(cls)`.
::::

::: versionadded
3.6
:::
::::::

When a class is created, `!type.__new__`{.interpreted-text role="meth"} scans the class variables and makes callbacks to those with a `~object.__set_name__`{.interpreted-text role="meth"} hook.

:::: method
object.\_\_set_name\_\_(self, owner, name)

Automatically called at the time the owning class *owner* is created. The object has been assigned to *name* in that class:

    class A:
        x = C()  # Automatically calls: x.__set_name__(A, 'x')

If the class variable is assigned after the class is created, `__set_name__`{.interpreted-text role="meth"} will not be called automatically. If needed, `__set_name__`{.interpreted-text role="meth"} can be called directly:

    class A:
       pass

    c = C()
    A.x = c                  # The hook is not called
    c.__set_name__(A, 'x')   # Manually invoke the hook

See `class-object-creation`{.interpreted-text role="ref"} for more details.

::: versionadded
3.6
:::
::::

#### Metaclasses

::: index
single: metaclass pair: built-in function; type single: = (equals); class definition
:::

By default, classes are constructed using `type`{.interpreted-text role="func"}. The class body is executed in a new namespace and the class name is bound locally to the result of `type(name, bases, namespace)`.

The class creation process can be customized by passing the `metaclass` keyword argument in the class definition line, or by inheriting from an existing class that included such an argument. In the following example, both `MyClass` and `MySubclass` are instances of `Meta`:

    class Meta(type):
        pass

    class MyClass(metaclass=Meta):
        pass

    class MySubclass(MyClass):
        pass

Any other keyword arguments that are specified in the class definition are passed through to all metaclass operations described below.

When a class definition is executed, the following steps occur:

- MRO entries are resolved;
- the appropriate metaclass is determined;
- the class namespace is prepared;
- the class body is executed;
- the class object is created.

#### Resolving MRO entries

::: method
object.\_\_mro_entries\_\_(self, bases)

If a base that appears in a class definition is not an instance of `type`{.interpreted-text role="class"}, then an `!__mro_entries__`{.interpreted-text role="meth"} method is searched on the base. If an `!__mro_entries__`{.interpreted-text role="meth"} method is found, the base is substituted with the result of a call to `!__mro_entries__`{.interpreted-text role="meth"} when creating the class. The method is called with the original bases tuple passed to the *bases* parameter, and must return a tuple of classes that will be used instead of the base. The returned tuple may be empty: in these cases, the original base is ignored.
:::

::: seealso

`types.resolve_bases`{.interpreted-text role="func"}

:   Dynamically resolve bases that are not instances of `type`{.interpreted-text role="class"}.

`types.get_original_bases`{.interpreted-text role="func"}

:   Retrieve a class\'s \"original bases\" prior to modifications by `~object.__mro_entries__`{.interpreted-text role="meth"}.

`560`{.interpreted-text role="pep"}

:   Core support for typing module and generic types.
:::

#### Determining the appropriate metaclass {#metaclass-determination}

::: index
single: metaclass hint
:::

The appropriate metaclass for a class definition is determined as follows:

- if no bases and no explicit metaclass are given, then `type`{.interpreted-text role="func"} is used;
- if an explicit metaclass is given and it is *not* an instance of `type`{.interpreted-text role="func"}, then it is used directly as the metaclass;
- if an instance of `type`{.interpreted-text role="func"} is given as the explicit metaclass, or bases are defined, then the most derived metaclass is used.

The most derived metaclass is selected from the explicitly specified metaclass (if any) and the metaclasses (i.e. `type(cls)`) of all specified base classes. The most derived metaclass is one which is a subtype of *all* of these candidate metaclasses. If none of the candidate metaclasses meets that criterion, then the class definition will fail with `TypeError`.

#### Preparing the class namespace {#prepare}

::: index
single: \_\_prepare\_\_ (metaclass method)
:::

Once the appropriate metaclass has been identified, then the class namespace is prepared. If the metaclass has a `__prepare__` attribute, it is called as `namespace = metaclass.__prepare__(name, bases, **kwds)` (where the additional keyword arguments, if any, come from the class definition). The `__prepare__` method should be implemented as a `classmethod <classmethod>`{.interpreted-text role="func"}. The namespace returned by `__prepare__` is passed in to `__new__`, but when the final class object is created the namespace is copied into a new `dict`.

If the metaclass has no `__prepare__` attribute, then the class namespace is initialised as an empty ordered mapping.

::: seealso

`3115`{.interpreted-text role="pep"} - Metaclasses in Python 3000

:   Introduced the `__prepare__` namespace hook
:::

#### Executing the class body

::: index
single: class; body
:::

The class body is executed (approximately) as `exec(body, globals(), namespace)`. The key difference from a normal call to `exec`{.interpreted-text role="func"} is that lexical scoping allows the class body (including any methods) to reference names from the current and outer scopes when the class definition occurs inside a function.

However, even when the class definition occurs inside the function, methods defined inside the class still cannot see names defined at the class scope. Class variables must be accessed through the first parameter of instance or class methods, or through the implicit lexically scoped `__class__` reference described in the next section.

#### Creating the class object {#class-object-creation}

::: index
single: \_\_class\_\_ (method cell) single: \_\_classcell\_\_ (class namespace entry)
:::

Once the class namespace has been populated by executing the class body, the class object is created by calling `metaclass(name, bases, namespace, **kwds)` (the additional keywords passed here are the same as those passed to `__prepare__`).

This class object is the one that will be referenced by the zero-argument form of `super`{.interpreted-text role="func"}. `__class__` is an implicit closure reference created by the compiler if any methods in a class body refer to either `__class__` or `super`. This allows the zero argument form of `super`{.interpreted-text role="func"} to correctly identify the class being defined based on lexical scoping, while the class or instance that was used to make the current call is identified based on the first argument passed to the method.

::: impl-detail
In CPython 3.6 and later, the `__class__` cell is passed to the metaclass as a `__classcell__` entry in the class namespace. If present, this must be propagated up to the `type.__new__` call in order for the class to be initialised correctly. Failing to do so will result in a `RuntimeError`{.interpreted-text role="exc"} in Python 3.8.
:::

When using the default metaclass `type`{.interpreted-text role="class"}, or any metaclass that ultimately calls `type.__new__`, the following additional customization steps are invoked after creating the class object:

1)  The `type.__new__` method collects all of the attributes in the class namespace that define a `~object.__set_name__`{.interpreted-text role="meth"} method;
2)  Those `__set_name__` methods are called with the class being defined and the assigned name of that particular attribute;
3)  The `~object.__init_subclass__`{.interpreted-text role="meth"} hook is called on the immediate parent of the new class in its method resolution order.

After the class object is created, it is passed to the class decorators included in the class definition (if any) and the resulting object is bound in the local namespace as the defined class.

When a new class is created by `type.__new__`, the object provided as the namespace parameter is copied to a new ordered mapping and the original object is discarded. The new copy is wrapped in a read-only proxy, which becomes the `~type.__dict__`{.interpreted-text role="attr"} attribute of the class object.

::: seealso

`3135`{.interpreted-text role="pep"} - New super

:   Describes the implicit `__class__` closure reference
:::

#### Uses for metaclasses

The potential uses for metaclasses are boundless. Some ideas that have been explored include enum, logging, interface checking, automatic delegation, automatic property creation, proxies, frameworks, and automatic resource locking/synchronization.

### Customizing instance and subclass checks

The following methods are used to override the default behavior of the `isinstance`{.interpreted-text role="func"} and `issubclass`{.interpreted-text role="func"} built-in functions.

In particular, the metaclass `abc.ABCMeta`{.interpreted-text role="class"} implements these methods in order to allow the addition of Abstract Base Classes (ABCs) as \"virtual base classes\" to any class or type (including built-in types), including other ABCs.

::: method
type.\_\_instancecheck\_\_(self, instance)

Return true if *instance* should be considered a (direct or indirect) instance of *class*. If defined, called to implement `isinstance(instance, class)`.
:::

::: method
type.\_\_subclasscheck\_\_(self, subclass)

Return true if *subclass* should be considered a (direct or indirect) subclass of *class*. If defined, called to implement `issubclass(subclass, class)`.
:::

Note that these methods are looked up on the type (metaclass) of a class. They cannot be defined as class methods in the actual class. This is consistent with the lookup of special methods that are called on instances, only in this case the instance is itself a class.

::: seealso

`3119`{.interpreted-text role="pep"} - Introducing Abstract Base Classes

:   Includes the specification for customizing `isinstance`{.interpreted-text role="func"} and `issubclass`{.interpreted-text role="func"} behavior through `~type.__instancecheck__`{.interpreted-text role="meth"} and `~type.__subclasscheck__`{.interpreted-text role="meth"}, with motivation for this functionality in the context of adding Abstract Base Classes (see the `abc`{.interpreted-text role="mod"} module) to the language.
:::

### Emulating generic types

When using `type annotations<annotation>`{.interpreted-text role="term"}, it is often useful to *parameterize* a `generic type`{.interpreted-text role="term"} using Python\'s square-brackets notation. For example, the annotation `list[int]` might be used to signify a `list`{.interpreted-text role="class"} in which all the elements are of type `int`{.interpreted-text role="class"}.

::: seealso

`484`{.interpreted-text role="pep"} - Type Hints

:   Introducing Python\'s framework for type annotations

`Generic Alias Types<types-genericalias>`{.interpreted-text role="ref"}

:   Documentation for objects representing parameterized generic classes

`Generics`{.interpreted-text role="ref"}, `user-defined generics<user-defined-generics>`{.interpreted-text role="ref"} and `typing.Generic`{.interpreted-text role="class"}

:   Documentation on how to implement generic classes that can be parameterized at runtime and understood by static type-checkers.
:::

A class can *generally* only be parameterized if it defines the special class method `__class_getitem__()`.

::: classmethod
object.\_\_class_getitem\_\_(cls, key)

Return an object representing the specialization of a generic class by type arguments found in *key*.

When defined on a class, `__class_getitem__()` is automatically a class method. As such, there is no need for it to be decorated with `classmethod`{.interpreted-text role="deco"} when it is defined.
:::

#### The purpose of *\_\_class_getitem\_\_*

The purpose of `~object.__class_getitem__`{.interpreted-text role="meth"} is to allow runtime parameterization of standard-library generic classes in order to more easily apply `type hints<type hint>`{.interpreted-text role="term"} to these classes.

To implement custom generic classes that can be parameterized at runtime and understood by static type-checkers, users should either inherit from a standard library class that already implements `~object.__class_getitem__`{.interpreted-text role="meth"}, or inherit from `typing.Generic`{.interpreted-text role="class"}, which has its own implementation of `__class_getitem__()`.

Custom implementations of `~object.__class_getitem__`{.interpreted-text role="meth"} on classes defined outside of the standard library may not be understood by third-party type-checkers such as mypy. Using `__class_getitem__()` on any class for purposes other than type hinting is discouraged.

#### *\_\_class_getitem\_\_* versus *\_\_getitem\_\_* {#classgetitem-versus-getitem}

Usually, the `subscription<subscriptions>`{.interpreted-text role="ref"} of an object using square brackets will call the `~object.__getitem__`{.interpreted-text role="meth"} instance method defined on the object\'s class. However, if the object being subscribed is itself a class, the class method `~object.__class_getitem__`{.interpreted-text role="meth"} may be called instead. `__class_getitem__()` should return a `GenericAlias<types-genericalias>`{.interpreted-text role="ref"} object if it is properly defined.

Presented with the `expression`{.interpreted-text role="term"} `obj[x]`, the Python interpreter follows something like the following process to decide whether `~object.__getitem__`{.interpreted-text role="meth"} or `~object.__class_getitem__`{.interpreted-text role="meth"} should be called:

    from inspect import isclass

    def subscribe(obj, x):
        """Return the result of the expression 'obj[x]'"""

        class_of_obj = type(obj)

        # If the class of obj defines __getitem__,
        # call class_of_obj.__getitem__(obj, x)
        if hasattr(class_of_obj, '__getitem__'):
            return class_of_obj.__getitem__(obj, x)

        # Else, if obj is a class and defines __class_getitem__,
        # call obj.__class_getitem__(x)
        elif isclass(obj) and hasattr(obj, '__class_getitem__'):
            return obj.__class_getitem__(x)

        # Else, raise an exception
        else:
            raise TypeError(
                f"'{class_of_obj.__name__}' object is not subscriptable"
            )

In Python, all classes are themselves instances of other classes. The class of a class is known as that class\'s `metaclass`{.interpreted-text role="term"}, and most classes have the `type`{.interpreted-text role="class"} class as their metaclass. `type`{.interpreted-text role="class"} does not define `~object.__getitem__`{.interpreted-text role="meth"}, meaning that expressions such as `list[int]`, `dict[str, float]` and `tuple[str, bytes]` all result in `~object.__class_getitem__`{.interpreted-text role="meth"} being called:

    >>> # list has class "type" as its metaclass, like most classes:
    >>> type(list)
    <class 'type'>
    >>> type(dict) == type(list) == type(tuple) == type(str) == type(bytes)
    True
    >>> # "list[int]" calls "list.__class_getitem__(int)"
    >>> list[int]
    list[int]
    >>> # list.__class_getitem__ returns a GenericAlias object:
    >>> type(list[int])
    <class 'types.GenericAlias'>

However, if a class has a custom metaclass that defines `~object.__getitem__`{.interpreted-text role="meth"}, subscribing the class may result in different behaviour. An example of this can be found in the `enum`{.interpreted-text role="mod"} module:

    >>> from enum import Enum
    >>> class Menu(Enum):
    ...     """A breakfast menu"""
    ...     SPAM = 'spam'
    ...     BACON = 'bacon'
    ...
    >>> # Enum classes have a custom metaclass:
    >>> type(Menu)
    <class 'enum.EnumMeta'>
    >>> # EnumMeta defines __getitem__,
    >>> # so __class_getitem__ is not called,
    >>> # and the result is not a GenericAlias object:
    >>> Menu['SPAM']
    <Menu.SPAM: 'spam'>
    >>> type(Menu['SPAM'])
    <enum 'Menu'>

::: seealso
`560`{.interpreted-text role="pep"} - Core Support for typing module and generic types Introducing `~object.__class_getitem__`{.interpreted-text role="meth"}, and outlining when a `subscription<subscriptions>`{.interpreted-text role="ref"} results in `__class_getitem__()` being called instead of `~object.__getitem__`{.interpreted-text role="meth"}
:::

### Emulating callable objects {#callable-types}

:::: method
object.\_\_call\_\_(self\[, args\...\])

::: index
pair: call; instance
:::

Called when the instance is \"called\" as a function; if this method is defined, `x(arg1, arg2, ...)` roughly translates to `type(x).__call__(x, arg1, ...)`. The `object`{.interpreted-text role="class"} class itself does not provide this method.
::::

### Emulating container types {#sequence-types}

The following methods can be defined to implement container objects. None of them are provided by the `object`{.interpreted-text role="class"} class itself. Containers usually are `sequences <sequence>`{.interpreted-text role="term"} (such as `lists <list>`{.interpreted-text role="class"} or `tuples <tuple>`{.interpreted-text role="class"}) or `mappings <mapping>`{.interpreted-text role="term"} (like `dictionaries <dictionary>`{.interpreted-text role="term"}), but can represent other containers as well. The first set of methods is used either to emulate a sequence or to emulate a mapping; the difference is that for a sequence, the allowable keys should be the integers *k* for which `0 <= k < N` where *N* is the length of the sequence, or `slice`{.interpreted-text role="class"} objects, which define a range of items. It is also recommended that mappings provide the methods `!keys`{.interpreted-text role="meth"}, `!values`{.interpreted-text role="meth"}, `!items`{.interpreted-text role="meth"}, `!get`{.interpreted-text role="meth"}, `!clear`{.interpreted-text role="meth"}, `!setdefault`{.interpreted-text role="meth"}, `!pop`{.interpreted-text role="meth"}, `!popitem`{.interpreted-text role="meth"}, `!copy`{.interpreted-text role="meth"}, and `!update`{.interpreted-text role="meth"} behaving similar to those for Python\'s standard `dictionary <dict>`{.interpreted-text role="class"} objects. The `collections.abc`{.interpreted-text role="mod"} module provides a `~collections.abc.MutableMapping`{.interpreted-text role="class"} `abstract base class`{.interpreted-text role="term"} to help create those methods from a base set of `~object.__getitem__`{.interpreted-text role="meth"}, `~object.__setitem__`{.interpreted-text role="meth"}, `~object.__delitem__`{.interpreted-text role="meth"}, and `!keys`{.interpreted-text role="meth"}.

Mutable sequences should provide methods `~sequence.append`{.interpreted-text role="meth"}, `~sequence.clear`{.interpreted-text role="meth"}, `~sequence.count`{.interpreted-text role="meth"}, `~sequence.extend`{.interpreted-text role="meth"}, `~sequence.index`{.interpreted-text role="meth"}, `~sequence.insert`{.interpreted-text role="meth"}, `~sequence.pop`{.interpreted-text role="meth"}, `~sequence.remove`{.interpreted-text role="meth"}, and `~sequence.reverse`{.interpreted-text role="meth"}, like Python standard `list`{.interpreted-text role="class"} objects. Finally, sequence types should implement addition (meaning concatenation) and multiplication (meaning repetition) by defining the methods `~object.__add__`{.interpreted-text role="meth"}, `~object.__radd__`{.interpreted-text role="meth"}, `~object.__iadd__`{.interpreted-text role="meth"}, `~object.__mul__`{.interpreted-text role="meth"}, `~object.__rmul__`{.interpreted-text role="meth"} and `~object.__imul__`{.interpreted-text role="meth"} described below; they should not define other numerical operators.

It is recommended that both mappings and sequences implement the `~object.__contains__`{.interpreted-text role="meth"} method to allow efficient use of the `in` operator; for mappings, `in` should search the mapping\'s keys; for sequences, it should search through the values. It is further recommended that both mappings and sequences implement the `~object.__iter__`{.interpreted-text role="meth"} method to allow efficient iteration through the container; for mappings, `!__iter__`{.interpreted-text role="meth"} should iterate through the object\'s keys; for sequences, it should iterate through the values.

::::: method
object.\_\_len\_\_(self)

::: index
pair: built-in function; len single: \_\_bool\_\_() (object method)
:::

Called to implement the built-in function `len`{.interpreted-text role="func"}. Should return the length of the object, an integer `>=` 0. Also, an object that doesn\'t define a `~object.__bool__`{.interpreted-text role="meth"} method and whose `!__len__`{.interpreted-text role="meth"} method returns zero is considered to be false in a Boolean context.

::: impl-detail
In CPython, the length is required to be at most `sys.maxsize`{.interpreted-text role="data"}. If the length is larger than `!sys.maxsize`{.interpreted-text role="data"} some features (such as `len`{.interpreted-text role="func"}) may raise `OverflowError`{.interpreted-text role="exc"}. To prevent raising `!OverflowError`{.interpreted-text role="exc"} by truth value testing, an object must define a `~object.__bool__`{.interpreted-text role="meth"} method.
:::
:::::

:::: method
object.\_\_length_hint\_\_(self)

Called to implement `operator.length_hint`{.interpreted-text role="func"}. Should return an estimated length for the object (which may be greater or less than the actual length). The length must be an integer `>=` 0. The return value may also be `NotImplemented`{.interpreted-text role="data"}, which is treated the same as if the `__length_hint__` method didn\'t exist at all. This method is purely an optimization and is never required for correctness.

::: versionadded
3.4
:::
::::

::: index
pair: object; slice
:::

:::: note
::: title
Note
:::

Slicing is done exclusively with the following three methods. A call like :

    a[1:2] = b

is translated to :

    a[slice(1, 2, None)] = b

and so forth. Missing slice items are always filled in with `None`.
::::

::::::: method
object.\_\_getitem\_\_(self, subscript)

Called to implement *subscription*, that is, `self[subscript]`. See `subscriptions`{.interpreted-text role="ref"} for details on the syntax.

There are two types of built-in objects that support subscription via `!__getitem__`{.interpreted-text role="meth"}:

- **sequences**, where *subscript* (also called `index`{.interpreted-text role="term"}) should be an integer or a `slice`{.interpreted-text role="class"} object. See the `sequence documentation <datamodel-sequences>`{.interpreted-text role="ref"} for the expected behavior, including handling `slice`{.interpreted-text role="class"} objects and negative indices.
- **mappings**, where *subscript* is also called the `key`{.interpreted-text role="term"}. See `mapping documentation <datamodel-mappings>`{.interpreted-text role="ref"} for the expected behavior.

If *subscript* is of an inappropriate type, `!__getitem__`{.interpreted-text role="meth"} should raise `TypeError`{.interpreted-text role="exc"}. If *subscript* has an inappropriate value, `!__getitem__`{.interpreted-text role="meth"} should raise an `LookupError`{.interpreted-text role="exc"} or one of its subclasses (`IndexError`{.interpreted-text role="exc"} for sequences; `KeyError`{.interpreted-text role="exc"} for mappings).

:::: note
::: title
Note
:::

The sequence iteration protocol (used, for example, in `for`{.interpreted-text role="keyword"} loops), expects that an `IndexError`{.interpreted-text role="exc"} will be raised for illegal indexes to allow proper detection of the end of a sequence.
::::

:::: note
::: title
Note
:::

When `subscripting <subscriptions>`{.interpreted-text role="ref"} a *class*, the special class method `~object.__class_getitem__`{.interpreted-text role="meth"} may be called instead of `!__getitem__`{.interpreted-text role="meth"}. See `classgetitem-versus-getitem`{.interpreted-text role="ref"} for more details.
::::
:::::::

::: method
object.\_\_setitem\_\_(self, key, value)

Called to implement assignment to `self[key]`. Same note as for `__getitem__`{.interpreted-text role="meth"}. This should only be implemented for mappings if the objects support changes to the values for keys, or if new keys can be added, or for sequences if elements can be replaced. The same exceptions should be raised for improper *key* values as for the `__getitem__`{.interpreted-text role="meth"} method.
:::

::: method
object.\_\_delitem\_\_(self, key)

Called to implement deletion of `self[key]`. Same note as for `__getitem__`{.interpreted-text role="meth"}. This should only be implemented for mappings if the objects support removal of keys, or for sequences if elements can be removed from the sequence. The same exceptions should be raised for improper *key* values as for the `__getitem__`{.interpreted-text role="meth"} method.
:::

::: method
object.\_\_missing\_\_(self, key)

Called by `dict`{.interpreted-text role="class"}.`__getitem__`{.interpreted-text role="meth"} to implement `self[key]` for dict subclasses when key is not in the dictionary.
:::

::: method
object.\_\_iter\_\_(self)

This method is called when an `iterator`{.interpreted-text role="term"} is required for a container. This method should return a new iterator object that can iterate over all the objects in the container. For mappings, it should iterate over the keys of the container.
:::

::: method
object.\_\_reversed\_\_(self)

Called (if present) by the `reversed`{.interpreted-text role="func"} built-in to implement reverse iteration. It should return a new iterator object that iterates over all the objects in the container in reverse order.

If the `__reversed__`{.interpreted-text role="meth"} method is not provided, the `reversed`{.interpreted-text role="func"} built-in will fall back to using the sequence protocol (`__len__`{.interpreted-text role="meth"} and `__getitem__`{.interpreted-text role="meth"}). Objects that support the sequence protocol should only provide `__reversed__`{.interpreted-text role="meth"} if they can provide an implementation that is more efficient than the one provided by `reversed`{.interpreted-text role="func"}.
:::

The membership test operators (`in`{.interpreted-text role="keyword"} and `not in`{.interpreted-text role="keyword"}) are normally implemented as an iteration through a container. However, container objects can supply the following special method with a more efficient implementation, which also does not require the object be iterable.

::: method
object.\_\_contains\_\_(self, item)

Called to implement membership test operators. Should return true if *item* is in *self*, false otherwise. For mapping objects, this should consider the keys of the mapping rather than the values or the key-item pairs.

For objects that don\'t define `__contains__`{.interpreted-text role="meth"}, the membership test first tries iteration via `__iter__`{.interpreted-text role="meth"}, then the old sequence iteration protocol via `__getitem__`{.interpreted-text role="meth"}, see `this section in the language
reference <membership-test-details>`{.interpreted-text role="ref"}.
:::

### Emulating numeric types {#numeric-types}

The following methods can be defined to emulate numeric objects. Methods corresponding to operations that are not supported by the particular kind of number implemented (e.g., bitwise operations for non-integral numbers) should be left undefined.

:::: method
object.\_\_add\_\_(self, other) object.\_\_sub\_\_(self, other) object.\_\_mul\_\_(self, other) object.\_\_matmul\_\_(self, other) object.\_\_truediv\_\_(self, other) object.\_\_floordiv\_\_(self, other) object.\_\_mod\_\_(self, other) object.\_\_divmod\_\_(self, other) object.\_\_pow\_\_(self, other\[, modulo\]) object.\_\_lshift\_\_(self, other) object.\_\_rshift\_\_(self, other) object.\_\_and\_\_(self, other) object.\_\_xor\_\_(self, other) object.\_\_or\_\_(self, other)

::: index
pair: built-in function; divmod pair: built-in function; pow pair: built-in function; pow
:::

These methods are called to implement the binary arithmetic operations (`+`, `-`, `*`, `@`, `/`, `//`, `%`, `divmod`{.interpreted-text role="func"}, `pow`{.interpreted-text role="func"}, `**`, `<<`, `>>`, `&`, `^`, `|`). For instance, to evaluate the expression `x + y`, where *x* is an instance of a class that has an `__add__`{.interpreted-text role="meth"} method, `type(x).__add__(x, y)` is called. The `__divmod__`{.interpreted-text role="meth"} method should be the equivalent to using `__floordiv__`{.interpreted-text role="meth"} and `__mod__`{.interpreted-text role="meth"}; it should not be related to `__truediv__`{.interpreted-text role="meth"}. Note that `__pow__`{.interpreted-text role="meth"} should be defined to accept an optional third argument if the three-argument version of the built-in `pow`{.interpreted-text role="func"} function is to be supported.

If one of those methods does not support the operation with the supplied arguments, it should return `NotImplemented`{.interpreted-text role="data"}.
::::

::::::: method
object.\_\_radd\_\_(self, other) object.\_\_rsub\_\_(self, other) object.\_\_rmul\_\_(self, other) object.\_\_rmatmul\_\_(self, other) object.\_\_rtruediv\_\_(self, other) object.\_\_rfloordiv\_\_(self, other) object.\_\_rmod\_\_(self, other) object.\_\_rdivmod\_\_(self, other) object.\_\_rpow\_\_(self, other\[, modulo\]) object.\_\_rlshift\_\_(self, other) object.\_\_rrshift\_\_(self, other) object.\_\_rand\_\_(self, other) object.\_\_rxor\_\_(self, other) object.\_\_ror\_\_(self, other)

::: index
pair: built-in function; divmod pair: built-in function; pow
:::

These methods are called to implement the binary arithmetic operations (`+`, `-`, `*`, `@`, `/`, `//`, `%`, `divmod`{.interpreted-text role="func"}, `pow`{.interpreted-text role="func"}, `**`, `<<`, `>>`, `&`, `^`, `|`) with reflected (swapped) operands. These functions are only called if the operands are of different types, when the left operand does not support the corresponding operation[^3], or the right operand\'s class is derived from the left operand\'s class.[^4] For instance, to evaluate the expression `x - y`, where *y* is an instance of a class that has an `__rsub__`{.interpreted-text role="meth"} method, `type(y).__rsub__(y, x)` is called if `type(x).__sub__(x, y)` returns `NotImplemented`{.interpreted-text role="data"} or `type(y)` is a subclass of `type(x)`.[^5]

Note that `__rpow__`{.interpreted-text role="meth"} should be defined to accept an optional third argument if the three-argument version of the built-in `pow`{.interpreted-text role="func"} function is to be supported.

::: versionchanged
3.14

Three-argument `pow`{.interpreted-text role="func"} now try calling `~object.__rpow__`{.interpreted-text role="meth"} if necessary. Previously it was only called in two-argument `!pow`{.interpreted-text role="func"} and the binary power operator.
:::

:::: note
::: title
Note
:::

If the right operand\'s type is a subclass of the left operand\'s type and that subclass provides a different implementation of the reflected method for the operation, this method will be called before the left operand\'s non-reflected method. This behavior allows subclasses to override their ancestors\' operations.
::::
:::::::

::: method
object.\_\_iadd\_\_(self, other) object.\_\_isub\_\_(self, other) object.\_\_imul\_\_(self, other) object.\_\_imatmul\_\_(self, other) object.\_\_itruediv\_\_(self, other) object.\_\_ifloordiv\_\_(self, other) object.\_\_imod\_\_(self, other) object.\_\_ipow\_\_(self, other\[, modulo\]) object.\_\_ilshift\_\_(self, other) object.\_\_irshift\_\_(self, other) object.\_\_iand\_\_(self, other) object.\_\_ixor\_\_(self, other) object.\_\_ior\_\_(self, other)

These methods are called to implement the augmented arithmetic assignments (`+=`, `-=`, `*=`, `@=`, `/=`, `//=`, `%=`, `**=`, `<<=`, `>>=`, `&=`, `^=`, `|=`). These methods should attempt to do the operation in-place (modifying *self*) and return the result (which could be, but does not have to be, *self*). If a specific method is not defined, or if that method returns `NotImplemented`{.interpreted-text role="data"}, the augmented assignment falls back to the normal methods. For instance, if *x* is an instance of a class with an `__iadd__`{.interpreted-text role="meth"} method, `x += y` is equivalent to `x = x.__iadd__(y)` . If `__iadd__`{.interpreted-text role="meth"} does not exist, or if `x.__iadd__(y)` returns `!NotImplemented`{.interpreted-text role="data"}, `x.__add__(y)` and `y.__radd__(x)` are considered, as with the evaluation of `x + y`. In certain situations, augmented assignment can result in unexpected errors (see `faq-augmented-assignment-tuple-error`{.interpreted-text role="ref"}), but this behavior is in fact part of the data model.
:::

:::: method
object.\_\_neg\_\_(self) object.\_\_pos\_\_(self) object.\_\_abs\_\_(self) object.\_\_invert\_\_(self)

::: index
pair: built-in function; abs
:::

Called to implement the unary arithmetic operations (`-`, `+`, `abs`{.interpreted-text role="func"} and `~`).
::::

:::: method
object.\_\_complex\_\_(self) object.\_\_int\_\_(self) object.\_\_float\_\_(self)

::: index
pair: built-in function; complex pair: built-in function; int pair: built-in function; float
:::

Called to implement the built-in functions `complex`{.interpreted-text role="func"}, `int`{.interpreted-text role="func"} and `float`{.interpreted-text role="func"}. Should return a value of the appropriate type.
::::

::: method
object.\_\_index\_\_(self)

Called to implement `operator.index`{.interpreted-text role="func"}, and whenever Python needs to losslessly convert the numeric object to an integer object (such as in slicing, or in the built-in `bin`{.interpreted-text role="func"}, `hex`{.interpreted-text role="func"} and `oct`{.interpreted-text role="func"} functions). Presence of this method indicates that the numeric object is an integer type. Must return an integer.

If `__int__`{.interpreted-text role="meth"}, `__float__`{.interpreted-text role="meth"} and `__complex__`{.interpreted-text role="meth"} are not defined then corresponding built-in functions `int`{.interpreted-text role="func"}, `float`{.interpreted-text role="func"} and `complex`{.interpreted-text role="func"} fall back to `__index__`{.interpreted-text role="meth"}.
:::

::::: method
object.\_\_round\_\_(self, \[,ndigits\]) object.\_\_trunc\_\_(self) object.\_\_floor\_\_(self) object.\_\_ceil\_\_(self)

::: index
pair: built-in function; round
:::

Called to implement the built-in function `round`{.interpreted-text role="func"} and `math`{.interpreted-text role="mod"} functions `~math.trunc`{.interpreted-text role="func"}, `~math.floor`{.interpreted-text role="func"} and `~math.ceil`{.interpreted-text role="func"}. Unless *ndigits* is passed to `!__round__`{.interpreted-text role="meth"} all these methods should return the value of the object truncated to an `~numbers.Integral`{.interpreted-text role="class"} (typically an `int`{.interpreted-text role="class"}).

::: versionchanged
3.14 `int`{.interpreted-text role="func"} no longer delegates to the `~object.__trunc__`{.interpreted-text role="meth"} method.
:::
:::::

### With Statement Context Managers {#context-managers}

A `context manager`{.interpreted-text role="dfn"} is an object that defines the runtime context to be established when executing a `with`{.interpreted-text role="keyword"} statement. The context manager handles the entry into, and the exit from, the desired runtime context for the execution of the block of code. Context managers are normally invoked using the `!with`{.interpreted-text role="keyword"} statement (described in section `with`{.interpreted-text role="ref"}), but can also be used by directly invoking their methods.

::: index
pair: statement; with single: context manager
:::

Typical uses of context managers include saving and restoring various kinds of global state, locking and unlocking resources, closing opened files, etc.

For more information on context managers, see `typecontextmanager`{.interpreted-text role="ref"}. The `object`{.interpreted-text role="class"} class itself does not provide the context manager methods.

::: method
object.\_\_enter\_\_(self)

Enter the runtime context related to this object. The `with`{.interpreted-text role="keyword"} statement will bind this method\'s return value to the target(s) specified in the `!as`{.interpreted-text role="keyword"} clause of the statement, if any.
:::

::: method
object.\_\_exit\_\_(self, exc_type, exc_value, traceback)

Exit the runtime context related to this object. The parameters describe the exception that caused the context to be exited. If the context was exited without an exception, all three arguments will be `None`{.interpreted-text role="const"}.

If an exception is supplied, and the method wishes to suppress the exception (i.e., prevent it from being propagated), it should return a true value. Otherwise, the exception will be processed normally upon exit from this method.

Note that `~object.__exit__`{.interpreted-text role="meth"} methods should not reraise the passed-in exception; this is the caller\'s responsibility.
:::

::: seealso

`343`{.interpreted-text role="pep"} - The \"with\" statement

:   The specification, background, and examples for the Python `with`{.interpreted-text role="keyword"} statement.
:::

### Customizing positional arguments in class pattern matching {#class-pattern-matching}

When using a class name in a pattern, positional arguments in the pattern are not allowed by default, i.e. `case MyClass(x, y)` is typically invalid without special support in `MyClass`. To be able to use that kind of pattern, the class needs to define a *\_\_match_args\_\_* attribute.

::: data
object.\_\_match_args\_\_

This class variable can be assigned a tuple of strings. When this class is used in a class pattern with positional arguments, each positional argument will be converted into a keyword argument, using the corresponding value in *\_\_match_args\_\_* as the keyword. The absence of this attribute is equivalent to setting it to `()`.
:::

For example, if `MyClass.__match_args__` is `("left", "center", "right")` that means that `case MyClass(x, y)` is equivalent to `case MyClass(left=x, center=y)`. Note that the number of arguments in the pattern must be smaller than or equal to the number of elements in *\_\_match_args\_\_*; if it is larger, the pattern match attempt will raise a `TypeError`{.interpreted-text role="exc"}.

::: versionadded
3.10
:::

::: seealso

`634`{.interpreted-text role="pep"} - Structural Pattern Matching

:   The specification for the Python `match` statement.
:::

### Emulating buffer types {#python-buffer-protocol}

The `buffer protocol <bufferobjects>`{.interpreted-text role="ref"} provides a way for Python objects to expose efficient access to a low-level memory array. This protocol is implemented by builtin types such as `bytes`{.interpreted-text role="class"} and `memoryview`{.interpreted-text role="class"}, and third-party libraries may define additional buffer types.

While buffer types are usually implemented in C, it is also possible to implement the protocol in Python.

::: method
object.\_\_buffer\_\_(self, flags)

Called when a buffer is requested from *self* (for example, by the `memoryview`{.interpreted-text role="class"} constructor). The *flags* argument is an integer representing the kind of buffer requested, affecting for example whether the returned buffer is read-only or writable. `inspect.BufferFlags`{.interpreted-text role="class"} provides a convenient way to interpret the flags. The method must return a `memoryview`{.interpreted-text role="class"} object.
:::

::: method
object.\_\_release_buffer\_\_(self, buffer)

Called when a buffer is no longer needed. The *buffer* argument is a `memoryview`{.interpreted-text role="class"} object that was previously returned by `~object.__buffer__`{.interpreted-text role="meth"}. The method must release any resources associated with the buffer. This method should return `None`. Buffer objects that do not need to perform any cleanup are not required to implement this method.
:::

::: versionadded
3.12
:::

::: seealso

`688`{.interpreted-text role="pep"} - Making the buffer protocol accessible in Python

:   Introduces the Python `__buffer__` and `__release_buffer__` methods.

`collections.abc.Buffer`{.interpreted-text role="class"}

:   ABC for buffer types.
:::

### Annotations

Functions, classes, and modules may contain `annotations <annotation>`{.interpreted-text role="term"}, which are a way to associate information (usually `type hints <type hint>`{.interpreted-text role="term"}) with a symbol.

:::: attribute
object.\_\_annotations\_\_

This attribute contains the annotations for an object. It is `lazily evaluated <lazy-evaluation>`{.interpreted-text role="ref"}, so accessing the attribute may execute arbitrary code and raise exceptions. If evaluation is successful, the attribute is set to a dictionary mapping from variable names to annotations.

::: versionchanged
3.14 Annotations are now lazily evaluated.
:::
::::

:::: method
object.\_\_annotate\_\_(format)

An `annotate function`{.interpreted-text role="term"}. Returns a new dictionary object mapping attribute/parameter names to their annotation values.

Takes a format parameter specifying the format in which annotations values should be provided. It must be a member of the `annotationlib.Format`{.interpreted-text role="class"} enum, or an integer with a value corresponding to a member of the enum.

If an annotate function doesn\'t support the requested format, it must raise `NotImplementedError`{.interpreted-text role="exc"}. Annotate functions must always support `~annotationlib.Format.VALUE`{.interpreted-text role="attr"} format; they must not raise `NotImplementedError()`{.interpreted-text role="exc"} when called with this format.

When called with `~annotationlib.Format.VALUE`{.interpreted-text role="attr"} format, an annotate function may raise `NameError`{.interpreted-text role="exc"}; it must not raise `!NameError`{.interpreted-text role="exc"} when called requesting any other format.

If an object does not have any annotations, `~object.__annotate__`{.interpreted-text role="attr"} should preferably be set to `None` (it can't be deleted), rather than set to a function that returns an empty dict.

::: versionadded
3.14
:::
::::

::: seealso

`649`{.interpreted-text role="pep"} \-\-- Deferred evaluation of annotation using descriptors

:   Introduces lazy evaluation of annotations and the `__annotate__` function.
:::

### Special method lookup {#special-lookup}

For custom classes, implicit invocations of special methods are only guaranteed to work correctly if defined on an object\'s type, not in the object\'s instance dictionary. That behaviour is the reason why the following code raises an exception:

    >>> class C:
    ...     pass
    ...
    >>> c = C()
    >>> c.__len__ = lambda: 5
    >>> len(c)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: object of type 'C' has no len()

The rationale behind this behaviour lies with a number of special methods such as `~object.__hash__`{.interpreted-text role="meth"} and `~object.__repr__`{.interpreted-text role="meth"} that are implemented by all objects, including type objects. If the implicit lookup of these methods used the conventional lookup process, they would fail when invoked on the type object itself:

    >>> 1 .__hash__() == hash(1)
    True
    >>> int.__hash__() == hash(int)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: descriptor '__hash__' of 'int' object needs an argument

Incorrectly attempting to invoke an unbound method of a class in this way is sometimes referred to as \'metaclass confusion\', and is avoided by bypassing the instance when looking up special methods:

    >>> type(1).__hash__(1) == hash(1)
    True
    >>> type(int).__hash__(int) == hash(int)
    True

In addition to bypassing any instance attributes in the interest of correctness, implicit special method lookup generally also bypasses the `~object.__getattribute__`{.interpreted-text role="meth"} method even of the object\'s metaclass:

    >>> class Meta(type):
    ...     def __getattribute__(*args):
    ...         print("Metaclass getattribute invoked")
    ...         return type.__getattribute__(*args)
    ...
    >>> class C(object, metaclass=Meta):
    ...     def __len__(self):
    ...         return 10
    ...     def __getattribute__(*args):
    ...         print("Class getattribute invoked")
    ...         return object.__getattribute__(*args)
    ...
    >>> c = C()
    >>> c.__len__()                 # Explicit lookup via instance
    Class getattribute invoked
    10
    >>> type(c).__len__(c)          # Explicit lookup via type
    Metaclass getattribute invoked
    10
    >>> len(c)                      # Implicit lookup
    10

Bypassing the `~object.__getattribute__`{.interpreted-text role="meth"} machinery in this fashion provides significant scope for speed optimisations within the interpreter, at the cost of some flexibility in the handling of special methods (the special method *must* be set on the class object itself in order to be consistently invoked by the interpreter).

::: index
single: coroutine
:::

## Coroutines

### Awaitable Objects

An `awaitable`{.interpreted-text role="term"} object generally implements an `~object.__await__`{.interpreted-text role="meth"} method. `Coroutine objects <coroutine>`{.interpreted-text role="term"} returned from `async def`{.interpreted-text role="keyword"} functions are awaitable.

:::: note
::: title
Note
:::

The `generator iterator`{.interpreted-text role="term"} objects returned from generators decorated with `types.coroutine`{.interpreted-text role="func"} are also awaitable, but they do not implement `~object.__await__`{.interpreted-text role="meth"}.
::::

::::: method
object.\_\_await\_\_(self)

Must return an `iterator`{.interpreted-text role="term"}. Should be used to implement `awaitable`{.interpreted-text role="term"} objects. For instance, `asyncio.Future`{.interpreted-text role="class"} implements this method to be compatible with the `await`{.interpreted-text role="keyword"} expression. The `object`{.interpreted-text role="class"} class itself is not awaitable and does not provide this method.

:::: note
::: title
Note
:::

The language doesn\'t place any restriction on the type or value of the objects yielded by the iterator returned by `__await__`, as this is specific to the implementation of the asynchronous execution framework (e.g. `asyncio`{.interpreted-text role="mod"}) that will be managing the `awaitable`{.interpreted-text role="term"} object.
::::
:::::

::: versionadded
3.5
:::

::: seealso
`492`{.interpreted-text role="pep"} for additional information about awaitable objects.
:::

### Coroutine Objects

`Coroutine objects <coroutine>`{.interpreted-text role="term"} are `awaitable`{.interpreted-text role="term"} objects. A coroutine\'s execution can be controlled by calling `~object.__await__`{.interpreted-text role="meth"} and iterating over the result. When the coroutine has finished executing and returns, the iterator raises `StopIteration`{.interpreted-text role="exc"}, and the exception\'s `~StopIteration.value`{.interpreted-text role="attr"} attribute holds the return value. If the coroutine raises an exception, it is propagated by the iterator. Coroutines should not directly raise unhandled `StopIteration`{.interpreted-text role="exc"} exceptions.

Coroutines also have the methods listed below, which are analogous to those of generators (see `generator-methods`{.interpreted-text role="ref"}). However, unlike generators, coroutines do not directly support iteration.

::: versionchanged
3.5.2 It is a `RuntimeError`{.interpreted-text role="exc"} to await on a coroutine more than once.
:::

::: method
coroutine.send(value)

Starts or resumes execution of the coroutine. If *value* is `None`, this is equivalent to advancing the iterator returned by `~object.__await__`{.interpreted-text role="meth"}. If *value* is not `None`, this method delegates to the `~generator.send`{.interpreted-text role="meth"} method of the iterator that caused the coroutine to suspend. The result (return value, `StopIteration`{.interpreted-text role="exc"}, or other exception) is the same as when iterating over the `!__await__`{.interpreted-text role="meth"} return value, described above.
:::

:::: method
coroutine.throw(value) coroutine.throw(type\[, value\[, traceback\]\])

Raises the specified exception in the coroutine. This method delegates to the `~generator.throw`{.interpreted-text role="meth"} method of the iterator that caused the coroutine to suspend, if it has such a method. Otherwise, the exception is raised at the suspension point. The result (return value, `StopIteration`{.interpreted-text role="exc"}, or other exception) is the same as when iterating over the `~object.__await__`{.interpreted-text role="meth"} return value, described above. If the exception is not caught in the coroutine, it propagates back to the caller.

::: versionchanged
3.12

The second signature (type\[, value\[, traceback\]\]) is deprecated and may be removed in a future version of Python.
:::
::::

::: method
coroutine.close()

Causes the coroutine to clean itself up and exit. If the coroutine is suspended, this method first delegates to the `~generator.close`{.interpreted-text role="meth"} method of the iterator that caused the coroutine to suspend, if it has such a method. Then it raises `GeneratorExit`{.interpreted-text role="exc"} at the suspension point, causing the coroutine to immediately clean itself up. Finally, the coroutine is marked as having finished executing, even if it was never started.

Coroutine objects are automatically closed using the above process when they are about to be destroyed.
:::

### Asynchronous Iterators {#async-iterators}

An *asynchronous iterator* can call asynchronous code in its `__anext__` method.

Asynchronous iterators can be used in an `async for`{.interpreted-text role="keyword"} statement.

The `object`{.interpreted-text role="class"} class itself does not provide these methods.

::: method
object.\_\_aiter\_\_(self)

Must return an *asynchronous iterator* object.
:::

::: method
object.\_\_anext\_\_(self)

Must return an *awaitable* resulting in a next value of the iterator. Should raise a `StopAsyncIteration`{.interpreted-text role="exc"} error when the iteration is over.
:::

An example of an asynchronous iterable object:

    class Reader:
        async def readline(self):
            ...

        def __aiter__(self):
            return self

        async def __anext__(self):
            val = await self.readline()
            if val == b'':
                raise StopAsyncIteration
            return val

::: versionadded
3.5
:::

::: versionchanged
3.7 Prior to Python 3.7, `~object.__aiter__`{.interpreted-text role="meth"} could return an *awaitable* that would resolve to an `asynchronous iterator <asynchronous iterator>`{.interpreted-text role="term"}.

Starting with Python 3.7, `~object.__aiter__`{.interpreted-text role="meth"} must return an asynchronous iterator object. Returning anything else will result in a `TypeError`{.interpreted-text role="exc"} error.
:::

### Asynchronous Context Managers {#async-context-managers}

An *asynchronous context manager* is a *context manager* that is able to suspend execution in its `__aenter__` and `__aexit__` methods.

Asynchronous context managers can be used in an `async with`{.interpreted-text role="keyword"} statement.

The `object`{.interpreted-text role="class"} class itself does not provide these methods.

::: method
object.\_\_aenter\_\_(self)

Semantically similar to `~object.__enter__`{.interpreted-text role="meth"}, the only difference being that it must return an *awaitable*.
:::

::: method
object.\_\_aexit\_\_(self, exc_type, exc_value, traceback)

Semantically similar to `~object.__exit__`{.interpreted-text role="meth"}, the only difference being that it must return an *awaitable*.
:::

An example of an asynchronous context manager class:

    class AsyncContextManager:
        async def __aenter__(self):
            await log('entering context')

        async def __aexit__(self, exc_type, exc, tb):
            await log('exiting context')

::: versionadded
3.5
:::

**Footnotes**

[^1]: It *is* possible in some cases to change an object\'s type, under certain controlled conditions. It generally isn\'t a good idea though, since it can lead to some very strange behaviour if it is handled incorrectly.

[^2]: The `~object.__hash__`{.interpreted-text role="meth"}, `~object.__iter__`{.interpreted-text role="meth"}, `~object.__reversed__`{.interpreted-text role="meth"}, `~object.__contains__`{.interpreted-text role="meth"}, `~object.__class_getitem__`{.interpreted-text role="meth"} and `~os.PathLike.__fspath__`{.interpreted-text role="meth"} methods have special handling for this. Others will still raise a `TypeError`{.interpreted-text role="exc"}, but may do so by relying on the behavior that `None` is not callable.

[^3]: \"Does not support\" here means that the class has no such method, or the method returns `NotImplemented`{.interpreted-text role="data"}. Do not set the method to `None` if you want to force fallback to the right operand\'s reflected method---that will instead have the opposite effect of explicitly *blocking* such fallback.

[^4]: For operands of the same type, it is assumed that if the non-reflected method (such as `~object.__add__`{.interpreted-text role="meth"}) fails then the operation is not supported, which is why the reflected method is not called.

[^5]: If the right operand\'s type is a subclass of the left operand\'s type, the reflected method having precedence allows subclasses to override their ancestors\' operations.
