# `!collections.abc`{.interpreted-text role="mod"} \-\-- Abstract Base Classes for Containers

::: {.module synopsis="Abstract base classes for containers"}
collections.abc
:::

::: versionadded
3.3 Formerly, this module was part of the `collections`{.interpreted-text role="mod"} module.
:::

**Source code:** `Lib/_collections_abc.py`{.interpreted-text role="source"}

::: testsetup
- 

from collections.abc import \* import itertools \_\_name\_\_ = \'\<doctest\>\'
:::

------------------------------------------------------------------------

This module provides `abstract base classes <abstract base class>`{.interpreted-text role="term"} that can be used to test whether a class provides a particular interface; for example, whether it is `hashable`{.interpreted-text role="term"} or whether it is a `mapping`{.interpreted-text role="term"}.

An `issubclass`{.interpreted-text role="func"} or `isinstance`{.interpreted-text role="func"} test for an interface works in one of three ways.

1)  A newly written class can inherit directly from one of the abstract base classes. The class must supply the required abstract methods. The remaining mixin methods come from inheritance and can be overridden if desired. Other methods may be added as needed:

    ::: testcode

    class C(Sequence): \# Direct inheritance

    :   def \_\_init\_\_(self): \... \# Extra method not required by the ABC def \_\_getitem\_\_(self, index): \... \# Required abstract method def \_\_len\_\_(self): \... \# Required abstract method def count(self, value): \... \# Optionally override a mixin method
    :::

    ::: doctest
    \>\>\> issubclass(C, Sequence) True \>\>\> isinstance(C(), Sequence) True
    :::

2)  Existing classes and built-in classes can be registered as \"virtual subclasses\" of the ABCs. Those classes should define the full API including all of the abstract methods and all of the mixin methods. This lets users rely on `issubclass`{.interpreted-text role="func"} or `isinstance`{.interpreted-text role="func"} tests to determine whether the full interface is supported. The exception to this rule is for methods that are automatically inferred from the rest of the API:

    ::: testcode

    class D: \# No inheritance

    :   def \_\_init\_\_(self): \... \# Extra method not required by the ABC def \_\_getitem\_\_(self, index): \... \# Abstract method def \_\_len\_\_(self): \... \# Abstract method def count(self, value): \... \# Mixin method def index(self, value): \... \# Mixin method

    Sequence.register(D) \# Register instead of inherit
    :::

    ::: doctest
    \>\>\> issubclass(D, Sequence) True \>\>\> isinstance(D(), Sequence) True
    :::

    In this example, class `!D`{.interpreted-text role="class"} does not need to define `__contains__`, `__iter__`, and `__reversed__` because the `in-operator <comparisons>`{.interpreted-text role="ref"}, the `iteration <iterable>`{.interpreted-text role="term"} logic, and the `reversed`{.interpreted-text role="func"} function automatically fall back to using `__getitem__` and `__len__`.

3)  Some simple interfaces are directly recognizable by the presence of the required methods (unless those methods have been set to `None`{.interpreted-text role="const"}):

    ::: testcode

    class E:

    :   def \_\_iter\_\_(self): \... def \_\_next\_\_(self): \...
    :::

    ::: doctest
    \>\>\> issubclass(E, Iterable) True \>\>\> isinstance(E(), Iterable) True
    :::

    Complex interfaces do not support this last technique because an interface is more than just the presence of method names. Interfaces specify semantics and relationships between methods that cannot be inferred solely from the presence of specific method names. For example, knowing that a class supplies `__getitem__`, `__len__`, and `__iter__` is insufficient for distinguishing a `Sequence`{.interpreted-text role="class"} from a `Mapping`{.interpreted-text role="class"}.

::: versionadded
3.9 These abstract classes now support `[]`. See `types-genericalias`{.interpreted-text role="ref"} and `585`{.interpreted-text role="pep"}.
:::

## Collections Abstract Base Classes

The collections module offers the following `ABCs <abstract base class>`{.interpreted-text role="term"}:

