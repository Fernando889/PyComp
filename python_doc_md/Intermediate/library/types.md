# `!types`{.interpreted-text role="mod"} \-\-- Dynamic type creation and names for built-in types

::: {.module synopsis="Names for built-in types."}
types
:::

**Source code:** `Lib/types.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module defines utility functions to assist in dynamic creation of new types.

It also defines names for some object types that are used by the standard Python interpreter, but not exposed as builtins like `int`{.interpreted-text role="class"} or `str`{.interpreted-text role="class"} are.

Finally, it provides some additional type-related utility classes and functions that are not fundamental enough to be builtins.

## Dynamic Type Creation

:::: function
new_class(name, bases=(), kwds=None, exec_body=None)

Creates a class object dynamically using the appropriate metaclass.

The first three arguments are the components that make up a class definition header: the class name, the base classes (in order), the keyword arguments (such as `metaclass`).

The *exec_body* argument is a callback that is used to populate the freshly created class namespace. It should accept the class namespace as its sole argument and update the namespace directly with the class contents. If no callback is provided, it has the same effect as passing in `lambda ns: None`.

::: versionadded
3.3
:::
::::

::::: function
prepare_class(name, bases=(), kwds=None)

Calculates the appropriate metaclass and creates the class namespace.

The arguments are the components that make up a class definition header: the class name, the base classes (in order) and the keyword arguments (such as `metaclass`).

The return value is a 3-tuple: `metaclass, namespace, kwds`

*metaclass* is the appropriate metaclass, *namespace* is the prepared class namespace and *kwds* is an updated copy of the passed in *kwds* argument with any `'metaclass'` entry removed. If no *kwds* argument is passed in, this will be an empty dict.

::: versionadded
3.3
:::

::: versionchanged
3.6

The default value for the `namespace` element of the returned tuple has changed. Now an insertion-order-preserving mapping is used when the metaclass does not have a `__prepare__` method.
:::
:::::

::: seealso

`metaclasses`{.interpreted-text role="ref"}

:   Full details of the class creation process supported by these functions

`3115`{.interpreted-text role="pep"} - Metaclasses in Python 3000

:   Introduced the `__prepare__` namespace hook
:::

:::: function
resolve_bases(bases)

Resolve MRO entries dynamically as specified by `560`{.interpreted-text role="pep"}.

This function looks for items in *bases* that are not instances of `type`{.interpreted-text role="class"}, and returns a tuple where each such object that has an `~object.__mro_entries__`{.interpreted-text role="meth"} method is replaced with an unpacked result of calling this method. If a *bases* item is an instance of `type`{.interpreted-text role="class"}, or it doesn\'t have an `!__mro_entries__`{.interpreted-text role="meth"} method, then it is included in the return tuple unchanged.

::: versionadded
3.7
:::
::::

:::: function
get_original_bases(cls, /)

Return the tuple of objects originally given as the bases of *cls* before the `~object.__mro_entries__`{.interpreted-text role="meth"} method has been called on any bases (following the mechanisms laid out in `560`{.interpreted-text role="pep"}). This is useful for introspecting `Generics <user-defined-generics>`{.interpreted-text role="ref"}.

For classes that have an `__orig_bases__` attribute, this function returns the value of `cls.__orig_bases__`. For classes without the `__orig_bases__` attribute, `cls.__bases__ <type.__bases__>`{.interpreted-text role="attr"} is returned.

Examples:

    from typing import TypeVar, Generic, NamedTuple, TypedDict

    T = TypeVar("T")
    class Foo(Generic[T]): ...
    class Bar(Foo[int], float): ...
    class Baz(list[str]): ...
    Eggs = NamedTuple("Eggs", [("a", int), ("b", str)])
    Spam = TypedDict("Spam", {"a": int, "b": str})

    assert Bar.__bases__ == (Foo, float)
    assert get_original_bases(Bar) == (Foo[int], float)

    assert Baz.__bases__ == (list,)
    assert get_original_bases(Baz) == (list[str],)

    assert Eggs.__bases__ == (tuple,)
    assert get_original_bases(Eggs) == (NamedTuple,)

    assert Spam.__bases__ == (dict,)
    assert get_original_bases(Spam) == (TypedDict,)

    assert int.__bases__ == (object,)
    assert get_original_bases(int) == (object,)

::: versionadded
3.12
:::
::::

::: seealso
`560`{.interpreted-text role="pep"} - Core support for typing module and generic types
:::

## Standard Interpreter Types

This module provides names for many of the types that are required to implement a Python interpreter. It deliberately avoids including some of the types that arise only incidentally during processing such as the `listiterator` type.

Typical use of these names is for `isinstance`{.interpreted-text role="func"} or `issubclass`{.interpreted-text role="func"} checks.

If you instantiate any of these types, note that signatures may vary between Python versions.

Standard names are defined for the following types:

:::: data
NoneType

The type of `None`{.interpreted-text role="data"}.

::: versionadded
3.10
:::
::::

:::: data
FunctionType LambdaType

The type of user-defined functions and functions created by `lambda`{.interpreted-text role="keyword"} expressions.

::: audit-event
function.\_\_new\_\_ code types.FunctionType
:::

The audit event only occurs for direct instantiation of function objects, and is not raised for normal compilation.
::::

::: data
GeneratorType

The type of `generator`{.interpreted-text role="term"}-iterator objects, created by generator functions.
:::

:::: data
CoroutineType

The type of `coroutine`{.interpreted-text role="term"} objects, created by `async def`{.interpreted-text role="keyword"} functions.

::: versionadded
3.5
:::
::::

:::: data
AsyncGeneratorType

The type of `asynchronous generator`{.interpreted-text role="term"}-iterator objects, created by asynchronous generator functions.

::: versionadded
3.6
:::
::::

::::: CodeType(**kwargs)
::: index
pair: built-in function; compile
:::

The type of `code objects <code-objects>`{.interpreted-text role="ref"} such as returned by `compile`{.interpreted-text role="func"}.

::: audit-event
code.\_\_new\_\_ code,filename,name,argcount,posonlyargcount,kwonlyargcount,nlocals,stacksize,flags types.CodeType
:::

Note that the audited arguments may not match the names or positions required by the initializer. The audit event only occurs for direct instantiation of code objects, and is not raised for normal compilation.
:::::

:::: data
CellType

The type for cell objects: such objects are used as containers for a function\'s `closure variables <closure variable>`{.interpreted-text role="term"}.

::: versionadded
3.8
:::
::::

::: data
MethodType

The type of methods of user-defined class instances.
:::

::: data
BuiltinFunctionType BuiltinMethodType

The type of built-in functions like `len`{.interpreted-text role="func"} or `sys.exit`{.interpreted-text role="func"}, and methods of built-in classes. (Here, the term \"built-in\" means \"written in C\".)
:::

:::: data
WrapperDescriptorType

The type of methods of some built-in data types and base classes such as `object.__init__`{.interpreted-text role="meth"} or `object.__lt__`{.interpreted-text role="meth"}.

::: versionadded
3.7
:::
::::

:::: data
MethodWrapperType

The type of *bound* methods of some built-in data types and base classes. For example it is the type of `object().__str__`.

::: versionadded
3.7
:::
::::

:::: data
NotImplementedType

The type of `NotImplemented`{.interpreted-text role="data"}.

::: versionadded
3.10
:::
::::

:::: data
MethodDescriptorType

The type of methods of some built-in data types such as `str.join`{.interpreted-text role="meth"}.

::: versionadded
3.7
:::
::::

:::: data
ClassMethodDescriptorType

The type of *unbound* class methods of some built-in data types such as `dict.__dict__['fromkeys']`.

::: versionadded
3.7
:::
::::

:::: {.ModuleType(name, .doc=None)}
The type of `modules <module>`{.interpreted-text role="term"}. The constructor takes the name of the module to be created and optionally its `docstring`{.interpreted-text role="term"}.

::: seealso

`Documentation on module objects <module-objects>`{.interpreted-text role="ref"}

:   Provides details on the special attributes that can be found on instances of `!ModuleType`{.interpreted-text role="class"}.

`importlib.util.module_from_spec`{.interpreted-text role="func"}

:   Modules created using the `!ModuleType`{.interpreted-text role="class"} constructor are created with many of their special attributes unset or set to default values. `!module_from_spec`{.interpreted-text role="func"} provides a more robust way of creating `!ModuleType`{.interpreted-text role="class"} instances which ensures the various attributes are set appropriately.
:::
::::

:::: data
EllipsisType

The type of `Ellipsis`{.interpreted-text role="data"}.

::: versionadded
3.10
:::
::::

:::::: {.GenericAlias(t_origin, .t_args)}
The type of `parameterized generics <types-genericalias>`{.interpreted-text role="ref"} such as `list[int]`.

`t_origin` should be a non-parameterized generic class, such as `list`, `tuple` or `dict`. `t_args` should be a `tuple`{.interpreted-text role="class"} (possibly of length 1) of types which parameterize `t_origin`:

    >>> from types import GenericAlias

    >>> list[int] == GenericAlias(list, (int,))
    True
    >>> dict[str, int] == GenericAlias(dict, (str, int))
    True

::: versionadded
3.9
:::

::: versionchanged
3.9.2 This type can now be subclassed.
:::

::: seealso

`Generic Alias Types<types-genericalias>`{.interpreted-text role="ref"}

:   In-depth documentation on instances of `!types.GenericAlias`{.interpreted-text role="class"}

`585`{.interpreted-text role="pep"} - Type Hinting Generics In Standard Collections

:   Introducing the `!types.GenericAlias`{.interpreted-text role="class"} class
:::
::::::

::::: UnionType
The type of `union type expressions<types-union>`{.interpreted-text role="ref"}.

::: versionadded
3.10
:::

::: versionchanged
3.14

This is now an alias for `typing.Union`{.interpreted-text role="class"}.
:::
:::::

::: {.TracebackType(tb_next, .tb_frame, .tb_lasti, .tb_lineno)}
The type of traceback objects such as found in `sys.exception().__traceback__`.

See `the language reference <traceback-objects>`{.interpreted-text role="ref"} for details of the available attributes and operations, and guidance on creating tracebacks dynamically.
:::

::: data
FrameType

The type of `frame objects <frame-objects>`{.interpreted-text role="ref"} such as found in `tb.tb_frame <traceback.tb_frame>`{.interpreted-text role="attr"} if `tb` is a traceback object.
:::

::::: data
FrameLocalsProxyType

The type of frame locals proxy objects, as found on the `frame.f_locals`{.interpreted-text role="attr"} attribute.

::: versionadded
3.15
:::

::: seealso
`667`{.interpreted-text role="pep"}
:::
:::::

::::: data
LazyImportType

The type of lazy import proxy objects. These objects are created when a module is lazily imported and serve as placeholders until the module is actually accessed. This type can be used to detect lazy imports programmatically.

::: versionadded
next
:::

::: seealso
`810`{.interpreted-text role="pep"}
:::
:::::

::: data
GetSetDescriptorType

The type of objects defined in extension modules with `PyGetSetDef`, such as `FrameType.f_locals <frame.f_locals>`{.interpreted-text role="attr"} or `array.array.typecode`. This type is used as descriptor for object attributes; it has the same purpose as the `property`{.interpreted-text role="class"} type, but for classes defined in extension modules.
:::

:::: data
MemberDescriptorType

The type of objects defined in extension modules with `PyMemberDef`, such as `datetime.timedelta.days`. This type is used as descriptor for simple C data members which use standard conversion functions; it has the same purpose as the `property`{.interpreted-text role="class"} type, but for classes defined in extension modules.

In addition, when a class is defined with a `~object.__slots__`{.interpreted-text role="attr"} attribute, then for each slot, an instance of `!MemberDescriptorType`{.interpreted-text role="class"} will be added as an attribute on the class. This allows the slot to appear in the class\'s `~type.__dict__`{.interpreted-text role="attr"}.

::: impl-detail
In other implementations of Python, this type may be identical to `GetSetDescriptorType`.
:::
::::

:::::::::::::::::: MappingProxyType(mapping)
Read-only proxy of a mapping. It provides a dynamic view on the mapping\'s entries, which means that when the mapping changes, the view reflects these changes.

::: versionadded
3.3
:::

::: versionchanged
3.9

Updated to support the new union (`|`) operator from `584`{.interpreted-text role="pep"}, which simply delegates to the underlying mapping.
:::

::: describe
key in proxy

Return `True` if the underlying mapping has a key *key*, else `False`.
:::

::: describe
proxy\[key\]

Return the item of the underlying mapping with key *key*. Raises a `KeyError`{.interpreted-text role="exc"} if *key* is not in the underlying mapping.
:::

::: describe
iter(proxy)

Return an iterator over the keys of the underlying mapping. This is a shortcut for `iter(proxy.keys())`.
:::

::: describe
len(proxy)

Return the number of items in the underlying mapping.
:::

::: method
copy()

Return a shallow copy of the underlying mapping.
:::

::: method
get(key\[, default\])

Return the value for *key* if *key* is in the underlying mapping, else *default*. If *default* is not given, it defaults to `None`, so that this method never raises a `KeyError`{.interpreted-text role="exc"}.
:::

::: method
items()

Return a new view of the underlying mapping\'s items (`(key, value)` pairs).
:::

::: method
keys()

Return a new view of the underlying mapping\'s keys.
:::

::: method
values()

Return a new view of the underlying mapping\'s values.
:::

:::: describe
reversed(proxy)

Return a reverse iterator over the keys of the underlying mapping.

::: versionadded
3.9
:::
::::

:::: describe
hash(proxy)

Return a hash of the underlying mapping.

::: versionadded
3.12
:::
::::
::::::::::::::::::

:::: CapsuleType
The type of `capsule objects <capsules>`{.interpreted-text role="ref"}.

::: versionadded
3.13
:::
::::

## Additional Utility Classes and Functions

:::::: SimpleNamespace
A simple `object`{.interpreted-text role="class"} subclass that provides attribute access to its namespace, as well as a meaningful repr.

Unlike `object`{.interpreted-text role="class"}, with `!SimpleNamespace`{.interpreted-text role="class"} you can add and remove attributes.

`SimpleNamespace`{.interpreted-text role="py:class"} objects may be initialized in the same way as `dict`{.interpreted-text role="class"}: either with keyword arguments, with a single positional argument, or with both. When initialized with keyword arguments, those are directly added to the underlying namespace. Alternatively, when initialized with a positional argument, the underlying namespace will be updated with key-value pairs from that argument (either a mapping object or an `iterable`{.interpreted-text role="term"} object producing key-value pairs). All such keys must be strings.

The type is roughly equivalent to the following code:

    class SimpleNamespace:
        def __init__(self, mapping_or_iterable=(), /, **kwargs):
            self.__dict__.update(mapping_or_iterable)
            self.__dict__.update(kwargs)

        def __repr__(self):
            items = (f"{k}={v!r}" for k, v in self.__dict__.items())
            return "{}({})".format(type(self).__name__, ", ".join(items))

        def __eq__(self, other):
            if isinstance(self, SimpleNamespace) and isinstance(other, SimpleNamespace):
               return self.__dict__ == other.__dict__
            return NotImplemented

`SimpleNamespace` may be useful as a replacement for `class NS: pass`. However, for a structured record type use `~collections.namedtuple`{.interpreted-text role="func"} instead.

`!SimpleNamespace`{.interpreted-text role="class"} objects are supported by `copy.replace`{.interpreted-text role="func"}.

::: versionadded
3.3
:::

::: versionchanged
3.9 Attribute order in the repr changed from alphabetical to insertion (like `dict`).
:::

::: versionchanged
3.13 Added support for an optional positional argument.
:::
::::::

:::: function
DynamicClassAttribute(fget=None, fset=None, fdel=None, doc=None)

Route attribute access on a class to \_\_getattr\_\_.

This is a descriptor, used to define attributes that act differently when accessed through an instance and through a class. Instance access remains normal, but access to an attribute through a class will be routed to the class\'s \_\_getattr\_\_ method; this is done by raising AttributeError.

This allows one to have properties active on an instance, and have virtual attributes on the class with the same name (see `enum.Enum`{.interpreted-text role="class"} for an example).

::: versionadded
3.4
:::
::::

## Coroutine Utility Functions

:::: function
coroutine(gen_func)

This function transforms a `generator`{.interpreted-text role="term"} function into a `coroutine function`{.interpreted-text role="term"} which returns a generator-based coroutine. The generator-based coroutine is still a `generator iterator`{.interpreted-text role="term"}, but is also considered to be a `coroutine`{.interpreted-text role="term"} object and is `awaitable`{.interpreted-text role="term"}. However, it may not necessarily implement the `~object.__await__`{.interpreted-text role="meth"} method.

If *gen_func* is a generator function, it will be modified in-place.

If *gen_func* is not a generator function, it will be wrapped. If it returns an instance of `collections.abc.Generator`{.interpreted-text role="class"}, the instance will be wrapped in an *awaitable* proxy object. All other types of objects will be returned as is.

::: versionadded
3.5
:::
::::
