# `!reprlib`{.interpreted-text role="mod"} \-\-- Alternate `repr`{.interpreted-text role="func"} implementation

::: {.module synopsis="Alternate repr() implementation with size limits."}
reprlib
:::

**Source code:** `Lib/reprlib.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!reprlib`{.interpreted-text role="mod"} module provides a means for producing object representations with limits on the size of the resulting strings. This is used in the Python debugger and may be useful in other contexts as well.

This module provides a class, an instance, and a function:

:::: {.Repr(*, .maxlevel=6, .maxtuple=6, .maxlist=6, .maxarray=5, .maxdict=4, .\\ .maxset=6, .maxfrozenset=6, .maxdeque=6, .maxstring=30, .maxlong=40, .\\ .maxother=30, .fillvalue=\"...\", .indent=None)}
Class which provides formatting services useful in implementing functions similar to the built-in `repr`{.interpreted-text role="func"}; size limits for different object types are added to avoid the generation of representations which are excessively long.

The keyword arguments of the constructor can be used as a shortcut to set the attributes of the `Repr`{.interpreted-text role="class"} instance. Which means that the following initialization:

    aRepr = reprlib.Repr(maxlevel=3)

Is equivalent to:

    aRepr = reprlib.Repr()
    aRepr.maxlevel = 3

See section [Repr Objects](#repr-objects) for more information about `Repr`{.interpreted-text role="class"} attributes.

::: versionchanged
3.12 Allow attributes to be set via keyword arguments.
:::
::::

::: data
aRepr

This is an instance of `Repr`{.interpreted-text role="class"} which is used to provide the `.repr`{.interpreted-text role="func"} function described below. Changing the attributes of this object will affect the size limits used by `.repr`{.interpreted-text role="func"} and the Python debugger.
:::

::: function
repr(obj)

This is the `~Repr.repr`{.interpreted-text role="meth"} method of `aRepr`. It returns a string similar to that returned by the built-in function of the same name, but with limits on most sizes.
:::

In addition to size-limiting tools, the module also provides a decorator for detecting recursive calls to `~object.__repr__`{.interpreted-text role="meth"} and substituting a placeholder string instead.

::: index
single: \...; placeholder
:::

::::: decorator
recursive_repr(fillvalue=\"\...\")

Decorator for `~object.__repr__`{.interpreted-text role="meth"} methods to detect recursive calls within the same thread. If a recursive call is made, the *fillvalue* is returned, otherwise, the usual `!__repr__`{.interpreted-text role="meth"} call is made. For example:

::: doctest
\>\>\> from reprlib import recursive_repr \>\>\> class MyList(list): \... \@recursive_repr() \... def \_\_repr\_\_(self): \... return \'\<\' + \'[\|\'.join(map(repr, self)) + \'\>\' \... \>\>\> m = MyList(\'abc\') \>\>\> m.append(m) \>\>\> m.append(\'x\') \>\>\> print(m) \<\'a\'\|](##SUBST##|'.join(map(repr, self)) + '>'
...
>>> m = MyList('abc')
>>> m.append(m)
>>> m.append('x')
>>> print(m)
<'a'|)\'b\'[\|\'c\'\|](##SUBST##|'c'|)\...\|\'x\'\>
:::

::: versionadded
3.2
:::
:::::

## Repr Objects

`Repr`{.interpreted-text role="class"} instances provide several attributes which can be used to provide size limits for the representations of different object types, and methods which format specific object types.

:::: attribute
Repr.fillvalue

This string is displayed for recursive references. It defaults to `...`.

::: versionadded
3.11
:::
::::

::: attribute
Repr.maxlevel

Depth limit on the creation of recursive representations. The default is `6`.
:::

::: attribute
Repr.maxdict Repr.maxlist Repr.maxtuple Repr.maxset Repr.maxfrozenset Repr.maxdeque Repr.maxarray

Limits on the number of entries represented for the named object type. The default is `4` for `maxdict`{.interpreted-text role="attr"}, `5` for `maxarray`{.interpreted-text role="attr"}, and `6` for the others.
:::

::: attribute
Repr.maxlong

Maximum number of characters in the representation for an integer. Digits are dropped from the middle. The default is `40`.
:::

::: attribute
Repr.maxstring

Limit on the number of characters in the representation of the string. Note that the \"normal\" representation of the string is used as the character source: if escape sequences are needed in the representation, these may be mangled when the representation is shortened. The default is `30`.
:::

::: attribute
Repr.maxother

This limit is used to control the size of object types for which no specific formatting method is available on the `Repr`{.interpreted-text role="class"} object. It is applied in a similar manner as `maxstring`{.interpreted-text role="attr"}. The default is `20`.
:::

::::::: attribute
Repr.indent

If this attribute is set to `None` (the default), the output is formatted with no line breaks or indentation, like the standard `repr`{.interpreted-text role="func"}. For example:

::: doctest
indent

\>\>\> example = \[ \... 1, \'spam\', {\'a\': 2, \'b\': \'spam eggs\', \'c\': {3: 4.5, 6: \[\]}}, \'ham\'\] \>\>\> import reprlib \>\>\> aRepr = reprlib.Repr() \>\>\> print(aRepr.repr(example)) \[1, \'spam\', {\'a\': 2, \'b\': \'spam eggs\', \'c\': {3: 4.5, 6: \[\]}}, \'ham\'\]
:::

If `~Repr.indent`{.interpreted-text role="attr"} is set to a string, each recursion level is placed on its own line, indented by that string:

::: doctest
indent

\>\>\> aRepr.indent = \'\--\>\' \>\>\> print(aRepr.repr(example)) \[ \--\>1, \--\>\'spam\', \--\>{ \--\>\--\>\'a\': 2, \--\>\--\>\'b\': \'spam eggs\', \--\>\--\>\'c\': { \--\>\--\>\--\>3: 4.5, \--\>\--\>\--\>6: \[\], \--\>\--\>}, \--\>}, \--\>\'ham\', \]
:::

Setting `~Repr.indent`{.interpreted-text role="attr"} to a positive integer value behaves as if it was set to a string with that number of spaces:

::: doctest
indent

\>\>\> aRepr.indent = 4 \>\>\> print(aRepr.repr(example)) \[ 1, \'spam\', { \'a\': 2, \'b\': \'spam eggs\', \'c\': { 3: 4.5, 6: \[\], }, }, \'ham\', \]
:::

::: versionadded
3.12
:::
:::::::

::: method
Repr.repr(obj)

The equivalent to the built-in `repr`{.interpreted-text role="func"} that uses the formatting imposed by the instance.
:::

::: method
Repr.repr1(obj, level)

Recursive implementation used by `.repr`{.interpreted-text role="meth"}. This uses the type of *obj* to determine which formatting method to call, passing it *obj* and *level*. The type-specific methods should call `repr1`{.interpreted-text role="meth"} to perform recursive formatting, with `level - 1` for the value of *level* in the recursive call.
:::

::: {.method noindex=""}
Repr.repr_TYPE(obj, level)

Formatting methods for specific types are implemented as methods with a name based on the type name. In the method name, **TYPE** is replaced by `'_'.join(type(obj).__name__.split())`. Dispatch to these methods is handled by `repr1`{.interpreted-text role="meth"}. Type-specific methods which need to recursively format a value should call `self.repr1(subobj, level - 1)`.
:::

## Subclassing Repr Objects {#subclassing-reprs}

The use of dynamic dispatching by `Repr.repr1`{.interpreted-text role="meth"} allows subclasses of `Repr`{.interpreted-text role="class"} to add support for additional built-in object types or to modify the handling of types already supported. This example shows how special support for file objects could be added:

::: testcode
import reprlib import sys

class MyRepr(reprlib.Repr):

> 
>
> def repr_TextIOWrapper(self, obj, level):
>
> :   
>
>     if obj.name in {\'\<stdin\>\', \'\<stdout\>\', \'\<stderr\>\'}:
>
>     :   return obj.name
>
>     return repr(obj)

aRepr = MyRepr() print(aRepr.repr(sys.stdin)) \# prints \'\<stdin\>\'
:::

::: testoutput
\<stdin\>
:::
