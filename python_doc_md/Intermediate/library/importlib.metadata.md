# `!importlib.metadata`{.interpreted-text role="mod"} \-- Accessing package metadata {#using}

::: {.module synopsis="Accessing package metadata"}
importlib.metadata
:::

::: versionadded
3.8
:::

::: versionchanged
3.10 `importlib.metadata` is no longer provisional.
:::

**Source code:** `Lib/importlib/metadata/__init__.py`{.interpreted-text role="source"}

`importlib.metadata` is a library that provides access to the metadata of an installed [Distribution Package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package), such as its entry points or its top-level names ([Import Package](https://packaging.python.org/en/latest/glossary/#term-Import-Package)s, modules, if any). Built in part on Python\'s import system, this library intends to replace similar functionality in the [entry point API](https://setuptools.readthedocs.io/en/latest/pkg_resources.html#entry-points) and [metadata API](https://setuptools.readthedocs.io/en/latest/pkg_resources.html#metadata-api) of `pkg_resources`. Along with `importlib.resources`{.interpreted-text role="mod"}, this package can eliminate the need to use the older and less efficient `pkg_resources` package.

`importlib.metadata` operates on third-party *distribution packages* installed into Python\'s `site-packages` directory via tools such as `pip`{.interpreted-text role="pypi"}. Specifically, it works with distributions with discoverable `dist-info` or `egg-info` directories, and metadata defined by the [Core metadata specifications](https://packaging.python.org/en/latest/specifications/core-metadata/#core-metadata).

:::: important
::: title
Important
:::

These are *not* necessarily equivalent to or correspond 1:1 with the top-level *import package* names that can be imported inside Python code. One *distribution package* can contain multiple *import packages* (and single modules), and one top-level *import package* may map to multiple *distribution packages* if it is a namespace package. You can use `packages_distributions() <package-distributions>`{.interpreted-text role="ref"} to get a mapping between them.
::::

By default, distribution metadata can live on the file system or in zip archives on `sys.path`{.interpreted-text role="data"}. Through an extension mechanism, the metadata can live almost anywhere.

::: seealso

<https://importlib-metadata.readthedocs.io/>

:   The documentation for `importlib_metadata`, which supplies a backport of `importlib.metadata`. This includes an [API reference](https://importlib-metadata.readthedocs.io/en/latest/api.html) for this module\'s classes and functions, as well as a [migration guide](https://importlib-metadata.readthedocs.io/en/latest/migration.html) for existing users of `pkg_resources`.
:::

## Overview

Let\'s say you wanted to get the version string for a [Distribution Package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package) you\'ve installed using `pip`. We start by creating a virtual environment and installing something into it:

``` shell-session
$ python -m venv example
$ source example/bin/activate
(example) $ python -m pip install wheel
```

You can get the version string for `wheel` by running the following:

``` pycon
(example) $ python
>>> from importlib.metadata import version  # doctest: +SKIP
>>> version('wheel')  # doctest: +SKIP
'0.32.3'
```

You can also get a collection of entry points selectable by properties of the EntryPoint (typically \'group\' or \'name\'), such as `console_scripts`, `distutils.commands` and others. Each group contains a collection of `EntryPoint <entry-points>`{.interpreted-text role="ref"} objects.

You can get the `metadata for a distribution <metadata>`{.interpreted-text role="ref"}:

    >>> list(metadata('wheel'))  # doctest: +SKIP
    ['Metadata-Version', 'Name', 'Version', 'Summary', 'Home-page', 'Author', 'Author-email', 'Maintainer', 'Maintainer-email', 'License', 'Project-URL', 'Project-URL', 'Project-URL', 'Keywords', 'Platform', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Requires-Python', 'Provides-Extra', 'Requires-Dist', 'Requires-Dist']

You can also get a `distribution's version number <version>`{.interpreted-text role="ref"}, list its `constituent files <files>`{.interpreted-text role="ref"}, and get a list of the distribution\'s `requirements`{.interpreted-text role="ref"}.

::: exception
PackageNotFoundError

Subclass of `ModuleNotFoundError`{.interpreted-text role="class"} raised by several functions in this module when queried for a distribution package which is not installed in the current Python environment.
:::

## Functional API

This package provides the following functionality via its public API.

### Entry points

::: function
entry_points(\*\*select_params)

Returns a `EntryPoints`{.interpreted-text role="class"} instance describing entry points for the current environment. Any given keyword parameters are passed to the `!select`{.interpreted-text role="meth"} method for comparison to the attributes of the individual entry point definitions.

Note: it is not currently possible to query for entry points based on their `!EntryPoint.dist`{.interpreted-text role="attr"} attribute (as different `!Distribution`{.interpreted-text role="class"} instances do not currently compare equal, even if they have the same attributes)
:::

::: EntryPoints
Details of a collection of installed entry points.

Also provides a `.groups` attribute that reports all identified entry point groups, and a `.names` attribute that reports all identified entry point names.
:::

::: EntryPoint
Details of an installed entry point.

Each `!EntryPoint`{.interpreted-text role="class"} instance has `.name`, `.group`, and `.value` attributes and a `.load()` method to resolve the value. There are also `.module`, `.attr`, and `.extras` attributes for getting the components of the `.value` attribute, and `.dist` for obtaining information regarding the distribution package that provides the entry point.
:::

Query all entry points:

    >>> eps = entry_points()  # doctest: +SKIP

The `!entry_points`{.interpreted-text role="func"} function returns a `!EntryPoints`{.interpreted-text role="class"} object, a collection of all `!EntryPoint`{.interpreted-text role="class"} objects with `names` and `groups` attributes for convenience:

    >>> sorted(eps.groups)  # doctest: +SKIP
    ['console_scripts', 'distutils.commands', 'distutils.setup_keywords', 'egg_info.writers', 'setuptools.installation']

`!EntryPoints`{.interpreted-text role="class"} has a `!select`{.interpreted-text role="meth"} method to select entry points matching specific properties. Select entry points in the `console_scripts` group:

    >>> scripts = eps.select(group='console_scripts')  # doctest: +SKIP

Equivalently, since `!entry_points`{.interpreted-text role="func"} passes keyword arguments through to select:

    >>> scripts = entry_points(group='console_scripts')  # doctest: +SKIP

Pick out a specific script named \"wheel\" (found in the wheel project):

    >>> 'wheel' in scripts.names  # doctest: +SKIP
    True
    >>> wheel = scripts['wheel']  # doctest: +SKIP

Equivalently, query for that entry point during selection:

    >>> (wheel,) = entry_points(group='console_scripts', name='wheel')  # doctest: +SKIP
    >>> (wheel,) = entry_points().select(group='console_scripts', name='wheel')  # doctest: +SKIP

Inspect the resolved entry point:

    >>> wheel  # doctest: +SKIP
    EntryPoint(name='wheel', value='wheel.cli:main', group='console_scripts')
    >>> wheel.module  # doctest: +SKIP
    'wheel.cli'
    >>> wheel.attr  # doctest: +SKIP
    'main'
    >>> wheel.extras  # doctest: +SKIP
    []
    >>> main = wheel.load()  # doctest: +SKIP
    >>> main  # doctest: +SKIP
    <function main at 0x103528488>

The `group` and `name` are arbitrary values defined by the package author and usually a client will wish to resolve all entry points for a particular group. Read [the setuptools docs](https://setuptools.pypa.io/en/latest/userguide/entry_point.html) for more information on entry points, their definition, and usage.

::: versionchanged
3.12 The \"selectable\" entry points were introduced in `importlib_metadata` 3.6 and Python 3.10. Prior to those changes, `entry_points` accepted no parameters and always returned a dictionary of entry points, keyed by group. With `importlib_metadata` 5.0 and Python 3.12, `entry_points` always returns an `EntryPoints` object. See `backports.entry_points_selectable`{.interpreted-text role="pypi"} for compatibility options.
:::

::: versionchanged
3.13 `EntryPoint` objects no longer present a tuple-like interface (`~object.__getitem__`{.interpreted-text role="meth"}).
:::

### Distribution metadata {#metadata}

::: function
metadata(distribution_name)

Return the distribution metadata corresponding to the named distribution package as a `PackageMetadata`{.interpreted-text role="class"} instance.

Raises `PackageNotFoundError`{.interpreted-text role="exc"} if the named distribution package is not installed in the current Python environment.
:::

::: PackageMetadata
A concrete implementation of the [PackageMetadata protocol](https://importlib-metadata.readthedocs.io/en/latest/api.html#importlib_metadata.PackageMetadata).

In addition to providing the defined protocol methods and attributes, subscripting the instance is equivalent to calling the `!get`{.interpreted-text role="meth"} method.
:::

Every [Distribution Package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package) includes some metadata, which you can extract using the `!metadata`{.interpreted-text role="func"} function:

    >>> wheel_metadata = metadata('wheel')  # doctest: +SKIP

The keys of the returned data structure name the metadata keywords, and the values are returned unparsed from the distribution metadata:

    >>> wheel_metadata['Requires-Python']  # doctest: +SKIP
    '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*'

`PackageMetadata`{.interpreted-text role="class"} also presents a `!json`{.interpreted-text role="attr"} attribute that returns all the metadata in a JSON-compatible form per [PEP 566](http://www.python.org/dev/peps/pep-0566/ "PEP 566"):

    >>> wheel_metadata.json['requires_python']
    '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*'

The full set of available metadata is not described here. See the PyPA [Core metadata specification](https://packaging.python.org/en/latest/specifications/core-metadata/#core-metadata) for additional details.

::: versionchanged
3.10 The `Description` is now included in the metadata when presented through the payload. Line continuation characters have been removed.

The `json` attribute was added.
:::

### Distribution versions {#version}

::: function
version(distribution_name)

Return the installed distribution package [version](https://packaging.python.org/en/latest/specifications/core-metadata/#version) for the named distribution package.

Raises `PackageNotFoundError`{.interpreted-text role="exc"} if the named distribution package is not installed in the current Python environment.
:::

The `!version`{.interpreted-text role="func"} function is the quickest way to get a [Distribution Package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package)\'s version number, as a string:

    >>> version('wheel')  # doctest: +SKIP
    '0.32.3'

### Distribution files {#files}

::: function
files(distribution_name)

Return the full set of files contained within the named distribution package.

Raises `PackageNotFoundError`{.interpreted-text role="exc"} if the named distribution package is not installed in the current Python environment.

Returns `None`{.interpreted-text role="const"} if the distribution is found but the installation database records reporting the files associated with the distribution package are missing.
:::

::: PackagePath
A `pathlib.PurePath`{.interpreted-text role="class"} derived object with additional `dist`, `size`, and `hash` properties corresponding to the distribution package\'s installation metadata for that file.
:::

The `!files`{.interpreted-text role="func"} function takes a [Distribution Package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package) name and returns all of the files installed by this distribution. Each file is reported as a `PackagePath`{.interpreted-text role="class"} instance. For example:

    >>> util = [p for p in files('wheel') if 'util.py' in str(p)][0]  # doctest: +SKIP
    >>> util  # doctest: +SKIP
    PackagePath('wheel/util.py')
    >>> util.size  # doctest: +SKIP
    859
    >>> util.dist  # doctest: +SKIP
    <importlib.metadata._hooks.PathDistribution object at 0x101e0cef0>
    >>> util.hash  # doctest: +SKIP
    <FileHash mode: sha256 value: bYkw5oMccfazVCoYQwKkkemoVyMAFoR34mmKBx8R1NI>

Once you have the file, you can also read its contents:

    >>> print(util.read_text())  # doctest: +SKIP
    import base64
    import sys
    ...
    def as_bytes(s):
        if isinstance(s, text_type):
            return s.encode('utf-8')
        return s

You can also use the `!locate`{.interpreted-text role="meth"} method to get the absolute path to the file:

    >>> util.locate()  # doctest: +SKIP
    PosixPath('/home/gustav/example/lib/site-packages/wheel/util.py')

In the case where the metadata file listing files (`RECORD` or `SOURCES.txt`) is missing, `!files`{.interpreted-text role="func"} will return `None`{.interpreted-text role="const"}. The caller may wish to wrap calls to `!files`{.interpreted-text role="func"} in [always_iterable](https://more-itertools.readthedocs.io/en/stable/api.html#more_itertools.always_iterable) or otherwise guard against this condition if the target distribution is not known to have the metadata present.

### Distribution requirements {#requirements}

::: function
requires(distribution_name)

Return the declared dependency specifiers for the named distribution package.

Raises `PackageNotFoundError`{.interpreted-text role="exc"} if the named distribution package is not installed in the current Python environment.
:::

To get the full set of requirements for a [Distribution Package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package), use the `!requires`{.interpreted-text role="func"} function:

    >>> requires('wheel')  # doctest: +SKIP
    ["pytest (>=3.0.0) ; extra == 'test'", "pytest-cov ; extra == 'test'"]

### Mapping import to distribution packages[]{#package-distributions} {#import-distribution-package-mapping}

::: function
packages_distributions()

Return a mapping from the top level module and import package names found via `sys.meta_path`{.interpreted-text role="data"} to the names of the distribution packages (if any) that provide the corresponding files.

To allow for namespace packages (which may have members provided by multiple distribution packages), each top level import name maps to a list of distribution names rather than mapping directly to a single name.
:::

A convenience method to resolve the [Distribution Package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package) name (or names, in the case of a namespace package) that provide each importable top-level Python module or [Import Package](https://packaging.python.org/en/latest/glossary/#term-Import-Package):

    >>> packages_distributions()
    {'importlib_metadata': ['importlib-metadata'], 'yaml': ['PyYAML'], 'jaraco': ['jaraco.classes', 'jaraco.functools'], ...}

Some editable installs, [do not supply top-level names](https://github.com/pypa/packaging-problems/issues/609), and thus this function is not reliable with such installs.

::: versionadded
3.10
:::

## Distributions

::: function
distribution(distribution_name)

Return a `Distribution`{.interpreted-text role="class"} instance describing the named distribution package.

Raises `PackageNotFoundError`{.interpreted-text role="exc"} if the named distribution package is not installed in the current Python environment.
:::

:::: Distribution
Details of an installed distribution package.

Note: different `!Distribution`{.interpreted-text role="class"} instances do not currently compare equal, even if they relate to the same installed distribution and accordingly have the same attributes.

::: method
discover(cls, *, context=None,*\*kwargs)

Returns an iterable of `Distribution`{.interpreted-text role="class"} instances for all packages.

The optional argument *context* is a `DistributionFinder.Context`{.interpreted-text role="class"} instance, used to modify the search for distributions. Alternatively, *kwargs* may contain keyword arguments for constructing a new `!DistributionFinder.Context`{.interpreted-text role="class"}.
:::
::::

While the module level API described above is the most common and convenient usage, you can get all of that information from the `!Distribution`{.interpreted-text role="class"} class. `!Distribution`{.interpreted-text role="class"} is an abstract object that represents the metadata for a Python [Distribution Package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package). You can get the concrete `!Distribution`{.interpreted-text role="class"} subclass instance for an installed distribution package by calling the `distribution`{.interpreted-text role="func"} function:

    >>> from importlib.metadata import distribution  # doctest: +SKIP
    >>> dist = distribution('wheel')  # doctest: +SKIP
    >>> type(dist)  # doctest: +SKIP
    <class 'importlib.metadata.PathDistribution'>

Thus, an alternative way to get the version number is through the `!Distribution`{.interpreted-text role="class"} instance:

    >>> dist.version  # doctest: +SKIP
    '0.32.3'

There are all kinds of additional metadata available on `!Distribution`{.interpreted-text role="class"} instances:

    >>> dist.metadata['Requires-Python']  # doctest: +SKIP
    '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*'
    >>> dist.metadata['License']  # doctest: +SKIP
    'MIT'

For editable packages, an `origin` property may present `610`{.interpreted-text role="pep"} metadata:

    >>> dist.origin.url
    'file:///path/to/wheel-0.32.3.editable-py3-none-any.whl'

The full set of available metadata is not described here. See the PyPA [Core metadata specification](https://packaging.python.org/en/latest/specifications/core-metadata/#core-metadata) for additional details.

::: versionadded
3.13 The `.origin` property was added.
:::

## Distribution Discovery

By default, this package provides built-in support for discovery of metadata for file system and zip file [Distribution Package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package)s. This metadata finder search defaults to `sys.path`, but varies slightly in how it interprets those values from how other import machinery does. In particular:

- `importlib.metadata` does not honor `bytes`{.interpreted-text role="class"} objects on `sys.path`.
- `importlib.metadata` will incidentally honor `pathlib.Path`{.interpreted-text role="py:class"} objects on `sys.path` even though such values will be ignored for imports.

::: DistributionFinder
A `~importlib.abc.MetaPathFinder`{.interpreted-text role="class"} subclass capable of discovering installed distributions.

Custom providers should implement this interface in order to supply metadata.

> ::::: Context(**kwargs)
> A `!Context`{.interpreted-text role="class"} gives a custom provider a means to solicit additional details from the callers of distribution discovery functions like `distributions`{.interpreted-text role="func"} or `Distribution.discover`{.interpreted-text role="meth"} beyond `!.name`{.interpreted-text role="attr"} and `!.path`{.interpreted-text role="attr"} when searching for distributions.
>
> For example, a provider could expose suites of packages in either a \"public\" or \"private\" `realm`. A caller of distribution discovery functions may wish to query only for distributions in a particular realm and could call `distributions(realm="private")` to signal to the custom provider to only include distributions from that realm.
>
> Each `!DistributionFinder`{.interpreted-text role="class"} must expect any parameters and should attempt to honor the canonical parameters defined below when appropriate.
>
> See the section on `implementing-custom-providers`{.interpreted-text role="ref"} for more details.
>
> ::: attribute
> name
>
> Specific name for which a distribution finder should match.
>
> A `!.name`{.interpreted-text role="attr"} of `None` matches all distributions.
> :::
>
> ::: attribute
> path
>
> A property providing the sequence of directory paths that a distribution finder should search.
>
> Typically refers to Python installed package paths such as \"site-packages\" directories and defaults to `sys.path`{.interpreted-text role="attr"}.
> :::
> :::::
:::

::: function
distributions(\*\*kwargs)

Returns an iterable of `Distribution`{.interpreted-text role="class"} instances for all packages.

The *kwargs* argument may contain either a keyword argument `context`, a `DistributionFinder.Context`{.interpreted-text role="class"} instance, or pass keyword arguments for constructing a new `!DistributionFinder.Context`{.interpreted-text role="class"}. The `!DistributionFinder.Context`{.interpreted-text role="class"} is used to modify the search for distributions.
:::

## Implementing Custom Providers

`importlib.metadata` address two API surfaces, one for *consumers* and another for *providers*. Most users are consumers, consuming metadata provided by the packages. There are other use-cases, however, where users wish to expose metadata through some other mechanism, such as alongside a custom importer. Such a use case calls for a *custom provider*.

Because [Distribution Package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package) metadata is not available through `sys.path`{.interpreted-text role="data"} searches, or package loaders directly, the metadata for a distribution is found through import system `finders <finders-and-loaders>`{.interpreted-text role="ref"}. To find a distribution package\'s metadata, `importlib.metadata` queries the list of `meta path finders <meta path finder>`{.interpreted-text role="term"} on `sys.meta_path`{.interpreted-text role="data"}.

The implementation has hooks integrated into the `PathFinder`, serving metadata for distribution packages found on the file system.

The abstract class `importlib.abc.MetaPathFinder`{.interpreted-text role="py:class"} defines the interface expected of finders by Python\'s import system. `importlib.metadata` extends this protocol by looking for an optional `find_distributions` callable on the finders from `sys.meta_path`{.interpreted-text role="data"} and presents this extended interface as the `DistributionFinder`{.interpreted-text role="class"} abstract base class, which defines this abstract method:

    @abc.abstractmethod
    def find_distributions(context=DistributionFinder.Context()) -> Iterable[Distribution]:
        """Return an iterable of all Distribution instances capable of
        loading the metadata for packages for the indicated ``context``.
        """

The `DistributionFinder.Context`{.interpreted-text role="class"} object provides `~DistributionFinder.Context.path`{.interpreted-text role="attr"} and `~DistributionFinder.Context.name`{.interpreted-text role="attr"} properties indicating the path to search and name to match and may supply other relevant context sought by the consumer.

In practice, to support finding distribution package metadata in locations other than the file system, subclass `Distribution` and implement the abstract methods. Then from a custom finder, return instances of this derived `Distribution` in the `find_distributions()` method.

### Example

Imagine a custom finder that loads Python modules from a database:

    class DatabaseImporter(importlib.abc.MetaPathFinder):
        def __init__(self, db):
            self.db = db

        def find_spec(self, fullname, target=None) -> ModuleSpec:
            return self.db.spec_from_name(fullname)

    sys.meta_path.append(DatabaseImporter(connect_db(...)))

That importer now presumably provides importable modules from a database, but it provides no metadata or entry points. For this custom importer to provide metadata, it would also need to implement `DistributionFinder`{.interpreted-text role="class"}:

    from importlib.metadata import DistributionFinder

    class DatabaseImporter(DistributionFinder):
        ...

        def find_distributions(self, context=DistributionFinder.Context()):
            query = dict(name=context.name) if context.name else {}
            for dist_record in self.db.query_distributions(query):
                yield DatabaseDistribution(dist_record)

In this way, `query_distributions` would return records for each distribution served by the database matching the query. For example, if `requests-1.0` is in the database, `find_distributions` would yield a `DatabaseDistribution` for `Context(name='requests')` or `Context(name=None)`.

For the sake of simplicity, this example ignores `context.path`. The `path` attribute defaults to `sys.path` and is the set of import paths to be considered in the search. A `DatabaseImporter` could potentially function without any concern for a search path. Assuming the importer does no partitioning, the \"path\" would be irrelevant. In order to illustrate the purpose of `path`, the example would need to illustrate a more complex `DatabaseImporter` whose behavior varied depending on `sys.path`/`PYTHONPATH`. In that case, the `find_distributions` should honor the `context.path` and only yield `Distribution`s pertinent to that path.

`DatabaseDistribution`, then, would look something like:

    class DatabaseDistribution(importlib.metadata.Distribution):
        def __init__(self, record):
            self.record = record

        def read_text(self, filename):
            """
            Read a file like "METADATA" for the current distribution.
            """
            if filename == "METADATA":
                return f"""Name: {self.record.name}
    Version: {self.record.version}
    """
            if filename == "entry_points.txt":
                return "\n".join(
                  f"""[{ep.group}]\n{ep.name}={ep.value}"""
                  for ep in self.record.entry_points)

        def locate_file(self, path):
            raise RuntimeError("This distribution has no file system")

This basic implementation should provide metadata and entry points for packages served by the `DatabaseImporter`, assuming that the `record` supplies suitable `.name`, `.version`, and `.entry_points` attributes.

The `DatabaseDistribution` may also provide other metadata files, like `RECORD` (required for `Distribution.files`) or override the implementation of `Distribution.files`. See the source for more inspiration.