::: tabularcolumns
[\|l\|](##SUBST##|l|)L[\|L\|](##SUBST##|L|)L\|
:::

  ABC                                                     Inherits from                                                                                                                      Abstract Methods                                                     Mixin Methods
  ------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------
  `Container`{.interpreted-text role="class"}[^1]                                                                                                                                            `__contains__`                                                       
  `Hashable`{.interpreted-text role="class"}[^2]                                                                                                                                             `__hash__`                                                           
  `Iterable`{.interpreted-text role="class"}[^3][^4]                                                                                                                                         `__iter__`                                                           
  `Iterator`{.interpreted-text role="class"}[^5]          `Iterable`{.interpreted-text role="class"}                                                                                         `__next__`                                                           `__iter__`
  `Reversible`{.interpreted-text role="class"}[^6]        `Iterable`{.interpreted-text role="class"}                                                                                         `__reversed__`                                                       
  `Generator`{.interpreted-text role="class"}[^7]         `Iterator`{.interpreted-text role="class"}                                                                                         `send`, `throw`                                                      `close`, `__iter__`, `__next__`
  `Sized`{.interpreted-text role="class"}[^8]                                                                                                                                                `__len__`                                                            
  `Callable`{.interpreted-text role="class"}[^9]                                                                                                                                             `__call__`                                                           
  `Collection`{.interpreted-text role="class"}[^10]       `Sized`{.interpreted-text role="class"}, `Iterable`{.interpreted-text role="class"}, `Container`{.interpreted-text role="class"}   `__contains__`, `__iter__`, `__len__`                                
  `Sequence`{.interpreted-text role="class"}              `Reversible`{.interpreted-text role="class"}, `Collection`{.interpreted-text role="class"}                                         `__getitem__`, `__len__`                                             `__contains__`, `__iter__`, `__reversed__`, `index`, and `count`
  `MutableSequence`{.interpreted-text role="class"}       `Sequence`{.interpreted-text role="class"}                                                                                         `__getitem__`, `__setitem__`, `__delitem__`, `__len__`, `insert`     Inherited `Sequence`{.interpreted-text role="class"} methods and `append`, `clear`, `reverse`, `extend`, `pop`, `remove`, and `__iadd__`
  `ByteString`{.interpreted-text role="class"}            `Sequence`{.interpreted-text role="class"}                                                                                         `__getitem__`, `__len__`                                             Inherited `Sequence`{.interpreted-text role="class"} methods
  `Set`{.interpreted-text role="class"}                   `Collection`{.interpreted-text role="class"}                                                                                       `__contains__`, `__iter__`, `__len__`                                `__le__`, `__lt__`, `__eq__`, `__ne__`, `__gt__`, `__ge__`, `__and__`, `__or__`, `__sub__`, `__rsub__`, `__xor__`, `__rxor__` and `isdisjoint`
  `MutableSet`{.interpreted-text role="class"}            `Set`{.interpreted-text role="class"}                                                                                              `__contains__`, `__iter__`, `__len__`, `add`, `discard`              Inherited `Set`{.interpreted-text role="class"} methods and `clear`, `pop`, `remove`, `__ior__`, `__iand__`, `__ixor__`, and `__isub__`
  `Mapping`{.interpreted-text role="class"}               `Collection`{.interpreted-text role="class"}                                                                                       `__getitem__`, `__iter__`, `__len__`                                 `__contains__`, `keys`, `items`, `values`, `get`, `__eq__`, and `__ne__`
  `MutableMapping`{.interpreted-text role="class"}        `Mapping`{.interpreted-text role="class"}                                                                                          `__getitem__`, `__setitem__`, `__delitem__`, `__iter__`, `__len__`   Inherited `Mapping`{.interpreted-text role="class"} methods and `pop`, `popitem`, `clear`, `update`, and `setdefault`
  `MappingView`{.interpreted-text role="class"}           `Sized`{.interpreted-text role="class"}                                                                                                                                                                 `__init__`, `__len__` and `__repr__`
  `ItemsView`{.interpreted-text role="class"}             `MappingView`{.interpreted-text role="class"}, `Set`{.interpreted-text role="class"}                                                                                                                    `__contains__`, `__iter__`
  `KeysView`{.interpreted-text role="class"}              `MappingView`{.interpreted-text role="class"}, `Set`{.interpreted-text role="class"}                                                                                                                    `__contains__`, `__iter__`
  `ValuesView`{.interpreted-text role="class"}            `MappingView`{.interpreted-text role="class"}, `Collection`{.interpreted-text role="class"}                                                                                                             `__contains__`, `__iter__`
  `Awaitable`{.interpreted-text role="class"}[^11]                                                                                                                                           `__await__`                                                          
  `Coroutine`{.interpreted-text role="class"}[^12]        `Awaitable`{.interpreted-text role="class"}                                                                                        `send`, `throw`                                                      `close`
  `AsyncIterable`{.interpreted-text role="class"}[^13]                                                                                                                                       `__aiter__`                                                          
  `AsyncIterator`{.interpreted-text role="class"}[^14]    `AsyncIterable`{.interpreted-text role="class"}                                                                                    `__anext__`                                                          `__aiter__`
  `AsyncGenerator`{.interpreted-text role="class"}[^15]   `AsyncIterator`{.interpreted-text role="class"}                                                                                    `asend`, `athrow`                                                    `aclose`, `__aiter__`, `__anext__`
  `Buffer`{.interpreted-text role="class"}[^16]                                                                                                                                              `__buffer__`                                                         

**Footnotes**

## Collections Abstract Base Classes \-- Detailed Descriptions

::: Container
ABC for classes that provide the `~object.__contains__`{.interpreted-text role="meth"} method.
:::

::: Hashable
ABC for classes that provide the `~object.__hash__`{.interpreted-text role="meth"} method.
:::

::: Sized
ABC for classes that provide the `~object.__len__`{.interpreted-text role="meth"} method.
:::

::: Callable
ABC for classes that provide the `~object.__call__`{.interpreted-text role="meth"} method.

See `annotating-callables`{.interpreted-text role="ref"} for details on how to use `!Callable`{.interpreted-text role="class"} in type annotations.
:::

::: Iterable
ABC for classes that provide the `~container.__iter__`{.interpreted-text role="meth"} method.

Checking `isinstance(obj, Iterable)` detects classes that are registered as `Iterable`{.interpreted-text role="class"} or that have an `~container.__iter__`{.interpreted-text role="meth"} method, but it does not detect classes that iterate with the `~object.__getitem__`{.interpreted-text role="meth"} method. The only reliable way to determine whether an object is `iterable`{.interpreted-text role="term"} is to call `iter(obj)`.
:::

:::: Collection
ABC for sized iterable container classes.

::: versionadded
3.6
:::
::::

::: Iterator
ABC for classes that provide the `~iterator.__iter__`{.interpreted-text role="meth"} and `~iterator.__next__`{.interpreted-text role="meth"} methods. See also the definition of `iterator`{.interpreted-text role="term"}.
:::

:::: Reversible
ABC for iterable classes that also provide the `~object.__reversed__`{.interpreted-text role="meth"} method.

::: versionadded
3.6
:::
::::

:::: Generator
ABC for `generator`{.interpreted-text role="term"} classes that implement the protocol defined in `342`{.interpreted-text role="pep"} that extends `iterators <iterator>`{.interpreted-text role="term"} with the `~generator.send`{.interpreted-text role="meth"}, `~generator.throw`{.interpreted-text role="meth"} and `~generator.close`{.interpreted-text role="meth"} methods.

See `annotating-generators-and-coroutines`{.interpreted-text role="ref"} for details on using `!Generator`{.interpreted-text role="class"} in type annotations.

::: versionadded
3.5
:::
::::

:::::: {.Sequence .MutableSequence .ByteString}
ABCs for read-only and mutable `sequences <sequence>`{.interpreted-text role="term"}.

Implementation note: Some of the mixin methods, such as `~container.__iter__`{.interpreted-text role="meth"}, `~object.__reversed__`{.interpreted-text role="meth"}, and `~sequence.index`{.interpreted-text role="meth"} make repeated calls to the underlying `~object.__getitem__`{.interpreted-text role="meth"} method. Consequently, if `~object.__getitem__`{.interpreted-text role="meth"} is implemented with constant access speed, the mixin methods will have linear performance; however, if the underlying method is linear (as it would be with a linked list), the mixins will have quadratic performance and will likely need to be overridden.

:::: method
index(value, start=0, stop=None)

Return first index of *value*.

Raises `ValueError`{.interpreted-text role="exc"} if the value is not present.

Supporting the *start* and *stop* arguments is optional, but recommended.

::: versionchanged
3.5 The `~sequence.index`{.interpreted-text role="meth"} method gained support for the *stop* and *start* arguments.
:::
::::

::: deprecated-removed
3.12 3.17 The `ByteString`{.interpreted-text role="class"} ABC has been deprecated.

Use `isinstance(obj, collections.abc.Buffer)` to test if `obj` implements the `buffer protocol <bufferobjects>`{.interpreted-text role="ref"} at runtime. For use in type annotations, either use `Buffer`{.interpreted-text role="class"} or a union that explicitly specifies the types your code supports (e.g., `bytes | bytearray | memoryview`).

`!ByteString`{.interpreted-text role="class"} was originally intended to be an abstract class that would serve as a supertype of both `bytes`{.interpreted-text role="class"} and `bytearray`{.interpreted-text role="class"}. However, since the ABC never had any methods, knowing that an object was an instance of `!ByteString`{.interpreted-text role="class"} never actually told you anything useful about the object. Other common buffer types such as `memoryview`{.interpreted-text role="class"} were also never understood as subtypes of `!ByteString`{.interpreted-text role="class"} (either at runtime or by static type checkers).

See `PEP 688 <688#current-options>`{.interpreted-text role="pep"} for more details.
:::
::::::

::: {.Set .MutableSet}
ABCs for read-only and mutable `sets <types-set>`{.interpreted-text role="ref"}.
:::

::: {.Mapping .MutableMapping}
ABCs for read-only and mutable `mappings <mapping>`{.interpreted-text role="term"}.
:::

::: {.MappingView .ItemsView .KeysView .ValuesView}
ABCs for mapping, items, keys, and values `views <dictionary view>`{.interpreted-text role="term"}.
:::

:::::: Awaitable
ABC for `awaitable`{.interpreted-text role="term"} objects, which can be used in `await`{.interpreted-text role="keyword"} expressions. Custom implementations must provide the `~object.__await__`{.interpreted-text role="meth"} method.

`Coroutine <coroutine>`{.interpreted-text role="term"} objects and instances of the `~collections.abc.Coroutine`{.interpreted-text role="class"} ABC are all instances of this ABC.

:::: note
::: title
Note
:::

In CPython, generator-based coroutines (`generators <generator>`{.interpreted-text role="term"} decorated with `types.coroutine`{.interpreted-text role="deco"}) are *awaitables*, even though they do not have an `~object.__await__`{.interpreted-text role="meth"} method. Using `isinstance(gencoro, Awaitable)` for them will return `False`. Use `inspect.isawaitable`{.interpreted-text role="func"} to detect them.
::::

::: versionadded
3.5
:::
::::::

:::::: Coroutine
ABC for `coroutine`{.interpreted-text role="term"} compatible classes. These implement the following methods, defined in `coroutine-objects`{.interpreted-text role="ref"}: `~coroutine.send`{.interpreted-text role="meth"}, `~coroutine.throw`{.interpreted-text role="meth"}, and `~coroutine.close`{.interpreted-text role="meth"}. Custom implementations must also implement `~object.__await__`{.interpreted-text role="meth"}. All `Coroutine`{.interpreted-text role="class"} instances are also instances of `Awaitable`{.interpreted-text role="class"}.

:::: note
::: title
Note
:::

In CPython, generator-based coroutines (`generators <generator>`{.interpreted-text role="term"} decorated with `types.coroutine`{.interpreted-text role="deco"}) are *awaitables*, even though they do not have an `~object.__await__`{.interpreted-text role="meth"} method. Using `isinstance(gencoro, Coroutine)` for them will return `False`. Use `inspect.isawaitable`{.interpreted-text role="func"} to detect them.
::::

See `annotating-generators-and-coroutines`{.interpreted-text role="ref"} for details on using `!Coroutine`{.interpreted-text role="class"} in type annotations. The variance and order of type parameters correspond to those of `Generator`{.interpreted-text role="class"}.

::: versionadded
3.5
:::
::::::

:::: AsyncIterable
ABC for classes that provide an `__aiter__` method. See also the definition of `asynchronous iterable`{.interpreted-text role="term"}.

::: versionadded
3.5
:::
::::

:::: AsyncIterator
ABC for classes that provide `__aiter__` and `__anext__` methods. See also the definition of `asynchronous iterator`{.interpreted-text role="term"}.

::: versionadded
3.5
:::
::::

:::: AsyncGenerator
ABC for `asynchronous generator`{.interpreted-text role="term"} classes that implement the protocol defined in `525`{.interpreted-text role="pep"} and `492`{.interpreted-text role="pep"}.

See `annotating-generators-and-coroutines`{.interpreted-text role="ref"} for details on using `!AsyncGenerator`{.interpreted-text role="class"} in type annotations.

::: versionadded
3.6
:::
::::

:::: Buffer
ABC for classes that provide the `~object.__buffer__`{.interpreted-text role="meth"} method, implementing the `buffer protocol <bufferobjects>`{.interpreted-text role="ref"}. See `688`{.interpreted-text role="pep"}.

::: versionadded
3.12
:::
::::

## Examples and Recipes

ABCs allow us to ask classes or instances if they provide particular functionality, for example:

    size = None
    if isinstance(myvar, collections.abc.Sized):
        size = len(myvar)

Several of the ABCs are also useful as mixins that make it easier to develop classes supporting container APIs. For example, to write a class supporting the full `Set`{.interpreted-text role="class"} API, it is only necessary to supply the three underlying abstract methods: `~object.__contains__`{.interpreted-text role="meth"}, `~container.__iter__`{.interpreted-text role="meth"}, and `~object.__len__`{.interpreted-text role="meth"}. The ABC supplies the remaining methods such as `!__and__`{.interpreted-text role="meth"} and `~frozenset.isdisjoint`{.interpreted-text role="meth"}:

    class ListBasedSet(collections.abc.Set):
        ''' Alternate set implementation favoring space over speed
            and not requiring the set elements to be hashable. '''
        def __init__(self, iterable):
            self.elements = lst = []
            for value in iterable:
                if value not in lst:
                    lst.append(value)

        def __iter__(self):
            return iter(self.elements)

        def __contains__(self, value):
            return value in self.elements

        def __len__(self):
            return len(self.elements)

    s1 = ListBasedSet('abcdef')
    s2 = ListBasedSet('defghi')
    overlap = s1 & s2            # The __and__() method is supported automatically

Notes on using `Set`{.interpreted-text role="class"} and `MutableSet`{.interpreted-text role="class"} as a mixin:

\(1\)

:   Since some set operations create new sets, the default mixin methods need a way to create new instances from an `iterable`{.interpreted-text role="term"}. The class constructor is assumed to have a signature in the form `ClassName(iterable)`. That assumption is factored-out to an internal `classmethod`{.interpreted-text role="class"} called `!_from_iterable`{.interpreted-text role="meth"} which calls `cls(iterable)` to produce a new set. If the `Set`{.interpreted-text role="class"} mixin is being used in a class with a different constructor signature, you will need to override `!_from_iterable`{.interpreted-text role="meth"} with a classmethod or regular method that can construct new instances from an iterable argument.

\(2\)

:   To override the comparisons (presumably for speed, as the semantics are fixed), redefine `~object.__le__`{.interpreted-text role="meth"} and `~object.__ge__`{.interpreted-text role="meth"}, then the other operations will automatically follow suit.

\(3\)

:   The `Set`{.interpreted-text role="class"} mixin provides a `!_hash`{.interpreted-text role="meth"} method to compute a hash value for the set; however, `~object.__hash__`{.interpreted-text role="meth"} is not defined because not all sets are `hashable`{.interpreted-text role="term"} or immutable. To add set hashability using mixins, inherit from both `Set`{.interpreted-text role="meth"} and `Hashable`{.interpreted-text role="meth"}, then define `__hash__ = Set._hash`.

::: seealso
- [OrderedSet recipe](https://code.activestate.com/recipes/576694/) for an example built on `MutableSet`{.interpreted-text role="class"}.
- For more about ABCs, see the `abc`{.interpreted-text role="mod"} module and `3119`{.interpreted-text role="pep"}.
:::

[^1]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.

[^2]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.

[^3]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.

[^4]: Checking `isinstance(obj, Iterable)` detects classes that are registered as `Iterable`{.interpreted-text role="class"} or that have an `~container.__iter__`{.interpreted-text role="meth"} method, but it does not detect classes that iterate with the `~object.__getitem__`{.interpreted-text role="meth"} method. The only reliable way to determine whether an object is `iterable`{.interpreted-text role="term"} is to call `iter(obj)`.

[^5]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.

[^6]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.

[^7]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.

[^8]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.

[^9]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.

[^10]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.

[^11]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.

[^12]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.

[^13]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.

[^14]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.

[^15]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.

[^16]: These ABCs override `~abc.ABCMeta.__subclasshook__`{.interpreted-text role="meth"} to support testing an interface by verifying the required methods are present and have not been set to `None`{.interpreted-text role="const"}. This only works for simple interfaces. More complex interfaces require registration or direct subclassing.
