# `!operator`{.interpreted-text role="mod"} \-\-- Standard operators as functions

::: {.module synopsis="Functions corresponding to the standard operators."}
operator
:::

**Source code:** `Lib/operator.py`{.interpreted-text role="source"}

::: testsetup
import operator from operator import itemgetter, iadd
:::

------------------------------------------------------------------------

The `!operator`{.interpreted-text role="mod"} module exports a set of efficient functions corresponding to the intrinsic operators of Python. For example, `operator.add(x, y)` is equivalent to the expression `x+y`. Many function names are those used for special methods, without the double underscores. For backward compatibility, many of these have a variant with the double underscores kept. The variants without the double underscores are preferred for clarity.

The functions fall into categories that perform object comparisons, logical operations, mathematical operations and sequence operations.

The object comparison functions are useful for all objects, and are named after the rich comparison operators they support:

::: function
lt(a, b) le(a, b) eq(a, b) ne(a, b) ge(a, b) gt(a, b) \_\_lt\_\_(a, b) \_\_le\_\_(a, b) \_\_eq\_\_(a, b) \_\_ne\_\_(a, b) \_\_ge\_\_(a, b) \_\_gt\_\_(a, b)

Perform \"rich comparisons\" between *a* and *b*. Specifically, `lt(a, b)` is equivalent to `a < b`, `le(a, b)` is equivalent to `a <= b`, `eq(a, b)` is equivalent to `a == b`, `ne(a, b)` is equivalent to `a != b`, `gt(a, b)` is equivalent to `a > b` and `ge(a, b)` is equivalent to `a >= b`. Note that these functions can return any value, which may or may not be interpretable as a Boolean value. See `comparisons`{.interpreted-text role="ref"} for more information about rich comparisons.
:::

The logical operations are also generally applicable to all objects, and support truth tests, identity tests, and boolean operations:

::: function
[not]()(obj) \_\_not\_\_(obj)

Return the outcome of `not`{.interpreted-text role="keyword"} *obj*. (Note that there is no `!__not__`{.interpreted-text role="meth"} method for object instances; only the interpreter core defines this operation. The result is affected by the `~object.__bool__`{.interpreted-text role="meth"} and `~object.__len__`{.interpreted-text role="meth"} methods.)
:::

::: function
truth(obj)

Return `True`{.interpreted-text role="const"} if *obj* is true, and `False`{.interpreted-text role="const"} otherwise. This is equivalent to using the `bool`{.interpreted-text role="class"} constructor.
:::

::: function
[is]()(a, b)

Return `a is b`. Tests object identity.
:::

::: function
is_not(a, b)

Return `a is not b`. Tests object identity.
:::

:::: function
is_none(a)

Return `a is None`. Tests object identity.

::: versionadded
3.14
:::
::::

:::: function
is_not_none(a)

Return `a is not None`. Tests object identity.

::: versionadded
3.14
:::
::::

The mathematical and bitwise operations are the most numerous:

::: function
abs(obj) \_\_abs\_\_(obj)

Return the absolute value of *obj*.
:::

::: function
add(a, b) \_\_add\_\_(a, b)

Return `a + b`, for *a* and *b* numbers.
:::

::: function
[and]()(a, b) \_\_and\_\_(a, b)

Return the bitwise and of *a* and *b*.
:::

::: function
floordiv(a, b) \_\_floordiv\_\_(a, b)

Return `a // b`.
:::

:::: function
index(a) \_\_index\_\_(a)

Return *a* converted to an integer. Equivalent to `a.__index__()`.

::: versionchanged
3.10 The result always has exact type `int`{.interpreted-text role="class"}. Previously, the result could have been an instance of a subclass of `int`.
:::
::::

::: function
inv(obj) invert(obj) \_\_inv\_\_(obj) \_\_invert\_\_(obj)

Return the bitwise inverse of the number *obj*. This is equivalent to `~obj`.
:::

::: function
lshift(a, b) \_\_lshift\_\_(a, b)

Return *a* shifted left by *b*.
:::

::: function
mod(a, b) \_\_mod\_\_(a, b)

Return `a % b`.
:::

::: function
mul(a, b) \_\_mul\_\_(a, b)

