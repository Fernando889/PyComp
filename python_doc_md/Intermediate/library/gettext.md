# `!gettext`{.interpreted-text role="mod"} \-\-- Multilingual internationalization services

::: {.module synopsis="Multilingual internationalization services."}
gettext
:::

**Source code:** `Lib/gettext.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!gettext`{.interpreted-text role="mod"} module provides internationalization (I18N) and localization (L10N) services for your Python modules and applications. It supports both the GNU `gettext`{.interpreted-text role="program"} message catalog API and a higher level, class-based API that may be more appropriate for Python files. The interface described below allows you to write your module and application messages in one natural language, and provide a catalog of translated messages for running under different natural languages.

Some hints on localizing your Python modules and applications are also given.

## GNU `gettext`{.interpreted-text role="program"} API

The `!gettext`{.interpreted-text role="mod"} module defines the following API, which is very similar to the GNU `gettext`{.interpreted-text role="program"} API. If you use this API you will affect the translation of your entire application globally. Often this is what you want if your application is monolingual, with the choice of language dependent on the locale of your user. If you are localizing a Python module, or if your application needs to switch languages on the fly, you probably want to use the class-based API instead.

::: function
bindtextdomain(domain, localedir=None)

Bind the *domain* to the locale directory *localedir*. More concretely, `!gettext`{.interpreted-text role="mod"} will look for binary `.mo`{.interpreted-text role="file"} files for the given domain using the path (on Unix): `{localedir}/{language}/LC_MESSAGES/{domain}.mo`{.interpreted-text role="file"}, where *language* is searched for in the environment variables `LANGUAGE`{.interpreted-text role="envvar"}, `LC_ALL`{.interpreted-text role="envvar"}, `LC_MESSAGES`{.interpreted-text role="envvar"}, and `LANG`{.interpreted-text role="envvar"} respectively.

If *localedir* is omitted or `None`, then the current binding for *domain* is returned.[^1]
:::

::: function
textdomain(domain=None)

Change or query the current global domain. If *domain* is `None`, then the current global domain is returned, otherwise the global domain is set to *domain*, which is returned.
:::

::: index
single: \_ (underscore); gettext
:::

::: function
gettext(message)

Return the localized translation of *message*, based on the current global domain, language, and locale directory. This function is usually aliased as `!_`{.interpreted-text role="func"} in the local namespace (see examples below).
:::

::: function
dgettext(domain, message)

Like `.gettext`{.interpreted-text role="func"}, but look the message up in the specified *domain*.
:::

::: function
ngettext(singular, plural, n)

Like `.gettext`{.interpreted-text role="func"}, but consider plural forms. If a translation is found, apply the plural formula to *n*, and return the resulting message (some languages have more than two plural forms). If no translation is found, return *singular* if *n* is 1; return *plural* otherwise.

