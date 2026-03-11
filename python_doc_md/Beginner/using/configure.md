# Configure Python

## Build Requirements

To build CPython, you will need:

- A [C11](https://en.cppreference.com/w/c/11) compiler. [Optional C11 features](https://en.wikipedia.org/wiki/C11_(C_standard_revision)#Optional_features) are not required.
- On Windows, Microsoft Visual Studio 2017 or later is required.
- Support for [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754) floating-point numbers and [floating-point Not-a-Number (NaN)](https://en.wikipedia.org/wiki/NaN#Floating_point).
- Support for threads.

::: versionchanged
3.5 On Windows, Visual Studio 2015 or later is now required.
:::

::: versionchanged
3.6 Selected C99 features, like `<stdint.h>` and `static inline` functions, are now required.
:::

::: versionchanged
3.7 Thread support is now required.
:::

::: versionchanged
3.11 C11 compiler, IEEE 754 and NaN support are now required. On Windows, Visual Studio 2017 or later is required.
:::

See also `7`{.interpreted-text role="pep"} \"Style Guide for C Code\" and `11`{.interpreted-text role="pep"} \"CPython platform support\".

### Requirements for optional modules {#optional-module-requirements}

Some `optional modules <optional module>`{.interpreted-text role="term"} of the standard library require third-party libraries installed for development (for example, header files must be available).

Missing requirements are reported in the `configure` output. Modules that are missing due to missing dependencies are listed near the end of the `make` output, sometimes using an internal name, for example, `_ctypes` for `ctypes`{.interpreted-text role="mod"} module.

If you distribute a CPython interpreter without optional modules, it\'s best practice to advise users, who generally expect that standard library modules are available.

Dependencies to build optional modules are:

+-------------------------------------------------------------------------------------------------------------------------+----------------------+------------------------------------------------------------------------------------------------------------------------------+
| Dependency                                                                                                              | Minimum version      | Python module                                                                                                                |
+=========================================================================================================================+======================+==============================================================================================================================+
| [libbz2](https://sourceware.org/bzip2/)                                                                                 |                      | `bz2`{.interpreted-text role="mod"}                                                                                          |
+-------------------------------------------------------------------------------------------------------------------------+----------------------+------------------------------------------------------------------------------------------------------------------------------+
| [libffi](https://sourceware.org/libffi/)                                                                                | 3.3.0 recommended    | `ctypes`{.interpreted-text role="mod"}                                                                                       |
+-------------------------------------------------------------------------------------------------------------------------+----------------------+------------------------------------------------------------------------------------------------------------------------------+
| [liblzma](https://tukaani.org/xz/)                                                                                      |                      | `lzma`{.interpreted-text role="mod"}                                                                                         |
+-------------------------------------------------------------------------------------------------------------------------+----------------------+------------------------------------------------------------------------------------------------------------------------------+
| [libmpdec](https://www.bytereef.org/mpdecimal/doc/libmpdec/)                                                            | 2.5.0                | `decimal`{.interpreted-text role="mod"}[^1]                                                                                  |
+-------------------------------------------------------------------------------------------------------------------------+----------------------+------------------------------------------------------------------------------------------------------------------------------+
| [libreadline](https://tiswww.case.edu/php/chet/readline/rltop.html) or [libedit](https://www.thrysoee.dk/editline/)[^2] |                      | `readline`{.interpreted-text role="mod"}                                                                                     |
+-------------------------------------------------------------------------------------------------------------------------+----------------------+------------------------------------------------------------------------------------------------------------------------------+
| [libuuid](https://linux.die.net/man/3/libuuid)                                                                          |                      | `_uuid`[^3]                                                                                                                  |
+-------------------------------------------------------------------------------------------------------------------------+----------------------+------------------------------------------------------------------------------------------------------------------------------+
| [ncurses](https://gnu.org/software/ncurses/ncurses.html)[^4]                                                            |                      | `curses`{.interpreted-text role="mod"}                                                                                       |
+-------------------------------------------------------------------------------------------------------------------------+----------------------+------------------------------------------------------------------------------------------------------------------------------+
| [OpenSSL](https://openssl-library.org/)                                                                                 | | 3.0.18 recommended | `ssl`{.interpreted-text role="mod"}, `hashlib`{.interpreted-text role="mod"}[^5]                                             |
|                                                                                                                         | | (1.1.1 minimum)    |                                                                                                                              |
+-------------------------------------------------------------------------------------------------------------------------+----------------------+------------------------------------------------------------------------------------------------------------------------------+
| [SQLite](https://sqlite.org/)                                                                                           | 3.15.2               | `sqlite3`{.interpreted-text role="mod"}                                                                                      |
+-------------------------------------------------------------------------------------------------------------------------+----------------------+------------------------------------------------------------------------------------------------------------------------------+
| [Tcl/Tk](https://www.tcl-lang.org/)                                                                                     | 8.5.12               | `tkinter`{.interpreted-text role="mod"}, `IDLE <idle>`{.interpreted-text role="ref"}, `turtle`{.interpreted-text role="mod"} |
+-------------------------------------------------------------------------------------------------------------------------+----------------------+------------------------------------------------------------------------------------------------------------------------------+
| [zlib](https://www.zlib.net)                                                                                            | 1.2.2.1              | `zlib`{.interpreted-text role="mod"}, `gzip`{.interpreted-text role="mod"}, `ensurepip`{.interpreted-text role="mod"}        |
+-------------------------------------------------------------------------------------------------------------------------+----------------------+------------------------------------------------------------------------------------------------------------------------------+
| [zstd](https://facebook.github.io/zstd/)                                                                                | 1.4.5                | `compression.zstd`{.interpreted-text role="mod"}                                                                             |
+-------------------------------------------------------------------------------------------------------------------------+----------------------+------------------------------------------------------------------------------------------------------------------------------+

Note that the table does not include all optional modules; in particular, platform-specific modules like `winreg`{.interpreted-text role="mod"} are not listed here.

::: seealso
- The [devguide](https://devguide.python.org/getting-started/setup-building/#install-dependencies) includes a full list of dependencies required to build all modules and instructions on how to install them on common platforms.
- `--with-system-expat`{.interpreted-text role="option"} allows building with an external [libexpat](https://libexpat.github.io/) library.
- `configure-options-for-dependencies`{.interpreted-text role="ref"}
:::

::: versionchanged
3.1 Tcl/Tk version 8.3.1 is now required for `tkinter`{.interpreted-text role="mod"}.
:::

::: versionchanged
3.5 Tcl/Tk version 8.4 is now required for `tkinter`{.interpreted-text role="mod"}.
:::

::: versionchanged
3.7 OpenSSL 1.0.2 is now required for `hashlib`{.interpreted-text role="mod"} and `ssl`{.interpreted-text role="mod"}.
:::

::: versionchanged
3.10 OpenSSL 1.1.1 is now required for `hashlib`{.interpreted-text role="mod"} and `ssl`{.interpreted-text role="mod"}. SQLite 3.7.15 is now required for `sqlite3`{.interpreted-text role="mod"}.
:::

::: versionchanged
3.11 Tcl/Tk version 8.5.12 is now required for `tkinter`{.interpreted-text role="mod"}.
:::

::: versionchanged
3.13 SQLite 3.15.2 is now required for `sqlite3`{.interpreted-text role="mod"}.
:::

## Generated files

To reduce build dependencies, Python source code contains multiple generated files. Commands to regenerate all generated files:

``` sh
make regen-all
make regen-stdlib-module-names
make regen-limited-abi
make regen-configure
```

The `Makefile.pre.in` file documents generated files, their inputs, and tools used to regenerate them. Search for `regen-*` make targets.

### configure script

The `make regen-configure` command regenerates the `aclocal.m4` file and the `configure` script using the `Tools/build/regen-configure.sh` shell script which uses an Ubuntu container to get the same tools versions and have a reproducible output.

The container is optional, the following command can be run locally:

``` sh
autoreconf -ivf -Werror
```

The generated files can change depending on the exact versions of the tools used. The container that CPython uses has [Autoconf](https://gnu.org/software/autoconf) 2.72, `aclocal` from [Automake](https://www.gnu.org/software/automake) 1.16.5, and [pkg-config](https://www.freedesktop.org/wiki/Software/pkg-config/) 1.8.1.

::: versionchanged
3.13 Autoconf 2.71 and aclocal 1.16.5 and are now used to regenerate `configure`{.interpreted-text role="file"}.
:::

::: versionchanged
3.14 Autoconf 2.72 is now used to regenerate `configure`{.interpreted-text role="file"}.
:::

## Configure Options

List all `configure`{.interpreted-text role="file"} script options using:

``` sh
./configure --help
```

See also the `Misc/SpecialBuilds.txt`{.interpreted-text role="file"} in the Python source distribution.

### General Options

:::: option

`--enable-loadable-sqlite-extensions`

:   

Support loadable extensions in the `!_sqlite`{.interpreted-text role="mod"} extension module (default is no) of the `sqlite3`{.interpreted-text role="mod"} module.

See the `sqlite3.Connection.enable_load_extension`{.interpreted-text role="meth"} method of the `sqlite3`{.interpreted-text role="mod"} module.

::: versionadded
3.6
:::
::::

::: option

`--disable-ipv6`

:   

Disable IPv6 support (enabled by default if supported), see the `socket`{.interpreted-text role="mod"} module.
:::

::: option
\--enable-big-digits=\[15\|30\]

Define the size in bits of Python `int`{.interpreted-text role="class"} digits: 15 or 30 bits.

By default, the digit size is 30.

Define the `PYLONG_BITS_IN_DIGIT` to `15` or `30`.

See `sys.int_info.bits_per_digit <sys.int_info>`{.interpreted-text role="data"}.
:::

:::: option

`--with-suffix=SUFFIX`

:   

Set the Python executable suffix to *SUFFIX*.

The default suffix is `.exe` on Windows and macOS (`python.exe` executable), `.js` on Emscripten node, `.html` on Emscripten browser, `.wasm` on WASI, and an empty string on other platforms (`python` executable).

::: versionchanged
3.11 The default suffix on WASM platform is one of `.js`, `.html` or `.wasm`.
:::
::::

:::: option

`--with-tzpath=<list of absolute paths separated by pathsep>`

:   

Select the default time zone search path for `zoneinfo.TZPATH`{.interpreted-text role="const"}. See the `Compile-time configuration
<zoneinfo_data_compile_time_config>`{.interpreted-text role="ref"} of the `zoneinfo`{.interpreted-text role="mod"} module.

Default: `/usr/share/zoneinfo:/usr/lib/zoneinfo:/usr/share/lib/zoneinfo:/etc/zoneinfo`.

See `os.pathsep`{.interpreted-text role="data"} path separator.

::: versionadded
3.9
:::
::::

:::: option

`--without-decimal-contextvar`

:   

Build the `_decimal` extension module using a thread-local context rather than a coroutine-local context (default), see the `decimal`{.interpreted-text role="mod"} module.

See `decimal.HAVE_CONTEXTVAR`{.interpreted-text role="const"} and the `contextvars`{.interpreted-text role="mod"} module.

::: versionadded
3.9
:::
::::

::: option

`--with-dbmliborder=<list of backend names>`

:   

Override order to check db backends for the `dbm`{.interpreted-text role="mod"} module

A valid value is a colon (`:`) separated string with the backend names:

- `ndbm`;
- `gdbm`;
- `bdb`.
:::

::: option

`--without-c-locale-coercion`

:   

Disable C locale coercion to a UTF-8 based locale (enabled by default).

Don\'t define the `PY_COERCE_C_LOCALE` macro.

See `PYTHONCOERCECLOCALE`{.interpreted-text role="envvar"} and the `538`{.interpreted-text role="pep"}.
:::

:::: option

`--with-platlibdir=DIRNAME`

:   

Python library directory name (default is `lib`).

Fedora and SuSE use `lib64` on 64-bit platforms.

See `sys.platlibdir`{.interpreted-text role="data"}.

::: versionadded
3.9
:::
::::

:::: option

`--with-wheel-pkg-dir=PATH`

:   

Directory of wheel packages used by the `ensurepip`{.interpreted-text role="mod"} module (none by default).

Some Linux distribution packaging policies recommend against bundling dependencies. For example, Fedora installs wheel packages in the `/usr/share/python-wheels/` directory and don\'t install the `!ensurepip._bundled`{.interpreted-text role="mod"} package.

::: versionadded
3.10
:::
::::

:::: option
\--with-pkg-config=\[check[\|yes\|](##SUBST##|yes|)no\]

Whether configure should use `pkg-config`{.interpreted-text role="program"} to detect build dependencies.

- `check` (default): `pkg-config`{.interpreted-text role="program"} is optional
- `yes`: `pkg-config`{.interpreted-text role="program"} is mandatory
- `no`: configure does not use `pkg-config`{.interpreted-text role="program"} even when present

::: versionadded
3.11
:::
::::

:::: option

`--with-missing-stdlib-config=FILE`

:   

Path to a [JSON](https://www.json.org/json-en.html) configuration file containing custom error messages for missing `standard library`{.interpreted-text role="term"} modules.

This option is intended for Python distributors who wish to provide distribution-specific guidance when users encounter standard library modules that are missing or packaged separately.

The JSON file should map missing module names to custom error message strings. For example, if your distribution packages `tkinter`{.interpreted-text role="mod"} and `_tkinter`{.interpreted-text role="mod"} separately and excludes `!_gdbm`{.interpreted-text role="mod"} for legal reasons, the configuration could contain:

``` json
{
    "_gdbm": "The '_gdbm' module is not available in this distribution",
    "tkinter": "Install the python-tk package to use tkinter",
    "_tkinter": "Install the python-tk package to use tkinter",
}
```

::: versionadded
3.15
:::
::::

:::: option

`--enable-pystats`

:   

Turn on internal Python performance statistics gathering.

By default, statistics gathering is off. Use `python3 -X pystats` command or set `PYTHONSTATS=1` environment variable to turn on statistics gathering at Python startup.

At Python exit, dump statistics if statistics gathering was on and not cleared.

Effects:

- Add `-X pystats <-X>`{.interpreted-text role="option"} command line option.
- Add `!PYTHONSTATS`{.interpreted-text role="envvar"} environment variable.
- Define the `Py_STATS` macro.
- Add functions to the `sys`{.interpreted-text role="mod"} module:
  - `!sys._stats_on`{.interpreted-text role="func"}: Turns on statistics gathering.
  - `!sys._stats_off`{.interpreted-text role="func"}: Turns off statistics gathering.
  - `!sys._stats_clear`{.interpreted-text role="func"}: Clears the statistics.
  - `!sys._stats_dump`{.interpreted-text role="func"}: Dump statistics to file, and clears the statistics.

The statistics will be dumped to a arbitrary (probably unique) file in `/tmp/py_stats/` (Unix) or `C:\temp\py_stats\` (Windows). If that directory does not exist, results will be printed on stderr.

Use `Tools/scripts/summarize_stats.py` to read the stats.

Statistics:

- Opcode:
  - Specialization: success, failure, hit, deferred, miss, deopt, failures;
  - Execution count;
  - Pair count.
- Call:
  - Inlined Python calls;
  - PyEval calls;
  - Frames pushed;
  - Frame object created;
  - Eval calls: vector, generator, legacy, function VECTORCALL, build class, slot, function \"ex\", API, method.
- Object:
  - incref and decref;
  - interpreter incref and decref;
  - allocations: all, 512 bytes, 4 kiB, big;
  - free;
  - to/from free lists;
  - dictionary materialized/dematerialized;
  - type cache;
  - optimization attempts;
  - optimization traces created/executed;
  - uops executed.
- Garbage collector:
  - Garbage collections;
  - Objects visited;
  - Objects collected.

::: versionadded
3.11
:::
::::

::::: {#free-threading-build}
:::: option

`--disable-gil`

:   

Enables support for running Python without the `global interpreter
lock`{.interpreted-text role="term"} (GIL): `free-threaded build`{.interpreted-text role="term"}.

Defines the `Py_GIL_DISABLED` macro and adds `"t"` to `sys.abiflags`{.interpreted-text role="data"}.

See `whatsnew313-free-threaded-cpython`{.interpreted-text role="ref"} for more detail.

::: versionadded
3.13
:::
::::
:::::

:::::: option
\--enable-experimental-jit=\[no[\|yes\|](##SUBST##|yes|)yes-off\|interpreter\]

Indicate how to integrate the `experimental just-in-time compiler <whatsnew314-jit-compiler>`{.interpreted-text role="ref"}.

- `no`: Don\'t build the JIT.
- `yes`: Enable the JIT. To disable it at runtime, set the environment variable `PYTHON_JIT=0 <PYTHON_JIT>`{.interpreted-text role="envvar"}.
- `yes-off`: Build the JIT, but disable it by default. To enable it at runtime, set the environment variable `PYTHON_JIT=1 <PYTHON_JIT>`{.interpreted-text role="envvar"}.
- `interpreter`: Enable the \"JIT interpreter\" (only useful for those debugging the JIT itself). To disable it at runtime, set the environment variable `PYTHON_JIT=0 <PYTHON_JIT>`{.interpreted-text role="envvar"}.

`--enable-experimental-jit=no` is the default behavior if the option is not provided, and `--enable-experimental-jit` is shorthand for `--enable-experimental-jit=yes`. See `Tools/jit/README.md`{.interpreted-text role="file"} for more information, including how to install the necessary build-time dependencies.

:::: note
::: title
Note
:::

When building CPython with JIT enabled, ensure that your system has Python 3.11 or later installed.
::::

::: versionadded
3.13
:::
::::::

::: option
PKG_CONFIG

Path to `pkg-config` utility.
:::

::: option
PKG_CONFIG_LIBDIR
:::

::: option
PKG_CONFIG_PATH

`pkg-config` options.
:::

### C compiler options

::: option
CC

C compiler command.
:::

::: option
CFLAGS

C compiler flags.
:::

::: option
CPP

C preprocessor command.
:::

::: option
CPPFLAGS

C preprocessor flags, e.g. `-I{include_dir}`{.interpreted-text role="samp"}.
:::

### Linker options

::: option
LDFLAGS

Linker flags, e.g. `-L{library_directory}`{.interpreted-text role="samp"}.
:::

::: option
LIBS

Libraries to pass to the linker, e.g. `-l{library}`{.interpreted-text role="samp"}.
:::

::: option
MACHDEP

Name for machine-dependent library files.
:::

### Options for third-party dependencies {#configure-options-for-dependencies}

::: versionadded
3.11
:::

::: option
BZIP2_CFLAGS
:::

::: option
BZIP2_LIBS

C compiler and linker flags to link Python to `libbz2`, used by `bz2`{.interpreted-text role="mod"} module, overriding `pkg-config`.
:::

::: option
CURSES_CFLAGS
:::

::: option
CURSES_LIBS

C compiler and linker flags for `libncurses` or `libncursesw`, used by `curses`{.interpreted-text role="mod"} module, overriding `pkg-config`.
:::

::: option
GDBM_CFLAGS
:::

::: option
GDBM_LIBS

C compiler and linker flags for `gdbm`.
:::

::: option
LIBEDIT_CFLAGS
:::

::: option
LIBEDIT_LIBS

C compiler and linker flags for `libedit`, used by `readline`{.interpreted-text role="mod"} module, overriding `pkg-config`.
:::

::: option
LIBFFI_CFLAGS
:::

::: option
LIBFFI_LIBS

C compiler and linker flags for `libffi`, used by `ctypes`{.interpreted-text role="mod"} module, overriding `pkg-config`.
:::

::: option
LIBMPDEC_CFLAGS
:::

::::: option
LIBMPDEC_LIBS

C compiler and linker flags for `libmpdec`, used by `decimal`{.interpreted-text role="mod"} module, overriding `pkg-config`.

:::: note
::: title
Note
:::

These environment variables have no effect unless `--with-system-libmpdec`{.interpreted-text role="option"} is specified.
::::
:::::

::: option
LIBLZMA_CFLAGS
:::

::: option
LIBLZMA_LIBS

C compiler and linker flags for `liblzma`, used by `lzma`{.interpreted-text role="mod"} module, overriding `pkg-config`.
:::

::: option
LIBREADLINE_CFLAGS
:::

::: option
LIBREADLINE_LIBS

C compiler and linker flags for `libreadline`, used by `readline`{.interpreted-text role="mod"} module, overriding `pkg-config`.
:::

::: option
LIBSQLITE3_CFLAGS
:::

::: option
LIBSQLITE3_LIBS

C compiler and linker flags for `libsqlite3`, used by `sqlite3`{.interpreted-text role="mod"} module, overriding `pkg-config`.
:::

::: option
LIBUUID_CFLAGS
:::

::: option
LIBUUID_LIBS

C compiler and linker flags for `libuuid`, used by `uuid`{.interpreted-text role="mod"} module, overriding `pkg-config`.
:::

::: option
LIBZSTD_CFLAGS
:::

:::: option
LIBZSTD_LIBS

C compiler and linker flags for `libzstd`, used by `compression.zstd`{.interpreted-text role="mod"} module, overriding `pkg-config`.

::: versionadded
3.14
:::
::::

::: option
PANEL_CFLAGS
:::

::: option
PANEL_LIBS

C compiler and linker flags for PANEL, overriding `pkg-config`.

C compiler and linker flags for `libpanel` or `libpanelw`, used by `curses.panel`{.interpreted-text role="mod"} module, overriding `pkg-config`.
:::

::: option
TCLTK_CFLAGS
:::

::: option
TCLTK_LIBS

C compiler and linker flags for TCLTK, overriding `pkg-config`.
:::

::: option
ZLIB_CFLAGS
:::

::: option
ZLIB_LIBS

C compiler and linker flags for `libzlib`, used by `gzip`{.interpreted-text role="mod"} module, overriding `pkg-config`.
:::

### WebAssembly Options

:::: option

`--enable-wasm-dynamic-linking`

:   

Turn on dynamic linking support for WASM.

Dynamic linking enables `dlopen`. File size of the executable increases due to limited dead code elimination and additional features.

::: versionadded
3.11
:::
::::

:::: option

`--enable-wasm-pthreads`

:   

Turn on pthreads support for WASM.

::: versionadded
3.11
:::
::::

### Install Options

::: option

`--prefix=PREFIX`

:   

Install architecture-independent files in PREFIX. On Unix, it defaults to `/usr/local`{.interpreted-text role="file"}.

This value can be retrieved at runtime using `sys.prefix`{.interpreted-text role="data"}.

As an example, one can use `--prefix="$HOME/.local/"` to install a Python in its home directory.
:::

::: option

`--exec-prefix=EPREFIX`

:   

Install architecture-dependent files in EPREFIX, defaults to `--prefix`{.interpreted-text role="option"}.

This value can be retrieved at runtime using `sys.exec_prefix`{.interpreted-text role="data"}.
:::

:::: option

`--disable-test-modules`

:   

Don\'t build nor install test modules, like the `test`{.interpreted-text role="mod"} package or the `!_testcapi`{.interpreted-text role="mod"} extension module (built and installed by default).

::: versionadded
3.10
:::
::::

:::: option
\--with-ensurepip=\[upgrade[\|install\|](##SUBST##|install|)no\]

Select the `ensurepip`{.interpreted-text role="mod"} command run on Python installation:

- `upgrade` (default): run `python -m ensurepip --altinstall --upgrade` command.
- `install`: run `python -m ensurepip --altinstall` command;
- `no`: don\'t run ensurepip;

::: versionadded
3.6
:::
::::

### Performance options

Configuring Python using `--enable-optimizations --with-lto` (PGO + LTO) is recommended for best performance. The experimental `--enable-bolt` flag can also be used to improve performance.

::::::: option

`--enable-optimizations`

:   

Enable Profile Guided Optimization (PGO) using `PROFILE_TASK`{.interpreted-text role="envvar"} (disabled by default).

The C compiler Clang requires `llvm-profdata` program for PGO. On macOS, GCC also requires it: GCC is just an alias to Clang on macOS.

Disable also semantic interposition in libpython if `--enable-shared` and GCC is used: add `-fno-semantic-interposition` to the compiler and linker flags.

:::: note
::: title
Note
:::

During the build, you may encounter compiler warnings about profile data not being available for some source files. These warnings are harmless, as only a subset of the code is exercised during profile data acquisition. To disable these warnings on Clang, manually suppress them by adding `-Wno-profile-instr-unprofiled` to `CFLAGS`{.interpreted-text role="envvar"}.
::::

::: versionadded
3.6
:::

::: versionchanged
3.10 Use `-fno-semantic-interposition` on GCC.
:::
:::::::

::::: envvar
PROFILE_TASK

Environment variable used in the Makefile: Python command line arguments for the PGO generation task.

Default: `-m test --pgo --timeout=$(TESTTIMEOUT)`.

::: versionadded
3.8
:::

::: versionchanged
3.13 Task failure is no longer ignored silently.
:::
:::::

:::::: option
\--with-lto=\[full[\|thin\|](##SUBST##|thin|)no\|yes\]

Enable Link Time Optimization (LTO) in any build (disabled by default).

The C compiler Clang requires `llvm-ar` for LTO (`ar` on macOS), as well as an LTO-aware linker (`ld.gold` or `lld`).

::: versionadded
3.6
:::

::: versionadded
3.11 To use ThinLTO feature, use `--with-lto=thin` on Clang.
:::

::: versionchanged
3.12 Use ThinLTO as the default optimization policy on Clang if the compiler accepts the flag.
:::
::::::

:::: option

`--enable-bolt`

:   

Enable usage of the [BOLT post-link binary optimizer](https://github.com/llvm/llvm-project/tree/main/bolt) (disabled by default).

BOLT is part of the LLVM project but is not always included in their binary distributions. This flag requires that `llvm-bolt` and `merge-fdata` are available.

BOLT is still a fairly new project so this flag should be considered experimental for now. Because this tool operates on machine code its success is dependent on a combination of the build environment + the other optimization configure args + the CPU architecture, and not all combinations are supported. BOLT versions before LLVM 16 are known to crash BOLT under some scenarios. Use of LLVM 16 or newer for BOLT optimization is strongly encouraged.

The `!BOLT_INSTRUMENT_FLAGS`{.interpreted-text role="envvar"} and `!BOLT_APPLY_FLAGS`{.interpreted-text role="envvar"} `configure`{.interpreted-text role="program"} variables can be defined to override the default set of arguments for `llvm-bolt`{.interpreted-text role="program"} to instrument and apply BOLT data to binaries, respectively.

::: versionadded
3.12
:::
::::

:::: option
BOLT_APPLY_FLAGS

Arguments to `llvm-bolt` when creating a [BOLT optimized binary](https://github.com/facebookarchive/BOLT).

::: versionadded
3.12
:::
::::

:::: option
BOLT_INSTRUMENT_FLAGS

Arguments to `llvm-bolt` when instrumenting binaries.

::: versionadded
3.12
:::
::::

::: option

`--with-computed-gotos`

:   

Enable computed gotos in evaluation loop (enabled by default on supported compilers).
:::

:::: option

`--with-tail-call-interp`

:   

Enable interpreters using tail calls in CPython. If enabled, enabling PGO (`--enable-optimizations`{.interpreted-text role="option"}) is highly recommended. This option specifically requires a C compiler with proper tail call support, and the [preserve_none](https://clang.llvm.org/docs/AttributeReference.html#preserve-none) calling convention. For example, Clang 19 and newer supports this feature.

::: versionadded
3.14
:::
::::

::: option

`--without-mimalloc`

:   

Disable the fast `mimalloc <mimalloc>`{.interpreted-text role="ref"} allocator (enabled by default).

See also `PYTHONMALLOC`{.interpreted-text role="envvar"} environment variable.
:::

::: option

`--without-pymalloc`

:   

Disable the specialized Python memory allocator `pymalloc <pymalloc>`{.interpreted-text role="ref"} (enabled by default).

See also `PYTHONMALLOC`{.interpreted-text role="envvar"} environment variable.
:::

:::: option

`--with-pymalloc-hugepages`

:   

Enable huge page support for `pymalloc <pymalloc>`{.interpreted-text role="ref"} arenas (disabled by default). When enabled, the arena size on 64-bit platforms is increased to 2 MiB and arena allocation uses `MAP_HUGETLB` (Linux) or `MEM_LARGE_PAGES` (Windows) with automatic fallback to regular pages.

Even when compiled with this option, huge pages are **not** used at runtime unless the `PYTHON_PYMALLOC_HUGEPAGES`{.interpreted-text role="envvar"} environment variable is set to `1`. This opt-in is required because huge pages carry risks on Linux: if the huge-page pool is exhausted, page faults (including copy-on-write faults after `os.fork`{.interpreted-text role="func"}) deliver `SIGBUS` and kill the process.

The configure script checks that the platform supports `MAP_HUGETLB` and emits a warning if it is not available.

On Windows, use the `--pymalloc-hugepages` flag with `build.bat` or set the `UsePymallocHugepages` MSBuild property.

::: versionadded
3.15
:::
::::

::: option

`--without-doc-strings`

:   

Disable static documentation strings to reduce the memory footprint (enabled by default). Documentation strings defined in Python are not affected.

Don\'t define the `WITH_DOC_STRINGS` macro.

See the `PyDoc_STRVAR()` macro.
:::

::: option

`--enable-profiling`

:   

Enable C-level code profiling with `gprof` (disabled by default).
:::

::: option

`--with-strict-overflow`

:   

Add `-fstrict-overflow` to the C compiler flags (by default we add `-fno-strict-overflow` instead).
:::

:::: option

`--without-remote-debug`

:   

Deactivate remote debugging support described in `768`{.interpreted-text role="pep"} (enabled by default). When this flag is provided the code that allows the interpreter to schedule the execution of a Python file in a separate process as described in `768`{.interpreted-text role="pep"} is not compiled. This includes both the functionality to schedule code to be executed and the functionality to receive code to be executed.

> This macro is defined by default, unless Python is configured with `--without-remote-debug`{.interpreted-text role="option"}.
>
> Note that even if the macro is defined, remote debugging may not be available (for example, on an incompatible platform).

::: versionadded
3.14
:::
::::

### Python Debug Build {#debug-build}

A debug build is Python built with the `--with-pydebug`{.interpreted-text role="option"} configure option.

Effects of a debug build:

- Display all warnings by default: the list of default warning filters is empty in the `warnings`{.interpreted-text role="mod"} module.
- Add `d` to `sys.abiflags`{.interpreted-text role="data"}.
- Add `!sys.gettotalrefcount`{.interpreted-text role="func"} function.
- Add `-X showrefcount <-X>`{.interpreted-text role="option"} command line option.
- Add `-d`{.interpreted-text role="option"} command line option and `PYTHONDEBUG`{.interpreted-text role="envvar"} environment variable to debug the parser.
- Add support for the `__lltrace__` variable: enable low-level tracing in the bytecode evaluation loop if the variable is defined.
- Install `debug hooks on memory allocators <default-memory-allocators>`{.interpreted-text role="ref"} to detect buffer overflow and other memory errors.
- Define `Py_DEBUG` and `Py_REF_DEBUG` macros.
- Add runtime checks: code surrounded by `#ifdef Py_DEBUG` and `#endif`. Enable `assert(...)` and `_PyObject_ASSERT(...)` assertions: don\'t set the `NDEBUG` macro (see also the `--with-assertions`{.interpreted-text role="option"} configure option). Main runtime checks:
  - Add sanity checks on the function arguments.
  - Unicode and int objects are created with their memory filled with a pattern to detect usage of uninitialized objects.
  - Ensure that functions which can clear or replace the current exception are not called with an exception raised.
  - Check that deallocator functions don\'t change the current exception.
  - The garbage collector (`gc.collect`{.interpreted-text role="func"} function) runs some basic checks on objects consistency.
  - The `!Py_SAFE_DOWNCAST()`{.interpreted-text role="c:macro"} macro checks for integer underflow and overflow when downcasting from wide types to narrow types.

See also the `Python Development Mode <devmode>`{.interpreted-text role="ref"} and the `--with-trace-refs`{.interpreted-text role="option"} configure option.

::: versionchanged
3.8 Release builds and debug builds are now ABI compatible: defining the `Py_DEBUG` macro no longer implies the `Py_TRACE_REFS` macro (see the `--with-trace-refs`{.interpreted-text role="option"} option).
:::

### Debug options

::: option

`--with-pydebug`

:   

`Build Python in debug mode <debug-build>`{.interpreted-text role="ref"}: define the `Py_DEBUG` macro (disabled by default).
:::

::::: option

`--with-trace-refs`

:   

Enable tracing references for debugging purpose (disabled by default).

Effects:

- Define the `Py_TRACE_REFS` macro.
- Add `sys.getobjects`{.interpreted-text role="func"} function.
- Add `PYTHONDUMPREFS`{.interpreted-text role="envvar"} environment variable.

The `PYTHONDUMPREFS`{.interpreted-text role="envvar"} environment variable can be used to dump objects and reference counts still alive at Python exit.

`Statically allocated objects <static-types>`{.interpreted-text role="ref"} are not traced.

::: versionadded
3.8
:::

::: versionchanged
3.13 This build is now ABI compatible with release build and `debug build
<debug-build>`{.interpreted-text role="ref"}.
:::
:::::

:::: option

`--with-assertions`

:   

Build with C assertions enabled (default is no): `assert(...);` and `_PyObject_ASSERT(...);`.

If set, the `NDEBUG` macro is not defined in the `OPT`{.interpreted-text role="envvar"} compiler variable.

See also the `--with-pydebug`{.interpreted-text role="option"} option (`debug build
<debug-build>`{.interpreted-text role="ref"}) which also enables assertions.

::: versionadded
3.6
:::
::::

::: option

`--with-valgrind`

:   

Enable Valgrind support (default is no).
:::

:::: option

`--with-dtrace`

:   

Enable DTrace support (default is no).

See `Instrumenting CPython with DTrace and SystemTap
<instrumentation>`{.interpreted-text role="ref"}.

::: versionadded
3.6
:::
::::

:::: option

`--with-address-sanitizer`

:   

Enable AddressSanitizer memory error detector, `asan` (default is no). To improve ASan detection capabilities you may also want to combine this with `--without-pymalloc`{.interpreted-text role="option"} to disable the specialized small-object allocator whose allocations are not tracked by ASan.

::: versionadded
3.6
:::
::::

:::: option

`--with-memory-sanitizer`

:   

Enable MemorySanitizer allocation error detector, `msan` (default is no).

::: versionadded
3.6
:::
::::

:::: option

`--with-undefined-behavior-sanitizer`

:   

Enable UndefinedBehaviorSanitizer undefined behaviour detector, `ubsan` (default is no).

::: versionadded
3.6
:::
::::

:::: option

`--with-thread-sanitizer`

:   

Enable ThreadSanitizer data race detector, `tsan` (default is no).

::: versionadded
3.13
:::
::::

### Linker options

::: option

`--enable-shared`

:   

Enable building a shared Python library: `libpython` (default is no).
:::

:::: option

`--without-static-libpython`

:   

Do not build `libpythonMAJOR.MINOR.a` and do not install `python.o` (built and enabled by default).

::: versionadded
3.10
:::
::::

### Libraries options

::: option
\--with-libs=\'lib1 \...\'

Link against additional libraries (default is no).
:::

::: option

`--with-system-expat`

:   

Build the `!pyexpat`{.interpreted-text role="mod"} module using an installed `expat` library (default is no).
:::

:::::::: option

`--with-system-libmpdec`

:   

Build the `_decimal` extension module using an installed `mpdecimal` library, see the `decimal`{.interpreted-text role="mod"} module (default is yes).

::: versionadded
3.3
:::

::: versionchanged
3.13 Default to using the installed `mpdecimal` library.
:::

::: versionchanged
3.15

A bundled copy of the library will no longer be selected implicitly if an installed `mpdecimal` library is not found. In Python 3.15 only, it can still be selected explicitly using `--with-system-libmpdec=no` or `--without-system-libmpdec`.
:::

::: deprecated-removed
3.13 3.16 A copy of the `mpdecimal` library sources will no longer be distributed with Python 3.16.
:::

::: seealso
`LIBMPDEC_CFLAGS`{.interpreted-text role="option"} and `LIBMPDEC_LIBS`{.interpreted-text role="option"}.
:::
::::::::

:::: option
\--with-readline=readline\|editline

Designate a backend library for the `readline`{.interpreted-text role="mod"} module.

- readline: Use readline as the backend.
- editline: Use editline as the backend.

::: versionadded
3.10
:::
::::

:::: option

`--without-readline`

:   

Don\'t build the `readline`{.interpreted-text role="mod"} module (built by default).

Don\'t define the `HAVE_LIBREADLINE` macro.

::: versionadded
3.10
:::
::::

::: option

`--with-libm=STRING`

:   

Override `libm` math library to *STRING* (default is system-dependent).
:::

::: option

`--with-libc=STRING`

:   

Override `libc` C library to *STRING* (default is system-dependent).
:::

:::: option

`--with-openssl=DIR`

:   

Root of the OpenSSL directory.

::: versionadded
3.7
:::
::::

:::: option
\--with-openssl-rpath=\[no[\|auto\|](##SUBST##|auto|)DIR\]

Set runtime library directory (rpath) for OpenSSL libraries:

- `no` (default): don\'t set rpath;
- `auto`: auto-detect rpath from `--with-openssl`{.interpreted-text role="option"} and `pkg-config`;
- *DIR*: set an explicit rpath.

::: versionadded
3.10
:::
::::

### Security Options

::::: option
\--with-hash-algorithm=\[fnv[\|siphash13\|](##SUBST##|siphash13|)siphash24\]

Select hash algorithm for use in `Python/pyhash.c`:

- `siphash13` (default);
- `siphash24`;
- `fnv`.

::: versionadded
3.4
:::

::: versionadded
3.11 `siphash13` is added and it is the new default.
:::
:::::

:::: option
\--with-builtin-hashlib-hashes=md5,sha1,sha256,sha512,sha3,blake2

Built-in hash modules:

- `md5`;
- `sha1`;
- `sha256`;
- `sha512`;
- `sha3` (with shake);
- `blake2`.

::: versionadded
3.9
:::
::::

::::: option
\--with-ssl-default-suites=\[python[\|openssl\|](##SUBST##|openssl|)STRING\]

Override the OpenSSL default cipher suites string:

- `python` (default): use Python\'s preferred selection;
- `openssl`: leave OpenSSL\'s defaults untouched;
- *STRING*: use a custom string

See the `ssl`{.interpreted-text role="mod"} module.

::: versionadded
3.7
:::

::: versionchanged
3.10

The settings `python` and *STRING* also set TLS 1.2 as minimum protocol version.
:::
:::::

:::: option

`--disable-safety`

:   

Disable compiler options that are [recommended by OpenSSF](https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.md) for security reasons with no performance overhead. If this option is not enabled, CPython will be built based on safety compiler options with no slow down. When this option is enabled, CPython will not be built with the compiler options listed below.

The following compiler options are disabled with `!--disable-safety`{.interpreted-text role="option"}:

- [-fstack-protector-strong](https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.md#enable-run-time-checks-for-stack-based-buffer-overflows): Enable run-time checks for stack-based buffer overflows.
- [-Wtrampolines](https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.md#enable-warning-about-trampolines-that-require-executable-stacks): Enable warnings about trampolines that require executable stacks.

::: versionadded
3.14
:::
::::

:::: option

`--enable-slower-safety`

:   

Enable compiler options that are [recommended by OpenSSF](https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.md) for security reasons which require overhead. If this option is not enabled, CPython will not be built based on safety compiler options which performance impact. When this option is enabled, CPython will be built with the compiler options listed below.

The following compiler options are enabled with `!--enable-slower-safety`{.interpreted-text role="option"}:

- [-D_FORTIFY_SOURCE=3](https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.md#fortify-sources-for-unsafe-libc-usage-and-buffer-overflows): Fortify sources with compile- and run-time checks for unsafe libc usage and buffer overflows.

::: versionadded
3.14
:::
::::

### macOS Options

See `Mac/README.rst`{.interpreted-text role="source"}.

::: option

`--enable-universalsdk`

:   
:::

::: option

`--enable-universalsdk=SDKDIR`

:   

Create a universal binary build. *SDKDIR* specifies which macOS SDK should be used to perform the build (default is no).
:::

::: option

`--enable-framework`

:   
:::

::: option

`--enable-framework=INSTALLDIR`

:   

Create a Python.framework rather than a traditional Unix install. Optional *INSTALLDIR* specifies the installation path (default is no).
:::

::: option

`--with-universal-archs=ARCH`

:   

Specify the kind of universal binary that should be created. This option is only valid when `--enable-universalsdk`{.interpreted-text role="option"} is set.

Options:

- `universal2` (x86-64 and arm64);
- `32-bit` (PPC and i386);
- `64-bit` (PPC64 and x86-64);
- `3-way` (i386, PPC and x86-64);
- `intel` (i386 and x86-64);
- `intel-32` (i386);
- `intel-64` (x86-64);
- `all` (PPC, i386, PPC64 and x86-64).

Note that values for this configuration item are *not* the same as the identifiers used for universal binary wheels on macOS. See the Python Packaging User Guide for details on the [packaging platform compatibility tags used on macOS](https://packaging.python.org/en/latest/specifications/platform-compatibility-tags/#macos)
:::

::: option

`--with-framework-name=FRAMEWORK`

:   

Specify the name for the python framework on macOS only valid when `--enable-framework`{.interpreted-text role="option"} is set (default: `Python`).
:::

::: option

`--with-app-store-compliance`

:   
:::

:::: option

`--with-app-store-compliance=PATCH-FILE`

:   

The Python standard library contains strings that are known to trigger automated inspection tool errors when submitted for distribution by the macOS and iOS App Stores. If enabled, this option will apply the list of patches that are known to correct app store compliance. A custom patch file can also be specified. This option is disabled by default.

::: versionadded
3.13
:::
::::

### iOS Options

See `iOS/README.rst`{.interpreted-text role="source"}.

::: option

`--enable-framework=INSTALLDIR`

:   

Create a Python.framework. Unlike macOS, the *INSTALLDIR* argument specifying the installation path is mandatory.
:::

::: option

`--with-framework-name=FRAMEWORK`

:   

Specify the name for the framework (default: `Python`).
:::

### Cross Compiling Options

Cross compiling, also known as cross building, can be used to build Python for another CPU architecture or platform. Cross compiling requires a Python interpreter for the build platform. The version of the build Python must match the version of the cross compiled host Python.

::: option

`--build=BUILD`

:   

configure for building on BUILD, usually guessed by `config.guess`{.interpreted-text role="program"}.
:::

::: option

`--host=HOST`

:   

cross-compile to build programs to run on HOST (target platform)
:::

:::: option
\--with-build-python=path/to/python

path to build `python` binary for cross compiling

::: versionadded
3.11
:::
::::

::: option
CONFIG_SITE=file

An environment variable that points to a file with configure overrides.

Example *config.site* file:

``` ini
# config.site-aarch64
ac_cv_buggy_getaddrinfo=no
ac_cv_file__dev_ptmx=yes
ac_cv_file__dev_ptc=no
```
:::

:::: option
HOSTRUNNER

Program to run CPython for the host platform for cross-compilation.

::: versionadded
3.11
:::
::::

Cross compiling example:

``` sh
CONFIG_SITE=config.site-aarch64 ../configure \
    --build=x86_64-pc-linux-gnu \
    --host=aarch64-unknown-linux-gnu \
    --with-build-python=../x86_64/python
```

## Python Build System

### Main files of the build system

- `configure.ac`{.interpreted-text role="file"} =\> `configure`{.interpreted-text role="file"};
- `Makefile.pre.in`{.interpreted-text role="file"} =\> `Makefile`{.interpreted-text role="file"} (created by `configure`{.interpreted-text role="file"});
- `pyconfig.h`{.interpreted-text role="file"} (created by `configure`{.interpreted-text role="file"});
- `Modules/Setup`{.interpreted-text role="file"}: C extensions built by the Makefile using `Module/makesetup`{.interpreted-text role="file"} shell script;

### Main build steps

- C files (`.c`) are built as object files (`.o`).
- A static `libpython` library (`.a`) is created from objects files.
- `python.o` and the static `libpython` library are linked into the final `python` program.
- C extensions are built by the Makefile (see `Modules/Setup`{.interpreted-text role="file"}).

### Main Makefile targets

#### make

For the most part, when rebuilding after editing some code or refreshing your checkout from upstream, all you need to do is execute `make`, which (per Make\'s semantics) builds the default target, the first one defined in the Makefile. By tradition (including in the CPython project) this is usually the `all` target. The `configure` script expands an `autoconf` variable, `@DEF_MAKE_ALL_RULE@` to describe precisely which targets `make all` will build. The three choices are:

- `profile-opt` (configured with `--enable-optimizations`)
- `build_wasm` (chosen if the host platform matches `wasm32-wasi*` or `wasm32-emscripten`)
- `build_all` (configured without explicitly using either of the others)

Depending on the most recent source file changes, Make will rebuild any targets (object files and executables) deemed out-of-date, including running `configure` again if necessary. Source/target dependencies are many and maintained manually however, so Make sometimes doesn\'t have all the information necessary to correctly detect all targets which need to be rebuilt. Depending on which targets aren\'t rebuilt, you might experience a number of problems. If you have build or test problems which you can\'t otherwise explain, `make clean && make` should work around most dependency problems, at the expense of longer build times.

#### make platform

Build the `python` program, but don\'t build the standard library extension modules. This generates a file named `platform` which contains a single line describing the details of the build platform, e.g., `macosx-14.3-arm64-3.12` or `linux-x86_64-3.13`.

#### make profile-opt

Build Python using profile-guided optimization (PGO). You can use the configure `--enable-optimizations`{.interpreted-text role="option"} option to make this the default target of the `make` command (`make all` or just `make`).

#### make clean

Remove built files.

#### make distclean

In addition to the work done by `make clean`, remove files created by the configure script. `configure` will have to be run before building again.[^6]

#### make install

Build the `all` target and install Python.

#### make test

Build the `all` target and run the Python test suite with the `--fast-ci` option without GUI tests. Variables:

- `TESTOPTS`: additional regrtest command-line options.
- `TESTPYTHONOPTS`: additional Python command-line options.
- `TESTTIMEOUT`: timeout in seconds (default: 10 minutes).

#### make ci

This is similar to `make test`, but uses the `-ugui` to also run GUI tests.

::: versionadded
3.14
:::

#### make buildbottest

This is similar to `make test`, but uses the `--slow-ci` option and default timeout of 20 minutes, instead of `--fast-ci` option.

#### make regen-all

Regenerate (almost) all generated files. These include (but are not limited to) bytecode cases, and parser generator file. `make regen-stdlib-module-names` and `autoconf` must be run separately for the remaining [generated files](#generated-files).

### C extensions

Some C extensions are built as built-in modules, like the `sys` module. They are built with the `Py_BUILD_CORE_BUILTIN` macro defined. Built-in modules have no `__file__` attribute:

``` pycon
>>> import sys
>>> sys
<module 'sys' (built-in)>
>>> sys.__file__
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'sys' has no attribute '__file__'
```

Other C extensions are built as dynamic libraries, like the `_asyncio` module. They are built with the `Py_BUILD_CORE_MODULE` macro defined. Example on Linux x86-64:

``` pycon
>>> import _asyncio
>>> _asyncio
<module '_asyncio' from '/usr/lib64/python3.9/lib-dynload/_asyncio.cpython-39-x86_64-linux-gnu.so'>
>>> _asyncio.__file__
'/usr/lib64/python3.9/lib-dynload/_asyncio.cpython-39-x86_64-linux-gnu.so'
```

`Modules/Setup`{.interpreted-text role="file"} is used to generate Makefile targets to build C extensions. At the beginning of the files, C extensions are built as built-in modules. Extensions defined after the `*shared*` marker are built as dynamic libraries.

The `!PyAPI_FUNC()`{.interpreted-text role="c:macro"}, `!PyAPI_DATA()`{.interpreted-text role="c:macro"} and `PyMODINIT_FUNC`{.interpreted-text role="c:macro"} macros of `Include/exports.h`{.interpreted-text role="file"} are defined differently depending if the `Py_BUILD_CORE_MODULE` macro is defined:

- Use `Py_EXPORTED_SYMBOL` if the `Py_BUILD_CORE_MODULE` is defined
- Use `Py_IMPORTED_SYMBOL` otherwise.

If the `Py_BUILD_CORE_BUILTIN` macro is used by mistake on a C extension built as a shared library, its `PyInit_{xxx}()`{.interpreted-text role="samp"} function is not exported, causing an `ImportError`{.interpreted-text role="exc"} on import.

## Compiler and linker flags

Options set by the `./configure` script and environment variables and used by `Makefile`.

### Preprocessor flags

:::: envvar
CONFIGURE_CPPFLAGS

Value of `CPPFLAGS`{.interpreted-text role="envvar"} variable passed to the `./configure` script.

::: versionadded
3.6
:::
::::

::: envvar
CPPFLAGS

(Objective) C/C++ preprocessor flags, e.g. `-I{include_dir}`{.interpreted-text role="samp"} if you have headers in a nonstandard directory *include_dir*.

Both `CPPFLAGS`{.interpreted-text role="envvar"} and `LDFLAGS`{.interpreted-text role="envvar"} need to contain the shell\'s value to be able to build extension modules using the directories specified in the environment variables.
:::

:::: envvar
BASECPPFLAGS

::: versionadded
3.4
:::
::::

:::: envvar
PY_CPPFLAGS

Extra preprocessor flags added for building the interpreter object files.

Default: `$(BASECPPFLAGS) -I. -I$(srcdir)/Include $(CONFIGURE_CPPFLAGS) $(CPPFLAGS)`.

::: versionadded
3.2
:::
::::

### Compiler flags

::: envvar
CC

C compiler command.

Example: `gcc -pthread`.
:::

::: envvar
CXX

C++ compiler command.

Example: `g++ -pthread`.
:::

::: envvar
CFLAGS

C compiler flags.
:::

:::: envvar
CFLAGS_NODIST

`CFLAGS_NODIST`{.interpreted-text role="envvar"} is used for building the interpreter and stdlib C extensions. Use it when a compiler flag should *not* be part of `CFLAGS`{.interpreted-text role="envvar"} once Python is installed (`65320`{.interpreted-text role="gh"}).

In particular, `CFLAGS`{.interpreted-text role="envvar"} should not contain:

- the compiler flag `-I` (for setting the search path for include files). The `-I` flags are processed from left to right, and any flags in `CFLAGS`{.interpreted-text role="envvar"} would take precedence over user- and package-supplied `-I` flags.
- hardening flags such as `-Werror` because distributions cannot control whether packages installed by users conform to such heightened standards.

::: versionadded
3.5
:::
::::

:::: envvar
COMPILEALL_OPTS

Options passed to the `compileall`{.interpreted-text role="mod"} command line when building PYC files in `make install`. Default: `-j0`.

::: versionadded
3.12
:::
::::

::: envvar
EXTRA_CFLAGS

Extra C compiler flags.
:::

:::: envvar
CONFIGURE_CFLAGS

Value of `CFLAGS`{.interpreted-text role="envvar"} variable passed to the `./configure` script.

::: versionadded
3.2
:::
::::

:::: envvar
CONFIGURE_CFLAGS_NODIST

Value of `CFLAGS_NODIST`{.interpreted-text role="envvar"} variable passed to the `./configure` script.

::: versionadded
3.5
:::
::::

::: envvar
BASECFLAGS

Base compiler flags.
:::

::: envvar
OPT

Optimization flags.
:::

:::: envvar
CFLAGS_ALIASING

Strict or non-strict aliasing flags used to compile `Python/dtoa.c`.

::: versionadded
3.7
:::
::::

::: envvar
CCSHARED

Compiler flags used to build a shared library.

For example, `-fPIC` is used on Linux and on BSD.
:::

::: envvar
CFLAGSFORSHARED

Extra C flags added for building the interpreter object files.

Default: `$(CCSHARED)` when `--enable-shared`{.interpreted-text role="option"} is used, or an empty string otherwise.
:::

::: envvar
PY_CFLAGS

Default: `$(BASECFLAGS) $(OPT) $(CONFIGURE_CFLAGS) $(CFLAGS) $(EXTRA_CFLAGS)`.
:::

:::: envvar
PY_CFLAGS_NODIST

Default: `$(CONFIGURE_CFLAGS_NODIST) $(CFLAGS_NODIST) -I$(srcdir)/Include/internal`.

::: versionadded
3.5
:::
::::

:::: envvar
PY_STDMODULE_CFLAGS

C flags used for building the interpreter object files.

Default: `$(PY_CFLAGS) $(PY_CFLAGS_NODIST) $(PY_CPPFLAGS) $(CFLAGSFORSHARED)`.

::: versionadded
3.7
:::
::::

:::: envvar
PY_CORE_CFLAGS

Default: `$(PY_STDMODULE_CFLAGS) -DPy_BUILD_CORE`.

::: versionadded
3.2
:::
::::

:::: envvar
PY_BUILTIN_MODULE_CFLAGS

Compiler flags to build a standard library extension module as a built-in module, like the `posix`{.interpreted-text role="mod"} module.

Default: `$(PY_STDMODULE_CFLAGS) -DPy_BUILD_CORE_BUILTIN`.

::: versionadded
3.8
:::
::::

::: envvar
PURIFY

Purify command. Purify is a memory debugger program.

Default: empty string (not used).
:::

### Linker flags

::: envvar
LINKCC

Linker command used to build programs like `python` and `_testembed`.

Default: `$(PURIFY) $(CC)`.
:::

:::: envvar
CONFIGURE_LDFLAGS

Value of `LDFLAGS`{.interpreted-text role="envvar"} variable passed to the `./configure` script.

Avoid assigning `CFLAGS`{.interpreted-text role="envvar"}, `LDFLAGS`{.interpreted-text role="envvar"}, etc. so users can use them on the command line to append to these values without stomping the pre-set values.

::: versionadded
3.2
:::
::::

::: envvar
LDFLAGS_NODIST

`LDFLAGS_NODIST`{.interpreted-text role="envvar"} is used in the same manner as `CFLAGS_NODIST`{.interpreted-text role="envvar"}. Use it when a linker flag should *not* be part of `LDFLAGS`{.interpreted-text role="envvar"} once Python is installed (`65320`{.interpreted-text role="gh"}).

In particular, `LDFLAGS`{.interpreted-text role="envvar"} should not contain:

- the compiler flag `-L` (for setting the search path for libraries). The `-L` flags are processed from left to right, and any flags in `LDFLAGS`{.interpreted-text role="envvar"} would take precedence over user- and package-supplied `-L` flags.
:::

:::: envvar
CONFIGURE_LDFLAGS_NODIST

Value of `LDFLAGS_NODIST`{.interpreted-text role="envvar"} variable passed to the `./configure` script.

::: versionadded
3.8
:::
::::

::: envvar
LDFLAGS

Linker flags, e.g. `-L{lib_dir}`{.interpreted-text role="samp"} if you have libraries in a nonstandard directory *lib_dir*.

Both `CPPFLAGS`{.interpreted-text role="envvar"} and `LDFLAGS`{.interpreted-text role="envvar"} need to contain the shell\'s value to be able to build extension modules using the directories specified in the environment variables.
:::

::: envvar
LIBS

Linker flags to pass libraries to the linker when linking the Python executable.

Example: `-lrt`.
:::

::: envvar
LDSHARED

Command to build a shared library.

Default: `@LDSHARED@ $(PY_LDFLAGS)`.
:::

::: envvar
BLDSHARED

Command to build `libpython` shared library.

Default: `@BLDSHARED@ $(PY_CORE_LDFLAGS)`.
:::

::: envvar
PY_LDFLAGS

Default: `$(CONFIGURE_LDFLAGS) $(LDFLAGS)`.
:::

:::: envvar
PY_LDFLAGS_NODIST

Default: `$(CONFIGURE_LDFLAGS_NODIST) $(LDFLAGS_NODIST)`.

::: versionadded
3.8
:::
::::

:::: envvar
PY_CORE_LDFLAGS

Linker flags used for building the interpreter object files.

::: versionadded
3.8
:::
::::

**Footnotes**

[^1]: If *libmpdec* is not available, the `decimal`{.interpreted-text role="mod"} module will use a pure-Python implementation. See `--with-system-libmpdec`{.interpreted-text role="option"} for details.

[^2]: See `--with-readline`{.interpreted-text role="option"} for choosing the backend for the `readline`{.interpreted-text role="mod"} module.

[^3]: The `uuid`{.interpreted-text role="mod"} module uses `_uuid` to generate \"safe\" UUIDs. See the module documentation for details.

[^4]: The `curses`{.interpreted-text role="mod"} module requires the `libncurses` or `libncursesw` library. The `curses.panel`{.interpreted-text role="mod"} module additionally requires the `libpanel` or `libpanelw` library.

[^5]: If OpenSSL is not available, the `hashlib`{.interpreted-text role="mod"} module will use bundled implementations of several hash functions. See `--with-builtin-hashlib-hashes`{.interpreted-text role="option"} for *forcing* usage of OpenSSL.

[^6]: `git clean -fdx` is an even more extreme way to \"clean\" your checkout. It removes all files not known to Git. When bug hunting using `git bisect`, this is [recommended between probes](https://github.com/python/cpython/issues/114505#issuecomment-1907021718) to guarantee a completely clean build. **Use with care**, as it will delete all files not checked into Git, including your new, uncommitted work.