Return `a * b`, for *a* and *b* numbers.
:::

:::: function
matmul(a, b) \_\_matmul\_\_(a, b)

Return `a @ b`.

::: versionadded
3.5
:::
::::

::: function
neg(obj) \_\_neg\_\_(obj)

Return *obj* negated (`-obj`).
:::

::: function
[or]()(a, b) \_\_or\_\_(a, b)

Return the bitwise or of *a* and *b*.
:::

::: function
pos(obj) \_\_pos\_\_(obj)

Return *obj* positive (`+obj`).
:::

::: function
pow(a, b) \_\_pow\_\_(a, b)

Return `a ** b`, for *a* and *b* numbers.
:::

::: function
rshift(a, b) \_\_rshift\_\_(a, b)

Return *a* shifted right by *b*.
:::

::: function
sub(a, b) \_\_sub\_\_(a, b)

Return `a - b`.
:::

::: function
truediv(a, b) \_\_truediv\_\_(a, b)

Return `a / b` where 2/3 is .66 rather than 0. This is also known as \"true\" division.
:::

::: function
xor(a, b) \_\_xor\_\_(a, b)

Return the bitwise exclusive or of *a* and *b*.
:::

Operations which work with sequences (some of them with mappings too) include:

::: function
concat(a, b) \_\_concat\_\_(a, b)

Return `a + b` for *a* and *b* sequences.
:::

::: function
contains(a, b) \_\_contains\_\_(a, b)

Return the outcome of the test `b in a`. Note the reversed operands.
:::

::: function
countOf(a, b)

Return the number of occurrences of *b* in *a*.
:::

::: function
delitem(a, b) \_\_delitem\_\_(a, b)

Remove the value of *a* at index *b*.
:::

::: function
getitem(a, b) \_\_getitem\_\_(a, b)

Return the value of *a* at index *b*.
:::

::: function
indexOf(a, b)

Return the index of the first of occurrence of *b* in *a*.
:::

::: function
setitem(a, b, c) \_\_setitem\_\_(a, b, c)

Set the value of *a* at index *b* to *c*.
:::

:::: function
length_hint(obj, default=0)

Return an estimated length for the object *obj*. First try to return its actual length, then an estimate using `object.__length_hint__`{.interpreted-text role="meth"}, and finally return the default value.

::: versionadded
3.4
:::
::::

The following operation works with callables:

:::: function
call(obj, /, *args,kwargs) \_\_call\_\_(obj, /,*args, \*\*kwargs)

Return `obj(*args, **kwargs)`.

::: versionadded
3.11
:::
::::

The `!operator`{.interpreted-text role="mod"} module also defines tools for generalized attribute and item lookups. These are useful for making fast field extractors as arguments for `map`{.interpreted-text role="func"}, `sorted`{.interpreted-text role="func"}, `itertools.groupby`{.interpreted-text role="meth"}, or other functions that expect a function argument.

::: function
attrgetter(attr) attrgetter(\*attrs)

Return a callable object that fetches *attr* from its operand. If more than one attribute is requested, returns a tuple of attributes. The attribute names can also contain dots. For example:

- After `f = attrgetter('name')`, the call `f(b)` returns `b.name`.
- After `f = attrgetter('name', 'date')`, the call `f(b)` returns `(b.name, b.date)`.
- After `f = attrgetter('name.first', 'name.last')`, the call `f(b)` returns `(b.name.first, b.name.last)`.

Equivalent to:

    def attrgetter(*items):
        if any(not isinstance(item, str) for item in items):
            raise TypeError('attribute name must be a string')
        if len(items) == 1:
            attr = items[0]
            def g(obj):
                return resolve_attr(obj, attr)
        else:
            def g(obj):
                return tuple(resolve_attr(obj, attr) for attr in items)
        return g

    def resolve_attr(obj, attr):
        for name in attr.split("."):
            obj = getattr(obj, name)
        return obj
:::

::: function
itemgetter(item) itemgetter(\*items)

Return a callable object that fetches *item* from its operand using the operand\'s `~object.__getitem__`{.interpreted-text role="meth"} method. If multiple items are specified, returns a tuple of lookup values. For example:

- After `f = itemgetter(2)`, the call `f(r)` returns `r[2]`.
- After `g = itemgetter(2, 5, 3)`, the call `g(r)` returns `(r[2], r[5], r[3])`.

Equivalent to:

    def itemgetter(*items):
        if len(items) == 1:
            item = items[0]
            def g(obj):
                return obj[item]
        else:
            def g(obj):
                return tuple(obj[item] for item in items)
        return g

The items can be any type accepted by the operand\'s `~object.__getitem__`{.interpreted-text role="meth"} method. Dictionaries accept any `hashable`{.interpreted-text role="term"} value. Lists, tuples, and strings accept an index or a slice:

> \>\>\> itemgetter(1)(\'ABCDEFG\') \'B\' \>\>\> itemgetter(1, 3, 5)(\'ABCDEFG\') (\'B\', \'D\', \'F\') \>\>\> itemgetter(slice(2, None))(\'ABCDEFG\') \'CDEFG\' \>\>\> soldier = dict(rank=\'captain\', name=\'dotterbart\') \>\>\> itemgetter(\'rank\')(soldier) \'captain\'

Example of using `itemgetter`{.interpreted-text role="func"} to retrieve specific fields from a tuple record:

> \>\>\> inventory = \[(\'apple\', 3), (\'banana\', 2), (\'pear\', 5), (\'orange\', 1)\] \>\>\> getcount = itemgetter(1) \>\>\> list(map(getcount, inventory)) \[3, 2, 5, 1\] \>\>\> sorted(inventory, key=getcount) \[(\'orange\', 1), (\'banana\', 2), (\'apple\', 3), (\'pear\', 5)\]
:::

::: function
methodcaller(name, /, *args,*\*kwargs)

Return a callable object that calls the method *name* on its operand. If additional arguments and/or keyword arguments are given, they will be given to the method as well. For example:

- After `f = methodcaller('name')`, the call `f(b)` returns `b.name()`.
- After `f = methodcaller('name', 'foo', bar=1)`, the call `f(b)` returns `b.name('foo', bar=1)`.

Equivalent to:

    def methodcaller(name, /, *args, **kwargs):
        def caller(obj):
            return getattr(obj, name)(*args, **kwargs)
        return caller
:::

## Mapping Operators to Functions {#operator-map}

This table shows how abstract operations correspond to operator symbols in the Python syntax and the functions in the `!operator`{.interpreted-text role="mod"} module.

  -----------------------------------------------------------------------------------
  Operation               Syntax                Function
  ----------------------- --------------------- -------------------------------------
  Addition                `a + b`               `add(a, b)`

  Concatenation           `seq1 + seq2`         `concat(seq1, seq2)`

  Containment Test        `obj in seq`          `contains(seq, obj)`

  Division                `a / b`               `truediv(a, b)`

  Division                `a // b`              `floordiv(a, b)`

  Bitwise And             `a & b`               `and_(a, b)`

  Bitwise Exclusive Or    `a ^ b`               `xor(a, b)`

  Bitwise Inversion       `~ a`                 `invert(a)`

  Bitwise Or              `a | b`               `or_(a, b)`

  Exponentiation          `a ** b`              `pow(a, b)`

  Identity                `a is b`              `is_(a, b)`

  Identity                `a is not b`          `is_not(a, b)`

  Identity                `a is None`           `is_none(a)`

  Identity                `a is not None`       `is_not_none(a)`

  Indexed Assignment      `obj[k] = v`          `setitem(obj, k, v)`

  Indexed Deletion        `del obj[k]`          `delitem(obj, k)`

  Indexing                `obj[k]`              `getitem(obj, k)`

  Left Shift              `a << b`              `lshift(a, b)`

  Modulo                  `a % b`               `mod(a, b)`

  Multiplication          `a * b`               `mul(a, b)`

  Matrix Multiplication   `a @ b`               `matmul(a, b)`

  Negation (Arithmetic)   `- a`                 `neg(a)`

  Negation (Logical)      `not a`               `not_(a)`

  Positive                `+ a`                 `pos(a)`

  Right Shift             `a >> b`              `rshift(a, b)`

  Slice Assignment        `seq[i:j] = values`   `setitem(seq, slice(i, j), values)`

  Slice Deletion          `del seq[i:j]`        `delitem(seq, slice(i, j))`

  Slicing                 `seq[i:j]`            `getitem(seq, slice(i, j))`

  String Formatting       `s % obj`             `mod(s, obj)`

  Subtraction             `a - b`               `sub(a, b)`

  Truth Test              `obj`                 `truth(obj)`

  Ordering                `a < b`               `lt(a, b)`

  Ordering                `a <= b`              `le(a, b)`

  Equality                `a == b`              `eq(a, b)`

  Difference              `a != b`              `ne(a, b)`

  Ordering                `a >= b`              `ge(a, b)`

  Ordering                `a > b`               `gt(a, b)`
  -----------------------------------------------------------------------------------

## In-place Operators

Many operations have an \"in-place\" version. Listed below are functions providing a more primitive access to in-place operators than the usual syntax does; for example, the `statement`{.interpreted-text role="term"} `x += y` is equivalent to `x = operator.iadd(x, y)`. Another way to put it is to say that `z = operator.iadd(x, y)` is equivalent to the compound statement `z = x; z += y`.

In those examples, note that when an in-place method is called, the computation and assignment are performed in two separate steps. The in-place functions listed below only do the first step, calling the in-place method. The second step, assignment, is not handled.

For immutable targets such as strings, numbers, and tuples, the updated value is computed, but not assigned back to the input variable:

\>\>\> a = \'hello\' \>\>\> iadd(a, \' world\') \'hello world\' \>\>\> a \'hello\'

For mutable targets such as lists and dictionaries, the in-place method will perform the update, so no subsequent assignment is necessary:

\>\>\> s = \[\'h\', \'e\', \'l\', \'l\', \'o\'\] \>\>\> iadd(s, \[\' \', \'w\', \'o\', \'r\', \'l\', \'d\'\]) \[\'h\', \'e\', \'l\', \'l\', \'o\', \' \', \'w\', \'o\', \'r\', \'l\', \'d\'\] \>\>\> s \[\'h\', \'e\', \'l\', \'l\', \'o\', \' \', \'w\', \'o\', \'r\', \'l\', \'d\'\]

::: function
iadd(a, b) \_\_iadd\_\_(a, b)

`a = iadd(a, b)` is equivalent to `a += b`.
:::

::: function
iand(a, b) \_\_iand\_\_(a, b)

`a = iand(a, b)` is equivalent to `a &= b`.
:::

::: function
iconcat(a, b) \_\_iconcat\_\_(a, b)

`a = iconcat(a, b)` is equivalent to `a += b` for *a* and *b* sequences.
:::

::: function
ifloordiv(a, b) \_\_ifloordiv\_\_(a, b)

`a = ifloordiv(a, b)` is equivalent to `a //= b`.
:::

::: function
ilshift(a, b) \_\_ilshift\_\_(a, b)

`a = ilshift(a, b)` is equivalent to `a <<= b`.
:::

::: function
imod(a, b) \_\_imod\_\_(a, b)

`a = imod(a, b)` is equivalent to `a %= b`.
:::

::: function
imul(a, b) \_\_imul\_\_(a, b)

`a = imul(a, b)` is equivalent to `a *= b`.
:::

:::: function
imatmul(a, b) \_\_imatmul\_\_(a, b)

`a = imatmul(a, b)` is equivalent to `a @= b`.

::: versionadded
3.5
:::
::::

::: function
ior(a, b) \_\_ior\_\_(a, b)

`a = ior(a, b)` is equivalent to `a |= b`.
:::

::: function
ipow(a, b) \_\_ipow\_\_(a, b)

`a = ipow(a, b)` is equivalent to `a **= b`.
:::

::: function
irshift(a, b) \_\_irshift\_\_(a, b)

`a = irshift(a, b)` is equivalent to `a >>= b`.
:::

::: function
isub(a, b) \_\_isub\_\_(a, b)

`a = isub(a, b)` is equivalent to `a -= b`.
:::

::: function
itruediv(a, b) \_\_itruediv\_\_(a, b)

`a = itruediv(a, b)` is equivalent to `a /= b`.
:::

::: function
ixor(a, b) \_\_ixor\_\_(a, b)

`a = ixor(a, b)` is equivalent to `a ^= b`.
:::
