# `!dbm`{.interpreted-text role="mod"} \-\-- Interfaces to Unix \"databases\"

::: {.module synopsis="Interfaces to various Unix \"database\" formats."}
dbm
:::

**Source code:** `Lib/dbm/__init__.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

`!dbm`{.interpreted-text role="mod"} is a generic interface to variants of the DBM database:

- `dbm.sqlite3`{.interpreted-text role="mod"}
- `dbm.gnu`{.interpreted-text role="mod"}
- `dbm.ndbm`{.interpreted-text role="mod"}

If none of these modules are installed, the slow-but-simple implementation in module `dbm.dumb`{.interpreted-text role="mod"} will be used. There is a [third party interface](https://www.jcea.es/programacion/pybsddb.htm) to the Oracle Berkeley DB.

:::: note
::: title
Note
:::

None of the underlying modules will automatically shrink the disk space used by the database file. However, `dbm.sqlite3`{.interpreted-text role="mod"}, `dbm.gnu`{.interpreted-text role="mod"} and `dbm.dumb`{.interpreted-text role="mod"} provide a `!reorganize`{.interpreted-text role="meth"} method that can be used for this purpose.
::::

::: exception
error

A tuple containing the exceptions that can be raised by each of the supported modules, with a unique exception also named `dbm.error`{.interpreted-text role="exc"} as the first item \-\-- the latter is used when `dbm.error`{.interpreted-text role="exc"} is raised.
:::

:::: function
whichdb(filename)

This function attempts to guess which of the several simple database modules available \-\-- `dbm.sqlite3`{.interpreted-text role="mod"}, `dbm.gnu`{.interpreted-text role="mod"}, `dbm.ndbm`{.interpreted-text role="mod"}, or `dbm.dumb`{.interpreted-text role="mod"} \-\-- should be used to open a given file.

Return one of the following values:

- `None` if the file can\'t be opened because it\'s unreadable or doesn\'t exist
- the empty string (`''`) if the file\'s format can\'t be guessed
- a string containing the required module name, such as `'dbm.ndbm'` or `'dbm.gnu'`

::: versionchanged
3.11 *filename* accepts a `path-like object`{.interpreted-text role="term"}.
:::
::::

:::: function
open(file, flag=\'r\', mode=0o666)

Open a database and return the corresponding database object.

param file

:   The database file to open.

    If the database file already exists, the `whichdb`{.interpreted-text role="func"} function is used to determine its type and the appropriate module is used; if it does not exist, the first submodule listed above that can be imported is used.

type file
:   `path-like object`{.interpreted-text role="term"}

param str flag

:   - `'r'` (default): Open existing database for reading only.
    - `'w'`: Open existing database for reading and writing.
    - `'c'`: Open database for reading and writing, creating it if it doesn\'t exist.
    - `'n'`: Always create a new, empty database, open for reading and writing.

param int mode
:   The Unix file access mode of the file (default: octal `0o666`), used only when the database has to be created.

::: versionchanged
3.11 *file* accepts a `path-like object`{.interpreted-text role="term"}.
:::
::::

The object returned by `~dbm.open`{.interpreted-text role="func"} supports the basic functionality of mutable `mappings <mapping>`{.interpreted-text role="term"}; keys and their corresponding values can be stored, retrieved, and deleted, and iteration, the `in`{.interpreted-text role="keyword"} operator and methods `!keys`{.interpreted-text role="meth"}, `!get`{.interpreted-text role="meth"}, `!setdefault`{.interpreted-text role="meth"} and `!clear`{.interpreted-text role="meth"} are available. The `!keys`{.interpreted-text role="meth"} method returns a list instead of a view object. The `!setdefault`{.interpreted-text role="meth"} method requires two arguments.

Key and values are always stored as `bytes`{.interpreted-text role="class"}. This means that when strings are used they are implicitly converted to the default encoding before being stored.

These objects also support being used in a `with`{.interpreted-text role="keyword"} statement, which will automatically close them when done.

::: versionchanged
3.2 `!get`{.interpreted-text role="meth"} and `!setdefault`{.interpreted-text role="meth"} methods are now available for all `!dbm`{.interpreted-text role="mod"} backends.
:::

::: versionchanged
3.4 Added native support for the context management protocol to the objects returned by `~dbm.open`{.interpreted-text role="func"}.
:::

::: versionchanged
3.8 Deleting a key from a read-only database raises a database module specific exception instead of `KeyError`{.interpreted-text role="exc"}.
:::

::: versionchanged
3.13 `!clear`{.interpreted-text role="meth"} methods are now available for all `!dbm`{.interpreted-text role="mod"} backends.
:::

The following example records some hostnames and a corresponding title, and then prints out the contents of the database:

    import dbm

    # Open database, creating it if necessary.
    with dbm.open('cache', 'c') as db:

        # Record some values
        db[b'hello'] = b'there'
        db['www.python.org'] = 'Python Website'
        db['www.cnn.com'] = 'Cable News Network'

        # Note that the keys are considered bytes now.
        assert db[b'www.python.org'] == b'Python Website'
        # Notice how the value is now in bytes.
        assert db['www.cnn.com'] == b'Cable News Network'

        # Often-used methods of the dict interface work too.
        print(db.get('python.org', b'not present'))

        # Storing a non-string key or value will raise an exception (most
        # likely a TypeError).
        db['www.yahoo.com'] = 4

    # db is automatically closed when leaving the with statement.

::: seealso

Module `shelve`{.interpreted-text role="mod"}

:   Persistence module which stores non-string data.
:::

The individual submodules are described in the following sections.

## `!dbm.sqlite3`{.interpreted-text role="mod"} \-\-- SQLite backend for dbm

::: {.module synopsis="SQLite backend for dbm"}
dbm.sqlite3
:::

::: versionadded
3.13
:::

**Source code:** `Lib/dbm/sqlite3.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module uses the standard library `sqlite3`{.interpreted-text role="mod"} module to provide an SQLite backend for the `!dbm`{.interpreted-text role="mod"} module. The files created by `!dbm.sqlite3`{.interpreted-text role="mod"} can thus be opened by `sqlite3`{.interpreted-text role="mod"}, or any other SQLite browser, including the SQLite CLI.

