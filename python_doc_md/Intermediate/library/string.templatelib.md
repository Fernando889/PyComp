# `!string.templatelib`{.interpreted-text role="mod"} \-\-- Support for template string literals

::: {.module synopsis="Support for template string literals."}
string.templatelib
:::

**Source code:** `Lib/string/templatelib.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

::: seealso
- `Format strings <f-strings>`{.interpreted-text role="ref"}
- `Template string literal (t-string) syntax <t-strings>`{.interpreted-text role="ref"}
- `750`{.interpreted-text role="pep"}
:::

## Template strings

::: versionadded
3.14
:::

Template strings are a mechanism for custom string processing. They have the full flexibility of Python\'s `f-strings`{.interpreted-text role="ref"}, but return a `Template`{.interpreted-text role="class"} instance that gives access to the static and interpolated (in curly brackets) parts of a string *before* they are combined.

To write a t-string, use a `'t'` prefix instead of an `'f'`, like so:

``` pycon
>>> pi = 3.14
>>> t't-strings are new in Python {pi!s}!'
Template(
   strings=('t-strings are new in Python ', '!'),
   interpolations=(Interpolation(3.14, 'pi', 's', ''),)
)
```

## Types

::::::::::: Template
The `!Template`{.interpreted-text role="class"} class describes the contents of a template string. It is immutable, meaning that attributes of a template cannot be reassigned.

The most common way to create a `!Template`{.interpreted-text role="class"} instance is to use the `template string literal syntax <t-strings>`{.interpreted-text role="ref"}. This syntax is identical to that of `f-strings <f-strings>`{.interpreted-text role="ref"}, except that it uses a `t` prefix in place of an `f`:

\>\>\> cheese = \'Red Leicester\' \>\>\> template = t\"We\'re fresh out of {cheese}, sir.\" \>\>\> type(template) \<class \'string.templatelib.Template\'\>

Templates are stored as sequences of literal `~Template.strings`{.interpreted-text role="attr"} and dynamic `~Template.interpolations`{.interpreted-text role="attr"}. A `~Template.values`{.interpreted-text role="attr"} attribute holds the values of the interpolations:

\>\>\> cheese = \'Camembert\' \>\>\> template = t\'Ah! We do have {cheese}.\' \>\>\> template.strings (\'Ah! We do have \', \'.\') \>\>\> template.interpolations (Interpolation(\'Camembert\', \...),) \>\>\> template.values (\'Camembert\',)

The `!strings`{.interpreted-text role="attr"} tuple has one more element than `!interpolations`{.interpreted-text role="attr"} and `!values`{.interpreted-text role="attr"}; the interpolations "belong" between the strings. This may be easier to understand when tuples are aligned

``` python
template.strings:  ('Ah! We do have ',              '.')
template.values:   (                   'Camembert',    )
```

**Attributes**

::: {.attribute type="tuple[str, ...]"}
strings

A `tuple`{.interpreted-text role="class"} of the static strings in the template.

\>\>\> cheese = \'Camembert\' \>\>\> template = t\'Ah! We do have {cheese}.\' \>\>\> template.strings (\'Ah! We do have \', \'.\')

Empty strings *are* included in the tuple:

\>\>\> response = \'We do have \' \>\>\> cheese = \'Camembert\' \>\>\> template = t\'Ah! {response}{cheese}.\' \>\>\> template.strings (\'Ah! \', \'\', \'.\')

The `strings` tuple is never empty, and always contains one more string than the `interpolations` and `values` tuples:

\>\>\> t\'\'.strings (\'\',) \>\>\> t\'\'.values () \>\>\> t\'{\'cheese\'}\'.strings (\'\', \'\') \>\>\> t\'{\'cheese\'}\'.values (\'cheese\',)
:::

::: {.attribute type="tuple[Interpolation, ...]"}
interpolations

A `tuple`{.interpreted-text role="class"} of the interpolations in the template.

\>\>\> cheese = \'Camembert\' \>\>\> template = t\'Ah! We do have {cheese}.\' \>\>\> template.interpolations (Interpolation(\'Camembert\', \'cheese\', None, \'\'),)

The `interpolations` tuple may be empty and always contains one fewer values than the `strings` tuple:

\>\>\> t\'Red Leicester\'.interpolations ()
:::

::: {.attribute type="tuple[object, ...]"}
values

A tuple of all interpolated values in the template.

\>\>\> cheese = \'Camembert\' \>\>\> template = t\'Ah! We do have {cheese}.\' \>\>\> template.values (\'Camembert\',)

The `values` tuple always has the same length as the `interpolations` tuple. It is always equivalent to `tuple(i.value for i in template.interpolations)`.
:::

**Methods**

::: method
\_\_new\_\_(\*args: str \| Interpolation)

While literal syntax is the most common way to create a `!Template`{.interpreted-text role="class"}, it is also possible to create them directly using the constructor:

\>\>\> from string.templatelib import Interpolation, Template \>\>\> cheese = \'Camembert\' \>\>\> template = Template( \... \'Ah! We do have \', Interpolation(cheese, \'cheese\'), \'.\' \... ) \>\>\> list(template) \[\'Ah! We do have \', Interpolation(\'Camembert\', \'cheese\', None, \'\'), \'.\'\]

If multiple strings are passed consecutively, they will be concatenated into a single value in the `~Template.strings`{.interpreted-text role="attr"} attribute. For example, the following code creates a `Template`{.interpreted-text role="class"} with a single final string:

\>\>\> from string.templatelib import Template \>\>\> template = Template(\'Ah! We do have \', \'Camembert\', \'.\') \>\>\> template.strings (\'Ah! We do have Camembert.\',)

If multiple interpolations are passed consecutively, they will be treated as separate interpolations and an empty string will be inserted between them. For example, the following code creates a template with empty placeholders in the `~Template.strings`{.interpreted-text role="attr"} attribute:

\>\>\> from string.templatelib import Interpolation, Template \>\>\> template = Template( \... Interpolation(\'Camembert\', \'cheese\'), \... Interpolation(\'.\', \'punctuation\'), \... ) \>\>\> template.strings (\'\', \'\', \'\')
:::

::::: describe
iter(template)

Iterate over the template, yielding each non-empty string and `Interpolation`{.interpreted-text role="class"} in the correct order:

\>\>\> cheese = \'Camembert\' \>\>\> list(t\'Ah! We do have {cheese}.\') \[\'Ah! We do have \', Interpolation(\'Camembert\', \'cheese\', None, \'\'), \'.\'\]

:::: caution
::: title
Caution
:::

Empty strings are **not** included in the iteration:

\>\>\> response = \'We do have \' \>\>\> cheese = \'Camembert\' \>\>\> list(t\'Ah! {response}{cheese}.\') \# doctest: +NORMALIZE_WHITESPACE \[\'Ah! \', Interpolation(\'We do have \', \'response\', None, \'\'), Interpolation(\'Camembert\', \'cheese\', None, \'\'), \'.\'\]
::::
:::::

::: describe
template + other template += other

Concatenate this template with another, returning a new `!Template`{.interpreted-text role="class"} instance:

\>\>\> cheese = \'Camembert\' \>\>\> list(t\'Ah! \' + t\'We do have {cheese}.\') \[\'Ah! We do have \', Interpolation(\'Camembert\', \'cheese\', None, \'\'), \'.\'\]

Concatenating a `!Template`{.interpreted-text role="class"} and a `str` is **not** supported. This is because it is unclear whether the string should be treated as a static string or an interpolation. If you want to concatenate a `!Template`{.interpreted-text role="class"} with a string, you should either wrap the string directly in a `!Template`{.interpreted-text role="class"} (to treat it as a static string) or use an `!Interpolation`{.interpreted-text role="class"} (to treat it as dynamic):

\>\>\> from string.templatelib import Interpolation, Template \>\>\> template = t\'Ah! \' \>\>\> \# Treat \'We do have \' as a static string \>\>\> template += Template(\'We do have \') \>\>\> \# Treat cheese as an interpolation \>\>\> cheese = \'Camembert\' \>\>\> template += Template(Interpolation(cheese, \'cheese\')) \>\>\> list(template) \[\'Ah! We do have \', Interpolation(\'Camembert\', \'cheese\', None, \'\')\]
:::
:::::::::::

:::::::::::: Interpolation
The `!Interpolation`{.interpreted-text role="class"} type represents an expression inside a template string. It is immutable, meaning that attributes of an interpolation cannot be reassigned.

Interpolations support pattern matching, allowing you to match against their attributes with the `match statement <match>`{.interpreted-text role="ref"}:

\>\>\> from string.templatelib import Interpolation \>\>\> interpolation = t\'{1. + 2.:.2f}\'.interpolations\[0\] \>\>\> interpolation Interpolation(3.0, \'1. + 2.\', None, \'.2f\') \>\>\> match interpolation: \... case Interpolation(value, expression, conversion, format_spec): \... print(value, expression, conversion, format_spec, sep=\' \| \') \... 3.0 \| 1. + 2. \| None \| .2f

**Attributes**

::: {.attribute type="object"}
value

The evaluated value of the interpolation.

\>\>\> t\'{1 + 2}\'.interpolations\[0\].value 3
:::

::: {.attribute type="str"}
expression

For interpolations created by t-string literals, `!expression`{.interpreted-text role="attr"} is the expression text found inside the curly brackets (`{` & `}`), including any whitespace, excluding the curly brackets themselves, and ending before the first `!`, `:`, or `=` if any is present. For manually created interpolations, `!expression`{.interpreted-text role="attr"} is the arbitrary string provided when constructing the interpolation instance.

We recommend using valid Python expressions or the empty string for the `expression` field of manually created `!Interpolation`{.interpreted-text role="class"} instances, although this is not enforced at runtime.

\>\>\> t\'{1 + 2}\'.interpolations\[0\].expression \'1 + 2\'
:::

::::: {.attribute type="typing.Literal['a', 'r', 's'] | None"}
conversion

The conversion to apply to the value, or `None`.

The `!conversion`{.interpreted-text role="attr"} is the optional conversion to apply to the value:

\>\>\> t\'{1 + 2!a}\'.interpolations\[0\].conversion \'a\'

:::: note
::: title
Note
:::

Unlike f-strings, where conversions are applied automatically, the expected behavior with t-strings is that code that *processes* the `!Template`{.interpreted-text role="class"} will decide how to interpret and whether to apply the `!conversion`{.interpreted-text role="attr"}. For convenience, the `convert`{.interpreted-text role="func"} function can be used to mimic f-string conversion semantics.
::::
:::::

::::: {.attribute type="str"}
format_spec

The format specification to apply to the value.

The `!format_spec`{.interpreted-text role="attr"} is an optional, arbitrary string used as the format specification to present the value:

\>\>\> t\'{1 + 2:.2f}\'.interpolations\[0\].format_spec \'.2f\'

:::: note
::: title
Note
:::

Unlike f-strings, where format specifications are applied automatically via the `format`{.interpreted-text role="func"} protocol, the expected behavior with t-strings is that code that *processes* the interpolation will decide how to interpret and whether to apply the format specification. As a result, `!format_spec`{.interpreted-text role="attr"} values in interpolations can be arbitrary strings, including those that do not conform to the `format`{.interpreted-text role="func"} protocol.
::::
:::::

**Methods**

::: method
\_\_new\_\_(value: object, expression: str, conversion: typing.Literal\[\'a\', \'r\', \'s\'\] \| None = None, format_spec: str = \'\')

Create a new `!Interpolation`{.interpreted-text role="class"} object from component parts.

param value
:   The evaluated, in-scope result of the interpolation.

param expression
:   The text of a valid Python expression, or an empty string.

param conversion
:   The `conversion <formatstrings>`{.interpreted-text role="ref"} to be used, one of `None`, `'a'`, `'r'`, or `'s'`.

param format_spec
:   An optional, arbitrary string used as the `format specification <formatspec>`{.interpreted-text role="ref"} to present the value.
:::
::::::::::::

## Helper functions

::: function
convert(obj, /, conversion)

Applies formatted string literal `conversion <formatstrings-conversion>`{.interpreted-text role="ref"} semantics to the given object *obj*. This is frequently useful for custom template string processing logic.

Three conversion flags are currently supported:

- `'s'` which calls `str`{.interpreted-text role="func"} on the value (like `!s`),
- `'r'` which calls `repr`{.interpreted-text role="func"} (like `!r`), and
- `'a'` which calls `ascii`{.interpreted-text role="func"} (like `!a`).

If the conversion flag is `None`, *obj* is returned unchanged.
:::
