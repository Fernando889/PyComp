# Compound statements {#compound}

::: index
pair: compound; statement
:::

Compound statements contain (groups of) other statements; they affect or control the execution of those other statements in some way. In general, compound statements span multiple lines, although in simple incarnations a whole compound statement may be contained in one line.

The `if`{.interpreted-text role="keyword"}, `while`{.interpreted-text role="keyword"} and `for`{.interpreted-text role="keyword"} statements implement traditional control flow constructs. `try`{.interpreted-text role="keyword"} specifies exception handlers and/or cleanup code for a group of statements, while the `with`{.interpreted-text role="keyword"} statement allows the execution of initialization and finalization code around a block of code. Function and class definitions are also syntactically compound statements.

::: index
single: clause single: suite single: ; (semicolon)
:::

A compound statement consists of one or more \'clauses.\' A clause consists of a header and a \'suite.\' The clause headers of a particular compound statement are all at the same indentation level. Each clause header begins with a uniquely identifying keyword and ends with a colon. A suite is a group of statements controlled by a clause. A suite can be one or more semicolon-separated simple statements on the same line as the header, following the header\'s colon, or it can be one or more indented statements on subsequent lines. Only the latter form of a suite can contain nested compound statements; the following is illegal, mostly because it wouldn\'t be clear to which `if`{.interpreted-text role="keyword"} clause a following `else`{.interpreted-text role="keyword"} clause would belong:

    if test1: if test2: print(x)

Also note that the semicolon binds tighter than the colon in this context, so that in the following example, either all or none of the `print`{.interpreted-text role="func"} calls are executed:

    if x < y < z: print(x); print(y); print(z)

Summarizing:

::: productionlist
python-grammar compound_stmt: [if_stmt]{.title-ref} : \| [while_stmt]{.title-ref} : \| [for_stmt]{.title-ref} : \| [try_stmt]{.title-ref} : \| [with_stmt]{.title-ref} : \| [match_stmt]{.title-ref} : \| [funcdef]{.title-ref} : \| [classdef]{.title-ref} : \| [async_with_stmt]{.title-ref} : \| [async_for_stmt]{.title-ref} : \| [async_funcdef]{.title-ref} suite: [stmt_list]{.title-ref} NEWLINE \| NEWLINE INDENT [statement]{.title-ref}+ DEDENT statement: [stmt_list]{.title-ref} NEWLINE \| [compound_stmt]{.title-ref} stmt_list: [simple_stmt]{.title-ref} (\";\" [simple_stmt]{.title-ref})\* \[\";\"\]
:::

::: index
single: NEWLINE token single: DEDENT token pair: dangling; else
:::

Note that statements always end in a `NEWLINE` possibly followed by a `DEDENT`. Also note that optional continuation clauses always begin with a keyword that cannot start a statement, thus there are no ambiguities (the \'dangling `else`{.interpreted-text role="keyword"}\' problem is solved in Python by requiring nested `if`{.interpreted-text role="keyword"} statements to be indented).

The formatting of the grammar rules in the following sections places each clause on a separate line for clarity.

## The `!if`{.interpreted-text role="keyword"} statement[]{#elif}[]{#if} {#else}

::: index
! pair: statement; if pair: keyword; elif pair: keyword; else single: : (colon); compound statement
:::

The `if`{.interpreted-text role="keyword"} statement is used for conditional execution:

::: productionlist
python-grammar if_stmt: \"if\" [assignment_expression]{.title-ref} \":\" [suite]{.title-ref} : (\"elif\" [assignment_expression]{.title-ref} \":\" [suite]{.title-ref})\* : \[\"else\" \":\" [suite]{.title-ref}\]
:::

It selects exactly one of the suites by evaluating the expressions one by one until one is found to be true (see section `booleans`{.interpreted-text role="ref"} for the definition of true and false); then that suite is executed (and no other part of the `if`{.interpreted-text role="keyword"} statement is executed or evaluated). If all expressions are false, the suite of the `else`{.interpreted-text role="keyword"} clause, if present, is executed.

## The `!while`{.interpreted-text role="keyword"} statement {#while}

::: index
! pair: statement; while pair: keyword; else pair: loop; statement single: : (colon); compound statement
:::

The `while`{.interpreted-text role="keyword"} statement is used for repeated execution as long as an expression is true:

::: productionlist
python-grammar while_stmt: \"while\" [assignment_expression]{.title-ref} \":\" [suite]{.title-ref} : \[\"else\" \":\" [suite]{.title-ref}\]
:::

This repeatedly tests the expression and, if it is true, executes the first suite; if the expression is false (which may be the first time it is tested) the suite of the `!else`{.interpreted-text role="keyword"} clause, if present, is executed and the loop terminates.

::: index
pair: statement; break pair: statement; continue
:::

A `break`{.interpreted-text role="keyword"} statement executed in the first suite terminates the loop without executing the `!else`{.interpreted-text role="keyword"} clause\'s suite. A `continue`{.interpreted-text role="keyword"} statement executed in the first suite skips the rest of the suite and goes back to testing the expression.

## The `!for`{.interpreted-text role="keyword"} statement {#for}

::: index
! pair: statement; for pair: keyword; in pair: keyword; else pair: target; list pair: loop; statement pair: object; sequence single: : (colon); compound statement
:::

The `for`{.interpreted-text role="keyword"} statement is used to iterate over the elements of a sequence (such as a string, tuple or list) or other iterable object:

::: productionlist
python-grammar for_stmt: \"for\" [target_list]{.title-ref} \"in\" [starred_expression_list]{.title-ref} \":\" [suite]{.title-ref} : \[\"else\" \":\" [suite]{.title-ref}\]
:::

The `~python-grammar:starred_expression_list`{.interpreted-text role="token"} expression is evaluated once; it should yield an `iterable`{.interpreted-text role="term"} object. An `iterator`{.interpreted-text role="term"} is created for that iterable. The first item provided by the iterator is then assigned to the target list using the standard rules for assignments (see `assignment`{.interpreted-text role="ref"}), and the suite is executed. This repeats for each item provided by the iterator. When the iterator is exhausted, the suite in the `!else`{.interpreted-text role="keyword"} clause, if present, is executed, and the loop terminates.

::: index
pair: statement; break pair: statement; continue
:::

A `break`{.interpreted-text role="keyword"} statement executed in the first suite terminates the loop without executing the `!else`{.interpreted-text role="keyword"} clause\'s suite. A `continue`{.interpreted-text role="keyword"} statement executed in the first suite skips the rest of the suite and continues with the next item, or with the `!else`{.interpreted-text role="keyword"} clause if there is no next item.

The for-loop makes assignments to the variables in the target list. This overwrites all previous assignments to those variables including those made in the suite of the for-loop:

    for i in range(10):
        print(i)
        i = 5             # this will not affect the for-loop
                          # because i will be overwritten with the next
                          # index in the range

::: index
pair: built-in function; range
:::

Names in the target list are not deleted when the loop is finished, but if the sequence is empty, they will not have been assigned to at all by the loop. Hint: the built-in type `range`{.interpreted-text role="func"} represents immutable arithmetic sequences of integers. For instance, iterating `range(3)` successively yields 0, 1, and then 2.

::: versionchanged
3.11 Starred elements are now allowed in the expression list.
:::

## The `!try`{.interpreted-text role="keyword"} statement {#try}

::: index
! pair: statement; try pair: keyword; except pair: keyword; finally pair: keyword; else pair: keyword; as single: : (colon); compound statement
:::

The `!try`{.interpreted-text role="keyword"} statement specifies exception handlers and/or cleanup code for a group of statements:

::: productionlist
python-grammar try_stmt: [try1_stmt]{.title-ref} \| [try2_stmt]{.title-ref} \| [try3_stmt]{.title-ref} try1_stmt: \"try\" \":\" [suite]{.title-ref} : (\"except\" \[[expression]{.title-ref} \[\"as\" [identifier]{.title-ref}\]\] \":\" [suite]{.title-ref})+ : \[\"else\" \":\" [suite]{.title-ref}\] : \[\"finally\" \":\" [suite]{.title-ref}\] try2_stmt: \"try\" \":\" [suite]{.title-ref} : (\"except\" \"\*\" [expression]{.title-ref} \[\"as\" [identifier]{.title-ref}\] \":\" [suite]{.title-ref})+ : \[\"else\" \":\" [suite]{.title-ref}\] : \[\"finally\" \":\" [suite]{.title-ref}\] try3_stmt: \"try\" \":\" [suite]{.title-ref} : \"finally\" \":\" [suite]{.title-ref}
:::

Additional information on exceptions can be found in section `exceptions`{.interpreted-text role="ref"}, and information on using the `raise`{.interpreted-text role="keyword"} statement to generate exceptions may be found in section `raise`{.interpreted-text role="ref"}.

::: versionchanged
3.14 Support for optionally dropping grouping parentheses when using multiple exception types. See `758`{.interpreted-text role="pep"}.
:::

### `!except`{.interpreted-text role="keyword"} clause {#except}

The `!except`{.interpreted-text role="keyword"} clause(s) specify one or more exception handlers. When no exception occurs in the `try`{.interpreted-text role="keyword"} clause, no exception handler is executed. When an exception occurs in the `!try`{.interpreted-text role="keyword"} suite, a search for an exception handler is started. This search inspects the `!except`{.interpreted-text role="keyword"} clauses in turn until one is found that matches the exception. An expression-less `!except`{.interpreted-text role="keyword"} clause, if present, must be last; it matches any exception.

For an `!except`{.interpreted-text role="keyword"} clause with an expression, the expression must evaluate to an exception type or a tuple of exception types. Parentheses can be dropped if multiple exception types are provided and the `as` clause is not used. The raised exception matches an `!except`{.interpreted-text role="keyword"} clause whose expression evaluates to the class or a `non-virtual base class <abstract base class>`{.interpreted-text role="term"} of the exception object, or to a tuple that contains such a class.

If no `!except`{.interpreted-text role="keyword"} clause matches the exception, the search for an exception handler continues in the surrounding code and on the invocation stack.[^1]

If the evaluation of an expression in the header of an `!except`{.interpreted-text role="keyword"} clause raises an exception, the original search for a handler is canceled and a search starts for the new exception in the surrounding code and on the call stack (it is treated as if the entire `try`{.interpreted-text role="keyword"} statement raised the exception).

::: index
single: as; except clause
:::

When a matching `!except`{.interpreted-text role="keyword"} clause is found, the exception is assigned to the target specified after the `!as`{.interpreted-text role="keyword"} keyword in that `!except`{.interpreted-text role="keyword"} clause, if present, and the `!except`{.interpreted-text role="keyword"} clause\'s suite is executed. All `!except`{.interpreted-text role="keyword"} clauses must have an executable block. When the end of this block is reached, execution continues normally after the entire `try`{.interpreted-text role="keyword"} statement. (This means that if two nested handlers exist for the same exception, and the exception occurs in the `!try`{.interpreted-text role="keyword"} clause of the inner handler, the outer handler will not handle the exception.)

When an exception has been assigned using `as target`, it is cleared at the end of the `!except`{.interpreted-text role="keyword"} clause. This is as if :

    except E as N:
        foo

was translated to :

    except E as N:
        try:
            foo
        finally:
            del N

This means the exception must be assigned to a different name to be able to refer to it after the `!except`{.interpreted-text role="keyword"} clause. Exceptions are cleared because with the traceback attached to them, they form a reference cycle with the stack frame, keeping all locals in that frame alive until the next garbage collection occurs.

::: index
pair: module; sys pair: object; traceback
:::

Before an `!except`{.interpreted-text role="keyword"} clause\'s suite is executed, the exception is stored in the `sys`{.interpreted-text role="mod"} module, where it can be accessed from within the body of the `!except`{.interpreted-text role="keyword"} clause by calling `sys.exception`{.interpreted-text role="func"}. When leaving an exception handler, the exception stored in the `sys`{.interpreted-text role="mod"} module is reset to its previous value:

    >>> print(sys.exception())
    None
    >>> try:
    ...     raise TypeError
    ... except:
    ...     print(repr(sys.exception()))
    ...     try:
    ...          raise ValueError
    ...     except:
    ...         print(repr(sys.exception()))
    ...     print(repr(sys.exception()))
    ...
    TypeError()
    ValueError()
    TypeError()
    >>> print(sys.exception())
    None

::: index
pair: keyword; except_star
:::

### `!except*`{.interpreted-text role="keyword"} clause {#except_star}

The `!except*`{.interpreted-text role="keyword"} clause(s) specify one or more handlers for groups of exceptions (`BaseExceptionGroup`{.interpreted-text role="exc"} instances). A `try`{.interpreted-text role="keyword"} statement can have either `except`{.interpreted-text role="keyword"} or `!except*`{.interpreted-text role="keyword"} clauses, but not both. The exception type for matching is mandatory in the case of `!except*`{.interpreted-text role="keyword"}, so `except*:` is a syntax error. The type is interpreted as in the case of `!except`{.interpreted-text role="keyword"}, but matching is performed on the exceptions contained in the group that is being handled. An `TypeError`{.interpreted-text role="exc"} is raised if a matching type is a subclass of `!BaseExceptionGroup`{.interpreted-text role="exc"}, because that would have ambiguous semantics.

When an exception group is raised in the try block, each `!except*`{.interpreted-text role="keyword"} clause splits (see `~BaseExceptionGroup.split`{.interpreted-text role="meth"}) it into the subgroups of matching and non-matching exceptions. If the matching subgroup is not empty, it becomes the handled exception (the value returned from `sys.exception`{.interpreted-text role="func"}) and assigned to the target of the `!except*`{.interpreted-text role="keyword"} clause (if there is one). Then, the body of the `!except*`{.interpreted-text role="keyword"} clause executes. If the non-matching subgroup is not empty, it is processed by the next `!except*`{.interpreted-text role="keyword"} in the same manner. This continues until all exceptions in the group have been matched, or the last `!except*`{.interpreted-text role="keyword"} clause has run.

After all `!except*`{.interpreted-text role="keyword"} clauses execute, the group of unhandled exceptions is merged with any exceptions that were raised or re-raised from within `!except*`{.interpreted-text role="keyword"} clauses. This merged exception group propagates on.:

    >>> try:
    ...     raise ExceptionGroup("eg",
    ...         [ValueError(1), TypeError(2), OSError(3), OSError(4)])
    ... except* TypeError as e:
    ...     print(f'caught {type(e)} with nested {e.exceptions}')
    ... except* OSError as e:
    ...     print(f'caught {type(e)} with nested {e.exceptions}')
    ...
    caught <class 'ExceptionGroup'> with nested (TypeError(2),)
    caught <class 'ExceptionGroup'> with nested (OSError(3), OSError(4))
      + Exception Group Traceback (most recent call last):
      |   File "<doctest default[0]>", line 2, in <module>
      |     raise ExceptionGroup("eg",
      |         [ValueError(1), TypeError(2), OSError(3), OSError(4)])
      | ExceptionGroup: eg (1 sub-exception)
      +-+---------------- 1 ----------------
        | ValueError: 1
        +------------------------------------

If the exception raised from the `try`{.interpreted-text role="keyword"} block is not an exception group and its type matches one of the `!except*`{.interpreted-text role="keyword"} clauses, it is caught and wrapped by an exception group with an empty message string. This ensures that the type of the target `e` is consistently `BaseExceptionGroup`{.interpreted-text role="exc"}:

    >>> try:
    ...     raise BlockingIOError
    ... except* BlockingIOError as e:
    ...     print(repr(e))
    ...
    ExceptionGroup('', (BlockingIOError(),))

`break`{.interpreted-text role="keyword"}, `continue`{.interpreted-text role="keyword"} and `return`{.interpreted-text role="keyword"} cannot appear in an `!except*`{.interpreted-text role="keyword"} clause.

::: index
pair: keyword; else pair: statement; return pair: statement; break pair: statement; continue
:::

### `!else`{.interpreted-text role="keyword"} clause {#except_else}

The optional `!else`{.interpreted-text role="keyword"} clause is executed if the control flow leaves the `try`{.interpreted-text role="keyword"} suite, no exception was raised, and no `return`{.interpreted-text role="keyword"}, `continue`{.interpreted-text role="keyword"}, or `break`{.interpreted-text role="keyword"} statement was executed. Exceptions in the `!else`{.interpreted-text role="keyword"} clause are not handled by the preceding `except`{.interpreted-text role="keyword"} clauses.

::: index
pair: keyword; finally
:::

### `!finally`{.interpreted-text role="keyword"} clause {#finally}

If `!finally`{.interpreted-text role="keyword"} is present, it specifies a \'cleanup\' handler. The `try`{.interpreted-text role="keyword"} clause is executed, including any `except`{.interpreted-text role="keyword"} and `else <except_else>`{.interpreted-text role="keyword"} clauses. If an exception occurs in any of the clauses and is not handled, the exception is temporarily saved. The `!finally`{.interpreted-text role="keyword"} clause is executed. If there is a saved exception it is re-raised at the end of the `!finally`{.interpreted-text role="keyword"} clause. If the `!finally`{.interpreted-text role="keyword"} clause raises another exception, the saved exception is set as the context of the new exception. If the `!finally`{.interpreted-text role="keyword"} clause executes a `return`{.interpreted-text role="keyword"}, `break`{.interpreted-text role="keyword"} or `continue`{.interpreted-text role="keyword"} statement, the saved exception is discarded. For example, this function returns 42.

``` 
def f():
    try:
        1/0
    finally:
        return 42
```

The exception information is not available to the program during execution of the `!finally`{.interpreted-text role="keyword"} clause.

::: index
pair: statement; return pair: statement; break pair: statement; continue
:::

When a `return`{.interpreted-text role="keyword"}, `break`{.interpreted-text role="keyword"} or `continue`{.interpreted-text role="keyword"} statement is executed in the `try`{.interpreted-text role="keyword"} suite of a `!try`{.interpreted-text role="keyword"}\...`!finally`{.interpreted-text role="keyword"} statement, the `!finally`{.interpreted-text role="keyword"} clause is also executed \'on the way out.\'

The return value of a function is determined by the last `return`{.interpreted-text role="keyword"} statement executed. Since the `!finally`{.interpreted-text role="keyword"} clause always executes, a `!return`{.interpreted-text role="keyword"} statement executed in the `!finally`{.interpreted-text role="keyword"} clause will always be the last one executed. The following function returns \'finally\'.

``` 
def foo():
    try:
        return 'try'
    finally:
        return 'finally'
```

::: versionchanged
3.8 Prior to Python 3.8, a `continue`{.interpreted-text role="keyword"} statement was illegal in the `!finally`{.interpreted-text role="keyword"} clause due to a problem with the implementation.
:::

::: versionchanged
3.14 The compiler emits a `SyntaxWarning`{.interpreted-text role="exc"} when a `return`{.interpreted-text role="keyword"}, `break`{.interpreted-text role="keyword"} or `continue`{.interpreted-text role="keyword"} appears in a `!finally`{.interpreted-text role="keyword"} block (see `765`{.interpreted-text role="pep"}).
:::

## The `!with`{.interpreted-text role="keyword"} statement[]{#with} {#as}

::: index
! pair: statement; with pair: keyword; as single: as; with statement single: , (comma); with statement single: : (colon); compound statement
:::

The `with`{.interpreted-text role="keyword"} statement is used to wrap the execution of a block with methods defined by a context manager (see section `context-managers`{.interpreted-text role="ref"}). This allows common `try`{.interpreted-text role="keyword"}\...`except`{.interpreted-text role="keyword"}\...`finally`{.interpreted-text role="keyword"} usage patterns to be encapsulated for convenient reuse.

::: productionlist
python-grammar with_stmt: \"with\" ( \"(\" [with_stmt_contents]{.title-ref} \",\"? \")\" \| [with_stmt_contents]{.title-ref} ) \":\" [suite]{.title-ref} with_stmt_contents: [with_item]{.title-ref} (\",\" [with_item]{.title-ref})\* with_item: [expression]{.title-ref} \[\"as\" [target]{.title-ref}\]
:::

The execution of the `with`{.interpreted-text role="keyword"} statement with one \"item\" proceeds as follows:

1.  The context expression (the expression given in the `~python-grammar:with_item`{.interpreted-text role="token"}) is evaluated to obtain a context manager.

2.  The context manager\'s `~object.__enter__`{.interpreted-text role="meth"} is loaded for later use.

3.  The context manager\'s `~object.__exit__`{.interpreted-text role="meth"} is loaded for later use.

4.  The context manager\'s `~object.__enter__`{.interpreted-text role="meth"} method is invoked.

5.  If a target was included in the `with`{.interpreted-text role="keyword"} statement, the return value from `~object.__enter__`{.interpreted-text role="meth"} is assigned to it.

    :::: note
    ::: title
    Note
    :::

    The `with`{.interpreted-text role="keyword"} statement guarantees that if the `~object.__enter__`{.interpreted-text role="meth"} method returns without an error, then `~object.__exit__`{.interpreted-text role="meth"} will always be called. Thus, if an error occurs during the assignment to the target list, it will be treated the same as an error occurring within the suite would be. See step 7 below.
    ::::

6.  The suite is executed.

7.  The context manager\'s `~object.__exit__`{.interpreted-text role="meth"} method is invoked. If an exception caused the suite to be exited, its type, value, and traceback are passed as arguments to `~object.__exit__`{.interpreted-text role="meth"}. Otherwise, three `None`{.interpreted-text role="const"} arguments are supplied.

    If the suite was exited due to an exception, and the return value from the `~object.__exit__`{.interpreted-text role="meth"} method was false, the exception is reraised. If the return value was true, the exception is suppressed, and execution continues with the statement following the `with`{.interpreted-text role="keyword"} statement.

    If the suite was exited for any reason other than an exception, the return value from `~object.__exit__`{.interpreted-text role="meth"} is ignored, and execution proceeds at the normal location for the kind of exit that was taken.

The following code:

    with EXPRESSION as TARGET:
        SUITE

is semantically equivalent to:

    manager = (EXPRESSION)
    enter = manager.__enter__
    exit = manager.__exit__
    value = enter()
    hit_except = False

    try:
        TARGET = value
        SUITE
    except:
        hit_except = True
        if not exit(*sys.exc_info()):
            raise
    finally:
        if not hit_except:
            exit(None, None, None)

except that implicit `special method lookup <special-lookup>`{.interpreted-text role="ref"} is used for `~object.__enter__`{.interpreted-text role="meth"} and `~object.__exit__`{.interpreted-text role="meth"}.

With more than one item, the context managers are processed as if multiple `with`{.interpreted-text role="keyword"} statements were nested:

    with A() as a, B() as b:
        SUITE

is semantically equivalent to:

    with A() as a:
        with B() as b:
            SUITE

You can also write multi-item context managers in multiple lines if the items are surrounded by parentheses. For example:

    with (
        A() as a,
        B() as b,
    ):
        SUITE

::: versionchanged
3.1 Support for multiple context expressions.
:::

::: versionchanged
3.10 Support for using grouping parentheses to break the statement in multiple lines.
:::

::: seealso

`343`{.interpreted-text role="pep"} - The \"with\" statement

:   The specification, background, and examples for the Python `with`{.interpreted-text role="keyword"} statement.
:::

## The `!match`{.interpreted-text role="keyword"} statement[]{#match} {#case}

::: index
! pair: statement; match ! pair: keyword; case ! single: pattern matching pair: keyword; if pair: keyword; as pair: match; case single: as; match statement single: : (colon); compound statement
:::

::: versionadded
3.10
:::

The match statement is used for pattern matching. Syntax:

::: productionlist
python-grammar match_stmt: \'match\' [subject_expr]{.title-ref} \":\" NEWLINE INDENT [case_block]{.title-ref}+ DEDENT subject_expr: [!star_named_expression]{.title-ref} \",\" [!star_named_expressions]{.title-ref}? : \| [!named_expression]{.title-ref} case_block: \'case\' [patterns]{.title-ref} \[[guard]{.title-ref}\] \":\" [!block]{.title-ref}
:::

:::: note
::: title
Note
:::

This section uses single quotes to denote `soft keywords <soft-keywords>`{.interpreted-text role="ref"}.
::::

Pattern matching takes a pattern as input (following `case`) and a subject value (following `match`). The pattern (which may contain subpatterns) is matched against the subject value. The outcomes are:

- A match success or failure (also termed a pattern success or failure).
- Possible binding of matched values to a name. The prerequisites for this are further discussed below.

The `match` and `case` keywords are `soft keywords <soft-keywords>`{.interpreted-text role="ref"}.

::: seealso
- `634`{.interpreted-text role="pep"} \-- Structural Pattern Matching: Specification
- `636`{.interpreted-text role="pep"} \-- Structural Pattern Matching: Tutorial
:::

### Overview

Here\'s an overview of the logical flow of a match statement:

1.  The subject expression `subject_expr` is evaluated and a resulting subject value obtained. If the subject expression contains a comma, a tuple is constructed using `the standard rules <typesseq-tuple>`{.interpreted-text role="ref"}.

2.  Each pattern in a `case_block` is attempted to match with the subject value. The specific rules for success or failure are described below. The match attempt can also bind some or all of the standalone names within the pattern. The precise pattern binding rules vary per pattern type and are specified below. **Name bindings made during a successful pattern match outlive the executed block and can be used after the match statement**.

    :::: note
    ::: title
    Note
    :::

    During failed pattern matches, some subpatterns may succeed. Do not rely on bindings being made for a failed match. Conversely, do not rely on variables remaining unchanged after a failed match. The exact behavior is dependent on implementation and may vary. This is an intentional decision made to allow different implementations to add optimizations.
    ::::

3.  If the pattern succeeds, the corresponding guard (if present) is evaluated. In this case all name bindings are guaranteed to have happened.

    - If the guard evaluates as true or is missing, the `block` inside `case_block` is executed.
    - Otherwise, the next `case_block` is attempted as described above.
    - If there are no further case blocks, the match statement is completed.

:::: note
::: title
Note
:::

Users should generally never rely on a pattern being evaluated. Depending on implementation, the interpreter may cache values or use other optimizations which skip repeated evaluations.
::::

A sample match statement:

    >>> flag = False
    >>> match (100, 200):
    ...    case (100, 300):  # Mismatch: 200 != 300
    ...        print('Case 1')
    ...    case (100, 200) if flag:  # Successful match, but guard fails
    ...        print('Case 2')
    ...    case (100, y):  # Matches and binds y to 200
    ...        print(f'Case 3, y: {y}')
    ...    case _:  # Pattern not attempted
    ...        print('Case 4, I match anything!')
    ...
    Case 3, y: 200

In this case, `if flag` is a guard. Read more about that in the next section.

### Guards

::: index
! guard
:::

::: productionlist
python-grammar guard: \"if\" [!named_expression]{.title-ref}
:::

A `guard` (which is part of the `case`) must succeed for code inside the `case` block to execute. It takes the form: `if`{.interpreted-text role="keyword"} followed by an expression.

The logical flow of a `case` block with a `guard` follows:

1.  Check that the pattern in the `case` block succeeded. If the pattern failed, the `guard` is not evaluated and the next `case` block is checked.
2.  If the pattern succeeded, evaluate the `guard`.
    - If the `guard` condition evaluates as true, the case block is selected.
    - If the `guard` condition evaluates as false, the case block is not selected.
    - If the `guard` raises an exception during evaluation, the exception bubbles up.

Guards are allowed to have side effects as they are expressions. Guard evaluation must proceed from the first to the last case block, one at a time, skipping case blocks whose pattern(s) don\'t all succeed. (I.e., guard evaluation must happen in order.) Guard evaluation must stop once a case block is selected.

### Irrefutable Case Blocks {#irrefutable_case}

::: index
irrefutable case block, case block
:::

An irrefutable case block is a match-all case block. A match statement may have at most one irrefutable case block, and it must be last.

A case block is considered irrefutable if it has no guard and its pattern is irrefutable. A pattern is considered irrefutable if we can prove from its syntax alone that it will always succeed. Only the following patterns are irrefutable:

- `as-patterns`{.interpreted-text role="ref"} whose left-hand side is irrefutable
- `or-patterns`{.interpreted-text role="ref"} containing at least one irrefutable pattern
- `capture-patterns`{.interpreted-text role="ref"}
- `wildcard-patterns`{.interpreted-text role="ref"}
- parenthesized irrefutable patterns

### Patterns

::: index
single: ! patterns single: AS pattern, OR pattern, capture pattern, wildcard pattern
:::

:::: note
::: title
Note
:::

This section uses grammar notations beyond standard EBNF:

- the notation `SEP.RULE+` is shorthand for `RULE (SEP RULE)*`
- the notation `!RULE` is shorthand for a negative lookahead assertion
::::

The top-level syntax for `patterns` is:

::: productionlist
python-grammar patterns: [open_sequence_pattern]{.title-ref} \| [pattern]{.title-ref} pattern: [as_pattern]{.title-ref} \| [or_pattern]{.title-ref} closed_pattern: \| [literal_pattern]{.title-ref} : \| [capture_pattern]{.title-ref} : \| [wildcard_pattern]{.title-ref} : \| [value_pattern]{.title-ref} : \| [group_pattern]{.title-ref} : \| [sequence_pattern]{.title-ref} : \| [mapping_pattern]{.title-ref} : \| [class_pattern]{.title-ref}
:::

The descriptions below will include a description \"in simple terms\" of what a pattern does for illustration purposes (credits to Raymond Hettinger for a document that inspired most of the descriptions). Note that these descriptions are purely for illustration purposes and **may not** reflect the underlying implementation. Furthermore, they do not cover all valid forms.

#### OR Patterns

An OR pattern is two or more patterns separated by vertical bars `|`. Syntax:

::: productionlist
python-grammar or_pattern: \"\|\".\`closed_pattern\`+
:::

Only the final subpattern may be `irrefutable <irrefutable_case>`{.interpreted-text role="ref"}, and each subpattern must bind the same set of names to avoid ambiguity.

An OR pattern matches each of its subpatterns in turn to the subject value, until one succeeds. The OR pattern is then considered successful. Otherwise, if none of the subpatterns succeed, the OR pattern fails.

In simple terms, `P1 | P2 | ...` will try to match `P1`, if it fails it will try to match `P2`, succeeding immediately if any succeeds, failing otherwise.

#### AS Patterns

An AS pattern matches an OR pattern on the left of the `as`{.interpreted-text role="keyword"} keyword against a subject. Syntax:

::: productionlist
python-grammar as_pattern: [or_pattern]{.title-ref} \"as\" [capture_pattern]{.title-ref}
:::

If the OR pattern fails, the AS pattern fails. Otherwise, the AS pattern binds the subject to the name on the right of the as keyword and succeeds. `capture_pattern` cannot be a `_`.

In simple terms `P as NAME` will match with `P`, and on success it will set `NAME = <subject>`.

#### Literal Patterns

A literal pattern corresponds to most `literals <literals>`{.interpreted-text role="ref"} in Python. Syntax:

::: productionlist
python-grammar literal_pattern: [signed_number]{.title-ref} : \| [signed_number]{.title-ref} \"+\" NUMBER : \| [signed_number]{.title-ref} \"-\" NUMBER : \| [strings]{.title-ref} : \| \"None\" : \| \"True\" : \| \"False\" signed_number: \[\"-\"\] NUMBER
:::

The rule `strings` and the token `NUMBER` are defined in the `standard Python grammar <./grammar>`{.interpreted-text role="doc"}. Triple-quoted strings are supported. Raw strings and byte strings are supported. `f-strings`{.interpreted-text role="ref"} and `t-strings`{.interpreted-text role="ref"} are not supported.

The forms `signed_number '+' NUMBER` and `signed_number '-' NUMBER` are for expressing `complex numbers <imaginary>`{.interpreted-text role="ref"}; they require a real number on the left and an imaginary number on the right. E.g. `3 + 4j`.

In simple terms, `LITERAL` will succeed only if `<subject> == LITERAL`. For the singletons `None`, `True` and `False`, the `is`{.interpreted-text role="keyword"} operator is used.

#### Capture Patterns

A capture pattern binds the subject value to a name. Syntax:

::: productionlist
python-grammar capture_pattern: !\'\_\' NAME
:::

A single underscore `_` is not a capture pattern (this is what `!'_'` expresses). It is instead treated as a `~python-grammar:wildcard_pattern`{.interpreted-text role="token"}.

In a given pattern, a given name can only be bound once. E.g. `case x, x: ...` is invalid while `case [x] | x: ...` is allowed.

Capture patterns always succeed. The binding follows scoping rules established by the assignment expression operator in `572`{.interpreted-text role="pep"}; the name becomes a local variable in the closest containing function scope unless there\'s an applicable `global`{.interpreted-text role="keyword"} or `nonlocal`{.interpreted-text role="keyword"} statement.

In simple terms `NAME` will always succeed and it will set `NAME = <subject>`.

#### Wildcard Patterns

A wildcard pattern always succeeds (matches anything) and binds no name. Syntax:

::: productionlist
python-grammar wildcard_pattern: \'\_\'
:::

`_` is a `soft keyword <soft-keywords>`{.interpreted-text role="ref"} within any pattern, but only within patterns. It is an identifier, as usual, even within `match` subject expressions, `guard`s, and `case` blocks.

In simple terms, `_` will always succeed.

#### Value Patterns

A value pattern represents a named value in Python. Syntax:

::: productionlist
python-grammar value_pattern: [attr]{.title-ref} attr: [name_or_attr]{.title-ref} \".\" NAME name_or_attr: [attr]{.title-ref} \| NAME
:::

The dotted name in the pattern is looked up using standard Python `name resolution rules <resolve_names>`{.interpreted-text role="ref"}. The pattern succeeds if the value found compares equal to the subject value (using the `==` equality operator).

In simple terms `NAME1.NAME2` will succeed only if `<subject> == NAME1.NAME2`

:::: note
::: title
Note
:::

If the same value occurs multiple times in the same match statement, the interpreter may cache the first value found and reuse it rather than repeat the same lookup. This cache is strictly tied to a given execution of a given match statement.
::::

#### Group Patterns

A group pattern allows users to add parentheses around patterns to emphasize the intended grouping. Otherwise, it has no additional syntax. Syntax:

::: productionlist
python-grammar group_pattern: \"(\" [pattern]{.title-ref} \")\"
:::

In simple terms `(P)` has the same effect as `P`.

#### Sequence Patterns

A sequence pattern contains several subpatterns to be matched against sequence elements. The syntax is similar to the unpacking of a list or tuple.

::: productionlist
python-grammar sequence_pattern: \"\[\" \[[maybe_sequence_pattern]{.title-ref}\] \"\]\" : \| \"(\" \[[open_sequence_pattern]{.title-ref}\] \")\" open_sequence_pattern: [maybe_star_pattern]{.title-ref} \",\" \[[maybe_sequence_pattern]{.title-ref}\] maybe_sequence_pattern: \",\".\`maybe_star_pattern\`+ \",\"? maybe_star_pattern: [star_pattern]{.title-ref} \| [pattern]{.title-ref} star_pattern: \"\*\" ([capture_pattern]{.title-ref} \| [wildcard_pattern]{.title-ref})
:::

There is no difference if parentheses or square brackets are used for sequence patterns (i.e. `(...)` vs `[...]` ).

:::: note
::: title
Note
:::

A single pattern enclosed in parentheses without a trailing comma (e.g. `(3 | 4)`) is a `group pattern <group-patterns>`{.interpreted-text role="ref"}. While a single pattern enclosed in square brackets (e.g. `[3 | 4]`) is still a sequence pattern.
::::

At most one star subpattern may be in a sequence pattern. The star subpattern may occur in any position. If no star subpattern is present, the sequence pattern is a fixed-length sequence pattern; otherwise it is a variable-length sequence pattern.

The following is the logical flow for matching a sequence pattern against a subject value:

1.  If the subject value is not a sequence[^2], the sequence pattern fails.

2.  If the subject value is an instance of `str`, `bytes` or `bytearray` the sequence pattern fails.

3.  The subsequent steps depend on whether the sequence pattern is fixed or variable-length.

    If the sequence pattern is fixed-length:

    1.  If the length of the subject sequence is not equal to the number of subpatterns, the sequence pattern fails
    2.  Subpatterns in the sequence pattern are matched to their corresponding items in the subject sequence from left to right. Matching stops as soon as a subpattern fails. If all subpatterns succeed in matching their corresponding item, the sequence pattern succeeds.

    Otherwise, if the sequence pattern is variable-length:

    1.  If the length of the subject sequence is less than the number of non-star subpatterns, the sequence pattern fails.
    2.  The leading non-star subpatterns are matched to their corresponding items as for fixed-length sequences.
    3.  If the previous step succeeds, the star subpattern matches a list formed of the remaining subject items, excluding the remaining items corresponding to non-star subpatterns following the star subpattern.
    4.  Remaining non-star subpatterns are matched to their corresponding subject items, as for a fixed-length sequence.

    :::: note
    ::: title
    Note
    :::

    The length of the subject sequence is obtained via `len`{.interpreted-text role="func"} (i.e. via the `~object.__len__`{.interpreted-text role="meth"} protocol). This length may be cached by the interpreter in a similar manner as `value patterns <value-patterns>`{.interpreted-text role="ref"}.
    ::::

In simple terms `[P1, P2, P3,` \... `, P<N>]` matches only if all the following happens:

- check `<subject>` is a sequence
- `len(subject) == <N>`
- `P1` matches `<subject>[0]` (note that this match can also bind names)
- `P2` matches `<subject>[1]` (note that this match can also bind names)
- \... and so on for the corresponding pattern/element.

#### Mapping Patterns

A mapping pattern contains one or more key-value patterns. The syntax is similar to the construction of a dictionary. Syntax:

::: productionlist
python-grammar mapping_pattern: \"{\" \[[items_pattern]{.title-ref}\] \"}\" items_pattern: \",\".\`key_value_pattern\`+ \",\"? key_value_pattern: ([literal_pattern]{.title-ref} \| [value_pattern]{.title-ref}) \":\" [pattern]{.title-ref} : \| [double_star_pattern]{.title-ref} double_star_pattern: \"\*\*\" [capture_pattern]{.title-ref}
:::

At most one double star pattern may be in a mapping pattern. The double star pattern must be the last subpattern in the mapping pattern.

Duplicate keys in mapping patterns are disallowed. Duplicate literal keys will raise a `SyntaxError`{.interpreted-text role="exc"}. Two keys that otherwise have the same value will raise a `ValueError`{.interpreted-text role="exc"} at runtime.

The following is the logical flow for matching a mapping pattern against a subject value:

1.  If the subject value is not a mapping[^3],the mapping pattern fails.
2.  If every key given in the mapping pattern is present in the subject mapping, and the pattern for each key matches the corresponding item of the subject mapping, the mapping pattern succeeds.
3.  If duplicate keys are detected in the mapping pattern, the pattern is considered invalid. A `SyntaxError`{.interpreted-text role="exc"} is raised for duplicate literal values; or a `ValueError`{.interpreted-text role="exc"} for named keys of the same value.

:::: note
::: title
Note
:::

Key-value pairs are matched using the two-argument form of the mapping subject\'s `get()` method. Matched key-value pairs must already be present in the mapping, and not created on-the-fly via `~object.__missing__`{.interpreted-text role="meth"} or `~object.__getitem__`{.interpreted-text role="meth"}.
::::

In simple terms `{KEY1: P1, KEY2: P2, ... }` matches only if all the following happens:

- check `<subject>` is a mapping
- `KEY1 in <subject>`
- `P1` matches `<subject>[KEY1]`
- \... and so on for the corresponding KEY/pattern pair.

#### Class Patterns

A class pattern represents a class and its positional and keyword arguments (if any). Syntax:

::: productionlist
python-grammar class_pattern: [name_or_attr]{.title-ref} \"(\" \[[pattern_arguments]{.title-ref} \",\"?\] \")\" pattern_arguments: [positional_patterns]{.title-ref} \[\",\" [keyword_patterns]{.title-ref}\] : \| [keyword_patterns]{.title-ref} positional_patterns: \",\".\`pattern\`+ keyword_patterns: \",\".\`keyword_pattern\`+ keyword_pattern: NAME \"=\" [pattern]{.title-ref}
:::

The same keyword should not be repeated in class patterns.

The following is the logical flow for matching a class pattern against a subject value:

1.  If `name_or_attr` is not an instance of the builtin `type`{.interpreted-text role="class"} , raise `TypeError`{.interpreted-text role="exc"}.

2.  If the subject value is not an instance of `name_or_attr` (tested via `isinstance`{.interpreted-text role="func"}), the class pattern fails.

3.  If no pattern arguments are present, the pattern succeeds. Otherwise, the subsequent steps depend on whether keyword or positional argument patterns are present.

    For a number of built-in types (specified below), a single positional subpattern is accepted which will match the entire subject; for these types keyword patterns also work as for other types.

    If only keyword patterns are present, they are processed as follows, one by one:

    I.  The keyword is looked up as an attribute on the subject.
        - If this raises an exception other than `AttributeError`{.interpreted-text role="exc"}, the exception bubbles up.
        - If this raises `AttributeError`{.interpreted-text role="exc"}, the class pattern has failed.
        - Else, the subpattern associated with the keyword pattern is matched against the subject\'s attribute value. If this fails, the class pattern fails; if this succeeds, the match proceeds to the next keyword.
    II. If all keyword patterns succeed, the class pattern succeeds.

    If any positional patterns are present, they are converted to keyword patterns using the `~object.__match_args__`{.interpreted-text role="data"} attribute on the class `name_or_attr` before matching:

    I.  The equivalent of `getattr(cls, "__match_args__", ())` is called.

        - If this raises an exception, the exception bubbles up.
        - If the returned value is not a tuple, the conversion fails and `TypeError`{.interpreted-text role="exc"} is raised.
        - If there are more positional patterns than `len(cls.__match_args__)`, `TypeError`{.interpreted-text role="exc"} is raised.
        - Otherwise, positional pattern `i` is converted to a keyword pattern using `__match_args__[i]` as the keyword. `__match_args__[i]` must be a string; if not `TypeError`{.interpreted-text role="exc"} is raised.
        - If there are duplicate keywords, `TypeError`{.interpreted-text role="exc"} is raised.

        ::: seealso
        `class-pattern-matching`{.interpreted-text role="ref"}
        :::

    II. Once all positional patterns have been converted to keyword patterns, the match proceeds as if there were only keyword patterns.

    For the following built-in types the handling of positional subpatterns is different:

    - `bool`{.interpreted-text role="class"}
    - `bytearray`{.interpreted-text role="class"}
    - `bytes`{.interpreted-text role="class"}
    - `dict`{.interpreted-text role="class"}
    - `float`{.interpreted-text role="class"}
    - `frozenset`{.interpreted-text role="class"}
    - `int`{.interpreted-text role="class"}
    - `list`{.interpreted-text role="class"}
    - `set`{.interpreted-text role="class"}
    - `str`{.interpreted-text role="class"}
    - `tuple`{.interpreted-text role="class"}

    These classes accept a single positional argument, and the pattern there is matched against the whole object rather than an attribute. For example `int(0|1)` matches the value `0`, but not the value `0.0`.

In simple terms `CLS(P1, attr=P2)` matches only if the following happens:

- `isinstance(<subject>, CLS)`
- convert `P1` to a keyword pattern using `CLS.__match_args__`
- For each keyword argument `attr=P2`:
  - `hasattr(<subject>, "attr")`
  - `P2` matches `<subject>.attr`
- \... and so on for the corresponding keyword argument/pattern pair.

::: seealso
- `634`{.interpreted-text role="pep"} \-- Structural Pattern Matching: Specification
- `636`{.interpreted-text role="pep"} \-- Structural Pattern Matching: Tutorial
:::

::: index
single: parameter; function definition
:::

## Function definitions[]{#function} {#def}

::: index
pair: statement; def pair: function; definition pair: function; name pair: name; binding pair: object; user-defined function pair: object; function pair: function; name pair: name; binding single: () (parentheses); function definition single: , (comma); parameter list single: : (colon); compound statement
:::

A function definition defines a user-defined function object (see section `types`{.interpreted-text role="ref"}):

::: productionlist
python-grammar funcdef: \[[decorators]{.title-ref}\] \"def\" [funcname]{.title-ref} \[[type_params]{.title-ref}\] \"(\" \[[parameter_list]{.title-ref}\] \")\" : \[\"-\>\" [expression]{.title-ref}\] \":\" [suite]{.title-ref} decorators: [decorator]{.title-ref}+ decorator: \"@\" [assignment_expression]{.title-ref} NEWLINE parameter_list: [defparameter]{.title-ref} (\",\" [defparameter]{.title-ref})\* \",\" \"/\" \[\",\" \[[parameter_list_no_posonly]{.title-ref}\]\] : \| [parameter_list_no_posonly]{.title-ref} parameter_list_no_posonly: [defparameter]{.title-ref} (\",\" [defparameter]{.title-ref})\* \[\",\" \[[parameter_list_starargs]{.title-ref}\]\] : \| [parameter_list_starargs]{.title-ref} parameter_list_starargs: \"\*\" \[[star_parameter]{.title-ref}\] (\",\" [defparameter]{.title-ref})\* \[\",\" \[[parameter_star_kwargs]{.title-ref}\]\] : \| \"\*\" (\",\" [defparameter]{.title-ref})+ \[\",\" \[[parameter_star_kwargs]{.title-ref}\]\] : \| [parameter_star_kwargs]{.title-ref} parameter_star_kwargs: \"\*\*\" [parameter]{.title-ref} \[\",\"\] parameter: [identifier]{.title-ref} \[\":\" [expression]{.title-ref}\] star_parameter: [identifier]{.title-ref} \[\":\" \[\"\*\"\] [expression]{.title-ref}\] defparameter: [parameter]{.title-ref} \[\"=\" [expression]{.title-ref}\] funcname: [identifier]{.title-ref}
:::

A function definition is an executable statement. Its execution binds the function name in the current local namespace to a function object (a wrapper around the executable code for the function). This function object contains a reference to the current global namespace as the global namespace to be used when the function is called.

The function definition does not execute the function body; this gets executed only when the function is called.[^4]

::: index
single: @ (at); function definition
:::

A function definition may be wrapped by one or more `decorator`{.interpreted-text role="term"} expressions. Decorator expressions are evaluated when the function is defined, in the scope that contains the function definition. The result must be a callable, which is invoked with the function object as the only argument. The returned value is bound to the function name instead of the function object. Multiple decorators are applied in nested fashion. For example, the following code :

    @f1(arg)
    @f2
    def func(): pass

is roughly equivalent to :

    def func(): pass
    func = f1(arg)(f2(func))

except that the original function is not temporarily bound to the name `func`.

::: versionchanged
3.9 Functions may be decorated with any valid `~python-grammar:assignment_expression`{.interpreted-text role="token"}. Previously, the grammar was much more restrictive; see `614`{.interpreted-text role="pep"} for details.
:::

A list of `type parameters <type-params>`{.interpreted-text role="ref"} may be given in square brackets between the function\'s name and the opening parenthesis for its parameter list. This indicates to static type checkers that the function is generic. At runtime, the type parameters can be retrieved from the function\'s `~function.__type_params__`{.interpreted-text role="attr"} attribute. See `generic-functions`{.interpreted-text role="ref"} for more.

::: versionchanged
3.12 Type parameter lists are new in Python 3.12.
:::

::: index
triple: default; parameter; value single: argument; function definition single: = (equals); function definition
:::

When one or more `parameters <parameter>`{.interpreted-text role="term"} have the form *parameter* `=` *expression*, the function is said to have \"default parameter values.\" For a parameter with a default value, the corresponding `argument`{.interpreted-text role="term"} may be omitted from a call, in which case the parameter\'s default value is substituted. If a parameter has a default value, all following parameters up until the \"`*`\" must also have a default value \-\-- this is a syntactic restriction that is not expressed by the grammar.

**Default parameter values are evaluated from left to right when the function definition is executed.** This means that the expression is evaluated once, when the function is defined, and that the same \"pre-computed\" value is used for each call. This is especially important to understand when a default parameter value is a mutable object, such as a list or a dictionary: if the function modifies the object (e.g. by appending an item to a list), the default parameter value is in effect modified. This is generally not what was intended. A way around this is to use `None` as the default, and explicitly test for it in the body of the function, e.g.:

    def whats_on_the_telly(penguin=None):
        if penguin is None:
            penguin = []
        penguin.append("property of the zoo")
        return penguin

::: index
single: / (slash); function definition single: \* (asterisk); function definition single: \*\*; function definition
:::

Function call semantics are described in more detail in section `calls`{.interpreted-text role="ref"}. A function call always assigns values to all parameters mentioned in the parameter list, either from positional arguments, from keyword arguments, or from default values. If the form \"`*identifier`\" is present, it is initialized to a tuple receiving any excess positional parameters, defaulting to the empty tuple. If the form \"`**identifier`\" is present, it is initialized to a new ordered mapping receiving any excess keyword arguments, defaulting to a new empty mapping of the same type. Parameters after \"`*`\" or \"`*identifier`\" are keyword-only parameters and may only be passed by keyword arguments. Parameters before \"`/`\" are positional-only parameters and may only be passed by positional arguments.

::: versionchanged
3.8 The `/` function parameter syntax may be used to indicate positional-only parameters. See `570`{.interpreted-text role="pep"} for details.
:::

::: index
pair: function; annotations single: -\>; function annotations single: : (colon); function annotations
:::

Parameters may have an `annotation <function annotation>`{.interpreted-text role="term"} of the form \"`: expression`\" following the parameter name. Any parameter may have an annotation, even those of the form `*identifier` or `**identifier`. (As a special case, parameters of the form `*identifier` may have an annotation \"`: *expression`\".) Functions may have \"return\" annotation of the form \"`-> expression`\" after the parameter list. These annotations can be any valid Python expression. The presence of annotations does not change the semantics of a function. See `annotations`{.interpreted-text role="ref"} for more information on annotations.

::: versionchanged
3.11 Parameters of the form \"`*identifier`\" may have an annotation \"`: *expression`\". See `646`{.interpreted-text role="pep"}.
:::

::: index
pair: lambda; expression
:::

It is also possible to create anonymous functions (functions not bound to a name), for immediate use in expressions. This uses lambda expressions, described in section `lambda`{.interpreted-text role="ref"}. Note that the lambda expression is merely a shorthand for a simplified function definition; a function defined in a \"`def`{.interpreted-text role="keyword"}\" statement can be passed around or assigned to another name just like a function defined by a lambda expression. The \"`!def`{.interpreted-text role="keyword"}\" form is actually more powerful since it allows the execution of multiple statements and annotations.

**Programmer\'s note:** Functions are first-class objects. A \"`def`\" statement executed inside a function definition defines a local function that can be returned or passed around. Free variables used in the nested function can access the local variables of the function containing the def. See section `naming`{.interpreted-text role="ref"} for details.

::: seealso

`3107`{.interpreted-text role="pep"} - Function Annotations

:   The original specification for function annotations.

`484`{.interpreted-text role="pep"} - Type Hints

:   Definition of a standard meaning for annotations: type hints.

`526`{.interpreted-text role="pep"} - Syntax for Variable Annotations

:   Ability to type hint variable declarations, including class variables and instance variables.

`563`{.interpreted-text role="pep"} - Postponed Evaluation of Annotations

:   Support for forward references within annotations by preserving annotations in a string form at runtime instead of eager evaluation.

`318`{.interpreted-text role="pep"} - Decorators for Functions and Methods

:   Function and method decorators were introduced. Class decorators were introduced in `3129`{.interpreted-text role="pep"}.
:::

## Class definitions {#class}

::: index
pair: object; class pair: statement; class pair: class; definition pair: class; name pair: name; binding pair: execution; frame single: inheritance single: docstring single: () (parentheses); class definition single: , (comma); expression list single: : (colon); compound statement
:::

A class definition defines a class object (see section `types`{.interpreted-text role="ref"}):

::: productionlist
python-grammar classdef: \[[decorators]{.title-ref}\] \"class\" [classname]{.title-ref} \[[type_params]{.title-ref}\] \[[inheritance]{.title-ref}\] \":\" [suite]{.title-ref} inheritance: \"(\" \[[argument_list]{.title-ref}\] \")\" classname: [identifier]{.title-ref}
:::

A class definition is an executable statement. The inheritance list usually gives a list of base classes (see `metaclasses`{.interpreted-text role="ref"} for more advanced uses), so each item in the list should evaluate to a class object which allows subclassing. Classes without an inheritance list inherit, by default, from the base class `object`{.interpreted-text role="class"}; hence, :

    class Foo:
        pass

is equivalent to :

    class Foo(object):
        pass

There may be one or more base classes; see `multiple-inheritance`{.interpreted-text role="ref"} below for more information.

The class\'s suite is then executed in a new execution frame (see `naming`{.interpreted-text role="ref"}), using a newly created local namespace and the original global namespace. (Usually, the suite contains mostly function definitions.) When the class\'s suite finishes execution, its execution frame is discarded but its local namespace is saved.[^5] A class object is then created using the inheritance list for the base classes and the saved local namespace for the attribute dictionary. The class name is bound to this class object in the original local namespace.

The order in which attributes are defined in the class body is preserved in the new class\'s `~type.__dict__`{.interpreted-text role="attr"}. Note that this is reliable only right after the class is created and only for classes that were defined using the definition syntax.

Class creation can be customized heavily using `metaclasses <metaclasses>`{.interpreted-text role="ref"}.

::: index
single: @ (at); class definition
:::

Classes can also be decorated: just like when decorating functions, :

    @f1(arg)
    @f2
    class Foo: pass

is roughly equivalent to :

    class Foo: pass
    Foo = f1(arg)(f2(Foo))

The evaluation rules for the decorator expressions are the same as for function decorators. The result is then bound to the class name.

::: versionchanged
3.9 Classes may be decorated with any valid `~python-grammar:assignment_expression`{.interpreted-text role="token"}. Previously, the grammar was much more restrictive; see `614`{.interpreted-text role="pep"} for details.
:::

A list of `type parameters <type-params>`{.interpreted-text role="ref"} may be given in square brackets immediately after the class\'s name. This indicates to static type checkers that the class is generic. At runtime, the type parameters can be retrieved from the class\'s `~type.__type_params__`{.interpreted-text role="attr"} attribute. See `generic-classes`{.interpreted-text role="ref"} for more.

::: versionchanged
3.12 Type parameter lists are new in Python 3.12.
:::

**Programmer\'s note:** Variables defined in the class definition are class attributes; they are shared by instances. Instance attributes can be set in a method with `self.name = value`. Both class and instance attributes are accessible through the notation \"`self.name`\", and an instance attribute hides a class attribute with the same name when accessed in this way. Class attributes can be used as defaults for instance attributes, but using mutable values there can lead to unexpected results. `Descriptors <descriptors>`{.interpreted-text role="ref"} can be used to create instance variables with different implementation details.

::: seealso

`3115`{.interpreted-text role="pep"} - Metaclasses in Python 3000

:   The proposal that changed the declaration of metaclasses to the current syntax, and the semantics for how classes with metaclasses are constructed.

`3129`{.interpreted-text role="pep"} - Class Decorators

:   The proposal that added class decorators. Function and method decorators were introduced in `318`{.interpreted-text role="pep"}.
:::

### Multiple inheritance

Python classes may have multiple base classes, a technique known as *multiple inheritance*. The base classes are specified in the class definition by listing them in parentheses after the class name, separated by commas. For example, the following class definition:

::: doctest
\>\>\> class A: pass \>\>\> class B: pass \>\>\> class C(A, B): pass
:::

defines a class `C` that inherits from classes `A` and `B`.

The `method resolution order`{.interpreted-text role="term"} (MRO) is the order in which base classes are searched when looking up an attribute on a class. See `python_2.3_mro`{.interpreted-text role="ref"} for a description of how Python determines the MRO for a class.

Multiple inheritance is not always allowed. Attempting to define a class with multiple inheritance will raise an error if one of the bases does not allow subclassing, if a consistent MRO cannot be created, if no valid metaclass can be determined, or if there is an instance layout conflict. We\'ll discuss each of these in turn.

First, all base classes must allow subclassing. While most classes allow subclassing, some built-in classes do not, such as `bool`{.interpreted-text role="class"}:

::: doctest
\>\>\> class SubBool(bool): \# TypeError \... pass Traceback (most recent call last): \... TypeError: type \'bool\' is not an acceptable base type
:::

In the resolved MRO of a class, the class\'s bases appear in the order they were specified in the class\'s bases list. Additionally, the MRO always lists a child class before any of its bases. A class definition will fail if it is impossible to resolve a consistent MRO that satisfies these rules from the list of bases provided:

::: doctest
\>\>\> class Base: pass \>\>\> class Child(Base): pass \>\>\> class Grandchild(Base, Child): pass \# TypeError Traceback (most recent call last): \... TypeError: Cannot create a consistent method resolution order (MRO) for bases Base, Child
:::

In the MRO of `Grandchild`, `Base` must appear before `Child` because it is first in the base class list, but it must also appear after `Child` because it is a parent of `Child`. This is a contradiction, so the class cannot be defined.

If some of the bases have a custom `metaclass`{.interpreted-text role="term"}, the metaclass of the resulting class is chosen among the metaclasses of the bases and the explicitly specified metaclass of the child class. It must be a metaclass that is a subclass of all other candidate metaclasses. If no such metaclass exists among the candidates, the class cannot be created, as explained in `metaclass-determination`{.interpreted-text role="ref"}.

Finally, the instance layouts of the bases must be compatible. This means that it must be possible to compute a *solid base* for the class. Exactly which classes are solid bases depends on the Python implementation.

::: impl-detail
In CPython, a class is a solid base if it has a nonempty `~object.__slots__`{.interpreted-text role="attr"} definition. Many but not all classes defined in C are also solid bases, including most builtins (such as `int`{.interpreted-text role="class"} or `BaseException`{.interpreted-text role="class"}) but excluding most concrete `Exception`{.interpreted-text role="class"} classes. Generally, a C class is a solid base if its underlying struct is different in size from its base class.
:::

Every class has a solid base. `object`{.interpreted-text role="class"}, the base class, has itself as its solid base. If there is a single base, the child class\'s solid base is that class if it is a solid base, or else the base class\'s solid base. If there are multiple bases, we first find the solid base for each base class to produce a list of candidate solid bases. If there is a unique solid base that is a subclass of all others, then that class is the solid base. Otherwise, class creation fails.

Example:

::: doctest
\>\>\> class Solid1: \... \_\_slots\_\_ = (\"solid1\",) \>\>\> \>\>\> class Solid2: \... \_\_slots\_\_ = (\"solid2\",) \>\>\> \>\>\> class SolidChild(Solid1): \... \_\_slots\_\_ = (\"solid_child\",) \>\>\> \>\>\> class C1: \# solid base is [object]{.title-ref} \... pass \>\>\> \>\>\> \# OK: solid bases are [Solid1]{.title-ref} and [object]{.title-ref}, and [Solid1]{.title-ref} is a subclass of [object]{.title-ref}. \>\>\> class C2(Solid1, C1): \# solid base is [Solid1]{.title-ref} \... pass \>\>\> \>\>\> \# OK: solid bases are [SolidChild]{.title-ref} and [Solid1]{.title-ref}, and [SolidChild]{.title-ref} is a subclass of [Solid1]{.title-ref}. \>\>\> class C3(SolidChild, Solid1): \# solid base is [SolidChild]{.title-ref} \... pass \>\>\> \>\>\> \# Error: solid bases are [Solid1]{.title-ref} and [Solid2]{.title-ref}, but neither is a subclass of the other. \>\>\> class C4(Solid1, Solid2): \# error: no single solid base \... pass Traceback (most recent call last): \... TypeError: multiple bases have instance lay-out conflict
:::

## Coroutines {#async}

::: versionadded
3.5
:::

::: index
pair: statement; async def
:::

### Coroutine function definition {#async def}

::: productionlist
python-grammar async_funcdef: \[[decorators]{.title-ref}\] \"async\" \"def\" [funcname]{.title-ref} \"(\" \[[parameter_list]{.title-ref}\] \")\" : \[\"-\>\" [expression]{.title-ref}\] \":\" [suite]{.title-ref}
:::

::: index
pair: keyword; async pair: keyword; await
:::

Execution of Python coroutines can be suspended and resumed at many points (see `coroutine`{.interpreted-text role="term"}). `await`{.interpreted-text role="keyword"} expressions, `async for`{.interpreted-text role="keyword"} and `async with`{.interpreted-text role="keyword"} can only be used in the body of a coroutine function.

Functions defined with `async def` syntax are always coroutine functions, even if they do not contain `await` or `async` keywords.

It is a `SyntaxError`{.interpreted-text role="exc"} to use a `yield from` expression inside the body of a coroutine function.

An example of a coroutine function:

    async def func(param1, param2):
        do_stuff()
        await some_coroutine()

::: versionchanged
3.7 `await` and `async` are now keywords; previously they were only treated as such inside the body of a coroutine function.
:::

::: index
pair: statement; async for
:::

### The `!async for`{.interpreted-text role="keyword"} statement {#async for}

::: productionlist
python-grammar async_for_stmt: \"async\" [for_stmt]{.title-ref}
:::

An `asynchronous iterable`{.interpreted-text role="term"} provides an `__aiter__` method that directly returns an `asynchronous iterator`{.interpreted-text role="term"}, which can call asynchronous code in its `__anext__` method.

The `async for` statement allows convenient iteration over asynchronous iterables.

The following code:

    async for TARGET in ITER:
        SUITE
    else:
        SUITE2

Is semantically equivalent to:

    iter = (ITER).__aiter__()
    running = True

    while running:
        try:
            TARGET = await iter.__anext__()
        except StopAsyncIteration:
            running = False
        else:
            SUITE
    else:
        SUITE2

except that implicit `special method lookup <special-lookup>`{.interpreted-text role="ref"} is used for `~object.__aiter__`{.interpreted-text role="meth"} and `~object.__anext__`{.interpreted-text role="meth"}.

It is a `SyntaxError`{.interpreted-text role="exc"} to use an `async for` statement outside the body of a coroutine function.

::: index
pair: statement; async with
:::

### The `!async with`{.interpreted-text role="keyword"} statement {#async with}

::: productionlist
python-grammar async_with_stmt: \"async\" [with_stmt]{.title-ref}
:::

An `asynchronous context manager`{.interpreted-text role="term"} is a `context manager`{.interpreted-text role="term"} that is able to suspend execution in its *enter* and *exit* methods.

The following code:

    async with EXPRESSION as TARGET:
        SUITE

is semantically equivalent to:

    manager = (EXPRESSION)
    aenter = manager.__aenter__
    aexit = manager.__aexit__
    value = await aenter()
    hit_except = False

    try:
        TARGET = value
        SUITE
    except:
        hit_except = True
        if not await aexit(*sys.exc_info()):
            raise
    finally:
        if not hit_except:
            await aexit(None, None, None)

except that implicit `special method lookup <special-lookup>`{.interpreted-text role="ref"} is used for `~object.__aenter__`{.interpreted-text role="meth"} and `~object.__aexit__`{.interpreted-text role="meth"}.

It is a `SyntaxError`{.interpreted-text role="exc"} to use an `async with` statement outside the body of a coroutine function.

::: seealso

`492`{.interpreted-text role="pep"} - Coroutines with async and await syntax

:   The proposal that made coroutines a proper standalone concept in Python, and added supporting syntax.
:::

## Type parameter lists {#type-params}

::: versionadded
3.12
:::

::: versionchanged
3.13 Support for default values was added (see `696`{.interpreted-text role="pep"}).
:::

::: index
single: type parameters
:::

::: productionlist
python-grammar type_params: \"\[\" [type_param]{.title-ref} (\",\" [type_param]{.title-ref})\* \"\]\" type_param: [typevar]{.title-ref} \| [typevartuple]{.title-ref} \| [paramspec]{.title-ref} typevar: [identifier]{.title-ref} (\":\" [expression]{.title-ref})? (\"=\" [expression]{.title-ref})? typevartuple: \"\*\" [identifier]{.title-ref} (\"=\" [expression]{.title-ref})? paramspec: \"\*\*\" [identifier]{.title-ref} (\"=\" [expression]{.title-ref})?
:::

`Functions <def>`{.interpreted-text role="ref"} (including `coroutines <async def>`{.interpreted-text role="ref"}), `classes <class>`{.interpreted-text role="ref"} and `type aliases <type>`{.interpreted-text role="ref"} may contain a type parameter list:

    def max[T](args: list[T]) -> T:
        ...

    async def amax[T](args: list[T]) -> T:
        ...

    class Bag[T]:
        def __iter__(self) -> Iterator[T]:
            ...

        def add(self, arg: T) -> None:
            ...

    type ListOrSet[T] = list[T] | set[T]

Semantically, this indicates that the function, class, or type alias is generic over a type variable. This information is primarily used by static type checkers, and at runtime, generic objects behave much like their non-generic counterparts.

Type parameters are declared in square brackets (`[]`) immediately after the name of the function, class, or type alias. The type parameters are accessible within the scope of the generic object, but not elsewhere. Thus, after a declaration `def func[T](): pass`, the name `T` is not available in the module scope. Below, the semantics of generic objects are described with more precision. The scope of type parameters is modeled with a special function (technically, an `annotation scope <annotation-scopes>`{.interpreted-text role="ref"}) that wraps the creation of the generic object.

Generic functions, classes, and type aliases have a `~definition.__type_params__`{.interpreted-text role="attr"} attribute listing their type parameters.

Type parameters come in three kinds:

- `typing.TypeVar`{.interpreted-text role="data"}, introduced by a plain name (e.g., `T`). Semantically, this represents a single type to a type checker.
- `typing.TypeVarTuple`{.interpreted-text role="data"}, introduced by a name prefixed with a single asterisk (e.g., `*Ts`). Semantically, this stands for a tuple of any number of types.
- `typing.ParamSpec`{.interpreted-text role="data"}, introduced by a name prefixed with two asterisks (e.g., `**P`). Semantically, this stands for the parameters of a callable.

`typing.TypeVar`{.interpreted-text role="data"} declarations can define *bounds* and *constraints* with a colon (`:`) followed by an expression. A single expression after the colon indicates a bound (e.g. `T: int`). Semantically, this means that the `!typing.TypeVar`{.interpreted-text role="data"} can only represent types that are a subtype of this bound. A parenthesized tuple of expressions after the colon indicates a set of constraints (e.g. `T: (str, bytes)`). Each member of the tuple should be a type (again, this is not enforced at runtime). Constrained type variables can only take on one of the types in the list of constraints.

For `!typing.TypeVar`{.interpreted-text role="data"}s declared using the type parameter list syntax, the bound and constraints are not evaluated when the generic object is created, but only when the value is explicitly accessed through the attributes `__bound__` and `__constraints__`. To accomplish this, the bounds or constraints are evaluated in a separate `annotation scope <annotation-scopes>`{.interpreted-text role="ref"}.

`typing.TypeVarTuple`{.interpreted-text role="data"}s and `typing.ParamSpec`{.interpreted-text role="data"}s cannot have bounds or constraints.

All three flavors of type parameters can also have a *default value*, which is used when the type parameter is not explicitly provided. This is added by appending a single equals sign (`=`) followed by an expression. Like the bounds and constraints of type variables, the default value is not evaluated when the object is created, but only when the type parameter\'s `__default__` attribute is accessed. To this end, the default value is evaluated in a separate `annotation scope <annotation-scopes>`{.interpreted-text role="ref"}. If no default value is specified for a type parameter, the `__default__` attribute is set to the special sentinel object `typing.NoDefault`{.interpreted-text role="data"}.

The following example indicates the full set of allowed type parameter declarations:

    def overly_generic[
       SimpleTypeVar,
       TypeVarWithDefault = int,
       TypeVarWithBound: int,
       TypeVarWithConstraints: (str, bytes),
       *SimpleTypeVarTuple = (int, float),
       **SimpleParamSpec = (str, bytearray),
    ](
       a: SimpleTypeVar,
       b: TypeVarWithDefault,
       c: TypeVarWithBound,
       d: Callable[SimpleParamSpec, TypeVarWithConstraints],
       *e: SimpleTypeVarTuple,
    ): ...

### Generic functions

Generic functions are declared as follows:

    def func[T](arg: T): ...

This syntax is equivalent to:

    annotation-def TYPE_PARAMS_OF_func():
        T = typing.TypeVar("T")
        def func(arg: T): ...
        func.__type_params__ = (T,)
        return func
    func = TYPE_PARAMS_OF_func()

Here `annotation-def` indicates an `annotation scope <annotation-scopes>`{.interpreted-text role="ref"}, which is not actually bound to any name at runtime. (One other liberty is taken in the translation: the syntax does not go through attribute access on the `typing`{.interpreted-text role="mod"} module, but creates an instance of `typing.TypeVar`{.interpreted-text role="data"} directly.)

The annotations of generic functions are evaluated within the annotation scope used for declaring the type parameters, but the function\'s defaults and decorators are not.

The following example illustrates the scoping rules for these cases, as well as for additional flavors of type parameters:

    @decorator
    def func[T: int, *Ts, **P](*args: *Ts, arg: Callable[P, T] = some_default):
        ...

Except for the `lazy evaluation <lazy-evaluation>`{.interpreted-text role="ref"} of the `~typing.TypeVar`{.interpreted-text role="class"} bound, this is equivalent to:

    DEFAULT_OF_arg = some_default

    annotation-def TYPE_PARAMS_OF_func():

        annotation-def BOUND_OF_T():
            return int
        # In reality, BOUND_OF_T() is evaluated only on demand.
        T = typing.TypeVar("T", bound=BOUND_OF_T())

        Ts = typing.TypeVarTuple("Ts")
        P = typing.ParamSpec("P")

        def func(*args: *Ts, arg: Callable[P, T] = DEFAULT_OF_arg):
            ...

        func.__type_params__ = (T, Ts, P)
        return func
    func = decorator(TYPE_PARAMS_OF_func())

The capitalized names like `DEFAULT_OF_arg` are not actually bound at runtime.

### Generic classes

Generic classes are declared as follows:

    class Bag[T]: ...

This syntax is equivalent to:

    annotation-def TYPE_PARAMS_OF_Bag():
        T = typing.TypeVar("T")
        class Bag(typing.Generic[T]):
            __type_params__ = (T,)
            ...
        return Bag
    Bag = TYPE_PARAMS_OF_Bag()

Here again `annotation-def` (not a real keyword) indicates an `annotation scope <annotation-scopes>`{.interpreted-text role="ref"}, and the name `TYPE_PARAMS_OF_Bag` is not actually bound at runtime.

Generic classes implicitly inherit from `typing.Generic`{.interpreted-text role="data"}. The base classes and keyword arguments of generic classes are evaluated within the type scope for the type parameters, and decorators are evaluated outside that scope. This is illustrated by this example:

    @decorator
    class Bag(Base[T], arg=T): ...

This is equivalent to:

    annotation-def TYPE_PARAMS_OF_Bag():
        T = typing.TypeVar("T")
        class Bag(Base[T], typing.Generic[T], arg=T):
            __type_params__ = (T,)
            ...
        return Bag
    Bag = decorator(TYPE_PARAMS_OF_Bag())

### Generic type aliases

The `type`{.interpreted-text role="keyword"} statement can also be used to create a generic type alias:

    type ListOrSet[T] = list[T] | set[T]

Except for the `lazy evaluation <lazy-evaluation>`{.interpreted-text role="ref"} of the value, this is equivalent to:

    annotation-def TYPE_PARAMS_OF_ListOrSet():
        T = typing.TypeVar("T")

        annotation-def VALUE_OF_ListOrSet():
            return list[T] | set[T]
        # In reality, the value is lazily evaluated
        return typing.TypeAliasType("ListOrSet", VALUE_OF_ListOrSet(), type_params=(T,))
    ListOrSet = TYPE_PARAMS_OF_ListOrSet()

Here, `annotation-def` (not a real keyword) indicates an `annotation scope <annotation-scopes>`{.interpreted-text role="ref"}. The capitalized names like `TYPE_PARAMS_OF_ListOrSet` are not actually bound at runtime.

## Annotations

::: versionchanged
3.14 Annotations are now lazily evaluated by default.
:::

Variables and function parameters may carry `annotations <annotation>`{.interpreted-text role="term"}, created by adding a colon after the name, followed by an expression:

    x: annotation = 1
    def f(param: annotation): ...

Functions may also carry a return annotation following an arrow:

    def f() -> annotation: ...

Annotations are conventionally used for `type hints <type hint>`{.interpreted-text role="term"}, but this is not enforced by the language, and in general annotations may contain arbitrary expressions. The presence of annotations does not change the runtime semantics of the code, except if some mechanism is used that introspects and uses the annotations (such as `dataclasses`{.interpreted-text role="mod"} or `functools.singledispatch`{.interpreted-text role="func"}).

By default, annotations are lazily evaluated in an `annotation scope <annotation-scopes>`{.interpreted-text role="ref"}. This means that they are not evaluated when the code containing the annotation is evaluated. Instead, the interpreter saves information that can be used to evaluate the annotation later if requested. The `annotationlib`{.interpreted-text role="mod"} module provides tools for evaluating annotations.

If the `future statement <future>`{.interpreted-text role="ref"} `from __future__ import annotations` is present, all annotations are instead stored as strings:

    >>> from __future__ import annotations
    >>> def f(param: annotation): ...
    >>> f.__annotations__
    {'param': 'annotation'}

This future statement will be deprecated and removed in a future version of Python, but not before Python 3.13 reaches its end of life (see `749`{.interpreted-text role="pep"}). When it is used, introspection tools like `annotationlib.get_annotations`{.interpreted-text role="func"} and `typing.get_type_hints`{.interpreted-text role="func"} are less likely to be able to resolve annotations at runtime.

**Footnotes**

[^1]: The exception is propagated to the invocation stack unless there is a `finally`{.interpreted-text role="keyword"} clause which happens to raise another exception. That new exception causes the old one to be lost.

[^2]: In pattern matching, a sequence is defined as one of the following:

    - a class that inherits from `collections.abc.Sequence`{.interpreted-text role="class"}
    - a Python class that has been registered as `collections.abc.Sequence`{.interpreted-text role="class"}
    - a builtin class that has its (CPython) `Py_TPFLAGS_SEQUENCE`{.interpreted-text role="c:macro"} bit set
    - a class that inherits from any of the above

    The following standard library classes are sequences:

    - `array.array`{.interpreted-text role="class"}
    - `collections.deque`{.interpreted-text role="class"}
    - `list`{.interpreted-text role="class"}
    - `memoryview`{.interpreted-text role="class"}
    - `range`{.interpreted-text role="class"}
    - `tuple`{.interpreted-text role="class"}

    :::: note
    ::: title
    Note
    :::

    Subject values of type `str`, `bytes`, and `bytearray` do not match sequence patterns.
    ::::

[^3]: In pattern matching, a mapping is defined as one of the following:

    - a class that inherits from `collections.abc.Mapping`{.interpreted-text role="class"}
    - a Python class that has been registered as `collections.abc.Mapping`{.interpreted-text role="class"}
    - a builtin class that has its (CPython) `Py_TPFLAGS_MAPPING`{.interpreted-text role="c:macro"} bit set
    - a class that inherits from any of the above

    The standard library classes `dict`{.interpreted-text role="class"} and `types.MappingProxyType`{.interpreted-text role="class"} are mappings.

[^4]: A string literal appearing as the first statement in the function body is transformed into the function\'s `~function.__doc__`{.interpreted-text role="attr"} attribute and therefore the function\'s `docstring`{.interpreted-text role="term"}.

[^5]: A string literal appearing as the first statement in the class body is transformed into the namespace\'s `~type.__doc__`{.interpreted-text role="attr"} item and therefore the class\'s `docstring`{.interpreted-text role="term"}.
