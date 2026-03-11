# Building C and C++ Extensions on Windows {#building-on-windows}

This chapter briefly explains how to create a Windows extension module for Python using Microsoft Visual C++, and follows with more detailed background information on how it works. The explanatory material is useful for both the Windows programmer learning to build Python extensions and the Unix programmer interested in producing software which can be successfully built on both Unix and Windows.

Module authors are encouraged to use the distutils approach for building extension modules, instead of the one described in this section. You will still need the C compiler that was used to build Python; typically Microsoft Visual C++.

:::: note
::: title
Note
:::

This chapter mentions a number of filenames that include an encoded Python version number. These filenames are represented with the version number shown as `XY`; in practice, `'X'` will be the major version number and `'Y'` will be the minor version number of the Python release you\'re working with. For example, if you are using Python 2.2.1, `XY` will actually be `22`.
::::

## A Cookbook Approach {#win-cookbook}

There are two approaches to building extension modules on Windows, just as there are on Unix: use the `setuptools` package to control the build process, or do things manually. The setuptools approach works well for most extensions; documentation on using `setuptools` to build and package extension modules is available in `setuptools-index`{.interpreted-text role="ref"}. If you find you really need to do things manually, it may be instructive to study the project file for the `winsound <PCbuild/winsound.vcxproj>`{.interpreted-text role="source"} standard library module.

## Differences Between Unix and Windows {#dynamic-linking}

Unix and Windows use completely different paradigms for run-time loading of code. Before you try to build a module that can be dynamically loaded, be aware of how your system works.

In Unix, a shared object (`.so`{.interpreted-text role="file"}) file contains code to be used by the program, and also the names of functions and data that it expects to find in the program. When the file is joined to the program, all references to those functions and data in the file\'s code are changed to point to the actual locations in the program where the functions and data are placed in memory. This is basically a link operation.

In Windows, a dynamic-link library (`.dll`{.interpreted-text role="file"}) file has no dangling references. Instead, an access to functions or data goes through a lookup table. So the DLL code does not have to be fixed up at runtime to refer to the program\'s memory; instead, the code already uses the DLL\'s lookup table, and the lookup table is modified at runtime to point to the functions and data.

In Unix, there is only one type of library file (`.a`{.interpreted-text role="file"}) which contains code from several object files (`.o`{.interpreted-text role="file"}). During the link step to create a shared object file (`.so`{.interpreted-text role="file"}), the linker may find that it doesn\'t know where an identifier is defined. The linker will look for it in the object files in the libraries; if it finds it, it will include all the code from that object file.

In Windows, there are two types of library, a static library and an import library (both called `.lib`{.interpreted-text role="file"}). A static library is like a Unix `.a`{.interpreted-text role="file"} file; it contains code to be included as necessary. An import library is basically used only to reassure the linker that a certain identifier is legal, and will be present in the program when the DLL is loaded. So the linker uses the information from the import library to build the lookup table for using identifiers that are not included in the DLL. When an application or a DLL is linked, an import library may be generated, which will need to be used for all future DLLs that depend on the symbols in the application or DLL.

Suppose you are building two dynamic-load modules, B and C, which should share another block of code A. On Unix, you would *not* pass `A.a`{.interpreted-text role="file"} to the linker for `B.so`{.interpreted-text role="file"} and `C.so`{.interpreted-text role="file"}; that would cause it to be included twice, so that B and C would each have their own copy. In Windows, building `A.dll`{.interpreted-text role="file"} will also build `A.lib`{.interpreted-text role="file"}. You *do* pass `A.lib`{.interpreted-text role="file"} to the linker for B and C. `A.lib`{.interpreted-text role="file"} does not contain code; it just contains information which will be used at runtime to access A\'s code.

In Windows, using an import library is sort of like using `import spam`; it gives you access to spam\'s names, but does not create a separate copy. On Unix, linking with a library is more like `from spam import *`; it does create a separate copy.

> Turn off the implicit, `#pragma`-based linkage with the Python library, performed inside CPython header files.
>
> ::: versionadded
> 3.14
> :::

## Using DLLs in Practice {#win-dlls}

Windows Python is built in Microsoft Visual C++; using other compilers may or may not work. The rest of this section is MSVC++ specific.

When creating DLLs in Windows, you can use the CPython library in two ways:

1.  By default, inclusion of `PC/pyconfig.h`{.interpreted-text role="file"} directly or via `Python.h`{.interpreted-text role="file"} triggers an implicit, configure-aware link with the library. The header file chooses `pythonXY_d.lib`{.interpreted-text role="file"} for Debug, `pythonXY.lib`{.interpreted-text role="file"} for Release, and `pythonX.lib`{.interpreted-text role="file"} for Release with the `Limited API <stable-application-binary-interface>`{.interpreted-text role="ref"} enabled.

    To build two DLLs, spam and ni (which uses C functions found in spam), you could use these commands:

    ``` c
    cl /LD /I/python/include spam.c
    cl /LD /I/python/include ni.c spam.lib
    ```

    The first command created three files: `spam.obj`{.interpreted-text role="file"}, `spam.dll`{.interpreted-text role="file"} and `spam.lib`{.interpreted-text role="file"}. `Spam.dll`{.interpreted-text role="file"} does not contain any Python functions (such as `PyArg_ParseTuple`{.interpreted-text role="c:func"}), but it does know how to find the Python code thanks to the implicitly linked `pythonXY.lib`{.interpreted-text role="file"}.

    The second command created `ni.dll`{.interpreted-text role="file"} (and `.obj`{.interpreted-text role="file"} and `.lib`{.interpreted-text role="file"}), which knows how to find the necessary functions from spam, and also from the Python executable.

2.  Manually by defining `Py_NO_LINK_LIB`{.interpreted-text role="c:macro"} macro before including `Python.h`{.interpreted-text role="file"}. You must pass `pythonXY.lib`{.interpreted-text role="file"} to the linker.

    To build two DLLs, spam and ni (which uses C functions found in spam), you could use these commands:

    ``` c
    cl /LD /DPy_NO_LINK_LIB /I/python/include spam.c ../libs/pythonXY.lib
    cl /LD /DPy_NO_LINK_LIB /I/python/include ni.c spam.lib ../libs/pythonXY.lib
    ```

    The first command created three files: `spam.obj`{.interpreted-text role="file"}, `spam.dll`{.interpreted-text role="file"} and `spam.lib`{.interpreted-text role="file"}. `Spam.dll`{.interpreted-text role="file"} does not contain any Python functions (such as `PyArg_ParseTuple`{.interpreted-text role="c:func"}), but it does know how to find the Python code thanks to `pythonXY.lib`{.interpreted-text role="file"}.

    The second command created `ni.dll`{.interpreted-text role="file"} (and `.obj`{.interpreted-text role="file"} and `.lib`{.interpreted-text role="file"}), which knows how to find the necessary functions from spam, and also from the Python executable.

Not every identifier is exported to the lookup table. If you want any other modules (including Python) to be able to see your identifiers, you have to say `_declspec(dllexport)`, as in `void _declspec(dllexport) initspam(void)` or `PyObject _declspec(dllexport) *NiGetSpamData(void)`.

Developer Studio will throw in a lot of import libraries that you do not really need, adding about 100K to your executable. To get rid of them, use the Project Settings dialog, Link tab, to specify *ignore default libraries*. Add the correct `msvcrt{xx}.lib`{.interpreted-text role="file"} to the list of libraries.
