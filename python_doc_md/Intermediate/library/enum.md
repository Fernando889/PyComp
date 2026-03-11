# `!enum`{.interpreted-text role="mod"} \-\-- Support for enumerations

::: {.module synopsis="Implementation of an enumeration class."}
enum
:::

::: versionadded
3.4
:::

**Source code:** `Lib/enum.py`{.interpreted-text role="source"}

::: sidebar
**Important**

This page contains the API reference information. For tutorial information and discussion of more advanced topics, see

- `Basic Tutorial <enum-basic-tutorial>`{.interpreted-text role="ref"}
- `Advanced Tutorial <enum-advanced-tutorial>`{.interpreted-text role="ref"}
- `Enum Cookbook <enum-cookbook>`{.interpreted-text role="ref"}
:::

------------------------------------------------------------------------

An enumeration:

- is a set of symbolic names (members) bound to unique values
- can be iterated over to return its canonical (i.e. non-alias) members in definition order
- uses *call* syntax to return members by value
- uses *index* syntax to return members by name

Enumerations are created either by using `class`{.interpreted-text role="keyword"} syntax, or by using function-call syntax:

    >>> from enum import Enum

    >>> # class syntax
    >>> class Color(Enum):
    ...     RED = 1
    ...     GREEN = 2
    ...     BLUE = 3

    >>> # functional syntax
    >>> Color = Enum('Color', [('RED', 1), ('GREEN', 2), ('BLUE', 3)])

Even though we can use `class`{.interpreted-text role="keyword"} syntax to create Enums, Enums are not normal Python classes. See `How are Enums different? <enum-class-differences>`{.interpreted-text role="ref"} for more details.

:::: note
::: title
Note
:::

Nomenclature

- The class `!Color`{.interpreted-text role="class"} is an *enumeration* (or *enum*)
- The attributes `!Color.RED`{.interpreted-text role="attr"}, `!Color.GREEN`{.interpreted-text role="attr"}, etc., are *enumeration members* (or *members*) and are functionally constants.
- The enum members have *names* and *values* (the name of `!Color.RED`{.interpreted-text role="attr"} is `RED`, the value of `!Color.BLUE`{.interpreted-text role="attr"} is `3`, etc.)
::::

------------------------------------------------------------------------

## Module Contents

