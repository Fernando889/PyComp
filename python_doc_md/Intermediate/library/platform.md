# `!platform`{.interpreted-text role="mod"} \-\-- Access to underlying platform\'s identifying data

::: {.module synopsis="Retrieves as much platform identifying data as possible."}
platform
:::

**Source code:** `Lib/platform.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

:::: note
::: title
Note
:::

Specific platforms listed alphabetically, with Linux included in the Unix section.
::::

## Cross platform

::::: function
architecture(executable=sys.executable, bits=\'\', linkage=\'\')

Queries the given executable (defaults to the Python interpreter binary) for various architecture information.

Returns a tuple `(bits, linkage)` which contain information about the bit architecture and the linkage format used for the executable. Both values are returned as strings.

Values that cannot be determined are returned as given by the parameter presets. If bits is given as `''`, the `sizeof(pointer)` (or `sizeof(long)` on Python version \< 1.5.2) is used as indicator for the supported pointer size.

The function relies on the system\'s `file`{.interpreted-text role="file"} command to do the actual work. This is available on most if not all Unix platforms and some non-Unix platforms and then only if the executable points to the Python interpreter. Reasonable defaults are used when the above needs are not met.

:::: note
::: title
Note
:::

On macOS (and perhaps other platforms), executable files may be universal files containing multiple architectures.

To get at the \"64-bitness\" of the current interpreter, it is more reliable to query the `sys.maxsize`{.interpreted-text role="data"} attribute:

    is_64bits = sys.maxsize > 2**32
::::
:::::

::: function
machine()

Returns the machine type, e.g. `'AMD64'`. An empty string is returned if the value cannot be determined.

The output is platform-dependent and may differ in casing and naming conventions.
:::

::: function
node()

Returns the computer\'s network name (may not be fully qualified!). An empty string is returned if the value cannot be determined.
:::

:::: function
platform(aliased=False, terse=False)

Returns a single string identifying the underlying platform with as much useful information as possible.

The output is intended to be *human readable* rather than machine parseable. It may look different on different platforms and this is intended.

If *aliased* is true, the function will use aliases for various platforms that report system names which differ from their common names, for example SunOS will be reported as Solaris. The `system_alias`{.interpreted-text role="func"} function is used to implement this.

Setting *terse* to true causes the function to return only the absolute minimum information needed to identify the platform.

::: versionchanged
3.8 On macOS, the function now uses `mac_ver`{.interpreted-text role="func"}, if it returns a non-empty release string, to get the macOS version rather than the darwin version.
:::
::::

::: function
processor()

Returns the (real) processor name, e.g. `'amdk6'`.

An empty string is returned if the value cannot be determined. Note that many platforms do not provide this information or simply return the same value as for `machine`{.interpreted-text role="func"}. NetBSD does this.
:::

::: function
python_build()

Returns a tuple `(buildno, builddate)` stating the Python build number and date as strings.
:::

::: function
python_compiler()

Returns a string identifying the compiler used for compiling Python.
:::

::: function
python_branch()

Returns a string identifying the Python implementation SCM branch.
:::

::: function
python_implementation()

Returns a string identifying the Python implementation. Possible return values are: \'CPython\', \'IronPython\', \'Jython\', \'PyPy\'.
:::

::: function
python_revision()

Returns a string identifying the Python implementation SCM revision.
:::

::: function
python_version()

Returns the Python version as string `'major.minor.patchlevel'`.

Note that unlike the Python `sys.version`, the returned value will always include the patchlevel (it defaults to 0).
:::

::: function
python_version_tuple()

Returns the Python version as tuple `(major, minor, patchlevel)` of strings.

Note that unlike the Python `sys.version`, the returned value will always include the patchlevel (it defaults to `'0'`).
:::

::: function
release()

Returns the system\'s release, e.g. `'2.2.0'` or `'NT'`. An empty string is returned if the value cannot be determined.
:::

::: function
system()

Returns the system/OS name, such as `'Linux'`, `'Darwin'`, `'Java'`, `'Windows'`. An empty string is returned if the value cannot be determined.

On iOS and Android, this returns the user-facing OS name (i.e, `'iOS`, `'iPadOS'` or `'Android'`). To obtain the kernel name (`'Darwin'` or `'Linux'`), use `os.uname`{.interpreted-text role="func"}.
:::

