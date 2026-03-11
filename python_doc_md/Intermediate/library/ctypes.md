# `!ctypes`{.interpreted-text role="mod"} \-\-- A foreign function library for Python

::: {.module synopsis="A foreign function library for Python."}
ctypes
:::

**Source code:** `Lib/ctypes`{.interpreted-text role="source"}

------------------------------------------------------------------------

`!ctypes`{.interpreted-text role="mod"} is a foreign function library for Python. It provides C compatible data types, and allows calling functions in DLLs or shared libraries. It can be used to wrap these libraries in pure Python.

This is an `optional module`{.interpreted-text role="term"}. If it is missing from your copy of CPython, look for documentation from your distributor (that is, whoever provided Python to you). If you are the distributor, see `optional-module-requirements`{.interpreted-text role="ref"}.

## ctypes tutorial {#ctypes-ctypes-tutorial}

Note: The code samples in this tutorial use `doctest`{.interpreted-text role="mod"} to make sure that they actually work. Since some code samples behave differently under Linux, Windows, or macOS, they contain doctest directives in comments.

Note: Some code samples reference the ctypes `c_int`{.interpreted-text role="class"} type. On platforms where `sizeof(long) == sizeof(int)` it is an alias to `c_long`{.interpreted-text role="class"}. So, you should not be confused if `c_long`{.interpreted-text role="class"} is printed if you would expect `c_int`{.interpreted-text role="class"} \-\-- they are actually the same type.

### Loading dynamic link libraries {#ctypes-loading-dynamic-link-libraries}

`!ctypes`{.interpreted-text role="mod"} exports the *cdll*, and on Windows *windll* and *oledll* objects, for loading dynamic link libraries.

You load libraries by accessing them as attributes of these objects. *cdll* loads libraries which export functions using the standard `cdecl` calling convention, while *windll* libraries call functions using the `stdcall` calling convention. *oledll* also uses the `stdcall` calling convention, and assumes the functions return a Windows `!HRESULT`{.interpreted-text role="c:type"} error code. The error code is used to automatically raise an `OSError`{.interpreted-text role="class"} exception when the function call fails.

::: versionchanged
3.3 Windows errors used to raise `WindowsError`{.interpreted-text role="exc"}, which is now an alias of `OSError`{.interpreted-text role="exc"}.
:::

Here are some examples for Windows. Note that `msvcrt` is the MS standard C library containing most standard C functions, and uses the `cdecl` calling convention:

    >>> from ctypes import *
    >>> print(windll.kernel32)  # doctest: +WINDOWS
    <WinDLL 'kernel32', handle ... at ...>
    >>> print(cdll.msvcrt)      # doctest: +WINDOWS
    <CDLL 'msvcrt', handle ... at ...>
    >>> libc = cdll.msvcrt      # doctest: +WINDOWS
    >>>

Windows appends the usual `.dll` file suffix automatically.

:::: note
::: title
Note
:::

Accessing the standard C library through `cdll.msvcrt` will use an outdated version of the library that may be incompatible with the one being used by Python. Where possible, use native Python functionality, or else import and use the `msvcrt` module.
::::

On Linux, it is required to specify the filename *including* the extension to load a library, so attribute access can not be used to load libraries. Either the `~LibraryLoader.LoadLibrary`{.interpreted-text role="meth"} method of the dll loaders should be used, or you should load the library by creating an instance of CDLL by calling the constructor:

    >>> cdll.LoadLibrary("libc.so.6")  # doctest: +LINUX
    <CDLL 'libc.so.6', handle ... at ...>
    >>> libc = CDLL("libc.so.6")       # doctest: +LINUX
    >>> libc                           # doctest: +LINUX
    <CDLL 'libc.so.6', handle ... at ...>
    >>>

### Accessing functions from loaded dlls {#ctypes-accessing-functions-from-loaded-dlls}

Functions are accessed as attributes of dll objects:

    >>> libc.printf
    <_FuncPtr object at 0x...>
    >>> print(windll.kernel32.GetModuleHandleA)  # doctest: +WINDOWS
    <_FuncPtr object at 0x...>
    >>> print(windll.kernel32.MyOwnFunction)     # doctest: +WINDOWS
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "ctypes.py", line 239, in __getattr__
        func = _StdcallFuncPtr(name, self)
    AttributeError: function 'MyOwnFunction' not found
    >>>

Note that win32 system dlls like `kernel32` and `user32` often export ANSI as well as UNICODE versions of a function. The UNICODE version is exported with a `W` appended to the name, while the ANSI version is exported with an `A` appended to the name. The win32 `GetModuleHandle` function, which returns a *module handle* for a given module name, has the following C prototype, and a macro is used to expose one of them as `GetModuleHandle` depending on whether UNICODE is defined or not:

    /* ANSI version */
    HMODULE GetModuleHandleA(LPCSTR lpModuleName);
    /* UNICODE version */
    HMODULE GetModuleHandleW(LPCWSTR lpModuleName);

*windll* does not try to select one of them by magic, you must access the version you need by specifying `GetModuleHandleA` or `GetModuleHandleW` explicitly, and then call it with bytes or string objects respectively.

Sometimes, dlls export functions with names which aren\'t valid Python identifiers, like `"??2@YAPAXI@Z"`. In this case you have to use `getattr`{.interpreted-text role="func"} to retrieve the function:

    >>> getattr(cdll.msvcrt, "??2@YAPAXI@Z")  # doctest: +WINDOWS
    <_FuncPtr object at 0x...>
    >>>

On Windows, some dlls export functions not by name but by ordinal. These functions can be accessed by indexing the dll object with the ordinal number:

    >>> cdll.kernel32[1]  # doctest: +WINDOWS
    <_FuncPtr object at 0x...>
    >>> cdll.kernel32[0]  # doctest: +WINDOWS
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "ctypes.py", line 310, in __getitem__
        func = _StdcallFuncPtr(name, self)
    AttributeError: function ordinal 0 not found
    >>>

### Calling functions {#ctypes-calling-functions}

You can call these functions like any other Python callable. This example uses the `rand()` function, which takes no arguments and returns a pseudo-random integer:

    >>> print(libc.rand())  # doctest: +SKIP
    1804289383

On Windows, you can call the `GetModuleHandleA()` function, which returns a win32 module handle (passing `None` as single argument to call it with a `NULL` pointer):

    >>> print(hex(windll.kernel32.GetModuleHandleA(None)))  # doctest: +WINDOWS
    0x1d000000
    >>>

`ValueError`{.interpreted-text role="exc"} is raised when you call an `stdcall` function with the `cdecl` calling convention, or vice versa:

    >>> cdll.kernel32.GetModuleHandleA(None)  # doctest: +WINDOWS
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: Procedure probably called with not enough arguments (4 bytes missing)
    >>>

    >>> windll.msvcrt.printf(b"spam")  # doctest: +WINDOWS
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: Procedure probably called with too many arguments (4 bytes in excess)
    >>>

To find out the correct calling convention you have to look into the C header file or the documentation for the function you want to call.

On Windows, `!ctypes`{.interpreted-text role="mod"} uses win32 structured exception handling to prevent crashes from general protection faults when functions are called with invalid argument values:

    >>> windll.kernel32.GetModuleHandleA(32)  # doctest: +WINDOWS
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    OSError: exception: access violation reading 0x00000020
    >>>

There are, however, enough ways to crash Python with `!ctypes`{.interpreted-text role="mod"}, so you should be careful anyway. The `faulthandler`{.interpreted-text role="mod"} module can be helpful in debugging crashes (e.g. from segmentation faults produced by erroneous C library calls).

`None`, integers, bytes objects and (unicode) strings are the only native Python objects that can directly be used as parameters in these function calls. `None` is passed as a C `NULL` pointer, bytes objects and strings are passed as pointer to the memory block that contains their data (`char *`{.interpreted-text role="c:expr"} or `wchar_t *`{.interpreted-text role="c:expr"}). Python integers are passed as the platform\'s default C `int`{.interpreted-text role="c:expr"} type, their value is masked to fit into the C type.

Before we move on calling functions with other parameter types, we have to learn more about `!ctypes`{.interpreted-text role="mod"} data types.

### Fundamental data types {#ctypes-fundamental-data-types}

`!ctypes`{.interpreted-text role="mod"} defines a number of primitive C compatible data types:

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  ctypes type                                      C type                                                                                                         Python type
  ------------------------------------------------ -------------------------------------------------------------------------------------------------------------- --------------------------
  `c_bool`{.interpreted-text role="class"}         `_Bool`{.interpreted-text role="c:expr"}                                                                       bool (1)

  `c_char`{.interpreted-text role="class"}         `char`{.interpreted-text role="c:expr"}                                                                        1-character bytes object

  `c_wchar`{.interpreted-text role="class"}        `wchar_t`{.interpreted-text role="c:type"}                                                                     1-character string

  `c_byte`{.interpreted-text role="class"}         `char`{.interpreted-text role="c:expr"}                                                                        int

  `c_ubyte`{.interpreted-text role="class"}        `unsigned char`{.interpreted-text role="c:expr"}                                                               int

  `c_short`{.interpreted-text role="class"}        `short`{.interpreted-text role="c:expr"}                                                                       int

  `c_ushort`{.interpreted-text role="class"}       `unsigned short`{.interpreted-text role="c:expr"}                                                              int

  `c_int`{.interpreted-text role="class"}          `int`{.interpreted-text role="c:expr"}                                                                         int

  `c_int8`{.interpreted-text role="class"}         `int8_t`{.interpreted-text role="c:type"}                                                                      int

  `c_int16`{.interpreted-text role="class"}        `int16_t`{.interpreted-text role="c:type"}                                                                     int

  `c_int32`{.interpreted-text role="class"}        `int32_t`{.interpreted-text role="c:type"}                                                                     int

  `c_int64`{.interpreted-text role="class"}        `int64_t`{.interpreted-text role="c:type"}                                                                     int

  `c_uint`{.interpreted-text role="class"}         `unsigned int`{.interpreted-text role="c:expr"}                                                                int

  `c_uint8`{.interpreted-text role="class"}        `uint8_t`{.interpreted-text role="c:type"}                                                                     int

  `c_uint16`{.interpreted-text role="class"}       `uint16_t`{.interpreted-text role="c:type"}                                                                    int

  `c_uint32`{.interpreted-text role="class"}       `uint32_t`{.interpreted-text role="c:type"}                                                                    int

  `c_uint64`{.interpreted-text role="class"}       `uint64_t`{.interpreted-text role="c:type"}                                                                    int

  `c_long`{.interpreted-text role="class"}         `long`{.interpreted-text role="c:expr"}                                                                        int

  `c_ulong`{.interpreted-text role="class"}        `unsigned long`{.interpreted-text role="c:expr"}                                                               int

  `c_longlong`{.interpreted-text role="class"}     `__int64`{.interpreted-text role="c:expr"} or `long long`{.interpreted-text role="c:expr"}                     int

  `c_ulonglong`{.interpreted-text role="class"}    `unsigned __int64`{.interpreted-text role="c:expr"} or `unsigned long long`{.interpreted-text role="c:expr"}   int

  `c_size_t`{.interpreted-text role="class"}       `size_t`{.interpreted-text role="c:type"}                                                                      int

  `c_ssize_t`{.interpreted-text role="class"}      `ssize_t`{.interpreted-text role="c:type"} or `Py_ssize_t`{.interpreted-text role="c:expr"}                    int

  `c_time_t`{.interpreted-text role="class"}       `time_t`{.interpreted-text role="c:type"}                                                                      int

  `c_float`{.interpreted-text role="class"}        `float`{.interpreted-text role="c:expr"}                                                                       float

  `c_double`{.interpreted-text role="class"}       `double`{.interpreted-text role="c:expr"}                                                                      float

  `c_longdouble`{.interpreted-text role="class"}   `long double`{.interpreted-text role="c:expr"}                                                                 float

  `c_char_p`{.interpreted-text role="class"}       `char *`{.interpreted-text role="c:expr"} (NUL terminated)                                                     bytes object or `None`

  `c_wchar_p`{.interpreted-text role="class"}      `wchar_t *`{.interpreted-text role="c:expr"} (NUL terminated)                                                  string or `None`

  `c_void_p`{.interpreted-text role="class"}       `void *`{.interpreted-text role="c:expr"}                                                                      int or `None`
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

\(1\)

:   The constructor accepts any object with a truth value.

Additionally, if IEC 60559 compatible complex arithmetic (Annex G) is supported in both C and `libffi`, the following complex types are available:

  --------------------------------------------------------------------------------------------------------------------------------
  ctypes type                                              C type                                                   Python type
  -------------------------------------------------------- -------------------------------------------------------- --------------
  `c_float_complex`{.interpreted-text role="class"}        `float complex`{.interpreted-text role="c:expr"}         complex

  `c_double_complex`{.interpreted-text role="class"}       `double complex`{.interpreted-text role="c:expr"}        complex

  `c_longdouble_complex`{.interpreted-text role="class"}   `long double complex`{.interpreted-text role="c:expr"}   complex
  --------------------------------------------------------------------------------------------------------------------------------

All these types can be created by calling them with an optional initializer of the correct type and value:

    >>> c_int()
    c_long(0)
    >>> c_wchar_p("Hello, World")
    c_wchar_p(140018365411392)
    >>> c_ushort(-3)
    c_ushort(65533)
    >>>

