# `!shelve`{.interpreted-text role="mod"} \-\-- Python object persistence

::: {.module synopsis="Python object persistence."}
shelve
:::

**Source code:** `Lib/shelve.py`{.interpreted-text role="source"}

::: index
pair: module; pickle
:::

------------------------------------------------------------------------

A \"shelf\" is a persistent, dictionary-like object. The difference with \"dbm\" databases is that the values (not the keys!) in a shelf can be essentially arbitrary Python objects \-\-- anything that the `pickle`{.interpreted-text role="mod"} module can handle. This includes most class instances, recursive data types, and objects containing lots of shared sub-objects. The keys are ordinary strings.

:::::::: function
open(filename, flag=\'c\', protocol=None, writeback=False, \*, serializer=None, deserializer=None)

Open a persistent dictionary. The filename specified is the base filename for the underlying database. As a side-effect, an extension may be added to the filename and more than one file may be created. By default, the underlying database file is opened for reading and writing. The optional *flag* parameter has the same interpretation as the *flag* parameter of `dbm.open`{.interpreted-text role="func"}.

By default, pickles created with `pickle.DEFAULT_PROTOCOL`{.interpreted-text role="const"} are used to serialize values. The version of the pickle protocol can be specified with the *protocol* parameter.

Because of Python semantics, a shelf cannot know when a mutable persistent-dictionary entry is modified. By default modified objects are written *only* when assigned to the shelf (see `shelve-example`{.interpreted-text role="ref"}). If the optional *writeback* parameter is set to `True`, all entries accessed are also cached in memory, and written back on `~Shelf.sync`{.interpreted-text role="meth"} and `~Shelf.close`{.interpreted-text role="meth"}; this can make it handier to mutate mutable entries in the persistent dictionary, but, if many entries are accessed, it can consume vast amounts of memory for the cache, and it can make the close operation very slow since all accessed entries are written back (there is no way to determine which accessed entries are mutable, nor which ones were actually mutated).

By default, `!shelve`{.interpreted-text role="mod"} uses `pickle.dumps`{.interpreted-text role="func"} and `pickle.loads`{.interpreted-text role="func"} for serializing and deserializing. This can be changed by supplying *serializer* and *deserializer*, respectively.

The *serializer* argument must be a callable which takes an object `obj` and the *protocol* as inputs and returns the representation `obj` as a `bytes-like object`{.interpreted-text role="term"}; the *protocol* value may be ignored by the serializer.

The *deserializer* argument must be a callable which takes a serialized object given as a `bytes`{.interpreted-text role="class"} object and returns the corresponding object.

A `ShelveError`{.interpreted-text role="exc"} is raised if *serializer* is given but *deserializer* is not, or vice-versa.

::: versionchanged
3.10 `pickle.DEFAULT_PROTOCOL`{.interpreted-text role="const"} is now used as the default pickle protocol.
:::

::: versionchanged
3.11 Accepts `path-like object`{.interpreted-text role="term"} for filename.
:::

::: versionchanged
3.15 Accepts custom *serializer* and *deserializer* functions in place of `pickle.dumps`{.interpreted-text role="func"} and `pickle.loads`{.interpreted-text role="func"}.
:::

:::: note
::: title
Note
:::

Do not rely on the shelf being closed automatically; always call `~Shelf.close`{.interpreted-text role="meth"} explicitly when you don\'t need it any more, or use `shelve.open`{.interpreted-text role="func"} as a context manager:

    with shelve.open('spam') as db:
        db['eggs'] = 'eggs'
::::
::::::::

::::: {#shelve-security}
:::: warning
::: title
Warning
:::

Because the `!shelve`{.interpreted-text role="mod"} module is backed by `pickle`{.interpreted-text role="mod"}, it is insecure to load a shelf from an untrusted source. Like with pickle, loading a shelf can execute arbitrary code.
::::
:::::

Shelf objects support most of the methods and operations supported by dictionaries (except copying, constructors and operators `|` and `|=`). This eases the transition from dictionary based scripts to those requiring persistent storage.

Two additional methods are supported:

::: method
Shelf.sync()

Write back all entries in the cache if the shelf was opened with *writeback* set to `True`{.interpreted-text role="const"}. Also empty the cache and synchronize the persistent dictionary on disk, if feasible. This is called automatically when `reorganize`{.interpreted-text role="meth"} is called or the shelf is closed with `close`{.interpreted-text role="meth"}.
:::

:::: method
Shelf.reorganize()

Calls `sync`{.interpreted-text role="meth"} and attempts to shrink space used on disk by removing empty space resulting from deletions.

::: versionadded
3.15
:::
::::

::: method
Shelf.close()

Synchronize and close the persistent *dict* object. Operations on a closed shelf will fail with a `ValueError`{.interpreted-text role="exc"}.
:::

::: seealso
[Persistent dictionary recipe](https://code.activestate.com/recipes/576642-persistent-dict-with-multiple-standard-file-format/) with widely supported storage formats and having the speed of native dictionaries.
:::

## Restrictions

::: index
pair: module; dbm.ndbm pair: module; dbm.gnu
:::

- The choice of which database package will be used (such as `dbm.ndbm`{.interpreted-text role="mod"} or `dbm.gnu`{.interpreted-text role="mod"}) depends on which interface is available. Therefore it is not safe to open the database directly using `dbm`{.interpreted-text role="mod"}. The database is also (unfortunately) subject to the limitations of `dbm`{.interpreted-text role="mod"}, if it is used \-\-- this means that (the pickled representation of) the objects stored in the database should be fairly small, and in rare cases key collisions may cause the database to refuse updates.
- The `!shelve`{.interpreted-text role="mod"} module does not support *concurrent* read/write access to shelved objects. (Multiple simultaneous read accesses are safe.) When a program has a shelf open for writing, no other program should have it open for reading or writing. Unix file locking can be used to solve this, but this differs across Unix versions and requires knowledge about the database implementation used.
- On macOS `dbm.ndbm`{.interpreted-text role="mod"} can silently corrupt the database file on updates, which can cause hard crashes when trying to read from the database.
- `Shelf.reorganize`{.interpreted-text role="meth"} may not be available for all database packages and may temporarily increase resource usage (especially disk space) when called. Additionally, it will never run automatically and instead needs to be called explicitly.

::::::: {.Shelf(dict, .protocol=None, .writeback=False, .\\ .keyencoding='utf-8', .*, .serializer=None, .deserializer=None)}
A subclass of `collections.abc.MutableMapping`{.interpreted-text role="class"} which stores pickled values in the *dict* object.

By default, pickles created with `pickle.DEFAULT_PROTOCOL`{.interpreted-text role="const"} are used to serialize values. The version of the pickle protocol can be specified with the *protocol* parameter. See the `pickle`{.interpreted-text role="mod"} documentation for a discussion of the pickle protocols.

If the *writeback* parameter is `True`, the object will hold a cache of all entries accessed and write them back to the *dict* at sync and close times. This allows natural operations on mutable entries, but can consume much more memory and make sync and close take a long time.

The *keyencoding* parameter is the encoding used to encode keys before they are used with the underlying dict.

The *serializer* and *deserializer* parameters have the same interpretation as in `~shelve.open`{.interpreted-text role="func"}.

A `Shelf`{.interpreted-text role="class"} object can also be used as a context manager, in which case it will be automatically closed when the `with`{.interpreted-text role="keyword"} block ends.

::: versionchanged
3.2 Added the *keyencoding* parameter; previously, keys were always encoded in UTF-8.
:::

::: versionchanged
3.4 Added context manager support.
:::

::: versionchanged
3.10 `pickle.DEFAULT_PROTOCOL`{.interpreted-text role="const"} is now used as the default pickle protocol.
:::

::: versionchanged
3.15 Added the *serializer* and *deserializer* parameters.
:::
:::::::

:::: {.BsdDbShelf(dict, .protocol=None, .writeback=False, .\\ .keyencoding='utf-8', .*, .\\ .serializer=None, .deserializer=None)}
A subclass of `Shelf`{.interpreted-text role="class"} which exposes `!first`{.interpreted-text role="meth"}, `!next`{.interpreted-text role="meth"}, `!previous`{.interpreted-text role="meth"}, `!last`{.interpreted-text role="meth"} and `!set_location`{.interpreted-text role="meth"} methods. These are available in the third-party `!bsddb`{.interpreted-text role="mod"} module from [pybsddb](https://www.jcea.es/programacion/pybsddb.htm) but not in other database modules. The *dict* object passed to the constructor must support those methods. This is generally accomplished by calling one of `!bsddb.hashopen`{.interpreted-text role="func"}, `!bsddb.btopen`{.interpreted-text role="func"} or `!bsddb.rnopen`{.interpreted-text role="func"}. The optional *protocol*, *writeback*, *keyencoding*, *serializer* and *deserializer* parameters have the same interpretation as in `~shelve.open`{.interpreted-text role="func"}.

::: versionchanged
3.15 Added the *serializer* and *deserializer* parameters.
:::
::::

:::: {.DbfilenameShelf(filename, .flag='c', .protocol=None, .\\ .writeback=False, .*, .serializer=None, .\\ .deserializer=None)}
A subclass of `Shelf`{.interpreted-text role="class"} which accepts a *filename* instead of a dict-like object. The underlying file will be opened using `dbm.open`{.interpreted-text role="func"}. By default, the file will be created and opened for both read and write. The optional *flag* parameter has the same interpretation as for the `.open`{.interpreted-text role="func"} function. The optional *protocol*, *writeback*, *serializer* and *deserializer* parameters have the same interpretation as in `~shelve.open`{.interpreted-text role="func"}.

::: versionchanged
3.15 Added the *serializer* and *deserializer* parameters.
:::
::::

## Example {#shelve-example}

To summarize the interface (`key` is a string, `data` is an arbitrary object):

    import shelve

    d = shelve.open(filename)  # open -- file may get suffix added by low-level
                               # library

    d[key] = data              # store data at key (overwrites old data if
                               # using an existing key)
    data = d[key]              # retrieve a COPY of data at key (raise KeyError
                               # if no such key)
    del d[key]                 # delete data stored at key (raises KeyError
                               # if no such key)

    flag = key in d            # true if the key exists
    klist = list(d.keys())     # a list of all existing keys (slow!)

    # as d was opened WITHOUT writeback=True, beware:
    d['xx'] = [0, 1, 2]        # this works as expected, but...
    d['xx'].append(3)          # *this doesn't!* -- d['xx'] is STILL [0, 1, 2]!

    # having opened d without writeback=True, you need to code carefully:
    temp = d['xx']             # extracts the copy
    temp.append(5)             # mutates the copy
    d['xx'] = temp             # stores the copy right back, to persist it

    # or, d=shelve.open(filename,writeback=True) would let you just code
    # d['xx'].append(5) and have it work as expected, BUT it would also
    # consume more memory and make the d.close() operation slower.

    d.close()                  # close it

## Exceptions

:::: exception
ShelveError

Exception raised when one of the arguments *deserializer* and *serializer* is missing in the `~shelve.open`{.interpreted-text role="func"}, `Shelf`{.interpreted-text role="class"}, `BsdDbShelf`{.interpreted-text role="class"} and `DbfilenameShelf`{.interpreted-text role="class"}.

The *deserializer* and *serializer* arguments must be given together.

::: versionadded
3.15
:::
::::

::: seealso

Module `dbm`{.interpreted-text role="mod"}

:   Generic interface to `dbm`-style databases.

Module `pickle`{.interpreted-text role="mod"}

:   Object serialization used by `!shelve`{.interpreted-text role="mod"}.
:::
