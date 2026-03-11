# Built-in Functions {#built-in-funcs}

The Python interpreter has a number of functions and types built into it that are always available. They are listed here in alphabetical order.

+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| > Built-in Functions                                                                                                                                                                                                                                                                                                                                                                                                                |
+====================================================================================================================+=========================================================================+=================================================================+====================================================================================================================================================================+
| |  \*\*A\*\*                                                                                                       | |  \*\*E\*\*                                                            | |  \*\*L\*\*                                                    | |  \*\*R\*\*                                                                                                                                                       |
| |  `abs`{.interpreted-text role="func"}                                                                            | |  `enumerate`{.interpreted-text role="func"}                           | |  `len`{.interpreted-text role="func"}                         | |  [`range()`](..%20class::%20range(stop,%20/)range(start,%20stop,%20step=1,%20/):noindex:)                                                                        |
| |  `aiter`{.interpreted-text role="func"}                                                                          | |  `eval`{.interpreted-text role="func"}                                | |  [`list()`](..%20class::%20list(iterable=(),%20/):noindex:)   | |  `repr`{.interpreted-text role="func"}                                                                                                                           |
| |  `all`{.interpreted-text role="func"}                                                                            | |  `exec`{.interpreted-text role="func"}                                | |  `locals`{.interpreted-text role="func"}                      | |  `reversed`{.interpreted-text role="func"}                                                                                                                       |
| |  `anext`{.interpreted-text role="func"}                                                                          | |                                                                       | |                                                               | |  `round`{.interpreted-text role="func"}                                                                                                                          |
| |  `any`{.interpreted-text role="func"}                                                                            | |  \*\*F\*\*                                                            | |  \*\*M\*\*                                                    | |                                                                                                                                                                  |
| |  `ascii`{.interpreted-text role="func"}                                                                          | |  `filter`{.interpreted-text role="func"}                              | |  `map`{.interpreted-text role="func"}                         | |  \*\*S\*\*                                                                                                                                                       |
| |                                                                                                                  | |  `float`{.interpreted-text role="func"}                               | |  `max`{.interpreted-text role="func"}                         | |  [`set()`](..%20class::%20set(iterable=(),%20/):noindex:)                                                                                                        |
| |  \*\*B\*\*                                                                                                       | |  `format`{.interpreted-text role="func"}                              | |  [`memoryview()`](..%20class::%20memoryview(object):noindex:) | |  `setattr`{.interpreted-text role="func"}                                                                                                                        |
| |  `bin`{.interpreted-text role="func"}                                                                            | |  [`frozenset()`](..%20class::%20frozenset(iterable=(),%20/):noindex:) | |  `min`{.interpreted-text role="func"}                         | |  `slice`{.interpreted-text role="func"}                                                                                                                          |
| |  `bool`{.interpreted-text role="func"}                                                                           | |                                                                       | |                                                               | |  `sorted`{.interpreted-text role="func"}                                                                                                                         |
| |  `breakpoint`{.interpreted-text role="func"}                                                                     | |  \*\*G\*\*                                                            | |  \*\*N\*\*                                                    | |  `staticmethod`{.interpreted-text role="func"}                                                                                                                   |
| |  [`bytearray()`](..%20class::%20bytearray(source=b'')bytearray(source,%20encoding,%20errors='strict'):noindex:)  | |  `getattr`{.interpreted-text role="func"}                             | |  `next`{.interpreted-text role="func"}                        | |  [`str()`](..%20class::%20str(*,%20encoding='utf-8',%20errors='strict')str(object)str(object,%20encoding,%20errors='strict')str(object,%20*,%20errors):noindex:) |
| |  [`bytes()`](..%20class::%20bytes(source=b'')bytes(source,%20encoding,%20errors='strict'):noindex:)              | |  `globals`{.interpreted-text role="func"}                             | |                                                               | |  `sum`{.interpreted-text role="func"}                                                                                                                            |
| |                                                                                                                  | |                                                                       | |  \*\*O\*\*                                                    | |  `super`{.interpreted-text role="func"}                                                                                                                          |
| |  \*\*C\*\*                                                                                                       | |  \*\*H\*\*                                                            | |  `object`{.interpreted-text role="func"}                      | |                                                                                                                                                                  |
| |  `callable`{.interpreted-text role="func"}                                                                       | |  `hasattr`{.interpreted-text role="func"}                             | |  `oct`{.interpreted-text role="func"}                         | |  \*\*T\*\*                                                                                                                                                       |
| |  `chr`{.interpreted-text role="func"}                                                                            | |  `hash`{.interpreted-text role="func"}                                | |  `open`{.interpreted-text role="func"}                        | |  [`tuple()`](..%20class::%20tuple(iterable=(),%20/):noindex:)                                                                                                    |
| |  `classmethod`{.interpreted-text role="func"}                                                                    | |  `help`{.interpreted-text role="func"}                                | |  `ord`{.interpreted-text role="func"}                         | |  `type`{.interpreted-text role="func"}                                                                                                                           |
| |  `compile`{.interpreted-text role="func"}                                                                        | |  `hex`{.interpreted-text role="func"}                                 | |                                                               | |                                                                                                                                                                  |
| |  `complex`{.interpreted-text role="func"}                                                                        | |                                                                       | |  \*\*P\*\*                                                    | |  \*\*V\*\*                                                                                                                                                       |
| |                                                                                                                  | |  \*\*I\*\*                                                            | |  `pow`{.interpreted-text role="func"}                         | |  `vars`{.interpreted-text role="func"}                                                                                                                           |
| |  \*\*D\*\*                                                                                                       | |  `id`{.interpreted-text role="func"}                                  | |  `print`{.interpreted-text role="func"}                       | |                                                                                                                                                                  |
| |  `delattr`{.interpreted-text role="func"}                                                                        | |  `input`{.interpreted-text role="func"}                               | |  `property`{.interpreted-text role="func"}                    | |  \*\*Z\*\*                                                                                                                                                       |
| |  [`dict()`](..%20class::%20dict(**kwargs)dict(mapping,%20/,%20**kwargs)dict(iterable,%20/,%20**kwargs):noindex:) | |  `int`{.interpreted-text role="func"}                                 | |                                                               | |  `zip`{.interpreted-text role="func"}                                                                                                                            |
| |  `dir`{.interpreted-text role="func"}                                                                            | |  `isinstance`{.interpreted-text role="func"}                          | |                                                               | |                                                                                                                                                                  |
| |  `divmod`{.interpreted-text role="func"}                                                                         | |  `issubclass`{.interpreted-text role="func"}                          | |                                                               | |  \*\*\_\*\*                                                                                                                                                      |
| |                                                                                                                  | |  `iter`{.interpreted-text role="func"}                                | |                                                               | |  `__import__`{.interpreted-text role="func"}                                                                                                                     |
+--------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+

::: function
abs(number, /)

Return the absolute value of a number. The argument may be an integer, a floating-point number, or an object implementing `~object.__abs__`{.interpreted-text role="meth"}. If the argument is a complex number, its magnitude is returned.
:::

:::: function
aiter(async_iterable, /)

Return an `asynchronous iterator`{.interpreted-text role="term"} for an `asynchronous iterable`{.interpreted-text role="term"}. Equivalent to calling `x.__aiter__()`.

Note: Unlike `iter`{.interpreted-text role="func"}, `aiter`{.interpreted-text role="func"} has no 2-argument variant.

::: versionadded
3.10
:::
::::

::: function
all(iterable, /)

Return `True` if all elements of the *iterable* are true (or if the iterable is empty). Equivalent to:

    def all(iterable):
        for element in iterable:
            if not element:
                return False
        return True
:::

:::: awaitablefunction
anext(async_iterator, /) anext(async_iterator, default, /)

When awaited, return the next item from the given `asynchronous
iterator`{.interpreted-text role="term"}, or *default* if given and the iterator is exhausted.

This is the async variant of the `next`{.interpreted-text role="func"} builtin, and behaves similarly.

This calls the `~object.__anext__`{.interpreted-text role="meth"} method of *async_iterator*, returning an `awaitable`{.interpreted-text role="term"}. Awaiting this returns the next value of the iterator. If *default* is given, it is returned if the iterator is exhausted, otherwise `StopAsyncIteration`{.interpreted-text role="exc"} is raised.

::: versionadded
3.10
:::
::::

::: function
any(iterable, /)

Return `True` if any element of the *iterable* is true. If the iterable is empty, return `False`. Equivalent to:

    def any(iterable):
        for element in iterable:
            if element:
                return True
        return False
:::

::: function
ascii(object, /)

As `repr`{.interpreted-text role="func"}, return a string containing a printable representation of an object, but escape the non-ASCII characters in the string returned by `repr`{.interpreted-text role="func"} using `\x`, `\u`, or `\U` escapes. This generates a string similar to that returned by `repr`{.interpreted-text role="func"} in Python 2.
:::

::: function
bin(integer, /)

Convert an integer number to a binary string prefixed with \"0b\". The result is a valid Python expression. If *integer* is not a Python `int`{.interpreted-text role="class"} object, it has to define an `~object.__index__`{.interpreted-text role="meth"} method that returns an integer. Some examples:

> \>\>\> bin(3) \'0b11\' \>\>\> bin(-10) \'-0b1010\'

If the prefix \"0b\" is desired or not, you can use either of the following ways.

