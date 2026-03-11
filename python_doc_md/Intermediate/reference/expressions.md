# Expressions

::: index
expression, BNF
:::

This chapter explains the meaning of the elements of expressions in Python.

**Syntax Notes:** In this and the following chapters, `grammar notation <notation>`{.interpreted-text role="ref"} will be used to describe syntax, not lexical analysis.

When (one alternative of) a syntax rule has the form:

::: productionlist
python-grammar name: othername
:::

and no semantics are given, the semantics of this form of `name` are the same as for `othername`.

## Arithmetic conversions {#conversions}

::: index
pair: arithmetic; conversion
:::

When a description of an arithmetic operator below uses the phrase \"the numeric arguments are converted to a common real type\", this means that the operator implementation for built-in numeric types works as described in the `Numeric Types <stdtypes-mixed-arithmetic>`{.interpreted-text role="ref"} section of the standard library documentation.

Some additional rules apply for certain operators and non-numeric operands (for example, a string as a left argument to the `%` operator). Extensions must define their own conversion behavior.

## Atoms

::: index
atom
:::

Atoms are the most basic elements of expressions. The simplest atoms are `names <identifiers>`{.interpreted-text role="ref"} or literals. Forms enclosed in parentheses, brackets or braces are also categorized syntactically as atoms.

Formally, the syntax for atoms is:

::: {.grammar-snippet group="python-grammar"}

atom:

:   | \'True\'
    | \'False\'
    | \'None\'
    | \'\...\'
    | [identifier]{.title-ref}
    | [literal]{.title-ref}
    | [enclosure]{.title-ref}

enclosure:

:   | [parenth_form]{.title-ref}
    | [list_display]{.title-ref}
    | [dict_display]{.title-ref}
    | [set_display]{.title-ref}
    | [generator_expression]{.title-ref}
    | [yield_atom]{.title-ref}
:::

### Built-in constants {#atom-singletons}

The keywords `True`, `False`, and `None` name `built-in constants <built-in-consts>`{.interpreted-text role="ref"}. The token `...` names the `Ellipsis`{.interpreted-text role="py:data"} constant.

Evaluation of these atoms yields the corresponding value.

:::: note
::: title
Note
:::

Several more built-in constants are available as global variables, but only the ones mentioned here are `keywords <keywords>`{.interpreted-text role="ref"}. In particular, these names cannot be reassigned or used as attributes:

``` pycon
>>> False = 123
  File "<input>", line 1
   False = 123
   ^^^^^
SyntaxError: cannot assign to False
```
::::

### Identifiers (Names) {#atom-identifiers}

::: index
name, identifier
:::

An identifier occurring as an atom is a name. See section `identifiers`{.interpreted-text role="ref"} for lexical definition and section `naming`{.interpreted-text role="ref"} for documentation of naming and binding.

::: index
pair: exception; NameError
:::

When the name is bound to an object, evaluation of the atom yields that object. When a name is not bound, an attempt to evaluate it raises a `NameError`{.interpreted-text role="exc"} exception.

