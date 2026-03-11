# `!textwrap`{.interpreted-text role="mod"} \-\-- Text wrapping and filling

::: {.module synopsis="Text wrapping and filling"}
textwrap
:::

**Source code:** `Lib/textwrap.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!textwrap`{.interpreted-text role="mod"} module provides some convenience functions, as well as `TextWrapper`{.interpreted-text role="class"}, the class that does all the work. If you\'re just wrapping or filling one or two text strings, the convenience functions should be good enough; otherwise, you should use an instance of `TextWrapper`{.interpreted-text role="class"} for efficiency.

::: function
wrap(text, width=70, \*, initial_indent=\"\", subsequent_indent=\"\", expand_tabs=True, replace_whitespace=True, fix_sentence_endings=False, break_long_words=True, drop_whitespace=True, break_on_hyphens=True, tabsize=8, max_lines=None, placeholder=\' \[\...\]\')

Wraps the single paragraph in *text* (a string) so every line is at most *width* characters long. Returns a list of output lines, without final newlines.

Optional keyword arguments correspond to the instance attributes of `TextWrapper`{.interpreted-text role="class"}, documented below.

See the `TextWrapper.wrap`{.interpreted-text role="meth"} method for additional details on how `wrap`{.interpreted-text role="func"} behaves.
:::

::: function
fill(text, width=70, \*, initial_indent=\"\", subsequent_indent=\"\", expand_tabs=True, replace_whitespace=True, fix_sentence_endings=False, break_long_words=True, drop_whitespace=True, break_on_hyphens=True, tabsize=8, max_lines=None, placeholder=\' \[\...\]\')

Wraps the single paragraph in *text*, and returns a single string containing the wrapped paragraph. `fill`{.interpreted-text role="func"} is shorthand for :

    "\n".join(wrap(text, ...))

In particular, `fill`{.interpreted-text role="func"} accepts exactly the same keyword arguments as `wrap`{.interpreted-text role="func"}.
:::

:::: function
shorten(text, width, \*, fix_sentence_endings=False, break_long_words=True, break_on_hyphens=True, placeholder=\' \[\...\]\')

Collapse and truncate the given *text* to fit in the given *width*.

First the whitespace in *text* is collapsed (all whitespace is replaced by single spaces). If the result fits in the *width*, it is returned. Otherwise, enough words are dropped from the end so that the remaining words plus the *placeholder* fit within *width*:

    >>> textwrap.shorten("Hello  world!", width=12)
    'Hello world!'
    >>> textwrap.shorten("Hello  world!", width=11)
    'Hello [...]'
    >>> textwrap.shorten("Hello world", width=10, placeholder="...")
    'Hello...'

Optional keyword arguments correspond to the instance attributes of `TextWrapper`{.interpreted-text role="class"}, documented below. Note that the whitespace is collapsed before the text is passed to the `TextWrapper`{.interpreted-text role="class"} `fill`{.interpreted-text role="meth"} function, so changing the value of `.tabsize`{.interpreted-text role="attr"}, `.expand_tabs`{.interpreted-text role="attr"}, `.drop_whitespace`{.interpreted-text role="attr"}, and `.replace_whitespace`{.interpreted-text role="attr"} will have no effect.

::: versionadded
3.4
:::
::::

:::: function
dedent(text)

Remove any common leading whitespace from every line in *text*.

This can be used to make triple-quoted strings line up with the left edge of the display, while still presenting them in the source code in indented form.

Note that tabs and spaces are both treated as whitespace, but they are not equal: the lines `"  hello"` and `"\thello"` are considered to have no common leading whitespace.

Lines containing only whitespace are ignored in the input and normalized to a single newline character in the output.

For example:

    def test():
        # end first line with \ to avoid the empty line!
        s = '''\
        hello
          world
        '''
        print(repr(s))          # prints '    hello\n      world\n    '
        print(repr(dedent(s)))  # prints 'hello\n  world\n'

::: versionchanged
3.14 The `!dedent`{.interpreted-text role="func"} function now correctly normalizes blank lines containing only whitespace characters. Previously, the implementation only normalized blank lines containing tabs and spaces.
:::
::::

:::: function
indent(text, prefix, predicate=None)

Add *prefix* to the beginning of selected lines in *text*.

Lines are separated by calling `text.splitlines(True)`.

By default, *prefix* is added to all lines that do not consist solely of whitespace (including any line endings).

For example:

    >>> s = 'hello\n\n \nworld'
    >>> indent(s, '  ')
    '  hello\n\n \n  world'

The optional *predicate* argument can be used to control which lines are indented. For example, it is easy to add *prefix* to even empty and whitespace-only lines:

    >>> print(indent(s, '+ ', lambda line: True))
    + hello
    +
    +
    + world

::: versionadded
3.3
:::
::::

`wrap`{.interpreted-text role="func"}, `fill`{.interpreted-text role="func"} and `shorten`{.interpreted-text role="func"} work by creating a `TextWrapper`{.interpreted-text role="class"} instance and calling a single method on it. That instance is not reused, so for applications that process many text strings using `wrap`{.interpreted-text role="func"} and/or `fill`{.interpreted-text role="func"}, it may be more efficient to create your own `TextWrapper`{.interpreted-text role="class"} object.

Text is preferably wrapped on whitespaces and right after the hyphens in hyphenated words; only then will long words be broken if necessary, unless `TextWrapper.break_long_words`{.interpreted-text role="attr"} is set to false.

::::::::::::::::::::::::: TextWrapper(**kwargs)
The `TextWrapper`{.interpreted-text role="class"} constructor accepts a number of optional keyword arguments. Each keyword argument corresponds to an instance attribute, so for example :

    wrapper = TextWrapper(initial_indent="* ")

is the same as :

    wrapper = TextWrapper()
    wrapper.initial_indent = "* "

You can reuse the same `TextWrapper`{.interpreted-text role="class"} object many times, and you can change any of its options through direct assignment to instance attributes between uses.

The `TextWrapper`{.interpreted-text role="class"} instance attributes (and keyword arguments to the constructor) are as follows:

::: attribute
width

(default: `70`) The maximum length of wrapped lines. As long as there are no individual words in the input text longer than `width`{.interpreted-text role="attr"}, `TextWrapper`{.interpreted-text role="class"} guarantees that no output line will be longer than `width`{.interpreted-text role="attr"} characters.
:::

::: attribute
expand_tabs

(default: `True`) If true, then all tab characters in *text* will be expanded to spaces using the `~str.expandtabs`{.interpreted-text role="meth"} method of *text*.
:::

:::: attribute
tabsize

(default: `8`) If `expand_tabs`{.interpreted-text role="attr"} is true, then all tab characters in *text* will be expanded to zero or more spaces, depending on the current column and the given tab size.

::: versionadded
3.3
:::
::::

::::::: attribute
replace_whitespace

(default: `True`) If true, after tab expansion but before wrapping, the `wrap`{.interpreted-text role="meth"} method will replace each whitespace character with a single space. The whitespace characters replaced are as follows: tab, newline, vertical tab, formfeed, and carriage return (`'\t\n\v\f\r'`).

:::: note
::: title
Note
:::

If `expand_tabs`{.interpreted-text role="attr"} is false and `replace_whitespace`{.interpreted-text role="attr"} is true, each tab character will be replaced by a single space, which is *not* the same as tab expansion.
::::

:::: note
::: title
Note
:::

If `replace_whitespace`{.interpreted-text role="attr"} is false, newlines may appear in the middle of a line and cause strange output. For this reason, text should be split into paragraphs (using `str.splitlines`{.interpreted-text role="meth"} or similar) which are wrapped separately.
::::
:::::::

::: attribute
drop_whitespace

(default: `True`) If true, whitespace at the beginning and ending of every line (after wrapping but before indenting) is dropped. Whitespace at the beginning of the paragraph, however, is not dropped if non-whitespace follows it. If whitespace being dropped takes up an entire line, the whole line is dropped.
:::

::: attribute
initial_indent

(default: `''`) String that will be prepended to the first line of wrapped output. Counts towards the length of the first line. The empty string is not indented.
:::

::: attribute
subsequent_indent

(default: `''`) String that will be prepended to all lines of wrapped output except the first. Counts towards the length of each line except the first.
:::

::: attribute
fix_sentence_endings

(default: `False`) If true, `TextWrapper`{.interpreted-text role="class"} attempts to detect sentence endings and ensure that sentences are always separated by exactly two spaces. This is generally desired for text in a monospaced font. However, the sentence detection algorithm is imperfect: it assumes that a sentence ending consists of a lowercase letter followed by one of `'.'`, `'!'`, or `'?'`, possibly followed by one of `'"'` or `"'"`, followed by a space. One problem with this algorithm is that it is unable to detect the difference between \"Dr.\" in :

    [...] Dr. Frankenstein's monster [...]

and \"Spot.\" in :

    [...] See Spot. See Spot run [...]

`fix_sentence_endings`{.interpreted-text role="attr"} is false by default.

Since the sentence detection algorithm relies on `string.lowercase` for the definition of \"lowercase letter\", and a convention of using two spaces after a period to separate sentences on the same line, it is specific to English-language texts.
:::

::: attribute
break_long_words

(default: `True`) If true, then words longer than `width`{.interpreted-text role="attr"} will be broken in order to ensure that no lines are longer than `width`{.interpreted-text role="attr"}. If it is false, long words will not be broken, and some lines may be longer than `width`{.interpreted-text role="attr"}. (Long words will be put on a line by themselves, in order to minimize the amount by which `width`{.interpreted-text role="attr"} is exceeded.)
:::

::: attribute
break_on_hyphens

(default: `True`) If true, wrapping will occur preferably on whitespaces and right after hyphens in compound words, as it is customary in English. If false, only whitespaces will be considered as potentially good places for line breaks, but you need to set `break_long_words`{.interpreted-text role="attr"} to false if you want truly insecable words. Default behaviour in previous versions was to always allow breaking hyphenated words.
:::

:::: attribute
max_lines

(default: `None`) If not `None`, then the output will contain at most *max_lines* lines, with *placeholder* appearing at the end of the output.

::: versionadded
3.4
:::
::::

::: index
single: \...; placeholder
:::

:::: attribute
placeholder

(default: `' [...]'`) String that will appear at the end of the output text if it has been truncated.

::: versionadded
3.4
:::
::::

`TextWrapper`{.interpreted-text role="class"} also provides some public methods, analogous to the module-level convenience functions:

::: method
wrap(text)

Wraps the single paragraph in *text* (a string) so every line is at most `width`{.interpreted-text role="attr"} characters long. All wrapping options are taken from instance attributes of the `TextWrapper`{.interpreted-text role="class"} instance. Returns a list of output lines, without final newlines. If the wrapped output has no content, the returned list is empty.
:::

::: method
fill(text)

Wraps the single paragraph in *text*, and returns a single string containing the wrapped paragraph.
:::
:::::::::::::::::::::::::