::: function
system_alias(system, release, version)

Returns `(system, release, version)` aliased to common marketing names used for some systems. It also does some reordering of the information in some cases where it would otherwise cause confusion.
:::

::: function
version()

Returns the system\'s release version, e.g. `'#3 on degas'`. An empty string is returned if the value cannot be determined.

On iOS and Android, this is the user-facing OS version. To obtain the Darwin or Linux kernel version, use `os.uname`{.interpreted-text role="func"}.
:::

::::: function
uname()

Fairly portable uname interface. Returns a `~collections.namedtuple`{.interpreted-text role="func"} containing six attributes: `system`{.interpreted-text role="attr"}, `node`{.interpreted-text role="attr"}, `release`{.interpreted-text role="attr"}, `version`{.interpreted-text role="attr"}, `machine`{.interpreted-text role="attr"}, and `processor`{.interpreted-text role="attr"}.

`processor`{.interpreted-text role="attr"} is resolved late, on demand.

Note: the first two attribute names differ from the names presented by `os.uname`{.interpreted-text role="func"}, where they are named `!sysname`{.interpreted-text role="attr"} and `!nodename`{.interpreted-text role="attr"}.

Entries which cannot be determined are set to `''`.

::: versionchanged
3.3 Result changed from a tuple to a `~collections.namedtuple`{.interpreted-text role="func"}.
:::

::: versionchanged
3.9 `processor`{.interpreted-text role="attr"} is resolved late instead of immediately.
:::
:::::

:::: function
invalidate_caches()

Clear out the internal cache of information, such as the `uname`{.interpreted-text role="func"}. This is typically useful when the platform\'s `node`{.interpreted-text role="func"} is changed by an external process and one needs to retrieve the updated value.

::: versionadded
3.14
:::
::::

## Windows platform

