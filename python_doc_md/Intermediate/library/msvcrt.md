# `!msvcrt`{.interpreted-text role="mod"} \-\-- Useful routines from the MS VC++ runtime

::: {.module synopsis="Miscellaneous useful routines from the MS VC++ runtime."}
msvcrt
:::

**Source code:** `PC/msvcrtmodule.c`{.interpreted-text role="source"}

------------------------------------------------------------------------

These functions provide access to some useful capabilities on Windows platforms. Some higher-level modules use these functions to build the Windows implementations of their services. For example, the `getpass`{.interpreted-text role="mod"} module uses this in the implementation of the `getpass`{.interpreted-text role="func"} function.

Further documentation on these functions can be found in the Platform API documentation.

The module implements both the normal and wide char variants of the console I/O api. The normal API deals only with ASCII characters and is of limited use for internationalized applications. The wide char API should be used where ever possible.

::: availability
Windows.
:::

::: versionchanged
3.3 Operations in this module now raise `OSError`{.interpreted-text role="exc"} where `IOError`{.interpreted-text role="exc"} was raised.
:::

## File Operations {#msvcrt-files}

:::: function
locking(fd, mode, nbytes)

Lock part of a file based on file descriptor *fd* from the C runtime. Raises `OSError`{.interpreted-text role="exc"} on failure. The locked region of the file extends from the current file position for *nbytes* bytes, and may continue beyond the end of the file. *mode* must be one of the `!LK_\*`{.interpreted-text role="const"} constants listed below. Multiple regions in a file may be locked at the same time, but may not overlap. Adjacent regions are not merged; they must be unlocked individually.

::: audit-event
msvcrt.locking fd,mode,nbytes msvcrt.locking
:::
::::

::: data
LK_LOCK LK_RLCK

Locks the specified bytes. If the bytes cannot be locked, the program immediately tries again after 1 second. If, after 10 attempts, the bytes cannot be locked, `OSError`{.interpreted-text role="exc"} is raised.
:::

::: data
LK_NBLCK LK_NBRLCK

Locks the specified bytes. If the bytes cannot be locked, `OSError`{.interpreted-text role="exc"} is raised.
:::

::: data
LK_UNLCK

Unlocks the specified bytes, which must have been previously locked.
:::

::: function
setmode(fd, flags)

Set the line-end translation mode for the file descriptor *fd*. To set it to text mode, *flags* should be `os.O_TEXT`{.interpreted-text role="const"}; for binary, it should be `os.O_BINARY`{.interpreted-text role="const"}.
:::

:::: function
open_osfhandle(handle, flags)

Create a C runtime file descriptor from the file handle *handle*. The *flags* parameter should be a bitwise OR of `os.O_APPEND`{.interpreted-text role="const"}, `os.O_RDONLY`{.interpreted-text role="const"}, `os.O_TEXT`{.interpreted-text role="const"} and `os.O_NOINHERIT`{.interpreted-text role="const"}. The returned file descriptor may be used as a parameter to `os.fdopen`{.interpreted-text role="func"} to create a file object.

The file descriptor is inheritable by default. Pass `os.O_NOINHERIT`{.interpreted-text role="const"} flag to make it non inheritable.

::: audit-event
msvcrt.open_osfhandle handle,flags msvcrt.open_osfhandle
:::
::::

:::: function
get_osfhandle(fd)

Return the file handle for the file descriptor *fd*. Raises `OSError`{.interpreted-text role="exc"} if *fd* is not recognized.

::: audit-event
msvcrt.get_osfhandle fd msvcrt.get_osfhandle
:::
::::

## Console I/O {#msvcrt-console}

::: function
kbhit()

Returns a nonzero value if a keypress is waiting to be read. Otherwise, return 0.
:::

::: function
getch()

Read a keypress and return the resulting character as a byte string. Nothing is echoed to the console. This call will block if a keypress is not already available, but will not wait for `Enter`{.interpreted-text role="kbd"} to be pressed. If the pressed key was a special function key, this will return `'\000'` or `'\xe0'`; the next call will return the keycode. The `Control-C`{.interpreted-text role="kbd"} keypress cannot be read with this function.
:::

::: function
getwch()

Wide char variant of `getch`{.interpreted-text role="func"}, returning a Unicode value.
:::

::: function
getche()

Similar to `getch`{.interpreted-text role="func"}, but the keypress will be echoed if it represents a printable character.
:::