Since these types are mutable, their value can also be changed afterwards:

    >>> i = c_int(42)
    >>> print(i)
    c_long(42)
    >>> print(i.value)
    42
    >>> i.value = -99
    >>> print(i.value)
    -99
    >>>

Assigning a new value to instances of the pointer types `c_char_p`{.interpreted-text role="class"}, `c_wchar_p`{.interpreted-text role="class"}, and `c_void_p`{.interpreted-text role="class"} changes the *memory location* they point to, *not the contents* of the memory block (of course not, because Python string objects are immutable):

    >>> s = "Hello, World"
    >>> c_s = c_wchar_p(s)
    >>> print(c_s)
    c_wchar_p(139966785747344)
    >>> print(c_s.value)
    Hello World
    >>> c_s.value = "Hi, there"
    >>> print(c_s)              # the memory location has changed
    c_wchar_p(139966783348904)
    >>> print(c_s.value)
    Hi, there
    >>> print(s)                # first object is unchanged
    Hello, World
    >>>

You should be careful, however, not to pass them to functions expecting pointers to mutable memory. If you need mutable memory blocks, ctypes has a `create_string_buffer`{.interpreted-text role="func"} function which creates these in various ways. The current memory block contents can be accessed (or changed) with the `raw` property; if you want to access it as NUL terminated string, use the `value` property:

    >>> from ctypes import *
    >>> p = create_string_buffer(3)            # create a 3 byte buffer, initialized to NUL bytes
    >>> print(sizeof(p), repr(p.raw))
    3 b'\x00\x00\x00'
    >>> p = create_string_buffer(b"Hello")     # create a buffer containing a NUL terminated string
    >>> print(sizeof(p), repr(p.raw))
    6 b'Hello\x00'
    >>> print(repr(p.value))
    b'Hello'
    >>> p = create_string_buffer(b"Hello", 10) # create a 10 byte buffer
    >>> print(sizeof(p), repr(p.raw))
    10 b'Hello\x00\x00\x00\x00\x00'
    >>> p.value = b"Hi"
    >>> print(sizeof(p), repr(p.raw))
    10 b'Hi\x00lo\x00\x00\x00\x00\x00'
    >>>

The `create_string_buffer`{.interpreted-text role="func"} function replaces the old `!c_buffer`{.interpreted-text role="func"} function (which is still available as an alias). To create a mutable memory block containing unicode characters of the C type `wchar_t`{.interpreted-text role="c:type"}, use the `create_unicode_buffer`{.interpreted-text role="func"} function.

### Calling functions, continued {#ctypes-calling-functions-continued}

Note that printf prints to the real standard output channel, *not* to `sys.stdout`{.interpreted-text role="data"}, so these examples will only work at the console prompt, not from within *IDLE* or *PythonWin*:

    >>> printf = libc.printf
    >>> printf(b"Hello, %s\n", b"World!")
    Hello, World!
    14
    >>> printf(b"Hello, %S\n", "World!")
    Hello, World!
    14
    >>> printf(b"%d bottles of beer\n", 42)
    42 bottles of beer
    19
    >>> printf(b"%f bottles of beer\n", 42.5)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ctypes.ArgumentError: argument 2: TypeError: Don't know how to convert parameter 2
    >>>

As has been mentioned before, all Python types except integers, strings, and bytes objects have to be wrapped in their corresponding `!ctypes`{.interpreted-text role="mod"} type, so that they can be converted to the required C data type:

    >>> printf(b"An int %d, a double %f\n", 1234, c_double(3.14))
    An int 1234, a double 3.140000
    31
    >>>

### Calling variadic functions {#ctypes-calling-variadic-functions}

On a lot of platforms calling variadic functions through ctypes is exactly the same as calling functions with a fixed number of parameters. On some platforms, and in particular ARM64 for Apple Platforms, the calling convention for variadic functions is different than that for regular functions.

On those platforms it is required to specify the `~_CFuncPtr.argtypes`{.interpreted-text role="attr"} attribute for the regular, non-variadic, function arguments:

``` python3
libc.printf.argtypes = [ctypes.c_char_p]
```

Because specifying the attribute does not inhibit portability it is advised to always specify `~_CFuncPtr.argtypes`{.interpreted-text role="attr"} for all variadic functions.

### Calling functions with your own custom data types {#ctypes-calling-functions-with-own-custom-data-types}

You can also customize `!ctypes`{.interpreted-text role="mod"} argument conversion to allow instances of your own classes be used as function arguments. `!ctypes`{.interpreted-text role="mod"} looks for an `!_as_parameter_`{.interpreted-text role="attr"} attribute and uses this as the function argument. The attribute must be an integer, string, bytes, a `!ctypes`{.interpreted-text role="mod"} instance, or an object with an `!_as_parameter_`{.interpreted-text role="attr"} attribute:

    >>> class Bottles:
    ...     def __init__(self, number):
    ...         self._as_parameter_ = number
    ...
    >>> bottles = Bottles(42)
    >>> printf(b"%d bottles of beer\n", bottles)
    42 bottles of beer
    19
    >>>

If you don\'t want to store the instance\'s data in the `!_as_parameter_`{.interpreted-text role="attr"} instance variable, you could define a `property`{.interpreted-text role="class"} which makes the attribute available on request.

### Specifying the required argument types (function prototypes) {#ctypes-specifying-required-argument-types}

It is possible to specify the required argument types of functions exported from DLLs by setting the `~_CFuncPtr.argtypes`{.interpreted-text role="attr"} attribute.

`~_CFuncPtr.argtypes`{.interpreted-text role="attr"} must be a sequence of C data types (the `!printf`{.interpreted-text role="func"} function is probably not a good example here, because it takes a variable number and different types of parameters depending on the format string, on the other hand this is quite handy to experiment with this feature):

    >>> printf.argtypes = [c_char_p, c_char_p, c_int, c_double]
    >>> printf(b"String '%s', Int %d, Double %f\n", b"Hi", 10, 2.2)
    String 'Hi', Int 10, Double 2.200000
    37
    >>>

Specifying a format protects against incompatible argument types (just as a prototype for a C function), and tries to convert the arguments to valid types:

    >>> printf(b"%d %d %d", 1, 2, 3)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ctypes.ArgumentError: argument 2: TypeError: 'int' object cannot be interpreted as ctypes.c_char_p
    >>> printf(b"%s %d %f\n", b"X", 2, 3)
    X 2 3.000000
    13
    >>>

If you have defined your own classes which you pass to function calls, you have to implement a `~_CData.from_param`{.interpreted-text role="meth"} class method for them to be able to use them in the `~_CFuncPtr.argtypes`{.interpreted-text role="attr"} sequence. The `~_CData.from_param`{.interpreted-text role="meth"} class method receives the Python object passed to the function call, it should do a typecheck or whatever is needed to make sure this object is acceptable, and then return the object itself, its `!_as_parameter_`{.interpreted-text role="attr"} attribute, or whatever you want to pass as the C function argument in this case. Again, the result should be an integer, string, bytes, a `!ctypes`{.interpreted-text role="mod"} instance, or an object with an `!_as_parameter_`{.interpreted-text role="attr"} attribute.

### Return types {#ctypes-return-types}