::: function
win32_ver(release=\'\', version=\'\', csd=\'\', ptype=\'\')

Get additional version information from the Windows Registry and return a tuple `(release, version, csd, ptype)` referring to OS release, version number, CSD level (service pack) and OS type (multi/single processor). Values which cannot be determined are set to the defaults given as parameters (which all default to an empty string).

As a hint: *ptype* is `'Uniprocessor Free'` on single processor NT machines and `'Multiprocessor Free'` on multi processor machines. The `'Free'` refers to the OS version being free of debugging code. It could also state `'Checked'` which means the OS version uses debugging code, i.e. code that checks arguments, ranges, etc.
:::

:::: function
win32_edition()

Returns a string representing the current Windows edition, or `None` if the value cannot be determined. Possible values include but are not limited to `'Enterprise'`, `'IoTUAP'`, `'ServerStandard'`, and `'nanoserver'`.

::: versionadded
3.8
:::
::::

:::: function
win32_is_iot()

Return `True` if the Windows edition returned by `win32_edition`{.interpreted-text role="func"} is recognized as an IoT edition.

::: versionadded
3.8
:::
::::

## macOS platform

::: function
mac_ver(release=\'\', versioninfo=(\'\',\'\',\'\'), machine=\'\')

Get macOS version information and return it as tuple `(release, versioninfo, machine)` with *versioninfo* being a tuple `(version, dev_stage, non_release_version)`.

Entries which cannot be determined are set to `''`. All tuple entries are strings.
:::

## iOS platform

::: function
ios_ver(system=\'\', release=\'\', model=\'\', is_simulator=False)

Get iOS version information and return it as a `~collections.namedtuple`{.interpreted-text role="func"} with the following attributes:

- `system` is the OS name; either `'iOS'` or `'iPadOS'`.
- `release` is the iOS version number as a string (e.g., `'17.2'`).
- `model` is the device model identifier; this will be a string like `'iPhone13,2'` for a physical device, or `'iPhone'` on a simulator.
- `is_simulator` is a boolean describing if the app is running on a simulator or a physical device.

Entries which cannot be determined are set to the defaults given as parameters.
:::

## Unix platforms

::: function
libc_ver(executable=sys.executable, lib=\'\', version=\'\', chunksize=16384)

Tries to determine the libc version against which the file executable (defaults to the Python interpreter) is linked. Returns a tuple of strings `(lib, version)` which default to the given parameters in case the lookup fails.

Note that this function has intimate knowledge of how different libc versions add symbols to the executable is probably only usable for executables compiled using `gcc`{.interpreted-text role="program"}.

The file is read and scanned in chunks of *chunksize* bytes.
:::

## Linux platforms

:::: function
freedesktop_os_release()

Get operating system identification from `os-release` file and return it as a dict. The `os-release` file is a [freedesktop.org standard](https://www.freedesktop.org/software/systemd/man/os-release.html) and is available in most Linux distributions. A noticeable exception is Android and Android-based distributions.

Raises `OSError`{.interpreted-text role="exc"} or subclass when neither `/etc/os-release` nor `/usr/lib/os-release` can be read.

On success, the function returns a dictionary where keys and values are strings. Values have their special characters like `"` and `$` unquoted. The fields `NAME`, `ID`, and `PRETTY_NAME` are always defined according to the standard. All other fields are optional. Vendors may include additional fields.

Note that fields like `NAME`, `VERSION`, and `VARIANT` are strings suitable for presentation to users. Programs should use fields like `ID`, `ID_LIKE`, `VERSION_ID`, or `VARIANT_ID` to identify Linux distributions.

Example:

    def get_like_distro():
        info = platform.freedesktop_os_release()
        ids = [info["ID"]]
        if "ID_LIKE" in info:
            # ids are space separated and ordered by precedence
            ids.extend(info["ID_LIKE"].split())
        return ids

::: versionadded
3.10
:::
::::

## Android platform

:::: function
android_ver(release=\"\", api_level=0, manufacturer=\"\", model=\"\", device=\"\", is_emulator=False)

Get Android device information. Returns a `~collections.namedtuple`{.interpreted-text role="func"} with the following attributes. Values which cannot be determined are set to the defaults given as parameters.

- `release` - Android version, as a string (e.g. `"14"`).
- `api_level` - API level of the running device, as an integer (e.g. `34` for Android 14). To get the API level which Python was built against, see `sys.getandroidapilevel`{.interpreted-text role="func"}.
- `manufacturer` - [Manufacturer name](https://developer.android.com/reference/android/os/Build#MANUFACTURER).
- `model` - [Model name](https://developer.android.com/reference/android/os/Build#MODEL) -- typically the marketing name or model number.
- `device` - [Device name](https://developer.android.com/reference/android/os/Build#DEVICE) -- typically the model number or a codename.
- `is_emulator` - `True` if the device is an emulator; `False` if it\'s a physical device.

Google maintains a [list of known model and device names](https://storage.googleapis.com/play_public/supported_devices.html).

::: versionadded
3.13
:::
::::

## Command-line usage {#platform-cli}

`!platform`{.interpreted-text role="mod"} can also be invoked directly using the `-m`{.interpreted-text role="option"} switch of the interpreter:

    python -m platform [--terse] [--nonaliased] [{nonaliased,terse} ...]

The following options are accepted:

::: program
platform
:::

::: option

`--terse`

:   

Print terse information about the platform. This is equivalent to calling `platform.platform`{.interpreted-text role="func"} with the *terse* argument set to `True`.
:::

::: option

`--nonaliased`

:   

Print platform information without system/OS name aliasing. This is equivalent to calling `platform.platform`{.interpreted-text role="func"} with the *aliased* argument set to `True`.
:::

You can also pass one or more positional arguments (`terse`, `nonaliased`) to explicitly control the output format. These behave similarly to their corresponding options.
