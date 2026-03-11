# `!pprint`{.interpreted-text role="mod"} \-\-- Data pretty printer

::: {.module synopsis="Data pretty printer."}
pprint
:::

**Source code:** `Lib/pprint.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!pprint`{.interpreted-text role="mod"} module provides a capability to \"pretty-print\" arbitrary Python data structures in a form which can be used as input to the interpreter. If the formatted structures include objects which are not fundamental Python types, the representation may not be loadable. This may be the case if objects such as files, sockets or classes are included, as well as many other objects which are not representable as Python literals.

The formatted representation keeps objects on a single line if it can, and breaks them onto multiple lines if they don\'t fit within the allowed width, adjustable by the *width* parameter defaulting to 80 characters.

::: versionchanged
3.9 Added support for pretty-printing `types.SimpleNamespace`{.interpreted-text role="class"}.
:::

::: versionchanged
3.10 Added support for pretty-printing `dataclasses.dataclass`{.interpreted-text role="class"}.
:::

## Functions {#pprint-functions}

:::: function
pp(object, stream=None, indent=1, width=80, depth=None, \*, compact=False, sort_dicts=False, underscore_numbers=False)

Prints the formatted representation of *object*, followed by a newline. This function may be used in the interactive interpreter instead of the `print`{.interpreted-text role="func"} function for inspecting values. Tip: you can reassign `print = pprint.pp` for use within a scope.

param object
:   The object to be printed.

param stream
:   A file-like object to which the output will be written by calling its `!write`{.interpreted-text role="meth"} method. If `None` (the default), `sys.stdout`{.interpreted-text role="data"} is used.

type stream
:   `file-like object`{.interpreted-text role="term"} \| None

param int indent
:   The amount of indentation added for each nesting level.

param int width
:   The desired maximum number of characters per line in the output. If a structure cannot be formatted within the width constraint, a best effort will be made.

param depth
:   The number of nesting levels which may be printed. If the data structure being printed is too deep, the next contained level is replaced by `...`. If `None` (the default), there is no constraint on the depth of the objects being formatted.

type depth
:   int \| None

param bool compact
:   Control the way long `sequences <sequence>`{.interpreted-text role="term"} are formatted. If `False` (the default), each item of a sequence will be formatted on a separate line, otherwise as many items as will fit within the *width* will be formatted on each output line.

param bool sort_dicts
:   If `True`, dictionaries will be formatted with their keys sorted, otherwise they will be displayed in insertion order (the default).

param bool underscore_numbers
:   If `True`, integers will be formatted with the `_` character for a thousands separator, otherwise underscores are not displayed (the default).