> `EnumType`{.interpreted-text role="class"}
>
> > The `type` for Enum and its subclasses.
>
> `Enum`{.interpreted-text role="class"}
>
> > Base class for creating enumerated constants.
>
> `IntEnum`{.interpreted-text role="class"}
>
> > Base class for creating enumerated constants that are also subclasses of `int`{.interpreted-text role="class"}. ([Notes](#notes))
>
> `StrEnum`{.interpreted-text role="class"}
>
> > Base class for creating enumerated constants that are also subclasses of `str`{.interpreted-text role="class"}. ([Notes](#notes))
>
> `Flag`{.interpreted-text role="class"}
>
> > Base class for creating enumerated constants that can be combined using the bitwise operations without losing their `Flag`{.interpreted-text role="class"} membership.
>
> `IntFlag`{.interpreted-text role="class"}
>
> > Base class for creating enumerated constants that can be combined using the bitwise operators without losing their `IntFlag`{.interpreted-text role="class"} membership. `IntFlag`{.interpreted-text role="class"} members are also subclasses of `int`{.interpreted-text role="class"}. ([Notes](#notes))
>
> `ReprEnum`{.interpreted-text role="class"}
>
> > Used by `IntEnum`{.interpreted-text role="class"}, `StrEnum`{.interpreted-text role="class"}, and `IntFlag`{.interpreted-text role="class"} to keep the `str() <str>`{.interpreted-text role="class"} of the mixed-in type.
>
> `EnumCheck`{.interpreted-text role="class"}
>
> > An enumeration with the values `CONTINUOUS`, `NAMED_FLAGS`, and `UNIQUE`, for use with `verify`{.interpreted-text role="func"} to ensure various constraints are met by a given enumeration.
>
> `FlagBoundary`{.interpreted-text role="class"}
>
> > An enumeration with the values `STRICT`, `CONFORM`, `EJECT`, and `KEEP` which allows for more fine-grained control over how invalid values are dealt with in an enumeration.
>
> `EnumDict`{.interpreted-text role="class"}
>
> > A subclass of `dict`{.interpreted-text role="class"} for use when subclassing `EnumType`{.interpreted-text role="class"}.
>
> `auto`{.interpreted-text role="class"}
>
> > Instances are replaced with an appropriate value for Enum members. `StrEnum`{.interpreted-text role="class"} defaults to the lower-cased version of the member name, while other Enums default to 1 and increase from there.
>
> `~enum.property`{.interpreted-text role="func"}
>
> > Allows `Enum`{.interpreted-text role="class"} members to have attributes without conflicting with member names. The `value` and `name` attributes are implemented this way.
>
> `unique`{.interpreted-text role="func"}
>
> > Enum class decorator that ensures only one name is bound to any one value.
>
> `verify`{.interpreted-text role="func"}
>
> > Enum class decorator that checks user-selectable constraints on an enumeration.
>
> `member`{.interpreted-text role="func"}
>
> > Make `obj` a member. Can be used as a decorator.
>
> `nonmember`{.interpreted-text role="func"}
>
> > Do not make `obj` a member. Can be used as a decorator.
>
> `global_enum`{.interpreted-text role="func"}
>
> > Modify the `str() <str>`{.interpreted-text role="class"} and `repr`{.interpreted-text role="func"} of an enum to show its members as belonging to the module instead of its class, and export the enum members to the global namespace.
>
> `show_flag_values`{.interpreted-text role="func"}
>
> > Return a list of all power-of-two integers contained in a flag.
>
> `enum.bin`{.interpreted-text role="func"}
>
> > Like built-in `bin`{.interpreted-text role="func"}, except negative values are represented in two\'s complement, and the leading bit always indicates sign (`0` implies positive, `1` implies negative).

::: versionadded
3.6 `Flag`, `IntFlag`, `auto`
:::

::: versionadded
3.11 `StrEnum`, `EnumCheck`, `ReprEnum`, `FlagBoundary`, `property`, `member`, `nonmember`, `global_enum`, `show_flag_values`
:::

::: versionadded
3.13 `EnumDict`
:::

------------------------------------------------------------------------

## Data Types

::::::::::::: EnumType
*EnumType* is the `metaclass`{.interpreted-text role="term"} for *enum* enumerations. It is possible to subclass *EnumType* \-- see `Subclassing EnumType <enumtype-examples>`{.interpreted-text role="ref"} for details.

`EnumType` is responsible for setting the correct `!__repr__`{.interpreted-text role="meth"}, `!__str__`{.interpreted-text role="meth"}, `!__format__`{.interpreted-text role="meth"}, and `!__reduce__`{.interpreted-text role="meth"} methods on the final *enum*, as well as creating the enum members, properly handling duplicates, providing iteration over the enum class, etc.

::: versionadded
3.11

Before 3.11 `EnumType` was called `EnumMeta`, which is still available as an alias.
:::

::: method
EnumType.\_\_call\_\_(cls, value, names=None, \*, module=None, qualname=None, type=None, start=1, boundary=None)

This method is called in two different ways:

- to look up an existing member:

  > 
  >
  > cls
  > :   The enum class being called.
  >
  > value
  > :   The value to lookup.

- to use the `cls` enum to create a new enum (only if the existing enum does not have any members):

  > 
  >
  > cls
  > :   The enum class being called.
  >
  > value
  > :   The name of the new Enum to create.
  >
  > names
  > :   The names/values of the members for the new Enum.
  >
  > module
  > :   The name of the module the new Enum is created in.
  >
  > qualname
  > :   The actual location in the module where this Enum can be found.
  >
  > type
  > :   A mix-in type for the new Enum.
  >
  > start
  > :   The first integer value for the Enum (used by `auto`{.interpreted-text role="class"}).
  >
  > boundary
  > :   How to handle out-of-range values from bit operations (`Flag`{.interpreted-text role="class"} only).
:::

:::: method
EnumType.\_\_contains\_\_(cls, member)

Returns `True` if member belongs to the `cls`:

    >>> some_var = Color.RED
    >>> some_var in Color
    True
    >>> Color.RED.value in Color
    True

::: versionchanged
3.12

Before Python 3.12, a `TypeError` is raised if a non-Enum-member is used in a containment check.
:::
::::

::: method
EnumType.\_\_dir\_\_(cls)

Returns `['__class__', '__doc__', '__members__', '__module__']` and the names of the members in *cls*:

    >>> dir(Color)
    ['BLUE', 'GREEN', 'RED', '__class__', '__contains__', '__doc__', '__getitem__', '__init_subclass__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__']
:::

::: method
EnumType.\_\_getitem\_\_(cls, name)

Returns the Enum member in *cls* matching *name*, or raises a `KeyError`{.interpreted-text role="exc"}:

    >>> Color['BLUE']
    <Color.BLUE: 3>
:::

::: method
EnumType.\_\_iter\_\_(cls)

Returns each member in *cls* in definition order:

    >>> list(Color)
    [<Color.RED: 1>, <Color.GREEN: 2>, <Color.BLUE: 3>]
:::

::: method
EnumType.\_\_len\_\_(cls)

Returns the number of member in *cls*:

    >>> len(Color)
    3
:::

::: attribute
EnumType.\_\_members\_\_

Returns a mapping of every enum name to its member, including aliases
:::

::: method
EnumType.\_\_reversed\_\_(cls)

Returns each member in *cls* in reverse definition order:

    >>> list(reversed(Color))
    [<Color.BLUE: 3>, <Color.GREEN: 2>, <Color.RED: 1>]
:::
:::::::::::::

:::::::::::::::::::::::::::::::::::::: Enum
*Enum* is the base class for all *enum* enumerations.

::: attribute
Enum.name

The name used to define the `Enum` member:

    >>> Color.BLUE.name
    'BLUE'
:::

::::: attribute
Enum.value

The value given to the `Enum` member:

    >>> Color.RED.value
    1

Value of the member, can be set in `~Enum.__new__`{.interpreted-text role="meth"}.

:::: note
::: title
Note
:::

Enum member values

Member values can be anything: `int`{.interpreted-text role="class"}, `str`{.interpreted-text role="class"}, etc. If the exact value is unimportant you may use `auto`{.interpreted-text role="class"} instances and an appropriate value will be chosen for you. See `auto`{.interpreted-text role="class"} for the details.

While mutable/unhashable values, such as `dict`{.interpreted-text role="class"}, `list`{.interpreted-text role="class"} or a mutable `~dataclasses.dataclass`{.interpreted-text role="class"}, can be used, they will have a quadratic performance impact during creation relative to the total number of mutable/unhashable values in the enum.
::::
:::::

::: attribute
Enum.\_name\_

Name of the member.
:::

::: attribute
Enum.\_value\_

Value of the member, can be set in `~Enum.__new__`{.interpreted-text role="meth"}.
:::

:::::: attribute
Enum.\_order\_

No longer used, kept for backward compatibility. (class attribute, removed during class creation).

The `~Enum._order_`{.interpreted-text role="attr"} attribute can be provided to help keep Python 2 / Python 3 code in sync. It will be checked against the actual order of the enumeration and raise an error if the two do not match:

    >>> class Color(Enum):
    ...     _order_ = 'RED GREEN BLUE'
    ...     RED = 1
    ...     BLUE = 3
    ...     GREEN = 2
    ...
    Traceback (most recent call last):
    ...
    TypeError: member order does not match _order_:
       ['RED', 'BLUE', 'GREEN']
       ['RED', 'GREEN', 'BLUE']

:::: note
::: title
Note
:::

In Python 2 code the `~Enum._order_`{.interpreted-text role="attr"} attribute is necessary as definition order is lost before it can be recorded.
::::

::: versionadded
3.6
:::
::::::

:::: attribute
Enum.\_ignore\_

`_ignore_` is only used during creation and is removed from the enumeration once creation is complete.

`_ignore_` is a list of names that will not become members, and whose names will also be removed from the completed enumeration. See `TimePeriod <enum-time-period>`{.interpreted-text role="ref"} for an example.

::: versionadded
3.7
:::
::::

::: method
Enum.\_\_dir\_\_(self)

Returns `['__class__', '__doc__', '__module__', 'name', 'value']` and any public methods defined on *self.\_\_class\_\_*:

    >>> from enum import Enum
    >>> from datetime import date
    >>> class Weekday(Enum):
    ...     MONDAY = 1
    ...     TUESDAY = 2
    ...     WEDNESDAY = 3
    ...     THURSDAY = 4
    ...     FRIDAY = 5
    ...     SATURDAY = 6
    ...     SUNDAY = 7
    ...     @classmethod
    ...     def today(cls):
    ...         print('today is %s' % cls(date.today().isoweekday()).name)
    ...
    >>> dir(Weekday.SATURDAY)
    ['__class__', '__doc__', '__eq__', '__hash__', '__module__', 'name', 'today', 'value']
:::

::::::: method
Enum.\_generate_next_value\_(name, start, count, last_values)

name
:   The name of the member being defined (e.g. \'RED\').

start
:   The start value for the Enum; the default is 1.

count
:   The number of members currently defined, not including this one.

last_values
:   A list of the previous values.

A *staticmethod* that is used to determine the next value returned by `auto`{.interpreted-text role="class"}.

:::: note
::: title
Note
:::
::::

For standard `Enum`{.interpreted-text role="class"} classes the next value chosen is the highest value seen incremented by one.

For `Flag`{.interpreted-text role="class"} classes the next value chosen will be the next highest power-of-two.

This method may be overridden, e.g.:

    >>> from enum import auto, Enum
    >>> class PowersOfThree(Enum):

\... \@staticmethod \... def [generate_next_value]{#generate_next_value}\_(name, start, count, last_values): \... return 3 \*\* (count + 1) \... FIRST = auto() \... SECOND = auto() \... \>\>\> PowersOfThree.SECOND.value 9

::: versionadded
3.6
:::

::: versionchanged
3.13
:::

Prior versions would use the last seen value instead of the highest value.
:::::::

::: method
Enum.\_\_init\_\_(self, *args,*\*kwds)

By default, does nothing. If multiple values are given in the member assignment, those values become separate arguments to `__init__`; e.g.

> \>\>\> from enum import Enum \>\>\> class Weekday(Enum): \... MONDAY = 1, \'Mon\'

`Weekday.__init__()` would be called as `Weekday.__init__(self, 1, 'Mon')`
:::

::: method
Enum.\_\_init_subclass\_\_(cls, \*\*kwds)

A *classmethod* that is used to further configure subsequent subclasses. By default, does nothing.
:::

:::: method
Enum.\_missing\_(cls, value)

A *classmethod* for looking up values not found in *cls*. By default it does nothing, but can be overridden to implement custom search behavior:

    >>> from enum import auto, StrEnum
    >>> class Build(StrEnum):
    ...     DEBUG = auto()
    ...     OPTIMIZED = auto()
    ...     @classmethod
    ...     def _missing_(cls, value):
    ...         value = value.lower()
    ...         for member in cls:
    ...             if member.value == value:
    ...                 return member
    ...         return None
    ...
    >>> Build.DEBUG.value
    'debug'
    >>> Build('deBUG')
    <Build.DEBUG: 'debug'>

::: versionadded
3.6
:::
::::

::::: method
Enum.\_\_new\_\_(cls, *args,*\*kwds)

By default, doesn\'t exist. If specified, either in the enum class definition or in a mixin class (such as `int`), all values given in the member assignment will be passed; e.g.

> \>\>\> from enum import Enum \>\>\> class MyIntEnum(int, Enum): \... TWENTYSIX = \'1a\', 16

results in the call `int('1a', 16)` and a value of `26` for the member.

:::: note
::: title
Note
:::

When writing a custom `__new__`, do not use `super().__new__` \-- call the appropriate `__new__` instead.
::::
:::::

::: method
Enum.\_\_repr\_\_(self)

Returns the string used for *repr()* calls. By default, returns the *Enum* name, member name, and value, but can be overridden:

    >>> from enum import auto, Enum
    >>> class OtherStyle(Enum):
    ...     ALTERNATE = auto()
    ...     OTHER = auto()
    ...     SOMETHING_ELSE = auto()
    ...     def __repr__(self):
    ...         cls_name = self.__class__.__name__
    ...         return f'{cls_name}.{self.name}'
    ...
    >>> OtherStyle.ALTERNATE, str(OtherStyle.ALTERNATE), f"{OtherStyle.ALTERNATE}"
    (OtherStyle.ALTERNATE, 'OtherStyle.ALTERNATE', 'OtherStyle.ALTERNATE')
:::

::: method
Enum.\_\_str\_\_(self)

Returns the string used for *str()* calls. By default, returns the *Enum* name and member name, but can be overridden:

    >>> from enum import auto, Enum
    >>> class OtherStyle(Enum):
    ...     ALTERNATE = auto()
    ...     OTHER = auto()
    ...     SOMETHING_ELSE = auto()
    ...     def __str__(self):
    ...         return f'{self.name}'
    ...
    >>> OtherStyle.ALTERNATE, str(OtherStyle.ALTERNATE), f"{OtherStyle.ALTERNATE}"
    (<OtherStyle.ALTERNATE: 1>, 'ALTERNATE', 'ALTERNATE')
:::

::: method
Enum.\_\_format\_\_(self)

Returns the string used for *format()* and *f-string* calls. By default, returns `__str__`{.interpreted-text role="meth"} return value, but can be overridden:

    >>> from enum import auto, Enum
    >>> class OtherStyle(Enum):
    ...     ALTERNATE = auto()
    ...     OTHER = auto()
    ...     SOMETHING_ELSE = auto()
    ...     def __format__(self, spec):
    ...         return f'{self.name}'
    ...
    >>> OtherStyle.ALTERNATE, str(OtherStyle.ALTERNATE), f"{OtherStyle.ALTERNATE}"
    (<OtherStyle.ALTERNATE: 1>, 'OtherStyle.ALTERNATE', 'ALTERNATE')
:::

:::: note
::: title
Note
:::

Using `auto`{.interpreted-text role="class"} with `Enum`{.interpreted-text role="class"} results in integers of increasing value, starting with `1`.
::::

::: versionchanged
3.12 Added `enum-dataclass-support`{.interpreted-text role="ref"}
:::

:::: method
Enum.\_add_alias\_

Adds a new name as an alias to an existing member:

    >>> Color.RED._add_alias_("ERROR")
    >>> Color.ERROR
    <Color.RED: 1>

Raises a `NameError`{.interpreted-text role="exc"} if the name is already assigned to a different member.

::: versionadded
3.13
:::
::::

:::: method
Enum.\_add_value_alias\_

Adds a new value as an alias to an existing member:

    >>> Color.RED._add_value_alias_(42)
    >>> Color(42)
    <Color.RED: 1>

| Raises a `ValueError`{.interpreted-text role="exc"} if the value is already linked with a different member.
| See `multi-value-enum`{.interpreted-text role="ref"} for an example.

::: versionadded
3.13
:::
::::
::::::::::::::::::::::::::::::::::::::

:::::: IntEnum
*IntEnum* is the same as `Enum`{.interpreted-text role="class"}, but its members are also integers and can be used anywhere that an integer can be used. If any integer operation is performed with an *IntEnum* member, the resulting value loses its enumeration status.

> \>\>\> from enum import IntEnum \>\>\> class Number(IntEnum): \... ONE = 1 \... TWO = 2 \... THREE = 3 \... \>\>\> Number.THREE \<Number.THREE: 3\> \>\>\> Number.ONE + Number.TWO 3 \>\>\> Number.THREE + 5 8 \>\>\> Number.THREE == 3 True

:::: note
::: title
Note
:::

Using `auto`{.interpreted-text role="class"} with `IntEnum`{.interpreted-text role="class"} results in integers of increasing value, starting with `1`.
::::

::: versionchanged
3.11 `~object.__str__`{.interpreted-text role="meth"} is now `!int.__str__`{.interpreted-text role="meth"} to better support the *replacement of existing constants* use-case. `~object.__format__`{.interpreted-text role="meth"} was already `!int.__format__`{.interpreted-text role="meth"} for that same reason.
:::
::::::

:::::::::: StrEnum
*StrEnum* is the same as `Enum`{.interpreted-text role="class"}, but its members are also strings and can be used in most of the same places that a string can be used. The result of any string operation performed on or with a *StrEnum* member is not part of the enumeration.

\>\>\> from enum import StrEnum, auto \>\>\> class Color(StrEnum): \... RED = \'r\' \... GREEN = \'g\' \... BLUE = \'b\' \... UNKNOWN = auto() \... \>\>\> Color.RED \<Color.RED: \'r\'\> \>\>\> Color.UNKNOWN \<Color.UNKNOWN: \'unknown\'\> \>\>\> str(Color.UNKNOWN) \'unknown\'

:::: note
::: title
Note
:::

There are places in the stdlib that check for an exact `str`{.interpreted-text role="class"} instead of a `str`{.interpreted-text role="class"} subclass (i.e. `type(unknown) == str` instead of `isinstance(unknown, str)`), and in those locations you will need to use `str(MyStrEnum.MY_MEMBER)`.
::::

:::: note
::: title
Note
:::

Using `auto`{.interpreted-text role="class"} with `StrEnum`{.interpreted-text role="class"} results in the lower-cased member name as the value.
::::

:::: note
::: title
Note
:::

`~object.__str__`{.interpreted-text role="meth"} is `!str.__str__`{.interpreted-text role="meth"} to better support the *replacement of existing constants* use-case. `~object.__format__`{.interpreted-text role="meth"} is likewise `!str.__format__`{.interpreted-text role="meth"} for that same reason.
::::

::: versionadded
3.11
:::
::::::::::

::::::::::::::::: Flag
`Flag` is the same as `Enum`{.interpreted-text role="class"}, but its members support the bitwise operators `&` (*AND*), `|` (*OR*), `^` (*XOR*), and `~` (*INVERT*); the results of those operations are (aliases of) members of the enumeration.

::: method
\_\_contains\_\_(self, value)

Returns *True* if value is in self:

    >>> from enum import Flag, auto
    >>> class Color(Flag):
    ...     RED = auto()
    ...     GREEN = auto()
    ...     BLUE = auto()
    ...
    >>> purple = Color.RED | Color.BLUE
    >>> white = Color.RED | Color.GREEN | Color.BLUE
    >>> Color.GREEN in purple
    False
    >>> Color.GREEN in white
    True
    >>> purple in white
    True
    >>> white in purple
    False
:::

:::: method
\_\_iter\_\_(self):

Returns all contained non-alias members:

    >>> list(Color.RED)
    [<Color.RED: 1>]
    >>> list(purple)
    [<Color.RED: 1>, <Color.BLUE: 4>]

::: versionadded
3.11
:::
::::

:::: method
\_\_len\_\_(self):

Returns number of members in flag:

    >>> len(Color.GREEN)
    1
    >>> len(white)
    3

::: versionadded
3.11
:::
::::

::: method
\_\_bool\_\_(self):

Returns *True* if any members in flag, *False* otherwise:

    >>> bool(Color.GREEN)
    True
    >>> bool(white)
    True
    >>> black = Color(0)
    >>> bool(black)
    False
:::

::: method
\_\_or\_\_(self, other)

Returns current flag binary or\'ed with other:

    >>> Color.RED | Color.GREEN
    <Color.RED|GREEN: 3>
:::

::: method
\_\_and\_\_(self, other)

Returns current flag binary and\'ed with other:

    >>> purple & white
    <Color.RED|BLUE: 5>
    >>> purple & Color.GREEN
    <Color: 0>
:::

::: method
\_\_xor\_\_(self, other)

Returns current flag binary xor\'ed with other:

    >>> purple ^ white
    <Color.GREEN: 2>
    >>> purple ^ Color.GREEN
    <Color.RED|GREEN|BLUE: 7>
:::

::: method
\_\_invert\_\_(self):

Returns all the flags in *type(self)* that are not in *self*:

    >>> ~white
    <Color: 0>
    >>> ~purple
    <Color.GREEN: 2>
    >>> ~Color.RED
    <Color.GREEN|BLUE: 6>
:::

::: method
[numeric_repr]{#numeric_repr}\_

Function used to format any remaining unnamed numeric values. Default is the value\'s repr; common choices are `hex`{.interpreted-text role="func"} and `oct`{.interpreted-text role="func"}.
:::

:::: note
::: title
Note
:::

Using `auto`{.interpreted-text role="class"} with `Flag`{.interpreted-text role="class"} results in integers that are powers of two, starting with `1`.
::::

::: versionchanged
3.11 The *repr()* of zero-valued flags has changed. It is now:

\>\>\> Color(0) \# doctest: +SKIP \<Color: 0\>
:::
:::::::::::::::::

:::::: IntFlag
`IntFlag` is the same as `Flag`{.interpreted-text role="class"}, but its members are also integers and can be used anywhere that an integer can be used.

> \>\>\> from enum import IntFlag, auto \>\>\> class Color(IntFlag): \... RED = auto() \... GREEN = auto() \... BLUE = auto() \... \>\>\> Color.RED & 2 \<Color: 0\> \>\>\> Color.RED \| 2 \<Color.RED\|GREEN: 3\>

If any integer operation is performed with an *IntFlag* member, the result is not an *IntFlag*:

    >>> Color.RED + 2
    3

If a `Flag`{.interpreted-text role="class"} operation is performed with an *IntFlag* member and:

- the result is a valid *IntFlag*: an *IntFlag* is returned
- the result is not a valid *IntFlag*: the result depends on the `FlagBoundary`{.interpreted-text role="class"} setting

The `repr`{.interpreted-text role="func"} of unnamed zero-valued flags has changed. It is now:

    >>> Color(0)
    <Color: 0>

:::: note
::: title
Note
:::

Using `auto`{.interpreted-text role="class"} with `IntFlag`{.interpreted-text role="class"} results in integers that are powers of two, starting with `1`.
::::

::: versionchanged
3.11

`~object.__str__`{.interpreted-text role="meth"} is now `!int.__str__`{.interpreted-text role="meth"} to better support the *replacement of existing constants* use-case. `~object.__format__`{.interpreted-text role="meth"} was already `!int.__format__`{.interpreted-text role="meth"} for that same reason.

Inversion of an `!IntFlag`{.interpreted-text role="class"} now returns a positive value that is the union of all flags not in the given flag, rather than a negative value. This matches the existing `Flag`{.interpreted-text role="class"} behavior.
:::
::::::

:::: ReprEnum
`!ReprEnum`{.interpreted-text role="class"} uses the `repr() <Enum.__repr__>`{.interpreted-text role="meth"} of `Enum`{.interpreted-text role="class"}, but the `str() <str>`{.interpreted-text role="class"} of the mixed-in data type:

- `!int.__str__`{.interpreted-text role="meth"} for `IntEnum`{.interpreted-text role="class"} and `IntFlag`{.interpreted-text role="class"}
- `!str.__str__`{.interpreted-text role="meth"} for `StrEnum`{.interpreted-text role="class"}

Inherit from `!ReprEnum`{.interpreted-text role="class"} to keep the `str() <str>`{.interpreted-text role="class"} / `format`{.interpreted-text role="func"} of the mixed-in data type instead of using the `Enum`{.interpreted-text role="class"}-default `str() <Enum.__str__>`{.interpreted-text role="meth"}.

::: versionadded
3.11
:::
::::

::::::::: EnumCheck
*EnumCheck* contains the options used by the `verify`{.interpreted-text role="func"} decorator to ensure various constraints; failed constraints result in a `ValueError`{.interpreted-text role="exc"}.

::: attribute
UNIQUE

Ensure that each value has only one name:

    >>> from enum import Enum, verify, UNIQUE
    >>> @verify(UNIQUE)
    ... class Color(Enum):
    ...     RED = 1
    ...     GREEN = 2
    ...     BLUE = 3
    ...     CRIMSON = 1
    Traceback (most recent call last):
    ...
    ValueError: aliases found in <enum 'Color'>: CRIMSON -> RED
:::

::: attribute
CONTINUOUS

Ensure that there are no missing values between the lowest-valued member and the highest-valued member:

    >>> from enum import Enum, verify, CONTINUOUS
    >>> @verify(CONTINUOUS)
    ... class Color(Enum):
    ...     RED = 1
    ...     GREEN = 2
    ...     BLUE = 5
    Traceback (most recent call last):
    ...
    ValueError: invalid enum 'Color': missing values 3, 4
:::

::: attribute
NAMED_FLAGS

Ensure that any flag groups/masks contain only named flags \-- useful when values are specified instead of being generated by `auto`{.interpreted-text role="func"}:

    >>> from enum import Flag, verify, NAMED_FLAGS
    >>> @verify(NAMED_FLAGS)
    ... class Color(Flag):
    ...     RED = 1
    ...     GREEN = 2
    ...     BLUE = 4
    ...     WHITE = 15
    ...     NEON = 31
    Traceback (most recent call last):
    ...
    ValueError: invalid Flag 'Color': aliases WHITE and NEON are missing combined values of 0x18 [use enum.show_flag_values(value) for details]
:::

:::: note
::: title
Note
:::

CONTINUOUS and NAMED_FLAGS are designed to work with integer-valued members.
::::

::: versionadded
3.11
:::
:::::::::

:::::::: FlagBoundary
`FlagBoundary` controls how out-of-range values are handled in `Flag`{.interpreted-text role="class"} and its subclasses.

::: attribute
STRICT

Out-of-range values cause a `ValueError`{.interpreted-text role="exc"} to be raised. This is the default for `Flag`{.interpreted-text role="class"}:

    >>> from enum import Flag, STRICT, auto
    >>> class StrictFlag(Flag, boundary=STRICT):
    ...     RED = auto()
    ...     GREEN = auto()
    ...     BLUE = auto()
    ...
    >>> StrictFlag(2**2 + 2**4)
    Traceback (most recent call last):
    ...
    ValueError: <flag 'StrictFlag'> invalid value 20
        given 0b0 10100
      allowed 0b0 00111
:::

::: attribute
CONFORM

Out-of-range values have invalid values removed, leaving a valid `Flag`{.interpreted-text role="class"} value:

    >>> from enum import Flag, CONFORM, auto
    >>> class ConformFlag(Flag, boundary=CONFORM):
    ...     RED = auto()
    ...     GREEN = auto()
    ...     BLUE = auto()
    ...
    >>> ConformFlag(2**2 + 2**4)
    <ConformFlag.BLUE: 4>
:::

::: attribute
EJECT

Out-of-range values lose their `Flag`{.interpreted-text role="class"} membership and revert to `int`{.interpreted-text role="class"}.

> \>\>\> from enum import Flag, EJECT, auto \>\>\> class EjectFlag(Flag, boundary=EJECT): \... RED = auto() \... GREEN = auto() \... BLUE = auto() \... \>\>\> EjectFlag(2\*\*2 + 2\*\*4) 20
:::

::: attribute
KEEP

Out-of-range values are kept, and the `Flag`{.interpreted-text role="class"} membership is kept. This is the default for `IntFlag`{.interpreted-text role="class"}:

    >>> from enum import Flag, KEEP, auto
    >>> class KeepFlag(Flag, boundary=KEEP):
    ...     RED = auto()
    ...     GREEN = auto()
    ...     BLUE = auto()
    ...
    >>> KeepFlag(2**2 + 2**4)
    <KeepFlag.BLUE|16: 20>
:::

::: versionadded
3.11
:::
::::::::

::::: EnumDict
*EnumDict* is a subclass of `dict`{.interpreted-text role="class"} that is used as the namespace for defining enum classes (see `prepare`{.interpreted-text role="ref"}). It is exposed to allow subclasses of `EnumType`{.interpreted-text role="class"} with advanced behavior like having multiple values per member. It should be called with the name of the enum class being created, otherwise private names and internal classes will not be handled correctly.

Note that only the `~collections.abc.MutableMapping`{.interpreted-text role="class"} interface (`~object.__setitem__`{.interpreted-text role="meth"} and `~dict.update`{.interpreted-text role="meth"}) is overridden. It may be possible to bypass the checks using other `!dict`{.interpreted-text role="class"} operations like `|= <object.__ior__>`{.interpreted-text role="meth"}.

::: attribute
EnumDict.member_names

A list of member names.
:::

::: versionadded
3.13
:::
:::::

------------------------------------------------------------------------

### Supported `__dunder__` names {#enum-dunder-sunder}

`~EnumType.__members__`{.interpreted-text role="attr"} is a read-only ordered mapping of `member_name`:`member` items. It is only available on the class.

`~Enum.__new__`{.interpreted-text role="meth"}, if specified, must create and return the enum members; it is also a very good idea to set the member\'s `~Enum._value_`{.interpreted-text role="attr"} appropriately. Once all the members are created it is no longer used.

### Supported `_sunder_` names

- `~Enum._name_`{.interpreted-text role="attr"} \-- name of the member
- `~Enum._value_`{.interpreted-text role="attr"} \-- value of the member; can be set in `__new__`
- `~Enum._missing_`{.interpreted-text role="meth"} \-- a lookup function used when a value is not found; may be overridden
- `~Enum._ignore_`{.interpreted-text role="attr"} \-- a list of names, either as a `list`{.interpreted-text role="class"} or a `str`{.interpreted-text role="class"}, that will not be transformed into members, and will be removed from the final class
- `~Enum._order_`{.interpreted-text role="attr"} \-- no longer used, kept for backward compatibility (class attribute, removed during class creation)
- `~Enum._generate_next_value_`{.interpreted-text role="meth"} \-- used to get an appropriate value for an enum member; may be overridden
- `~Enum._add_alias_`{.interpreted-text role="meth"} \-- adds a new name as an alias to an existing member.
- `~Enum._add_value_alias_`{.interpreted-text role="meth"} \-- adds a new value as an alias to an existing member.
- While `_sunder_` names are generally reserved for the further development of the `Enum`{.interpreted-text role="class"} class and can not be used, some are explicitly allowed:
  - `_repr_*` (e.g. `_repr_html_`), as used in [IPython\'s rich display](https://ipython.readthedocs.io/en/stable/config/integrating.html#rich-display)

::: versionadded
3.6 `_missing_`, `_order_`, `_generate_next_value_`
:::

::: versionadded
3.7 `_ignore_`
:::

::: versionadded
3.13 `_add_alias_`, `_add_value_alias_`, `_repr_*`
:::

------------------------------------------------------------------------

## Utilities and Decorators

:::::: auto
*auto* can be used in place of a value. If used, the *Enum* machinery will call an `Enum`{.interpreted-text role="class"}\'s `~Enum._generate_next_value_`{.interpreted-text role="meth"} to get an appropriate value. For `Enum`{.interpreted-text role="class"} and `IntEnum`{.interpreted-text role="class"} that appropriate value will be the last value plus one; for `Flag`{.interpreted-text role="class"} and `IntFlag`{.interpreted-text role="class"} it will be the first power-of-two greater than the highest value; for `StrEnum`{.interpreted-text role="class"} it will be the lower-cased version of the member\'s name. Care must be taken if mixing *auto()* with manually specified values.

*auto* instances are only resolved when at the top level of an assignment, either by itself or as part of a tuple:

- `FIRST = auto()` will work (auto() is replaced with `1`);
- `SECOND = auto(), -2` will work (auto is replaced with `2`, so `2, -2` is used to create the `SECOND` enum member;
- `THREE = [auto(), -3]` will *not* work (`[<auto instance>, -3]` is used to create the `THREE` enum member)

::: versionchanged
3.11.1

In prior versions, `auto()` had to be the only thing on the assignment line to work properly.
:::

`_generate_next_value_` can be overridden to customize the values used by *auto*.

:::: note
::: title
Note
:::

in 3.13 the default `_generate_next_value_` will always return the highest member value incremented by 1, and will fail if any member is an incompatible type.
::::
::::::

:::::: decorator
property

A decorator similar to the built-in *property*, but specifically for enumerations. It allows member attributes to have the same names as members themselves.

:::: note
::: title
Note
:::

the *property* and the member must be defined in separate classes; for example, the *value* and *name* attributes are defined in the *Enum* class, and *Enum* subclasses can define members with the names `value` and `name`.
::::

::: versionadded
3.11
:::
::::::

::: decorator
unique

A `class`{.interpreted-text role="keyword"} decorator specifically for enumerations. It searches an enumeration\'s `~EnumType.__members__`{.interpreted-text role="attr"}, gathering any aliases it finds; if any are found `ValueError`{.interpreted-text role="exc"} is raised with the details:

    >>> from enum import Enum, unique
    >>> @unique
    ... class Mistake(Enum):
    ...     ONE = 1
    ...     TWO = 2
    ...     THREE = 3
    ...     FOUR = 3
    ...
    Traceback (most recent call last):
    ...
    ValueError: duplicate values found in <enum 'Mistake'>: FOUR -> THREE
:::

:::: decorator
verify

A `class`{.interpreted-text role="keyword"} decorator specifically for enumerations. Members from `EnumCheck`{.interpreted-text role="class"} are used to specify which constraints should be checked on the decorated enumeration.

::: versionadded
3.11
:::
::::

:::: decorator
member

A decorator for use in enums: its target will become a member.

::: versionadded
3.11
:::
::::

:::: decorator
nonmember

A decorator for use in enums: its target will not become a member.

::: versionadded
3.11
:::
::::

:::: decorator
global_enum

A decorator to change the `str() <str>`{.interpreted-text role="class"} and `repr`{.interpreted-text role="func"} of an enum to show its members as belonging to the module instead of its class. Should only be used when the enum members are exported to the module global namespace (see `re.RegexFlag`{.interpreted-text role="class"} for an example).

::: versionadded
3.11
:::
::::

:::: function
show_flag_values(value)

Return a list of all power-of-two integers contained in a flag *value*.

::: versionadded
3.11
:::
::::

:::: function
bin(num, max_bits=None)

Like built-in `bin`{.interpreted-text role="func"}, except negative values are represented in two\'s complement, and the leading bit always indicates sign (`0` implies positive, `1` implies negative).

> \>\>\> import enum \>\>\> enum.bin(10) \'0b0 1010\' \>\>\> enum.bin(\~10) \# \~10 is -11 \'0b1 0101\'

::: versionadded
3.11
:::
::::

------------------------------------------------------------------------

## Notes

`IntEnum`{.interpreted-text role="class"}, `StrEnum`{.interpreted-text role="class"}, and `IntFlag`{.interpreted-text role="class"}

> These three enum types are designed to be drop-in replacements for existing integer- and string-based values; as such, they have extra limitations:
>
> - `__str__` uses the value and not the name of the enum member
> - `__format__`, because it uses `__str__`, will also use the value of the enum member instead of its name
>
> If you do not need/want those limitations, you can either create your own base class by mixing in the `int` or `str` type yourself:
>
>     >>> from enum import Enum
>     >>> class MyIntEnum(int, Enum):
>     ...     pass
>
> or you can reassign the appropriate `str`{.interpreted-text role="meth"}, etc., in your enum:
>
>     >>> from enum import Enum, IntEnum
>     >>> class MyIntEnum(IntEnum):
>     ...     __str__ = Enum.__str__