The Plural formula is taken from the catalog header. It is a C or Python expression that has a free variable *n*; the expression evaluates to the index of the plural in the catalog. See [the GNU gettext documentation](https://www.gnu.org/software/gettext/manual/gettext.html) for the precise syntax to be used in `.po`{.interpreted-text role="file"} files and the formulas for a variety of languages.
:::

::: function
dngettext(domain, singular, plural, n)

Like `ngettext`{.interpreted-text role="func"}, but look the message up in the specified *domain*.
:::

::: function
pgettext(context, message)
:::

::: function
dpgettext(domain, context, message)
:::

::: function
npgettext(context, singular, plural, n)
:::

:::: function
dnpgettext(domain, context, singular, plural, n)

Similar to the corresponding functions without the `p` in the prefix (that is, `gettext`{.interpreted-text role="func"}, `dgettext`{.interpreted-text role="func"}, `ngettext`{.interpreted-text role="func"}, `dngettext`{.interpreted-text role="func"}), but the translation is restricted to the given message *context*.

::: versionadded
3.8
:::
::::

Note that GNU `gettext`{.interpreted-text role="program"} also defines a `!dcgettext`{.interpreted-text role="func"} method, but this was deemed not useful and so it is currently unimplemented.

Here\'s an example of typical usage for this API:

    import gettext
    gettext.bindtextdomain('myapplication', '/path/to/my/language/directory')
    gettext.textdomain('myapplication')
    _ = gettext.gettext
    # ...
    print(_('This is a translatable string.'))

## Class-based API

The class-based API of the `!gettext`{.interpreted-text role="mod"} module gives you more flexibility and greater convenience than the GNU `gettext`{.interpreted-text role="program"} API. It is the recommended way of localizing your Python applications and modules. `!gettext`{.interpreted-text role="mod"} defines a `GNUTranslations`{.interpreted-text role="class"} class which implements the parsing of GNU `.mo`{.interpreted-text role="file"} format files, and has methods for returning strings. Instances of this class can also install themselves in the built-in namespace as the function `!_`{.interpreted-text role="func"}.

::: function
find(domain, localedir=None, languages=None, all=False)

This function implements the standard `.mo`{.interpreted-text role="file"} file search algorithm. It takes a *domain*, identical to what `textdomain`{.interpreted-text role="func"} takes. Optional *localedir* is as in `bindtextdomain`{.interpreted-text role="func"}. Optional *languages* is a list of strings, where each string is a language code.

If *localedir* is not given, then the default system locale directory is used. [^2] If *languages* is not given, then the following environment variables are searched: `LANGUAGE`{.interpreted-text role="envvar"}, `LC_ALL`{.interpreted-text role="envvar"}, `LC_MESSAGES`{.interpreted-text role="envvar"}, and `LANG`{.interpreted-text role="envvar"}. The first one returning a non-empty value is used for the *languages* variable. The environment variables should contain a colon separated list of languages, which will be split on the colon to produce the expected list of language code strings.

`find`{.interpreted-text role="func"} then expands and normalizes the languages, and then iterates through them, searching for an existing file built of these components:

`{localedir}/{language}/LC_MESSAGES/{domain}.mo`{.interpreted-text role="file"}

The first such file name that exists is returned by `find`{.interpreted-text role="func"}. If no such file is found, then `None` is returned. If *all* is given, it returns a list of all file names, in the order in which they appear in the languages list or the environment variables.
:::

::::: function
translation(domain, localedir=None, languages=None, [class]()=None, fallback=False)

Return a `*Translations` instance based on the *domain*, *localedir*, and *languages*, which are first passed to `find`{.interpreted-text role="func"} to get a list of the associated `.mo`{.interpreted-text role="file"} file paths. Instances with identical `.mo`{.interpreted-text role="file"} file names are cached. The actual class instantiated is *class\_* if provided, otherwise `GNUTranslations`{.interpreted-text role="class"}. The class\'s constructor must take a single `file object`{.interpreted-text role="term"} argument.

If multiple files are found, later files are used as fallbacks for earlier ones. To allow setting the fallback, `copy.copy`{.interpreted-text role="func"} is used to clone each translation object from the cache; the actual instance data is still shared with the cache.

If no `.mo`{.interpreted-text role="file"} file is found, this function raises `OSError`{.interpreted-text role="exc"} if *fallback* is false (which is the default), and returns a `NullTranslations`{.interpreted-text role="class"} instance if *fallback* is true.

::: versionchanged
3.3 `IOError`{.interpreted-text role="exc"} used to be raised, it is now an alias of `OSError`{.interpreted-text role="exc"}.
:::

::: versionchanged
3.11 *codeset* parameter is removed.
:::
:::::

:::: function
install(domain, localedir=None, \*, names=None)

This installs the function `!_`{.interpreted-text role="func"} in Python\'s builtins namespace, based on *domain* and *localedir* which are passed to the function `translation`{.interpreted-text role="func"}.

For the *names* parameter, please see the description of the translation object\'s `~NullTranslations.install`{.interpreted-text role="meth"} method.

As seen below, you usually mark the strings in your application that are candidates for translation, by wrapping them in a call to the `!_`{.interpreted-text role="func"} function, like this:

    print(_('This string will be translated.'))

For convenience, you want the `!_`{.interpreted-text role="func"} function to be installed in Python\'s builtins namespace, so it is easily accessible in all modules of your application.

::: versionchanged
3.11 *names* is now a keyword-only parameter.
:::
::::

### The `NullTranslations`{.interpreted-text role="class"} class

Translation classes are what actually implement the translation of original source file message strings to translated message strings. The base class used by all translation classes is `NullTranslations`{.interpreted-text role="class"}; this provides the basic interface you can use to write your own specialized translation classes. Here are the methods of `!NullTranslations`{.interpreted-text role="class"}:

::::::::::::::: NullTranslations(fp=None)
Takes an optional `file object`{.interpreted-text role="term"} *fp*, which is ignored by the base class. Initializes \"protected\" instance variables *\_info* and *\_charset* which are set by derived classes, as well as *\_fallback*, which is set through `add_fallback`{.interpreted-text role="meth"}. It then calls `self._parse(fp)` if *fp* is not `None`.

::: method
[parse]{#parse}(fp)

No-op in the base class, this method takes file object *fp*, and reads the data from the file, initializing its message catalog. If you have an unsupported message catalog file format, you should override this method to parse your format.
:::

::: method
add_fallback(fallback)

Add *fallback* as the fallback object for the current translation object. A translation object should consult the fallback if it cannot provide a translation for a given message.
:::

::: method
gettext(message)

If a fallback has been set, forward `!gettext`{.interpreted-text role="meth"} to the fallback. Otherwise, return *message*. Overridden in derived classes.
:::

::: method
ngettext(singular, plural, n)

If a fallback has been set, forward `!ngettext`{.interpreted-text role="meth"} to the fallback. Otherwise, return *singular* if *n* is 1; return *plural* otherwise. Overridden in derived classes.
:::

:::: method
pgettext(context, message)

If a fallback has been set, forward `pgettext`{.interpreted-text role="meth"} to the fallback. Otherwise, return the translated message. Overridden in derived classes.

::: versionadded
3.8
:::
::::

:::: method
npgettext(context, singular, plural, n)

If a fallback has been set, forward `npgettext`{.interpreted-text role="meth"} to the fallback. Otherwise, return the translated message. Overridden in derived classes.

::: versionadded
3.8
:::
::::

::: method
info()

Return a dictionary containing the metadata found in the message catalog file.
:::

::: method
charset()

Return the encoding of the message catalog file.
:::

:::: method
install(names=None)

This method installs `.gettext`{.interpreted-text role="meth"} into the built-in namespace, binding it to `_`.

If the *names* parameter is given, it must be a sequence containing the names of functions you want to install in the builtins namespace in addition to `!_`{.interpreted-text role="func"}. Supported names are `'gettext'`, `'ngettext'`, `'pgettext'`, and `'npgettext'`.

Note that this is only one way, albeit the most convenient way, to make the `!_`{.interpreted-text role="func"} function available to your application. Because it affects the entire application globally, and specifically the built-in namespace, localized modules should never install `!_`{.interpreted-text role="func"}. Instead, they should use this code to make `!_`{.interpreted-text role="func"} available to their module:

    import gettext
    t = gettext.translation('mymodule', ...)
    _ = t.gettext

This puts `!_`{.interpreted-text role="func"} only in the module\'s global namespace and so only affects calls within this module.

::: versionchanged
3.8 Added `'pgettext'` and `'npgettext'`.
:::
::::
:::::::::::::::

### The `GNUTranslations`{.interpreted-text role="class"} class

The `!gettext`{.interpreted-text role="mod"} module provides one additional class derived from `NullTranslations`{.interpreted-text role="class"}: `GNUTranslations`{.interpreted-text role="class"}. This class overrides `!_parse`{.interpreted-text role="meth"} to enable reading GNU `gettext`{.interpreted-text role="program"} format `.mo`{.interpreted-text role="file"} files in both big-endian and little-endian format.

`GNUTranslations`{.interpreted-text role="class"} parses optional metadata out of the translation catalog. It is convention with GNU `gettext`{.interpreted-text role="program"} to include metadata as the translation for the empty string. This metadata is in `822`{.interpreted-text role="rfc"}-style `key: value` pairs, and should contain the `Project-Id-Version` key. If the key `Content-Type` is found, then the `charset` property is used to initialize the \"protected\" `!_charset`{.interpreted-text role="attr"} instance variable, defaulting to `None` if not found. If the charset encoding is specified, then all message ids and message strings read from the catalog are converted to Unicode using this encoding, else ASCII is assumed.

Since message ids are read as Unicode strings too, all `*gettext()` methods will assume message ids as Unicode strings, not byte strings.

The entire set of key/value pairs are placed into a dictionary and set as the \"protected\" `!_info`{.interpreted-text role="attr"} instance variable.

If the `.mo`{.interpreted-text role="file"} file\'s magic number is invalid, the major version number is unexpected, or if other problems occur while reading the file, instantiating a `GNUTranslations`{.interpreted-text role="class"} class can raise `OSError`{.interpreted-text role="exc"}.

::::::::: GNUTranslations
The following methods are overridden from the base class implementation:

::: method
gettext(message)

Look up the *message* id in the catalog and return the corresponding message string, as a Unicode string. If there is no entry in the catalog for the *message* id, and a fallback has been set, the look up is forwarded to the fallback\'s `~NullTranslations.gettext`{.interpreted-text role="meth"} method. Otherwise, the *message* id is returned.
:::

::: method
ngettext(singular, plural, n)

Do a plural-forms lookup of a message id. *singular* is used as the message id for purposes of lookup in the catalog, while *n* is used to determine which plural form to use. The returned message string is a Unicode string.

If the message id is not found in the catalog, and a fallback is specified, the request is forwarded to the fallback\'s `~NullTranslations.ngettext`{.interpreted-text role="meth"} method. Otherwise, when *n* is 1 *singular* is returned, and *plural* is returned in all other cases.

Here is an example:

    n = len(os.listdir('.'))
    cat = GNUTranslations(somefile)
    message = cat.ngettext(
        'There is %(num)d file in this directory',
        'There are %(num)d files in this directory',
        n) % {'num': n}
:::

:::: method
pgettext(context, message)

Look up the *context* and *message* id in the catalog and return the corresponding message string, as a Unicode string. If there is no entry in the catalog for the *message* id and *context*, and a fallback has been set, the look up is forwarded to the fallback\'s `pgettext`{.interpreted-text role="meth"} method. Otherwise, the *message* id is returned.

::: versionadded
3.8
:::
::::

:::: method
npgettext(context, singular, plural, n)

Do a plural-forms lookup of a message id. *singular* is used as the message id for purposes of lookup in the catalog, while *n* is used to determine which plural form to use.

If the message id for *context* is not found in the catalog, and a fallback is specified, the request is forwarded to the fallback\'s `npgettext`{.interpreted-text role="meth"} method. Otherwise, when *n* is 1 *singular* is returned, and *plural* is returned in all other cases.

::: versionadded
3.8
:::
::::
:::::::::

### Solaris message catalog support

The Solaris operating system defines its own binary `.mo`{.interpreted-text role="file"} file format, but since no documentation can be found on this format, it is not supported at this time.

### The Catalog constructor

::: index
single: GNOME
:::

GNOME uses a version of the `!gettext`{.interpreted-text role="mod"} module by James Henstridge, but this version has a slightly different API. Its documented usage was:

    import gettext
    cat = gettext.Catalog(domain, localedir)
    _ = cat.gettext
    print(_('hello world'))

For compatibility with this older module, the function `!Catalog`{.interpreted-text role="func"} is an alias for the `translation`{.interpreted-text role="func"} function described above.

One difference between this module and Henstridge\'s: his catalog objects supported access through a mapping API, but this appears to be unused and so is not currently supported.

## Internationalizing your programs and modules {#i18n-howto}

Internationalization (I18N) refers to the operation by which a program is made aware of multiple languages. Localization (L10N) refers to the adaptation of your program, once internationalized, to the local language and cultural habits. In order to provide multilingual messages for your Python programs, you need to take the following steps:

1.  prepare your program or module by specially marking translatable strings
2.  run a suite of tools over your marked files to generate raw messages catalogs
3.  create language-specific translations of the message catalogs
4.  use the `!gettext`{.interpreted-text role="mod"} module so that message strings are properly translated

In order to prepare your code for I18N, you need to look at all the strings in your files. Any string that needs to be translated should be marked by wrapping it in `_('...')` \-\-- that is, a call to the function `_ <gettext>`{.interpreted-text role="func"}. For example:

    filename = 'mylog.txt'
    message = _('writing a log message')
    with open(filename, 'w') as fp:
        fp.write(message)

In this example, the string `'writing a log message'` is marked as a candidate for translation, while the strings `'mylog.txt'` and `'w'` are not.

There are a few tools to extract the strings meant for translation. The original GNU `gettext`{.interpreted-text role="program"} only supported C or C++ source code but its extended version `xgettext`{.interpreted-text role="program"} scans code written in a number of languages, including Python, to find strings marked as translatable. [Babel](https://babel.pocoo.org/) is a Python internationalization library that includes a `pybabel`{.interpreted-text role="file"} script to extract and compile message catalogs. François Pinard\'s program called `xpot`{.interpreted-text role="program"} does a similar job and is available as part of his [po-utils package](https://github.com/pinard/po-utils).

(Python also includes pure-Python versions of these programs, called `pygettext.py`{.interpreted-text role="program"} and `msgfmt.py`{.interpreted-text role="program"}; some Python distributions will install them for you. `pygettext.py`{.interpreted-text role="program"} is similar to `xgettext`{.interpreted-text role="program"}, but only understands Python source code and cannot handle other programming languages such as C or C++. `pygettext.py`{.interpreted-text role="program"} supports a command-line interface similar to `xgettext`{.interpreted-text role="program"}; for details on its use, run `pygettext.py --help`. `msgfmt.py`{.interpreted-text role="program"} is binary compatible with GNU `msgfmt`{.interpreted-text role="program"}. With these two programs, you may not need the GNU `gettext`{.interpreted-text role="program"} package to internationalize your Python applications.)

`xgettext`{.interpreted-text role="program"}, `pygettext`{.interpreted-text role="program"}, and similar tools generate `.po`{.interpreted-text role="file"} files that are message catalogs. They are structured human-readable files that contain every marked string in the source code, along with a placeholder for the translated versions of these strings.

Copies of these `.po`{.interpreted-text role="file"} files are then handed over to the individual human translators who write translations for every supported natural language. They send back the completed language-specific versions as a `<language-name>.po`{.interpreted-text role="file"} file that\'s compiled into a machine-readable `.mo`{.interpreted-text role="file"} binary catalog file using the `msgfmt`{.interpreted-text role="program"} program. The `.mo`{.interpreted-text role="file"} files are used by the `!gettext`{.interpreted-text role="mod"} module for the actual translation processing at run-time.

How you use the `!gettext`{.interpreted-text role="mod"} module in your code depends on whether you are internationalizing a single module or your entire application. The next two sections will discuss each case.

### Localizing your module

If you are localizing your module, you must take care not to make global changes, e.g. to the built-in namespace. You should not use the GNU `gettext`{.interpreted-text role="program"} API but instead the class-based API.

Let\'s say your module is called \"spam\" and the module\'s various natural language translation `.mo`{.interpreted-text role="file"} files reside in `/usr/share/locale`{.interpreted-text role="file"} in GNU `gettext`{.interpreted-text role="program"} format. Here\'s what you would put at the top of your module:

    import gettext
    t = gettext.translation('spam', '/usr/share/locale')
    _ = t.gettext

### Localizing your application

If you are localizing your application, you can install the `!_`{.interpreted-text role="func"} function globally into the built-in namespace, usually in the main driver file of your application. This will let all your application-specific files just use `_('...')` without having to explicitly install it in each file.

In the simple case then, you need only add the following bit of code to the main driver file of your application:

    import gettext
    gettext.install('myapplication')

If you need to set the locale directory, you can pass it into the `install`{.interpreted-text role="func"} function:

    import gettext
    gettext.install('myapplication', '/usr/share/locale')

### Changing languages on the fly

If your program needs to support many languages at the same time, you may want to create multiple translation instances and then switch between them explicitly, like so:

    import gettext

    lang1 = gettext.translation('myapplication', languages=['en'])
    lang2 = gettext.translation('myapplication', languages=['fr'])
    lang3 = gettext.translation('myapplication', languages=['de'])

    # start by using language1
    lang1.install()

    # ... time goes by, user selects language 2
    lang2.install()

    # ... more time goes by, user selects language 3
    lang3.install()

### Deferred translations

In most coding situations, strings are translated where they are coded. Occasionally however, you need to mark strings for translation, but defer actual translation until later. A classic example is:

    animals = ['mollusk',
               'albatross',
               'rat',
               'penguin',
               'python', ]
    # ...
    for a in animals:
        print(a)

Here, you want to mark the strings in the `animals` list as being translatable, but you don\'t actually want to translate them until they are printed.

Here is one way you can handle this situation:

    def _(message): return message

    animals = [_('mollusk'),
               _('albatross'),
               _('rat'),
               _('penguin'),
               _('python'), ]

    del _

    # ...
    for a in animals:
        print(_(a))

This works because the dummy definition of `!_`{.interpreted-text role="func"} simply returns the string unchanged. And this dummy definition will temporarily override any definition of `!_`{.interpreted-text role="func"} in the built-in namespace (until the `del`{.interpreted-text role="keyword"} command). Take care, though if you have a previous definition of `!_`{.interpreted-text role="func"} in the local namespace.

Note that the second use of `!_`{.interpreted-text role="func"} will not identify \"a\" as being translatable to the `gettext`{.interpreted-text role="program"} program, because the parameter is not a string literal.

Another way to handle this is with the following example:

    def N_(message): return message

    animals = [N_('mollusk'),
               N_('albatross'),
               N_('rat'),
               N_('penguin'),
               N_('python'), ]

    # ...
    for a in animals:
        print(_(a))

In this case, you are marking translatable strings with the function `!N_`{.interpreted-text role="func"}, which won\'t conflict with any definition of `!_`{.interpreted-text role="func"}. However, you will need to teach your message extraction program to look for translatable strings marked with `!N_`{.interpreted-text role="func"}. `xgettext`{.interpreted-text role="program"}, `pygettext`{.interpreted-text role="program"}, `pybabel extract`, and `xpot`{.interpreted-text role="program"} all support this through the use of the `!-k`{.interpreted-text role="option"} command-line switch. The choice of `!N_`{.interpreted-text role="func"} here is totally arbitrary; it could have just as easily been `!MarkThisStringForTranslation`{.interpreted-text role="func"}.

## Acknowledgements

The following people contributed code, feedback, design suggestions, previous implementations, and valuable experience to the creation of this module:

- Peter Funk
- James Henstridge
- Juan David Ibáñez Palomar
- Marc-André Lemburg
- Martin von Löwis
- François Pinard
- Barry Warsaw
- Gustavo Niemeyer

**Footnotes**

[^1]: The default locale directory is system dependent; for example, on Red Hat Linux it is `/usr/share/locale`{.interpreted-text role="file"}, but on Solaris it is `/usr/lib/locale`{.interpreted-text role="file"}. The `!gettext`{.interpreted-text role="mod"} module does not try to support these system dependent defaults; instead its default is `{sys.base_prefix}/share/locale`{.interpreted-text role="file"} (see `sys.base_prefix`{.interpreted-text role="data"}). For this reason, it is always best to call `bindtextdomain`{.interpreted-text role="func"} with an explicit absolute path at the start of your application.

[^2]: See the footnote for `bindtextdomain`{.interpreted-text role="func"} above.