::: availability
not WASI.

This module does not work or is not available on WebAssembly. See `wasm-availability`{.interpreted-text role="ref"} for more information.
:::

:::::::: function
open(filename, /, flag=\"r\", mode=0o666)

Open an SQLite database.

param filename
:   The path to the database to be opened.

type filename
:   `path-like object`{.interpreted-text role="term"}

param str flag

:   

> - `'r'` (default): Open existing database for reading only.
> - `'w'`: Open existing database for reading and writing.
> - `'c'`: Open database for reading and writing, creating it if it doesn\'t exist.
> - `'n'`: Always create a new, empty database, open for reading and writing.

param mode
:   The Unix file access mode of the file (default: octal `0o666`), used only when the database has to be created.

The returned database object behaves similar to a mutable `mapping`{.interpreted-text role="term"}, but the `!keys`{.interpreted-text role="meth"} method returns a list, and the `!setdefault`{.interpreted-text role="meth"} method requires two arguments. It also supports a \"closing\" context manager via the `with`{.interpreted-text role="keyword"} keyword.

The following methods are also provided:

::: method
sqlite3.close()

Close the SQLite database.
:::

:::::: method
sqlite3.reorganize()

If you have carried out a lot of deletions and would like to shrink the space used on disk, this method will reorganize the database; otherwise, deleted file space will be kept and reused as new (key, value) pairs are added.

:::: note
::: title
Note
:::

While reorganizing, as much as two times the size of the original database is required in free disk space. However, be aware that this factor changes for each `!dbm`{.interpreted-text role="mod"} submodule.
::::

::: versionadded
3.15
:::
::::::
::::::::

## `!dbm.gnu`{.interpreted-text role="mod"} \-\-- GNU database manager

::: {.module synopsis="GNU database manager"}
dbm.gnu
:::

**Source code:** `Lib/dbm/gnu.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!dbm.gnu`{.interpreted-text role="mod"} module provides an interface to the `GDBM (GNU dbm)`{.interpreted-text role="abbr"} library, similar to the `dbm.ndbm`{.interpreted-text role="mod"} module, but with additional functionality like crash tolerance.

:::: note
::: title
Note
:::

The file formats created by `!dbm.gnu`{.interpreted-text role="mod"} and `dbm.ndbm`{.interpreted-text role="mod"} are incompatible and can not be used interchangeably.
::::

::: availability
not Android, not iOS, not WASI.

This module is not supported on `mobile platforms <mobile-availability>`{.interpreted-text role="ref"} or `WebAssembly platforms <wasm-availability>`{.interpreted-text role="ref"}.
:::

::: availability
Unix.
:::

::: exception
error

Raised on `!dbm.gnu`{.interpreted-text role="mod"}-specific errors, such as I/O errors. `KeyError`{.interpreted-text role="exc"} is raised for general mapping errors like specifying an incorrect key.
:::

::: data
open_flags

A string of characters the *flag* parameter of `~dbm.gnu.open`{.interpreted-text role="meth"} supports.
:::

::::::::::::: function
open(filename, flag=\"r\", mode=0o666, /)

Open a GDBM database and return a `!gdbm`{.interpreted-text role="class"} object.

param filename
:   The database file to open.

type filename
:   `path-like object`{.interpreted-text role="term"}

param str flag

:   - `'r'` (default): Open existing database for reading only.
    - `'w'`: Open existing database for reading and writing.
    - `'c'`: Open database for reading and writing, creating it if it doesn\'t exist.
    - `'n'`: Always create a new, empty database, open for reading and writing.

    The following additional characters may be appended to control how the database is opened:

    - `'f'`: Open the database in fast mode. Writes to the database will not be synchronized.
    - `'s'`: Synchronized mode. Changes to the database will be written immediately to the file.
    - `'u'`: Do not lock database.

    Not all flags are valid for all versions of GDBM. See the `open_flags`{.interpreted-text role="data"} member for a list of supported flag characters.

param int mode
:   The Unix file access mode of the file (default: octal `0o666`), used only when the database has to be created.

raises error
:   If an invalid *flag* argument is passed.

::: versionchanged
3.11 *filename* accepts a `path-like object`{.interpreted-text role="term"}.
:::

`!gdbm`{.interpreted-text role="class"} objects behave similar to mutable `mappings <mapping>`{.interpreted-text role="term"}, but methods `!items`{.interpreted-text role="meth"}, `!values`{.interpreted-text role="meth"}, `!pop`{.interpreted-text role="meth"}, `!popitem`{.interpreted-text role="meth"}, and `!update`{.interpreted-text role="meth"} are not supported, the `!keys`{.interpreted-text role="meth"} method returns a list, and the `!setdefault`{.interpreted-text role="meth"} method requires two arguments. It also supports a \"closing\" context manager via the `with`{.interpreted-text role="keyword"} keyword.

::: versionchanged
3.2 Added the `!get`{.interpreted-text role="meth"} and `!setdefault`{.interpreted-text role="meth"} methods.
:::

::: versionchanged
3.13 Added the `!clear`{.interpreted-text role="meth"} method.
:::

The following methods are also provided:

::: method
gdbm.close()

Close the GDBM database.
:::

::: method
gdbm.firstkey()

It\'s possible to loop over every key in the database using this method and the `nextkey`{.interpreted-text role="meth"} method. The traversal is ordered by GDBM\'s internal hash values, and won\'t be sorted by the key values. This method returns the starting key.
:::

::: method
gdbm.nextkey(key)

Returns the key that follows *key* in the traversal. The following code prints every key in the database `db`, without having to create a list in memory that contains them all:

    k = db.firstkey()
    while k is not None:
        print(k)
        k = db.nextkey(k)
:::

::::: method
gdbm.reorganize()

If you have carried out a lot of deletions and would like to shrink the space used by the GDBM file, this routine will reorganize the database. `!gdbm`{.interpreted-text role="class"} objects will not shorten the length of a database file except by using this reorganization; otherwise, deleted file space will be kept and reused as new (key, value) pairs are added.

:::: note
::: title
Note
:::

While reorganizing, as much as one time the size of the original database is required in free disk space. However, be aware that this factor changes for each `!dbm`{.interpreted-text role="mod"} submodule.
::::
:::::

::: method
gdbm.sync()

When the database has been opened in fast mode, this method forces any unwritten data to be written to the disk.
:::
:::::::::::::

## `!dbm.ndbm`{.interpreted-text role="mod"} \-\-- New Database Manager

::: {.module synopsis="The New Database Manager"}
dbm.ndbm
:::

**Source code:** `Lib/dbm/ndbm.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!dbm.ndbm`{.interpreted-text role="mod"} module provides an interface to the `NDBM (New Database Manager)`{.interpreted-text role="abbr"} library. This module can be used with the \"classic\" NDBM interface or the `GDBM (GNU dbm)`{.interpreted-text role="abbr"} compatibility interface.

:::: note
::: title
Note
:::

The file formats created by `dbm.gnu`{.interpreted-text role="mod"} and `!dbm.ndbm`{.interpreted-text role="mod"} are incompatible and can not be used interchangeably.
::::

:::: warning
::: title
Warning
:::

The NDBM library shipped as part of macOS has an undocumented limitation on the size of values, which can result in corrupted database files when storing values larger than this limit. Reading such corrupted files can result in a hard crash (segmentation fault).
::::

::: availability
not Android, not iOS, not WASI.

This module is not supported on `mobile platforms <mobile-availability>`{.interpreted-text role="ref"} or `WebAssembly platforms <wasm-availability>`{.interpreted-text role="ref"}.
:::

::: availability
Unix.
:::

::: exception
error

Raised on `!dbm.ndbm`{.interpreted-text role="mod"}-specific errors, such as I/O errors. `KeyError`{.interpreted-text role="exc"} is raised for general mapping errors like specifying an incorrect key.
:::

::: data
library

Name of the NDBM implementation library used.
:::

::::::: function
open(filename, flag=\"r\", mode=0o666, /)

Open an NDBM database and return an `!ndbm`{.interpreted-text role="class"} object.

param filename
:   The basename of the database file (without the `.dir`{.interpreted-text role="file"} or `.pag`{.interpreted-text role="file"} extensions).

type filename
:   `path-like object`{.interpreted-text role="term"}

param str flag

:   - `'r'` (default): Open existing database for reading only.
    - `'w'`: Open existing database for reading and writing.
    - `'c'`: Open database for reading and writing, creating it if it doesn\'t exist.
    - `'n'`: Always create a new, empty database, open for reading and writing.

param int mode
:   The Unix file access mode of the file (default: octal `0o666`), used only when the database has to be created.

::: versionchanged
3.11 Accepts `path-like object`{.interpreted-text role="term"} for filename.
:::

`!ndbm`{.interpreted-text role="class"} objects behave similar to mutable `mappings <mapping>`{.interpreted-text role="term"}, but methods `!items`{.interpreted-text role="meth"}, `!values`{.interpreted-text role="meth"}, `!pop`{.interpreted-text role="meth"}, `!popitem`{.interpreted-text role="meth"}, and `!update`{.interpreted-text role="meth"} are not supported, the `!keys`{.interpreted-text role="meth"} method returns a list, and the `!setdefault`{.interpreted-text role="meth"} method requires two arguments. It also supports a \"closing\" context manager via the `with`{.interpreted-text role="keyword"} keyword.

::: versionchanged
3.2 Added the `!get`{.interpreted-text role="meth"} and `!setdefault`{.interpreted-text role="meth"} methods.
:::

::: versionchanged
3.13 Added the `!clear`{.interpreted-text role="meth"} method.
:::

The following method is also provided:

::: method
ndbm.close()

Close the NDBM database.
:::
:::::::

## `!dbm.dumb`{.interpreted-text role="mod"} \-\-- Portable DBM implementation

::: {.module synopsis="Portable implementation of the simple DBM interface."}
dbm.dumb
:::

**Source code:** `Lib/dbm/dumb.py`{.interpreted-text role="source"}

::: index
single: databases
:::

:::: note
::: title
Note
:::

The `!dbm.dumb`{.interpreted-text role="mod"} module is intended as a last resort fallback for the `!dbm`{.interpreted-text role="mod"} module when a more robust module is not available. The `!dbm.dumb`{.interpreted-text role="mod"} module is not written for speed and is not nearly as heavily used as the other database modules.
::::

------------------------------------------------------------------------

The `!dbm.dumb`{.interpreted-text role="mod"} module provides a persistent `dict`{.interpreted-text role="class"}-like interface which is written entirely in Python. Unlike other `!dbm`{.interpreted-text role="mod"} backends, such as `dbm.gnu`{.interpreted-text role="mod"}, no external library is required.

The `!dbm.dumb`{.interpreted-text role="mod"} module defines the following:

::: exception
error

Raised on `!dbm.dumb`{.interpreted-text role="mod"}-specific errors, such as I/O errors. `KeyError`{.interpreted-text role="exc"} is raised for general mapping errors like specifying an incorrect key.
:::

:::::::::::::::: function
open(filename, flag=\"c\", mode=0o666)

Open a `!dbm.dumb`{.interpreted-text role="mod"} database.

param filename

:   The basename of the database file (without extensions). A new database creates the following files:

    - `{filename}.dat`{.interpreted-text role="file"}
    - `{filename}.dir`{.interpreted-text role="file"}

type database
:   `path-like object`{.interpreted-text role="term"}

param str flag

:   - `'r'`: Open existing database for reading only.
    - `'w'`: Open existing database for reading and writing.
    - `'c'` (default): Open database for reading and writing, creating it if it doesn\'t exist.
    - `'n'`: Always create a new, empty database, open for reading and writing.

param int mode
:   The Unix file access mode of the file (default: octal `0o666`), used only when the database has to be created.

:::: warning
::: title
Warning
:::

It is possible to crash the Python interpreter when loading a database with a sufficiently large/complex entry due to stack depth limitations in Python\'s AST compiler.
::::

:::: warning
::: title
Warning
:::

`!dbm.dumb`{.interpreted-text role="mod"} does not support concurrent read/write access. (Multiple simultaneous read accesses are safe.) When a program has the database open for writing, no other program should have it open for reading or writing.
::::

::: versionchanged
3.5 `~dbm.dumb.open`{.interpreted-text role="func"} always creates a new database when *flag* is `'n'`.
:::

::: versionchanged
3.8 A database opened read-only if *flag* is `'r'`. A database is not created if it does not exist if *flag* is `'r'` or `'w'`.
:::

::: versionchanged
3.11 *filename* accepts a `path-like object`{.interpreted-text role="term"}.
:::

The returned database object behaves similar to a mutable `mapping`{.interpreted-text role="term"}, but the `!keys`{.interpreted-text role="meth"} and `!items`{.interpreted-text role="meth"} methods return lists, and the `!setdefault`{.interpreted-text role="meth"} method requires two arguments. It also supports a \"closing\" context manager via the `with`{.interpreted-text role="keyword"} keyword.

The following methods are also provided:

::: method
dumbdbm.close()

Close the database.
:::

:::::: method
dumbdbm.reorganize()

If you have carried out a lot of deletions and would like to shrink the space used on disk, this method will reorganize the database; otherwise, deleted file space will not be reused.

:::: note
::: title
Note
:::

While reorganizing, no additional free disk space is required. However, be aware that this factor changes for each `!dbm`{.interpreted-text role="mod"} submodule.
::::

::: versionadded
3.15
:::
::::::

::: method
dumbdbm.sync()

Synchronize the on-disk directory and data files. This method is called by the `shelve.Shelf.sync`{.interpreted-text role="meth"} method.
:::
::::::::::::::::
