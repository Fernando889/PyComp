# `!traceback`{.interpreted-text role="mod"} \-\-- Print or retrieve a stack traceback

::: {.module synopsis="Print or retrieve a stack traceback."}
traceback
:::

**Source code:** `Lib/traceback.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module provides a standard interface to extract, format and print stack traces of Python programs. It is more flexible than the interpreter\'s default traceback display, and therefore makes it possible to configure certain aspects of the output. Finally, it contains a utility for capturing enough information about an exception to print it later, without the need to save a reference to the actual exception. Since exceptions can be the roots of large objects graph, this utility can significantly improve memory management.

::: index
pair: object; traceback
:::

The module uses `traceback objects <traceback-objects>`{.interpreted-text role="ref"} \-\-- these are objects of type `types.TracebackType`{.interpreted-text role="class"}, which are assigned to the `~BaseException.__traceback__`{.interpreted-text role="attr"} field of `BaseException`{.interpreted-text role="class"} instances.

::: seealso

Module `faulthandler`{.interpreted-text role="mod"}

:   Used to dump Python tracebacks explicitly, on a fault, after a timeout, or on a user signal.

Module `pdb`{.interpreted-text role="mod"}

:   Interactive source code debugger for Python programs.
:::

The module\'s API can be divided into two parts:

- Module-level functions offering basic functionality, which are useful for interactive inspection of exceptions and tracebacks.
- `TracebackException`{.interpreted-text role="class"} class and its helper classes `StackSummary`{.interpreted-text role="class"} and `FrameSummary`{.interpreted-text role="class"}. These offer both more flexibility in the output generated and the ability to store the information necessary for later formatting without holding references to actual exception and traceback objects.

::: versionadded
3.13 Output is colorized by default and can be `controlled using environment variables <using-on-controlling-color>`{.interpreted-text role="ref"}.
:::

## Module-Level Functions

:::::: function
print_tb(tb, limit=None, file=None)

Print up to *limit* stack trace entries from `traceback object <traceback-objects>`{.interpreted-text role="ref"} *tb* (starting from the caller\'s frame) if *limit* is positive. Otherwise, print the last `abs(limit)` entries. If *limit* is omitted or `None`, all entries are printed. If *file* is omitted or `None`, the output goes to `sys.stderr`{.interpreted-text role="data"}; otherwise it should be an open `file <file object>`{.interpreted-text role="term"} or `file-like object`{.interpreted-text role="term"} to receive the output.

:::: note
::: title
Note
:::

The meaning of the *limit* parameter is different than the meaning of `sys.tracebacklimit`{.interpreted-text role="const"}. A negative *limit* value corresponds to a positive value of `!sys.tracebacklimit`{.interpreted-text role="const"}, whereas the behaviour of a positive *limit* value cannot be achieved with `!sys.tracebacklimit`{.interpreted-text role="const"}.
::::

::: versionchanged
3.5 Added negative *limit* support.
:::
::::::

:::::: function
print_exception(exc, /\[, value, tb\], limit=None, file=None, chain=True)

Print exception information and stack trace entries from `traceback object <traceback-objects>`{.interpreted-text role="ref"} *tb* to *file*. This differs from `print_tb`{.interpreted-text role="func"} in the following ways:

- if *tb* is not `None`, it prints a header `Traceback (most recent call last):`
- it prints the exception type and *value* after the stack trace

::: index
single: \^ (caret); marker
:::

- if *type(value)* is `SyntaxError`{.interpreted-text role="exc"} and *value* has the appropriate format, it prints the line where the syntax error occurred with a caret indicating the approximate position of the error.

Since Python 3.10, instead of passing *value* and *tb*, an exception object can be passed as the first argument. If *value* and *tb* are provided, the first argument is ignored in order to provide backwards compatibility.

The optional *limit* argument has the same meaning as for `print_tb`{.interpreted-text role="func"}. If *chain* is true (the default), then chained exceptions (the `~BaseException.__cause__`{.interpreted-text role="attr"} or `~BaseException.__context__`{.interpreted-text role="attr"} attributes of the exception) will be printed as well, like the interpreter itself does when printing an unhandled exception.

::: versionchanged
3.5 The *etype* argument is ignored and inferred from the type of *value*.
:::

::: versionchanged
3.10 The *etype* parameter has been renamed to *exc* and is now positional-only.
:::
::::::

::: function
print_exc(limit=None, file=None, chain=True)

This is a shorthand for `print_exception(sys.exception(), limit=limit, file=file, chain=chain)`.
:::

::: function
print_last(limit=None, file=None, chain=True)

This is a shorthand for `print_exception(sys.last_exc, limit=limit, file=file, chain=chain)`. In general it will work only after an exception has reached an interactive prompt (see `sys.last_exc`{.interpreted-text role="data"}).
:::

:::: function
print_stack(f=None, limit=None, file=None)

Print up to *limit* stack trace entries (starting from the invocation point) if *limit* is positive. Otherwise, print the last `abs(limit)` entries. If *limit* is omitted or `None`, all entries are printed. The optional *f* argument can be used to specify an alternate `stack frame <frame-objects>`{.interpreted-text role="ref"} to start. The optional *file* argument has the same meaning as for `print_tb`{.interpreted-text role="func"}.

::: versionchanged
3.5 Added negative *limit* support.
:::
::::

::: function
extract_tb(tb, limit=None)

Return a `StackSummary`{.interpreted-text role="class"} object representing a list of \"pre-processed\" stack trace entries extracted from the `traceback object <traceback-objects>`{.interpreted-text role="ref"} *tb*. It is useful for alternate formatting of stack traces. The optional *limit* argument has the same meaning as for `print_tb`{.interpreted-text role="func"}. A \"pre-processed\" stack trace entry is a `FrameSummary`{.interpreted-text role="class"} object containing attributes `~FrameSummary.filename`{.interpreted-text role="attr"}, `~FrameSummary.lineno`{.interpreted-text role="attr"}, `~FrameSummary.name`{.interpreted-text role="attr"}, and `~FrameSummary.line`{.interpreted-text role="attr"} representing the information that is usually printed for a stack trace.
:::

::: function
extract_stack(f=None, limit=None)

Extract the raw traceback from the current `stack frame <frame-objects>`{.interpreted-text role="ref"}. The return value has the same format as for `extract_tb`{.interpreted-text role="func"}. The optional *f* and *limit* arguments have the same meaning as for `print_stack`{.interpreted-text role="func"}.
:::

::: function
print_list(extracted_list, file=None)

Print the list of tuples as returned by `extract_tb`{.interpreted-text role="func"} or `extract_stack`{.interpreted-text role="func"} as a formatted stack trace to the given file. If *file* is `None`, the output is written to `sys.stderr`{.interpreted-text role="data"}.
:::

::: function
format_list(extracted_list)

Given a list of tuples or `FrameSummary`{.interpreted-text role="class"} objects as returned by `extract_tb`{.interpreted-text role="func"} or `extract_stack`{.interpreted-text role="func"}, return a list of strings ready for printing. Each string in the resulting list corresponds to the item with the same index in the argument list. Each string ends in a newline; the strings may contain internal newlines as well, for those items whose source text line is not `None`.
:::

:::::: function
format_exception_only(exc, /\[, value\], \*, show_group=False)

Format the exception part of a traceback using an exception value such as given by `sys.last_value`{.interpreted-text role="data"}. The return value is a list of strings, each ending in a newline. The list contains the exception\'s message, which is normally a single string; however, for `SyntaxError`{.interpreted-text role="exc"} exceptions, it contains several lines that (when printed) display detailed information about where the syntax error occurred. Following the message, the list contains the exception\'s `notes <BaseException.__notes__>`{.interpreted-text role="attr"}.

Since Python 3.10, instead of passing *value*, an exception object can be passed as the first argument. If *value* is provided, the first argument is ignored in order to provide backwards compatibility.

When *show_group* is `True`, and the exception is an instance of `BaseExceptionGroup`{.interpreted-text role="exc"}, the nested exceptions are included as well, recursively, with indentation relative to their nesting depth.

::: versionchanged
3.10 The *etype* parameter has been renamed to *exc* and is now positional-only.
:::

::: versionchanged
3.11 The returned list now includes any `notes <BaseException.__notes__>`{.interpreted-text role="attr"} attached to the exception.
:::

::: versionchanged
3.13 *show_group* parameter was added.
:::
::::::

::::: function
format_exception(exc, /\[, value, tb\], limit=None, chain=True)

Format a stack trace and the exception information. The arguments have the same meaning as the corresponding arguments to `print_exception`{.interpreted-text role="func"}. The return value is a list of strings, each ending in a newline and some containing internal newlines. When these lines are concatenated and printed, exactly the same text is printed as does `print_exception`{.interpreted-text role="func"}.

::: versionchanged
3.5 The *etype* argument is ignored and inferred from the type of *value*.
:::

::: versionchanged
3.10 This function\'s behavior and signature were modified to match `print_exception`{.interpreted-text role="func"}.
:::
:::::

::: function
format_exc(limit=None, chain=True)

This is like `print_exc(limit)` but returns a string instead of printing to a file.
:::

::: function
format_tb(tb, limit=None)

A shorthand for `format_list(extract_tb(tb, limit))`.
:::

::: function
format_stack(f=None, limit=None)

A shorthand for `format_list(extract_stack(f, limit))`.
:::

:::: function
clear_frames(tb)

Clears the local variables of all the stack frames in a `traceback <traceback-objects>`{.interpreted-text role="ref"} *tb* by calling the `~frame.clear`{.interpreted-text role="meth"} method of each `frame object <frame-objects>`{.interpreted-text role="ref"}.

::: versionadded
3.4
:::
::::

::::: function
walk_stack(f)

Walk a stack following `f.f_back <frame.f_back>`{.interpreted-text role="attr"} from the given frame, yielding the frame and line number for each frame. If *f* is `None`, the current stack is used. This helper is used with `StackSummary.extract`{.interpreted-text role="meth"}.

::: versionadded
3.5
:::

::: versionchanged
3.14 This function previously returned a generator that would walk the stack when first iterated over. The generator returned now is the state of the stack when `walk_stack` is called.
:::
:::::

:::: function
walk_tb(tb)

Walk a traceback following `~traceback.tb_next`{.interpreted-text role="attr"} yielding the frame and line number for each frame. This helper is used with `StackSummary.extract`{.interpreted-text role="meth"}.

::: versionadded
3.5
:::
::::

## `!TracebackException`{.interpreted-text role="class"} Objects

::: versionadded
3.5
:::

`!TracebackException`{.interpreted-text role="class"} objects are created from actual exceptions to capture data for later printing. They offer a more lightweight method of storing this information by avoiding holding references to `traceback<traceback-objects>`{.interpreted-text role="ref"} and `frame<frame-objects>`{.interpreted-text role="ref"} objects. In addition, they expose more options to configure the output compared to the module-level functions described above.

::::::::::::::::::::::::::::::::: {.TracebackException(exc_type, .exc_value, .exc_traceback, .*, .limit=None, .lookup_lines=True, .capture_locals=False, .compact=False, .max_group_width=15, .max_group_depth=10)}
Capture an exception for later rendering. The meaning of *limit*, *lookup_lines* and *capture_locals* are as for the `StackSummary`{.interpreted-text role="class"} class.

If *compact* is true, only data that is required by `!TracebackException`{.interpreted-text role="class"}\'s `format`{.interpreted-text role="meth"} method is saved in the class attributes. In particular, the `__context__`{.interpreted-text role="attr"} field is calculated only if `__cause__`{.interpreted-text role="attr"} is `None` and `__suppress_context__`{.interpreted-text role="attr"} is false.

Note that when locals are captured, they are also shown in the traceback.

*max_group_width* and *max_group_depth* control the formatting of exception groups (see `BaseExceptionGroup`{.interpreted-text role="exc"}). The depth refers to the nesting level of the group, and the width refers to the size of a single exception group\'s exceptions array. The formatted output is truncated when either limit is exceeded.

::: versionchanged
3.10 Added the *compact* parameter.
:::

::: versionchanged
3.11 Added the *max_group_width* and *max_group_depth* parameters.
:::

::: attribute
\_\_cause\_\_

A `!TracebackException`{.interpreted-text role="class"} of the original `~BaseException.__cause__`{.interpreted-text role="attr"}.
:::

::: attribute
\_\_context\_\_

A `!TracebackException`{.interpreted-text role="class"} of the original `~BaseException.__context__`{.interpreted-text role="attr"}.
:::

:::: attribute
exceptions

If `self` represents an `ExceptionGroup`{.interpreted-text role="exc"}, this field holds a list of `!TracebackException`{.interpreted-text role="class"} instances representing the nested exceptions. Otherwise it is `None`.

::: versionadded
3.11
:::
::::

::: attribute
\_\_suppress_context\_\_

The `~BaseException.__suppress_context__`{.interpreted-text role="attr"} value from the original exception.
:::

:::: attribute
\_\_notes\_\_

The `~BaseException.__notes__`{.interpreted-text role="attr"} value from the original exception, or `None` if the exception does not have any notes. If it is not `None` is it formatted in the traceback after the exception string.

::: versionadded
3.11
:::
::::

::: attribute
stack

A `StackSummary`{.interpreted-text role="class"} representing the traceback.
:::

:::: attribute
exc_type

The class of the original traceback.

::: deprecated
3.13
:::
::::

:::: attribute
exc_type_str

String display of the class of the original exception.

::: versionadded
3.13
:::
::::

::: attribute
filename

For syntax errors - the file name where the error occurred.
:::

::: attribute
lineno

For syntax errors - the line number where the error occurred.
:::

:::: attribute
end_lineno

For syntax errors - the end line number where the error occurred. Can be `None` if not present.

::: versionadded
3.10
:::
::::

::: attribute
text

For syntax errors - the text where the error occurred.
:::

::: attribute
offset

For syntax errors - the offset into the text where the error occurred.
:::

:::: attribute
end_offset

For syntax errors - the end offset into the text where the error occurred. Can be `None` if not present.

::: versionadded
3.10
:::
::::

::: attribute
msg

For syntax errors - the compiler error message.
:::

::: classmethod
from_exception(exc, \*, limit=None, lookup_lines=True, capture_locals=False)

Capture an exception for later rendering. *limit*, *lookup_lines* and *capture_locals* are as for the `StackSummary`{.interpreted-text role="class"} class.

Note that when locals are captured, they are also shown in the traceback.
:::

:::: method
print(\*, file=None, chain=True)

Print to *file* (default `sys.stderr`) the exception information returned by `format`{.interpreted-text role="meth"}.

::: versionadded
3.11
:::
::::

::: method
format(\*, chain=True)

Format the exception.

If *chain* is not `True`, `__cause__`{.interpreted-text role="attr"} and `__context__`{.interpreted-text role="attr"} will not be formatted.

The return value is a generator of strings, each ending in a newline and some containing internal newlines. `~traceback.print_exception`{.interpreted-text role="func"} is a wrapper around this method which just prints the lines to a file.
:::

::::: method
format_exception_only(\*, show_group=False)

Format the exception part of the traceback.

The return value is a generator of strings, each ending in a newline.

When *show_group* is `False`, the generator emits the exception\'s message followed by its notes (if it has any). The exception message is normally a single string; however, for `SyntaxError`{.interpreted-text role="exc"} exceptions, it consists of several lines that (when printed) display detailed information about where the syntax error occurred.

When *show_group* is `True`, and the exception is an instance of `BaseExceptionGroup`{.interpreted-text role="exc"}, the nested exceptions are included as well, recursively, with indentation relative to their nesting depth.

::: versionchanged
3.11 The exception\'s `notes <BaseException.__notes__>`{.interpreted-text role="attr"} are now included in the output.
:::

::: versionchanged
3.13 Added the *show_group* parameter.
:::
:::::
:::::::::::::::::::::::::::::::::

## `!StackSummary`{.interpreted-text role="class"} Objects

::: versionadded
3.5
:::

`!StackSummary`{.interpreted-text role="class"} objects represent a call stack ready for formatting.

:::::::::: StackSummary
:::: classmethod
extract(frame_gen, \*, limit=None, lookup_lines=True, capture_locals=False)

Construct a `!StackSummary`{.interpreted-text role="class"} object from a frame generator (such as is returned by `~traceback.walk_stack`{.interpreted-text role="func"} or `~traceback.walk_tb`{.interpreted-text role="func"}).

If *limit* is supplied, only this many frames are taken from *frame_gen*. If *lookup_lines* is `False`, the returned `FrameSummary`{.interpreted-text role="class"} objects will not have read their lines in yet, making the cost of creating the `!StackSummary`{.interpreted-text role="class"} cheaper (which may be valuable if it may not actually get formatted). If *capture_locals* is `True` the local variables in each `!FrameSummary`{.interpreted-text role="class"} are captured as object representations.

::: versionchanged
3.12 Exceptions raised from `repr`{.interpreted-text role="func"} on a local variable (when *capture_locals* is `True`) are no longer propagated to the caller.
:::
::::

::: classmethod
from_list(a_list)

Construct a `!StackSummary`{.interpreted-text role="class"} object from a supplied list of `FrameSummary`{.interpreted-text role="class"} objects or old-style list of tuples. Each tuple should be a 4-tuple with *filename*, *lineno*, *name*, *line* as the elements.
:::

:::: method
format()

Returns a list of strings ready for printing. Each string in the resulting list corresponds to a single `frame <frame-objects>`{.interpreted-text role="ref"} from the stack. Each string ends in a newline; the strings may contain internal newlines as well, for those items with source text lines.

For long sequences of the same frame and line, the first few repetitions are shown, followed by a summary line stating the exact number of further repetitions.

::: versionchanged
3.6 Long sequences of repeated frames are now abbreviated.
:::
::::

:::: method
format_frame_summary(frame_summary)

Returns a string for printing one of the `frames <frame-objects>`{.interpreted-text role="ref"} involved in the stack. This method is called for each `FrameSummary`{.interpreted-text role="class"} object to be printed by `StackSummary.format`{.interpreted-text role="meth"}. If it returns `None`, the frame is omitted from the output.

::: versionadded
3.11
:::
::::
::::::::::

## `!FrameSummary`{.interpreted-text role="class"} Objects

::: versionadded
3.5
:::

A `!FrameSummary`{.interpreted-text role="class"} object represents a single `frame <frame-objects>`{.interpreted-text role="ref"} in a `traceback <traceback-objects>`{.interpreted-text role="ref"}.

::::::::::: {.FrameSummary(filename, .lineno, .name, .*,\\ .lookup_line=True, .locals=None,\\ .line=None, .end_lineno=None, .colno=None, .end_colno=None)}
Represents a single `frame <frame-objects>`{.interpreted-text role="ref"} in the `traceback <traceback-objects>`{.interpreted-text role="ref"} or stack that is being formatted or printed. It may optionally have a stringified version of the frame\'s locals included in it. If *lookup_line* is `False`, the source code is not looked up until the `!FrameSummary`{.interpreted-text role="class"} has the `~FrameSummary.line`{.interpreted-text role="attr"} attribute accessed (which also happens when casting it to a `tuple`{.interpreted-text role="class"}). `~FrameSummary.line`{.interpreted-text role="attr"} may be directly provided, and will prevent line lookups happening at all. *locals* is an optional local variable mapping, and if supplied the variable representations are stored in the summary for later display.

`!FrameSummary`{.interpreted-text role="class"} instances have the following attributes:

::: attribute
FrameSummary.filename

The filename of the source code for this frame. Equivalent to accessing `f.f_code.co_filename <codeobject.co_filename>`{.interpreted-text role="attr"} on a `frame object <frame-objects>`{.interpreted-text role="ref"} *f*.
:::

::: attribute
FrameSummary.lineno

The line number of the source code for this frame.
:::

::: attribute
FrameSummary.name

Equivalent to accessing `f.f_code.co_name <codeobject.co_name>`{.interpreted-text role="attr"} on a `frame object <frame-objects>`{.interpreted-text role="ref"} *f*.
:::

::: attribute
FrameSummary.line

A string representing the source code for this frame, with leading and trailing whitespace stripped. If the source is not available, it is `None`.
:::

:::: attribute
FrameSummary.end_lineno

The last line number of the source code for this frame. By default, it is set to `lineno` and indexation starts from 1.

::: versionchanged
3.13 The default value changed from `None` to `lineno`.
:::
::::

::: attribute
FrameSummary.colno

The column number of the source code for this frame. By default, it is `None` and indexation starts from 0.
:::

::: attribute
FrameSummary.end_colno

The last column number of the source code for this frame. By default, it is `None` and indexation starts from 0.
:::
:::::::::::

## Examples of Using the Module-Level Functions {#traceback-example}

This simple example implements a basic read-eval-print loop, similar to (but less useful than) the standard Python interactive interpreter loop. For a more complete implementation of the interpreter loop, refer to the `code`{.interpreted-text role="mod"} module. :

    import sys, traceback

    def run_user_code(envdir):
        source = input(">>> ")
        try:
            exec(source, envdir)
        except Exception:
            print("Exception in user code:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)

    envdir = {}
    while True:
        run_user_code(envdir)

The following example demonstrates the different ways to print and format the exception and traceback:

::: testcode
import sys, traceback

def lumberjack():

:   bright_side_of_life()

def bright_side_of_life():

:   return tuple()\[0\]

try:

:   lumberjack()

except IndexError as exc:

:   print(\"\*\*\* print_tb:\") traceback.print_tb(exc.\_\_traceback\_\_, limit=1, file=sys.stdout) print(\"\*\*\* print_exception:\") traceback.print_exception(exc, limit=2, file=sys.stdout) print(\"\*\*\* print_exc:\") traceback.print_exc(limit=2, file=sys.stdout) print(\"\*\*\* format_exc, first and last line:\") formatted_lines = traceback.format_exc().splitlines() print(formatted_lines\[0\]) print(formatted_lines\[-1\]) print(\"\*\*\* format_exception:\") print(repr(traceback.format_exception(exc))) print(\"\*\*\* extract_tb:\") print(repr(traceback.extract_tb(exc.\_\_traceback\_\_))) print(\"\*\*\* format_tb:\") print(repr(traceback.format_tb(exc.\_\_traceback\_\_))) print(\"\*\*\* tb_lineno:\", exc.\_\_traceback\_\_.tb_lineno)
:::

The output for the example would look similar to this:

::: {.testoutput options="+NORMALIZE_WHITESPACE"}
**\* print_tb: File \"\<doctest\...\>\", line 10, in \<module\> lumberjack() \~\~\~\~\~\~\~\~\~\~\^\^**\* print_exception: Traceback (most recent call last): File \"\<doctest\...\>\", line 10, in \<module\> lumberjack() \~\~\~\~\~\~\~\~\~\~\^\^ File \"\<doctest\...\>\", line 4, in lumberjack bright_side_of_life() \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\^\^ IndexError: tuple index out of range **\* print_exc: Traceback (most recent call last): File \"\<doctest\...\>\", line 10, in \<module\> lumberjack() \~\~\~\~\~\~\~\~\~\~\^\^ File \"\<doctest\...\>\", line 4, in lumberjack bright_side_of_life() \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\^\^ IndexError: tuple index out of range**\* format_exc, first and last line: Traceback (most recent call last): IndexError: tuple index out of range **\* format_exception: \[\'Traceback (most recent call last):n\', \' File \"\<doctest default\[0\]\>\", line 10, in \<module\>n lumberjack()n \~\~\~\~\~\~\~\~\~\~\^\^n\', \' File \"\<doctest default\[0\]\>\", line 4, in lumberjackn bright_side_of_life()n \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\^\^n\', \' File \"\<doctest default\[0\]\>\", line 7, in bright_side_of_lifen return tuple()\[0\]n \~\~\~\~\~\~\~\^\^\^n\', \'IndexError: tuple index out of rangen\'\]**\* extract_tb: \[\<FrameSummary file \<doctest\...\>, line 10 in \<module\>\>, \<FrameSummary file \<doctest\...\>, line 4 in lumberjack\>, \<FrameSummary file \<doctest\...\>, line 7 in bright_side_of_life\>\] **\* format_tb: \[\' File \"\<doctest default\[0\]\>\", line 10, in \<module\>n lumberjack()n \~\~\~\~\~\~\~\~\~\~\^\^n\', \' File \"\<doctest default\[0\]\>\", line 4, in lumberjackn bright_side_of_life()n \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\^\^n\', \' File \"\<doctest default\[0\]\>\", line 7, in bright_side_of_lifen return tuple()\[0\]n \~\~\~\~\~\~\~\^\^\^n\'\]**\* tb_lineno: 10
:::

The following example shows the different ways to print and format the stack:

    >>> import traceback
    >>> def another_function():
    ...     lumberstack()
    ...
    >>> def lumberstack():
    ...     traceback.print_stack()
    ...     print(repr(traceback.extract_stack()))
    ...     print(repr(traceback.format_stack()))
    ...
    >>> another_function()
      File "<doctest>", line 10, in <module>
        another_function()
      File "<doctest>", line 3, in another_function
        lumberstack()
      File "<doctest>", line 6, in lumberstack
        traceback.print_stack()
    [('<doctest>', 10, '<module>', 'another_function()'),
     ('<doctest>', 3, 'another_function', 'lumberstack()'),
     ('<doctest>', 7, 'lumberstack', 'print(repr(traceback.extract_stack()))')]
    ['  File "<doctest>", line 10, in <module>\n    another_function()\n',
     '  File "<doctest>", line 3, in another_function\n    lumberstack()\n',
     '  File "<doctest>", line 8, in lumberstack\n    print(repr(traceback.format_stack()))\n']

This last example demonstrates the final few formatting functions:

::: {.doctest options="+NORMALIZE_WHITESPACE"}
\>\>\> import traceback \>\>\> traceback.format_list(\[(\'spam.py\', 3, \'\<module\>\', \'spam.eggs()\'), \... (\'eggs.py\', 42, \'eggs\', \'return \"bacon\"\')\]) \[\' File \"spam.py\", line 3, in \<module\>n spam.eggs()n\', \' File \"eggs.py\", line 42, in eggsn return \"bacon\"n\'\] \>\>\> an_error = IndexError(\'tuple index out of range\') \>\>\> traceback.format_exception_only(an_error) \[\'IndexError: tuple index out of rangen\'\]
:::

## Examples of Using `TracebackException`{.interpreted-text role="class"}

With the helper class, we have more options:

    >>> import sys
    >>> from traceback import TracebackException
    >>>
    >>> def lumberjack():
    ...     bright_side_of_life()
    ...
    >>> def bright_side_of_life():
    ...     t = "bright", "side", "of", "life"
    ...     return t[5]
    ...
    >>> try:
    ...     lumberjack()
    ... except IndexError as e:
    ...     exc = e
    ...
    >>> try:
    ...     try:
    ...         lumberjack()
    ...     except:
    ...         1/0
    ... except Exception as e:
    ...     chained_exc = e
    ...
    >>> # limit works as with the module-level functions
    >>> TracebackException.from_exception(exc, limit=-2).print()
    Traceback (most recent call last):
      File "<python-input-1>", line 6, in lumberjack
        bright_side_of_life()
        ~~~~~~~~~~~~~~~~~~~^^
      File "<python-input-1>", line 10, in bright_side_of_life
        return t[5]
               ~^^^
    IndexError: tuple index out of range

    >>> # capture_locals adds local variables in frames
    >>> TracebackException.from_exception(exc, limit=-2, capture_locals=True).print()
    Traceback (most recent call last):
      File "<python-input-1>", line 6, in lumberjack
        bright_side_of_life()
        ~~~~~~~~~~~~~~~~~~~^^
      File "<python-input-1>", line 10, in bright_side_of_life
        return t[5]
               ~^^^
        t = ("bright", "side", "of", "life")
    IndexError: tuple index out of range

    >>> # The *chain* kwarg to print() controls whether chained
    >>> # exceptions are displayed
    >>> TracebackException.from_exception(chained_exc).print()
    Traceback (most recent call last):
      File "<python-input-19>", line 4, in <module>
        lumberjack()
        ~~~~~~~~~~^^
      File "<python-input-8>", line 7, in lumberjack
        bright_side_of_life()
        ~~~~~~~~~~~~~~~~~~~^^
      File "<python-input-8>", line 11, in bright_side_of_life
        return t[5]
               ~^^^
    IndexError: tuple index out of range

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "<python-input-19>", line 6, in <module>
        1/0
        ~^~
    ZeroDivisionError: division by zero

    >>> TracebackException.from_exception(chained_exc).print(chain=False)
    Traceback (most recent call last):
      File "<python-input-19>", line 6, in <module>
        1/0
        ~^~
    ZeroDivisionError: division by zero