> \>\>\> format(14, \'#b\'), format(14, \'b\') (\'0b1110\', \'1110\') \>\>\> f\'{14:#b}\', f\'{14:b}\' (\'0b1110\', \'1110\')

See also `enum.bin`{.interpreted-text role="func"} to represent negative values as twos-complement.

See also `format`{.interpreted-text role="func"} for more information.
:::

::::: {.bool(object=False, ./)}
Return a Boolean value, i.e. one of `True` or `False`. The argument is converted using the standard `truth testing procedure <truth>`{.interpreted-text role="ref"}. If the argument is false or omitted, this returns `False`; otherwise, it returns `True`. The `bool`{.interpreted-text role="class"} class is a subclass of `int`{.interpreted-text role="class"} (see `typesnumeric`{.interpreted-text role="ref"}). It cannot be subclassed further. Its only instances are `False` and `True` (see `typebool`{.interpreted-text role="ref"}).

::: index
pair: Boolean; type
:::

::: versionchanged
3.7 The parameter is now positional-only.
:::
:::::

::::: function
breakpoint(*args,*\*kws)

This function drops you into the debugger at the call site. Specifically, it calls `sys.breakpointhook`{.interpreted-text role="func"}, passing `args` and `kws` straight through. By default, `sys.breakpointhook()` calls `pdb.set_trace`{.interpreted-text role="func"} expecting no arguments. In this case, it is purely a convenience function so you don\'t have to explicitly import `pdb`{.interpreted-text role="mod"} or type as much code to enter the debugger. However, `sys.breakpointhook`{.interpreted-text role="func"} can be set to some other function and `breakpoint`{.interpreted-text role="func"} will automatically call that, allowing you to drop into the debugger of choice. If `sys.breakpointhook`{.interpreted-text role="func"} is not accessible, this function will raise `RuntimeError`{.interpreted-text role="exc"}.

By default, the behavior of `breakpoint`{.interpreted-text role="func"} can be changed with the `PYTHONBREAKPOINT`{.interpreted-text role="envvar"} environment variable. See `sys.breakpointhook`{.interpreted-text role="func"} for usage details.

Note that this is not guaranteed if `sys.breakpointhook`{.interpreted-text role="func"} has been replaced.

::: audit-event
builtins.breakpoint breakpointhook breakpoint
:::

::: versionadded
3.7
:::
:::::

> Return a new array of bytes. The `bytearray`{.interpreted-text role="class"} class is a mutable sequence of integers in the range 0 \<= x \< 256. It has most of the usual methods of mutable sequences, described in `typesseq-mutable`{.interpreted-text role="ref"}, as well as most methods that the `bytes`{.interpreted-text role="class"} type has, see `bytes-methods`{.interpreted-text role="ref"}.
>
> The optional *source* parameter can be used to initialize the array in a few different ways:
>
> - If it is a *string*, you must also give the *encoding* (and optionally, *errors*) parameters; `bytearray`{.interpreted-text role="func"} then converts the string to bytes using `str.encode`{.interpreted-text role="meth"}.
> - If it is an *integer*, the array will have that size and will be initialized with null bytes.
> - If it is an object conforming to the `buffer interface <bufferobjects>`{.interpreted-text role="ref"}, a read-only buffer of the object will be used to initialize the bytes array.
> - If it is an *iterable*, it must be an iterable of integers in the range `0 <= x < 256`, which are used as the initial contents of the array.
>
> Without an argument, an array of size 0 is created.
>
> See also `binaryseq`{.interpreted-text role="ref"} and `typebytearray`{.interpreted-text role="ref"}.

> Return a new \"bytes\" object which is an immutable sequence of integers in the range `0 <= x < 256`. `bytes`{.interpreted-text role="class"} is an immutable version of `bytearray`{.interpreted-text role="class"} \-- it has the same non-mutating methods and the same indexing and slicing behavior.
>
> Accordingly, constructor arguments are interpreted as for `bytearray`{.interpreted-text role="func"}.
>
> Bytes objects can also be created with literals, see `strings`{.interpreted-text role="ref"}.
>
> See also `binaryseq`{.interpreted-text role="ref"}, `typebytes`{.interpreted-text role="ref"}, and `bytes-methods`{.interpreted-text role="ref"}.

:::: function
callable(object, /)

Return `True`{.interpreted-text role="const"} if the *object* argument appears callable, `False`{.interpreted-text role="const"} if not. If this returns `True`, it is still possible that a call fails, but if it is `False`, calling *object* will never succeed. Note that classes are callable (calling a class returns a new instance); instances are callable if their class has a `~object.__call__`{.interpreted-text role="meth"} method.

::: versionadded
3.2 This function was first removed in Python 3.0 and then brought back in Python 3.2.
:::
::::

::: function
chr(codepoint, /)

Return the string representing a character with the specified Unicode code point. For example, `chr(97)` returns the string `'a'`, while `chr(8364)` returns the string `'€'`. This is the inverse of `ord`{.interpreted-text role="func"}.

The valid range for the argument is from 0 through 1,114,111 (0x10FFFF in base 16). `ValueError`{.interpreted-text role="exc"} will be raised if it is outside that range.
:::

:::::: decorator
classmethod

Transform a method into a class method.

A class method receives the class as an implicit first argument, just like an instance method receives the instance. To declare a class method, use this idiom:

    class C:
        @classmethod
        def f(cls, arg1, arg2): ...

The `@classmethod` form is a function `decorator`{.interpreted-text role="term"} \-- see `function`{.interpreted-text role="ref"} for details.

A class method can be called either on the class (such as `C.f()`) or on an instance (such as `C().f()`). The instance is ignored except for its class. If a class method is called for a derived class, the derived class object is passed as the implied first argument.

Class methods are different than C++ or Java static methods. If you want those, see `staticmethod`{.interpreted-text role="func"} in this section. For more information on class methods, see `types`{.interpreted-text role="ref"}.

::: versionchanged
3.9 Class methods can now wrap other `descriptors <descriptor>`{.interpreted-text role="term"} such as `property`{.interpreted-text role="func"}.
:::

::: versionchanged
3.10 Class methods now inherit the method attributes (`~function.__module__`{.interpreted-text role="attr"}, `~function.__name__`{.interpreted-text role="attr"}, `~function.__qualname__`{.interpreted-text role="attr"}, `~function.__doc__`{.interpreted-text role="attr"} and `~function.__annotations__`{.interpreted-text role="attr"}) and have a new `__wrapped__` attribute.
:::

::: deprecated-removed
3.11 3.13 Class methods can no longer wrap other `descriptors <descriptor>`{.interpreted-text role="term"} such as `property`{.interpreted-text role="func"}.
:::
::::::

:::::::::::: function
compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1, \*, module=None)

Compile the *source* into a code or AST object. Code objects can be executed by `exec`{.interpreted-text role="func"} or `eval`{.interpreted-text role="func"}. *source* can either be a normal string, a byte string, or an AST object. Refer to the `ast`{.interpreted-text role="mod"} module documentation for information on how to work with AST objects.

The *filename* argument should give the file from which the code was read; pass some recognizable value if it wasn\'t read from a file (`'<string>'` is commonly used).

The *mode* argument specifies what kind of code must be compiled; it can be `'exec'` if *source* consists of a sequence of statements, `'eval'` if it consists of a single expression, or `'single'` if it consists of a single interactive statement (in the latter case, expression statements that evaluate to something other than `None` will be printed).

The optional arguments *flags* and *dont_inherit* control which `compiler options <ast-compiler-flags>`{.interpreted-text role="ref"} should be activated and which `future features <future>`{.interpreted-text role="ref"} should be allowed. If neither is present (or both are zero) the code is compiled with the same flags that affect the code that is calling `compile`{.interpreted-text role="func"}. If the *flags* argument is given and *dont_inherit* is not (or is zero) then the compiler options and the future statements specified by the *flags* argument are used in addition to those that would be used anyway. If *dont_inherit* is a non-zero integer then the *flags* argument is it \-- the flags (future features and compiler options) in the surrounding code are ignored.

Compiler options and future statements are specified by bits which can be bitwise ORed together to specify multiple options. The bitfield required to specify a given future feature can be found as the `~__future__._Feature.compiler_flag`{.interpreted-text role="attr"} attribute on the `~__future__._Feature`{.interpreted-text role="class"} instance in the `__future__`{.interpreted-text role="mod"} module. `Compiler flags <ast-compiler-flags>`{.interpreted-text role="ref"} can be found in `ast`{.interpreted-text role="mod"} module, with `PyCF_` prefix.

The argument *optimize* specifies the optimization level of the compiler; the default value of `-1` selects the optimization level of the interpreter as given by `-O`{.interpreted-text role="option"} options. Explicit levels are `0` (no optimization; `__debug__` is true), `1` (asserts are removed, `__debug__` is false) or `2` (docstrings are removed too).

The optional argument *module* specifies the module name. It is needed to unambiguous `filter <warning-filter>`{.interpreted-text role="ref"} syntax warnings by module name.

This function raises `SyntaxError`{.interpreted-text role="exc"} or `ValueError`{.interpreted-text role="exc"} if the compiled source is invalid.

If you want to parse Python code into its AST representation, see `ast.parse`{.interpreted-text role="func"}.

::: audit-event
compile source,filename compile

Raises an `auditing event <auditing>`{.interpreted-text role="ref"} `compile` with arguments `source` and `filename`. This event may also be raised by implicit compilation.
:::

:::: note
::: title
Note
:::

When compiling a string with multi-line code in `'single'` or `'eval'` mode, input must be terminated by at least one newline character. This is to facilitate detection of incomplete and complete statements in the `code`{.interpreted-text role="mod"} module.
::::

:::: warning
::: title
Warning
:::

It is possible to crash the Python interpreter with a sufficiently large/complex string when compiling to an AST object due to stack depth limitations in Python\'s AST compiler.
::::

::: versionchanged
3.2 Allowed use of Windows and Mac newlines. Also, input in `'exec'` mode does not have to end in a newline anymore. Added the *optimize* parameter.
:::

::: versionchanged
3.5 Previously, `TypeError`{.interpreted-text role="exc"} was raised when null bytes were encountered in *source*.
:::

::: versionadded
3.8 `ast.PyCF_ALLOW_TOP_LEVEL_AWAIT` can now be passed in flags to enable support for top-level `await`, `async for`, and `async with`.
:::

::: versionadded
3.15 Added the *module* parameter.
:::
::::::::::::

:::::::: {.complex(number=0, ./) .complex(string, ./) .complex(real=0, .imag=0)}
Convert a single string or number to a complex number, or create a complex number from real and imaginary parts.

Examples:

::: doctest
\>\>\> complex(\'+1.23\') (1.23+0j) \>\>\> complex(\'-4.5j\') -4.5j \>\>\> complex(\'-1.23+4.5j\') (-1.23+4.5j) \>\>\> complex(\'t( -1.23+4.5J )n\') (-1.23+4.5j) \>\>\> complex(\'-Infinity+NaNj\') (-inf+nanj) \>\>\> complex(1.23) (1.23+0j) \>\>\> complex(imag=-4.5) -4.5j \>\>\> complex(-1.23, 4.5) (-1.23+4.5j)
:::

If the argument is a string, it must contain either a real part (in the same format as for `float`{.interpreted-text role="func"}) or an imaginary part (in the same format but with a `'j'` or `'J'` suffix), or both real and imaginary parts (the sign of the imaginary part is mandatory in this case). The string can optionally be surrounded by whitespaces and the round parentheses `'('` and `')'`, which are ignored. The string must not contain whitespace between `'+'`, `'-'`, the `'j'` or `'J'` suffix, and the decimal number. For example, `complex('1+2j')` is fine, but `complex('1 + 2j')` raises `ValueError`{.interpreted-text role="exc"}. More precisely, the input must conform to the `~float:complexvalue`{.interpreted-text role="token"} production rule in the following grammar, after parentheses and leading and trailing whitespace characters are removed:

::: productionlist
float complexvalue: [floatvalue]{.title-ref} \| : [floatvalue]{.title-ref} (\"j\" \| \"J\") \| : [floatvalue]{.title-ref} [sign]{.title-ref} [absfloatvalue]{.title-ref} (\"j\" \| \"J\")
:::

If the argument is a number, the constructor serves as a numeric conversion like `int`{.interpreted-text role="class"} and `float`{.interpreted-text role="class"}. For a general Python object `x`, `complex(x)` delegates to `x.__complex__()`. If `~object.__complex__`{.interpreted-text role="meth"} is not defined then it falls back to `~object.__float__`{.interpreted-text role="meth"}. If `!__float__`{.interpreted-text role="meth"} is not defined then it falls back to `~object.__index__`{.interpreted-text role="meth"}.

If two arguments are provided or keyword arguments are used, each argument may be any numeric type (including complex). If both arguments are real numbers, return a complex number with the real component *real* and the imaginary component *imag*. If both arguments are complex numbers, return a complex number with the real component `real.real-imag.imag` and the imaginary component `real.imag+imag.real`. If one of arguments is a real number, only its real component is used in the above expressions.

See also `complex.from_number`{.interpreted-text role="meth"} which only accepts a single numeric argument.

If all arguments are omitted, returns `0j`.

The complex type is described in `typesnumeric`{.interpreted-text role="ref"}.

::: versionchanged
3.6 Grouping digits with underscores as in code literals is allowed.
:::

::: versionchanged
3.8 Falls back to `~object.__index__`{.interpreted-text role="meth"} if `~object.__complex__`{.interpreted-text role="meth"} and `~object.__float__`{.interpreted-text role="meth"} are not defined.
:::

::: deprecated
3.14 Passing a complex number as the *real* or *imag* argument is now deprecated; it should only be passed as a single positional argument.
:::
::::::::

::: function
delattr(object, name, /)

This is a relative of `setattr`{.interpreted-text role="func"}. The arguments are an object and a string. The string must be the name of one of the object\'s attributes. The function deletes the named attribute, provided the object allows it. For example, `delattr(x, 'foobar')` is equivalent to `del x.foobar`. *name* need not be a Python identifier (see `setattr`{.interpreted-text role="func"}).
:::

> Create a new dictionary. The `dict`{.interpreted-text role="class"} object is the dictionary class. See `dict`{.interpreted-text role="class"} and `typesmapping`{.interpreted-text role="ref"} for documentation about this class.
>
> For other containers see the built-in `list`{.interpreted-text role="class"}, `set`{.interpreted-text role="class"}, and `tuple`{.interpreted-text role="class"} classes, as well as the `collections`{.interpreted-text role="mod"} module.

::::: function
dir() dir(object, /)

Without arguments, return the list of names in the current local scope. With an argument, attempt to return a list of valid attributes for that object.

If the object has a method named `~object.__dir__`{.interpreted-text role="meth"}, this method will be called and must return the list of attributes. This allows objects that implement a custom `~object.__getattr__`{.interpreted-text role="func"} or `~object.__getattribute__`{.interpreted-text role="func"} function to customize the way `dir`{.interpreted-text role="func"} reports their attributes.

If the object does not provide `~object.__dir__`{.interpreted-text role="meth"}, the function tries its best to gather information from the object\'s `~object.__dict__`{.interpreted-text role="attr"} attribute, if defined, and from its type object. The resulting list is not necessarily complete and may be inaccurate when the object has a custom `~object.__getattr__`{.interpreted-text role="func"}.

The default `dir`{.interpreted-text role="func"} mechanism behaves differently with different types of objects, as it attempts to produce the most relevant, rather than complete, information:

- If the object is a module object, the list contains the names of the module\'s attributes.
- If the object is a type or class object, the list contains the names of its attributes, and recursively of the attributes of its bases.
- Otherwise, the list contains the object\'s attributes\' names, the names of its class\'s attributes, and recursively of the attributes of its class\'s base classes.

The resulting list is sorted alphabetically. For example:

> \>\>\> import struct \>\>\> dir() \# show the names in the module namespace \# doctest: +SKIP \[\'\_\_builtins\_\_\', \'\_\_name\_\_\', \'struct\'\] \>\>\> dir(struct) \# show the names in the struct module \# doctest: +SKIP \[\'Struct\', \'\_\_all\_\_\', \'\_\_builtins\_\_\', \'\_\_doc\_\_\', \'\_\_file\_\_\', \'\_\_initializing\_\_\', \'\_\_loader\_\_\', \'\_\_name\_\_\', \'\_\_package\_\_\', \'\_clearcache\', \'calcsize\', \'error\', \'pack\', \'pack_into\', \'unpack\', \'unpack_from\'\] \>\>\> class Shape: \... def \_\_dir\_\_(self): \... return \[\'area\', \'perimeter\', \'location\'\] \... \>\>\> s = Shape() \>\>\> dir(s) \[\'area\', \'location\', \'perimeter\'\]

:::: note
::: title
Note
:::

Because `dir`{.interpreted-text role="func"} is supplied primarily as a convenience for use at an interactive prompt, it tries to supply an interesting set of names more than it tries to supply a rigorously or consistently defined set of names, and its detailed behavior may change across releases. For example, metaclass attributes are not in the result list when the argument is a class.
::::
:::::

::: function
divmod(a, b, /)

Take two (non-complex) numbers as arguments and return a pair of numbers consisting of their quotient and remainder when using integer division. With mixed operand types, the rules for binary arithmetic operators apply. For integers, the result is the same as `(a // b, a % b)`. For floating-point numbers the result is `(q, a % b)`, where *q* is usually `math.floor(a / b)` but may be 1 less than that. In any case `q * b + a % b` is very close to *a*, if `a % b` is non-zero it has the same sign as *b*, and `0 <= abs(a % b) < abs(b)`.
:::

::: function
enumerate(iterable, start=0)

Return an enumerate object. *iterable* must be a sequence, an `iterator`{.interpreted-text role="term"}, or some other object which supports iteration. The `~iterator.__next__`{.interpreted-text role="meth"} method of the iterator returned by `enumerate`{.interpreted-text role="func"} returns a tuple containing a count (from *start* which defaults to 0) and the values obtained from iterating over *iterable*.

> \>\>\> seasons = \[\'Spring\', \'Summer\', \'Fall\', \'Winter\'\] \>\>\> list(enumerate(seasons)) \[(0, \'Spring\'), (1, \'Summer\'), (2, \'Fall\'), (3, \'Winter\')\] \>\>\> list(enumerate(seasons, start=1)) \[(1, \'Spring\'), (2, \'Summer\'), (3, \'Fall\'), (4, \'Winter\')\]

Equivalent to:

    def enumerate(iterable, start=0):
        n = start
        for elem in iterable:
            yield n, elem
            n += 1
:::

::::::::: {#func-eval}
:::::::: function
eval(source, /, globals=None, locals=None)

param source
:   A Python expression.

type source
:   `str`{.interpreted-text role="class"} \| `code object <code-objects>`{.interpreted-text role="ref"}

param globals
:   The global namespace (default: `None`).

type globals
:   `dict`{.interpreted-text role="class"} \| `None`

param locals
:   The local namespace (default: `None`).

type locals
:   `mapping`{.interpreted-text role="term"} \| `None`

returns
:   The result of the evaluated expression.

raises
:   Syntax errors are reported as exceptions.

:::: warning
::: title
Warning
:::

This function executes arbitrary code. Calling it with user-supplied input may lead to security vulnerabilities.
::::

The *source* argument is parsed and evaluated as a Python expression (technically speaking, a condition list) using the *globals* and *locals* mappings as global and local namespace. If the *globals* dictionary is present and does not contain a value for the key `__builtins__`, a reference to the dictionary of the built-in module `builtins`{.interpreted-text role="mod"} is inserted under that key before *source* is parsed. That way you can control what builtins are available to the executed code by inserting your own `__builtins__` dictionary into *globals* before passing it to `eval`{.interpreted-text role="func"}. If the *locals* mapping is omitted it defaults to the *globals* dictionary. If both mappings are omitted, the source is executed with the *globals* and *locals* in the environment where `eval`{.interpreted-text role="func"} is called. Note, *eval()* will only have access to the `nested scopes <nested scope>`{.interpreted-text role="term"} (non-locals) in the enclosing environment if they are already referenced in the scope that is calling `eval`{.interpreted-text role="func"} (e.g. via a `nonlocal`{.interpreted-text role="keyword"} statement).

Example:

> \>\>\> x = 1 \>\>\> eval(\'x+1\') 2

This function can also be used to execute arbitrary code objects (such as those created by `compile`{.interpreted-text role="func"}). In this case, pass a code object instead of a string. If the code object has been compiled with `'exec'` as the *mode* argument, `eval`{.interpreted-text role="func"}\'s return value will be `None`.

Hints: dynamic execution of statements is supported by the `exec`{.interpreted-text role="func"} function. The `globals`{.interpreted-text role="func"} and `locals`{.interpreted-text role="func"} functions return the current global and local dictionary, respectively, which may be useful to pass around for use by `eval`{.interpreted-text role="func"} or `exec`{.interpreted-text role="func"}.

If the given source is a string, then leading and trailing spaces and tabs are stripped.

See `ast.literal_eval`{.interpreted-text role="func"} for a function that can safely evaluate strings with expressions containing only literals.

::: audit-event
exec code_object eval

Raises an `auditing event <auditing>`{.interpreted-text role="ref"} `exec` with the code object as the argument. Code compilation events may also be raised.
:::

::: versionchanged
3.13

The *globals* and *locals* arguments can now be passed as keywords.
:::

::: versionchanged
3.13

The semantics of the default *locals* namespace have been adjusted as described for the `locals`{.interpreted-text role="func"} builtin.
:::
::::::::
:::::::::

::: index
pair: built-in function; exec
:::

::::::::::::::: function
exec(source, /, globals=None, locals=None, \*, closure=None)

:::: warning
::: title
Warning
:::

This function executes arbitrary code. Calling it with user-supplied input may lead to security vulnerabilities.
::::

This function supports dynamic execution of Python code. *source* must be either a string or a code object. If it is a string, the string is parsed as a suite of Python statements which is then executed (unless a syntax error occurs).[^1] If it is a code object, it is simply executed. In all cases, the code that\'s executed is expected to be valid as file input (see the section `file-input`{.interpreted-text role="ref"} in the Reference Manual). Be aware that the `nonlocal`{.interpreted-text role="keyword"}, `yield`{.interpreted-text role="keyword"}, and `return`{.interpreted-text role="keyword"} statements may not be used outside of function definitions even within the context of code passed to the `exec`{.interpreted-text role="func"} function. The return value is `None`.

In all cases, if the optional parts are omitted, the code is executed in the current scope. If only *globals* is provided, it must be a dictionary (and not a subclass of dictionary), which will be used for both the global and the local variables. If *globals* and *locals* are given, they are used for the global and local variables, respectively. If provided, *locals* can be any mapping object. Remember that at the module level, globals and locals are the same dictionary.

:::: note
::: title
Note
:::

When `exec` gets two separate objects as *globals* and *locals*, the code will be executed as if it were embedded in a class definition. This means functions and classes defined in the executed code will not be able to access variables assigned at the top level (as the \"top level\" variables are treated as class variables in a class definition).
::::

If the *globals* dictionary does not contain a value for the key `__builtins__`, a reference to the dictionary of the built-in module `builtins`{.interpreted-text role="mod"} is inserted under that key. That way you can control what builtins are available to the executed code by inserting your own `__builtins__` dictionary into *globals* before passing it to `exec`{.interpreted-text role="func"}.

The *closure* argument specifies a closure\--a tuple of cellvars. It\'s only valid when the *object* is a code object containing `free (closure) variables <closure variable>`{.interpreted-text role="term"}. The length of the tuple must exactly match the length of the code object\'s `~codeobject.co_freevars`{.interpreted-text role="attr"} attribute.

::: audit-event
exec code_object exec

Raises an `auditing event <auditing>`{.interpreted-text role="ref"} `exec` with the code object as the argument. Code compilation events may also be raised.
:::

:::: note
::: title
Note
:::

The built-in functions `globals`{.interpreted-text role="func"} and `locals`{.interpreted-text role="func"} return the current global and local namespace, respectively, which may be useful to pass around for use as the second and third argument to `exec`{.interpreted-text role="func"}.
::::

:::: note
::: title
Note
:::

The default *locals* act as described for function `locals`{.interpreted-text role="func"} below. Pass an explicit *locals* dictionary if you need to see effects of the code on *locals* after function `exec`{.interpreted-text role="func"} returns.
::::

::: versionchanged
3.11 Added the *closure* parameter.
:::

::: versionchanged
3.13

The *globals* and *locals* arguments can now be passed as keywords.
:::

::: versionchanged
3.13

The semantics of the default *locals* namespace have been adjusted as described for the `locals`{.interpreted-text role="func"} builtin.
:::
:::::::::::::::

::: function
filter(function, iterable, /)

Construct an iterator from those elements of *iterable* for which *function* is true. *iterable* may be either a sequence, a container which supports iteration, or an iterator. If *function* is `None`, the identity function is assumed, that is, all elements of *iterable* that are false are removed.

Note that `filter(function, iterable)` is equivalent to the generator expression `(item for item in iterable if function(item))` if function is not `None` and `(item for item in iterable if item)` if function is `None`.

See `itertools.filterfalse`{.interpreted-text role="func"} for the complementary function that returns elements of *iterable* for which *function* is false.
:::

::::::::: {.float(number=0.0, ./) .float(string, ./)}
::: index
single: NaN single: Infinity
:::

Return a floating-point number constructed from a number or a string.

Examples:

::: doctest
\>\>\> float(\'+1.23\') 1.23 \>\>\> float(\' -12345n\') -12345.0 \>\>\> float(\'1e-003\') 0.001 \>\>\> float(\'+1E6\') 1000000.0 \>\>\> float(\'-Infinity\') -inf
:::

If the argument is a string, it should contain a decimal number, optionally preceded by a sign, and optionally embedded in whitespace. The optional sign may be `'+'` or `'-'`; a `'+'` sign has no effect on the value produced. The argument may also be a string representing a NaN (not-a-number), or positive or negative infinity. More precisely, the input must conform to the `~float:floatvalue`{.interpreted-text role="token"} production rule in the following grammar, after leading and trailing whitespace characters are removed:

::: productionlist
float sign: \"+\" \| \"-\" infinity: \"Infinity\" \| \"inf\" nan: \"nan\" digit: \<a Unicode decimal digit, i.e. characters in Unicode general category Nd\> digitpart: [digit]{.title-ref} (\[\"\_\"\] [digit]{.title-ref})\* number: \[[digitpart]{.title-ref}\] \".\" [digitpart]{.title-ref} \| [digitpart]{.title-ref} \[\".\"\] exponent: (\"e\" \| \"E\") \[[sign]{.title-ref}\] [digitpart]{.title-ref} floatnumber: [number]{.title-ref} \[[exponent]{.title-ref}\] absfloatvalue: [floatnumber]{.title-ref} \| [infinity]{.title-ref} \| [nan]{.title-ref} floatvalue: \[[sign]{.title-ref}\] [absfloatvalue]{.title-ref}
:::

Case is not significant, so, for example, \"inf\", \"Inf\", \"INFINITY\", and \"iNfINity\" are all acceptable spellings for positive infinity.

Otherwise, if the argument is an integer or a floating-point number, a floating-point number with the same value (within Python\'s floating-point precision) is returned. If the argument is outside the range of a Python float, an `OverflowError`{.interpreted-text role="exc"} will be raised.

For a general Python object `x`, `float(x)` delegates to `x.__float__()`. If `~object.__float__`{.interpreted-text role="meth"} is not defined then it falls back to `~object.__index__`{.interpreted-text role="meth"}.

See also `float.from_number`{.interpreted-text role="meth"} which only accepts a numeric argument.

If no argument is given, `0.0` is returned.

The float type is described in `typesnumeric`{.interpreted-text role="ref"}.

::: versionchanged
3.6 Grouping digits with underscores as in code literals is allowed.
:::

::: versionchanged
3.7 The parameter is now positional-only.
:::

::: versionchanged
3.8 Falls back to `~object.__index__`{.interpreted-text role="meth"} if `~object.__float__`{.interpreted-text role="meth"} is not defined.
:::
:::::::::

::: index
single: \_\_format\_\_ single: string; format() (built-in function)
:::

:::: function
format(value, format_spec=\"\", /)

Convert a *value* to a \"formatted\" representation, as controlled by *format_spec*. The interpretation of *format_spec* will depend on the type of the *value* argument; however, there is a standard formatting syntax that is used by most built-in types: `formatspec`{.interpreted-text role="ref"}.

The default *format_spec* is an empty string which usually gives the same effect as calling `str(value) <str>`{.interpreted-text role="func"}.

A call to `format(value, format_spec)` is translated to `type(value).__format__(value, format_spec)` which bypasses the instance dictionary when searching for the value\'s `~object.__format__`{.interpreted-text role="meth"} method. A `TypeError`{.interpreted-text role="exc"} exception is raised if the method search reaches `object`{.interpreted-text role="mod"} and the *format_spec* is non-empty, or if either the *format_spec* or the return value are not strings.

::: versionchanged
3.4 `object().__format__(format_spec)` raises `TypeError`{.interpreted-text role="exc"} if *format_spec* is not an empty string.
:::
::::

> Return a new `frozenset`{.interpreted-text role="class"} object, optionally with elements taken from *iterable*. `frozenset` is a built-in class. See `frozenset`{.interpreted-text role="class"} and `types-set`{.interpreted-text role="ref"} for documentation about this class.
>
> For other containers see the built-in `set`{.interpreted-text role="class"}, `list`{.interpreted-text role="class"}, `tuple`{.interpreted-text role="class"}, and `dict`{.interpreted-text role="class"} classes, as well as the `collections`{.interpreted-text role="mod"} module.

::::: function
getattr(object, name, /) getattr(object, name, default, /)

Return the value of the named attribute of *object*. *name* must be a string. If the string is the name of one of the object\'s attributes, the result is the value of that attribute. For example, `getattr(x, 'foobar')` is equivalent to `x.foobar`. If the named attribute does not exist, *default* is returned if provided, otherwise `AttributeError`{.interpreted-text role="exc"} is raised. *name* need not be a Python identifier (see `setattr`{.interpreted-text role="func"}).

:::: note
::: title
Note
:::

Since `private name mangling <private-name-mangling>`{.interpreted-text role="ref"} happens at compilation time, one must manually mangle a private attribute\'s (attributes with two leading underscores) name in order to retrieve it with `getattr`{.interpreted-text role="func"}.
::::
:::::

::: function
globals()

Return the dictionary implementing the current module namespace. For code within functions, this is set when the function is defined and remains the same regardless of where the function is called.
:::

::: function
hasattr(object, name, /)

The arguments are an object and a string. The result is `True` if the string is the name of one of the object\'s attributes, `False` if not. (This is implemented by calling `getattr(object, name)` and seeing whether it raises an `AttributeError`{.interpreted-text role="exc"} or not.)
:::

::::: function
hash(object, /)

Return the hash value of the object (if it has one). Hash values are integers. They are used to quickly compare dictionary keys during a dictionary lookup. Numeric values that compare equal have the same hash value (even if they are of different types, as is the case for 1 and 1.0).

:::: note
::: title
Note
:::

For objects with custom `~object.__hash__`{.interpreted-text role="meth"} methods, note that `hash`{.interpreted-text role="func"} truncates the return value based on the bit width of the host machine.
::::
:::::

:::: function
help() help(request)

Invoke the built-in help system. (This function is intended for interactive use.) If no argument is given, the interactive help system starts on the interpreter console. If the argument is a string, then the string is looked up as the name of a module, function, class, method, keyword, or documentation topic, and a help page is printed on the console. If the argument is any other kind of object, a help page on the object is generated.

Note that if a slash(/) appears in the parameter list of a function when invoking `help`{.interpreted-text role="func"}, it means that the parameters prior to the slash are positional-only. For more info, see `the FAQ entry on positional-only parameters <faq-positional-only-arguments>`{.interpreted-text role="ref"}.

This function is added to the built-in namespace by the `site`{.interpreted-text role="mod"} module.

::: versionchanged
3.4 Changes to `pydoc`{.interpreted-text role="mod"} and `inspect`{.interpreted-text role="mod"} mean that the reported signatures for callables are now more comprehensive and consistent.
:::
::::

::::: function
hex(integer, /)

Convert an integer number to a lowercase hexadecimal string prefixed with \"0x\". If *integer* is not a Python `int`{.interpreted-text role="class"} object, it has to define an `~object.__index__`{.interpreted-text role="meth"} method that returns an integer. Some examples:

> \>\>\> hex(255) \'0xff\' \>\>\> hex(-42) \'-0x2a\'

If you want to convert an integer number to an uppercase or lower hexadecimal string with prefix or not, you can use either of the following ways:

> \>\>\> \'%#x\' % 255, \'%x\' % 255, \'%X\' % 255 (\'0xff\', \'ff\', \'FF\') \>\>\> format(255, \'#x\'), format(255, \'x\'), format(255, \'X\') (\'0xff\', \'ff\', \'FF\') \>\>\> f\'{255:#x}\', f\'{255:x}\', f\'{255:X}\' (\'0xff\', \'ff\', \'FF\')

See also `format`{.interpreted-text role="func"} for more information.

See also `int`{.interpreted-text role="func"} for converting a hexadecimal string to an integer using a base of 16.

:::: note
::: title
Note
:::

To obtain a hexadecimal string representation for a float, use the `float.hex`{.interpreted-text role="meth"} method.
::::
:::::

::::: function
id(object, /)

Return the \"identity\" of an object. This is an integer which is guaranteed to be unique and constant for this object during its lifetime. Two objects with non-overlapping lifetimes may have the same `id`{.interpreted-text role="func"} value.

::: impl-detail
This is the address of the object in memory.
:::

::: audit-event
builtins.id id id
:::
:::::

::::: function
input() input(prompt, /)

If the *prompt* argument is present, it is written to standard output without a trailing newline. The function then reads a line from input, converts it to a string (stripping a trailing newline), and returns that. When EOF is read, `EOFError`{.interpreted-text role="exc"} is raised. Example:

    >>> s = input('--> ')  # doctest: +SKIP
    --> Monty Python's Flying Circus
    >>> s  # doctest: +SKIP
    "Monty Python's Flying Circus"

If the `readline`{.interpreted-text role="mod"} module was loaded, then `input`{.interpreted-text role="func"} will use it to provide elaborate line editing and history features.

::: audit-event
builtins.input prompt input

Raises an `auditing event <auditing>`{.interpreted-text role="ref"} `builtins.input` with argument `prompt` before reading input
:::

::: audit-event
builtins.input/result result input

Raises an `auditing event <auditing>`{.interpreted-text role="ref"} `builtins.input/result` with the result after successfully reading input.
:::
:::::

:::::::::: {.int(number=0, ./) .int(string, ./, .base=10)}
Return an integer object constructed from a number or a string, or return `0` if no arguments are given.

Examples:

::: doctest
\>\>\> int(123.45) 123 \>\>\> int(\'123\') 123 \>\>\> int(\' -12_345n\') -12345 \>\>\> int(\'FACE\', 16) 64206 \>\>\> int(\'0xface\', 0) 64206 \>\>\> int(\'01110011\', base=2) 115
:::

If the argument defines `~object.__int__`{.interpreted-text role="meth"}, `int(x)` returns `x.__int__()`. If the argument defines `~object.__index__`{.interpreted-text role="meth"}, it returns `x.__index__()`. For floating-point numbers, this truncates towards zero.

If the argument is not a number or if *base* is given, then it must be a string, `bytes`{.interpreted-text role="class"}, or `bytearray`{.interpreted-text role="class"} instance representing an integer in radix *base*. Optionally, the string can be preceded by `+` or `-` (with no space in between), have leading zeros, be surrounded by whitespace, and have single underscores interspersed between digits.

A base-n integer string contains digits, each representing a value from 0 to n-1. The values 0\--9 can be represented by any Unicode decimal digit. The values 10\--35 can be represented by `a` to `z` (or `A` to `Z`). The default *base* is 10. The allowed bases are 0 and 2\--36. Base-2, -8, and -16 strings can be optionally prefixed with `0b`/`0B`, `0o`/`0O`, or `0x`/`0X`, as with integer literals in code. For base 0, the string is interpreted in a similar way to an `integer literal in code <integers>`{.interpreted-text role="ref"}, in that the actual base is 2, 8, 10, or 16 as determined by the prefix. Base 0 also disallows leading zeros: `int('010', 0)` is not legal, while `int('010')` and `int('010', 8)` are.

The integer type is described in `typesnumeric`{.interpreted-text role="ref"}.

::: versionchanged
3.4 If *base* is not an instance of `int`{.interpreted-text role="class"} and the *base* object has a `base.__index__ <object.__index__>`{.interpreted-text role="meth"} method, that method is called to obtain an integer for the base. Previous versions used `base.__int__ <object.__int__>`{.interpreted-text role="meth"} instead of `base.__index__
<object.__index__>`{.interpreted-text role="meth"}.
:::

::: versionchanged
3.6 Grouping digits with underscores as in code literals is allowed.
:::

::: versionchanged
3.7 The first parameter is now positional-only.
:::

::: versionchanged
3.8 Falls back to `~object.__index__`{.interpreted-text role="meth"} if `~object.__int__`{.interpreted-text role="meth"} is not defined.
:::

::: versionchanged
3.11 `int`{.interpreted-text role="class"} string inputs and string representations can be limited to help avoid denial of service attacks. A `ValueError`{.interpreted-text role="exc"} is raised when the limit is exceeded while converting a string to an `int`{.interpreted-text role="class"} or when converting an `int`{.interpreted-text role="class"} into a string would exceed the limit. See the `integer string conversion length limitation
<int_max_str_digits>`{.interpreted-text role="ref"} documentation.
:::

::: versionchanged
3.14 `int`{.interpreted-text role="func"} no longer delegates to the `~object.__trunc__`{.interpreted-text role="meth"} method.
:::
::::::::::

:::: function
isinstance(object, classinfo, /)

Return `True` if the *object* argument is an instance of the *classinfo* argument, or of a (direct, indirect, or `virtual <abstract base
class>`{.interpreted-text role="term"}) subclass thereof. If *object* is not an object of the given type, the function always returns `False`. If *classinfo* is a tuple of type objects (or recursively, other such tuples) or a `types-union`{.interpreted-text role="ref"} of multiple types, return `True` if *object* is an instance of any of the types. If *classinfo* is not a type or tuple of types and such tuples, a `TypeError`{.interpreted-text role="exc"} exception is raised. `TypeError`{.interpreted-text role="exc"} may not be raised for an invalid type if an earlier check succeeds.

::: versionchanged
3.10 *classinfo* can be a `types-union`{.interpreted-text role="ref"}.
:::
::::

:::: function
issubclass(class, classinfo, /)

Return `True` if *class* is a subclass (direct, indirect, or `virtual
<abstract base class>`{.interpreted-text role="term"}) of *classinfo*. A class is considered a subclass of itself. *classinfo* may be a tuple of class objects (or recursively, other such tuples) or a `types-union`{.interpreted-text role="ref"}, in which case return `True` if *class* is a subclass of any entry in *classinfo*. In any other case, a `TypeError`{.interpreted-text role="exc"} exception is raised.

::: versionchanged
3.10 *classinfo* can be a `types-union`{.interpreted-text role="ref"}.
:::
::::

::: function
iter(iterable, /) iter(callable, sentinel, /)

Return an `iterator`{.interpreted-text role="term"} object. The first argument is interpreted very differently depending on the presence of the second argument. Without a second argument, the single argument must be a collection object which supports the `iterable`{.interpreted-text role="term"} protocol (the `~object.__iter__`{.interpreted-text role="meth"} method), or it must support the sequence protocol (the `~object.__getitem__`{.interpreted-text role="meth"} method with integer arguments starting at `0`). If it does not support either of those protocols, `TypeError`{.interpreted-text role="exc"} is raised. If the second argument, *sentinel*, is given, then the first argument must be a callable object. The iterator created in this case will call *callable* with no arguments for each call to its `~iterator.__next__`{.interpreted-text role="meth"} method; if the value returned is equal to *sentinel*, `StopIteration`{.interpreted-text role="exc"} will be raised, otherwise the value will be returned.

See also `typeiter`{.interpreted-text role="ref"}.

One useful application of the second form of `iter`{.interpreted-text role="func"} is to build a block-reader. For example, reading fixed-width blocks from a binary database file until the end of file is reached:

    from functools import partial
    with open('mydata.db', 'rb') as f:
        for block in iter(partial(f.read, 64), b''):
            process_block(block)
:::

:::: function
len(object, /)

Return the length (the number of items) of an object. The argument may be a sequence (such as a string, bytes, tuple, list, or range) or a collection (such as a dictionary, set, or frozen set).

::: impl-detail
`len` raises `OverflowError`{.interpreted-text role="exc"} on lengths larger than `sys.maxsize`{.interpreted-text role="data"}, such as `range(2 ** 100) <range>`{.interpreted-text role="class"}.
:::
::::

> Rather than being a function, `list`{.interpreted-text role="class"} is actually a mutable sequence type, as documented in `typesseq-list`{.interpreted-text role="ref"} and `typesseq`{.interpreted-text role="ref"}.

::::: function
locals()

Return a mapping object representing the current local symbol table, with variable names as the keys, and their currently bound references as the values.

At module scope, as well as when using `exec`{.interpreted-text role="func"} or `eval`{.interpreted-text role="func"} with a single namespace, this function returns the same namespace as `globals`{.interpreted-text role="func"}.

At class scope, it returns the namespace that will be passed to the metaclass constructor.

When using `exec()` or `eval()` with separate local and global arguments, it returns the local namespace passed in to the function call.

In all of the above cases, each call to `locals()` in a given frame of execution will return the *same* mapping object. Changes made through the mapping object returned from `locals()` will be visible as assigned, reassigned, or deleted local variables, and assigning, reassigning, or deleting local variables will immediately affect the contents of the returned mapping object.

In an `optimized scope`{.interpreted-text role="term"} (including functions, generators, and coroutines), each call to `locals()` instead returns a fresh dictionary containing the current bindings of the function\'s local variables and any nonlocal cell references. In this case, name binding changes made via the returned dict are *not* written back to the corresponding local variables or nonlocal cell references, and assigning, reassigning, or deleting local variables and nonlocal cell references does *not* affect the contents of previously returned dictionaries.

Calling `locals()` as part of a comprehension in a function, generator, or coroutine is equivalent to calling it in the containing scope, except that the comprehension\'s initialised iteration variables will be included. In other scopes, it behaves as if the comprehension were running as a nested function.

Calling `locals()` as part of a generator expression is equivalent to calling it in a nested generator function.

::: versionchanged
3.12 The behaviour of `locals()` in a comprehension has been updated as described in `709`{.interpreted-text role="pep"}.
:::

::: versionchanged
3.13 As part of `667`{.interpreted-text role="pep"}, the semantics of mutating the mapping objects returned from this function are now defined. The behavior in `optimized scopes <optimized scope>`{.interpreted-text role="term"} is now as described above. Aside from being defined, the behaviour in other scopes remains unchanged from previous versions.
:::
:::::

:::: function
map(function, iterable, /, \*iterables, strict=False)

Return an iterator that applies *function* to every item of *iterable*, yielding the results. If additional *iterables* arguments are passed, *function* must take that many arguments and is applied to the items from all iterables in parallel. With multiple iterables, the iterator stops when the shortest iterable is exhausted. If *strict* is `True` and one of the iterables is exhausted before the others, a `ValueError`{.interpreted-text role="exc"} is raised. For cases where the function inputs are already arranged into argument tuples, see `itertools.starmap`{.interpreted-text role="func"}.

::: versionchanged
3.14 Added the *strict* parameter.
:::
::::

::::: function
max(iterable, /, *, key=None) max(iterable, /,*, default, key=None) max(arg1, arg2, /, \*args, key=None)

Return the largest item in an iterable or the largest of two or more arguments.

If one positional argument is provided, it should be an `iterable`{.interpreted-text role="term"}. The largest item in the iterable is returned. If two or more positional arguments are provided, the largest of the positional arguments is returned.

There are two optional keyword-only arguments. The *key* argument specifies a one-argument ordering function like that used for `list.sort`{.interpreted-text role="meth"}. The *default* argument specifies an object to return if the provided iterable is empty. If the iterable is empty and *default* is not provided, a `ValueError`{.interpreted-text role="exc"} is raised.

If multiple items are maximal, the function returns the first one encountered. This is consistent with other sort-stability preserving tools such as `sorted(iterable, key=keyfunc, reverse=True)[0]` and `heapq.nlargest(1, iterable, key=keyfunc)`.

::: versionchanged
3.4 Added the *default* keyword-only parameter.
:::

::: versionchanged
3.8 The *key* can be `None`.
:::
:::::

> Return a \"memory view\" object created from the given argument. See `typememoryview`{.interpreted-text role="ref"} for more information.

::::: function
min(iterable, /, *, key=None) min(iterable, /,*, default, key=None) min(arg1, arg2, /, \*args, key=None)

Return the smallest item in an iterable or the smallest of two or more arguments.

If one positional argument is provided, it should be an `iterable`{.interpreted-text role="term"}. The smallest item in the iterable is returned. If two or more positional arguments are provided, the smallest of the positional arguments is returned.

There are two optional keyword-only arguments. The *key* argument specifies a one-argument ordering function like that used for `list.sort`{.interpreted-text role="meth"}. The *default* argument specifies an object to return if the provided iterable is empty. If the iterable is empty and *default* is not provided, a `ValueError`{.interpreted-text role="exc"} is raised.

If multiple items are minimal, the function returns the first one encountered. This is consistent with other sort-stability preserving tools such as `sorted(iterable, key=keyfunc)[0]` and `heapq.nsmallest(1, iterable, key=keyfunc)`.

::: versionchanged
3.4 Added the *default* keyword-only parameter.
:::

::: versionchanged
3.8 The *key* can be `None`.
:::
:::::

::: function
next(iterator, /) next(iterator, default, /)

Retrieve the next item from the `iterator`{.interpreted-text role="term"} by calling its `~iterator.__next__`{.interpreted-text role="meth"} method. If *default* is given, it is returned if the iterator is exhausted, otherwise `StopIteration`{.interpreted-text role="exc"} is raised.
:::

::::: object()
This is the ultimate base class of all other classes. It has methods that are common to all instances of Python classes. When the constructor is called, it returns a new featureless object. The constructor does not accept any arguments.

:::: note
::: title
Note
:::

`object`{.interpreted-text role="class"} instances do *not* have `~object.__dict__`{.interpreted-text role="attr"} attributes, so you can\'t assign arbitrary attributes to an instance of `object`{.interpreted-text role="class"}.
::::
:::::

::: function
oct(integer, /)

Convert an integer number to an octal string prefixed with \"0o\". The result is a valid Python expression. If *integer* is not a Python `int`{.interpreted-text role="class"} object, it has to define an `~object.__index__`{.interpreted-text role="meth"} method that returns an integer. For example:

> \>\>\> oct(8) \'0o10\' \>\>\> oct(-56) \'-0o70\'

If you want to convert an integer number to an octal string either with the prefix \"0o\" or not, you can use either of the following ways.

> \>\>\> \'%#o\' % 10, \'%o\' % 10 (\'0o12\', \'12\') \>\>\> format(10, \'#o\'), format(10, \'o\') (\'0o12\', \'12\') \>\>\> f\'{10:#o}\', f\'{10:o}\' (\'0o12\', \'12\')

See also `format`{.interpreted-text role="func"} for more information.
:::

::: index
single: file object; open() built-in function
:::

:::::::::::::::: function
open(file, mode=\'r\', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)

Open *file* and return a corresponding `file object`{.interpreted-text role="term"}. If the file cannot be opened, an `OSError`{.interpreted-text role="exc"} is raised. See `tut-files`{.interpreted-text role="ref"} for more examples of how to use this function.

*file* is a `path-like object`{.interpreted-text role="term"} giving the pathname (absolute or relative to the current working directory) of the file to be opened or an integer file descriptor of the file to be wrapped. (If a file descriptor is given, it is closed when the returned I/O object is closed unless *closefd* is set to `False`.)

*mode* is an optional string that specifies the mode in which the file is opened. It defaults to `'r'` which means open for reading in text mode. Other common values are `'w'` for writing (truncating the file if it already exists), `'x'` for exclusive creation, and `'a'` for appending (which on *some* Unix systems, means that *all* writes append to the end of the file regardless of the current seek position). In text mode, if *encoding* is not specified the encoding used is platform-dependent: `locale.getencoding`{.interpreted-text role="func"} is called to get the current locale encoding. (For reading and writing raw bytes use binary mode and leave *encoding* unspecified.) The available modes are:

:::: {#filemodes}
::: index
pair: file; modes
:::
::::

  Character   Meaning
  ----------- -----------------------------------------------------------------
  `'r'`       open for reading (default)
  `'w'`       open for writing, truncating the file first
  `'x'`       open for exclusive creation, failing if the file already exists
  `'a'`       open for writing, appending to the end of file if it exists
  `'b'`       binary mode
  `'t'`       text mode (default)
  `'+'`       open for updating (reading and writing)

The default mode is `'r'` (open for reading text, a synonym of `'rt'`). Modes `'w+'` and `'w+b'` open and truncate the file. Modes `'r+'` and `'r+b'` open the file with no truncation.

As mentioned in the `io-overview`{.interpreted-text role="ref"}, Python distinguishes between binary and text I/O. Files opened in binary mode (including `'b'` in the *mode* argument) return contents as `bytes`{.interpreted-text role="class"} objects without any decoding. In text mode (the default, or when `'t'` is included in the *mode* argument), the contents of the file are returned as `str`{.interpreted-text role="class"}, the bytes having been first decoded using a platform-dependent encoding or using the specified *encoding* if given.

:::: note
::: title
Note
:::

Python doesn\'t depend on the underlying operating system\'s notion of text files; all the processing is done by Python itself, and is therefore platform-independent.
::::

*buffering* is an optional integer used to set the buffering policy. Pass 0 to switch buffering off (only allowed in binary mode), 1 to select line buffering (only usable when writing in text mode), and an integer \> 1 to indicate the size in bytes of a fixed-size chunk buffer. Note that specifying a buffer size this way applies for binary buffered I/O, but `TextIOWrapper` (i.e., files opened with `mode='r+'`) would have another buffering. To disable buffering in `TextIOWrapper`, consider using the `write_through` flag for `io.TextIOWrapper.reconfigure`{.interpreted-text role="func"}. When no *buffering* argument is given, the default buffering policy works as follows:

- Binary files are buffered in fixed-size chunks; the size of the buffer is `max(min(blocksize, 8 MiB), DEFAULT_BUFFER_SIZE)` when the device block size is available. On most systems, the buffer will typically be 128 kilobytes long.
- \"Interactive\" text files (files for which `~io.IOBase.isatty`{.interpreted-text role="meth"} returns `True`) use line buffering. Other text files use the policy described above for binary files.

*encoding* is the name of the encoding used to decode or encode the file. This should only be used in text mode. The default encoding is platform dependent (whatever `locale.getencoding`{.interpreted-text role="func"} returns), but any `text encoding`{.interpreted-text role="term"} supported by Python can be used. See the `codecs`{.interpreted-text role="mod"} module for the list of supported encodings.

*errors* is an optional string that specifies how encoding and decoding errors are to be handled---this cannot be used in binary mode. A variety of standard error handlers are available, though any error handling name that has been registered with `codecs.register_error`{.interpreted-text role="func"} is also valid. The standard names can be found in `error-handlers`{.interpreted-text role="ref"}.

::: index
single: universal newlines; open() built-in function
:::

::: {#open-newline-parameter}
*newline* determines how to parse newline characters from the stream. It can be `None`, `''`, `'\n'`, `'\r'`, and `'\r\n'`. It works as follows:
:::

- When reading input from the stream, if *newline* is `None`, universal newlines mode is enabled. Lines in the input can end in `'\n'`, `'\r'`, or `'\r\n'`, and these are translated into `'\n'` before being returned to the caller. If it is `''`, universal newlines mode is enabled, but line endings are returned to the caller untranslated. If it has any of the other legal values, input lines are only terminated by the given string, and the line ending is returned to the caller untranslated.
- When writing output to the stream, if *newline* is `None`, any `'\n'` characters written are translated to the system default line separator, `os.linesep`{.interpreted-text role="data"}. If *newline* is `''` or `'\n'`, no translation takes place. If *newline* is any of the other legal values, any `'\n'` characters written are translated to the given string.

If *closefd* is `False` and a file descriptor rather than a filename was given, the underlying file descriptor will be kept open when the file is closed. If a filename is given *closefd* must be `True` (the default); otherwise, an error will be raised.

A custom opener can be used by passing a callable as *opener*. The underlying file descriptor for the file object is then obtained by calling *opener* with (*file*, *flags*). *opener* must return an open file descriptor (passing `os.open`{.interpreted-text role="mod"} as *opener* results in functionality similar to passing `None`).

The newly created file is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

The following example uses the `dir_fd <dir_fd>`{.interpreted-text role="ref"} parameter of the `os.open`{.interpreted-text role="func"} function to open a file relative to a given directory:

    >>> import os
    >>> dir_fd = os.open('somedir', os.O_RDONLY)
    >>> def opener(path, flags):
    ...     return os.open(path, flags, dir_fd=dir_fd)
    ...
    >>> with open('spamspam.txt', 'w', opener=opener) as f:
    ...     print('This will be written to somedir/spamspam.txt', file=f)
    ...
    >>> os.close(dir_fd)  # don't leak a file descriptor

The type of `file object`{.interpreted-text role="term"} returned by the `open`{.interpreted-text role="func"} function depends on the mode. When `open`{.interpreted-text role="func"} is used to open a file in a text mode (`'w'`, `'r'`, `'wt'`, `'rt'`, etc.), it returns a subclass of `io.TextIOBase`{.interpreted-text role="class"} (specifically `io.TextIOWrapper`{.interpreted-text role="class"}). When used to open a file in a binary mode with buffering, the returned class is a subclass of `io.BufferedIOBase`{.interpreted-text role="class"}. The exact class varies: in read binary mode, it returns an `io.BufferedReader`{.interpreted-text role="class"}; in write binary and append binary modes, it returns an `io.BufferedWriter`{.interpreted-text role="class"}, and in read/write mode, it returns an `io.BufferedRandom`{.interpreted-text role="class"}. When buffering is disabled, the raw stream, a subclass of `io.RawIOBase`{.interpreted-text role="class"}, `io.FileIO`{.interpreted-text role="class"}, is returned.

::: index
single: line-buffered I/O single: unbuffered I/O single: buffer size, I/O single: I/O control; buffering single: binary mode single: text mode pair: module; sys
:::

See also the file handling modules, such as `fileinput`{.interpreted-text role="mod"}, `io`{.interpreted-text role="mod"} (where `open`{.interpreted-text role="func"} is declared), `os`{.interpreted-text role="mod"}, `os.path`{.interpreted-text role="mod"}, `tempfile`{.interpreted-text role="mod"}, and `shutil`{.interpreted-text role="mod"}.

::: audit-event
open path,mode,flags open
:::

The `mode` and `flags` arguments may have been modified or inferred from the original call.

::: versionchanged
3.3

- The *opener* parameter was added.
- The `'x'` mode was added.
- `IOError`{.interpreted-text role="exc"} used to be raised, it is now an alias of `OSError`{.interpreted-text role="exc"}.
- `FileExistsError`{.interpreted-text role="exc"} is now raised if the file opened in exclusive creation mode (`'x'`) already exists.
:::

::: versionchanged
3.4

- The file is now non-inheritable.
:::

::: versionchanged
3.5

- If the system call is interrupted and the signal handler does not raise an exception, the function now retries the system call instead of raising an `InterruptedError`{.interpreted-text role="exc"} exception (see `475`{.interpreted-text role="pep"} for the rationale).
- The `'namereplace'` error handler was added.
:::

::: versionchanged
3.6

- Support added to accept objects implementing `os.PathLike`{.interpreted-text role="class"}.
- On Windows, opening a console buffer may return a subclass of `io.RawIOBase`{.interpreted-text role="class"} other than `io.FileIO`{.interpreted-text role="class"}.
:::

::: versionchanged
3.11 The `'U'` mode has been removed.
:::
::::::::::::::::

::: function
ord(character, /)

Return the ordinal value of a character.

If the argument is a one-character string, return the Unicode code point of that character. For example, `ord('a')` returns the integer `97` and `ord('€')` (Euro sign) returns `8364`. This is the inverse of `chr`{.interpreted-text role="func"}.

If the argument is a `bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"} object of length 1, return its single byte value. For example, `ord(b'a')` returns the integer `97`.
:::

::::: function
pow(base, exp, mod=None)

Return *base* to the power *exp*; if *mod* is present, return *base* to the power *exp*, modulo *mod* (computed more efficiently than `pow(base, exp) % mod`). The two-argument form `pow(base, exp)` is equivalent to using the power operator: `base**exp`.

When arguments are builtin numeric types with mixed operand types, the coercion rules for binary arithmetic operators apply. For `int`{.interpreted-text role="class"} operands, the result has the same type as the operands (after coercion) unless the second argument is negative; in that case, all arguments are converted to float and a float result is delivered. For example, `pow(10, 2)` returns `100`, but `pow(10, -2)` returns `0.01`. For a negative base of type `int`{.interpreted-text role="class"} or `float`{.interpreted-text role="class"} and a non-integral exponent, a complex result is delivered. For example, `pow(-9, 0.5)` returns a value close to `3j`. Whereas, for a negative base of type `int`{.interpreted-text role="class"} or `float`{.interpreted-text role="class"} with an integral exponent, a float result is delivered. For example, `pow(-9, 2.0)` returns `81.0`.

For `int`{.interpreted-text role="class"} operands *base* and *exp*, if *mod* is present, *mod* must also be of integer type and *mod* must be nonzero. If *mod* is present and *exp* is negative, *base* must be relatively prime to *mod*. In that case, `pow(inv_base, -exp, mod)` is returned, where *inv_base* is an inverse to *base* modulo *mod*.

Here\'s an example of computing an inverse for `38` modulo `97`:

    >>> pow(38, -1, mod=97)
    23
    >>> 23 * 38 % 97 == 1
    True

::: versionchanged
3.8 For `int`{.interpreted-text role="class"} operands, the three-argument form of `pow` now allows the second argument to be negative, permitting computation of modular inverses.
:::

::: versionchanged
3.8 Allow keyword arguments. Formerly, only positional arguments were supported.
:::
:::::

:::: function
print(\*objects, sep=\' \', end=\'n\', file=None, flush=False)

Print *objects* to the text stream *file*, separated by *sep* and followed by *end*. *sep*, *end*, *file*, and *flush*, if present, must be given as keyword arguments.

All non-keyword arguments are converted to strings like `str`{.interpreted-text role="func"} does and written to the stream, separated by *sep* and followed by *end*. Both *sep* and *end* must be strings; they can also be `None`, which means to use the default values. If no *objects* are given, `print`{.interpreted-text role="func"} will just write *end*.

The *file* argument must be an object with a `write(string)` method; if it is not present or `None`, `sys.stdout`{.interpreted-text role="data"} will be used. Since printed arguments are converted to text strings, `print`{.interpreted-text role="func"} cannot be used with binary mode file objects. For these, use `file.write(...)` instead.

Output buffering is usually determined by *file*. However, if *flush* is true, the stream is forcibly flushed.

::: versionchanged
3.3 Added the *flush* keyword argument.
:::
::::

:::::::::: {.property(fget=None, .fset=None, .fdel=None, .doc=None)}
Return a property attribute.

*fget* is a function for getting an attribute value. *fset* is a function for setting an attribute value. *fdel* is a function for deleting an attribute value. And *doc* creates a docstring for the attribute.

A typical use is to define a managed attribute `x`:

    class C:
        def __init__(self):
            self._x = None

        def getx(self):
            return self._x

        def setx(self, value):
            self._x = value

        def delx(self):
            del self._x

        x = property(getx, setx, delx, "I'm the 'x' property.")

If *c* is an instance of *C*, `c.x` will invoke the getter, `c.x = value` will invoke the setter, and `del c.x` the deleter.

If given, *doc* will be the docstring of the property attribute. Otherwise, the property will copy *fget*\'s docstring (if it exists). This makes it possible to create read-only properties easily using `property`{.interpreted-text role="func"} as a `decorator`{.interpreted-text role="term"}:

    class Parrot:
        def __init__(self):
            self._voltage = 100000

        @property
        def voltage(self):
            """Get the current voltage."""
            return self._voltage

The `@property` decorator turns the `!voltage`{.interpreted-text role="meth"} method into a \"getter\" for a read-only attribute with the same name, and it sets the docstring for *voltage* to \"Get the current voltage.\"

::: decorator
property.getter
:::

::: decorator
property.setter
:::

:::: decorator
property.deleter

A property object has `getter`, `setter`, and `deleter` methods usable as decorators that create a copy of the property with the corresponding accessor function set to the decorated function. This is best explained with an example:

::: testcode

class C:

:   

    def \_\_init\_\_(self):

    :   self.\_x = None

    \@property def x(self): \"\"\"I\'m the \'x\' property.\"\"\" return self.\_x

    \@x.setter def x(self, value): self.\_x = value

    \@x.deleter def x(self): del self.\_x
:::

This code is exactly equivalent to the first example. Be sure to give the additional functions the same name as the original property (`x` in this case.)

The returned property object also has the attributes `fget`, `fset`, and `fdel` corresponding to the constructor arguments.
::::

::: versionchanged
3.5 The docstrings of property objects are now writeable.
:::

:::: attribute
\_\_name\_\_

Attribute holding the name of the property. The name of the property can be changed at runtime.

::: versionadded
3.13
:::
::::
::::::::::

> Rather than being a function, `range`{.interpreted-text role="class"} is actually an immutable sequence type, as documented in `typesseq-range`{.interpreted-text role="ref"} and `typesseq`{.interpreted-text role="ref"}.

::: function
repr(object, /)

Return a string containing a printable representation of an object. For many types, this function makes an attempt to return a string that would yield an object with the same value when passed to `eval`{.interpreted-text role="func"}; otherwise, the representation is a string enclosed in angle brackets that contains the name of the type of the object together with additional information often including the name and address of the object. A class can control what this function returns for its instances by defining a `~object.__repr__`{.interpreted-text role="meth"} method. If `sys.displayhook`{.interpreted-text role="func"} is not accessible, this function will raise `RuntimeError`{.interpreted-text role="exc"}.

This class has a custom representation that can be evaluated:

    class Person:
       def __init__(self, name, age):
          self.name = name
          self.age = age

       def __repr__(self):
          return f"Person('{self.name}', {self.age})"
:::

::: function
reversed(object, /)

Return a reverse `iterator`{.interpreted-text role="term"}. The argument must be an object which has a `~object.__reversed__`{.interpreted-text role="meth"} method or supports the sequence protocol (the `~object.__len__`{.interpreted-text role="meth"} method and the `~object.__getitem__`{.interpreted-text role="meth"} method with integer arguments starting at `0`).
:::

::::: function
round(number, ndigits=None)

Return *number* rounded to *ndigits* precision after the decimal point. If *ndigits* is omitted or is `None`, it returns the nearest integer to its input.

For the built-in types supporting `round`{.interpreted-text role="func"}, values are rounded to the closest multiple of 10 to the power minus *ndigits*; if two multiples are equally close, rounding is done toward the even choice (so, for example, both `round(0.5)` and `round(-0.5)` are `0`, and `round(1.5)` is `2`). Any integer value is valid for *ndigits* (positive, zero, or negative). The return value is an integer if *ndigits* is omitted or `None`. Otherwise, the return value has the same type as *number*.

For a general Python object `number`, `round` delegates to `number.__round__`.

:::: note
::: title
Note
:::

The behavior of `round`{.interpreted-text role="func"} for floats can be surprising: for example, `round(2.675, 2)` gives `2.67` instead of the expected `2.68`. This is not a bug: it\'s a result of the fact that most decimal fractions can\'t be represented exactly as a float. See `tut-fp-issues`{.interpreted-text role="ref"} for more information.
::::
:::::

> Return a new `set`{.interpreted-text role="class"} object, optionally with elements taken from *iterable*. `set` is a built-in class. See `set`{.interpreted-text role="class"} and `types-set`{.interpreted-text role="ref"} for documentation about this class.
>
> For other containers see the built-in `frozenset`{.interpreted-text role="class"}, `list`{.interpreted-text role="class"}, `tuple`{.interpreted-text role="class"}, and `dict`{.interpreted-text role="class"} classes, as well as the `collections`{.interpreted-text role="mod"} module.

::::: function
setattr(object, name, value, /)

This is the counterpart of `getattr`{.interpreted-text role="func"}. The arguments are an object, a string, and an arbitrary value. The string may name an existing attribute or a new attribute. The function assigns the value to the attribute, provided the object allows it. For example, `setattr(x, 'foobar', 123)` is equivalent to `x.foobar = 123`.

*name* need not be a Python identifier as defined in `identifiers`{.interpreted-text role="ref"} unless the object chooses to enforce that, for example in a custom `~object.__getattribute__`{.interpreted-text role="meth"} or via `~object.__slots__`{.interpreted-text role="attr"}. An attribute whose name is not an identifier will not be accessible using the dot notation, but is accessible through `getattr`{.interpreted-text role="func"} etc..

:::: note
::: title
Note
:::

Since `private name mangling <private-name-mangling>`{.interpreted-text role="ref"} happens at compilation time, one must manually mangle a private attribute\'s (attributes with two leading underscores) name in order to set it with `setattr`{.interpreted-text role="func"}.
::::
:::::

::::: {.slice(stop, ./) .slice(start, .stop, .step=None, ./)}
Return a `slice`{.interpreted-text role="term"} object representing the set of indices specified by `range(start, stop, step)`. The *start* and *step* arguments default to `None`.

Slice objects are also generated when `slicing syntax <slicings>`{.interpreted-text role="ref"} is used. For example: `a[start:stop:step]` or `a[start:stop, i]`.

See `itertools.islice`{.interpreted-text role="func"} for an alternate version that returns an `iterator`{.interpreted-text role="term"}.

::: attribute
slice.start slice.stop slice.step

These read-only attributes are set to the argument values (or their default). They have no other explicit functionality; however, they are used by NumPy and other third-party packages.
:::

::: versionchanged
3.12 Slice objects are now `hashable`{.interpreted-text role="term"} (provided `~slice.start`{.interpreted-text role="attr"}, `~slice.stop`{.interpreted-text role="attr"}, and `~slice.step`{.interpreted-text role="attr"} are hashable).
:::
:::::

::: function
sorted(iterable, /, \*, key=None, reverse=False)

Return a new sorted list from the items in *iterable*.

Has two optional arguments which must be specified as keyword arguments.

*key* specifies a function of one argument that is used to extract a comparison key from each element in *iterable* (for example, `key=str.lower`). The default value is `None` (compare the elements directly).

*reverse* is a boolean value. If set to `True`, then the list elements are sorted as if each comparison were reversed.

Use `functools.cmp_to_key`{.interpreted-text role="func"} to convert an old-style *cmp* function to a *key* function.

The built-in `sorted`{.interpreted-text role="func"} function is guaranteed to be stable. A sort is stable if it guarantees not to change the relative order of elements that compare equal \-\-- this is helpful for sorting in multiple passes (for example, sort by department, then by salary grade).

The sort algorithm uses only `<` comparisons between items. While defining an `~object.__lt__`{.interpreted-text role="meth"} method will suffice for sorting, [PEP 8](http://www.python.org/dev/peps/pep-0008/ "PEP 8") recommends that all six `rich comparisons
<comparisons>`{.interpreted-text role="ref"} be implemented. This will help avoid bugs when using the same data with other ordering tools such as `max`{.interpreted-text role="func"} that rely on a different underlying method. Implementing all six comparisons also helps avoid confusion for mixed type comparisons which can call the reflected `~object.__gt__`{.interpreted-text role="meth"} method.

For sorting examples and a brief sorting tutorial, see `sortinghowto`{.interpreted-text role="ref"}.
:::

:::: decorator
staticmethod

Transform a method into a static method.

A static method does not receive an implicit first argument. To declare a static method, use this idiom:

    class C:
        @staticmethod
        def f(arg1, arg2, argN): ...

The `@staticmethod` form is a function `decorator`{.interpreted-text role="term"} \-- see `function`{.interpreted-text role="ref"} for details.

A static method can be called either on the class (such as `C.f()`) or on an instance (such as `C().f()`). Moreover, the static method `descriptor`{.interpreted-text role="term"} is also callable, so it can be used in the class definition (such as `f()`).

Static methods in Python are similar to those found in Java or C++. Also, see `classmethod`{.interpreted-text role="func"} for a variant that is useful for creating alternate class constructors.

Like all decorators, it is also possible to call `staticmethod` as a regular function and do something with its result. This is needed in some cases where you need a reference to a function from a class body and you want to avoid the automatic transformation to instance method. For these cases, use this idiom:

    def regular_function():
        ...

    class C:
        method = staticmethod(regular_function)

For more information on static methods, see `types`{.interpreted-text role="ref"}.

::: versionchanged
3.10 Static methods now inherit the method attributes (`~function.__module__`{.interpreted-text role="attr"}, `~function.__name__`{.interpreted-text role="attr"}, `~function.__qualname__`{.interpreted-text role="attr"}, `~function.__doc__`{.interpreted-text role="attr"} and `~function.__annotations__`{.interpreted-text role="attr"}), have a new `__wrapped__` attribute, and are now callable as regular functions.
:::
::::

::: index
single: string; str() (built-in function)
:::

> Return a `str`{.interpreted-text role="class"} version of *object*. See `str`{.interpreted-text role="func"} for details.
>
> `str` is the built-in string `class`{.interpreted-text role="term"}. For general information about strings, see `textseq`{.interpreted-text role="ref"}.

:::::: function
sum(iterable, /, start=0)

Sums *start* and the items of an *iterable* from left to right and returns the total. The *iterable*\'s items are normally numbers, and the start value is not allowed to be a string.

For some use cases, there are good alternatives to `sum`{.interpreted-text role="func"}. The preferred, fast way to concatenate a sequence of strings is by calling `''.join(sequence)`. To add floating-point values with extended precision, see `math.fsum`{.interpreted-text role="func"}. To concatenate a series of iterables, consider using `itertools.chain`{.interpreted-text role="func"}.

::: versionchanged
3.8 The *start* parameter can be specified as a keyword argument.
:::

::: versionchanged
3.12 Summation of floats switched to an algorithm that gives higher accuracy and better commutativity on most builds.
:::

::: versionchanged
3.14 Added specialization for summation of complexes, using same algorithm as for summation of floats.
:::
::::::

:::: {.super() .super(type, .object_or_type=None, ./)}
Return a proxy object that delegates method calls to a parent or sibling class of *type*. This is useful for accessing inherited methods that have been overridden in a class.

The *object_or_type* determines the `method resolution order`{.interpreted-text role="term"} to be searched. The search starts from the class right after the *type*.

For example, if `~type.__mro__`{.interpreted-text role="attr"} of *object_or_type* is `D -> B -> C -> A -> object` and the value of *type* is `B`, then `super`{.interpreted-text role="func"} searches `C -> A -> object`.

The `~type.__mro__`{.interpreted-text role="attr"} attribute of the class corresponding to *object_or_type* lists the method resolution search order used by both `getattr`{.interpreted-text role="func"} and `super`{.interpreted-text role="func"}. The attribute is dynamic and can change whenever the inheritance hierarchy is updated.

If the second argument is omitted, the super object returned is unbound. If the second argument is an object, `isinstance(obj, type)` must be true. If the second argument is a type, `issubclass(type2, type)` must be true (this is useful for classmethods).

When called directly within an ordinary method of a class, both arguments may be omitted (\"zero-argument `!super`{.interpreted-text role="func"}\"). In this case, *type* will be the enclosing class, and *obj* will be the first argument of the immediately enclosing function (typically `self`). (This means that zero-argument `!super`{.interpreted-text role="func"} will not work as expected within nested functions, including generator expressions, which implicitly create nested functions.)

There are two typical use cases for *super*. In a class hierarchy with single inheritance, *super* can be used to refer to parent classes without naming them explicitly, thus making the code more maintainable. This use closely parallels the use of *super* in other programming languages.

The second use case is to support cooperative multiple inheritance in a dynamic execution environment. This use case is unique to Python and is not found in statically compiled languages or languages that only support single inheritance. This makes it possible to implement \"diamond diagrams\" where multiple base classes implement the same method. Good design dictates that such implementations have the same calling signature in every case (because the order of calls is determined at runtime, because that order adapts to changes in the class hierarchy, and because that order can include sibling classes that are unknown prior to runtime).

For both use cases, a typical superclass call looks like this:

    class C(B):
        def method(self, arg):
            super().method(arg)    # This does the same thing as:
                                   # super(C, self).method(arg)

In addition to method lookups, `super`{.interpreted-text role="func"} also works for attribute lookups. One possible use case for this is calling `descriptors <descriptor>`{.interpreted-text role="term"} in a parent or sibling class.

Note that `super`{.interpreted-text role="func"} is implemented as part of the binding process for explicit dotted attribute lookups such as `super().__getitem__(name)`. It does so by implementing its own `~object.__getattribute__`{.interpreted-text role="meth"} method for searching classes in a predictable order that supports cooperative multiple inheritance. Accordingly, `super`{.interpreted-text role="func"} is undefined for implicit lookups using statements or operators such as `super()[name]`.

Also note that, aside from the zero argument form, `super`{.interpreted-text role="func"} is not limited to use inside methods. The two argument form specifies the arguments exactly and makes the appropriate references. The zero argument form only works inside a class definition, as the compiler fills in the necessary details to correctly retrieve the class being defined, as well as accessing the current instance for ordinary methods.

For practical suggestions on how to design cooperative classes using `super`{.interpreted-text role="func"}, see [guide to using super()](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/).

::: versionchanged
3.14 `super`{.interpreted-text role="class"} objects are now `pickleable <pickle>`{.interpreted-text role="mod"} and `copyable <copy>`{.interpreted-text role="mod"}.
:::
::::

> Rather than being a function, `tuple`{.interpreted-text role="class"} is actually an immutable sequence type, as documented in `typesseq-tuple`{.interpreted-text role="ref"} and `typesseq`{.interpreted-text role="ref"}.

::::: {.type(object, ./) .type(name, .bases, .dict, ./, .**kwargs)}
::: index
pair: object; type
:::

With one argument, return the type of an *object*. The return value is a type object and generally the same object as returned by `object.__class__`{.interpreted-text role="attr"}.

The `isinstance`{.interpreted-text role="func"} built-in function is recommended for testing the type of an object, because it takes subclasses into account.

With three arguments, return a new type object. This is essentially a dynamic form of the `class`{.interpreted-text role="keyword"} statement. The *name* string is the class name and becomes the `~type.__name__`{.interpreted-text role="attr"} attribute. The *bases* tuple contains the base classes and becomes the `~type.__bases__`{.interpreted-text role="attr"} attribute; if empty, `object`{.interpreted-text role="class"}, the ultimate base of all classes, is added. The *dict* dictionary contains attribute and method definitions for the class body; it may be copied or wrapped before becoming the `~type.__dict__`{.interpreted-text role="attr"} attribute. The following two statements create identical `!type`{.interpreted-text role="class"} objects:

> \>\>\> class X: \... a = 1 \... \>\>\> X = type(\'X\', (), dict(a=1))

See also:

- `Documentation on attributes and methods on classes <class-attrs-and-methods>`{.interpreted-text role="ref"}.
- `bltin-type-objects`{.interpreted-text role="ref"}

Keyword arguments provided to the three argument form are passed to the appropriate metaclass machinery (usually `~object.__init_subclass__`{.interpreted-text role="meth"}) in the same way that keywords in a class definition (besides *metaclass*) would.

See also `class-customization`{.interpreted-text role="ref"}.

::: versionchanged
3.6 Subclasses of `!type`{.interpreted-text role="class"} which don\'t override `type.__new__` may no longer use the one-argument form to get the type of an object.
:::
:::::

:::: function
vars() vars(object, /)

Return the `~object.__dict__`{.interpreted-text role="attr"} attribute for a module, class, instance, or any other object with a `!__dict__`{.interpreted-text role="attr"} attribute.

Objects such as modules and instances have an updateable `~object.__dict__`{.interpreted-text role="attr"} attribute; however, other objects may have write restrictions on their `!__dict__`{.interpreted-text role="attr"} attributes (for example, classes use a `types.MappingProxyType`{.interpreted-text role="class"} to prevent direct dictionary updates).

Without an argument, `vars`{.interpreted-text role="func"} acts like `locals`{.interpreted-text role="func"}.

A `TypeError`{.interpreted-text role="exc"} exception is raised if an object is specified but it doesn\'t have a `~object.__dict__`{.interpreted-text role="attr"} attribute (for example, if its class defines the `~object.__slots__`{.interpreted-text role="attr"} attribute).

::: versionchanged
3.13

The result of calling this function without an argument has been updated as described for the `locals`{.interpreted-text role="func"} builtin.
:::
::::

:::: function
zip(\*iterables, strict=False)

Iterate over several iterables in parallel, producing tuples with an item from each one.

Example:

    >>> for item in zip([1, 2, 3], ['sugar', 'spice', 'everything nice']):
    ...     print(item)
    ...
    (1, 'sugar')
    (2, 'spice')
    (3, 'everything nice')

More formally: `zip`{.interpreted-text role="func"} returns an iterator of tuples, where the *i*-th tuple contains the *i*-th element from each of the argument iterables.

Another way to think of `zip`{.interpreted-text role="func"} is that it turns rows into columns, and columns into rows. This is similar to [transposing a matrix](https://en.wikipedia.org/wiki/Transpose).

`zip`{.interpreted-text role="func"} is lazy: The elements won\'t be processed until the iterable is iterated on, e.g. by a `!for`{.interpreted-text role="keyword"} loop or by wrapping in a `list`{.interpreted-text role="class"}.

One thing to consider is that the iterables passed to `zip`{.interpreted-text role="func"} could have different lengths; sometimes by design, and sometimes because of a bug in the code that prepared these iterables. Python offers three different approaches to dealing with this issue:

- By default, `zip`{.interpreted-text role="func"} stops when the shortest iterable is exhausted. It will ignore the remaining items in the longer iterables, cutting off the result to the length of the shortest iterable:

      >>> list(zip(range(3), ['fee', 'fi', 'fo', 'fum']))
      [(0, 'fee'), (1, 'fi'), (2, 'fo')]

- `zip`{.interpreted-text role="func"} is often used in cases where the iterables are assumed to be of equal length. In such cases, it\'s recommended to use the `strict=True` option. Its output is the same as regular `zip`{.interpreted-text role="func"}:

      >>> list(zip(('a', 'b', 'c'), (1, 2, 3), strict=True))
      [('a', 1), ('b', 2), ('c', 3)]

  Unlike the default behavior, it raises a `ValueError`{.interpreted-text role="exc"} if one iterable is exhausted before the others:

  > \>\>\> for item in zip(range(3), \[\'fee\', \'fi\', \'fo\', \'fum\'\], strict=True): \# doctest: +SKIP \... print(item) \... (0, \'fee\') (1, \'fi\') (2, \'fo\') Traceback (most recent call last): \... ValueError: zip() argument 2 is longer than argument 1

  Without the `strict=True` argument, any bug that results in iterables of different lengths will be silenced, possibly manifesting as a hard-to-find bug in another part of the program.

- Shorter iterables can be padded with a constant value to make all the iterables have the same length. This is done by `itertools.zip_longest`{.interpreted-text role="func"}.

Edge cases: With a single iterable argument, `zip`{.interpreted-text role="func"} returns an iterator of 1-tuples. With no arguments, it returns an empty iterator.

Tips and tricks:

- The left-to-right evaluation order of the iterables is guaranteed. This makes possible an idiom for clustering a data series into n-length groups using `zip(*[iter(s)]*n, strict=True)`. This repeats the *same* iterator `n` times so that each output tuple has the result of `n` calls to the iterator. This has the effect of dividing the input into n-length chunks.

- `zip`{.interpreted-text role="func"} in conjunction with the `*` operator can be used to unzip a list:

      >>> x = [1, 2, 3]
      >>> y = [4, 5, 6]
      >>> list(zip(x, y))
      [(1, 4), (2, 5), (3, 6)]
      >>> x2, y2 = zip(*zip(x, y))
      >>> x == list(x2) and y == list(y2)
      True

::: versionchanged
3.10 Added the `strict` argument.
:::
::::

:::::::: function
\_\_import\_\_(name, globals=None, locals=None, fromlist=(), level=0)

::: index
pair: statement; import pair: module; builtins
:::

:::: note
::: title
Note
:::

This is an advanced function that is not needed in everyday Python programming, unlike `importlib.import_module`{.interpreted-text role="func"}.
::::

This function is invoked by the `import`{.interpreted-text role="keyword"} statement. It can be replaced (by importing the `builtins`{.interpreted-text role="mod"} module and assigning to `builtins.__import__`) in order to change semantics of the `!import`{.interpreted-text role="keyword"} statement, but doing so is **strongly** discouraged as it is usually simpler to use import hooks (see `302`{.interpreted-text role="pep"}) to attain the same goals and does not cause issues with code which assumes the default import implementation is in use. Direct use of `__import__`{.interpreted-text role="func"} is also discouraged in favor of `importlib.import_module`{.interpreted-text role="func"}.

The function imports the module *name*, potentially using the given *globals* and *locals* to determine how to interpret the name in a package context. The *fromlist* gives the names of objects or submodules that should be imported from the module given by *name*. The standard implementation does not use its *locals* argument at all and uses its *globals* only to determine the package context of the `import`{.interpreted-text role="keyword"} statement.

*level* specifies whether to use absolute or relative imports. `0` (the default) means only perform absolute imports. Positive values for *level* indicate the number of parent directories to search relative to the directory of the module calling `__import__`{.interpreted-text role="func"} (see `328`{.interpreted-text role="pep"} for the details).

When the *name* variable is of the form `package.module`, normally, the top-level package (the name up till the first dot) is returned, *not* the module named by *name*. However, when a non-empty *fromlist* argument is given, the module named by *name* is returned.

For example, the statement `import spam` results in bytecode resembling the following code:

    spam = __import__('spam', globals(), locals(), [], 0)

The statement `import spam.ham` results in this call:

    spam = __import__('spam.ham', globals(), locals(), [], 0)

Note how `__import__`{.interpreted-text role="func"} returns the toplevel module here because this is the object that is bound to a name by the `import`{.interpreted-text role="keyword"} statement.

On the other hand, the statement `from spam.ham import eggs, sausage as saus` results in :

    _temp = __import__('spam.ham', globals(), locals(), ['eggs', 'sausage'], 0)
    eggs = _temp.eggs
    saus = _temp.sausage

Here, the `spam.ham` module is returned from `__import__`{.interpreted-text role="func"}. From this object, the names to import are retrieved and assigned to their respective names.

If you simply want to import a module (potentially within a package) by name, use `importlib.import_module`{.interpreted-text role="func"}.

::: versionchanged
3.3 Negative values for *level* are no longer supported (which also changes the default value to 0).
:::

::: versionchanged
3.9 When the command line options `-E`{.interpreted-text role="option"} or `-I`{.interpreted-text role="option"} are being used, the environment variable `PYTHONCASEOK`{.interpreted-text role="envvar"} is now ignored.
:::
::::::::

**Footnotes**

[^1]: Note that the parser only accepts the Unix-style end of line convention. If you are reading the code from a file, make sure to use newline conversion mode to convert Windows or Mac-style newlines.
