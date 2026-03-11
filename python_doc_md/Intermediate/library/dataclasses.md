# `!dataclasses`{.interpreted-text role="mod"} \-\-- Data Classes

::: {.module synopsis="Generate special methods on user-defined classes."}
dataclasses
:::

**Source code:** `Lib/dataclasses.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module provides a decorator and functions for automatically adding generated `special methods <special method>`{.interpreted-text role="term"} such as `~object.__init__`{.interpreted-text role="meth"} and `~object.__repr__`{.interpreted-text role="meth"} to user-defined classes. It was originally described in `557`{.interpreted-text role="pep"}.

The member variables to use in these generated methods are defined using `526`{.interpreted-text role="pep"} type annotations. For example, this code:

    from dataclasses import dataclass

    @dataclass
    class InventoryItem:
        """Class for keeping track of an item in inventory."""
        name: str
        unit_price: float
        quantity_on_hand: int = 0

        def total_cost(self) -> float:
            return self.unit_price * self.quantity_on_hand

will add, among other things, a `!__init__`{.interpreted-text role="meth"} that looks like:

    def __init__(self, name: str, unit_price: float, quantity_on_hand: int = 0):
        self.name = name
        self.unit_price = unit_price
        self.quantity_on_hand = quantity_on_hand

Note that this method is automatically added to the class: it is not directly specified in the `!InventoryItem`{.interpreted-text role="class"} definition shown above.

::: versionadded
3.7
:::

## Module contents

::: decorator
dataclass(\*, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False, weakref_slot=False)

This function is a `decorator`{.interpreted-text role="term"} that is used to add generated `special methods <special method>`{.interpreted-text role="term"} to classes, as described below.

The `@dataclass` decorator examines the class to find `field`s. A `field` is defined as a class variable that has a `type annotation <variable annotation>`{.interpreted-text role="term"}. With two exceptions described below, nothing in `@dataclass` examines the type specified in the variable annotation.

The order of the fields in all of the generated methods is the order in which they appear in the class definition.

The `@dataclass` decorator will add various \"dunder\" methods to the class, described below. If any of the added methods already exist in the class, the behavior depends on the parameter, as documented below. The decorator returns the same class that it is called on; no new class is created.

If `@dataclass` is used just as a simple decorator with no parameters, it acts as if it has the default values documented in this signature. That is, these three uses of `@dataclass` are equivalent:

    @dataclass
    class C:
        ...

    @dataclass()
    class C:
        ...

    @dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False,
               match_args=True, kw_only=False, slots=False, weakref_slot=False)
    class C:
        ...

The parameters to `@dataclass` are:

- *init*: If true (the default), a `~object.__init__`{.interpreted-text role="meth"} method will be generated.

  If the class already defines `!__init__`{.interpreted-text role="meth"}, this parameter is ignored.

- *repr*: If true (the default), a `~object.__repr__`{.interpreted-text role="meth"} method will be generated. The generated repr string will have the class name and the name and repr of each field, in the order they are defined in the class. Fields that are marked as being excluded from the repr are not included. For example: `InventoryItem(name='widget', unit_price=3.0, quantity_on_hand=10)`.

  If the class already defines `!__repr__`{.interpreted-text role="meth"}, this parameter is ignored.

- *eq*: If true (the default), an `~object.__eq__`{.interpreted-text role="meth"} method will be generated. This method compares the class as if it were a tuple of its fields, in order. Both instances in the comparison must be of the identical type.

  If the class already defines `!__eq__`{.interpreted-text role="meth"}, this parameter is ignored.

- *order*: If true (the default is `False`), `~object.__lt__`{.interpreted-text role="meth"}, `~object.__le__`{.interpreted-text role="meth"}, `~object.__gt__`{.interpreted-text role="meth"}, and `~object.__ge__`{.interpreted-text role="meth"} methods will be generated. These compare the class as if it were a tuple of its fields, in order. Both instances in the comparison must be of the identical type. If *order* is true and *eq* is false, a `ValueError`{.interpreted-text role="exc"} is raised.

  If the class already defines any of `!__lt__`{.interpreted-text role="meth"}, `!__le__`{.interpreted-text role="meth"}, `!__gt__`{.interpreted-text role="meth"}, or `!__ge__`{.interpreted-text role="meth"}, then `TypeError`{.interpreted-text role="exc"} is raised.

- *unsafe_hash*: If true, force `dataclasses` to create a `~object.__hash__`{.interpreted-text role="meth"} method, even though it may not be safe to do so. Otherwise, generate a `~object.__hash__`{.interpreted-text role="meth"} method according to how *eq* and *frozen* are set. The default value is `False`.

  `!__hash__`{.interpreted-text role="meth"} is used by built-in `hash`{.interpreted-text role="meth"}, and when objects are added to hashed collections such as dictionaries and sets. Having a `!__hash__`{.interpreted-text role="meth"} implies that instances of the class are immutable. Mutability is a complicated property that depends on the programmer\'s intent, the existence and behavior of `!__eq__`{.interpreted-text role="meth"}, and the values of the *eq* and *frozen* flags in the `@dataclass` decorator.

  By default, `@dataclass` will not implicitly add a `~object.__hash__`{.interpreted-text role="meth"} method unless it is safe to do so. Neither will it add or change an existing explicitly defined `!__hash__`{.interpreted-text role="meth"} method. Setting the class attribute `__hash__ = None` has a specific meaning to Python, as described in the `!__hash__`{.interpreted-text role="meth"} documentation.

  If `!__hash__`{.interpreted-text role="meth"} is not explicitly defined, or if it is set to `None`, then `@dataclass` *may* add an implicit `!__hash__`{.interpreted-text role="meth"} method. Although not recommended, you can force `@dataclass` to create a `!__hash__`{.interpreted-text role="meth"} method with `unsafe_hash=True`. This might be the case if your class is logically immutable but can still be mutated. This is a specialized use case and should be considered carefully.

  Here are the rules governing implicit creation of a `!__hash__`{.interpreted-text role="meth"} method. Note that you cannot both have an explicit `!__hash__`{.interpreted-text role="meth"} method in your dataclass and set `unsafe_hash=True`; this will result in a `TypeError`{.interpreted-text role="exc"}.

  If *eq* and *frozen* are both true, by default `@dataclass` will generate a `!__hash__`{.interpreted-text role="meth"} method for you. If *eq* is true and *frozen* is false, `!__hash__`{.interpreted-text role="meth"} will be set to `None`, marking it unhashable (which it is, since it is mutable). If *eq* is false, `!__hash__`{.interpreted-text role="meth"} will be left untouched meaning the `!__hash__`{.interpreted-text role="meth"} method of the superclass will be used (if the superclass is `object`{.interpreted-text role="class"}, this means it will fall back to id-based hashing).

- *frozen*: If true (the default is `False`), assigning to fields will generate an exception. This emulates read-only frozen instances. See the `discussion <dataclasses-frozen>`{.interpreted-text role="ref"} below.

  If `~object.__setattr__`{.interpreted-text role="meth"} or `~object.__delattr__`{.interpreted-text role="meth"} is defined in the class and *frozen* is true, then `TypeError`{.interpreted-text role="exc"} is raised.

- *match_args*: If true (the default is `True`), the `~object.__match_args__`{.interpreted-text role="attr"} tuple will be created from the list of non keyword-only parameters to the generated `~object.__init__`{.interpreted-text role="meth"} method (even if `!__init__`{.interpreted-text role="meth"} is not generated, see above). If false, or if `!__match_args__`{.interpreted-text role="attr"} is already defined in the class, then `!__match_args__`{.interpreted-text role="attr"} will not be generated.

> ::: versionadded
> 3.10
> :::

- *kw_only*: If true (the default value is `False`), then all fields will be marked as keyword-only. If a field is marked as keyword-only, then the only effect is that the `~object.__init__`{.interpreted-text role="meth"} parameter generated from a keyword-only field must be specified with a keyword when `!__init__`{.interpreted-text role="meth"} is called. See the `parameter`{.interpreted-text role="term"} glossary entry for details. Also see the `KW_ONLY`{.interpreted-text role="const"} section.

  Keyword-only fields are not included in `!__match_args__`{.interpreted-text role="attr"}.

> ::: versionadded
> 3.10
> :::

- *slots*: If true (the default is `False`), `~object.__slots__`{.interpreted-text role="attr"} attribute will be generated and new class will be returned instead of the original one. If `!__slots__`{.interpreted-text role="attr"} is already defined in the class, then `TypeError`{.interpreted-text role="exc"} is raised.

> :::: warning
> ::: title
> Warning
> :::
>
> Passing parameters to a base class `~object.__init_subclass__`{.interpreted-text role="meth"} when using `slots=True` will result in a `TypeError`{.interpreted-text role="exc"}. Either use `__init_subclass__` with no parameters or use default values as a workaround. See `91126`{.interpreted-text role="gh"} for full details.
> ::::
>
> ::: versionadded
> 3.10
> :::
>
> ::: versionchanged
> 3.11 If a field name is already included in the `!__slots__`{.interpreted-text role="attr"} of a base class, it will not be included in the generated `!__slots__`{.interpreted-text role="attr"} to prevent `overriding them <datamodel-note-slots>`{.interpreted-text role="ref"}. Therefore, do not use `!__slots__`{.interpreted-text role="attr"} to retrieve the field names of a dataclass. Use `fields`{.interpreted-text role="func"} instead. To be able to determine inherited slots, base class `!__slots__`{.interpreted-text role="attr"} may be any iterable, but *not* an iterator.
> :::

- *weakref_slot*: If true (the default is `False`), add a slot named \"\_\_weakref\_\_\", which is required to make an instance `weakref-able <weakref.ref>`{.interpreted-text role="func"}. It is an error to specify `weakref_slot=True` without also specifying `slots=True`.

> ::: versionadded
> 3.11
> :::

`field`s may optionally specify a default value, using normal Python syntax:

    @dataclass
    class C:
        a: int       # 'a' has no default value
        b: int = 0   # assign a default value for 'b'

In this example, both `!a`{.interpreted-text role="attr"} and `!b`{.interpreted-text role="attr"} will be included in the added `~object.__init__`{.interpreted-text role="meth"} method, which will be defined as:

    def __init__(self, a: int, b: int = 0):

`TypeError`{.interpreted-text role="exc"} will be raised if a field without a default value follows a field with a default value. This is true whether this occurs in a single class, or as a result of class inheritance.
:::

:::: function
field(\*, default=MISSING, default_factory=MISSING, init=True, repr=True, hash=None, compare=True, metadata=None, kw_only=MISSING, doc=None)

For common and simple use cases, no other functionality is required. There are, however, some dataclass features that require additional per-field information. To satisfy this need for additional information, you can replace the default field value with a call to the provided `!field`{.interpreted-text role="func"} function. For example:

    @dataclass
    class C:
        mylist: list[int] = field(default_factory=list)

    c = C()
    c.mylist += [1, 2, 3]

As shown above, the `MISSING`{.interpreted-text role="const"} value is a sentinel object used to detect if some parameters are provided by the user. This sentinel is used because `None` is a valid value for some parameters with a distinct meaning. No code should directly use the `MISSING`{.interpreted-text role="const"} value.

The parameters to `!field`{.interpreted-text role="func"} are:

- *default*: If provided, this will be the default value for this field. This is needed because the `!field`{.interpreted-text role="func"} call itself replaces the normal position of the default value.

- *default_factory*: If provided, it must be a zero-argument callable that will be called when a default value is needed for this field. Among other purposes, this can be used to specify fields with mutable default values, as discussed below. It is an error to specify both *default* and *default_factory*.

- *init*: If true (the default), this field is included as a parameter to the generated `~object.__init__`{.interpreted-text role="meth"} method.

- *repr*: If true (the default), this field is included in the string returned by the generated `~object.__repr__`{.interpreted-text role="meth"} method.

- *hash*: This can be a bool or `None`. If true, this field is included in the generated `~object.__hash__`{.interpreted-text role="meth"} method. If false, this field is excluded from the generated `~object.__hash__`{.interpreted-text role="meth"}. If `None` (the default), use the value of *compare*: this would normally be the expected behavior, since a field should be included in the hash if it\'s used for comparisons. Setting this value to anything other than `None` is discouraged.

  One possible reason to set `hash=False` but `compare=True` would be if a field is expensive to compute a hash value for, that field is needed for equality testing, and there are other fields that contribute to the type\'s hash value. Even if a field is excluded from the hash, it will still be used for comparisons.

- *compare*: If true (the default), this field is included in the generated equality and comparison methods (`~object.__eq__`{.interpreted-text role="meth"}, `~object.__gt__`{.interpreted-text role="meth"}, et al.).

- *metadata*: This can be a mapping or `None`. `None` is treated as an empty dict. This value is wrapped in `~types.MappingProxyType`{.interpreted-text role="func"} to make it read-only, and exposed on the `Field`{.interpreted-text role="class"} object. It is not used at all by Data Classes, and is provided as a third-party extension mechanism. Multiple third-parties can each have their own key, to use as a namespace in the metadata.

- *kw_only*: If true, this field will be marked as keyword-only. This is used when the generated `~object.__init__`{.interpreted-text role="meth"} method\'s parameters are computed.

  Keyword-only fields are also not included in `!__match_args__`{.interpreted-text role="attr"}.

> ::: versionadded
> 3.10
> :::

- *doc*: optional docstring for this field.

> ::: versionadded
> 3.14
> :::

If the default value of a field is specified by a call to `!field`{.interpreted-text role="func"}, then the class attribute for this field will be replaced by the specified *default* value. If *default* is not provided, then the class attribute will be deleted. The intent is that after the `dataclass`{.interpreted-text role="deco"} decorator runs, the class attributes will all contain the default values for the fields, just as if the default value itself were specified. For example, after:

    @dataclass
    class C:
        x: int
        y: int = field(repr=False)
        z: int = field(repr=False, default=10)
        t: int = 20

The class attribute `!C.z`{.interpreted-text role="attr"} will be `10`, the class attribute `!C.t`{.interpreted-text role="attr"} will be `20`, and the class attributes `!C.x`{.interpreted-text role="attr"} and `!C.y`{.interpreted-text role="attr"} will not be set.

::: versionchanged
next If *metadata* is `None`, use an empty `frozendict`{.interpreted-text role="class"}, instead of a `~types.MappingProxyType`{.interpreted-text role="func"} of an empty `dict`{.interpreted-text role="class"}.
:::
::::

::: Field
`!Field`{.interpreted-text role="class"} objects describe each defined field. These objects are created internally, and are returned by the `fields`{.interpreted-text role="func"} module-level method (see below). Users should never instantiate a `!Field`{.interpreted-text role="class"} object directly. Its documented attributes are:

- `!name`{.interpreted-text role="attr"}: The name of the field.
- `!type`{.interpreted-text role="attr"}: The type of the field.
- `!default`{.interpreted-text role="attr"}, `!default_factory`{.interpreted-text role="attr"}, `!init`{.interpreted-text role="attr"}, `!repr`{.interpreted-text role="attr"}, `!hash`{.interpreted-text role="attr"}, `!compare`{.interpreted-text role="attr"}, `!metadata`{.interpreted-text role="attr"}, and `!kw_only`{.interpreted-text role="attr"} have the identical meaning and values as they do in the `field`{.interpreted-text role="func"} function.

Other attributes may exist, but they are private and must not be inspected or relied on.
:::

::: InitVar
`InitVar[T]` type annotations describe variables that are `init-only
<dataclasses-init-only-variables>`{.interpreted-text role="ref"}. Fields annotated with `!InitVar`{.interpreted-text role="class"} are considered pseudo-fields, and thus are neither returned by the `fields`{.interpreted-text role="func"} function nor used in any way except adding them as parameters to `~object.__init__`{.interpreted-text role="meth"} and an optional `__post_init__`{.interpreted-text role="meth"}.
:::

::: function
fields(class_or_instance)

Returns a tuple of `Field`{.interpreted-text role="class"} objects that define the fields for this dataclass. Accepts either a dataclass, or an instance of a dataclass. Raises `TypeError`{.interpreted-text role="exc"} if not passed a dataclass or instance of one. Does not return pseudo-fields which are `ClassVar` or `InitVar`.
:::

::: function
asdict(obj, \*, dict_factory=dict)

Converts the dataclass *obj* to a dict (by using the factory function *dict_factory*). Each dataclass is converted to a dict of its fields, as `name: value` pairs. dataclasses, dicts, lists, and tuples are recursed into. Other objects are copied with `copy.deepcopy`{.interpreted-text role="func"}.

Example of using `!asdict`{.interpreted-text role="func"} on nested dataclasses:

    @dataclass
    class Point:
         x: int
         y: int

    @dataclass
    class C:
         mylist: list[Point]

    p = Point(10, 20)
    assert asdict(p) == {'x': 10, 'y': 20}

    c = C([Point(0, 0), Point(10, 4)])
    assert asdict(c) == {'mylist': [{'x': 0, 'y': 0}, {'x': 10, 'y': 4}]}

To create a shallow copy, the following workaround may be used:

    {field.name: getattr(obj, field.name) for field in fields(obj)}

`!asdict`{.interpreted-text role="func"} raises `TypeError`{.interpreted-text role="exc"} if *obj* is not a dataclass instance.
:::

::: function
astuple(obj, \*, tuple_factory=tuple)

Converts the dataclass *obj* to a tuple (by using the factory function *tuple_factory*). Each dataclass is converted to a tuple of its field values. dataclasses, dicts, lists, and tuples are recursed into. Other objects are copied with `copy.deepcopy`{.interpreted-text role="func"}.

Continuing from the previous example:

    assert astuple(p) == (10, 20)
    assert astuple(c) == ([(0, 0), (10, 4)],)

To create a shallow copy, the following workaround may be used:

    tuple(getattr(obj, field.name) for field in dataclasses.fields(obj))

`!astuple`{.interpreted-text role="func"} raises `TypeError`{.interpreted-text role="exc"} if *obj* is not a dataclass instance.
:::

:::: function
make_dataclass(cls_name, fields, \*, bases=(), namespace=None, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False, weakref_slot=False, module=None, decorator=dataclass)

Creates a new dataclass with name *cls_name*, fields as defined in *fields*, base classes as given in *bases*, and initialized with a namespace as given in *namespace*. *fields* is an iterable whose elements are each either `name`, `(name, type)`, or `(name, type, Field)`. If just `name` is supplied, `typing.Any`{.interpreted-text role="data"} is used for `type`. The values of *init*, *repr*, *eq*, *order*, *unsafe_hash*, *frozen*, *match_args*, *kw_only*, *slots*, and *weakref_slot* have the same meaning as they do in `dataclass`{.interpreted-text role="deco"}.

If *module* is defined, the `!__module__`{.interpreted-text role="attr"} attribute of the dataclass is set to that value. By default, it is set to the module name of the caller.

The *decorator* parameter is a callable that will be used to create the dataclass. It should take the class object as a first argument and the same keyword arguments as `dataclass`{.interpreted-text role="deco"}. By default, the `dataclass`{.interpreted-text role="deco"} function is used.

This function is not strictly required, because any Python mechanism for creating a new class with `~object.__annotations__`{.interpreted-text role="attr"} can then apply the `dataclass`{.interpreted-text role="deco"} function to convert that class to a dataclass. This function is provided as a convenience. For example:

    C = make_dataclass('C',
                       [('x', int),
                         'y',
                        ('z', int, field(default=5))],
                       namespace={'add_one': lambda self: self.x + 1})

Is equivalent to:

    @dataclass
    class C:
        x: int
        y: 'typing.Any'
        z: int = 5

        def add_one(self):
            return self.x + 1

::: versionadded
3.14 Added the *decorator* parameter.
:::
::::

::: function
replace(obj, /, \*\*changes)

Creates a new object of the same type as *obj*, replacing fields with values from *changes*. If *obj* is not a Data Class, raises `TypeError`{.interpreted-text role="exc"}. If keys in *changes* are not field names of the given dataclass, raises `TypeError`{.interpreted-text role="exc"}.

The newly returned object is created by calling the `~object.__init__`{.interpreted-text role="meth"} method of the dataclass. This ensures that `__post_init__`{.interpreted-text role="meth"}, if present, is also called.

Init-only variables without default values, if any exist, must be specified on the call to `!replace`{.interpreted-text role="func"} so that they can be passed to `!__init__`{.interpreted-text role="meth"} and `__post_init__`{.interpreted-text role="meth"}.

It is an error for *changes* to contain any fields that are defined as having `init=False`. A `ValueError`{.interpreted-text role="exc"} will be raised in this case.

Be forewarned about how `init=False` fields work during a call to `!replace`{.interpreted-text role="func"}. They are not copied from the source object, but rather are initialized in `__post_init__`{.interpreted-text role="meth"}, if they\'re initialized at all. It is expected that `init=False` fields will be rarely and judiciously used. If they are used, it might be wise to have alternate class constructors, or perhaps a custom `!replace`{.interpreted-text role="func"} (or similarly named) method which handles instance copying.

Dataclass instances are also supported by generic function `copy.replace`{.interpreted-text role="func"}.
:::

::: function
is_dataclass(obj)

Return `True` if its parameter is a dataclass (including subclasses of a dataclass) or an instance of one, otherwise return `False`.

If you need to know if a class is an instance of a dataclass (and not a dataclass itself), then add a further check for `not isinstance(obj, type)`:

    def is_dataclass_instance(obj):
        return is_dataclass(obj) and not isinstance(obj, type)
:::

::: data
MISSING

A sentinel value signifying a missing default or default_factory.
:::

:::: data
KW_ONLY

A sentinel value used as a type annotation. Any fields after a pseudo-field with the type of `!KW_ONLY`{.interpreted-text role="const"} are marked as keyword-only fields. Note that a pseudo-field of type `!KW_ONLY`{.interpreted-text role="const"} is otherwise completely ignored. This includes the name of such a field. By convention, a name of `_` is used for a `!KW_ONLY`{.interpreted-text role="const"} field. Keyword-only fields signify `~object.__init__`{.interpreted-text role="meth"} parameters that must be specified as keywords when the class is instantiated.

In this example, the fields `y` and `z` will be marked as keyword-only fields:

    @dataclass
    class Point:
        x: float
        _: KW_ONLY
        y: float
        z: float

    p = Point(0, y=1.5, z=2.0)

In a single dataclass, it is an error to specify more than one field whose type is `!KW_ONLY`{.interpreted-text role="const"}.

::: versionadded
3.10
:::
::::

::: exception
FrozenInstanceError

Raised when an implicitly defined `~object.__setattr__`{.interpreted-text role="meth"} or `~object.__delattr__`{.interpreted-text role="meth"} is called on a dataclass which was defined with `frozen=True`. It is a subclass of `AttributeError`{.interpreted-text role="exc"}.
:::

## Post-init processing

::: function
\_\_post_init\_\_()

When defined on the class, it will be called by the generated `~object.__init__`{.interpreted-text role="meth"}, normally as `!self.__post_init__`{.interpreted-text role="meth"}. However, if any `InitVar` fields are defined, they will also be passed to `!__post_init__`{.interpreted-text role="meth"} in the order they were defined in the class. If no `!__init__`{.interpreted-text role="meth"} method is generated, then `!__post_init__`{.interpreted-text role="meth"} will not automatically be called.

Among other uses, this allows for initializing field values that depend on one or more other fields. For example:

    @dataclass
    class C:
        a: float
        b: float
        c: float = field(init=False)

        def __post_init__(self):
            self.c = self.a + self.b
:::

The `~object.__init__`{.interpreted-text role="meth"} method generated by `dataclass`{.interpreted-text role="deco"} does not call base class `!__init__`{.interpreted-text role="meth"} methods. If the base class has an `!__init__`{.interpreted-text role="meth"} method that has to be called, it is common to call this method in a `__post_init__`{.interpreted-text role="meth"} method:

    class Rectangle:
        def __init__(self, height, width):
            self.height = height
            self.width = width

    @dataclass
    class Square(Rectangle):
        side: float

        def __post_init__(self):
            super().__init__(self.side, self.side)

Note, however, that in general the dataclass-generated `!__init__`{.interpreted-text role="meth"} methods don\'t need to be called, since the derived dataclass will take care of initializing all fields of any base class that is a dataclass itself.

See the section below on init-only variables for ways to pass parameters to `!__post_init__`{.interpreted-text role="meth"}. Also see the warning about how `replace`{.interpreted-text role="func"} handles `init=False` fields.

## Class variables {#dataclasses-class-variables}

One of the few places where `dataclass`{.interpreted-text role="deco"} actually inspects the type of a field is to determine if a field is a class variable as defined in `526`{.interpreted-text role="pep"}. It does this by checking if the type of the field is `typing.ClassVar`{.interpreted-text role="data"}. If a field is a `ClassVar`, it is excluded from consideration as a field and is ignored by the dataclass mechanisms. Such `ClassVar` pseudo-fields are not returned by the module-level `fields`{.interpreted-text role="func"} function.

## Init-only variables {#dataclasses-init-only-variables}

Another place where `dataclass`{.interpreted-text role="deco"} inspects a type annotation is to determine if a field is an init-only variable. It does this by seeing if the type of a field is of type `InitVar`{.interpreted-text role="class"}. If a field is an `InitVar`{.interpreted-text role="class"}, it is considered a pseudo-field called an init-only field. As it is not a true field, it is not returned by the module-level `fields`{.interpreted-text role="func"} function. Init-only fields are added as parameters to the generated `~object.__init__`{.interpreted-text role="meth"} method, and are passed to the optional `__post_init__`{.interpreted-text role="meth"} method. They are not otherwise used by dataclasses.

For example, suppose a field will be initialized from a database, if a value is not provided when creating the class:

    @dataclass
    class C:
        i: int
        j: int | None = None
        database: InitVar[DatabaseType | None] = None

        def __post_init__(self, database):
            if self.j is None and database is not None:
                self.j = database.lookup('j')

    c = C(10, database=my_database)

In this case, `fields`{.interpreted-text role="func"} will return `Field`{.interpreted-text role="class"} objects for `!i`{.interpreted-text role="attr"} and `!j`{.interpreted-text role="attr"}, but not for `!database`{.interpreted-text role="attr"}.

## Frozen instances {#dataclasses-frozen}

It is not possible to create truly immutable Python objects. However, by passing `frozen=True` to the `dataclass`{.interpreted-text role="deco"} decorator you can emulate immutability. In that case, dataclasses will add `~object.__setattr__`{.interpreted-text role="meth"} and `~object.__delattr__`{.interpreted-text role="meth"} methods to the class. These methods will raise a `FrozenInstanceError`{.interpreted-text role="exc"} when invoked.

There is a tiny performance penalty when using `frozen=True`: `~object.__init__`{.interpreted-text role="meth"} cannot use simple assignment to initialize fields, and must use `!object.__setattr__`{.interpreted-text role="meth"}.

## Inheritance {#dataclasses-inheritance}

When the dataclass is being created by the `dataclass`{.interpreted-text role="deco"} decorator, it looks through all of the class\'s base classes in reverse MRO (that is, starting at `object`{.interpreted-text role="class"}) and, for each dataclass that it finds, adds the fields from that base class to an ordered mapping of fields. After all of the base class fields are added, it adds its own fields to the ordered mapping. All of the generated methods will use this combined, calculated ordered mapping of fields. Because the fields are in insertion order, derived classes override base classes. An example:

    @dataclass
    class Base:
        x: Any = 15.0
        y: int = 0

    @dataclass
    class C(Base):
        z: int = 10
        x: int = 15

The final list of fields is, in order, `!x`{.interpreted-text role="attr"}, `!y`{.interpreted-text role="attr"}, `!z`{.interpreted-text role="attr"}. The final type of `!x`{.interpreted-text role="attr"} is `int`{.interpreted-text role="class"}, as specified in class `!C`{.interpreted-text role="class"}.

The generated `~object.__init__`{.interpreted-text role="meth"} method for `!C`{.interpreted-text role="class"} will look like:

    def __init__(self, x: int = 15, y: int = 0, z: int = 10):

## Re-ordering of keyword-only parameters in `!__init__`{.interpreted-text role="meth"}

After the parameters needed for `~object.__init__`{.interpreted-text role="meth"} are computed, any keyword-only parameters are moved to come after all regular (non-keyword-only) parameters. This is a requirement of how keyword-only parameters are implemented in Python: they must come after non-keyword-only parameters.

In this example, `!Base.y`{.interpreted-text role="attr"}, `!Base.w`{.interpreted-text role="attr"}, and `!D.t`{.interpreted-text role="attr"} are keyword-only fields, and `!Base.x`{.interpreted-text role="attr"} and `!D.z`{.interpreted-text role="attr"} are regular fields:

    @dataclass
    class Base:
        x: Any = 15.0
        _: KW_ONLY
        y: int = 0
        w: int = 1

    @dataclass
    class D(Base):
        z: int = 10
        t: int = field(kw_only=True, default=0)

The generated `!__init__`{.interpreted-text role="meth"} method for `!D`{.interpreted-text role="class"} will look like:

    def __init__(self, x: Any = 15.0, z: int = 10, *, y: int = 0, w: int = 1, t: int = 0):

Note that the parameters have been re-ordered from how they appear in the list of fields: parameters derived from regular fields are followed by parameters derived from keyword-only fields.

The relative ordering of keyword-only parameters is maintained in the re-ordered `!__init__`{.interpreted-text role="meth"} parameter list.

## Default factory functions

If a `field`{.interpreted-text role="func"} specifies a *default_factory*, it is called with zero arguments when a default value for the field is needed. For example, to create a new instance of a list, use:

    mylist: list = field(default_factory=list)

If a field is excluded from `~object.__init__`{.interpreted-text role="meth"} (using `init=False`) and the field also specifies *default_factory*, then the default factory function will always be called from the generated `!__init__`{.interpreted-text role="meth"} function. This happens because there is no other way to give the field an initial value.

## Mutable default values

Python stores default member variable values in class attributes. Consider this example, not using dataclasses:

    class C:
        x = []
        def add(self, element):
            self.x.append(element)

    o1 = C()
    o2 = C()
    o1.add(1)
    o2.add(2)
    assert o1.x == [1, 2]
    assert o1.x is o2.x

Note that the two instances of class `!C`{.interpreted-text role="class"} share the same class variable `!x`{.interpreted-text role="attr"}, as expected.

Using dataclasses, *if* this code was valid:

    @dataclass
    class D:
        x: list = []      # This code raises ValueError
        def add(self, element):
            self.x.append(element)

it would generate code similar to:

    class D:
        x = []
        def __init__(self, x=x):
            self.x = x
        def add(self, element):
            self.x.append(element)

    assert D().x is D().x

This has the same issue as the original example using class `!C`{.interpreted-text role="class"}. That is, two instances of class `!D`{.interpreted-text role="class"} that do not specify a value for `!x`{.interpreted-text role="attr"} when creating a class instance will share the same copy of `!x`{.interpreted-text role="attr"}. Because dataclasses just use normal Python class creation they also share this behavior. There is no general way for Data Classes to detect this condition. Instead, the `dataclass`{.interpreted-text role="deco"} decorator will raise a `ValueError`{.interpreted-text role="exc"} if it detects an unhashable default parameter. The assumption is that if a value is unhashable, it is mutable. This is a partial solution, but it does protect against many common errors.

Using default factory functions is a way to create new instances of mutable types as default values for fields:

    @dataclass
    class D:
        x: list = field(default_factory=list)

    assert D().x is not D().x

::: versionchanged
3.11 Instead of looking for and disallowing objects of type `list`{.interpreted-text role="class"}, `dict`{.interpreted-text role="class"}, or `set`{.interpreted-text role="class"}, unhashable objects are now not allowed as default values. Unhashability is used to approximate mutability.
:::

## Descriptor-typed fields

Fields that are assigned `descriptor objects <descriptors>`{.interpreted-text role="ref"} as their default value have the following special behaviors:

- The value for the field passed to the dataclass\'s `~object.__init__`{.interpreted-text role="meth"} method is passed to the descriptor\'s `~object.__set__`{.interpreted-text role="meth"} method rather than overwriting the descriptor object.
- Similarly, when getting or setting the field, the descriptor\'s `~object.__get__`{.interpreted-text role="meth"} or `!__set__`{.interpreted-text role="meth"} method is called rather than returning or overwriting the descriptor object.
- To determine whether a field contains a default value, `dataclass`{.interpreted-text role="deco"} will call the descriptor\'s `!__get__`{.interpreted-text role="meth"} method using its class access form: `descriptor.__get__(obj=None, type=cls)`. If the descriptor returns a value in this case, it will be used as the field\'s default. On the other hand, if the descriptor raises `AttributeError`{.interpreted-text role="exc"} in this situation, no default value will be provided for the field.

<!-- -->

    class IntConversionDescriptor:
        def __init__(self, *, default):
            self._default = default

        def __set_name__(self, owner, name):
            self._name = "_" + name

        def __get__(self, obj, type):
            if obj is None:
                return self._default

            return getattr(obj, self._name, self._default)

        def __set__(self, obj, value):
            setattr(obj, self._name, int(value))

    @dataclass
    class InventoryItem:
        quantity_on_hand: IntConversionDescriptor = IntConversionDescriptor(default=100)

    i = InventoryItem()
    print(i.quantity_on_hand)   # 100
    i.quantity_on_hand = 2.5    # calls __set__ with 2.5
    print(i.quantity_on_hand)   # 2

Note that if a field is annotated with a descriptor type, but is not assigned a descriptor object as its default value, the field will act like a normal field.
