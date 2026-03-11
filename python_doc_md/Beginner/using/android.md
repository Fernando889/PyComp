# Using Python on Android {#using-android}

Python on Android is unlike Python on desktop platforms. On a desktop platform, Python is generally installed as a system resource that can be used by any user of that computer. Users then interact with Python by running a `python`{.interpreted-text role="program"} executable and entering commands at an interactive prompt, or by running a Python script.

On Android, there is no concept of installing as a system resource. The only unit of software distribution is an \"app\". There is also no console where you could run a `python`{.interpreted-text role="program"} executable, or interact with a Python REPL.

As a result, the only way you can use Python on Android is in embedded mode -- that is, by writing a native Android application, embedding a Python interpreter using `libpython`, and invoking Python code using the `Python embedding
API <embedding>`{.interpreted-text role="ref"}. The full Python interpreter, the standard library, and all your Python code is then packaged into your app for its own private use.

The Python standard library has some notable omissions and restrictions on Android. See the `API availability guide <mobile-availability>`{.interpreted-text role="ref"} for details.

## Adding Python to an Android app

Most app developers should use one of the following tools, which will provide a much easier experience:

- [Briefcase](https://briefcase.readthedocs.io), from the BeeWare project
- [Buildozer](https://buildozer.readthedocs.io), from the Kivy project
- [Chaquopy](https://chaquo.com/chaquopy)
- [pyqtdeploy](https://www.riverbankcomputing.com/static/Docs/pyqtdeploy/)
- [Termux](https://termux.dev/en/)

If you\'re sure you want to do all of this manually, read on. You can use the `testbed app <Android/testbed>`{.interpreted-text role="source"} as a guide; each step below contains a link to the relevant file.

- First, acquire a build of Python for Android:
  - The easiest way is to download an Android release from [python.org](https://www.python.org/downloads/android/). The `prefix` directory mentioned below is at the top level of the package.
  - Or if you want to build it yourself, follow the instructions in `Android/README.md`{.interpreted-text role="source"}. The `prefix` directory will be created under `cross-build/{HOST}`{.interpreted-text role="samp"}.
- Add code to your `build.gradle <Android/testbed/app/build.gradle.kts>`{.interpreted-text role="source"} file to copy the following items into your project. All except your own Python code can be copied from `prefix/lib`:
  - In your JNI libraries:
    - `libpython*.*.so`
    - `lib*_python.so` (external libraries such as OpenSSL)
  - In your assets:
    - `python*.*` (the Python standard library)
    - `python*.*/site-packages` (your own Python code)
- Add code to your app to `extract the assets to the filesystem
  <Android/testbed/app/src/main/java/org/python/testbed/MainActivity.kt>`{.interpreted-text role="source"}.
- Add code to your app to `start Python in embedded mode
  <Android/testbed/app/src/main/c/main_activity.c>`{.interpreted-text role="source"}. This will need to be C code called via JNI.

## Building a Python package for Android

Python packages can be built for Android as wheels and released on PyPI. The recommended tool for doing this is [cibuildwheel](https://cibuildwheel.pypa.io/en/stable/platforms/#android), which automates all the details of setting up a cross-compilation environment, building the wheel, and testing it on an emulator.