:::: {#private-name-mangling}
::: index
pair: name; mangling pair: private; names
:::
::::

#### Private name mangling

When an identifier that textually occurs in a class definition begins with two or more underscore characters and does not end in two or more underscores, it is considered a `private name`{.interpreted-text role="dfn"} of that class.

::: seealso
The `class specifications <class>`{.interpreted-text role="ref"}.
:::

More precisely, private names are transformed to a longer form before code is generated for them. If the transformed name is longer than 255 characters, implementation-defined truncation may happen.

The transformation is independent of the syntactical context in which the identifier is used but only the following private identifiers are mangled:

- Any name used as the name of a variable that is assigned or read or any name of an attribute being accessed.

  The `~definition.__name__`{.interpreted-text role="attr"} attribute of nested functions, classes, and type aliases is however not mangled.

- The name of imported modules, e.g., `__spam` in `import __spam`. If the module is part of a package (i.e., its name contains a dot), the name is *not* mangled, e.g., the `__foo` in `import __foo.bar` is not mangled.

- The name of an imported member, e.g., `__f` in `from spam import __f`.

The transformation rule is defined as follows:

- The class name, with leading underscores removed and a single leading underscore inserted, is inserted in front of the identifier, e.g., the identifier `__spam` occurring in a class named `Foo`, `_Foo` or `__Foo` is transformed to `_Foo__spam`.
- If the class name consists only of underscores, the transformation is the identity, e.g., the identifier `__spam` occurring in a class named `_` or `__` is left as is.

### Literals {#atom-literals}

::: index
single: literal
:::

A `literal`{.interpreted-text role="dfn"} is a textual representation of a value. Python supports numeric, string and bytes literals. `Format strings <f-strings>`{.interpreted-text role="ref"} and `template strings <t-strings>`{.interpreted-text role="ref"} are treated as string literals.

Numeric literals consist of a single `NUMBER <python-grammar:NUMBER>`{.interpreted-text role="token"} token, which names an integer, floating-point number, or an imaginary number. See the `numbers`{.interpreted-text role="ref"} section in Lexical analysis documentation for details.

String and bytes literals may consist of several tokens. See section `string-concatenation`{.interpreted-text role="ref"} for details.

Note that negative and complex numbers, like `-3` or `3+4.2j`, are syntactically not literals, but `unary <unary>`{.interpreted-text role="ref"} or `binary <binary>`{.interpreted-text role="ref"} arithmetic operations involving the `-` or `+` operator.

Evaluation of a literal yields an object of the given type (`int`{.interpreted-text role="class"}, `float`{.interpreted-text role="class"}, `complex`{.interpreted-text role="class"}, `str`{.interpreted-text role="class"}, `bytes`{.interpreted-text role="class"}, or `~string.templatelib.Template`{.interpreted-text role="class"}) with the given value. The value may be approximated in the case of floating-point and imaginary literals.

The formal grammar for literals is:

::: {.grammar-snippet group="python-grammar"}
literal: [strings]{.title-ref} \| [NUMBER]{.title-ref}
:::

::: index
triple: immutable; data; type pair: immutable; object
:::

#### Literals and object identity

All literals correspond to immutable data types, and hence the object\'s identity is less important than its value. Multiple evaluations of literals with the same value (either the same occurrence in the program text or a different occurrence) may obtain the same object or a different object with the same value.

::: admonition
CPython implementation detail

For example, in CPython, *small* integers with the same value evaluate to the same object:

    >>> x = 7
    >>> y = 7
    >>> x is y
    True

However, large integers evaluate to different objects:

    >>> x = 123456789
    >>> y = 123456789
    >>> x is y
    False

This behavior may change in future versions of CPython. In particular, the boundary between \"small\" and \"large\" integers has already changed in the past.

CPython will emit a `SyntaxWarning`{.interpreted-text role="py:exc"} when you compare literals using `is`:

    >>> x = 7
    >>> x is 7
    <input>:1: SyntaxWarning: "is" with 'int' literal. Did you mean "=="?
    True

See `faq-identity-with-is`{.interpreted-text role="ref"} for more information.
:::

`Template strings <t-strings>`{.interpreted-text role="ref"} are immutable but may reference mutable objects as `~string.templatelib.Interpolation`{.interpreted-text role="class"} values. For the purposes of this section, two t-strings have the \"same value\" if both their structure and the *identity* of the values match.

::: impl-detail
Currently, each evaluation of a template string results in a different object.
:::

#### String literal concatenation {#string-concatenation}

Multiple adjacent string or bytes literals, possibly using different quoting conventions, are allowed, and their meaning is the same as their concatenation:

    >>> "hello" 'world'
    "helloworld"

This feature is defined at the syntactical level, so it only works with literals. To concatenate string expressions at run time, the \'+\' operator may be used:

    >>> greeting = "Hello"
    >>> space = " "
    >>> name = "Blaise"
    >>> print(greeting + space + name)   # not: print(greeting space name)
    Hello Blaise

Literal concatenation can freely mix raw strings, triple-quoted strings, and formatted string literals. For example:

    >>> "Hello" r', ' f"{name}!"
    "Hello, Blaise!"

This feature can be used to reduce the number of backslashes needed, to split long strings conveniently across long lines, or even to add comments to parts of strings. For example:

    re.compile("[A-Za-z_]"       # letter or underscore
               "[A-Za-z0-9_]*"   # letter, digit or underscore
              )

However, bytes literals may only be combined with other byte literals; not with string literals of any kind. Also, template string literals may only be combined with other template string literals:

    >>> t"Hello" t"{name}!"
    Template(strings=('Hello', '!'), interpolations=(...))

Formally:

::: {.grammar-snippet group="python-grammar"}
strings: ([STRING]{.title-ref} \| [fstring]{.title-ref})+ \| [tstring]{.title-ref}+
:::

### Parenthesized forms {#parenthesized}

::: index
single: parenthesized form single: () (parentheses); tuple display
:::

A parenthesized form is an optional expression list enclosed in parentheses:

::: productionlist
python-grammar parenth_form: \"(\" \[[starred_expression]{.title-ref}\] \")\"
:::

A parenthesized expression list yields whatever that expression list yields: if the list contains at least one comma, it yields a tuple; otherwise, it yields the single expression that makes up the expression list.

::: index
pair: empty; tuple
:::

An empty pair of parentheses yields an empty tuple object. Since tuples are immutable, the same rules as for literals apply (i.e., two occurrences of the empty tuple may or may not yield the same object).

::: index
single: comma single: , (comma)
:::

Note that tuples are not formed by the parentheses, but rather by use of the comma. The exception is the empty tuple, for which parentheses *are* required \-\-- allowing unparenthesized \"nothing\" in expressions would cause ambiguities and allow common typos to pass uncaught.

### Displays for lists, sets and dictionaries {#comprehensions}

::: index
single: comprehensions
:::

For constructing a list, a set or a dictionary Python provides special syntax called \"displays\", each of them in two flavors:

- either the container contents are listed explicitly, or
- they are computed via a set of looping and filtering instructions, called a `comprehension`{.interpreted-text role="dfn"}.

::: index
single: for; in comprehensions single: if; in comprehensions single: async for; in comprehensions
:::

Common syntax elements for comprehensions are:

::: productionlist
python-grammar comprehension: [flexible_expression]{.title-ref} [comp_for]{.title-ref} comp_for: \[\"async\"\] \"for\" [target_list]{.title-ref} \"in\" [or_test]{.title-ref} \[[comp_iter]{.title-ref}\] comp_iter: [comp_for]{.title-ref} \| [comp_if]{.title-ref} comp_if: \"if\" [or_test]{.title-ref} \[[comp_iter]{.title-ref}\]
:::

The comprehension consists of a single expression followed by at least one `!for`{.interpreted-text role="keyword"} clause and zero or more `!for`{.interpreted-text role="keyword"} or `!if`{.interpreted-text role="keyword"} clauses. In this case, the elements of the new container are those that would be produced by considering each of the `!for`{.interpreted-text role="keyword"} or `!if`{.interpreted-text role="keyword"} clauses a block, nesting from left to right, and evaluating the expression to produce an element each time the innermost block is reached. If the expression is starred, the result will instead be unpacked to produce zero or more elements.

However, aside from the iterable expression in the leftmost `!for`{.interpreted-text role="keyword"} clause, the comprehension is executed in a separate implicitly nested scope. This ensures that names assigned to in the target list don\'t \"leak\" into the enclosing scope.

The iterable expression in the leftmost `!for`{.interpreted-text role="keyword"} clause is evaluated directly in the enclosing scope and then passed as an argument to the implicitly nested scope. Subsequent `!for`{.interpreted-text role="keyword"} clauses and any filter condition in the leftmost `!for`{.interpreted-text role="keyword"} clause cannot be evaluated in the enclosing scope as they may depend on the values obtained from the leftmost iterable. For example: `[x*y for x in range(10) for y in range(x, x+10)]`.

To ensure the comprehension always results in a container of the appropriate type, `yield` and `yield from` expressions are prohibited in the implicitly nested scope.

::: index
single: await; in comprehensions
:::

Since Python 3.6, in an `async def`{.interpreted-text role="keyword"} function, an `!async for`{.interpreted-text role="keyword"} clause may be used to iterate over a `asynchronous iterator`{.interpreted-text role="term"}. A comprehension in an `!async def`{.interpreted-text role="keyword"} function may consist of either a `!for`{.interpreted-text role="keyword"} or `!async for`{.interpreted-text role="keyword"} clause following the leading expression, may contain additional `!for`{.interpreted-text role="keyword"} or `!async for`{.interpreted-text role="keyword"} clauses, and may also use `await`{.interpreted-text role="keyword"} expressions.

If a comprehension contains `!async for`{.interpreted-text role="keyword"} clauses, or if it contains `!await`{.interpreted-text role="keyword"} expressions or other asynchronous comprehensions anywhere except the iterable expression in the leftmost `!for`{.interpreted-text role="keyword"} clause, it is called an `asynchronous comprehension`{.interpreted-text role="dfn"}. An asynchronous comprehension may suspend the execution of the coroutine function in which it appears. See also `530`{.interpreted-text role="pep"}.

::: versionadded
3.6 Asynchronous comprehensions were introduced.
:::

::: versionchanged
3.8 `yield` and `yield from` prohibited in the implicitly nested scope.
:::

::: versionchanged
3.11 Asynchronous comprehensions are now allowed inside comprehensions in asynchronous functions. Outer comprehensions implicitly become asynchronous.
:::

::: versionchanged
3.15 Unpacking with the `*` operator is now allowed in the expression.
:::

### List displays {#lists}

::: index
pair: list; display pair: list; comprehensions pair: empty; list pair: object; list single: \[\] (square brackets); list expression single: , (comma); expression list
:::

A list display is a possibly empty series of expressions enclosed in square brackets:

::: productionlist
python-grammar list_display: \"\[\" \[[flexible_expression_list]{.title-ref} \| [comprehension]{.title-ref}\] \"\]\"
:::

A list display yields a new list object, the contents being specified by either a list of expressions or a comprehension. When a comma-separated list of expressions is supplied, its elements are evaluated from left to right and placed into the list object in that order. When a comprehension is supplied, the list is constructed from the elements resulting from the comprehension.

### Set displays {#set}

::: index
pair: set; display pair: set; comprehensions pair: object; set single: {} (curly brackets); set expression single: , (comma); expression list
:::

A set display is denoted by curly braces and distinguishable from dictionary displays by the lack of colons separating keys and values:

::: productionlist
python-grammar set_display: \"{\" ([flexible_expression_list]{.title-ref} \| [comprehension]{.title-ref}) \"}\"
:::

A set display yields a new mutable set object, the contents being specified by either a sequence of expressions or a comprehension. When a comma-separated list of expressions is supplied, its elements are evaluated from left to right and added to the set object. When a comprehension is supplied, the set is constructed from the elements resulting from the comprehension.

An empty set cannot be constructed with `{}`; this literal constructs an empty dictionary.

### Dictionary displays {#dict}

::: index
pair: dictionary; display pair: dictionary; comprehensions key, value, key/value pair pair: object; dictionary single: {} (curly brackets); dictionary expression single: : (colon); in dictionary expressions single: , (comma); in dictionary displays
:::

A dictionary display is a possibly empty series of dict items (key/value pairs) enclosed in curly braces:

::: productionlist
python-grammar dict_display: \"{\" \[[dict_item_list]{.title-ref} \| [dict_comprehension]{.title-ref}\] \"}\" dict_item_list: [dict_item]{.title-ref} (\",\" [dict_item]{.title-ref})\* \[\",\"\] dict_comprehension: [dict_item]{.title-ref} [comp_for]{.title-ref} dict_item: [expression]{.title-ref} \":\" [expression]{.title-ref} \| \"\*\*\" [or_expr]{.title-ref}
:::

A dictionary display yields a new dictionary object.

If a comma-separated sequence of dict items is given, they are evaluated from left to right to define the entries of the dictionary: each key object is used as a key into the dictionary to store the corresponding value. This means that you can specify the same key multiple times in the dict item list, and the final dictionary\'s value for that key will be the last one given.

::: index
unpacking; dictionary single: \*\*; in dictionary displays
:::

A double asterisk `**` denotes `dictionary unpacking`{.interpreted-text role="dfn"}. Its operand must be a `mapping`{.interpreted-text role="term"}. Each mapping item is added to the new dictionary. Later values replace values already set by earlier dict items and earlier dictionary unpackings.

::: versionadded
3.5 Unpacking into dictionary displays, originally proposed by `448`{.interpreted-text role="pep"}.
:::

A dict comprehension may take one of two forms:

- The first form uses two expressions separated with a colon followed by the usual \"for\" and \"if\" clauses. When the comprehension is run, the resulting key and value elements are inserted in the new dictionary in the order they are produced.
- The second form uses a single expression prefixed by the `**` dictionary unpacking operator followed by the usual \"for\" and \"if\" clauses. When the comprehension is evaluated, the expression is evaluated and then unpacked, inserting zero or more key/value pairs into the new dictionary.

Both forms of dictionary comprehension retain the property that if the same key is specified multiple times, the associated value in the resulting dictionary will be the last one specified.

::: index
pair: immutable; object hashable
:::

Restrictions on the types of the key values are listed earlier in section `types`{.interpreted-text role="ref"}. (To summarize, the key type should be `hashable`{.interpreted-text role="term"}, which excludes all mutable objects.) Clashes between duplicate keys are not detected; the last value (textually rightmost in the display) stored for a given key value prevails.

::: versionchanged
3.8 Prior to Python 3.8, in dict comprehensions, the evaluation order of key and value was not well-defined. In CPython, the value was evaluated before the key. Starting with 3.8, the key is evaluated before the value, as proposed by `572`{.interpreted-text role="pep"}.
:::

::: versionchanged
3.15 Unpacking with the `**` operator is now allowed in dictionary comprehensions.
:::

### Generator expressions {#genexpr}

::: index
pair: generator; expression pair: object; generator single: () (parentheses); generator expression
:::

A generator expression is a compact generator notation in parentheses:

::: productionlist
python-grammar generator_expression: \"(\" [flexible_expression]{.title-ref} [comp_for]{.title-ref} \")\"
:::

A generator expression yields a new generator object. Its syntax is the same as for comprehensions, except that it is enclosed in parentheses instead of brackets or curly braces.

Variables used in the generator expression are evaluated lazily when the `~generator.__next__`{.interpreted-text role="meth"} method is called for the generator object (in the same fashion as normal generators). However, the iterable expression in the leftmost `!for`{.interpreted-text role="keyword"} clause is immediately evaluated, and the `iterator`{.interpreted-text role="term"} is immediately created for that iterable, so that an error produced while creating the iterator will be emitted at the point where the generator expression is defined, rather than at the point where the first value is retrieved. Subsequent `!for`{.interpreted-text role="keyword"} clauses and any filter condition in the leftmost `!for`{.interpreted-text role="keyword"} clause cannot be evaluated in the enclosing scope as they may depend on the values obtained from the leftmost iterable. For example: `(x*y for x in range(10) for y in range(x, x+10))`.

The parentheses can be omitted on calls with only one argument. See section `calls`{.interpreted-text role="ref"} for details.

To avoid interfering with the expected operation of the generator expression itself, `yield` and `yield from` expressions are prohibited in the implicitly defined generator.

If a generator expression contains either `!async for`{.interpreted-text role="keyword"} clauses or `await`{.interpreted-text role="keyword"} expressions it is called an `asynchronous generator expression`{.interpreted-text role="dfn"}. An asynchronous generator expression returns a new asynchronous generator object, which is an asynchronous iterator (see `async-iterators`{.interpreted-text role="ref"}).

::: versionadded
3.6 Asynchronous generator expressions were introduced.
:::

::: versionchanged
3.7 Prior to Python 3.7, asynchronous generator expressions could only appear in `async def`{.interpreted-text role="keyword"} coroutines. Starting with 3.7, any function can use asynchronous generator expressions.
:::

::: versionchanged
3.8 `yield` and `yield from` prohibited in the implicitly nested scope.
:::

### Yield expressions {#yieldexpr}

::: index
pair: keyword; yield pair: keyword; from pair: yield; expression pair: generator; function
:::

::: productionlist
python-grammar yield_atom: \"(\" [yield_expression]{.title-ref} \")\" yield_from: \"yield\" \"from\" [expression]{.title-ref} yield_expression: \"yield\" [yield_list]{.title-ref} \| [yield_from]{.title-ref}
:::

The yield expression is used when defining a `generator`{.interpreted-text role="term"} function or an `asynchronous generator`{.interpreted-text role="term"} function and thus can only be used in the body of a function definition. Using a yield expression in a function\'s body causes that function to be a generator function, and using it in an `async def`{.interpreted-text role="keyword"} function\'s body causes that coroutine function to be an asynchronous generator function. For example:

    def gen():  # defines a generator function
        yield 123

    async def agen(): # defines an asynchronous generator function
        yield 123

Due to their side effects on the containing scope, `yield` expressions are not permitted as part of the implicitly defined scopes used to implement comprehensions and generator expressions.

::: versionchanged
3.8 Yield expressions prohibited in the implicitly nested scopes used to implement comprehensions and generator expressions.
:::

Generator functions are described below, while asynchronous generator functions are described separately in section `asynchronous-generator-functions`{.interpreted-text role="ref"}.

When a generator function is called, it returns an iterator known as a generator. That generator then controls the execution of the generator function. The execution starts when one of the generator\'s methods is called. At that time, the execution proceeds to the first yield expression, where it is suspended again, returning the value of `~python-grammar:yield_list`{.interpreted-text role="token"} to the generator\'s caller, or `None` if `~python-grammar:yield_list`{.interpreted-text role="token"} is omitted. By suspended, we mean that all local state is retained, including the current bindings of local variables, the instruction pointer, the internal evaluation stack, and the state of any exception handling. When the execution is resumed by calling one of the generator\'s methods, the function can proceed exactly as if the yield expression were just another external call. The value of the yield expression after resuming depends on the method which resumed the execution. If `~generator.__next__`{.interpreted-text role="meth"} is used (typically via either a `for`{.interpreted-text role="keyword"} or the `next`{.interpreted-text role="func"} builtin) then the result is `None`{.interpreted-text role="const"}. Otherwise, if `~generator.send`{.interpreted-text role="meth"} is used, then the result will be the value passed in to that method.

::: index
single: coroutine
:::

All of this makes generator functions quite similar to coroutines; they yield multiple times, they have more than one entry point and their execution can be suspended. The only difference is that a generator function cannot control where the execution should continue after it yields; the control is always transferred to the generator\'s caller.

Yield expressions are allowed anywhere in a `try`{.interpreted-text role="keyword"} construct. If the generator is not resumed before it is finalized (by reaching a zero reference count or by being garbage collected), the generator-iterator\'s `~generator.close`{.interpreted-text role="meth"} method will be called, allowing any pending `finally`{.interpreted-text role="keyword"} clauses to execute.

::: index
single: from; yield from expression
:::

When `yield from <expr>` is used, the supplied expression must be an iterable. The values produced by iterating that iterable are passed directly to the caller of the current generator\'s methods. Any values passed in with `~generator.send`{.interpreted-text role="meth"} and any exceptions passed in with `~generator.throw`{.interpreted-text role="meth"} are passed to the underlying iterator if it has the appropriate methods. If this is not the case, then `~generator.send`{.interpreted-text role="meth"} will raise `AttributeError`{.interpreted-text role="exc"} or `TypeError`{.interpreted-text role="exc"}, while `~generator.throw`{.interpreted-text role="meth"} will just raise the passed in exception immediately.

When the underlying iterator is complete, the `~StopIteration.value`{.interpreted-text role="attr"} attribute of the raised `StopIteration`{.interpreted-text role="exc"} instance becomes the value of the yield expression. It can be either set explicitly when raising `StopIteration`{.interpreted-text role="exc"}, or automatically when the subiterator is a generator (by returning a value from the subgenerator).

::: versionchanged
3.3 Added `yield from <expr>` to delegate control flow to a subiterator.
:::

The parentheses may be omitted when the yield expression is the sole expression on the right hand side of an assignment statement.

::: seealso

`255`{.interpreted-text role="pep"} - Simple Generators

:   The proposal for adding generators and the `yield`{.interpreted-text role="keyword"} statement to Python.

`342`{.interpreted-text role="pep"} - Coroutines via Enhanced Generators

:   The proposal to enhance the API and syntax of generators, making them usable as simple coroutines.

`380`{.interpreted-text role="pep"} - Syntax for Delegating to a Subgenerator

:   The proposal to introduce the `~python-grammar:yield_from`{.interpreted-text role="token"} syntax, making delegation to subgenerators easy.

`525`{.interpreted-text role="pep"} - Asynchronous Generators

:   The proposal that expanded on `492`{.interpreted-text role="pep"} by adding generator capabilities to coroutine functions.
:::

::: index
pair: object; generator
:::

#### Generator-iterator methods {#generator-methods}

This subsection describes the methods of a generator iterator. They can be used to control the execution of a generator function.

Note that calling any of the generator methods below when the generator is already executing raises a `ValueError`{.interpreted-text role="exc"} exception.

::: index
pair: exception; StopIteration
:::

::: method
generator.\_\_next\_\_()

Starts the execution of a generator function or resumes it at the last executed yield expression. When a generator function is resumed with a `~generator.__next__`{.interpreted-text role="meth"} method, the current yield expression always evaluates to `None`{.interpreted-text role="const"}. The execution then continues to the next yield expression, where the generator is suspended again, and the value of the `~python-grammar:yield_list`{.interpreted-text role="token"} is returned to `__next__`{.interpreted-text role="meth"}\'s caller. If the generator exits without yielding another value, a `StopIteration`{.interpreted-text role="exc"} exception is raised.

This method is normally called implicitly, e.g. by a `for`{.interpreted-text role="keyword"} loop, or by the built-in `next`{.interpreted-text role="func"} function.
:::

::: method
generator.send(value)

Resumes the execution and \"sends\" a value into the generator function. The *value* argument becomes the result of the current yield expression. The `send`{.interpreted-text role="meth"} method returns the next value yielded by the generator, or raises `StopIteration`{.interpreted-text role="exc"} if the generator exits without yielding another value. When `send`{.interpreted-text role="meth"} is called to start the generator, it must be called with `None`{.interpreted-text role="const"} as the argument, because there is no yield expression that could receive the value.
:::

:::: method
generator.throw(value) generator.throw(type\[, value\[, traceback\]\])

Raises an exception at the point where the generator was paused, and returns the next value yielded by the generator function. If the generator exits without yielding another value, a `StopIteration`{.interpreted-text role="exc"} exception is raised. If the generator function does not catch the passed-in exception, or raises a different exception, then that exception propagates to the caller.

In typical use, this is called with a single exception instance similar to the way the `raise`{.interpreted-text role="keyword"} keyword is used.

For backwards compatibility, however, the second signature is supported, following a convention from older versions of Python. The *type* argument should be an exception class, and *value* should be an exception instance. If the *value* is not provided, the *type* constructor is called to get an instance. If *traceback* is provided, it is set on the exception, otherwise any existing `~BaseException.__traceback__`{.interpreted-text role="attr"} attribute stored in *value* may be cleared.

::: versionchanged
3.12

The second signature (type\[, value\[, traceback\]\]) is deprecated and may be removed in a future version of Python.
:::
::::

::: index
pair: exception; GeneratorExit
:::

:::: method
generator.close()

Raises a `GeneratorExit`{.interpreted-text role="exc"} exception at the point where the generator function was paused (equivalent to calling `throw(GeneratorExit)`). The exception is raised by the yield expression where the generator was paused. If the generator function catches the exception and returns a value, this value is returned from `close`{.interpreted-text role="meth"}. If the generator function is already closed, or raises `GeneratorExit`{.interpreted-text role="exc"} (by not catching the exception), `close`{.interpreted-text role="meth"} returns `None`{.interpreted-text role="const"}. If the generator yields a value, a `RuntimeError`{.interpreted-text role="exc"} is raised. If the generator raises any other exception, it is propagated to the caller. If the generator has already exited due to an exception or normal exit, `close`{.interpreted-text role="meth"} returns `None`{.interpreted-text role="const"} and has no other effect.

::: versionchanged
3.13

If a generator returns a value upon being closed, the value is returned by `close`{.interpreted-text role="meth"}.
:::
::::

::: index
single: yield; examples
:::

#### Examples

Here is a simple example that demonstrates the behavior of generators and generator functions:

    >>> def echo(value=None):
    ...     print("Execution starts when 'next()' is called for the first time.")
    ...     try:
    ...         while True:
    ...             try:
    ...                 value = (yield value)
    ...             except Exception as e:
    ...                 value = e
    ...     finally:
    ...         print("Don't forget to clean up when 'close()' is called.")
    ...
    >>> generator = echo(1)
    >>> print(next(generator))
    Execution starts when 'next()' is called for the first time.
    1
    >>> print(next(generator))
    None
    >>> print(generator.send(2))
    2
    >>> generator.throw(TypeError, "spam")
    TypeError('spam',)
    >>> generator.close()
    Don't forget to clean up when 'close()' is called.

For examples using `yield from`, see `pep-380`{.interpreted-text role="ref"} in \"What\'s New in Python.\"

#### Asynchronous generator functions

The presence of a yield expression in a function or method defined using `async def`{.interpreted-text role="keyword"} further defines the function as an `asynchronous generator`{.interpreted-text role="term"} function.

When an asynchronous generator function is called, it returns an asynchronous iterator known as an asynchronous generator object. That object then controls the execution of the generator function. An asynchronous generator object is typically used in an `async for`{.interpreted-text role="keyword"} statement in a coroutine function analogously to how a generator object would be used in a `for`{.interpreted-text role="keyword"} statement.

Calling one of the asynchronous generator\'s methods returns an `awaitable`{.interpreted-text role="term"} object, and the execution starts when this object is awaited on. At that time, the execution proceeds to the first yield expression, where it is suspended again, returning the value of `~python-grammar:yield_list`{.interpreted-text role="token"} to the awaiting coroutine. As with a generator, suspension means that all local state is retained, including the current bindings of local variables, the instruction pointer, the internal evaluation stack, and the state of any exception handling. When the execution is resumed by awaiting on the next object returned by the asynchronous generator\'s methods, the function can proceed exactly as if the yield expression were just another external call. The value of the yield expression after resuming depends on the method which resumed the execution. If `~agen.__anext__`{.interpreted-text role="meth"} is used then the result is `None`{.interpreted-text role="const"}. Otherwise, if `~agen.asend`{.interpreted-text role="meth"} is used, then the result will be the value passed in to that method.

If an asynchronous generator happens to exit early by `break`{.interpreted-text role="keyword"}, the caller task being cancelled, or other exceptions, the generator\'s async cleanup code will run and possibly raise exceptions or access context variables in an unexpected context\--perhaps after the lifetime of tasks it depends, or during the event loop shutdown when the async-generator garbage collection hook is called. To prevent this, the caller must explicitly close the async generator by calling `~agen.aclose`{.interpreted-text role="meth"} method to finalize the generator and ultimately detach it from the event loop.

In an asynchronous generator function, yield expressions are allowed anywhere in a `try`{.interpreted-text role="keyword"} construct. However, if an asynchronous generator is not resumed before it is finalized (by reaching a zero reference count or by being garbage collected), then a yield expression within a `!try`{.interpreted-text role="keyword"} construct could result in a failure to execute pending `finally`{.interpreted-text role="keyword"} clauses. In this case, it is the responsibility of the event loop or scheduler running the asynchronous generator to call the asynchronous generator-iterator\'s `~agen.aclose`{.interpreted-text role="meth"} method and run the resulting coroutine object, thus allowing any pending `!finally`{.interpreted-text role="keyword"} clauses to execute.

To take care of finalization upon event loop termination, an event loop should define a *finalizer* function which takes an asynchronous generator-iterator and presumably calls `~agen.aclose`{.interpreted-text role="meth"} and executes the coroutine. This *finalizer* may be registered by calling `sys.set_asyncgen_hooks`{.interpreted-text role="func"}. When first iterated over, an asynchronous generator-iterator will store the registered *finalizer* to be called upon finalization. For a reference example of a *finalizer* method see the implementation of `asyncio.Loop.shutdown_asyncgens` in `Lib/asyncio/base_events.py`{.interpreted-text role="source"}.

The expression `yield from <expr>` is a syntax error when used in an asynchronous generator function.

::: index
pair: object; asynchronous-generator
:::

#### Asynchronous generator-iterator methods {#asynchronous-generator-methods}

This subsection describes the methods of an asynchronous generator iterator, which are used to control the execution of a generator function.

::: index
pair: exception; StopAsyncIteration
:::

::: {.method async=""}
agen.\_\_anext\_\_()

Returns an awaitable which when run starts to execute the asynchronous generator or resumes it at the last executed yield expression. When an asynchronous generator function is resumed with an `~agen.__anext__`{.interpreted-text role="meth"} method, the current yield expression always evaluates to `None`{.interpreted-text role="const"} in the returned awaitable, which when run will continue to the next yield expression. The value of the `~python-grammar:yield_list`{.interpreted-text role="token"} of the yield expression is the value of the `StopIteration`{.interpreted-text role="exc"} exception raised by the completing coroutine. If the asynchronous generator exits without yielding another value, the awaitable instead raises a `StopAsyncIteration`{.interpreted-text role="exc"} exception, signalling that the asynchronous iteration has completed.

This method is normally called implicitly by a `async for`{.interpreted-text role="keyword"} loop.
:::

::: {.method async=""}
agen.asend(value)

Returns an awaitable which when run resumes the execution of the asynchronous generator. As with the `~generator.send`{.interpreted-text role="meth"} method for a generator, this \"sends\" a value into the asynchronous generator function, and the *value* argument becomes the result of the current yield expression. The awaitable returned by the `asend`{.interpreted-text role="meth"} method will return the next value yielded by the generator as the value of the raised `StopIteration`{.interpreted-text role="exc"}, or raises `StopAsyncIteration`{.interpreted-text role="exc"} if the asynchronous generator exits without yielding another value. When `asend`{.interpreted-text role="meth"} is called to start the asynchronous generator, it must be called with `None`{.interpreted-text role="const"} as the argument, because there is no yield expression that could receive the value.
:::

:::: {.method async=""}
agen.athrow(value) agen.athrow(type\[, value\[, traceback\]\])

Returns an awaitable that raises an exception of type `type` at the point where the asynchronous generator was paused, and returns the next value yielded by the generator function as the value of the raised `StopIteration`{.interpreted-text role="exc"} exception. If the asynchronous generator exits without yielding another value, a `StopAsyncIteration`{.interpreted-text role="exc"} exception is raised by the awaitable. If the generator function does not catch the passed-in exception, or raises a different exception, then when the awaitable is run that exception propagates to the caller of the awaitable.

::: versionchanged
3.12

The second signature (type\[, value\[, traceback\]\]) is deprecated and may be removed in a future version of Python.
:::
::::

::: index
pair: exception; GeneratorExit
:::

::: {.method async=""}
agen.aclose()

Returns an awaitable that when run will throw a `GeneratorExit`{.interpreted-text role="exc"} into the asynchronous generator function at the point where it was paused. If the asynchronous generator function then exits gracefully, is already closed, or raises `GeneratorExit`{.interpreted-text role="exc"} (by not catching the exception), then the returned awaitable will raise a `StopIteration`{.interpreted-text role="exc"} exception. Any further awaitables returned by subsequent calls to the asynchronous generator will raise a `StopAsyncIteration`{.interpreted-text role="exc"} exception. If the asynchronous generator yields a value, a `RuntimeError`{.interpreted-text role="exc"} is raised by the awaitable. If the asynchronous generator raises any other exception, it is propagated to the caller of the awaitable. If the asynchronous generator has already exited due to an exception or normal exit, then further calls to `aclose`{.interpreted-text role="meth"} will return an awaitable that does nothing.
:::

## Primaries

::: index
single: primary
:::

Primaries represent the most tightly bound operations of the language. Their syntax is:

::: productionlist
python-grammar primary: [atom]{.title-ref} \| [attributeref]{.title-ref} \| [subscription]{.title-ref} \| [call]{.title-ref}
:::

### Attribute references

::: index
pair: attribute; reference single: . (dot); attribute reference
:::

An attribute reference is a primary followed by a period and a name:

::: productionlist
python-grammar attributeref: [primary]{.title-ref} \".\" [identifier]{.title-ref}
:::

::: index
pair: exception; AttributeError pair: object; module pair: object; list
:::

The primary must evaluate to an object of a type that supports attribute references, which most objects do. This object is then asked to produce the attribute whose name is the identifier. The type and value produced is determined by the object. Multiple evaluations of the same attribute reference may yield different objects.

This production can be customized by overriding the `~object.__getattribute__`{.interpreted-text role="meth"} method or the `~object.__getattr__`{.interpreted-text role="meth"} method. The `!__getattribute__`{.interpreted-text role="meth"} method is called first and either returns a value or raises `AttributeError`{.interpreted-text role="exc"} if the attribute is not available.

If an `AttributeError`{.interpreted-text role="exc"} is raised and the object has a `!__getattr__`{.interpreted-text role="meth"} method, that method is called as a fallback.

### Subscriptions and slicings {#subscriptions}

::: index
single: subscription single: \[\] (square brackets); subscription
:::

::: index
pair: object; sequence pair: object; mapping pair: object; string pair: object; tuple pair: object; list pair: object; dictionary pair: sequence; item
:::

The `subscription`{.interpreted-text role="dfn"} syntax is usually used for selecting an element from a `container <sequence-types>`{.interpreted-text role="ref"} \-- for example, to get a value from a `dict`{.interpreted-text role="class"}:

    >>> digits_by_name = {'one': 1, 'two': 2}
    >>> digits_by_name['two']  # Subscripting a dictionary using the key 'two'
    2

In the subscription syntax, the object being subscribed \-- a `primary <primaries>`{.interpreted-text role="ref"} \-- is followed by a `subscript`{.interpreted-text role="dfn"} in square brackets. In the simplest case, the subscript is a single expression.

Depending on the type of the object being subscribed, the subscript is sometimes called a `key`{.interpreted-text role="term"} (for mappings), `index`{.interpreted-text role="term"} (for sequences), or *type argument* (for `generic types <generic type>`{.interpreted-text role="term"}). Syntactically, these are all equivalent:

    >>> colors = ['red', 'blue', 'green', 'black']
    >>> colors[3]  # Subscripting a list using the index 3
    'black'

    >>> list[str]  # Parameterizing the list type using the type argument str
    list[str]

At runtime, the interpreter will evaluate the primary and the subscript, and call the primary\'s `~object.__getitem__`{.interpreted-text role="meth"} or `~object.__class_getitem__`{.interpreted-text role="meth"} `special method`{.interpreted-text role="term"} with the subscript as argument. For more details on which of these methods is called, see `classgetitem-versus-getitem`{.interpreted-text role="ref"}.

To show how subscription works, we can define a custom object that implements `~object.__getitem__`{.interpreted-text role="meth"} and prints out the value of the subscript:

    >>> class SubscriptionDemo:
    ...     def __getitem__(self, key):
    ...         print(f'subscripted with: {key!r}')
    ...
    >>> demo = SubscriptionDemo()
    >>> demo[1]
    subscripted with: 1
    >>> demo['a' * 3]
    subscripted with: 'aaa'

See `~object.__getitem__`{.interpreted-text role="meth"} documentation for how built-in types handle subscription.

Subscriptions may also be used as targets in `assignment <assignment>`{.interpreted-text role="ref"} or `deletion <del>`{.interpreted-text role="ref"} statements. In these cases, the interpreter will call the subscripted object\'s `~object.__setitem__`{.interpreted-text role="meth"} or `~object.__delitem__`{.interpreted-text role="meth"} `special method`{.interpreted-text role="term"}, respectively, instead of `~object.__getitem__`{.interpreted-text role="meth"}.

``` 
>>> colors = ['red', 'blue', 'green', 'black']
>>> colors[3] = 'white'  # Setting item at index
>>> colors
['red', 'blue', 'green', 'white']
>>> del colors[3]  # Deleting item at index 3
>>> colors
['red', 'blue', 'green']
```

All advanced forms of *subscript* documented in the following sections are also usable for assignment and deletion.

::: index
single: slicing single: slice single: : (colon); slicing single: , (comma); slicing
:::

::: index
pair: object; sequence pair: object; string pair: object; tuple pair: object; list
:::

#### Slicings

A more advanced form of subscription, `slicing`{.interpreted-text role="dfn"}, is commonly used to extract a portion of a `sequence <datamodel-sequences>`{.interpreted-text role="ref"}. In this form, the subscript is a `slice`{.interpreted-text role="term"}: up to three expressions separated by colons. Any of the expressions may be omitted, but a slice must contain at least one colon:

    >>> number_names = ['zero', 'one', 'two', 'three', 'four', 'five']
    >>> number_names[1:3]
    ['one', 'two']
    >>> number_names[1:]
    ['one', 'two', 'three', 'four', 'five']
    >>> number_names[:3]
    ['zero', 'one', 'two']
    >>> number_names[:]
    ['zero', 'one', 'two', 'three', 'four', 'five']
    >>> number_names[::2]
    ['zero', 'two', 'four']
    >>> number_names[:-3]
    ['zero', 'one', 'two']
    >>> del number_names[4:]
    >>> number_names
    ['zero', 'one', 'two', 'three']

When a slice is evaluated, the interpreter constructs a `slice`{.interpreted-text role="class"} object whose `~slice.start`{.interpreted-text role="attr"}, `~slice.stop`{.interpreted-text role="attr"} and `~slice.step`{.interpreted-text role="attr"} attributes, respectively, are the results of the expressions between the colons. Any missing expression evaluates to `None`{.interpreted-text role="const"}. This `!slice`{.interpreted-text role="class"} object is then passed to the `~object.__getitem__`{.interpreted-text role="meth"} or `~object.__class_getitem__`{.interpreted-text role="meth"} `special method`{.interpreted-text role="term"}, as above. :

    # continuing with the SubscriptionDemo instance defined above:
    >>> demo[2:3]
    subscripted with: slice(2, 3, None)
    >>> demo[::'spam']
    subscripted with: slice(None, None, 'spam')

#### Comma-separated subscripts

The subscript can also be given as two or more comma-separated expressions or slices:

    # continuing with the SubscriptionDemo instance defined above:
    >>> demo[1, 2, 3]
    subscripted with: (1, 2, 3)
    >>> demo[1:2, 3]
    subscripted with: (slice(1, 2, None), 3)

This form is commonly used with numerical libraries for slicing multi-dimensional data. In this case, the interpreter constructs a `tuple`{.interpreted-text role="class"} of the results of the expressions or slices, and passes this tuple to the `~object.__getitem__`{.interpreted-text role="meth"} or `~object.__class_getitem__`{.interpreted-text role="meth"} `special method`{.interpreted-text role="term"}, as above.

The subscript may also be given as a single expression or slice followed by a comma, to specify a one-element tuple:

    >>> demo['spam',]
    subscripted with: ('spam',)

#### \"Starred\" subscriptions

::: versionadded
3.11 Expressions in *tuple_slices* may be starred. See `646`{.interpreted-text role="pep"}.
:::

The subscript can also contain a starred expression. In this case, the interpreter unpacks the result into a tuple, and passes this tuple to `~object.__getitem__`{.interpreted-text role="meth"} or `~object.__class_getitem__`{.interpreted-text role="meth"}:

    # continuing with the SubscriptionDemo instance defined above:
    >>> demo[*range(10)]
    subscripted with: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

Starred expressions may be combined with comma-separated expressions and slices:

    >>> demo['a', 'b', *range(3), 'c']
    subscripted with: ('a', 'b', 0, 1, 2, 'c')

#### Formal subscription grammar

::: {.grammar-snippet group="python-grammar"}
subscription: [primary]{.title-ref} \'\[\' [subscript]{.title-ref} \'\]\' subscript: [single_subscript]{.title-ref} \| [tuple_subscript]{.title-ref} single_subscript: [proper_slice]{.title-ref} \| [assignment_expression]{.title-ref} proper_slice: \[[expression]{.title-ref}\] \":\" \[[expression]{.title-ref}\] \[ \":\" \[[expression]{.title-ref}\] \] tuple_subscript: \',\'.([single_subscript]{.title-ref} \| [starred_expression]{.title-ref})+ \[\',\'\]
:::

Recall that the `|` operator `denotes ordered choice <notation>`{.interpreted-text role="ref"}. Specifically, in `!subscript`{.interpreted-text role="token"}, if both alternatives would match, the first (`!single_subscript`{.interpreted-text role="token"}) has priority.

::: index
pair: object; callable single: call single: argument; call semantics single: () (parentheses); call single: , (comma); argument list single: = (equals); in function calls
:::

### Calls

A call calls a callable object (e.g., a `function`{.interpreted-text role="term"}) with a possibly empty series of `arguments <argument>`{.interpreted-text role="term"}:

::: productionlist
python-grammar call: [primary]{.title-ref} \"(\" \[[argument_list]{.title-ref} \[\",\"\] \| [comprehension]{.title-ref}\] \")\" argument_list: [positional_arguments]{.title-ref} \[\",\" [starred_and_keywords]{.title-ref}\] : \[\",\" [keywords_arguments]{.title-ref}\] : \| [starred_and_keywords]{.title-ref} \[\",\" [keywords_arguments]{.title-ref}\] : \| [keywords_arguments]{.title-ref} positional_arguments: [positional_item]{.title-ref} (\",\" [positional_item]{.title-ref})\* positional_item: [assignment_expression]{.title-ref} \| \"\*\" [expression]{.title-ref} starred_and_keywords: (\"\*\" [expression]{.title-ref} \| [keyword_item]{.title-ref}) : (\",\" \"\*\" [expression]{.title-ref} \| \",\" [keyword_item]{.title-ref})\* keywords_arguments: ([keyword_item]{.title-ref} \| \"\*\*\" [expression]{.title-ref}) : (\",\" [keyword_item]{.title-ref} \| \",\" \"\*\*\" [expression]{.title-ref})\* keyword_item: [identifier]{.title-ref} \"=\" [expression]{.title-ref}
:::

An optional trailing comma may be present after the positional and keyword arguments but does not affect the semantics.

::: index
single: parameter; call semantics
:::

The primary must evaluate to a callable object (user-defined functions, built-in functions, methods of built-in objects, class objects, methods of class instances, and all objects having a `~object.__call__`{.interpreted-text role="meth"} method are callable). All argument expressions are evaluated before the call is attempted. Please refer to section `function`{.interpreted-text role="ref"} for the syntax of formal `parameter`{.interpreted-text role="term"} lists.

If keyword arguments are present, they are first converted to positional arguments, as follows. First, a list of unfilled slots is created for the formal parameters. If there are N positional arguments, they are placed in the first N slots. Next, for each keyword argument, the identifier is used to determine the corresponding slot (if the identifier is the same as the first formal parameter name, the first slot is used, and so on). If the slot is already filled, a `TypeError`{.interpreted-text role="exc"} exception is raised. Otherwise, the argument is placed in the slot, filling it (even if the expression is `None`, it fills the slot). When all arguments have been processed, the slots that are still unfilled are filled with the corresponding default value from the function definition. (Default values are calculated, once, when the function is defined; thus, a mutable object such as a list or dictionary used as default value will be shared by all calls that don\'t specify an argument value for the corresponding slot; this should usually be avoided.) If there are any unfilled slots for which no default value is specified, a `TypeError`{.interpreted-text role="exc"} exception is raised. Otherwise, the list of filled slots is used as the argument list for the call.

::: impl-detail
An implementation may provide built-in functions whose positional parameters do not have names, even if they are \'named\' for the purpose of documentation, and which therefore cannot be supplied by keyword. In CPython, this is the case for functions implemented in C that use `PyArg_ParseTuple`{.interpreted-text role="c:func"} to parse their arguments.
:::

If there are more positional arguments than there are formal parameter slots, a `TypeError`{.interpreted-text role="exc"} exception is raised, unless a formal parameter using the syntax `*identifier` is present; in this case, that formal parameter receives a tuple containing the excess positional arguments (or an empty tuple if there were no excess positional arguments).

If any keyword argument does not correspond to a formal parameter name, a `TypeError`{.interpreted-text role="exc"} exception is raised, unless a formal parameter using the syntax `**identifier` is present; in this case, that formal parameter receives a dictionary containing the excess keyword arguments (using the keywords as keys and the argument values as corresponding values), or a (new) empty dictionary if there were no excess keyword arguments.

::: index
single: \* (asterisk); in function calls single: unpacking; in function calls
:::

If the syntax `*expression` appears in the function call, `expression` must evaluate to an `iterable`{.interpreted-text role="term"}. Elements from these iterables are treated as if they were additional positional arguments. For the call `f(x1, x2, *y, x3, x4)`, if *y* evaluates to a sequence *y1*, \..., *yM*, this is equivalent to a call with M+4 positional arguments *x1*, *x2*, *y1*, \..., *yM*, *x3*, *x4*.

A consequence of this is that although the `*expression` syntax may appear *after* explicit keyword arguments, it is processed *before* the keyword arguments (and any `**expression` arguments \-- see below). So:

    >>> def f(a, b):
    ...     print(a, b)
    ...
    >>> f(b=1, *(2,))
    2 1
    >>> f(a=1, *(2,))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: f() got multiple values for keyword argument 'a'
    >>> f(1, *(2,))
    1 2

It is unusual for both keyword arguments and the `*expression` syntax to be used in the same call, so in practice this confusion does not often arise.

::: index
single: \*\*; in function calls
:::

If the syntax `**expression` appears in the function call, `expression` must evaluate to a `mapping`{.interpreted-text role="term"}, the contents of which are treated as additional keyword arguments. If a parameter matching a key has already been given a value (by an explicit keyword argument, or from another unpacking), a `TypeError`{.interpreted-text role="exc"} exception is raised.

When `**expression` is used, each key in this mapping must be a string. Each value from the mapping is assigned to the first formal parameter eligible for keyword assignment whose name is equal to the key. A key need not be a Python identifier (e.g. `"max-temp °F"` is acceptable, although it will not match any formal parameter that could be declared). If there is no match to a formal parameter the key-value pair is collected by the `**` parameter, if there is one, or if there is not, a `TypeError`{.interpreted-text role="exc"} exception is raised.

Formal parameters using the syntax `*identifier` or `**identifier` cannot be used as positional argument slots or as keyword argument names.

::: versionchanged
3.5 Function calls accept any number of `*` and `**` unpackings, positional arguments may follow iterable unpackings (`*`), and keyword arguments may follow dictionary unpackings (`**`). Originally proposed by `448`{.interpreted-text role="pep"}.
:::

A call always returns some value, possibly `None`, unless it raises an exception. How this value is computed depends on the type of the callable object.

If it is\-\--

a user-defined function:

:   ::: index
    pair: function; call triple: user-defined; function; call pair: object; user-defined function pair: object; function
    :::

    The code block for the function is executed, passing it the argument list. The first thing the code block will do is bind the formal parameters to the arguments; this is described in section `function`{.interpreted-text role="ref"}. When the code block executes a `return`{.interpreted-text role="keyword"} statement, this specifies the return value of the function call. If execution reaches the end of the code block without executing a `return`{.interpreted-text role="keyword"} statement, the return value is `None`.

a built-in function or method:

:   ::: index
    pair: function; call pair: built-in function; call pair: method; call pair: built-in method; call pair: object; built-in method pair: object; built-in function pair: object; method pair: object; function
    :::

    The result is up to the interpreter; see `built-in-funcs`{.interpreted-text role="ref"} for the descriptions of built-in functions and methods.

a class object:

:   ::: index
    pair: object; class pair: class object; call
    :::

    A new instance of that class is returned.

a class instance method:

:   ::: index
    pair: object; class instance pair: object; instance pair: class instance; call
    :::

    The corresponding user-defined function is called, with an argument list that is one longer than the argument list of the call: the instance becomes the first argument.

a class instance:

:   ::: index
    pair: instance; call single: \_\_call\_\_() (object method)
    :::

    The class must define a `~object.__call__`{.interpreted-text role="meth"} method; the effect is then the same as if that method was called.

::: index
pair: keyword; await
:::

## Await expression {#await}

Suspend the execution of `coroutine`{.interpreted-text role="term"} on an `awaitable`{.interpreted-text role="term"} object. Can only be used inside a `coroutine function`{.interpreted-text role="term"}.

::: productionlist
python-grammar await_expr: \"await\" [primary]{.title-ref}
:::

::: versionadded
3.5
:::

## The power operator {#power}

::: index
pair: power; operation pair: operator; \*\*
:::

The power operator binds more tightly than unary operators on its left; it binds less tightly than unary operators on its right. The syntax is:

::: productionlist
python-grammar power: ([await_expr]{.title-ref} \| [primary]{.title-ref}) \[\"\*\*\" [u_expr]{.title-ref}\]
:::

Thus, in an unparenthesized sequence of power and unary operators, the operators are evaluated from right to left (this does not constrain the evaluation order for the operands): `-1**2` results in `-1`.

The power operator has the same semantics as the built-in `pow`{.interpreted-text role="func"} function, when called with two arguments: it yields its left argument raised to the power of its right argument. Numeric arguments are first `converted to a common type <stdtypes-mixed-arithmetic>`{.interpreted-text role="ref"}, and the result is of that type.

For int operands, the result has the same type as the operands unless the second argument is negative; in that case, all arguments are converted to float and a float result is delivered. For example, `10**2` returns `100`, but `10**-2` returns `0.01`.

Raising `0.0` to a negative power results in a `ZeroDivisionError`{.interpreted-text role="exc"}. Raising a negative number to a fractional power results in a `complex`{.interpreted-text role="class"} number. (In earlier versions it raised a `ValueError`{.interpreted-text role="exc"}.)

This operation can be customized using the special `~object.__pow__`{.interpreted-text role="meth"} and `~object.__rpow__`{.interpreted-text role="meth"} methods.

## Unary arithmetic and bitwise operations {#unary}

::: index
triple: unary; arithmetic; operation triple: unary; bitwise; operation
:::

All unary arithmetic and bitwise operations have the same priority:

::: productionlist
python-grammar u_expr: [power]{.title-ref} \| \"-\" [u_expr]{.title-ref} \| \"+\" [u_expr]{.title-ref} \| \"\~\" [u_expr]{.title-ref}
:::

::: index
single: negation single: minus single: operator; - (minus) single: - (minus); unary operator
:::

The unary `-` (minus) operator yields the negation of its numeric argument; the operation can be overridden with the `~object.__neg__`{.interpreted-text role="meth"} special method.

::: index
single: plus single: operator; + (plus) single: + (plus); unary operator
:::

The unary `+` (plus) operator yields its numeric argument unchanged; the operation can be overridden with the `~object.__pos__`{.interpreted-text role="meth"} special method.

::: index
single: inversion pair: operator; \~ (tilde)
:::

The unary `~` (invert) operator yields the bitwise inversion of its integer argument. The bitwise inversion of `x` is defined as `-(x+1)`. It only applies to integral numbers or to custom objects that override the `~object.__invert__`{.interpreted-text role="meth"} special method.

::: index
pair: exception; TypeError
:::

In all three cases, if the argument does not have the proper type, a `TypeError`{.interpreted-text role="exc"} exception is raised.

## Binary arithmetic operations {#binary}

::: index
triple: binary; arithmetic; operation
:::

The binary arithmetic operations have the conventional priority levels. Note that some of these operations also apply to certain non-numeric types. Apart from the power operator, there are only two levels, one for multiplicative operators and one for additive operators:

::: productionlist
python-grammar m_expr: [u_expr]{.title-ref} \| [m_expr]{.title-ref} \"\*\" [u_expr]{.title-ref} \| [m_expr]{.title-ref} \"@\" [m_expr]{.title-ref} \| : [m_expr]{.title-ref} \"//\" [u_expr]{.title-ref} \| [m_expr]{.title-ref} \"/\" [u_expr]{.title-ref} \| : [m_expr]{.title-ref} \"%\" [u_expr]{.title-ref} a_expr: [m_expr]{.title-ref} \| [a_expr]{.title-ref} \"+\" [m_expr]{.title-ref} \| [a_expr]{.title-ref} \"-\" [m_expr]{.title-ref}
:::

::: index
single: multiplication pair: operator; \* (asterisk)
:::

The `*` (multiplication) operator yields the product of its arguments. The arguments must either both be numbers, or one argument must be an integer and the other must be a sequence. In the former case, the numbers are `converted to a common real type <stdtypes-mixed-arithmetic>`{.interpreted-text role="ref"} and then multiplied together. In the latter case, sequence repetition is performed; a negative repetition factor yields an empty sequence.

This operation can be customized using the special `~object.__mul__`{.interpreted-text role="meth"} and `~object.__rmul__`{.interpreted-text role="meth"} methods.

::: versionchanged
3.14 If only one operand is a complex number, the other operand is converted to a floating-point number.
:::

::: index
single: matrix multiplication pair: operator; @ (at)
:::

The `@` (at) operator is intended to be used for matrix multiplication. No builtin Python types implement this operator.

This operation can be customized using the special `~object.__matmul__`{.interpreted-text role="meth"} and `~object.__rmatmul__`{.interpreted-text role="meth"} methods.

::: versionadded
3.5
:::

::: index
pair: exception; ZeroDivisionError single: division pair: operator; / (slash) pair: operator; //
:::

The `/` (division) and `//` (floor division) operators yield the quotient of their arguments. The numeric arguments are first `converted to a common type <stdtypes-mixed-arithmetic>`{.interpreted-text role="ref"}. Division of integers yields a float, while floor division of integers results in an integer; the result is that of mathematical division with the \'floor\' function applied to the result. Division by zero raises the `ZeroDivisionError`{.interpreted-text role="exc"} exception.

The division operation can be customized using the special `~object.__truediv__`{.interpreted-text role="meth"} and `~object.__rtruediv__`{.interpreted-text role="meth"} methods. The floor division operation can be customized using the special `~object.__floordiv__`{.interpreted-text role="meth"} and `~object.__rfloordiv__`{.interpreted-text role="meth"} methods.

::: index
single: modulo pair: operator; % (percent)
:::

The `%` (modulo) operator yields the remainder from the division of the first argument by the second. The numeric arguments are first `converted to a common type <stdtypes-mixed-arithmetic>`{.interpreted-text role="ref"}. A zero right argument raises the `ZeroDivisionError`{.interpreted-text role="exc"} exception. The arguments may be floating-point numbers, e.g., `3.14%0.7` equals `0.34` (since `3.14` equals `4*0.7 + 0.34`.) The modulo operator always yields a result with the same sign as its second operand (or zero); the absolute value of the result is strictly smaller than the absolute value of the second operand [^1].

The floor division and modulo operators are connected by the following identity: `x == (x//y)*y + (x%y)`. Floor division and modulo are also connected with the built-in function `divmod`{.interpreted-text role="func"}: `divmod(x, y) == (x//y, x%y)`.[^2].

In addition to performing the modulo operation on numbers, the `%` operator is also overloaded by string objects to perform old-style string formatting (also known as interpolation). The syntax for string formatting is described in the Python Library Reference, section `old-string-formatting`{.interpreted-text role="ref"}.

The *modulo* operation can be customized using the special `~object.__mod__`{.interpreted-text role="meth"} and `~object.__rmod__`{.interpreted-text role="meth"} methods.

The floor division operator, the modulo operator, and the `divmod`{.interpreted-text role="func"} function are not defined for complex numbers. Instead, convert to a floating-point number using the `abs`{.interpreted-text role="func"} function if appropriate.

::: index
single: addition single: operator; + (plus) single: + (plus); binary operator
:::

The `+` (addition) operator yields the sum of its arguments. The arguments must either both be numbers or both be sequences of the same type. In the former case, the numbers are `converted to a common real type <stdtypes-mixed-arithmetic>`{.interpreted-text role="ref"} and then added together. In the latter case, the sequences are concatenated.

This operation can be customized using the special `~object.__add__`{.interpreted-text role="meth"} and `~object.__radd__`{.interpreted-text role="meth"} methods.

::: versionchanged
3.14 If only one operand is a complex number, the other operand is converted to a floating-point number.
:::

::: index
single: subtraction single: operator; - (minus) single: - (minus); binary operator
:::

The `-` (subtraction) operator yields the difference of its arguments. The numeric arguments are first `converted to a common real type <stdtypes-mixed-arithmetic>`{.interpreted-text role="ref"}.

This operation can be customized using the special `~object.__sub__`{.interpreted-text role="meth"} and `~object.__rsub__`{.interpreted-text role="meth"} methods.

::: versionchanged
3.14 If only one operand is a complex number, the other operand is converted to a floating-point number.
:::

## Shifting operations {#shifting}

::: index
pair: shifting; operation pair: operator; \<\< pair: operator; \>\>
:::

The shifting operations have lower priority than the arithmetic operations:

::: productionlist
python-grammar shift_expr: [a_expr]{.title-ref} \| [shift_expr]{.title-ref} (\"\<\<\" \| \"\>\>\") [a_expr]{.title-ref}
:::

These operators accept integers as arguments. They shift the first argument to the left or right by the number of bits given by the second argument.

The left shift operation can be customized using the special `~object.__lshift__`{.interpreted-text role="meth"} and `~object.__rlshift__`{.interpreted-text role="meth"} methods. The right shift operation can be customized using the special `~object.__rshift__`{.interpreted-text role="meth"} and `~object.__rrshift__`{.interpreted-text role="meth"} methods.

::: index
pair: exception; ValueError
:::

A right shift by *n* bits is defined as floor division by `pow(2,n)`. A left shift by *n* bits is defined as multiplication with `pow(2,n)`.

## Binary bitwise operations {#bitwise}

::: index
triple: binary; bitwise; operation
:::

Each of the three bitwise operations has a different priority level:

::: productionlist
python-grammar and_expr: [shift_expr]{.title-ref} \| [and_expr]{.title-ref} \"&\" [shift_expr]{.title-ref} xor_expr: [and_expr]{.title-ref} \| [xor_expr]{.title-ref} \"\^\" [and_expr]{.title-ref} or_expr: [xor_expr]{.title-ref} \| [or_expr]{.title-ref} \"\|\" [xor_expr]{.title-ref}
:::

::: index
pair: bitwise; and pair: operator; & (ampersand)
:::

The `&` operator yields the bitwise AND of its arguments, which must be integers or one of them must be a custom object overriding `~object.__and__`{.interpreted-text role="meth"} or `~object.__rand__`{.interpreted-text role="meth"} special methods.

::: index
pair: bitwise; xor pair: exclusive; or pair: operator; \^ (caret)
:::

The `^` operator yields the bitwise XOR (exclusive OR) of its arguments, which must be integers or one of them must be a custom object overriding `~object.__xor__`{.interpreted-text role="meth"} or `~object.__rxor__`{.interpreted-text role="meth"} special methods.

::: index
pair: bitwise; or pair: inclusive; or pair: operator; \| (vertical bar)
:::

The `|` operator yields the bitwise (inclusive) OR of its arguments, which must be integers or one of them must be a custom object overriding `~object.__or__`{.interpreted-text role="meth"} or `~object.__ror__`{.interpreted-text role="meth"} special methods.

## Comparisons

::: index
single: comparison pair: C; language pair: operator; \< (less) pair: operator; \> (greater) pair: operator; \<= pair: operator; \>= pair: operator; == pair: operator; !=
:::

Unlike C, all comparison operations in Python have the same priority, which is lower than that of any arithmetic, shifting or bitwise operation. Also unlike C, expressions like `a < b < c` have the interpretation that is conventional in mathematics:

::: productionlist
python-grammar comparison: [or_expr]{.title-ref} ([comp_operator]{.title-ref} [or_expr]{.title-ref})\* comp_operator: \"\<\" \| \"\>\" \| \"==\" \| \"\>=\" \| \"\<=\" \| \"!=\" : \| \"is\" \[\"not\"\] \| \[\"not\"\] \"in\"
:::

Comparisons yield boolean values: `True` or `False`. Custom `rich comparison methods`{.interpreted-text role="dfn"} may return non-boolean values. In this case Python will call `bool`{.interpreted-text role="func"} on such value in boolean contexts.

::: index
pair: chaining; comparisons
:::

Comparisons can be chained arbitrarily, e.g., `x < y <= z` is equivalent to `x < y and y <= z`, except that `y` is evaluated only once (but in both cases `z` is not evaluated at all when `x < y` is found to be false).

Formally, if *a*, *b*, *c*, \..., *y*, *z* are expressions and *op1*, *op2*, \..., *opN* are comparison operators, then `a op1 b op2 c ... y opN z` is equivalent to `a op1 b and b op2 c and ... y opN z`, except that each expression is evaluated at most once.

Note that `a op1 b op2 c` doesn\'t imply any kind of comparison between *a* and *c*, so that, e.g., `x < y > z` is perfectly legal (though perhaps not pretty).

### Value comparisons {#expressions-value-comparisons}

The operators `<`, `>`, `==`, `>=`, `<=`, and `!=` compare the values of two objects. The objects do not need to have the same type.

Chapter `objects`{.interpreted-text role="ref"} states that objects have a value (in addition to type and identity). The value of an object is a rather abstract notion in Python: For example, there is no canonical access method for an object\'s value. Also, there is no requirement that the value of an object should be constructed in a particular way, e.g. comprised of all its data attributes. Comparison operators implement a particular notion of what the value of an object is. One can think of them as defining the value of an object indirectly, by means of their comparison implementation.

Because all types are (direct or indirect) subtypes of `object`{.interpreted-text role="class"}, they inherit the default comparison behavior from `object`{.interpreted-text role="class"}. Types can customize their comparison behavior by implementing `rich comparison methods`{.interpreted-text role="dfn"} like `~object.__lt__`{.interpreted-text role="meth"}, described in `customization`{.interpreted-text role="ref"}.

The default behavior for equality comparison (`==` and `!=`) is based on the identity of the objects. Hence, equality comparison of instances with the same identity results in equality, and equality comparison of instances with different identities results in inequality. A motivation for this default behavior is the desire that all objects should be reflexive (i.e. `x is y` implies `x == y`).

A default order comparison (`<`, `>`, `<=`, and `>=`) is not provided; an attempt raises `TypeError`{.interpreted-text role="exc"}. A motivation for this default behavior is the lack of a similar invariant as for equality.

The behavior of the default equality comparison, that instances with different identities are always unequal, may be in contrast to what types will need that have a sensible definition of object value and value-based equality. Such types will need to customize their comparison behavior, and in fact, a number of built-in types have done that.

The following list describes the comparison behavior of the most important built-in types.

- Numbers of built-in numeric types (`typesnumeric`{.interpreted-text role="ref"}) and of the standard library types `fractions.Fraction`{.interpreted-text role="class"} and `decimal.Decimal`{.interpreted-text role="class"} can be compared within and across their types, with the restriction that complex numbers do not support order comparison. Within the limits of the types involved, they compare mathematically (algorithmically) correct without loss of precision.

  The not-a-number values `float('NaN')` and `decimal.Decimal('NaN')` are special. Any ordered comparison of a number to a not-a-number value is false. A counter-intuitive implication is that not-a-number values are not equal to themselves. For example, if `x = float('NaN')`, `3 < x`, `x < 3` and `x == x` are all false, while `x != x` is true. This behavior is compliant with IEEE 754.

- `None` and `NotImplemented`{.interpreted-text role="data"} are singletons. [PEP 8](http://www.python.org/dev/peps/pep-0008/ "PEP 8") advises that comparisons for singletons should always be done with `is` or `is not`, never the equality operators.

- Binary sequences (instances of `bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"}) can be compared within and across their types. They compare lexicographically using the numeric values of their elements.

- Strings (instances of `str`{.interpreted-text role="class"}) compare lexicographically using the numerical Unicode code points (the result of the built-in function `ord`{.interpreted-text role="func"}) of their characters.[^3]

  Strings and binary sequences cannot be directly compared.

- Sequences (instances of `tuple`{.interpreted-text role="class"}, `list`{.interpreted-text role="class"}, or `range`{.interpreted-text role="class"}) can be compared only within each of their types, with the restriction that ranges do not support order comparison. Equality comparison across these types results in inequality, and ordering comparison across these types raises `TypeError`{.interpreted-text role="exc"}.

  Sequences compare lexicographically using comparison of corresponding elements. The built-in containers typically assume identical objects are equal to themselves. That lets them bypass equality tests for identical objects to improve performance and to maintain their internal invariants.

  Lexicographical comparison between built-in collections works as follows:

  - For two collections to compare equal, they must be of the same type, have the same length, and each pair of corresponding elements must compare equal (for example, `[1,2] == (1,2)` is false because the type is not the same).
  - Collections that support order comparison are ordered the same as their first unequal elements (for example, `[1,2,x] <= [1,2,y]` has the same value as `x <= y`). If a corresponding element does not exist, the shorter collection is ordered first (for example, `[1,2] < [1,2,3]` is true).

- Mappings (instances of `dict`{.interpreted-text role="class"}) compare equal if and only if they have equal `(key, value)` pairs. Equality comparison of the keys and values enforces reflexivity.

  Order comparisons (`<`, `>`, `<=`, and `>=`) raise `TypeError`{.interpreted-text role="exc"}.

- Sets (instances of `set`{.interpreted-text role="class"} or `frozenset`{.interpreted-text role="class"}) can be compared within and across their types.

  They define order comparison operators to mean subset and superset tests. Those relations do not define total orderings (for example, the two sets `{1,2}` and `{2,3}` are not equal, nor subsets of one another, nor supersets of one another). Accordingly, sets are not appropriate arguments for functions which depend on total ordering (for example, `min`{.interpreted-text role="func"}, `max`{.interpreted-text role="func"}, and `sorted`{.interpreted-text role="func"} produce undefined results given a list of sets as inputs).

  Comparison of sets enforces reflexivity of its elements.

- Most other built-in types have no comparison methods implemented, so they inherit the default comparison behavior.

User-defined classes that customize their comparison behavior should follow some consistency rules, if possible:

- Equality comparison should be reflexive. In other words, identical objects should compare equal:

  > `x is y` implies `x == y`

- Comparison should be symmetric. In other words, the following expressions should have the same result:

  > `x == y` and `y == x`
  >
  > `x != y` and `y != x`
  >
  > `x < y` and `y > x`
  >
  > `x <= y` and `y >= x`

- Comparison should be transitive. The following (non-exhaustive) examples illustrate that:

  > `x > y and y > z` implies `x > z`
  >
  > `x < y and y <= z` implies `x < z`

- Inverse comparison should result in the boolean negation. In other words, the following expressions should have the same result:

  > `x == y` and `not x != y`
  >
  > `x < y` and `not x >= y` (for total ordering)
  >
  > `x > y` and `not x <= y` (for total ordering)

  The last two expressions apply to totally ordered collections (e.g. to sequences, but not to sets or mappings). See also the `~functools.total_ordering`{.interpreted-text role="func"} decorator.

- The `hash`{.interpreted-text role="func"} result should be consistent with equality. Objects that are equal should either have the same hash value, or be marked as unhashable.

Python does not enforce these consistency rules. In fact, the not-a-number values are an example for not following these rules.

### Membership test operations[]{#not in}[]{#in} {#membership-test-details}

The operators `in`{.interpreted-text role="keyword"} and `not in`{.interpreted-text role="keyword"} test for membership. `x in s` evaluates to `True` if *x* is a member of *s*, and `False` otherwise. `x not in s` returns the negation of `x in s`. All built-in sequences and set types support this as well as dictionary, for which `!in`{.interpreted-text role="keyword"} tests whether the dictionary has a given key. For container types such as list, tuple, set, frozenset, dict, or collections.deque, the expression `x in y` is equivalent to `any(x is e or x == e for e in y)`.

For the string and bytes types, `x in y` is `True` if and only if *x* is a substring of *y*. An equivalent test is `y.find(x) != -1`. Empty strings are always considered to be a substring of any other string, so `"" in "abc"` will return `True`.

For user-defined classes which define the `~object.__contains__`{.interpreted-text role="meth"} method, `x in y` returns `True` if `y.__contains__(x)` returns a true value, and `False` otherwise.

For user-defined classes which do not define `~object.__contains__`{.interpreted-text role="meth"} but do define `~object.__iter__`{.interpreted-text role="meth"}, `x in y` is `True` if some value `z`, for which the expression `x is z or x == z` is true, is produced while iterating over `y`. If an exception is raised during the iteration, it is as if `in`{.interpreted-text role="keyword"} raised that exception.

Lastly, the old-style iteration protocol is tried: if a class defines `~object.__getitem__`{.interpreted-text role="meth"}, `x in y` is `True` if and only if there is a non-negative integer index *i* such that `x is y[i] or x == y[i]`, and no lower integer index raises the `IndexError`{.interpreted-text role="exc"} exception. (If any other exception is raised, it is as if `in`{.interpreted-text role="keyword"} raised that exception).

::: index
pair: operator; in pair: operator; not in pair: membership; test pair: object; sequence
:::

The operator `not in`{.interpreted-text role="keyword"} is defined to have the inverse truth value of `in`{.interpreted-text role="keyword"}.

::: index
pair: operator; is pair: operator; is not pair: identity; test
:::

### Identity comparisons[]{#is} {#is not}

The operators `is`{.interpreted-text role="keyword"} and `is not`{.interpreted-text role="keyword"} test for an object\'s identity: `x is y` is true if and only if *x* and *y* are the same object. An Object\'s identity is determined using the `id`{.interpreted-text role="meth"} function. `x is not y` yields the inverse truth value.[^4]

## Boolean operations[]{#or}[]{#and}[]{#booleans} {#not}

::: index
pair: Conditional; expression pair: Boolean; operation
:::

::: productionlist
python-grammar or_test: [and_test]{.title-ref} \| [or_test]{.title-ref} \"or\" [and_test]{.title-ref} and_test: [not_test]{.title-ref} \| [and_test]{.title-ref} \"and\" [not_test]{.title-ref} not_test: [comparison]{.title-ref} \| \"not\" [not_test]{.title-ref}
:::

In the context of Boolean operations, and also when expressions are used by control flow statements, the following values are interpreted as false: `False`, `None`, numeric zero of all types, and empty strings and containers (including strings, tuples, lists, dictionaries, sets and frozensets). All other values are interpreted as true. User-defined objects can customize their truth value by providing a `~object.__bool__`{.interpreted-text role="meth"} method.

::: index
pair: operator; not
:::

The operator `not`{.interpreted-text role="keyword"} yields `True` if its argument is false, `False` otherwise.

::: index
pair: operator; and
:::

The expression `x and y` first evaluates *x*; if *x* is false, its value is returned; otherwise, *y* is evaluated and the resulting value is returned.

::: index
pair: operator; or
:::

The expression `x or y` first evaluates *x*; if *x* is true, its value is returned; otherwise, *y* is evaluated and the resulting value is returned.

Note that neither `and`{.interpreted-text role="keyword"} nor `or`{.interpreted-text role="keyword"} restrict the value and type they return to `False` and `True`, but rather return the last evaluated argument. This is sometimes useful, e.g., if `s` is a string that should be replaced by a default value if it is empty, the expression `s or 'foo'` yields the desired value. Because `not`{.interpreted-text role="keyword"} has to create a new value, it returns a boolean value regardless of the type of its argument (for example, `not 'foo'` produces `False` rather than `''`.)

::: index
single: := (colon equals) single: assignment expression single: walrus operator single: named expression pair: assignment; expression
:::

## Assignment expressions

::: productionlist
python-grammar assignment_expression: \[[identifier]{.title-ref} \":=\"\] [expression]{.title-ref}
:::

An assignment expression (sometimes also called a \"named expression\" or \"walrus\") assigns an `~python-grammar:expression`{.interpreted-text role="token"} to an `~python-grammar:identifier`{.interpreted-text role="token"}, while also returning the value of the `~python-grammar:expression`{.interpreted-text role="token"}.

One common use case is when handling matched regular expressions:

``` python
if matching := pattern.search(data):
    do_something(matching)
```

Or, when processing a file stream in chunks:

``` python
while chunk := file.read(9000):
    process(chunk)
```

Assignment expressions must be surrounded by parentheses when used as expression statements and when used as sub-expressions in slicing, conditional, lambda, keyword-argument, and comprehension-if expressions and in `assert`, `with`, and `assignment` statements. In all other places where they can be used, parentheses are not required, including in `if` and `while` statements.

::: versionadded
3.8 See `572`{.interpreted-text role="pep"} for more details about assignment expressions.
:::

## Conditional expressions {#if_expr}

::: index
pair: conditional; expression pair: ternary; operator single: if; conditional expression single: else; conditional expression
:::

::: productionlist
python-grammar conditional_expression: [or_test]{.title-ref} \[\"if\" [or_test]{.title-ref} \"else\" [expression]{.title-ref}\] expression: [conditional_expression]{.title-ref} \| [lambda_expr]{.title-ref}
:::

A conditional expression (sometimes called a \"ternary operator\") is an alternative to the if-else statement. As it is an expression, it returns a value and can appear as a sub-expression.

The expression `x if C else y` first evaluates the condition, *C* rather than *x*. If *C* is true, *x* is evaluated and its value is returned; otherwise, *y* is evaluated and its value is returned.

See `308`{.interpreted-text role="pep"} for more details about conditional expressions.

## Lambdas[]{#lambdas} {#lambda}

::: index
pair: lambda; expression pair: lambda; form pair: anonymous; function single: : (colon); lambda expression
:::

::: productionlist
python-grammar lambda_expr: \"lambda\" \[[parameter_list]{.title-ref}\] \":\" [expression]{.title-ref}
:::

Lambda expressions (sometimes called lambda forms) are used to create anonymous functions. The expression `lambda parameters: expression` yields a function object. The unnamed object behaves like a function object defined with:

``` none
def <lambda>(parameters):
    return expression
```

See section `function`{.interpreted-text role="ref"} for the syntax of parameter lists. Note that functions created with lambda expressions cannot contain statements or annotations.

## Expression lists {#exprlists}

::: index
pair: expression; list single: , (comma); expression list
:::

::: productionlist
python-grammar starred_expression: \"\*\" [or_expr]{.title-ref} \| [expression]{.title-ref} flexible_expression: [assignment_expression]{.title-ref} \| [starred_expression]{.title-ref} flexible_expression_list: [flexible_expression]{.title-ref} (\",\" [flexible_expression]{.title-ref})\* \[\",\"\] starred_expression_list: [starred_expression]{.title-ref} (\",\" [starred_expression]{.title-ref})\* \[\",\"\] expression_list: [expression]{.title-ref} (\",\" [expression]{.title-ref})\* \[\",\"\] yield_list: [expression_list]{.title-ref} \| [starred_expression]{.title-ref} \",\" \[[starred_expression_list]{.title-ref}\]
:::

::: index
pair: object; tuple
:::

Except when part of a list or set display, an expression list containing at least one comma yields a tuple. The length of the tuple is the number of expressions in the list. The expressions are evaluated from left to right.

::: index
pair: iterable; unpacking single: \* (asterisk); in expression lists
:::

An asterisk `*` denotes `iterable unpacking`{.interpreted-text role="dfn"}. Its operand must be an `iterable`{.interpreted-text role="term"}. The iterable is expanded into a sequence of items, which are included in the new tuple, list, or set, at the site of the unpacking.

::: versionadded
3.5 Iterable unpacking in expression lists, originally proposed by `448`{.interpreted-text role="pep"}.
:::

::: versionadded
3.11 Any item in an expression list may be starred. See `646`{.interpreted-text role="pep"}.
:::

::: index
pair: trailing; comma
:::

A trailing comma is required only to create a one-item tuple, such as `1,`; it is optional in all other cases. A single expression without a trailing comma doesn\'t create a tuple, but rather yields the value of that expression. (To create an empty tuple, use an empty pair of parentheses: `()`.)

## Evaluation order {#evalorder}

::: index
pair: evaluation; order
:::

Python evaluates expressions from left to right. Notice that while evaluating an assignment, the right-hand side is evaluated before the left-hand side.

In the following lines, expressions will be evaluated in the arithmetic order of their suffixes:

    expr1, expr2, expr3, expr4
    (expr1, expr2, expr3, expr4)
    {expr1: expr2, expr3: expr4}
    expr1 + expr2 * (expr3 - expr4)
    expr1(expr2, expr3, *expr4, **expr5)
    expr3, expr4 = expr1, expr2

## Operator precedence {#operator-summary}

::: index
pair: operator; precedence
:::

The following table summarizes the operator precedence in Python, from highest precedence (most binding) to lowest precedence (least binding). Operators in the same box have the same precedence. Unless the syntax is explicitly given, operators are binary. Operators in the same box group left to right (except for exponentiation and conditional expressions, which group from right to left).

Note that comparisons, membership tests, and identity tests, all have the same precedence and have a left-to-right chaining feature as described in the `comparisons`{.interpreted-text role="ref"} section.

+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| Operator                                                                                                                                                                                                 | Description                                                                        |
+==========================================================================================================================================================================================================+====================================================================================+
| `(expressions...)`,                                                                                                                                                                                      | Binding or parenthesized expression, list display, dictionary display, set display |
|                                                                                                                                                                                                          |                                                                                    |
| `[expressions...]`, `{key: value...}`, `{expressions...}`                                                                                                                                                |                                                                                    |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `x[index]`, `x[index:index]` `x(arguments...)`, `x.attribute`                                                                                                                                            | Subscription (including slicing), call, attribute reference                        |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `await x <await>`{.interpreted-text role="keyword"}                                                                                                                                                      | Await expression                                                                   |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `**`                                                                                                                                                                                                     | Exponentiation[^5]                                                                 |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `+x`, `-x`, `~x`                                                                                                                                                                                         | Positive, negative, bitwise NOT                                                    |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `*`, `@`, `/`, `//`, `%`                                                                                                                                                                                 | Multiplication, matrix multiplication, division, floor division, remainder[^6]     |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `+`, `-`                                                                                                                                                                                                 | Addition and subtraction                                                           |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `<<`, `>>`                                                                                                                                                                                               | Shifts                                                                             |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `&`                                                                                                                                                                                                      | Bitwise AND                                                                        |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `^`                                                                                                                                                                                                      | Bitwise XOR                                                                        |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `|`                                                                                                                                                                                                      | Bitwise OR                                                                         |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `in`{.interpreted-text role="keyword"}, `not in`{.interpreted-text role="keyword"}, `is`{.interpreted-text role="keyword"}, `is not`{.interpreted-text role="keyword"}, `<`, `<=`, `>`, `>=`, `!=`, `==` | Comparisons, including membership tests and identity tests                         |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `not x <not>`{.interpreted-text role="keyword"}                                                                                                                                                          | Boolean NOT                                                                        |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `and`{.interpreted-text role="keyword"}                                                                                                                                                                  | Boolean AND                                                                        |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `or`{.interpreted-text role="keyword"}                                                                                                                                                                   | Boolean OR                                                                         |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `if <if_expr>`{.interpreted-text role="keyword"} \-- `!else`{.interpreted-text role="keyword"}                                                                                                           | Conditional expression                                                             |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `lambda`{.interpreted-text role="keyword"}                                                                                                                                                               | Lambda expression                                                                  |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| `:=`                                                                                                                                                                                                     | Assignment expression                                                              |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+

**Footnotes**

[^1]: While `abs(x%y) < abs(y)` is true mathematically, for floats it may not be true numerically due to roundoff. For example, and assuming a platform on which a Python float is an IEEE 754 double-precision number, in order that `-1e-100 % 1e100` have the same sign as `1e100`, the computed result is `-1e-100 + 1e100`, which is numerically exactly equal to `1e100`. The function `math.fmod`{.interpreted-text role="func"} returns a result whose sign matches the sign of the first argument instead, and so returns `-1e-100` in this case. Which approach is more appropriate depends on the application.

[^2]: If x is very close to an exact integer multiple of y, it\'s possible for `x//y` to be one larger than `(x-x%y)//y` due to rounding. In such cases, Python returns the latter result, in order to preserve that `divmod(x,y)[0] * y + x % y` be very close to `x`.

[^3]: The Unicode standard distinguishes between `code points`{.interpreted-text role="dfn"} (e.g. U+0041) and `abstract characters`{.interpreted-text role="dfn"} (e.g. \"LATIN CAPITAL LETTER A\"). While most abstract characters in Unicode are only represented using one code point, there is a number of abstract characters that can in addition be represented using a sequence of more than one code point. For example, the abstract character \"LATIN CAPITAL LETTER C WITH CEDILLA\" can be represented as a single `precomposed character`{.interpreted-text role="dfn"} at code position U+00C7, or as a sequence of a `base character`{.interpreted-text role="dfn"} at code position U+0043 (LATIN CAPITAL LETTER C), followed by a `combining character`{.interpreted-text role="dfn"} at code position U+0327 (COMBINING CEDILLA).

    The comparison operators on strings compare at the level of Unicode code points. This may be counter-intuitive to humans. For example, `"\u00C7" == "\u0043\u0327"` is `False`, even though both strings represent the same abstract character \"LATIN CAPITAL LETTER C WITH CEDILLA\".

    To compare strings at the level of abstract characters (that is, in a way intuitive to humans), use `unicodedata.normalize`{.interpreted-text role="func"}.

[^4]: Due to automatic garbage-collection, free lists, and the dynamic nature of descriptors, you may notice seemingly unusual behaviour in certain uses of the `is`{.interpreted-text role="keyword"} operator, like those involving comparisons between instance methods, or constants. Check their documentation for more info.

[^5]: The power operator `**` binds less tightly than an arithmetic or bitwise unary operator on its right, that is, `2**-1` is `0.5`.

[^6]: The `%` operator is also used for string formatting; the same precedence applies.