::: testsetup
from ctypes import CDLL, c_char, c_char_p from ctypes.util import find_library libc = CDLL(find_library(\'c\')) strchr = libc.strchr
:::

By default functions are assumed to return the C `int`{.interpreted-text role="c:expr"} type. Other return types can be specified by setting the `~_CFuncPtr.restype`{.interpreted-text role="attr"} attribute of the function object.

The C prototype of `time`{.interpreted-text role="c:func"} is `time_t time(time_t *)`. Because `time_t`{.interpreted-text role="c:type"} might be of a different type than the default return type `int`{.interpreted-text role="c:expr"}, you should specify the `!restype`{.interpreted-text role="attr"} attribute:

    >>> libc.time.restype = c_time_t

The argument types can be specified using `~_CFuncPtr.argtypes`{.interpreted-text role="attr"}:

    >>> libc.time.argtypes = (POINTER(c_time_t),)

To call the function with a `NULL` pointer as first argument, use `None`:

    >>> print(libc.time(None))  # doctest: +SKIP
    1150640792

Here is a more advanced example, it uses the `!strchr`{.interpreted-text role="func"} function, which expects a string pointer and a char, and returns a pointer to a string:

    >>> strchr = libc.strchr
    >>> strchr(b"abcdef", ord("d"))  # doctest: +SKIP
    8059983
    >>> strchr.restype = c_char_p    # c_char_p is a pointer to a string
    >>> strchr(b"abcdef", ord("d"))
    b'def'
    >>> print(strchr(b"abcdef", ord("x")))
    None
    >>>

If you want to avoid the `ord("x") <ord>`{.interpreted-text role="func"} calls above, you can set the `~_CFuncPtr.argtypes`{.interpreted-text role="attr"} attribute, and the second argument will be converted from a single character Python bytes object into a C char:

::: doctest
\>\>\> strchr.restype = c_char_p \>\>\> strchr.argtypes = \[c_char_p, c_char\] \>\>\> strchr(b\"abcdef\", b\"d\") b\'def\' \>\>\> strchr(b\"abcdef\", b\"def\") Traceback (most recent call last): ctypes.ArgumentError: argument 2: TypeError: one character bytes, bytearray or integer expected \>\>\> print(strchr(b\"abcdef\", b\"x\")) None \>\>\> strchr(b\"abcdef\", b\"d\") b\'def\' \>\>\>
:::

You can also use a callable Python object (a function or a class for example) as the `~_CFuncPtr.restype`{.interpreted-text role="attr"} attribute, if the foreign function returns an integer. The callable will be called with the *integer* the C function returns, and the result of this call will be used as the result of your function call. This is useful to check for error return values and automatically raise an exception:

    >>> GetModuleHandle = windll.kernel32.GetModuleHandleA  # doctest: +WINDOWS
    >>> def ValidHandle(value):
    ...     if value == 0:
    ...         raise WinError()
    ...     return value
    ...
    >>>
    >>> GetModuleHandle.restype = ValidHandle  # doctest: +WINDOWS
    >>> GetModuleHandle(None)  # doctest: +WINDOWS
    486539264
    >>> GetModuleHandle("something silly")  # doctest: +WINDOWS
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 3, in ValidHandle
    OSError: [Errno 126] The specified module could not be found.
    >>>

`WinError` is a function which will call Windows `FormatMessage()` api to get the string representation of an error code, and *returns* an exception. `WinError` takes an optional error code parameter, if no one is used, it calls `GetLastError`{.interpreted-text role="func"} to retrieve it.

Please note that a much more powerful error checking mechanism is available through the `~_CFuncPtr.errcheck`{.interpreted-text role="attr"} attribute; see the reference manual for details.

### Passing pointers (or: passing parameters by reference) {#ctypes-passing-pointers}

Sometimes a C api function expects a *pointer* to a data type as parameter, probably to write into the corresponding location, or if the data is too large to be passed by value. This is also known as *passing parameters by reference*.

`!ctypes`{.interpreted-text role="mod"} exports the `byref`{.interpreted-text role="func"} function which is used to pass parameters by reference. The same effect can be achieved with the `pointer`{.interpreted-text role="func"} function, although `pointer`{.interpreted-text role="func"} does a lot more work since it constructs a real pointer object, so it is faster to use `byref`{.interpreted-text role="func"} if you don\'t need the pointer object in Python itself:

    >>> i = c_int()
    >>> f = c_float()
    >>> s = create_string_buffer(b'\000' * 32)
    >>> print(i.value, f.value, repr(s.value))
    0 0.0 b''
    >>> libc.sscanf(b"1 3.14 Hello", b"%d %f %s",
    ...             byref(i), byref(f), s)
    3
    >>> print(i.value, f.value, repr(s.value))
    1 3.1400001049 b'Hello'
    >>>

### Structures and unions {#ctypes-structures-unions}

Structures and unions must derive from the `Structure`{.interpreted-text role="class"} and `Union`{.interpreted-text role="class"} base classes which are defined in the `!ctypes`{.interpreted-text role="mod"} module. Each subclass must define a `~Structure._fields_`{.interpreted-text role="attr"} attribute. `!_fields_`{.interpreted-text role="attr"} must be a list of *2-tuples*, containing a *field name* and a *field type*.

The field type must be a `!ctypes`{.interpreted-text role="mod"} type like `c_int`{.interpreted-text role="class"}, or any other derived `!ctypes`{.interpreted-text role="mod"} type: structure, union, array, pointer.

Here is a simple example of a POINT structure, which contains two integers named *x* and *y*, and also shows how to initialize a structure in the constructor:

    >>> from ctypes import *
    >>> class POINT(Structure):
    ...     _fields_ = [("x", c_int),
    ...                 ("y", c_int)]
    ...
    >>> point = POINT(10, 20)
    >>> print(point.x, point.y)
    10 20
    >>> point = POINT(y=5)
    >>> print(point.x, point.y)
    0 5
    >>> POINT(1, 2, 3)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: too many initializers
    >>>

You can, however, build much more complicated structures. A structure can itself contain other structures by using a structure as a field type.

Here is a RECT structure which contains two POINTs named *upperleft* and *lowerright*:

    >>> class RECT(Structure):
    ...     _fields_ = [("upperleft", POINT),
    ...                 ("lowerright", POINT)]
    ...
    >>> rc = RECT(point)
    >>> print(rc.upperleft.x, rc.upperleft.y)
    0 5
    >>> print(rc.lowerright.x, rc.lowerright.y)
    0 0
    >>>

Nested structures can also be initialized in the constructor in several ways:

    >>> r = RECT(POINT(1, 2), POINT(3, 4))
    >>> r = RECT((1, 2), (3, 4))

Field `descriptor`{.interpreted-text role="term"}s can be retrieved from the *class*, they are useful for debugging because they can provide useful information. See `CField`{.interpreted-text role="class"}:

    >>> POINT.x
    <ctypes.CField 'x' type=c_int, ofs=0, size=4>
    >>> POINT.y
    <ctypes.CField 'y' type=c_int, ofs=4, size=4>
    >>>

::::: {#ctypes-structureunion-alignment-byte-order}
:::: warning
::: title
Warning
:::

`!ctypes`{.interpreted-text role="mod"} does not support passing unions or structures with bit-fields to functions by value. While this may work on 32-bit x86, it\'s not guaranteed by the library to work in the general case. Unions and structures with bit-fields should always be passed to functions by pointer.
::::
:::::

### Structure/union layout, alignment and byte order

By default, Structure and Union fields are laid out in the same way the C compiler does it. It is possible to override this behavior entirely by specifying a `~Structure._layout_`{.interpreted-text role="attr"} class attribute in the subclass definition; see the attribute documentation for details.

It is possible to specify the maximum alignment for the fields and/or for the structure itself by setting the class attributes `~Structure._pack_`{.interpreted-text role="attr"} and/or `~Structure._align_`{.interpreted-text role="attr"}, respectively. See the attribute documentation for details.

`!ctypes`{.interpreted-text role="mod"} uses the native byte order for Structures and Unions. To build structures with non-native byte order, you can use one of the `BigEndianStructure`{.interpreted-text role="class"}, `LittleEndianStructure`{.interpreted-text role="class"}, `BigEndianUnion`{.interpreted-text role="class"}, and `LittleEndianUnion`{.interpreted-text role="class"} base classes. These classes cannot contain pointer fields.

### Bit fields in structures and unions {#ctypes-bit-fields-in-structures-unions}

It is possible to create structures and unions containing bit fields. Bit fields are only possible for integer fields, the bit width is specified as the third item in the `~Structure._fields_`{.interpreted-text role="attr"} tuples:

    >>> class Int(Structure):
    ...     _fields_ = [("first_16", c_int, 16),
    ...                 ("second_16", c_int, 16)]
    ...
    >>> print(Int.first_16)
    <ctypes.CField 'first_16' type=c_int, ofs=0, bit_size=16, bit_offset=0>
    >>> print(Int.second_16)
    <ctypes.CField 'second_16' type=c_int, ofs=0, bit_size=16, bit_offset=16>

It is important to note that bit field allocation and layout in memory are not defined as a C standard; their implementation is compiler-specific. By default, Python will attempt to match the behavior of a \"native\" compiler for the current platform. See the `~Structure._layout_`{.interpreted-text role="attr"} attribute for details on the default behavior and how to change it.

### Arrays {#ctypes-arrays}

Arrays are sequences, containing a fixed number of instances of the same type.

The recommended way to create array types is by multiplying a data type with a positive integer:

    TenPointsArrayType = POINT * 10

Here is an example of a somewhat artificial data type, a structure containing 4 POINTs among other stuff:

    >>> from ctypes import *
    >>> class POINT(Structure):
    ...     _fields_ = ("x", c_int), ("y", c_int)
    ...
    >>> class MyStruct(Structure):
    ...     _fields_ = [("a", c_int),
    ...                 ("b", c_float),
    ...                 ("point_array", POINT * 4)]
    >>>
    >>> print(len(MyStruct().point_array))
    4
    >>>

Instances are created in the usual way, by calling the class:

    arr = TenPointsArrayType()
    for pt in arr:
        print(pt.x, pt.y)

The above code print a series of `0 0` lines, because the array contents is initialized to zeros.

Initializers of the correct type can also be specified:

    >>> from ctypes import *
    >>> TenIntegers = c_int * 10
    >>> ii = TenIntegers(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    >>> print(ii)
    <c_long_Array_10 object at 0x...>
    >>> for i in ii: print(i, end=" ")
    ...
    1 2 3 4 5 6 7 8 9 10
    >>>

### Pointers {#ctypes-pointers}

Pointer instances are created by calling the `pointer`{.interpreted-text role="func"} function on a `!ctypes`{.interpreted-text role="mod"} type:

    >>> from ctypes import *
    >>> i = c_int(42)
    >>> pi = pointer(i)
    >>>

Pointer instances have a `~_Pointer.contents`{.interpreted-text role="attr"} attribute which returns the object to which the pointer points, the `i` object above:

    >>> pi.contents
    c_long(42)
    >>>

Note that `!ctypes`{.interpreted-text role="mod"} does not have OOR (original object return), it constructs a new, equivalent object each time you retrieve an attribute:

    >>> pi.contents is i
    False
    >>> pi.contents is pi.contents
    False
    >>>

Assigning another `c_int`{.interpreted-text role="class"} instance to the pointer\'s contents attribute would cause the pointer to point to the memory location where this is stored:

    >>> i = c_int(99)
    >>> pi.contents = i
    >>> pi.contents
    c_long(99)
    >>>

Pointer instances can also be indexed with integers:

    >>> pi[0]
    99
    >>>

Assigning to an integer index changes the pointed to value:

    >>> print(i)
    c_long(99)
    >>> pi[0] = 22
    >>> print(i)
    c_long(22)
    >>>

It is also possible to use indexes different from 0, but you must know what you\'re doing, just as in C: You can access or change arbitrary memory locations. Generally you only use this feature if you receive a pointer from a C function, and you *know* that the pointer actually points to an array instead of a single item.

Behind the scenes, the `pointer`{.interpreted-text role="func"} function does more than simply create pointer instances, it has to create pointer *types* first. This is done with the `POINTER`{.interpreted-text role="func"} function, which accepts any `!ctypes`{.interpreted-text role="mod"} type, and returns a new type:

    >>> PI = POINTER(c_int)
    >>> PI
    <class 'ctypes.LP_c_long'>
    >>> PI(42)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: expected c_long instead of int
    >>> PI(c_int(42))
    <ctypes.LP_c_long object at 0x...>
    >>>

Calling the pointer type without an argument creates a `NULL` pointer. `NULL` pointers have a `False` boolean value:

    >>> null_ptr = POINTER(c_int)()
    >>> print(bool(null_ptr))
    False
    >>>

`!ctypes`{.interpreted-text role="mod"} checks for `NULL` when dereferencing pointers (but dereferencing invalid non-`NULL` pointers would crash Python):

    >>> null_ptr[0]
    Traceback (most recent call last):
        ....
    ValueError: NULL pointer access
    >>>

    >>> null_ptr[0] = 1234
    Traceback (most recent call last):
        ....
    ValueError: NULL pointer access
    >>>

### Thread safety without the GIL {#ctypes-thread-safety}

From Python 3.13 onward, the `GIL`{.interpreted-text role="term"} can be disabled on the `free-threaded build`{.interpreted-text role="term"}. In ctypes, reads and writes to a single object concurrently is safe, but not across multiple objects:

> ``` pycon
> >>> number = c_int(42)
> >>> pointer_a = pointer(number)
> >>> pointer_b = pointer(number)
> ```

In the above, it\'s only safe for one object to read and write to the address at once if the GIL is disabled. So, `pointer_a` can be shared and written to across multiple threads, but only if `pointer_b` is not also attempting to do the same. If this is an issue, consider using a `threading.Lock`{.interpreted-text role="class"} to synchronize access to memory:

> ``` pycon
> >>> import threading
> >>> lock = threading.Lock()
> >>> # Thread 1
> >>> with lock:
> ...    pointer_a.contents = 24
> >>> # Thread 2
> >>> with lock:
> ...    pointer_b.contents = 42
> ```

### Type conversions {#ctypes-type-conversions}

Usually, ctypes does strict type checking. This means, if you have `POINTER(c_int)` in the `~_CFuncPtr.argtypes`{.interpreted-text role="attr"} list of a function or as the type of a member field in a structure definition, only instances of exactly the same type are accepted. There are some exceptions to this rule, where ctypes accepts other objects. For example, you can pass compatible array instances instead of pointer types. So, for `POINTER(c_int)`, ctypes accepts an array of c_int:

    >>> class Bar(Structure):
    ...     _fields_ = [("count", c_int), ("values", POINTER(c_int))]
    ...
    >>> bar = Bar()
    >>> bar.values = (c_int * 3)(1, 2, 3)
    >>> bar.count = 3
    >>> for i in range(bar.count):
    ...     print(bar.values[i])
    ...
    1
    2
    3
    >>>

In addition, if a function argument is explicitly declared to be a pointer type (such as `POINTER(c_int)`) in `~_CFuncPtr.argtypes`{.interpreted-text role="attr"}, an object of the pointed type (`c_int` in this case) can be passed to the function. ctypes will apply the required `byref`{.interpreted-text role="func"} conversion in this case automatically.

To set a POINTER type field to `NULL`, you can assign `None`:

    >>> bar.values = None
    >>>

Sometimes you have instances of incompatible types. In C, you can cast one type into another type. `!ctypes`{.interpreted-text role="mod"} provides a `cast`{.interpreted-text role="func"} function which can be used in the same way. The `Bar` structure defined above accepts `POINTER(c_int)` pointers or `c_int`{.interpreted-text role="class"} arrays for its `values` field, but not instances of other types:

    >>> bar.values = (c_byte * 4)()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: incompatible types, c_byte_Array_4 instance instead of LP_c_long instance
    >>>

For these cases, the `cast`{.interpreted-text role="func"} function is handy.

The `cast`{.interpreted-text role="func"} function can be used to cast a ctypes instance into a pointer to a different ctypes data type. `cast`{.interpreted-text role="func"} takes two parameters, a ctypes object that is or can be converted to a pointer of some kind, and a ctypes pointer type. It returns an instance of the second argument, which references the same memory block as the first argument:

    >>> a = (c_byte * 4)()
    >>> cast(a, POINTER(c_int))
    <ctypes.LP_c_long object at ...>
    >>>

So, `cast`{.interpreted-text role="func"} can be used to assign to the `values` field of `Bar` the structure:

    >>> bar = Bar()
    >>> bar.values = cast((c_byte * 4)(), POINTER(c_int))
    >>> print(bar.values[0])
    0
    >>>

### Incomplete Types {#ctypes-incomplete-types}

*Incomplete Types* are structures, unions or arrays whose members are not yet specified. In C, they are specified by forward declarations, which are defined later:

    struct cell; /* forward declaration */

    struct cell {
        char *name;
        struct cell *next;
    };

The straightforward translation into ctypes code would be this, but it does not work:

    >>> class cell(Structure):
    ...     _fields_ = [("name", c_char_p),
    ...                 ("next", POINTER(cell))]
    ...
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 2, in cell
    NameError: name 'cell' is not defined
    >>>

because the new `class cell` is not available in the class statement itself. In `!ctypes`{.interpreted-text role="mod"}, we can define the `cell` class and set the `~Structure._fields_`{.interpreted-text role="attr"} attribute later, after the class statement:

    >>> from ctypes import *
    >>> class cell(Structure):
    ...     pass
    ...
    >>> cell._fields_ = [("name", c_char_p),
    ...                  ("next", POINTER(cell))]
    >>>

Let\'s try it. We create two instances of `cell`, and let them point to each other, and finally follow the pointer chain a few times:

    >>> c1 = cell()
    >>> c1.name = b"foo"
    >>> c2 = cell()
    >>> c2.name = b"bar"
    >>> c1.next = pointer(c2)
    >>> c2.next = pointer(c1)
    >>> p = c1
    >>> for i in range(8):
    ...     print(p.name, end=" ")
    ...     p = p.next[0]
    ...
    foo bar foo bar foo bar foo bar
    >>>

### Callback functions {#ctypes-callback-functions}

`!ctypes`{.interpreted-text role="mod"} allows creating C callable function pointers from Python callables. These are sometimes called *callback functions*.

First, you must create a class for the callback function. The class knows the calling convention, the return type, and the number and types of arguments this function will receive.

The `CFUNCTYPE`{.interpreted-text role="func"} factory function creates types for callback functions using the `cdecl` calling convention. On Windows, the `WINFUNCTYPE`{.interpreted-text role="func"} factory function creates types for callback functions using the `stdcall` calling convention.

Both of these factory functions are called with the result type as first argument, and the callback functions expected argument types as the remaining arguments.

I will present an example here which uses the standard C library\'s `!qsort`{.interpreted-text role="c:func"} function, that is used to sort items with the help of a callback function. `!qsort`{.interpreted-text role="c:func"} will be used to sort an array of integers:

    >>> IntArray5 = c_int * 5
    >>> ia = IntArray5(5, 1, 7, 33, 99)
    >>> qsort = libc.qsort
    >>> qsort.restype = None
    >>>

`!qsort`{.interpreted-text role="func"} must be called with a pointer to the data to sort, the number of items in the data array, the size of one item, and a pointer to the comparison function, the callback. The callback will then be called with two pointers to items, and it must return a negative integer if the first item is smaller than the second, a zero if they are equal, and a positive integer otherwise.

So our callback function receives pointers to integers, and must return an integer. First we create the `type` for the callback function:

    >>> CMPFUNC = CFUNCTYPE(c_int, POINTER(c_int), POINTER(c_int))
    >>>

To get started, here is a simple callback that shows the values it gets passed:

    >>> def py_cmp_func(a, b):
    ...     print("py_cmp_func", a[0], b[0])
    ...     return 0
    ...
    >>> cmp_func = CMPFUNC(py_cmp_func)
    >>>

The result:

    >>> qsort(ia, len(ia), sizeof(c_int), cmp_func)  # doctest: +LINUX
    py_cmp_func 5 1
    py_cmp_func 33 99
    py_cmp_func 7 33
    py_cmp_func 5 7
    py_cmp_func 1 7
    >>>

Now we can actually compare the two items and return a useful result:

    >>> def py_cmp_func(a, b):
    ...     print("py_cmp_func", a[0], b[0])
    ...     return a[0] - b[0]
    ...
    >>>
    >>> qsort(ia, len(ia), sizeof(c_int), CMPFUNC(py_cmp_func)) # doctest: +LINUX
    py_cmp_func 5 1
    py_cmp_func 33 99
    py_cmp_func 7 33
    py_cmp_func 1 7
    py_cmp_func 5 7
    >>>

As we can easily check, our array is sorted now:

    >>> for i in ia: print(i, end=" ")
    ...
    1 5 7 33 99
    >>>

The function factories can be used as decorator factories, so we may as well write:

    >>> @CFUNCTYPE(c_int, POINTER(c_int), POINTER(c_int))
    ... def py_cmp_func(a, b):
    ...     print("py_cmp_func", a[0], b[0])
    ...     return a[0] - b[0]
    ...
    >>> qsort(ia, len(ia), sizeof(c_int), py_cmp_func)
    py_cmp_func 5 1
    py_cmp_func 33 99
    py_cmp_func 7 33
    py_cmp_func 1 7
    py_cmp_func 5 7
    >>>

:::: note
::: title
Note
:::

Make sure you keep references to `CFUNCTYPE`{.interpreted-text role="func"} objects as long as they are used from C code. `!ctypes`{.interpreted-text role="mod"} doesn\'t, and if you don\'t, they may be garbage collected, crashing your program when a callback is made.

Also, note that if the callback function is called in a thread created outside of Python\'s control (e.g. by the foreign code that calls the callback), ctypes creates a new dummy Python thread on every invocation. This behavior is correct for most purposes, but it means that values stored with `threading.local`{.interpreted-text role="class"} will *not* survive across different callbacks, even when those calls are made from the same C thread.
::::

### Accessing values exported from dlls {#ctypes-accessing-values-exported-from-dlls}

Some shared libraries not only export functions, they also export variables. An example in the Python library itself is the `Py_Version`{.interpreted-text role="c:data"}, Python runtime version number encoded in a single constant integer.

`!ctypes`{.interpreted-text role="mod"} can access values like this with the `~_CData.in_dll`{.interpreted-text role="meth"} class methods of the type. *pythonapi* is a predefined symbol giving access to the Python C api:

    >>> version = ctypes.c_int.in_dll(ctypes.pythonapi, "Py_Version")
    >>> print(hex(version.value))
    0x30c00a0

An extended example which also demonstrates the use of pointers accesses the `PyImport_FrozenModules`{.interpreted-text role="c:data"} pointer exported by Python.

Quoting the docs for that value:

> This pointer is initialized to point to an array of `_frozen`{.interpreted-text role="c:struct"} records, terminated by one whose members are all `NULL` or zero. When a frozen module is imported, it is searched in this table. Third-party code could play tricks with this to provide a dynamically created collection of frozen modules.

So manipulating this pointer could even prove useful. To restrict the example size, we show only how this table can be read with `!ctypes`{.interpreted-text role="mod"}:

    >>> from ctypes import *
    >>>
    >>> class struct_frozen(Structure):
    ...     _fields_ = [("name", c_char_p),
    ...                 ("code", POINTER(c_ubyte)),
    ...                 ("size", c_int),
    ...                 ("get_code", POINTER(c_ubyte)),  # Function pointer
    ...                ]
    ...
    >>>

We have defined the `_frozen`{.interpreted-text role="c:struct"} data type, so we can get the pointer to the table:

    >>> FrozenTable = POINTER(struct_frozen)
    >>> table = FrozenTable.in_dll(pythonapi, "_PyImport_FrozenBootstrap")
    >>>

Since `table` is a `pointer` to the array of `struct_frozen` records, we can iterate over it, but we just have to make sure that our loop terminates, because pointers have no size. Sooner or later it would probably crash with an access violation or whatever, so it\'s better to break out of the loop when we hit the `NULL` entry:

    >>> for item in table:
    ...     if item.name is None:
    ...         break
    ...     print(item.name.decode("ascii"), item.size)
    ...
    _frozen_importlib 31764
    _frozen_importlib_external 41499
    zipimport 12345
    >>>

The fact that standard Python has a frozen module and a frozen package (indicated by the negative `size` member) is not well known, it is only used for testing. Try it out with `import __hello__` for example.

### Surprises {#ctypes-surprises}

There are some edges in `!ctypes`{.interpreted-text role="mod"} where you might expect something other than what actually happens.

Consider the following example:

    >>> from ctypes import *
    >>> class POINT(Structure):
    ...     _fields_ = ("x", c_int), ("y", c_int)
    ...
    >>> class RECT(Structure):
    ...     _fields_ = ("a", POINT), ("b", POINT)
    ...
    >>> p1 = POINT(1, 2)
    >>> p2 = POINT(3, 4)
    >>> rc = RECT(p1, p2)
    >>> print(rc.a.x, rc.a.y, rc.b.x, rc.b.y)
    1 2 3 4
    >>> # now swap the two points
    >>> rc.a, rc.b = rc.b, rc.a
    >>> print(rc.a.x, rc.a.y, rc.b.x, rc.b.y)
    3 4 3 4
    >>>

Hm. We certainly expected the last statement to print `3 4 1 2`. What happened? Here are the steps of the `rc.a, rc.b = rc.b, rc.a` line above:

    >>> temp0, temp1 = rc.b, rc.a
    >>> rc.a = temp0
    >>> rc.b = temp1
    >>>

Note that `temp0` and `temp1` are objects still using the internal buffer of the `rc` object above. So executing `rc.a = temp0` copies the buffer contents of `temp0` into `rc` \'s buffer. This, in turn, changes the contents of `temp1`. So, the last assignment `rc.b = temp1`, doesn\'t have the expected effect.

Keep in mind that retrieving sub-objects from Structure, Unions, and Arrays doesn\'t *copy* the sub-object, instead it retrieves a wrapper object accessing the root-object\'s underlying buffer.

Another example that may behave differently from what one would expect is this:

    >>> s = c_char_p()
    >>> s.value = b"abc def ghi"
    >>> s.value
    b'abc def ghi'
    >>> s.value is s.value
    False
    >>>

:::: note
::: title
Note
:::

Objects instantiated from `c_char_p`{.interpreted-text role="class"} can only have their value set to bytes or integers.
::::

Why is it printing `False`? ctypes instances are objects containing a memory block plus some `descriptor`{.interpreted-text role="term"}s accessing the contents of the memory. Storing a Python object in the memory block does not store the object itself, instead the `contents` of the object is stored. Accessing the contents again constructs a new Python object each time!

### Variable-sized data types {#ctypes-variable-sized-data-types}

`!ctypes`{.interpreted-text role="mod"} provides some support for variable-sized arrays and structures.

The `resize`{.interpreted-text role="func"} function can be used to resize the memory buffer of an existing ctypes object. The function takes the object as first argument, and the requested size in bytes as the second argument. The memory block cannot be made smaller than the natural memory block specified by the objects type, a `ValueError`{.interpreted-text role="exc"} is raised if this is tried:

    >>> short_array = (c_short * 4)()
    >>> print(sizeof(short_array))
    8
    >>> resize(short_array, 4)
    Traceback (most recent call last):
        ...
    ValueError: minimum size is 8
    >>> resize(short_array, 32)
    >>> sizeof(short_array)
    32
    >>> sizeof(type(short_array))
    8
    >>>

This is nice and fine, but how would one access the additional elements contained in this array? Since the type still only knows about 4 elements, we get errors accessing other elements:

    >>> short_array[:]
    [0, 0, 0, 0]
    >>> short_array[7]
    Traceback (most recent call last):
        ...
    IndexError: invalid index
    >>>

Another way to use variable-sized data types with `!ctypes`{.interpreted-text role="mod"} is to use the dynamic nature of Python, and (re-)define the data type after the required size is already known, on a case by case basis.

## ctypes reference {#ctypes-ctypes-reference}

### Finding shared libraries {#ctypes-finding-shared-libraries}

When programming in a compiled language, shared libraries are accessed when compiling/linking a program, and when the program is run.

The purpose of the `~ctypes.util.find_library`{.interpreted-text role="func"} function is to locate a library in a way similar to what the compiler or runtime loader does (on platforms with several versions of a shared library the most recent should be loaded), while the ctypes library loaders act like when a program is run, and call the runtime loader directly.

The `!ctypes.util`{.interpreted-text role="mod"} module provides a function which can help to determine the library to load.

::: {.data module="ctypes.util" noindex=""}
find_library(name)

Try to find a library and return a pathname. *name* is the library name without any prefix like *lib*, suffix like `.so`, `.dylib` or version number (this is the form used for the posix linker option `!-l`{.interpreted-text role="option"}). If no library can be found, returns `None`.
:::

The exact functionality is system dependent.

On Linux, `~ctypes.util.find_library`{.interpreted-text role="func"} tries to run external programs (`/sbin/ldconfig`, `gcc`, `objdump` and `ld`) to find the library file. It returns the filename of the library file.

Note that if the output of these programs does not correspond to the dynamic linker used by Python, the result of this function may be misleading.

::: versionchanged
3.6 On Linux, the value of the environment variable `LD_LIBRARY_PATH` is used when searching for libraries, if a library cannot be found by any other means.
:::

Here are some examples:

    >>> from ctypes.util import find_library
    >>> find_library("m")
    'libm.so.6'
    >>> find_library("c")
    'libc.so.6'
    >>> find_library("bz2")
    'libbz2.so.1.0'
    >>>

On macOS and Android, `~ctypes.util.find_library`{.interpreted-text role="func"} uses the system\'s standard naming schemes and paths to locate the library, and returns a full pathname if successful:

    >>> from ctypes.util import find_library
    >>> find_library("c")
    '/usr/lib/libc.dylib'
    >>> find_library("m")
    '/usr/lib/libm.dylib'
    >>> find_library("bz2")
    '/usr/lib/libbz2.dylib'
    >>> find_library("AGL")
    '/System/Library/Frameworks/AGL.framework/AGL'
    >>>

On Windows, `~ctypes.util.find_library`{.interpreted-text role="func"} searches along the system search path, and returns the full pathname, but since there is no predefined naming scheme a call like `find_library("c")` will fail and return `None`.

If wrapping a shared library with `!ctypes`{.interpreted-text role="mod"}, it *may* be better to determine the shared library name at development time, and hardcode that into the wrapper module instead of using `~ctypes.util.find_library`{.interpreted-text role="func"} to locate the library at runtime.

### Listing loaded shared libraries {#ctypes-listing-loaded-shared-libraries}

When writing code that relies on code loaded from shared libraries, it can be useful to know which shared libraries have already been loaded into the current process.

The `!ctypes.util`{.interpreted-text role="mod"} module provides the `~ctypes.util.dllist`{.interpreted-text role="func"} function, which calls the different APIs provided by the various platforms to help determine which shared libraries have already been loaded into the current process.

The exact output of this function will be system dependent. On most platforms, the first entry of this list represents the current process itself, which may be an empty string. For example, on glibc-based Linux, the return may look like:

    >>> from ctypes.util import dllist
    >>> dllist()
    ['', 'linux-vdso.so.1', '/lib/x86_64-linux-gnu/libm.so.6', '/lib/x86_64-linux-gnu/libc.so.6', ... ]

### Loading shared libraries {#ctypes-loading-shared-libraries}

There are several ways to load shared libraries into the Python process. One way is to instantiate one of the following classes:

:::: {.CDLL(name, .mode=DEFAULT_MODE, .handle=None, .use_errno=False, .use_last_error=False, .winmode=None)}
Instances of this class represent loaded shared libraries. Functions in these libraries use the standard C calling convention, and are assumed to return `int`{.interpreted-text role="c:expr"}.

On Windows creating a `CDLL`{.interpreted-text role="class"} instance may fail even if the DLL name exists. When a dependent DLL of the loaded DLL is not found, a `OSError`{.interpreted-text role="exc"} error is raised with the message *\"\[WinError 126\] The specified module could not be found\".* This error message does not contain the name of the missing DLL because the Windows API does not return this information making this error hard to diagnose. To resolve this error and determine which DLL is not found, you need to find the list of dependent DLLs and determine which one is not found using Windows debugging and tracing tools.

::: versionchanged
3.12

The *name* parameter can now be a `path-like object`{.interpreted-text role="term"}.
:::
::::

::: seealso
[Microsoft DUMPBIN tool](https://docs.microsoft.com/cpp/build/reference/dependents) \-- A tool to find DLL dependents.
:::

:::::: {.OleDLL(name, .mode=DEFAULT_MODE, .handle=None, .use_errno=False, .use_last_error=False, .winmode=None)}
Instances of this class represent loaded shared libraries, functions in these libraries use the `stdcall` calling convention, and are assumed to return the windows specific `HRESULT`{.interpreted-text role="class"} code. `HRESULT`{.interpreted-text role="class"} values contain information specifying whether the function call failed or succeeded, together with additional error code. If the return value signals a failure, an `OSError`{.interpreted-text role="class"} is automatically raised.

::: availability
Windows
:::

::: versionchanged
3.3 `WindowsError`{.interpreted-text role="exc"} used to be raised, which is now an alias of `OSError`{.interpreted-text role="exc"}.
:::

::: versionchanged
3.12

The *name* parameter can now be a `path-like object`{.interpreted-text role="term"}.
:::
::::::

::::: {.WinDLL(name, .mode=DEFAULT_MODE, .handle=None, .use_errno=False, .use_last_error=False, .winmode=None)}
Instances of this class represent loaded shared libraries, functions in these libraries use the `stdcall` calling convention, and are assumed to return `int`{.interpreted-text role="c:expr"} by default.

::: availability
Windows
:::

::: versionchanged
3.12

The *name* parameter can now be a `path-like object`{.interpreted-text role="term"}.
:::
:::::

The Python `global interpreter lock`{.interpreted-text role="term"} is released before calling any function exported by these libraries, and reacquired afterwards.

:::: {.PyDLL(name, .mode=DEFAULT_MODE, .handle=None)}
Instances of this class behave like `CDLL`{.interpreted-text role="class"} instances, except that the Python GIL is *not* released during the function call, and after the function execution the Python error flag is checked. If the error flag is set, a Python exception is raised.

Thus, this is only useful to call Python C api functions directly.

::: versionchanged
3.12

The *name* parameter can now be a `path-like object`{.interpreted-text role="term"}.
:::
::::

All these classes can be instantiated by calling them with at least one argument, the pathname of the shared library. If you have an existing handle to an already loaded shared library, it can be passed as the `handle` named parameter, otherwise the underlying platform\'s `!dlopen`{.interpreted-text role="c:func"} or `!LoadLibrary`{.interpreted-text role="c:func"} function is used to load the library into the process, and to get a handle to it.

The *mode* parameter can be used to specify how the library is loaded. For details, consult the `dlopen(3)`{.interpreted-text role="manpage"} manpage. On Windows, *mode* is ignored. On posix systems, RTLD_NOW is always added, and is not configurable.

The *use_errno* parameter, when set to true, enables a ctypes mechanism that allows accessing the system `errno`{.interpreted-text role="data"} error number in a safe way. `!ctypes`{.interpreted-text role="mod"} maintains a thread-local copy of the system\'s `errno`{.interpreted-text role="data"} variable; if you call foreign functions created with `use_errno=True` then the `errno`{.interpreted-text role="data"} value before the function call is swapped with the ctypes private copy, the same happens immediately after the function call.

The function `ctypes.get_errno`{.interpreted-text role="func"} returns the value of the ctypes private copy, and the function `ctypes.set_errno`{.interpreted-text role="func"} changes the ctypes private copy to a new value and returns the former value.

The *use_last_error* parameter, when set to true, enables the same mechanism for the Windows error code which is managed by the `GetLastError`{.interpreted-text role="func"} and `!SetLastError`{.interpreted-text role="func"} Windows API functions; `ctypes.get_last_error`{.interpreted-text role="func"} and `ctypes.set_last_error`{.interpreted-text role="func"} are used to request and change the ctypes private copy of the windows error code.

The *winmode* parameter is used on Windows to specify how the library is loaded (since *mode* is ignored). It takes any value that is valid for the Win32 API `LoadLibraryEx` flags parameter. When omitted, the default is to use the flags that result in the most secure DLL load, which avoids issues such as DLL hijacking. Passing the full path to the DLL is the safest way to ensure the correct library and dependencies are loaded.

::: versionchanged
3.8 Added *winmode* parameter.
:::

::: {.data noindex=""}
RTLD_GLOBAL

Flag to use as *mode* parameter. On platforms where this flag is not available, it is defined as the integer zero.
:::

::: {.data noindex=""}
RTLD_LOCAL

Flag to use as *mode* parameter. On platforms where this is not available, it is the same as *RTLD_GLOBAL*.
:::

::: {.data noindex=""}
DEFAULT_MODE

The default mode which is used to load shared libraries. On OSX 10.3, this is *RTLD_GLOBAL*, otherwise it is the same as *RTLD_LOCAL*.
:::

Instances of these classes have no public methods. Functions exported by the shared library can be accessed as attributes or by index. Please note that accessing the function through an attribute caches the result and therefore accessing it repeatedly returns the same object each time. On the other hand, accessing it through an index returns a new object each time:

    >>> from ctypes import CDLL
    >>> libc = CDLL("libc.so.6")  # On Linux
    >>> libc.time == libc.time
    True
    >>> libc['time'] == libc['time']
    False

The following public attributes are available, their name starts with an underscore to not clash with exported function names:

::: attribute
PyDLL.\_handle

The system handle used to access the library.
:::

::: attribute
PyDLL.\_name

The name of the library passed in the constructor.
:::

Shared libraries can also be loaded by using one of the prefabricated objects, which are instances of the `LibraryLoader`{.interpreted-text role="class"} class, either by calling the `~LibraryLoader.LoadLibrary`{.interpreted-text role="meth"} method, or by retrieving the library as attribute of the loader instance.

:::: LibraryLoader(dlltype)
Class which loads shared libraries. *dlltype* should be one of the `CDLL`{.interpreted-text role="class"}, `PyDLL`{.interpreted-text role="class"}, `WinDLL`{.interpreted-text role="class"}, or `OleDLL`{.interpreted-text role="class"} types.

`!__getattr__`{.interpreted-text role="meth"} has special behavior: It allows loading a shared library by accessing it as attribute of a library loader instance. The result is cached, so repeated attribute accesses return the same library each time.

::: method
LoadLibrary(name)

Load a shared library into the process and return it. This method always returns a new instance of the library.
:::
::::

These prefabricated library loaders are available:

::: {.data noindex=""}
cdll

Creates `CDLL`{.interpreted-text role="class"} instances.
:::

:::: {.data noindex=""}
windll

Creates `WinDLL`{.interpreted-text role="class"} instances.

::: availability
Windows
:::
::::

:::: {.data noindex=""}
oledll

Creates `OleDLL`{.interpreted-text role="class"} instances.

::: availability
Windows
:::
::::

::: {.data noindex=""}
pydll

Creates `PyDLL`{.interpreted-text role="class"} instances.
:::

For accessing the C Python api directly, a ready-to-use Python shared library object is available:

::: {.data noindex=""}
pythonapi

An instance of `PyDLL`{.interpreted-text role="class"} that exposes Python C API functions as attributes. Note that all these functions are assumed to return C `int`{.interpreted-text role="c:expr"}, which is of course not always the truth, so you have to assign the correct `!restype`{.interpreted-text role="attr"} attribute to use these functions.
:::

::: audit-event
ctypes.dlopen name ctypes.LibraryLoader

Loading a library through any of these objects raises an `auditing event <auditing>`{.interpreted-text role="ref"} `ctypes.dlopen` with string argument `name`, the name used to load the library.
:::

::: audit-event
ctypes.dlsym library,name ctypes.LibraryLoader

Accessing a function on a loaded library raises an auditing event `ctypes.dlsym` with arguments `library` (the library object) and `name` (the symbol\'s name as a string or integer).
:::

::: audit-event
ctypes.dlsym/handle handle,name ctypes.LibraryLoader

In cases when only the library handle is available rather than the object, accessing a function raises an auditing event `ctypes.dlsym/handle` with arguments `handle` (the raw library handle) and `name`.
:::

### Foreign functions {#ctypes-foreign-functions}

As explained in the previous section, foreign functions can be accessed as attributes of loaded shared libraries. The function objects created in this way by default accept any number of arguments, accept any ctypes data instances as arguments, and return the default result type specified by the library loader.

They are instances of a private local class `!_FuncPtr`{.interpreted-text role="class"} (not exposed in `!ctypes`{.interpreted-text role="mod"}) which inherits from the private `_CFuncPtr`{.interpreted-text role="class"} class:

::: doctest
\>\>\> import ctypes \>\>\> lib = ctypes.CDLL(None) \>\>\> issubclass(lib.\_FuncPtr, ctypes.\_CFuncPtr) True \>\>\> lib.\_FuncPtr is ctypes.\_CFuncPtr False
:::

::::::: _CFuncPtr
Base class for C callable foreign functions.

Instances of foreign functions are also C compatible data types; they represent C function pointers.

This behavior can be customized by assigning to special attributes of the foreign function object.

::: attribute
restype

Assign a ctypes type to specify the result type of the foreign function. Use `None` for `void`{.interpreted-text role="c:expr"}, a function not returning anything.

It is possible to assign a callable Python object that is not a ctypes type, in this case the function is assumed to return a C `int`{.interpreted-text role="c:expr"}, and the callable will be called with this integer, allowing further processing or error checking. Using this is deprecated, for more flexible post processing or error checking use a ctypes data type as `!restype`{.interpreted-text role="attr"} and assign a callable to the `errcheck`{.interpreted-text role="attr"} attribute.
:::

::: attribute
argtypes

Assign a tuple of ctypes types to specify the argument types that the function accepts. Functions using the `stdcall` calling convention can only be called with the same number of arguments as the length of this tuple; functions using the C calling convention accept additional, unspecified arguments as well.

When a foreign function is called, each actual argument is passed to the `~_CData.from_param`{.interpreted-text role="meth"} class method of the items in the `argtypes`{.interpreted-text role="attr"} tuple, this method allows adapting the actual argument to an object that the foreign function accepts. For example, a `c_char_p`{.interpreted-text role="class"} item in the `argtypes`{.interpreted-text role="attr"} tuple will convert a string passed as argument into a bytes object using ctypes conversion rules.

New: It is now possible to put items in argtypes which are not ctypes types, but each item must have a `~_CData.from_param`{.interpreted-text role="meth"} method which returns a value usable as argument (integer, string, ctypes instance). This allows defining adapters that can adapt custom objects as function parameters.
:::

:::: attribute
errcheck

Assign a Python function or another callable to this attribute. The callable will be called with three or more arguments:

::: {.function noindex="" module=""}
callable(result, func, arguments)

*result* is what the foreign function returns, as specified by the `!restype`{.interpreted-text role="attr"} attribute.

*func* is the foreign function object itself, this allows reusing the same callable object to check or post process the results of several functions.

*arguments* is a tuple containing the parameters originally passed to the function call, this allows specializing the behavior on the arguments used.
:::

The object that this function returns will be returned from the foreign function call, but it can also check the result value and raise an exception if the foreign function call failed.
::::
:::::::

::: audit-event
ctypes.set_exception code foreign-functions

On Windows, when a foreign function call raises a system exception (for example, due to an access violation), it will be captured and replaced with a suitable Python exception. Further, an auditing event `ctypes.set_exception` with argument `code` will be raised, allowing an audit hook to replace the exception with its own.
:::

::: audit-event
ctypes.call_function func_pointer,arguments foreign-functions

Some ways to invoke foreign function calls as well as some of the functions in this module may raise an auditing event `ctypes.call_function` with arguments `function pointer` and `arguments`.
:::

### Function prototypes {#ctypes-function-prototypes}

Foreign functions can also be created by instantiating function prototypes. Function prototypes are similar to function prototypes in C; they describe a function (return type, argument types, calling convention) without defining an implementation. The factory functions must be called with the desired result type and the argument types of the function, and can be used as decorator factories, and as such, be applied to functions through the `@wrapper` syntax. See `ctypes-callback-functions`{.interpreted-text role="ref"} for examples.

::: function
CFUNCTYPE(restype, \*argtypes, use_errno=False, use_last_error=False)

The returned function prototype creates functions that use the standard C calling convention. The function will release the GIL during the call. If *use_errno* is set to true, the ctypes private copy of the system `errno`{.interpreted-text role="data"} variable is exchanged with the real `errno`{.interpreted-text role="data"} value before and after the call; *use_last_error* does the same for the Windows error code.
:::

:::: function
WINFUNCTYPE(restype, \*argtypes, use_errno=False, use_last_error=False)

The returned function prototype creates functions that use the `stdcall` calling convention. The function will release the GIL during the call. *use_errno* and *use_last_error* have the same meaning as above.

::: availability
Windows
:::
::::

::: function
PYFUNCTYPE(restype, \*argtypes)

The returned function prototype creates functions that use the Python calling convention. The function will *not* release the GIL during the call.
:::

Function prototypes created by these factory functions can be instantiated in different ways, depending on the type and number of the parameters in the call:

::: {.function noindex="" module=""}
prototype(address)

Returns a foreign function at the specified address which must be an integer.
:::

::: {.function noindex="" module=""}
prototype(callable)

Create a C callable function (a callback function) from a Python *callable*.
:::

::: {.function noindex="" module=""}
prototype(func_spec\[, paramflags\])

Returns a foreign function exported by a shared library. *func_spec* must be a 2-tuple `(name_or_ordinal, library)`. The first item is the name of the exported function as string, or the ordinal of the exported function as small integer. The second item is the shared library instance.
:::

:::: {.function noindex="" module=""}
prototype(vtbl_index, name\[, paramflags\[, iid\]\])

Returns a foreign function that will call a COM method. *vtbl_index* is the index into the virtual function table, a small non-negative integer. *name* is name of the COM method. *iid* is an optional pointer to the interface identifier which is used in extended error reporting.

If *iid* is not specified, an `OSError`{.interpreted-text role="exc"} is raised if the COM method call fails. If *iid* is specified, a `~ctypes.COMError`{.interpreted-text role="exc"} is raised instead.

COM methods use a special calling convention: They require a pointer to the COM interface as first argument, in addition to those parameters that are specified in the `!argtypes`{.interpreted-text role="attr"} tuple.

::: availability
Windows
:::
::::

The optional *paramflags* parameter creates foreign function wrappers with much more functionality than the features described above.

*paramflags* must be a tuple of the same length as `~_CFuncPtr.argtypes`{.interpreted-text role="attr"}.

Each item in this tuple contains further information about a parameter, it must be a tuple containing one, two, or three items.

The first item is an integer containing a combination of direction flags for the parameter:

> 
>
> 1
>
> :   Specifies an input parameter to the function.
>
> 2
>
> :   Output parameter. The foreign function fills in a value.
>
> 4
>
> :   Input parameter which defaults to the integer zero.

The optional second item is the parameter name as string. If this is specified, the foreign function can be called with named parameters.

The optional third item is the default value for this parameter.

The following example demonstrates how to wrap the Windows `MessageBoxW` function so that it supports default parameters and named arguments. The C declaration from the windows header file is this:

    WINUSERAPI int WINAPI
    MessageBoxW(
        HWND hWnd,
        LPCWSTR lpText,
        LPCWSTR lpCaption,
        UINT uType);

Here is the wrapping with `!ctypes`{.interpreted-text role="mod"}:

    >>> from ctypes import c_int, WINFUNCTYPE, windll
    >>> from ctypes.wintypes import HWND, LPCWSTR, UINT
    >>> prototype = WINFUNCTYPE(c_int, HWND, LPCWSTR, LPCWSTR, UINT)
    >>> paramflags = (1, "hwnd", 0), (1, "text", "Hi"), (1, "caption", "Hello from ctypes"), (1, "flags", 0)
    >>> MessageBox = prototype(("MessageBoxW", windll.user32), paramflags)

The `MessageBox` foreign function can now be called in these ways:

    >>> MessageBox()
    >>> MessageBox(text="Spam, spam, spam")
    >>> MessageBox(flags=2, text="foo bar")

A second example demonstrates output parameters. The win32 `GetWindowRect` function retrieves the dimensions of a specified window by copying them into `RECT` structure that the caller has to supply. Here is the C declaration:

    WINUSERAPI BOOL WINAPI
    GetWindowRect(
         HWND hWnd,
         LPRECT lpRect);

Here is the wrapping with `!ctypes`{.interpreted-text role="mod"}:

    >>> from ctypes import POINTER, WINFUNCTYPE, windll, WinError
    >>> from ctypes.wintypes import BOOL, HWND, RECT
    >>> prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
    >>> paramflags = (1, "hwnd"), (2, "lprect")
    >>> GetWindowRect = prototype(("GetWindowRect", windll.user32), paramflags)
    >>>

Functions with output parameters will automatically return the output parameter value if there is a single one, or a tuple containing the output parameter values when there are more than one, so the GetWindowRect function now returns a RECT instance, when called.

Output parameters can be combined with the `~_CFuncPtr.errcheck`{.interpreted-text role="attr"} protocol to do further output processing and error checking. The win32 `GetWindowRect` api function returns a `BOOL` to signal success or failure, so this function could do the error checking, and raises an exception when the api call failed:

    >>> def errcheck(result, func, args):
    ...     if not result:
    ...         raise WinError()
    ...     return args
    ...
    >>> GetWindowRect.errcheck = errcheck
    >>>

If the `~_CFuncPtr.errcheck`{.interpreted-text role="attr"} function returns the argument tuple it receives unchanged, `!ctypes`{.interpreted-text role="mod"} continues the normal processing it does on the output parameters. If you want to return a tuple of window coordinates instead of a `RECT` instance, you can retrieve the fields in the function and return them instead, the normal processing will no longer take place:

    >>> def errcheck(result, func, args):
    ...     if not result:
    ...         raise WinError()
    ...     rc = args[1]
    ...     return rc.left, rc.top, rc.bottom, rc.right
    ...
    >>> GetWindowRect.errcheck = errcheck
    >>>

### Utility functions {#ctypes-utility-functions}

:::: function
addressof(obj)

Returns the address of the memory buffer as integer. *obj* must be an instance of a ctypes type.

::: audit-event
ctypes.addressof obj ctypes.addressof
:::
::::

::: function
alignment(obj_or_type)

Returns the alignment requirements of a ctypes type. *obj_or_type* must be a ctypes type or instance.
:::

::: function
byref(obj\[, offset\])

Returns a light-weight pointer to *obj*, which must be an instance of a ctypes type. *offset* defaults to zero, and must be an integer that will be added to the internal pointer value.

`byref(obj, offset)` corresponds to this C code:

    (((char *)&obj) + offset)

The returned object can only be used as a foreign function call parameter. It behaves similar to `pointer(obj)`, but the construction is a lot faster.
:::

::::: function
CopyComPointer(src, dst)

Copies a COM pointer from *src* to *dst* and returns the Windows specific `!HRESULT`{.interpreted-text role="c:type"} value.

If *src* is not `NULL`, its `AddRef` method is called, incrementing the reference count.

In contrast, the reference count of *dst* will not be decremented before assigning the new value. Unless *dst* is `NULL`, the caller is responsible for decrementing the reference count by calling its `Release` method when necessary.

::: availability
Windows
:::

::: versionadded
3.14
:::
:::::

::: function
cast(obj, type)

This function is similar to the cast operator in C. It returns a new instance of *type* which points to the same memory block as *obj*. *type* must be a pointer type, and *obj* must be an object that can be interpreted as a pointer.
:::

:::::: function
create_string_buffer(init, size=None) create_string_buffer(size)

This function creates a mutable character buffer. The returned object is a ctypes array of `c_char`{.interpreted-text role="class"}.

If *size* is given (and not `None`), it must be an `int`{.interpreted-text role="class"}. It specifies the size of the returned array.

If the *init* argument is given, it must be `bytes`{.interpreted-text role="class"}. It is used to initialize the array items. Bytes not initialized this way are set to zero (NUL).

If *size* is not given (or if it is `None`), the buffer is made one element larger than *init*, effectively adding a NUL terminator.

If both arguments are given, *size* must not be less than `len(init)`.

:::: warning
::: title
Warning
:::

If *size* is equal to `len(init)`, a NUL terminator is not added. Do not treat such a buffer as a C string.
::::

For example:

    >>> bytes(create_string_buffer(2))
    b'\x00\x00'
    >>> bytes(create_string_buffer(b'ab'))
    b'ab\x00'
    >>> bytes(create_string_buffer(b'ab', 2))
    b'ab'
    >>> bytes(create_string_buffer(b'ab', 4))
    b'ab\x00\x00'
    >>> bytes(create_string_buffer(b'abcdef', 2))
    Traceback (most recent call last):
       ...
    ValueError: byte string too long

::: audit-event
ctypes.create_string_buffer init,size ctypes.create_string_buffer
:::
::::::

:::: function
create_unicode_buffer(init, size=None) create_unicode_buffer(size)

This function creates a mutable unicode character buffer. The returned object is a ctypes array of `c_wchar`{.interpreted-text role="class"}.

The function takes the same arguments as `~create_string_buffer`{.interpreted-text role="func"} except *init* must be a string and *size* counts `c_wchar`{.interpreted-text role="class"}.

::: audit-event
ctypes.create_unicode_buffer init,size ctypes.create_unicode_buffer
:::
::::

:::: function
DllCanUnloadNow()

This function is a hook which allows implementing in-process COM servers with ctypes. It is called from the DllCanUnloadNow function that the [ctypes]{#ctypes} extension dll exports.

::: availability
Windows
:::
::::

:::: function
DllGetClassObject()

This function is a hook which allows implementing in-process COM servers with ctypes. It is called from the DllGetClassObject function that the `_ctypes` extension dll exports.

::: availability
Windows
:::
::::

::: {.function module="ctypes.util"}
find_library(name)

Try to find a library and return a pathname. *name* is the library name without any prefix like `lib`, suffix like `.so`, `.dylib` or version number (this is the form used for the posix linker option `!-l`{.interpreted-text role="option"}). If no library can be found, returns `None`.

The exact functionality is system dependent.

See `ctypes-finding-shared-libraries`{.interpreted-text role="ref"} for complete documentation.
:::

:::: {.function module="ctypes.util"}
find_msvcrt()

Returns the filename of the VC runtime library used by Python, and by the extension modules. If the name of the library cannot be determined, `None` is returned.

If you need to free memory, for example, allocated by an extension module with a call to the `free(void *)`, it is important that you use the function in the same library that allocated the memory.

::: availability
Windows
:::
::::

::::: {.function module="ctypes.util"}
dllist()

Try to provide a list of paths of the shared libraries loaded into the current process. These paths are not normalized or processed in any way. The function can raise `OSError`{.interpreted-text role="exc"} if the underlying platform APIs fail. The exact functionality is system dependent.

On most platforms, the first element of the list represents the current executable file. It may be an empty string.

::: availability
Windows, macOS, iOS, glibc, BSD libc, musl
:::

::: versionadded
3.14
:::
:::::

:::: function
FormatError(\[code\])

Returns a textual description of the error code *code*. If no error code is specified, the last error code is used by calling the Windows API function `GetLastError`{.interpreted-text role="func"}.

::: availability
Windows
:::
::::

:::: function
GetLastError()

Returns the last error code set by Windows in the calling thread. This function calls the Windows `GetLastError()` function directly, it does not return the ctypes-private copy of the error code.

::: availability
Windows
:::
::::

:::: function
get_errno()

Returns the current value of the ctypes-private copy of the system `errno`{.interpreted-text role="data"} variable in the calling thread.

::: audit-event
ctypes.get_errno \"\" ctypes.get_errno
:::
::::

::::: function
get_last_error()

Returns the current value of the ctypes-private copy of the system `!LastError`{.interpreted-text role="data"} variable in the calling thread.

::: availability
Windows
:::

::: audit-event
ctypes.get_last_error \"\" ctypes.get_last_error
:::
:::::

::: function
memmove(dst, src, count)

Same as the standard C memmove library function: copies *count* bytes from *src* to *dst*. *dst* and *src* must be integers or ctypes instances that can be converted to pointers.
:::

::: function
memset(dst, c, count)

Same as the standard C memset library function: fills the memory block at address *dst* with *count* bytes of value *c*. *dst* must be an integer specifying an address, or a ctypes instance.
:::

:::: function
POINTER(type, /)

Create or return a ctypes pointer type. Pointer types are cached and reused internally, so calling this function repeatedly is cheap. *type* must be a ctypes type.

::: impl-detail
The resulting pointer type is cached in the `__pointer_type__` attribute of *type*. It is possible to set this attribute before the first call to `POINTER` in order to set a custom pointer type. However, doing this is discouraged: manually creating a suitable pointer type is difficult without relying on implementation details that may change in future Python versions.
:::
::::

::: function
pointer(obj, /)

Create a new pointer instance, pointing to *obj*. The returned object is of the type `POINTER(type(obj))`.

Note: If you just want to pass a pointer to an object to a foreign function call, you should use `byref(obj)` which is much faster.
:::

::: function
resize(obj, size)

This function resizes the internal memory buffer of *obj*, which must be an instance of a ctypes type. It is not possible to make the buffer smaller than the native size of the objects type, as given by `sizeof(type(obj))`, but it is possible to enlarge the buffer.
:::

:::: function
set_errno(value)

Set the current value of the ctypes-private copy of the system `errno`{.interpreted-text role="data"} variable in the calling thread to *value* and return the previous value.

::: audit-event
ctypes.set_errno errno ctypes.set_errno
:::
::::

::::: function
set_last_error(value)

Sets the current value of the ctypes-private copy of the system `!LastError`{.interpreted-text role="data"} variable in the calling thread to *value* and return the previous value.

::: availability
Windows
:::

::: audit-event
ctypes.set_last_error error ctypes.set_last_error
:::
:::::

::: function
sizeof(obj_or_type)

Returns the size in bytes of a ctypes type or instance memory buffer. Does the same as the C `sizeof` operator.
:::

:::: function
string_at(ptr, size=-1)

Return the byte string at *void \*ptr*. If *size* is specified, it is used as size, otherwise the string is assumed to be zero-terminated.

::: audit-event
ctypes.string_at ptr,size ctypes.string_at
:::
::::

::::: function
WinError(code=None, descr=None)

Creates an instance of `OSError`{.interpreted-text role="exc"}. If *code* is not specified, `GetLastError`{.interpreted-text role="func"} is called to determine the error code. If *descr* is not specified, `FormatError`{.interpreted-text role="func"} is called to get a textual description of the error.

::: availability
Windows
:::

::: versionchanged
3.3 An instance of `WindowsError`{.interpreted-text role="exc"} used to be created, which is now an alias of `OSError`{.interpreted-text role="exc"}.
:::
:::::

:::: function
wstring_at(ptr, size=-1)

Return the wide-character string at *void \*ptr*. If *size* is specified, it is used as the number of characters of the string, otherwise the string is assumed to be zero-terminated.

::: audit-event
ctypes.wstring_at ptr,size ctypes.wstring_at
:::
::::

::::: function
memoryview_at(ptr, size, readonly=False)

Return a `memoryview`{.interpreted-text role="class"} object of length *size* that references memory starting at *void \*ptr*.

If *readonly* is true, the returned `!memoryview`{.interpreted-text role="class"} object can not be used to modify the underlying memory. (Changes made by other means will still be reflected in the returned object.)

This function is similar to `string_at`{.interpreted-text role="func"} with the key difference of not making a copy of the specified memory. It is a semantically equivalent (but more efficient) alternative to `memoryview((c_byte * size).from_address(ptr))`. (While `~_CData.from_address`{.interpreted-text role="meth"} only takes integers, *ptr* can also be given as a `ctypes.POINTER`{.interpreted-text role="class"} or a `~ctypes.byref`{.interpreted-text role="func"} object.)

::: audit-event
ctypes.memoryview_at address,size,readonly
:::

::: versionadded
3.14
:::
:::::

### Data types {#ctypes-data-types}

:::::::::::::::: _CData
This non-public class is the common base class of all ctypes data types. Among other things, all ctypes type instances contain a memory block that hold C compatible data; the address of the memory block is returned by the `addressof`{.interpreted-text role="func"} helper function. Another instance variable is exposed as `_objects`{.interpreted-text role="attr"}; this contains other Python objects that need to be kept alive in case the memory block contains pointers.

Common methods of ctypes data types, these are all class methods (to be exact, they are methods of the `metaclass`{.interpreted-text role="term"}):

:::: method
[CData.from_buffer]{#cdata.from_buffer}(source\[, offset\])

This method returns a ctypes instance that shares the buffer of the *source* object. The *source* object must support the writeable buffer interface. The optional *offset* parameter specifies an offset into the source buffer in bytes; the default is zero. If the source buffer is not large enough a `ValueError`{.interpreted-text role="exc"} is raised.

::: audit-event
ctypes.cdata/buffer pointer,size,offset ctypes.\_CData.from_buffer
:::
::::

:::: method
[CData.from_buffer_copy]{#cdata.from_buffer_copy}(source\[, offset\])

This method creates a ctypes instance, copying the buffer from the *source* object buffer which must be readable. The optional *offset* parameter specifies an offset into the source buffer in bytes; the default is zero. If the source buffer is not large enough a `ValueError`{.interpreted-text role="exc"} is raised.

::: audit-event
ctypes.cdata/buffer pointer,size,offset ctypes.\_CData.from_buffer_copy
:::
::::

:::: method
from_address(address)

This method returns a ctypes type instance using the memory specified by *address* which must be an integer.

::: audit-event
ctypes.cdata address ctypes.\_CData.from_address

This method, and others that indirectly call this method, raises an `auditing event <auditing>`{.interpreted-text role="ref"} `ctypes.cdata` with argument `address`.
:::
::::

::: method
from_param(obj)

This method adapts *obj* to a ctypes type. It is called with the actual object used in a foreign function call when the type is present in the foreign function\'s `~_CFuncPtr.argtypes`{.interpreted-text role="attr"} tuple; it must return an object that can be used as a function call parameter.

All ctypes data types have a default implementation of this classmethod that normally returns *obj* if that is an instance of the type. Some types accept other objects as well.
:::

::: method
in_dll(library, name)

This method returns a ctypes type instance exported by a shared library. *name* is the name of the symbol that exports the data, *library* is the loaded shared library.
:::

Common class variables of ctypes data types:

:::: attribute
\_\_pointer_type\_\_

The pointer type that was created by calling `POINTER`{.interpreted-text role="func"} for corresponding ctypes data type. If a pointer type was not yet created, the attribute is missing.

::: versionadded
3.14
:::
::::

Common instance variables of ctypes data types:

::: attribute
[b_base]{#b_base}\_

Sometimes ctypes data instances do not own the memory block they contain, instead they share part of the memory block of a base object. The `_b_base_`{.interpreted-text role="attr"} read-only member is the root ctypes object that owns the memory block.
:::

::: attribute
[b_needsfree]{#b_needsfree}\_

This read-only variable is true when the ctypes data instance has allocated the memory block itself, false otherwise.
:::

::: attribute
[objects]{#objects}

This member is either `None` or a dictionary containing Python objects that need to be kept alive so that the memory block contents is kept valid. This object is only exposed for debugging; never modify the contents of this dictionary.
:::
::::::::::::::::

### Fundamental data types {#ctypes-fundamental-data-types-2}

:::: _SimpleCData
This non-public class is the base class of all fundamental ctypes data types. It is mentioned here because it contains the common attributes of the fundamental ctypes data types. `_SimpleCData`{.interpreted-text role="class"} is a subclass of `_CData`{.interpreted-text role="class"}, so it inherits their methods and attributes. ctypes data types that are not and do not contain pointers can now be pickled.

Instances have a single attribute:

::: attribute
value

This attribute contains the actual value of the instance. For integer and pointer types, it is an integer, for character types, it is a single character bytes object or string, for character pointer types it is a Python bytes object or string.

When the `value` attribute is retrieved from a ctypes instance, usually a new object is returned each time. `!ctypes`{.interpreted-text role="mod"} does *not* implement original object return, always a new object is constructed. The same is true for all other ctypes object instances.
:::
::::

Fundamental data types, when returned as foreign function call results, or, for example, by retrieving structure field members or array items, are transparently converted to native Python types. In other words, if a foreign function has a `~_CFuncPtr.restype`{.interpreted-text role="attr"} of `c_char_p`{.interpreted-text role="class"}, you will always receive a Python bytes object, *not* a `c_char_p`{.interpreted-text role="class"} instance.

Subclasses of fundamental data types do *not* inherit this behavior. So, if a foreign functions `!restype`{.interpreted-text role="attr"} is a subclass of `c_void_p`{.interpreted-text role="class"}, you will receive an instance of this subclass from the function call. Of course, you can get the value of the pointer by accessing the `value` attribute.

These are the fundamental ctypes data types:

::: c_byte
Represents the C `signed char`{.interpreted-text role="c:expr"} datatype, and interprets the value as small integer. The constructor accepts an optional integer initializer; no overflow checking is done.
:::

::: c_char
Represents the C `char`{.interpreted-text role="c:expr"} datatype, and interprets the value as a single character. The constructor accepts an optional string initializer, the length of the string must be exactly one character.
:::

::: c_char_p
Represents the C `char *`{.interpreted-text role="c:expr"} datatype when it points to a zero-terminated string. For a general character pointer that may also point to binary data, `POINTER(c_char)` must be used. The constructor accepts an integer address, or a bytes object.
:::

::: c_double
Represents the C `double`{.interpreted-text role="c:expr"} datatype. The constructor accepts an optional float initializer.
:::

::: c_longdouble
Represents the C `long double`{.interpreted-text role="c:expr"} datatype. The constructor accepts an optional float initializer. On platforms where `sizeof(long double) == sizeof(double)` it is an alias to `c_double`{.interpreted-text role="class"}.
:::

::: c_float
Represents the C `float`{.interpreted-text role="c:expr"} datatype. The constructor accepts an optional float initializer.
:::

:::: c_double_complex
Represents the C `double complex`{.interpreted-text role="c:expr"} datatype, if available. The constructor accepts an optional `complex`{.interpreted-text role="class"} initializer.

::: versionadded
3.14
:::
::::

:::: c_float_complex
Represents the C `float complex`{.interpreted-text role="c:expr"} datatype, if available. The constructor accepts an optional `complex`{.interpreted-text role="class"} initializer.

::: versionadded
3.14
:::
::::

:::: c_longdouble_complex
Represents the C `long double complex`{.interpreted-text role="c:expr"} datatype, if available. The constructor accepts an optional `complex`{.interpreted-text role="class"} initializer.

::: versionadded
3.14
:::
::::

::: c_int
Represents the C `signed int`{.interpreted-text role="c:expr"} datatype. The constructor accepts an optional integer initializer; no overflow checking is done. On platforms where `sizeof(int) == sizeof(long)` it is an alias to `c_long`{.interpreted-text role="class"}.
:::

::: c_int8
Represents the C 8-bit `signed int`{.interpreted-text role="c:expr"} datatype. It is an alias for `c_byte`{.interpreted-text role="class"}.
:::

::: c_int16
Represents the C 16-bit `signed int`{.interpreted-text role="c:expr"} datatype. Usually an alias for `c_short`{.interpreted-text role="class"}.
:::

::: c_int32
Represents the C 32-bit `signed int`{.interpreted-text role="c:expr"} datatype. Usually an alias for `c_int`{.interpreted-text role="class"}.
:::

::: c_int64
Represents the C 64-bit `signed int`{.interpreted-text role="c:expr"} datatype. Usually an alias for `c_longlong`{.interpreted-text role="class"}.
:::

::: c_long
Represents the C `signed long`{.interpreted-text role="c:expr"} datatype. The constructor accepts an optional integer initializer; no overflow checking is done.
:::

::: c_longlong
Represents the C `signed long long`{.interpreted-text role="c:expr"} datatype. The constructor accepts an optional integer initializer; no overflow checking is done.
:::

::: c_short
Represents the C `signed short`{.interpreted-text role="c:expr"} datatype. The constructor accepts an optional integer initializer; no overflow checking is done.
:::

::: c_size_t
Represents the C `size_t`{.interpreted-text role="c:type"} datatype.
:::

:::: c_ssize_t
Represents the C `ssize_t`{.interpreted-text role="c:type"} datatype.

::: versionadded
3.2
:::
::::

:::: c_time_t
Represents the C `time_t`{.interpreted-text role="c:type"} datatype.

::: versionadded
3.12
:::
::::

::: c_ubyte
Represents the C `unsigned char`{.interpreted-text role="c:expr"} datatype, it interprets the value as small integer. The constructor accepts an optional integer initializer; no overflow checking is done.
:::

::: c_uint
Represents the C `unsigned int`{.interpreted-text role="c:expr"} datatype. The constructor accepts an optional integer initializer; no overflow checking is done. On platforms where `sizeof(int) == sizeof(long)` it is an alias for `c_ulong`{.interpreted-text role="class"}.
:::

::: c_uint8
Represents the C 8-bit `unsigned int`{.interpreted-text role="c:expr"} datatype. It is an alias for `c_ubyte`{.interpreted-text role="class"}.
:::

::: c_uint16
Represents the C 16-bit `unsigned int`{.interpreted-text role="c:expr"} datatype. Usually an alias for `c_ushort`{.interpreted-text role="class"}.
:::

::: c_uint32
Represents the C 32-bit `unsigned int`{.interpreted-text role="c:expr"} datatype. Usually an alias for `c_uint`{.interpreted-text role="class"}.
:::

::: c_uint64
Represents the C 64-bit `unsigned int`{.interpreted-text role="c:expr"} datatype. Usually an alias for `c_ulonglong`{.interpreted-text role="class"}.
:::

::: c_ulong
Represents the C `unsigned long`{.interpreted-text role="c:expr"} datatype. The constructor accepts an optional integer initializer; no overflow checking is done.
:::

::: c_ulonglong
Represents the C `unsigned long long`{.interpreted-text role="c:expr"} datatype. The constructor accepts an optional integer initializer; no overflow checking is done.
:::

::: c_ushort
Represents the C `unsigned short`{.interpreted-text role="c:expr"} datatype. The constructor accepts an optional integer initializer; no overflow checking is done.
:::

::: c_void_p
Represents the C `void *`{.interpreted-text role="c:expr"} type. The value is represented as integer. The constructor accepts an optional integer initializer.
:::

::: c_wchar
Represents the C `wchar_t`{.interpreted-text role="c:type"} datatype, and interprets the value as a single character unicode string. The constructor accepts an optional string initializer, the length of the string must be exactly one character.
:::

::: c_wchar_p
Represents the C `wchar_t *`{.interpreted-text role="c:expr"} datatype, which must be a pointer to a zero-terminated wide character string. The constructor accepts an integer address, or a string.
:::

::: c_bool
Represent the C `bool`{.interpreted-text role="c:expr"} datatype (more accurately, `_Bool`{.interpreted-text role="c:expr"} from C99). Its value can be `True` or `False`, and the constructor accepts any object that has a truth value.
:::

:::: HRESULT
Represents a `!HRESULT`{.interpreted-text role="c:type"} value, which contains success or error information for a function or method call.

::: availability
Windows
:::
::::

:::: py_object
Represents the C `PyObject *`{.interpreted-text role="c:expr"} datatype. Calling this without an argument creates a `NULL` `PyObject *`{.interpreted-text role="c:expr"} pointer.

::: versionchanged
3.14 `!py_object`{.interpreted-text role="class"} is now a `generic type`{.interpreted-text role="term"}.
:::
::::

The `!ctypes.wintypes`{.interpreted-text role="mod"} module provides quite some other Windows specific data types, for example `!HWND`{.interpreted-text role="c:type"}, `!WPARAM`{.interpreted-text role="c:type"}, or `!DWORD`{.interpreted-text role="c:type"}. Some useful structures like `!MSG`{.interpreted-text role="c:type"} or `!RECT`{.interpreted-text role="c:type"} are also defined.

### Structured data types {#ctypes-structured-data-types}

::: {.Union(*args, .**kw)}
Abstract base class for unions in native byte order.

Unions share common attributes and behavior with structures; see `Structure`{.interpreted-text role="class"} documentation for details.
:::

:::: {.BigEndianUnion(*args, .**kw)}
Abstract base class for unions in *big endian* byte order.

::: versionadded
3.11
:::
::::

:::: {.LittleEndianUnion(*args, .**kw)}
Abstract base class for unions in *little endian* byte order.

::: versionadded
3.11
:::
::::

::: {.BigEndianStructure(*args, .**kw)}
Abstract base class for structures in *big endian* byte order.
:::

::: {.LittleEndianStructure(*args, .**kw)}
Abstract base class for structures in *little endian* byte order.
:::

Structures and unions with non-native byte order cannot contain pointer type fields, or any other data types containing pointer type fields.

::::::::::: {.Structure(*args, .**kw)}
Abstract base class for structures in *native* byte order.

Concrete structure and union types must be created by subclassing one of these types, and at least define a `_fields_`{.interpreted-text role="attr"} class variable. `!ctypes`{.interpreted-text role="mod"} will create `descriptor`{.interpreted-text role="term"}s which allow reading and writing the fields by direct attribute accesses. These are the

::: attribute
[fields]{#fields}\_

A sequence defining the structure fields. The items must be 2-tuples or 3-tuples. The first item is the name of the field, the second item specifies the type of the field; it can be any ctypes data type.

For integer type fields like `c_int`{.interpreted-text role="class"}, a third optional item can be given. It must be a small positive integer defining the bit width of the field.

Field names must be unique within one structure or union. This is not checked, only one field can be accessed when names are repeated.

It is possible to define the `_fields_`{.interpreted-text role="attr"} class variable *after* the class statement that defines the Structure subclass, this allows creating data types that directly or indirectly reference themselves:

    class List(Structure):
        pass
    List._fields_ = [("pnext", POINTER(List)),
                     ...
                    ]

The `!_fields_`{.interpreted-text role="attr"} class variable can only be set once. Later assignments will raise an `AttributeError`{.interpreted-text role="exc"}.

Additionally, the `!_fields_`{.interpreted-text role="attr"} class variable must be defined before the structure or union type is first used: an instance or subclass is created, `sizeof`{.interpreted-text role="func"} is called on it, and so on. Later assignments to `!_fields_`{.interpreted-text role="attr"} will raise an `AttributeError`{.interpreted-text role="exc"}. If `!_fields_`{.interpreted-text role="attr"} has not been set before such use, the structure or union will have no own fields, as if `!_fields_`{.interpreted-text role="attr"} was empty.

Sub-subclasses of structure types inherit the fields of the base class plus the `_fields_`{.interpreted-text role="attr"} defined in the sub-subclass, if any.
:::

:::: attribute
[pack]{#pack}\_

An optional small integer that allows overriding the alignment of structure fields in the instance.

This is only implemented for the MSVC-compatible memory layout (see `_layout_`{.interpreted-text role="attr"}).

Setting `!_pack_`{.interpreted-text role="attr"} to 0 is the same as not setting it at all. Otherwise, the value must be a positive power of two. The effect is equivalent to `#pragma pack(N)` in C, except `!ctypes`{.interpreted-text role="mod"} may allow larger *n* than what the compiler accepts.

`!_pack_`{.interpreted-text role="attr"} must already be defined when `_fields_`{.interpreted-text role="attr"} is assigned, otherwise it will have no effect.

::: deprecated-removed
3.14 3.19

For historical reasons, if `!_pack_`{.interpreted-text role="attr"} is non-zero, the MSVC-compatible layout will be used by default. On non-Windows platforms, this default is deprecated and is slated to become an error in Python 3.19. If it is intended, set `~Structure._layout_`{.interpreted-text role="attr"} to `'ms'` explicitly.
:::
::::

:::: attribute
[align]{#align}\_

An optional small integer that allows increasing the alignment of the structure when being packed or unpacked to/from memory.

The value must not be negative. The effect is equivalent to `__attribute__((aligned(N)))` on GCC or `#pragma align(N)` on MSVC, except `!ctypes`{.interpreted-text role="mod"} may allow values that the compiler would reject.

`!_align_`{.interpreted-text role="attr"} can only *increase* a structure\'s alignment requirements. Setting it to 0 or 1 has no effect.

Using values that are not powers of two is discouraged and may lead to surprising behavior.

`!_align_`{.interpreted-text role="attr"} must already be defined when `_fields_`{.interpreted-text role="attr"} is assigned, otherwise it will have no effect.

::: versionadded
3.13
:::
::::

:::: attribute
[layout]{#layout}\_

An optional string naming the struct/union layout. It can currently be set to:

- `"ms"`: the layout used by the Microsoft compiler (MSVC). On GCC and Clang, this layout can be selected with `__attribute__((ms_struct))`.
- `"gcc-sysv"`: the layout used by GCC with the System V or "SysV-like" data model, as used on Linux and macOS. With this layout, `~Structure._pack_`{.interpreted-text role="attr"} must be unset or zero.

If not set explicitly, `ctypes` will use a default that matches the platform conventions. This default may change in future Python releases (for example, when a new platform gains official support, or when a difference between similar platforms is found). Currently the default will be:

- On Windows: `"ms"`
- When `~Structure._pack_`{.interpreted-text role="attr"} is specified: `"ms"`. (This is deprecated; see `~Structure._pack_`{.interpreted-text role="attr"} documentation.)
- Otherwise: `"gcc-sysv"`

`!_layout_`{.interpreted-text role="attr"} must already be defined when `~Structure._fields_`{.interpreted-text role="attr"} is assigned, otherwise it will have no effect.

::: versionadded
3.14
:::
::::

::: attribute
[anonymous]{#anonymous}\_

An optional sequence that lists the names of unnamed (anonymous) fields. `_anonymous_`{.interpreted-text role="attr"} must be already defined when `_fields_`{.interpreted-text role="attr"} is assigned, otherwise it will have no effect.

The fields listed in this variable must be structure or union type fields. `!ctypes`{.interpreted-text role="mod"} will create descriptors in the structure type that allows accessing the nested fields directly, without the need to create the structure or union field.

Here is an example type (Windows):

    class _U(Union):
        _fields_ = [("lptdesc", POINTER(TYPEDESC)),
                    ("lpadesc", POINTER(ARRAYDESC)),
                    ("hreftype", HREFTYPE)]

    class TYPEDESC(Structure):
        _anonymous_ = ("u",)
        _fields_ = [("u", _U),
                    ("vt", VARTYPE)]

The `TYPEDESC` structure describes a COM data type, the `vt` field specifies which one of the union fields is valid. Since the `u` field is defined as anonymous field, it is now possible to access the members directly off the TYPEDESC instance. `td.lptdesc` and `td.u.lptdesc` are equivalent, but the former is faster since it does not need to create a temporary union instance:

    td = TYPEDESC()
    td.vt = VT_PTR
    td.lptdesc = POINTER(some_type)
    td.u.lptdesc = POINTER(some_type)
:::

It is possible to define sub-subclasses of structures, they inherit the fields of the base class. If the subclass definition has a separate `_fields_`{.interpreted-text role="attr"} variable, the fields specified in this are appended to the fields of the base class.

Structure and union constructors accept both positional and keyword arguments. Positional arguments are used to initialize member fields in the same order as they are appear in `_fields_`{.interpreted-text role="attr"}. Keyword arguments in the constructor are interpreted as attribute assignments, so they will initialize `_fields_`{.interpreted-text role="attr"} with the same name, or create new attributes for names not present in `_fields_`{.interpreted-text role="attr"}.
:::::::::::

:::::::::::: {.CField(*args, .**kw)}
Descriptor for fields of a `Structure`{.interpreted-text role="class"} and `Union`{.interpreted-text role="class"}. For example:

    >>> class Color(Structure):
    ...     _fields_ = (
    ...         ('red', c_uint8),
    ...         ('green', c_uint8),
    ...         ('blue', c_uint8),
    ...         ('intense', c_bool, 1),
    ...         ('blinking', c_bool, 1),
    ...    )
    ...
    >>> Color.red
    <ctypes.CField 'red' type=c_ubyte, ofs=0, size=1>
    >>> Color.green.type
    <class 'ctypes.c_ubyte'>
    >>> Color.blue.byte_offset
    2
    >>> Color.intense
    <ctypes.CField 'intense' type=c_bool, ofs=3, bit_size=1, bit_offset=0>
    >>> Color.blinking.bit_offset
    1

All attributes are read-only.

`!CField`{.interpreted-text role="class"} objects are created via `~Structure._fields_`{.interpreted-text role="attr"}; do not instantiate the class directly.

::: versionadded
3.14

Previously, descriptors only had `offset` and `size` attributes and a readable string representation; the `!CField`{.interpreted-text role="class"} class was not available directly.
:::

::: attribute
name

Name of the field, as a string.
:::

::: attribute
type

Type of the field, as a `ctypes class <ctypes-data-types>`{.interpreted-text role="ref"}.
:::

::: attribute
offset byte_offset

Offset of the field, in bytes.

For bitfields, this is the offset of the underlying byte-aligned *storage unit*; see `~CField.bit_offset`{.interpreted-text role="attr"}.
:::

::: attribute
byte_size

Size of the field, in bytes.

For bitfields, this is the size of the underlying *storage unit*. Typically, it has the same size as the bitfield\'s type.
:::

::: attribute
size

For non-bitfields, equivalent to `~CField.byte_size`{.interpreted-text role="attr"}.

For bitfields, this contains a backwards-compatible bit-packed value that combines `~CField.bit_size`{.interpreted-text role="attr"} and `~CField.bit_offset`{.interpreted-text role="attr"}. Prefer using the explicit attributes instead.
:::

::: attribute
is_bitfield

True if this is a bitfield.
:::

::: attribute
bit_offset bit_size

The location of a bitfield within its *storage unit*, that is, within `~CField.byte_size`{.interpreted-text role="attr"} bytes of memory starting at `~CField.byte_offset`{.interpreted-text role="attr"}.

To get the field\'s value, read the storage unit as an integer, `shift left <shifting>`{.interpreted-text role="ref"} by `!bit_offset`{.interpreted-text role="attr"} and take the `!bit_size`{.interpreted-text role="attr"} least significant bits.

For non-bitfields, `!bit_offset`{.interpreted-text role="attr"} is zero and `!bit_size`{.interpreted-text role="attr"} is equal to `byte_size * 8`.
:::

::: attribute
is_anonymous

True if this field is anonymous, that is, it contains nested sub-fields that should be merged into a containing structure or union.
:::
::::::::::::

### Arrays and pointers {#ctypes-arrays-pointers}

::::: Array(*args)
Abstract base class for arrays.

The recommended way to create concrete array types is by multiplying any `!ctypes`{.interpreted-text role="mod"} data type with a non-negative integer. Alternatively, you can subclass this type and define `_length_`{.interpreted-text role="attr"} and `_type_`{.interpreted-text role="attr"} class variables. Array elements can be read and written using standard subscript and slice accesses; for slice reads, the resulting object is *not* itself an `Array`{.interpreted-text role="class"}.

::: attribute
[length]{#length}\_

A positive integer specifying the number of elements in the array. Out-of-range subscripts result in an `IndexError`{.interpreted-text role="exc"}. Will be returned by `len`{.interpreted-text role="func"}.
:::

::: attribute
[type]{#type}\_

Specifies the type of each element in the array.
:::

Array subclass constructors accept positional arguments, used to initialize the elements in order.
:::::

::: function
ARRAY(type, length)

Create an array. Equivalent to `type * length`, where *type* is a `!ctypes`{.interpreted-text role="mod"} data type and *length* an integer.

This function is `soft deprecated`{.interpreted-text role="term"} in favor of multiplication. There are no plans to remove it.
:::

::::: _Pointer
Private, abstract base class for pointers.

Concrete pointer types are created by calling `POINTER`{.interpreted-text role="func"} with the type that will be pointed to; this is done automatically by `pointer`{.interpreted-text role="func"}.

If a pointer points to an array, its elements can be read and written using standard subscript and slice accesses. Pointer objects have no size, so `len`{.interpreted-text role="func"} will raise `TypeError`{.interpreted-text role="exc"}. Negative subscripts will read from the memory *before* the pointer (as in C), and out-of-range subscripts will probably crash with an access violation (if you\'re lucky).

::: attribute
[type]{#type}\_

Specifies the type pointed to.
:::

::: attribute
contents

Returns the object to which to pointer points. Assigning to this attribute changes the pointer to point to the assigned object.
:::
:::::

### Exceptions {#ctypes-exceptions}

::: exception
ArgumentError

This exception is raised when a foreign function call cannot convert one of the passed arguments.
:::

:::::::: exception
COMError(hresult, text, details)

This exception is raised when a COM method call failed.

::: attribute
hresult

The integer value representing the error code.
:::

::: attribute
text

The error message.
:::

::: attribute
details

The 5-tuple `(descr, source, helpfile, helpcontext, progid)`.

*descr* is the textual description. *source* is the language-dependent `ProgID` for the class or application that raised the error. *helpfile* is the path of the help file. *helpcontext* is the help context identifier. *progid* is the `ProgID` of the interface that defined the error.
:::

::: availability
Windows
:::

::: versionadded
3.14
:::
::::::::