::: function
getwche()

Wide char variant of `getche`{.interpreted-text role="func"}, returning a Unicode value.
:::

::: function
putch(char)

Print the byte string *char* to the console without buffering.
:::

::: function
putwch(unicode_char)

Wide char variant of `putch`{.interpreted-text role="func"}, accepting a Unicode value.
:::

::: function
ungetch(char)

Cause the byte string *char* to be \"pushed back\" into the console buffer; it will be the next character read by `getch`{.interpreted-text role="func"} or `getche`{.interpreted-text role="func"}.
:::

::: function
ungetwch(unicode_char)

Wide char variant of `ungetch`{.interpreted-text role="func"}, accepting a Unicode value.
:::

## Other Functions {#msvcrt-other}

::: function
heapmin()

Force the `malloc`{.interpreted-text role="c:func"} heap to clean itself up and return unused blocks to the operating system. On failure, this raises `OSError`{.interpreted-text role="exc"}.
:::

::: function
set_error_mode(mode)

Changes the location where the C runtime writes an error message for an error that might end the program. *mode* must be one of the `!OUT_\*`{.interpreted-text role="const"} constants listed below or `REPORT_ERRMODE`{.interpreted-text role="const"}. Returns the old setting or -1 if an error occurs. Only available in `debug build of Python <debug-build>`{.interpreted-text role="ref"}.
:::

::: data
OUT_TO_DEFAULT

Error sink is determined by the app\'s type. Only available in `debug build of Python <debug-build>`{.interpreted-text role="ref"}.
:::

::: data
OUT_TO_STDERR

Error sink is a standard error. Only available in `debug build of Python <debug-build>`{.interpreted-text role="ref"}.
:::

::: data
OUT_TO_MSGBOX

Error sink is a message box. Only available in `debug build of Python <debug-build>`{.interpreted-text role="ref"}.
:::

::: data
REPORT_ERRMODE

Report the current error mode value. Only available in `debug build of Python <debug-build>`{.interpreted-text role="ref"}.
:::

::: function
CrtSetReportMode(type, mode)

Specifies the destination or destinations for a specific report type generated by `!_CrtDbgReport`{.interpreted-text role="c:func"} in the MS VC++ runtime. *type* must be one of the `!CRT_\*`{.interpreted-text role="const"} constants listed below. *mode* must be one of the `!CRTDBG_\*`{.interpreted-text role="const"} constants listed below. Only available in `debug build of Python <debug-build>`{.interpreted-text role="ref"}.
:::

::: function
CrtSetReportFile(type, file)

After you use `CrtSetReportMode`{.interpreted-text role="func"} to specify `CRTDBG_MODE_FILE`{.interpreted-text role="const"}, you can specify the file handle to receive the message text. *type* must be one of the `!CRT_\*`{.interpreted-text role="const"} constants listed below. *file* should be the file handle your want specified. Only available in `debug build of Python <debug-build>`{.interpreted-text role="ref"}.
:::

::: data
CRT_WARN

Warnings, messages, and information that doesn\'t need immediate attention.
:::

::: data
CRT_ERROR

Errors, unrecoverable problems, and issues that require immediate attention.
:::

::: data
CRT_ASSERT

Assertion failures.
:::

::: data
CRTDBG_MODE_DEBUG

Writes the message to the debugger\'s output window.
:::

::: data
CRTDBG_MODE_FILE

Writes the message to a user-supplied file handle. `CrtSetReportFile`{.interpreted-text role="func"} should be called to define the specific file or stream to use as the destination.
:::

::: data
CRTDBG_MODE_WNDW

Creates a message box to display the message along with the `Abort`, `Retry`, and `Ignore` buttons.
:::

::: data
CRTDBG_REPORT_MODE

Returns current *mode* for the specified *type*.
:::

::: data
CRT_ASSEMBLY_VERSION

The CRT Assembly version, from the `crtassem.h`{.interpreted-text role="file"} header file.
:::

::: data
VC_ASSEMBLY_PUBLICKEYTOKEN

The VC Assembly public key token, from the `crtassem.h`{.interpreted-text role="file"} header file.
:::

::: data
LIBRARIES_ASSEMBLY_NAME_PREFIX

The Libraries Assembly name prefix, from the `crtassem.h`{.interpreted-text role="file"} header file.
:::