\>\>\> import pprint \>\>\> stuff = \[\'spam\', \'eggs\', \'lumberjack\', \'knights\', \'ni\'\] \>\>\> stuff.insert(0, stuff) \>\>\> pprint.pp(stuff) \[\<Recursion on list with id=\...\>, \'spam\', \'eggs\', \'lumberjack\', \'knights\', \'ni\'\]

::: versionadded
3.8
:::
::::

::: function
pprint(object, stream=None, indent=1, width=80, depth=None, \*, compact=False, sort_dicts=True, underscore_numbers=False)

Alias for `~pprint.pp`{.interpreted-text role="func"} with *sort_dicts* set to `True` by default, which would automatically sort the dictionaries\' keys, you might want to use `~pprint.pp`{.interpreted-text role="func"} instead where it is `False` by default.
:::

::: function
pformat(object, indent=1, width=80, depth=None, \*, compact=False, sort_dicts=True, underscore_numbers=False)

Return the formatted representation of *object* as a string. *indent*, *width*, *depth*, *compact*, *sort_dicts* and *underscore_numbers* are passed to the `PrettyPrinter`{.interpreted-text role="class"} constructor as formatting parameters and their meanings are as described in the documentation above.
:::

:::: function
isreadable(object)

::: index
pair: built-in function; eval
:::

Determine if the formatted representation of *object* is \"readable\", or can be used to reconstruct the value using `eval`{.interpreted-text role="func"}. This always returns `False` for recursive objects.

> \>\>\> pprint.isreadable(stuff) False
::::

::: function
isrecursive(object)

Determine if *object* requires a recursive representation. This function is subject to the same limitations as noted in `saferepr`{.interpreted-text role="func"} below and may raise an `RecursionError`{.interpreted-text role="exc"} if it fails to detect a recursive object.
:::

::: function
saferepr(object)

Return a string representation of *object*, protected against recursion in some common data structures, namely instances of `dict`{.interpreted-text role="class"}, `list`{.interpreted-text role="class"} and `tuple`{.interpreted-text role="class"} or subclasses whose `__repr__` has not been overridden. If the representation of object exposes a recursive entry, the recursive reference will be represented as `<Recursion on typename with id=number>`. The representation is not otherwise formatted.

\>\>\> pprint.saferepr(stuff) \"\[\<Recursion on list with id=\...\>, \'spam\', \'eggs\', \'lumberjack\', \'knights\', \'ni\'\]\"
:::

## PrettyPrinter Objects

::: index
single: \...; placeholder
:::

::::::: {.PrettyPrinter(indent=1, .width=80, .depth=None, .stream=None, .*, .\\ .compact=False, .sort_dicts=True, .underscore_numbers=False)}
Construct a `PrettyPrinter`{.interpreted-text role="class"} instance.

Arguments have the same meaning as for `~pprint.pp`{.interpreted-text role="func"}. Note that they are in a different order, and that *sort_dicts* defaults to `True`.

\>\>\> import pprint \>\>\> stuff = \[\'spam\', \'eggs\', \'lumberjack\', \'knights\', \'ni\'\] \>\>\> stuff.insert(0, stuff\[:\]) \>\>\> pp = pprint.PrettyPrinter(indent=4) \>\>\> pp.pprint(stuff) \[ \[\'spam\', \'eggs\', \'lumberjack\', \'knights\', \'ni\'\], \'spam\', \'eggs\', \'lumberjack\', \'knights\', \'ni\'\] \>\>\> pp = pprint.PrettyPrinter(width=41, compact=True) \>\>\> pp.pprint(stuff) \[\[\'spam\', \'eggs\', \'lumberjack\', \'knights\', \'ni\'\], \'spam\', \'eggs\', \'lumberjack\', \'knights\', \'ni\'\] \>\>\> tup = (\'spam\', (\'eggs\', (\'lumberjack\', (\'knights\', (\'ni\', (\'dead\', \... (\'parrot\', (\'fresh fruit\',)))))))) \>\>\> pp = pprint.PrettyPrinter(depth=6) \>\>\> pp.pprint(tup) (\'spam\', (\'eggs\', (\'lumberjack\', (\'knights\', (\'ni\', (\'dead\', (\...)))))))

::: versionchanged
3.4 Added the *compact* parameter.
:::

::: versionchanged
3.8 Added the *sort_dicts* parameter.
:::

::: versionchanged
3.10 Added the *underscore_numbers* parameter.
:::

::: versionchanged
3.11 No longer attempts to write to `!sys.stdout`{.interpreted-text role="data"} if it is `None`.
:::
:::::::

`PrettyPrinter`{.interpreted-text role="class"} instances have the following methods:

::: method
PrettyPrinter.pformat(object)

Return the formatted representation of *object*. This takes into account the options passed to the `PrettyPrinter`{.interpreted-text role="class"} constructor.
:::

::: method
PrettyPrinter.pprint(object)

Print the formatted representation of *object* on the configured stream, followed by a newline.
:::

The following methods provide the implementations for the corresponding functions of the same names. Using these methods on an instance is slightly more efficient since new `PrettyPrinter`{.interpreted-text role="class"} objects don\'t need to be created.

:::: method
PrettyPrinter.isreadable(object)

::: index
pair: built-in function; eval
:::

Determine if the formatted representation of the object is \"readable,\" or can be used to reconstruct the value using `eval`{.interpreted-text role="func"}. Note that this returns `False` for recursive objects. If the *depth* parameter of the `PrettyPrinter`{.interpreted-text role="class"} is set and the object is deeper than allowed, this returns `False`.
::::

::: method
PrettyPrinter.isrecursive(object)

Determine if the object requires a recursive representation.
:::

This method is provided as a hook to allow subclasses to modify the way objects are converted to strings. The default implementation uses the internals of the `saferepr`{.interpreted-text role="func"} implementation.

::: method
PrettyPrinter.format(object, context, maxlevels, level)

Returns three values: the formatted version of *object* as a string, a flag indicating whether the result is readable, and a flag indicating whether recursion was detected. The first argument is the object to be presented. The second is a dictionary which contains the `id`{.interpreted-text role="func"} of objects that are part of the current presentation context (direct and indirect containers for *object* that are affecting the presentation) as the keys; if an object needs to be presented which is already represented in *context*, the third return value should be `True`. Recursive calls to the `.format`{.interpreted-text role="meth"} method should add additional entries for containers to this dictionary. The third argument, *maxlevels*, gives the requested limit to recursion; this will be `0` if there is no requested limit. This argument should be passed unmodified to recursive calls. The fourth argument, *level*, gives the current level; recursive calls should be passed a value less than that of the current call.
:::

## Example {#pprint-example}

To demonstrate several uses of the `~pprint.pp`{.interpreted-text role="func"} function and its parameters, let\'s fetch information about a project from [PyPI](https://pypi.org):

    >>> import json
    >>> import pprint
    >>> from urllib.request import urlopen
    >>> with urlopen('https://pypi.org/pypi/sampleproject/1.2.0/json') as resp:
    ...     project_info = json.load(resp)['info']

In its basic form, `~pprint.pp`{.interpreted-text role="func"} shows the whole object:

    >>> pprint.pp(project_info)
    {'author': 'The Python Packaging Authority',
     'author_email': 'pypa-dev@googlegroups.com',
     'bugtrack_url': None,
     'classifiers': ['Development Status :: 3 - Alpha',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Programming Language :: Python :: 2',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.2',
                     'Programming Language :: Python :: 3.3',
                     'Programming Language :: Python :: 3.4',
                     'Topic :: Software Development :: Build Tools'],
     'description': 'A sample Python project\n'
                    '=======================\n'
                    '\n'
                    'This is the description file for the project.\n'
                    '\n'
                    'The file should use UTF-8 encoding and be written using '
                    'ReStructured Text. It\n'
                    'will be used to generate the project webpage on PyPI, and '
                    'should be written for\n'
                    'that purpose.\n'
                    '\n'
                    'Typical contents for this file would include an overview of '
                    'the project, basic\n'
                    'usage examples, etc. Generally, including the project '
                    'changelog in here is not\n'
                    'a good idea, although a simple "What\'s New" section for the '
                    'most recent version\n'
                    'may be appropriate.',
     'description_content_type': None,
     'docs_url': None,
     'download_url': 'UNKNOWN',
     'downloads': {'last_day': -1, 'last_month': -1, 'last_week': -1},
     'home_page': 'https://github.com/pypa/sampleproject',
     'keywords': 'sample setuptools development',
     'license': 'MIT',
     'maintainer': None,
     'maintainer_email': None,
     'name': 'sampleproject',
     'package_url': 'https://pypi.org/project/sampleproject/',
     'platform': 'UNKNOWN',
     'project_url': 'https://pypi.org/project/sampleproject/',
     'project_urls': {'Download': 'UNKNOWN',
                      'Homepage': 'https://github.com/pypa/sampleproject'},
     'release_url': 'https://pypi.org/project/sampleproject/1.2.0/',
     'requires_dist': None,
     'requires_python': None,
     'summary': 'A sample Python project',
     'version': '1.2.0'}

The result can be limited to a certain *depth* (ellipsis is used for deeper contents):

    >>> pprint.pp(project_info, depth=1)
    {'author': 'The Python Packaging Authority',
     'author_email': 'pypa-dev@googlegroups.com',
     'bugtrack_url': None,
     'classifiers': [...],
     'description': 'A sample Python project\n'
                    '=======================\n'
                    '\n'
                    'This is the description file for the project.\n'
                    '\n'
                    'The file should use UTF-8 encoding and be written using '
                    'ReStructured Text. It\n'
                    'will be used to generate the project webpage on PyPI, and '
                    'should be written for\n'
                    'that purpose.\n'
                    '\n'
                    'Typical contents for this file would include an overview of '
                    'the project, basic\n'
                    'usage examples, etc. Generally, including the project '
                    'changelog in here is not\n'
                    'a good idea, although a simple "What\'s New" section for the '
                    'most recent version\n'
                    'may be appropriate.',
     'description_content_type': None,
     'docs_url': None,
     'download_url': 'UNKNOWN',
     'downloads': {...},
     'home_page': 'https://github.com/pypa/sampleproject',
     'keywords': 'sample setuptools development',
     'license': 'MIT',
     'maintainer': None,
     'maintainer_email': None,
     'name': 'sampleproject',
     'package_url': 'https://pypi.org/project/sampleproject/',
     'platform': 'UNKNOWN',
     'project_url': 'https://pypi.org/project/sampleproject/',
     'project_urls': {...},
     'release_url': 'https://pypi.org/project/sampleproject/1.2.0/',
     'requires_dist': None,
     'requires_python': None,
     'summary': 'A sample Python project',
     'version': '1.2.0'}

Additionally, maximum character *width* can be suggested. If a long object cannot be split, the specified width will be exceeded:

    >>> pprint.pp(project_info, depth=1, width=60)
    {'author': 'The Python Packaging Authority',
     'author_email': 'pypa-dev@googlegroups.com',
     'bugtrack_url': None,
     'classifiers': [...],
     'description': 'A sample Python project\n'
                    '=======================\n'
                    '\n'
                    'This is the description file for the '
                    'project.\n'
                    '\n'
                    'The file should use UTF-8 encoding and be '
                    'written using ReStructured Text. It\n'
                    'will be used to generate the project '
                    'webpage on PyPI, and should be written '
                    'for\n'
                    'that purpose.\n'
                    '\n'
                    'Typical contents for this file would '
                    'include an overview of the project, '
                    'basic\n'
                    'usage examples, etc. Generally, including '
                    'the project changelog in here is not\n'
                    'a good idea, although a simple "What\'s '
                    'New" section for the most recent version\n'
                    'may be appropriate.',
     'description_content_type': None,
     'docs_url': None,
     'download_url': 'UNKNOWN',
     'downloads': {...},
     'home_page': 'https://github.com/pypa/sampleproject',
     'keywords': 'sample setuptools development',
     'license': 'MIT',
     'maintainer': None,
     'maintainer_email': None,
     'name': 'sampleproject',
     'package_url': 'https://pypi.org/project/sampleproject/',
     'platform': 'UNKNOWN',
     'project_url': 'https://pypi.org/project/sampleproject/',
     'project_urls': {...},
     'release_url': 'https://pypi.org/project/sampleproject/1.2.0/',
     'requires_dist': None,
     'requires_python': None,
     'summary': 'A sample Python project',
     'version': '1.2.0'}
