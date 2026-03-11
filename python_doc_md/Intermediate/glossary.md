# Glossary

::: glossary

`>>>`

:   The default Python prompt of the `interactive`{.interpreted-text role="term"} shell. Often seen for code examples which can be executed interactively in the interpreter.

`...`

:   Can refer to:

    - The default Python prompt of the `interactive`{.interpreted-text role="term"} shell when entering the code for an indented code block, when within a pair of matching left and right delimiters (parentheses, square brackets, curly braces or triple quotes), or after specifying a decorator.

    ::: index
    single: \...; ellipsis literal
    :::

    - The three dots form of the `Ellipsis <bltin-ellipsis-object>`{.interpreted-text role="ref"} object.

abstract base class

:   Abstract base classes complement `duck-typing`{.interpreted-text role="term"} by providing a way to define interfaces when other techniques like `hasattr`{.interpreted-text role="func"} would be clumsy or subtly wrong (for example with `magic methods <special-lookup>`{.interpreted-text role="ref"}). ABCs introduce virtual subclasses, which are classes that don\'t inherit from a class but are still recognized by `isinstance`{.interpreted-text role="func"} and `issubclass`{.interpreted-text role="func"}; see the `abc`{.interpreted-text role="mod"} module documentation. Python comes with many built-in ABCs for data structures (in the `collections.abc`{.interpreted-text role="mod"} module), numbers (in the `numbers`{.interpreted-text role="mod"} module), streams (in the `io`{.interpreted-text role="mod"} module), import finders and loaders (in the `importlib.abc`{.interpreted-text role="mod"} module). You can create your own ABCs with the `abc`{.interpreted-text role="mod"} module.

annotate function

:   A function that can be called to retrieve the `annotations <annotation>`{.interpreted-text role="term"} of an object. This function is accessible as the `~object.__annotate__`{.interpreted-text role="attr"} attribute of functions, classes, and modules. Annotate functions are a subset of `evaluate functions <evaluate function>`{.interpreted-text role="term"}.

annotation

:   A label associated with a variable, a class attribute or a function parameter or return value, used by convention as a `type hint`{.interpreted-text role="term"}.

    Annotations of local variables cannot be accessed at runtime, but annotations of global variables, class attributes, and functions can be retrieved by calling `annotationlib.get_annotations`{.interpreted-text role="func"} on modules, classes, and functions, respectively.

    See `variable annotation`{.interpreted-text role="term"}, `function annotation`{.interpreted-text role="term"}, `484`{.interpreted-text role="pep"}, `526`{.interpreted-text role="pep"}, and `649`{.interpreted-text role="pep"}, which describe this functionality. Also see `annotations-howto`{.interpreted-text role="ref"} for best practices on working with annotations.

argument

:   A value passed to a `function`{.interpreted-text role="term"} (or `method`{.interpreted-text role="term"}) when calling the function. There are two kinds of argument:

    - `keyword argument`{.interpreted-text role="dfn"}: an argument preceded by an identifier (e.g. `name=`) in a function call or passed as a value in a dictionary preceded by `**`. For example, `3` and `5` are both keyword arguments in the following calls to `complex`{.interpreted-text role="func"}:

          complex(real=3, imag=5)
          complex(**{'real': 3, 'imag': 5})

    - `positional argument`{.interpreted-text role="dfn"}: an argument that is not a keyword argument. Positional arguments can appear at the beginning of an argument list and/or be passed as elements of an `iterable`{.interpreted-text role="term"} preceded by `*`. For example, `3` and `5` are both positional arguments in the following calls:

          complex(3, 5)
          complex(*(3, 5))

    Arguments are assigned to the named local variables in a function body. See the `calls`{.interpreted-text role="ref"} section for the rules governing this assignment. Syntactically, any expression can be used to represent an argument; the evaluated value is assigned to the local variable.

    See also the `parameter`{.interpreted-text role="term"} glossary entry, the FAQ question on `the difference between arguments and parameters
    <faq-argument-vs-parameter>`{.interpreted-text role="ref"}, and `362`{.interpreted-text role="pep"}.

asynchronous context manager

:   An object which controls the environment seen in an `async with`{.interpreted-text role="keyword"} statement by defining `~object.__aenter__`{.interpreted-text role="meth"} and `~object.__aexit__`{.interpreted-text role="meth"} methods. Introduced by `492`{.interpreted-text role="pep"}.

asynchronous generator

:   A function which returns an `asynchronous generator iterator`{.interpreted-text role="term"}. It looks like a coroutine function defined with `async def`{.interpreted-text role="keyword"} except that it contains `yield`{.interpreted-text role="keyword"} expressions for producing a series of values usable in an `async for`{.interpreted-text role="keyword"} loop.

    Usually refers to an asynchronous generator function, but may refer to an *asynchronous generator iterator* in some contexts. In cases where the intended meaning isn\'t clear, using the full terms avoids ambiguity.

    An asynchronous generator function may contain `await`{.interpreted-text role="keyword"} expressions as well as `async for`{.interpreted-text role="keyword"}, and `async with`{.interpreted-text role="keyword"} statements.

asynchronous generator iterator

:   An object created by an `asynchronous generator`{.interpreted-text role="term"} function.

    This is an `asynchronous iterator`{.interpreted-text role="term"} which when called using the `~object.__anext__`{.interpreted-text role="meth"} method returns an awaitable object which will execute the body of the asynchronous generator function until the next `yield`{.interpreted-text role="keyword"} expression.

    Each `yield`{.interpreted-text role="keyword"} temporarily suspends processing, remembering the execution state (including local variables and pending try-statements). When the *asynchronous generator iterator* effectively resumes with another awaitable returned by `~object.__anext__`{.interpreted-text role="meth"}, it picks up where it left off. See `492`{.interpreted-text role="pep"} and `525`{.interpreted-text role="pep"}.

asynchronous iterable

:   An object, that can be used in an `async for`{.interpreted-text role="keyword"} statement. Must return an `asynchronous iterator`{.interpreted-text role="term"} from its `~object.__aiter__`{.interpreted-text role="meth"} method. Introduced by `492`{.interpreted-text role="pep"}.

asynchronous iterator

:   An object that implements the `~object.__aiter__`{.interpreted-text role="meth"} and `~object.__anext__`{.interpreted-text role="meth"} methods. `~object.__anext__`{.interpreted-text role="meth"} must return an `awaitable`{.interpreted-text role="term"} object. `async for`{.interpreted-text role="keyword"} resolves the awaitables returned by an asynchronous iterator\'s `~object.__anext__`{.interpreted-text role="meth"} method until it raises a `StopAsyncIteration`{.interpreted-text role="exc"} exception. Introduced by `492`{.interpreted-text role="pep"}.

atomic operation

:   An operation that appears to execute as a single, indivisible step: no other thread can observe it half-done, and its effects become visible all at once. Python does not guarantee that high-level statements are atomic (for example, `x += 1` performs multiple bytecode operations and is not atomic). Atomicity is only guaranteed where explicitly documented. See also `race condition`{.interpreted-text role="term"} and `data race`{.interpreted-text role="term"}.

attached thread state

> A `thread state`{.interpreted-text role="term"} that is active for the current OS thread.
>
> When a `thread state`{.interpreted-text role="term"} is attached, the OS thread has access to the full Python C API and can safely invoke the bytecode interpreter.
>
> Unless a function explicitly notes otherwise, attempting to call the C API without an attached thread state will result in a fatal error or undefined behavior. A thread state can be attached and detached explicitly by the user through the C API, or implicitly by the runtime, including during blocking C calls and by the bytecode interpreter in between calls.
>
> On most builds of Python, having an attached thread state implies that the caller holds the `GIL`{.interpreted-text role="term"} for the current interpreter, so only one OS thread can have an attached thread state at a given moment. In `free-threaded builds <free-threaded build>`{.interpreted-text role="term"} of Python, threads can concurrently hold an attached thread state, allowing for true parallelism of the bytecode interpreter.

attribute

:   A value associated with an object which is usually referenced by name using dotted expressions. For example, if an object *o* has an attribute *a* it would be referenced as *o.a*.

    It is possible to give an object an attribute whose name is not an identifier as defined by `identifiers`{.interpreted-text role="ref"}, for example using `setattr`{.interpreted-text role="func"}, if the object allows it. Such an attribute will not be accessible using a dotted expression, and would instead need to be retrieved with `getattr`{.interpreted-text role="func"}.

awaitable

:   An object that can be used in an `await`{.interpreted-text role="keyword"} expression. Can be a `coroutine`{.interpreted-text role="term"} or an object with an `~object.__await__`{.interpreted-text role="meth"} method. See also `492`{.interpreted-text role="pep"}.

BDFL

:   Benevolent Dictator For Life, a.k.a. [Guido van Rossum](https://gvanrossum.github.io/), Python\'s creator.

binary file

:   A `file object`{.interpreted-text role="term"} able to read and write `bytes-like objects <bytes-like object>`{.interpreted-text role="term"}. Examples of binary files are files opened in binary mode (`'rb'`, `'wb'` or `'rb+'`), `sys.stdin.buffer <sys.stdin>`{.interpreted-text role="data"}, `sys.stdout.buffer <sys.stdout>`{.interpreted-text role="data"}, and instances of `io.BytesIO`{.interpreted-text role="class"} and `gzip.GzipFile`{.interpreted-text role="class"}.

    See also `text file`{.interpreted-text role="term"} for a file object able to read and write `str`{.interpreted-text role="class"} objects.

borrowed reference

:   In Python\'s C API, a borrowed reference is a reference to an object, where the code using the object does not own the reference. It becomes a dangling pointer if the object is destroyed. For example, a garbage collection can remove the last `strong reference`{.interpreted-text role="term"} to the object and so destroy it.

    Calling `Py_INCREF`{.interpreted-text role="c:func"} on the `borrowed reference`{.interpreted-text role="term"} is recommended to convert it to a `strong reference`{.interpreted-text role="term"} in-place, except when the object cannot be destroyed before the last usage of the borrowed reference. The `Py_NewRef`{.interpreted-text role="c:func"} function can be used to create a new `strong reference`{.interpreted-text role="term"}.

bytes-like object

:   An object that supports the `bufferobjects`{.interpreted-text role="ref"} and can export a C-`contiguous`{.interpreted-text role="term"} buffer. This includes all `bytes`{.interpreted-text role="class"}, `bytearray`{.interpreted-text role="class"}, and `array.array`{.interpreted-text role="class"} objects, as well as many common `memoryview`{.interpreted-text role="class"} objects. Bytes-like objects can be used for various operations that work with binary data; these include compression, saving to a binary file, and sending over a socket.

    Some operations need the binary data to be mutable. The documentation often refers to these as \"read-write bytes-like objects\". Example mutable buffer objects include `bytearray`{.interpreted-text role="class"} and a `memoryview`{.interpreted-text role="class"} of a `bytearray`{.interpreted-text role="class"}. Other operations require the binary data to be stored in immutable objects (\"read-only bytes-like objects\"); examples of these include `bytes`{.interpreted-text role="class"} and a `memoryview`{.interpreted-text role="class"} of a `bytes`{.interpreted-text role="class"} object.

bytecode

:   Python source code is compiled into bytecode, the internal representation of a Python program in the CPython interpreter. The bytecode is also cached in `.pyc` files so that executing the same file is faster the second time (recompilation from source to bytecode can be avoided). This \"intermediate language\" is said to run on a `virtual machine`{.interpreted-text role="term"} that executes the machine code corresponding to each bytecode. Do note that bytecodes are not expected to work between different Python virtual machines, nor to be stable between Python releases.

    A list of bytecode instructions can be found in the documentation for `the dis module <bytecodes>`{.interpreted-text role="ref"}.

callable

:   A callable is an object that can be called, possibly with a set of arguments (see `argument`{.interpreted-text role="term"}), with the following syntax:

        callable(argument1, argument2, argumentN)

    A `function`{.interpreted-text role="term"}, and by extension a `method`{.interpreted-text role="term"}, is a callable. An instance of a class that implements the `~object.__call__`{.interpreted-text role="meth"} method is also a callable.

callback

:   A subroutine function which is passed as an argument to be executed at some point in the future.

class

:   A template for creating user-defined objects. Class definitions normally contain method definitions which operate on instances of the class.

class variable

:   A variable defined in a class and intended to be modified only at class level (i.e., not in an instance of the class).

closure variable

:   A `free variable`{.interpreted-text role="term"} referenced from a `nested scope`{.interpreted-text role="term"} that is defined in an outer scope rather than being resolved at runtime from the globals or builtin namespaces. May be explicitly defined with the `nonlocal`{.interpreted-text role="keyword"} keyword to allow write access, or implicitly defined if the variable is only being read.

    For example, in the `inner` function in the following code, both `x` and `print` are `free variables <free variable>`{.interpreted-text role="term"}, but only `x` is a *closure variable*:

        def outer():
            x = 0
            def inner():
                nonlocal x
                x += 1
                print(x)
            return inner

    Due to the `codeobject.co_freevars`{.interpreted-text role="attr"} attribute (which, despite its name, only includes the names of closure variables rather than listing all referenced free variables), the more general `free variable`{.interpreted-text role="term"} term is sometimes used even when the intended meaning is to refer specifically to closure variables.

complex number

:   An extension of the familiar real number system in which all numbers are expressed as a sum of a real part and an imaginary part. Imaginary numbers are real multiples of the imaginary unit (the square root of `-1`), often written `i` in mathematics or `j` in engineering. Python has built-in support for complex numbers, which are written with this latter notation; the imaginary part is written with a `j` suffix, e.g., `3+1j`. To get access to complex equivalents of the `math`{.interpreted-text role="mod"} module, use `cmath`{.interpreted-text role="mod"}. Use of complex numbers is a fairly advanced mathematical feature. If you\'re not aware of a need for them, it\'s almost certain you can safely ignore them.

concurrency

:   The ability of a computer program to perform multiple tasks at the same time. Python provides libraries for writing programs that make use of different forms of concurrency. `asyncio`{.interpreted-text role="mod"} is a library for dealing with asynchronous tasks and coroutines. `threading`{.interpreted-text role="mod"} provides access to operating system threads and `multiprocessing`{.interpreted-text role="mod"} to operating system processes. Multi-core processors can execute threads and processes on different CPU cores at the same time (see `parallelism`{.interpreted-text role="term"}).

concurrent modification

:   When multiple threads modify shared data at the same time. Concurrent modification without proper synchronization can cause `race conditions <race condition>`{.interpreted-text role="term"}, and might also trigger a `data race <data race>`{.interpreted-text role="term"}, data corruption, or both.

context

:   This term has different meanings depending on where and how it is used. Some common meanings:

    - The temporary state or environment established by a `context
      manager`{.interpreted-text role="term"} via a `with`{.interpreted-text role="keyword"} statement.
    - The collection of key­value bindings associated with a particular `contextvars.Context`{.interpreted-text role="class"} object and accessed via `~contextvars.ContextVar`{.interpreted-text role="class"} objects. Also see `context
      variable`{.interpreted-text role="term"}.
    - A `contextvars.Context`{.interpreted-text role="class"} object. Also see `current
      context`{.interpreted-text role="term"}.

context management protocol

:   The `~object.__enter__`{.interpreted-text role="meth"} and `~object.__exit__`{.interpreted-text role="meth"} methods called by the `with`{.interpreted-text role="keyword"} statement. See `343`{.interpreted-text role="pep"}.

context manager

:   An object which implements the `context management protocol`{.interpreted-text role="term"} and controls the environment seen in a `with`{.interpreted-text role="keyword"} statement. See `343`{.interpreted-text role="pep"}.

context variable

:   A variable whose value depends on which context is the `current
    context`{.interpreted-text role="term"}. Values are accessed via `contextvars.ContextVar`{.interpreted-text role="class"} objects. Context variables are primarily used to isolate state between concurrent asynchronous tasks.

contiguous

:   ::: index
    C-contiguous, Fortran contiguous
    :::

    A buffer is considered contiguous exactly if it is either *C-contiguous* or *Fortran contiguous*. Zero-dimensional buffers are C and Fortran contiguous. In one-dimensional arrays, the items must be laid out in memory next to each other, in order of increasing indexes starting from zero. In multidimensional C-contiguous arrays, the last index varies the fastest when visiting items in order of memory address. However, in Fortran contiguous arrays, the first index varies the fastest.

coroutine

:   Coroutines are a more generalized form of subroutines. Subroutines are entered at one point and exited at another point. Coroutines can be entered, exited, and resumed at many different points. They can be implemented with the `async def`{.interpreted-text role="keyword"} statement. See also `492`{.interpreted-text role="pep"}.

coroutine function

:   A function which returns a `coroutine`{.interpreted-text role="term"} object. A coroutine function may be defined with the `async def`{.interpreted-text role="keyword"} statement, and may contain `await`{.interpreted-text role="keyword"}, `async for`{.interpreted-text role="keyword"}, and `async with`{.interpreted-text role="keyword"} keywords. These were introduced by `492`{.interpreted-text role="pep"}.

CPython

:   The canonical implementation of the Python programming language, as distributed on [python.org](https://www.python.org). The term \"CPython\" is used when necessary to distinguish this implementation from others such as Jython or IronPython.

current context

:   The `context`{.interpreted-text role="term"} (`contextvars.Context`{.interpreted-text role="class"} object) that is currently used by `~contextvars.ContextVar`{.interpreted-text role="class"} objects to access (get or set) the values of `context variables <context variable>`{.interpreted-text role="term"}. Each thread has its own current context. Frameworks for executing asynchronous tasks (see `asyncio`{.interpreted-text role="mod"}) associate each task with a context which becomes the current context whenever the task starts or resumes execution.

cyclic isolate

:   A subgroup of one or more objects that reference each other in a reference cycle, but are not referenced by objects outside the group. The goal of the `cyclic garbage collector <garbage collection>`{.interpreted-text role="term"} is to identify these groups and break the reference cycles so that the memory can be reclaimed.

data race

:   A situation where multiple threads access the same memory location concurrently, at least one of the accesses is a write, and the threads do not use any synchronization to control their access. Data races lead to `non-deterministic`{.interpreted-text role="term"} behavior and can cause data corruption. Proper use of `locks <lock>`{.interpreted-text role="term"} and other `synchronization primitives
    <synchronization primitive>`{.interpreted-text role="term"} prevents data races. Note that data races can only happen in native code, but that `native code`{.interpreted-text role="term"} might be exposed in a Python API. See also `race condition`{.interpreted-text role="term"} and `thread-safe`{.interpreted-text role="term"}.

deadlock

:   A situation in which two or more tasks (threads, processes, or coroutines) wait indefinitely for each other to release resources or complete actions, preventing any from making progress. For example, if thread A holds lock 1 and waits for lock 2, while thread B holds lock 2 and waits for lock 1, both threads will wait indefinitely. In Python this often arises from acquiring multiple locks in conflicting orders or from circular join/await dependencies. Deadlocks can be avoided by always acquiring multiple `locks <lock>`{.interpreted-text role="term"} in a consistent order. See also `lock`{.interpreted-text role="term"} and `reentrant`{.interpreted-text role="term"}.

decorator

:   A function returning another function, usually applied as a function transformation using the `@wrapper` syntax. Common examples for decorators are `classmethod`{.interpreted-text role="func"} and `staticmethod`{.interpreted-text role="func"}.

    The decorator syntax is merely syntactic sugar, the following two function definitions are semantically equivalent:

        def f(arg):
            ...
        f = staticmethod(f)

        @staticmethod
        def f(arg):
            ...

    The same concept exists for classes, but is less commonly used there. See the documentation for `function definitions <function>`{.interpreted-text role="ref"} and `class definitions <class>`{.interpreted-text role="ref"} for more about decorators.

descriptor

:   Any object which defines the methods `~object.__get__`{.interpreted-text role="meth"}, `~object.__set__`{.interpreted-text role="meth"}, or `~object.__delete__`{.interpreted-text role="meth"}. When a class attribute is a descriptor, its special binding behavior is triggered upon attribute lookup. Normally, using *a.b* to get, set or delete an attribute looks up the object named *b* in the class dictionary for *a*, but if *b* is a descriptor, the respective descriptor method gets called. Understanding descriptors is a key to a deep understanding of Python because they are the basis for many features including functions, methods, properties, class methods, static methods, and reference to super classes.

    For more information about descriptors\' methods, see `descriptors`{.interpreted-text role="ref"} or the `Descriptor How To Guide <descriptorhowto>`{.interpreted-text role="ref"}.

dictionary

:   An associative array, where arbitrary keys are mapped to values. The keys can be any object with `~object.__hash__`{.interpreted-text role="meth"} and `~object.__eq__`{.interpreted-text role="meth"} methods. Called a hash in Perl.

dictionary comprehension

:   A compact way to process all or part of the elements in an iterable and return a dictionary with the results. `results = {n: n ** 2 for n in range(10)}` generates a dictionary containing key `n` mapped to value `n ** 2`. See `comprehensions`{.interpreted-text role="ref"}.

dictionary view

:   The objects returned from `dict.keys`{.interpreted-text role="meth"}, `dict.values`{.interpreted-text role="meth"}, and `dict.items`{.interpreted-text role="meth"} are called dictionary views. They provide a dynamic view on the dictionary's entries, which means that when the dictionary changes, the view reflects these changes. To force the dictionary view to become a full list use `list(dictview)`. See `dict-views`{.interpreted-text role="ref"}.

docstring

:   A string literal which appears as the first expression in a class, function or module. While ignored when the suite is executed, it is recognized by the compiler and put into the `~definition.__doc__`{.interpreted-text role="attr"} attribute of the enclosing class, function or module. Since it is available via introspection, it is the canonical place for documentation of the object.

duck-typing

:   A programming style which does not look at an object\'s type to determine if it has the right interface; instead, the method or attribute is simply called or used (\"If it looks like a duck and quacks like a duck, it must be a duck.\") By emphasizing interfaces rather than specific types, well-designed code improves its flexibility by allowing polymorphic substitution. Duck-typing avoids tests using `type`{.interpreted-text role="func"} or `isinstance`{.interpreted-text role="func"}. (Note, however, that duck-typing can be complemented with `abstract base classes <abstract base class>`{.interpreted-text role="term"}.) Instead, it typically employs `hasattr`{.interpreted-text role="func"} tests or `EAFP`{.interpreted-text role="term"} programming.

dunder

:   An informal short-hand for \"double underscore\", used when talking about a `special method`{.interpreted-text role="term"}. For example, `__init__` is often pronounced \"dunder init\".

EAFP

:   Easier to ask for forgiveness than permission. This common Python coding style assumes the existence of valid keys or attributes and catches exceptions if the assumption proves false. This clean and fast style is characterized by the presence of many `try`{.interpreted-text role="keyword"} and `except`{.interpreted-text role="keyword"} statements. The technique contrasts with the `LBYL`{.interpreted-text role="term"} style common to many other languages such as C.

evaluate function

:   A function that can be called to evaluate a lazily evaluated attribute of an object, such as the value of type aliases created with the `type`{.interpreted-text role="keyword"} statement.

expression

:   A piece of syntax which can be evaluated to some value. In other words, an expression is an accumulation of expression elements like literals, names, attribute access, operators or function calls which all return a value. In contrast to many other languages, not all language constructs are expressions. There are also `statement`{.interpreted-text role="term"}s which cannot be used as expressions, such as `while`{.interpreted-text role="keyword"}. Assignments are also statements, not expressions.

extension module

:   A module written in C or C++, using Python\'s C API to interact with the core and with user code.

f-string f-strings String literals prefixed with `f` or `F` are commonly called \"f-strings\" which is short for `formatted string literals <f-strings>`{.interpreted-text role="ref"}. See also `498`{.interpreted-text role="pep"}.

file object

:   An object exposing a file-oriented API (with methods such as `!read`{.interpreted-text role="meth"} or `!write`{.interpreted-text role="meth"}) to an underlying resource. Depending on the way it was created, a file object can mediate access to a real on-disk file or to another type of storage or communication device (for example standard input/output, in-memory buffers, sockets, pipes, etc.). File objects are also called `file-like objects`{.interpreted-text role="dfn"} or `streams`{.interpreted-text role="dfn"}.

    There are actually three categories of file objects: raw `binary files <binary file>`{.interpreted-text role="term"}, buffered `binary files <binary file>`{.interpreted-text role="term"} and `text files <text file>`{.interpreted-text role="term"}. Their interfaces are defined in the `io`{.interpreted-text role="mod"} module. The canonical way to create a file object is by using the `open`{.interpreted-text role="func"} function.

file-like object

:   A synonym for `file object`{.interpreted-text role="term"}.

filesystem encoding and error handler

:   Encoding and error handler used by Python to decode bytes from the operating system and encode Unicode to the operating system.

    The filesystem encoding must guarantee to successfully decode all bytes below 128. If the file system encoding fails to provide this guarantee, API functions can raise `UnicodeError`{.interpreted-text role="exc"}.

    The `sys.getfilesystemencoding`{.interpreted-text role="func"} and `sys.getfilesystemencodeerrors`{.interpreted-text role="func"} functions can be used to get the filesystem encoding and error handler.

    The `filesystem encoding and error handler`{.interpreted-text role="term"} are configured at Python startup by the `PyConfig_Read`{.interpreted-text role="c:func"} function: see `~PyConfig.filesystem_encoding`{.interpreted-text role="c:member"} and `~PyConfig.filesystem_errors`{.interpreted-text role="c:member"} members of `PyConfig`{.interpreted-text role="c:type"}.

    See also the `locale encoding`{.interpreted-text role="term"}.

finder

:   An object that tries to find the `loader`{.interpreted-text role="term"} for a module that is being imported.

    There are two types of finder: `meta path finders
    <meta path finder>`{.interpreted-text role="term"} for use with `sys.meta_path`{.interpreted-text role="data"}, and `path
    entry finders <path entry finder>`{.interpreted-text role="term"} for use with `sys.path_hooks`{.interpreted-text role="data"}.

    See `finders-and-loaders`{.interpreted-text role="ref"} and `importlib`{.interpreted-text role="mod"} for much more detail.

floor division

:   Mathematical division that rounds down to nearest integer. The floor division operator is `//`. For example, the expression `11 // 4` evaluates to `2` in contrast to the `2.75` returned by float true division. Note that `(-11) // 4` is `-3` because that is `-2.75` rounded *downward*. See `238`{.interpreted-text role="pep"}.

free threading

:   A threading model where multiple threads can run Python bytecode simultaneously within the same interpreter. This is in contrast to the `global interpreter lock`{.interpreted-text role="term"} which allows only one thread to execute Python bytecode at a time. See `703`{.interpreted-text role="pep"}.

free-threaded build

> A build of `CPython`{.interpreted-text role="term"} that supports `free threading`{.interpreted-text role="term"}, configured using the `--disable-gil`{.interpreted-text role="option"} option before compilation.
>
> See `freethreading-python-howto`{.interpreted-text role="ref"}.

free variable

:   Formally, as defined in the `language execution model <bind_names>`{.interpreted-text role="ref"}, a free variable is any variable used in a namespace which is not a local variable in that namespace. See `closure variable`{.interpreted-text role="term"} for an example. Pragmatically, due to the name of the `codeobject.co_freevars`{.interpreted-text role="attr"} attribute, the term is also sometimes used as a synonym for `closure variable`{.interpreted-text role="term"}.

function

:   A series of statements which returns some value to a caller. It can also be passed zero or more `arguments <argument>`{.interpreted-text role="term"} which may be used in the execution of the body. See also `parameter`{.interpreted-text role="term"}, `method`{.interpreted-text role="term"}, and the `function`{.interpreted-text role="ref"} section.

function annotation

:   An `annotation`{.interpreted-text role="term"} of a function parameter or return value.

    Function annotations are usually used for `type hints <type hint>`{.interpreted-text role="term"}: for example, this function is expected to take two `int`{.interpreted-text role="class"} arguments and is also expected to have an `int`{.interpreted-text role="class"} return value:

        def sum_two_numbers(a: int, b: int) -> int:
           return a + b

    Function annotation syntax is explained in section `function`{.interpreted-text role="ref"}.

    See `variable annotation`{.interpreted-text role="term"} and `484`{.interpreted-text role="pep"}, which describe this functionality. Also see `annotations-howto`{.interpreted-text role="ref"} for best practices on working with annotations.

\_\_future\_\_

:   A `future statement <future>`{.interpreted-text role="ref"}, `from __future__ import <feature>`, directs the compiler to compile the current module using syntax or semantics that will become standard in a future release of Python. The `__future__`{.interpreted-text role="mod"} module documents the possible values of *feature*. By importing this module and evaluating its variables, you can see when a new feature was first added to the language and when it will (or did) become the default:

        >>> import __future__
        >>> __future__.division
        _Feature((2, 2, 0, 'alpha', 2), (3, 0, 0, 'alpha', 0), 8192)

garbage collection

:   The process of freeing memory when it is not used anymore. Python performs garbage collection via reference counting and a cyclic garbage collector that is able to detect and break reference cycles. The garbage collector can be controlled using the `gc`{.interpreted-text role="mod"} module.

    ::: index
    single: generator
    :::

generator

:   A function which returns a `generator iterator`{.interpreted-text role="term"}. It looks like a normal function except that it contains `yield`{.interpreted-text role="keyword"} expressions for producing a series of values usable in a for-loop or that can be retrieved one at a time with the `next`{.interpreted-text role="func"} function.

    Usually refers to a generator function, but may refer to a *generator iterator* in some contexts. In cases where the intended meaning isn\'t clear, using the full terms avoids ambiguity.

generator iterator

:   An object created by a `generator`{.interpreted-text role="term"} function.

    Each `yield`{.interpreted-text role="keyword"} temporarily suspends processing, remembering the execution state (including local variables and pending try-statements). When the *generator iterator* resumes, it picks up where it left off (in contrast to functions which start fresh on every invocation).

    ::: index
    single: generator expression
    :::

generator expression

:   An `expression`{.interpreted-text role="term"} that returns an `iterator`{.interpreted-text role="term"}. It looks like a normal expression followed by a `!for`{.interpreted-text role="keyword"} clause defining a loop variable, range, and an optional `!if`{.interpreted-text role="keyword"} clause. The combined expression generates values for an enclosing function:

        >>> sum(i*i for i in range(10))         # sum of squares 0, 1, 4, ... 81
        285

generic function

:   A function composed of multiple functions implementing the same operation for different types. Which implementation should be used during a call is determined by the dispatch algorithm.

    See also the `single dispatch`{.interpreted-text role="term"} glossary entry, the `functools.singledispatch`{.interpreted-text role="func"} decorator, and `443`{.interpreted-text role="pep"}.

generic type

:   A `type`{.interpreted-text role="term"} that can be parameterized; typically a `container class<sequence-types>`{.interpreted-text role="ref"} such as `list`{.interpreted-text role="class"} or `dict`{.interpreted-text role="class"}. Used for `type hints <type hint>`{.interpreted-text role="term"} and `annotations <annotation>`{.interpreted-text role="term"}.

    For more details, see `generic alias types<types-genericalias>`{.interpreted-text role="ref"}, `483`{.interpreted-text role="pep"}, `484`{.interpreted-text role="pep"}, `585`{.interpreted-text role="pep"}, and the `typing`{.interpreted-text role="mod"} module.

GIL

:   See `global interpreter lock`{.interpreted-text role="term"}.

global interpreter lock

:   The mechanism used by the `CPython`{.interpreted-text role="term"} interpreter to assure that only one thread executes Python `bytecode`{.interpreted-text role="term"} at a time. This simplifies the CPython implementation by making the object model (including critical built-in types such as `dict`{.interpreted-text role="class"}) implicitly safe against concurrent access. Locking the entire interpreter makes it easier for the interpreter to be multi-threaded, at the expense of much of the parallelism afforded by multi-processor machines.

    However, some extension modules, either standard or third-party, are designed so as to release the GIL when doing computationally intensive tasks such as compression or hashing. Also, the GIL is always released when doing I/O.

    As of Python 3.13, the GIL can be disabled using the `--disable-gil`{.interpreted-text role="option"} build configuration. After building Python with this option, code must be run with `-X gil=0 <-X>`{.interpreted-text role="option"} or after setting the `PYTHON_GIL=0 <PYTHON_GIL>`{.interpreted-text role="envvar"} environment variable. This feature enables improved performance for multi-threaded applications and makes it easier to use multi-core CPUs efficiently. For more details, see `703`{.interpreted-text role="pep"}.

    In prior versions of Python\'s C API, a function might declare that it requires the GIL to be held in order to use it. This refers to having an `attached thread state`{.interpreted-text role="term"}.

global state

:   Data that is accessible throughout a program, such as module-level variables, class variables, or C static variables in `extension modules
    <extension module>`{.interpreted-text role="term"}. In multi-threaded programs, global state shared between threads typically requires synchronization to avoid `race conditions <race condition>`{.interpreted-text role="term"} and `data races <data race>`{.interpreted-text role="term"}.

hash-based pyc

:   A bytecode cache file that uses the hash rather than the last-modified time of the corresponding source file to determine its validity. See `pyc-invalidation`{.interpreted-text role="ref"}.

hashable

:   An object is *hashable* if it has a hash value which never changes during its lifetime (it needs a `~object.__hash__`{.interpreted-text role="meth"} method), and can be compared to other objects (it needs an `~object.__eq__`{.interpreted-text role="meth"} method). Hashable objects which compare equal must have the same hash value.

    Hashability makes an object usable as a dictionary key and a set member, because these data structures use the hash value internally.

    Most of Python\'s immutable built-in objects are hashable; mutable containers (such as lists or dictionaries) are not; immutable containers (such as tuples and frozensets) are only hashable if their elements are hashable. Objects which are instances of user-defined classes are hashable by default. They all compare unequal (except with themselves), and their hash value is derived from their `id`{.interpreted-text role="func"}.

IDLE

:   An Integrated Development and Learning Environment for Python. `idle`{.interpreted-text role="ref"} is a basic editor and interpreter environment which ships with the standard distribution of Python.

immortal

:   *Immortal objects* are a CPython implementation detail introduced in `683`{.interpreted-text role="pep"}.

    If an object is immortal, its `reference count`{.interpreted-text role="term"} is never modified, and therefore it is never deallocated while the interpreter is running. For example, `True`{.interpreted-text role="const"} and `None`{.interpreted-text role="const"} are immortal in CPython.

    Immortal objects can be identified via `sys._is_immortal`{.interpreted-text role="func"}, or via `PyUnstable_IsImmortal`{.interpreted-text role="c:func"} in the C API.

immutable

:   An object with a fixed value. Immutable objects include numbers, strings and tuples. Such an object cannot be altered. A new object has to be created if a different value has to be stored. They play an important role in places where a constant hash value is needed, for example as a key in a dictionary. Immutable objects are inherently `thread-safe`{.interpreted-text role="term"} because their state cannot be modified after creation, eliminating concerns about improperly synchronized `concurrent modification`{.interpreted-text role="term"}.

import path

:   A list of locations (or `path entries <path entry>`{.interpreted-text role="term"}) that are searched by the `path based finder`{.interpreted-text role="term"} for modules to import. During import, this list of locations usually comes from `sys.path`{.interpreted-text role="data"}, but for subpackages it may also come from the parent package\'s `__path__` attribute.

importing

:   The process by which Python code in one module is made available to Python code in another module.

importer

:   An object that both finds and loads a module; both a `finder`{.interpreted-text role="term"} and `loader`{.interpreted-text role="term"} object.

index

:   A numeric value that represents the position of an element in a `sequence`{.interpreted-text role="term"}.

    In Python, indexing starts at zero. For example, `things[0]` names the *first* element of `things`; `things[1]` names the second one.

    In some contexts, Python allows negative indexes for counting from the end of a sequence, and indexing using `slices <slice>`{.interpreted-text role="term"}.

    See also `subscript`{.interpreted-text role="term"}.

interactive

:   Python has an interactive interpreter which means you can enter statements and expressions at the interpreter prompt, immediately execute them and see their results. Just launch `python` with no arguments (possibly by selecting it from your computer\'s main menu). It is a very powerful way to test out new ideas or inspect modules and packages (remember `help(x)`). For more on interactive mode, see `tut-interac`{.interpreted-text role="ref"}.

interpreted

:   Python is an interpreted language, as opposed to a compiled one, though the distinction can be blurry because of the presence of the bytecode compiler. This means that source files can be run directly without explicitly creating an executable which is then run. Interpreted languages typically have a shorter development/debug cycle than compiled ones, though their programs generally also run more slowly. See also `interactive`{.interpreted-text role="term"}.

interpreter shutdown

:   When asked to shut down, the Python interpreter enters a special phase where it gradually releases all allocated resources, such as modules and various critical internal structures. It also makes several calls to the `garbage collector <garbage collection>`{.interpreted-text role="term"}. This can trigger the execution of code in user-defined destructors or weakref callbacks. Code executed during the shutdown phase can encounter various exceptions as the resources it relies on may not function anymore (common examples are library modules or the warnings machinery).

    The main reason for interpreter shutdown is that the `__main__` module or the script being run has finished executing.

iterable

:   An object capable of returning its members one at a time. Examples of iterables include all sequence types (such as `list`{.interpreted-text role="class"}, `str`{.interpreted-text role="class"}, and `tuple`{.interpreted-text role="class"}) and some non-sequence types like `dict`{.interpreted-text role="class"}, `file objects <file object>`{.interpreted-text role="term"}, and objects of any classes you define with an `~object.__iter__`{.interpreted-text role="meth"} method or with a `~object.__getitem__`{.interpreted-text role="meth"} method that implements `sequence`{.interpreted-text role="term"} semantics.

    Iterables can be used in a `for`{.interpreted-text role="keyword"} loop and in many other places where a sequence is needed (`zip`{.interpreted-text role="func"}, `map`{.interpreted-text role="func"}, \...). When an iterable object is passed as an argument to the built-in function `iter`{.interpreted-text role="func"}, it returns an iterator for the object. This iterator is good for one pass over the set of values. When using iterables, it is usually not necessary to call `iter`{.interpreted-text role="func"} or deal with iterator objects yourself. The `for`{.interpreted-text role="keyword"} statement does that automatically for you, creating a temporary unnamed variable to hold the iterator for the duration of the loop. See also `iterator`{.interpreted-text role="term"}, `sequence`{.interpreted-text role="term"}, and `generator`{.interpreted-text role="term"}.

iterator

:   An object representing a stream of data. Repeated calls to the iterator\'s `~iterator.__next__`{.interpreted-text role="meth"} method (or passing it to the built-in function `next`{.interpreted-text role="func"}) return successive items in the stream. When no more data are available a `StopIteration`{.interpreted-text role="exc"} exception is raised instead. At this point, the iterator object is exhausted and any further calls to its `!__next__`{.interpreted-text role="meth"} method just raise `StopIteration`{.interpreted-text role="exc"} again. Iterators are required to have an `~iterator.__iter__`{.interpreted-text role="meth"} method that returns the iterator object itself so every iterator is also iterable and may be used in most places where other iterables are accepted. One notable exception is code which attempts multiple iteration passes. A container object (such as a `list`{.interpreted-text role="class"}) produces a fresh new iterator each time you pass it to the `iter`{.interpreted-text role="func"} function or use it in a `for`{.interpreted-text role="keyword"} loop. Attempting this with an iterator will just return the same exhausted iterator object used in the previous iteration pass, making it appear like an empty container.

    More information can be found in `typeiter`{.interpreted-text role="ref"}.

    ::: impl-detail
    CPython does not consistently apply the requirement that an iterator define `~iterator.__iter__`{.interpreted-text role="meth"}. And also please note that `free-threaded <free threading>`{.interpreted-text role="term"} CPython does not guarantee `thread-safe`{.interpreted-text role="term"} behavior of iterator operations.
    :::

key

:   A value that identifies an entry in a `mapping`{.interpreted-text role="term"}. See also `subscript`{.interpreted-text role="term"}.

key function

:   A key function or collation function is a callable that returns a value used for sorting or ordering. For example, `locale.strxfrm`{.interpreted-text role="func"} is used to produce a sort key that is aware of locale specific sort conventions.

    A number of tools in Python accept key functions to control how elements are ordered or grouped. They include `min`{.interpreted-text role="func"}, `max`{.interpreted-text role="func"}, `sorted`{.interpreted-text role="func"}, `list.sort`{.interpreted-text role="meth"}, `heapq.merge`{.interpreted-text role="func"}, `heapq.nsmallest`{.interpreted-text role="func"}, `heapq.nlargest`{.interpreted-text role="func"}, and `itertools.groupby`{.interpreted-text role="func"}.

    There are several ways to create a key function. For example. the `str.casefold`{.interpreted-text role="meth"} method can serve as a key function for case insensitive sorts. Alternatively, a key function can be built from a `lambda`{.interpreted-text role="keyword"} expression such as `lambda r: (r[0], r[2])`. Also, `operator.attrgetter`{.interpreted-text role="func"}, `operator.itemgetter`{.interpreted-text role="func"}, and `operator.methodcaller`{.interpreted-text role="func"} are three key function constructors. See the `Sorting HOW TO
    <sortinghowto>`{.interpreted-text role="ref"} for examples of how to create and use key functions.

keyword argument

:   See `argument`{.interpreted-text role="term"}.

lambda

:   An anonymous inline function consisting of a single `expression`{.interpreted-text role="term"} which is evaluated when the function is called. The syntax to create a lambda function is `lambda [parameters]: expression`

LBYL

:   Look before you leap. This coding style explicitly tests for pre-conditions before making calls or lookups. This style contrasts with the `EAFP`{.interpreted-text role="term"} approach and is characterized by the presence of many `if`{.interpreted-text role="keyword"} statements.

    In a multi-threaded environment, the LBYL approach can risk introducing a `race condition`{.interpreted-text role="term"} between \"the looking\" and \"the leaping\". For example, the code, `if key in mapping: return mapping[key]` can fail if another thread removes *key* from *mapping* after the test, but before the lookup. This issue can be solved with `locks <lock>`{.interpreted-text role="term"} or by using the `EAFP`{.interpreted-text role="term"} approach. See also `thread-safe`{.interpreted-text role="term"}.

lexical analyzer

> Formal name for the *tokenizer*; see `token`{.interpreted-text role="term"}.

list

:   A built-in Python `sequence`{.interpreted-text role="term"}. Despite its name it is more akin to an array in other languages than to a linked list since access to elements is *O*(1).

list comprehension

:   A compact way to process all or part of the elements in a sequence and return a list with the results. `result = ['{:#04x}'.format(x) for x in range(256) if x % 2 == 0]` generates a list of strings containing even hex numbers (0x..) in the range from 0 to 255. The `if`{.interpreted-text role="keyword"} clause is optional. If omitted, all elements in `range(256)` are processed.

lock

:   A `synchronization primitive`{.interpreted-text role="term"} that allows only one thread at a time to access a shared resource. A thread must acquire a lock before accessing the protected resource and release it afterward. If a thread attempts to acquire a lock that is already held by another thread, it will block until the lock becomes available. Python\'s `threading`{.interpreted-text role="mod"} module provides `~threading.Lock`{.interpreted-text role="class"} (a basic lock) and `~threading.RLock`{.interpreted-text role="class"} (a `reentrant`{.interpreted-text role="term"} lock). Locks are used to prevent `race conditions <race condition>`{.interpreted-text role="term"} and ensure `thread-safe`{.interpreted-text role="term"} access to shared data. Alternative design patterns to locks exist such as queues, producer/consumer patterns, and thread-local state. See also `deadlock`{.interpreted-text role="term"}, and `reentrant`{.interpreted-text role="term"}.

lock-free

:   An operation that does not acquire any `lock`{.interpreted-text role="term"} and uses atomic CPU instructions to ensure correctness. Lock-free operations can execute concurrently without blocking each other and cannot be blocked by operations that hold locks. In `free-threaded <free threading>`{.interpreted-text role="term"} Python, built-in types like `dict`{.interpreted-text role="class"} and `list`{.interpreted-text role="class"} provide lock-free read operations, which means other threads may observe intermediate states during multi-step modifications even when those modifications hold the `per-object lock`{.interpreted-text role="term"}.

loader

:   An object that loads a module. It must define the `!exec_module`{.interpreted-text role="meth"} and `!create_module`{.interpreted-text role="meth"} methods to implement the `~importlib.abc.Loader`{.interpreted-text role="class"} interface. A loader is typically returned by a `finder`{.interpreted-text role="term"}. See also:

    - `finders-and-loaders`{.interpreted-text role="ref"}
    - `importlib.abc.Loader`{.interpreted-text role="class"}
    - `302`{.interpreted-text role="pep"}

locale encoding

:   On Unix, it is the encoding of the LC_CTYPE locale. It can be set with `locale.setlocale(locale.LC_CTYPE, new_locale) <locale.setlocale>`{.interpreted-text role="func"}.

    On Windows, it is the ANSI code page (ex: `"cp1252"`).

    On Android and VxWorks, Python uses `"utf-8"` as the locale encoding.

    `locale.getencoding`{.interpreted-text role="func"} can be used to get the locale encoding.

    See also the `filesystem encoding and error handler`{.interpreted-text role="term"}.

magic method

:   ::: index
    pair: magic; method
    :::

    An informal synonym for `special method`{.interpreted-text role="term"}.

mapping

:   A container object that supports arbitrary key lookups and implements the methods specified in the `collections.abc.Mapping`{.interpreted-text role="class"} or `collections.abc.MutableMapping`{.interpreted-text role="class"} `abstract base classes <collections-abstract-base-classes>`{.interpreted-text role="ref"}. Examples include `dict`{.interpreted-text role="class"}, `collections.defaultdict`{.interpreted-text role="class"}, `collections.OrderedDict`{.interpreted-text role="class"} and `collections.Counter`{.interpreted-text role="class"}.

meta path finder

:   A `finder`{.interpreted-text role="term"} returned by a search of `sys.meta_path`{.interpreted-text role="data"}. Meta path finders are related to, but different from `path entry finders
    <path entry finder>`{.interpreted-text role="term"}.

    See `importlib.abc.MetaPathFinder`{.interpreted-text role="class"} for the methods that meta path finders implement.

metaclass

:   The class of a class. Class definitions create a class name, a class dictionary, and a list of base classes. The metaclass is responsible for taking those three arguments and creating the class. Most object oriented programming languages provide a default implementation. What makes Python special is that it is possible to create custom metaclasses. Most users never need this tool, but when the need arises, metaclasses can provide powerful, elegant solutions. They have been used for logging attribute access, adding thread-safety, tracking object creation, implementing singletons, and many other tasks.

    More information can be found in `metaclasses`{.interpreted-text role="ref"}.

method

:   A function which is defined inside a class body. If called as an attribute of an instance of that class, the method will get the instance object as its first `argument`{.interpreted-text role="term"} (which is usually called `self`). See `function`{.interpreted-text role="term"} and `nested scope`{.interpreted-text role="term"}.

method resolution order

:   Method Resolution Order is the order in which base classes are searched for a member during lookup. See `python_2.3_mro`{.interpreted-text role="ref"} for details of the algorithm used by the Python interpreter since the 2.3 release.

module

:   An object that serves as an organizational unit of Python code. Modules have a namespace containing arbitrary Python objects. Modules are loaded into Python by the process of `importing`{.interpreted-text role="term"}.

    See also `package`{.interpreted-text role="term"}.

module spec

:   A namespace containing the import-related information used to load a module. An instance of `importlib.machinery.ModuleSpec`{.interpreted-text role="class"}.

    See also `module-specs`{.interpreted-text role="ref"}.

MRO

:   See `method resolution order`{.interpreted-text role="term"}.

mutable

:   An `object`{.interpreted-text role="term"} with state that is allowed to change during the course of the program. In multi-threaded programs, mutable objects that are shared between threads require careful synchronization to avoid `race conditions <race condition>`{.interpreted-text role="term"}. See also `immutable`{.interpreted-text role="term"}, `thread-safe`{.interpreted-text role="term"}, and `concurrent modification`{.interpreted-text role="term"}.

named tuple

:   The term \"named tuple\" applies to any type or class that inherits from tuple and whose indexable elements are also accessible using named attributes. The type or class may have other features as well.

    Several built-in types are named tuples, including the values returned by `time.localtime`{.interpreted-text role="func"} and `os.stat`{.interpreted-text role="func"}. Another example is `sys.float_info`{.interpreted-text role="data"}:

        >>> sys.float_info[1]                   # indexed access
        1024
        >>> sys.float_info.max_exp              # named field access
        1024
        >>> isinstance(sys.float_info, tuple)   # kind of tuple
        True

    Some named tuples are built-in types (such as the above examples). Alternatively, a named tuple can be created from a regular class definition that inherits from `tuple`{.interpreted-text role="class"} and that defines named fields. Such a class can be written by hand, or it can be created by inheriting `typing.NamedTuple`{.interpreted-text role="class"}, or with the factory function `collections.namedtuple`{.interpreted-text role="func"}. The latter techniques also add some extra methods that may not be found in hand-written or built-in named tuples.

namespace

:   The place where a variable is stored. Namespaces are implemented as dictionaries. There are the local, global and built-in namespaces as well as nested namespaces in objects (in methods). Namespaces support modularity by preventing naming conflicts. For instance, the functions `builtins.open <.open>`{.interpreted-text role="func"} and `os.open`{.interpreted-text role="func"} are distinguished by their namespaces. Namespaces also aid readability and maintainability by making it clear which module implements a function. For instance, writing `random.seed`{.interpreted-text role="func"} or `itertools.islice`{.interpreted-text role="func"} makes it clear that those functions are implemented by the `random`{.interpreted-text role="mod"} and `itertools`{.interpreted-text role="mod"} modules, respectively.

namespace package

:   A `package`{.interpreted-text role="term"} which serves only as a container for subpackages. Namespace packages may have no physical representation, and specifically are not like a `regular package`{.interpreted-text role="term"} because they have no `__init__.py` file.

    Namespace packages allow several individually installable packages to have a common parent package. Otherwise, it is recommended to use a `regular package`{.interpreted-text role="term"}.

    For more information, see `420`{.interpreted-text role="pep"} and `reference-namespace-package`{.interpreted-text role="ref"}.

    See also `module`{.interpreted-text role="term"}.

native code

:   Code that is compiled to machine instructions and runs directly on the processor, as opposed to code that is interpreted or runs in a virtual machine. In the context of Python, native code typically refers to C, C++, Rust or Fortran code in `extension modules <extension module>`{.interpreted-text role="term"} that can be called from Python. See also `extension module`{.interpreted-text role="term"}.

nested scope

:   The ability to refer to a variable in an enclosing definition. For instance, a function defined inside another function can refer to variables in the outer function. Note that nested scopes by default work only for reference and not for assignment. Local variables both read and write in the innermost scope. Likewise, global variables read and write to the global namespace. The `nonlocal`{.interpreted-text role="keyword"} allows writing to outer scopes.

new-style class

:   Old name for the flavor of classes now used for all class objects. In earlier Python versions, only new-style classes could use Python\'s newer, versatile features like `~object.__slots__`{.interpreted-text role="attr"}, descriptors, properties, `~object.__getattribute__`{.interpreted-text role="meth"}, class methods, and static methods.

non-deterministic

:   Behavior where the outcome of a program can vary between executions with the same inputs. In multi-threaded programs, non-deterministic behavior often results from `race conditions <race condition>`{.interpreted-text role="term"} where the relative timing or interleaving of threads affects the result. Proper synchronization using `locks <lock>`{.interpreted-text role="term"} and other `synchronization primitives <synchronization primitive>`{.interpreted-text role="term"} helps ensure deterministic behavior.

object

:   Any data with state (attributes or value) and defined behavior (methods). Also the ultimate base class of any `new-style
    class`{.interpreted-text role="term"}.

optimized scope

:   A scope where target local variable names are reliably known to the compiler when the code is compiled, allowing optimization of read and write access to these names. The local namespaces for functions, generators, coroutines, comprehensions, and generator expressions are optimized in this fashion. Note: most interpreter optimizations are applied to all scopes, only those relying on a known set of local and nonlocal variable names are restricted to optimized scopes.

optional module

:   An `extension module`{.interpreted-text role="term"} that is part of the `standard library`{.interpreted-text role="term"}, but may be absent in some builds of `CPython`{.interpreted-text role="term"}, usually due to missing third-party libraries or because the module is not available for a given platform.

    See `optional-module-requirements`{.interpreted-text role="ref"} for a list of optional modules that require third-party libraries.

package

:   A Python `module`{.interpreted-text role="term"} which can contain submodules or recursively, subpackages. Technically, a package is a Python module with a `__path__` attribute.

    See also `regular package`{.interpreted-text role="term"} and `namespace package`{.interpreted-text role="term"}.

parallelism

:   Executing multiple operations at the same time (e.g. on multiple CPU cores). In Python builds with the `global interpreter lock (GIL) <global interpreter lock>`{.interpreted-text role="term"}, only one thread runs Python bytecode at a time, so taking advantage of multiple CPU cores typically involves multiple processes (e.g. `multiprocessing`{.interpreted-text role="mod"}) or native extensions that release the GIL. In `free-threaded <free threading>`{.interpreted-text role="term"} Python, multiple Python threads can run Python code simultaneously on different cores.

parameter

:   A named entity in a `function`{.interpreted-text role="term"} (or method) definition that specifies an `argument`{.interpreted-text role="term"} (or in some cases, arguments) that the function can accept. There are five kinds of parameter:

    - `positional-or-keyword`{.interpreted-text role="dfn"}: specifies an argument that can be passed either `positionally <argument>`{.interpreted-text role="term"} or as a `keyword argument
      <argument>`{.interpreted-text role="term"}. This is the default kind of parameter, for example *foo* and *bar* in the following:

          def func(foo, bar=None): ...

    ::: {#positional-only_parameter}
    - `positional-only`{.interpreted-text role="dfn"}: specifies an argument that can be supplied only by position. Positional-only parameters can be defined by including a `/` character in the parameter list of the function definition after them, for example *posonly1* and *posonly2* in the following:

          def func(posonly1, posonly2, /, positional_or_keyword): ...
    :::

    ::: {#keyword-only_parameter}
    - `keyword-only`{.interpreted-text role="dfn"}: specifies an argument that can be supplied only by keyword. Keyword-only parameters can be defined by including a single var-positional parameter or bare `*` in the parameter list of the function definition before them, for example *kw_only1* and *kw_only2* in the following:

          def func(arg, *, kw_only1, kw_only2): ...

    - `var-positional`{.interpreted-text role="dfn"}: specifies that an arbitrary sequence of positional arguments can be provided (in addition to any positional arguments already accepted by other parameters). Such a parameter can be defined by prepending the parameter name with `*`, for example *args* in the following:

          def func(*args, **kwargs): ...

    - `var-keyword`{.interpreted-text role="dfn"}: specifies that arbitrarily many keyword arguments can be provided (in addition to any keyword arguments already accepted by other parameters). Such a parameter can be defined by prepending the parameter name with `**`, for example *kwargs* in the example above.
    :::

    Parameters can specify both optional and required arguments, as well as default values for some optional arguments.

    See also the `argument`{.interpreted-text role="term"} glossary entry, the FAQ question on `the difference between arguments and parameters
    <faq-argument-vs-parameter>`{.interpreted-text role="ref"}, the `inspect.Parameter`{.interpreted-text role="class"} class, the `function`{.interpreted-text role="ref"} section, and `362`{.interpreted-text role="pep"}.

per-object lock

:   A `lock`{.interpreted-text role="term"} associated with an individual object instance rather than a global lock shared across all objects. In `free-threaded
    <free threading>`{.interpreted-text role="term"} Python, built-in types like `dict`{.interpreted-text role="class"} and `list`{.interpreted-text role="class"} use per-object locks to allow concurrent operations on different objects while serializing operations on the same object. Operations that hold the per-object lock prevent other locking operations on the same object from proceeding, but do not block `lock-free`{.interpreted-text role="term"} operations.

path entry

:   A single location on the `import path`{.interpreted-text role="term"} which the `path
    based finder`{.interpreted-text role="term"} consults to find modules for importing.

path entry finder

:   A `finder`{.interpreted-text role="term"} returned by a callable on `sys.path_hooks`{.interpreted-text role="data"} (i.e. a `path entry hook`{.interpreted-text role="term"}) which knows how to locate modules given a `path entry`{.interpreted-text role="term"}.

    See `importlib.abc.PathEntryFinder`{.interpreted-text role="class"} for the methods that path entry finders implement.

path entry hook

:   A callable on the `sys.path_hooks`{.interpreted-text role="data"} list which returns a `path
    entry finder`{.interpreted-text role="term"} if it knows how to find modules on a specific `path
    entry`{.interpreted-text role="term"}.

path based finder

:   One of the default `meta path finders <meta path finder>`{.interpreted-text role="term"} which searches an `import path`{.interpreted-text role="term"} for modules.

path-like object

:   An object representing a file system path. A path-like object is either a `str`{.interpreted-text role="class"} or `bytes`{.interpreted-text role="class"} object representing a path, or an object implementing the `os.PathLike`{.interpreted-text role="class"} protocol. An object that supports the `os.PathLike`{.interpreted-text role="class"} protocol can be converted to a `str`{.interpreted-text role="class"} or `bytes`{.interpreted-text role="class"} file system path by calling the `os.fspath`{.interpreted-text role="func"} function; `os.fsdecode`{.interpreted-text role="func"} and `os.fsencode`{.interpreted-text role="func"} can be used to guarantee a `str`{.interpreted-text role="class"} or `bytes`{.interpreted-text role="class"} result instead, respectively. Introduced by `519`{.interpreted-text role="pep"}.

PEP

:   Python Enhancement Proposal. A PEP is a design document providing information to the Python community, or describing a new feature for Python or its processes or environment. PEPs should provide a concise technical specification and a rationale for proposed features.

    PEPs are intended to be the primary mechanisms for proposing major new features, for collecting community input on an issue, and for documenting the design decisions that have gone into Python. The PEP author is responsible for building consensus within the community and documenting dissenting opinions.

    See `1`{.interpreted-text role="pep"}.

portion

:   A set of files in a single directory (possibly stored in a zip file) that contribute to a namespace package, as defined in `420`{.interpreted-text role="pep"}.

positional argument

:   See `argument`{.interpreted-text role="term"}.

provisional API

:   A provisional API is one which has been deliberately excluded from the standard library\'s backwards compatibility guarantees. While major changes to such interfaces are not expected, as long as they are marked provisional, backwards incompatible changes (up to and including removal of the interface) may occur if deemed necessary by core developers. Such changes will not be made gratuitously \-- they will occur only if serious fundamental flaws are uncovered that were missed prior to the inclusion of the API.

    Even for provisional APIs, backwards incompatible changes are seen as a \"solution of last resort\" - every attempt will still be made to find a backwards compatible resolution to any identified problems.

    This process allows the standard library to continue to evolve over time, without locking in problematic design errors for extended periods of time. See `411`{.interpreted-text role="pep"} for more details.

provisional package

:   See `provisional API`{.interpreted-text role="term"}.

Python 3000

:   Nickname for the Python 3.x release line (coined long ago when the release of version 3 was something in the distant future.) This is also abbreviated \"Py3k\".

Pythonic

:   An idea or piece of code which closely follows the most common idioms of the Python language, rather than implementing code using concepts common to other languages. For example, a common idiom in Python is to loop over all elements of an iterable using a `for`{.interpreted-text role="keyword"} statement. Many other languages don\'t have this type of construct, so people unfamiliar with Python sometimes use a numerical counter instead:

        for i in range(len(food)):
            print(food[i])

    As opposed to the cleaner, Pythonic method:

        for piece in food:
            print(piece)

qualified name

:   A dotted name showing the \"path\" from a module\'s global scope to a class, function or method defined in that module, as defined in `3155`{.interpreted-text role="pep"}. For top-level functions and classes, the qualified name is the same as the object\'s name:

        >>> class C:
        ...     class D:
        ...         def meth(self):
        ...             pass
        ...
        >>> C.__qualname__
        'C'
        >>> C.D.__qualname__
        'C.D'
        >>> C.D.meth.__qualname__
        'C.D.meth'

    When used to refer to modules, the *fully qualified name* means the entire dotted path to the module, including any parent packages, e.g. `email.mime.text`:

        >>> import email.mime.text
        >>> email.mime.text.__name__
        'email.mime.text'

race condition

:   A condition of a program where the behavior depends on the relative timing or ordering of events, particularly in multi-threaded programs. Race conditions can lead to `non-deterministic`{.interpreted-text role="term"} behavior and bugs that are difficult to reproduce. A `data race`{.interpreted-text role="term"} is a specific type of race condition involving unsynchronized access to shared memory. The `LBYL`{.interpreted-text role="term"} coding style is particularly susceptible to race conditions in multi-threaded code. Using `locks <lock>`{.interpreted-text role="term"} and other `synchronization primitives <synchronization primitive>`{.interpreted-text role="term"} helps prevent race conditions.

reference count

:   The number of references to an object. When the reference count of an object drops to zero, it is deallocated. Some objects are `immortal`{.interpreted-text role="term"} and have reference counts that are never modified, and therefore the objects are never deallocated. Reference counting is generally not visible to Python code, but it is a key element of the `CPython`{.interpreted-text role="term"} implementation. Programmers can call the `sys.getrefcount`{.interpreted-text role="func"} function to return the reference count for a particular object.

    In `CPython`{.interpreted-text role="term"}, reference counts are not considered to be stable or well-defined values; the number of references to an object, and how that number is affected by Python code, may be different between versions.

regular package

:   A traditional `package`{.interpreted-text role="term"}, such as a directory containing an `__init__.py` file.

    See also `namespace package`{.interpreted-text role="term"}.

reentrant

:   A property of a function or `lock`{.interpreted-text role="term"} that allows it to be called or acquired multiple times by the same thread without causing errors or a `deadlock`{.interpreted-text role="term"}.

    For functions, reentrancy means the function can be safely called again before a previous invocation has completed, which is important when functions may be called recursively or from signal handlers. Thread-unsafe functions may be `non-deterministic`{.interpreted-text role="term"} if they\'re called reentrantly in a multithreaded program.

    For locks, Python\'s `threading.RLock`{.interpreted-text role="class"} (reentrant lock) is reentrant, meaning a thread that already holds the lock can acquire it again without blocking. In contrast, `threading.Lock`{.interpreted-text role="class"} is not reentrant - attempting to acquire it twice from the same thread will cause a deadlock.

    See also `lock`{.interpreted-text role="term"} and `deadlock`{.interpreted-text role="term"}.

REPL

:   An acronym for the \"read--eval--print loop\", another name for the `interactive`{.interpreted-text role="term"} interpreter shell.

\_\_slots\_\_

:   A declaration inside a class that saves memory by pre-declaring space for instance attributes and eliminating instance dictionaries. Though popular, the technique is somewhat tricky to get right and is best reserved for rare cases where there are large numbers of instances in a memory-critical application.

sequence

:   An `iterable`{.interpreted-text role="term"} which supports efficient element access using integer indices via the `~object.__getitem__`{.interpreted-text role="meth"} special method and defines a `~object.__len__`{.interpreted-text role="meth"} method that returns the length of the sequence. Some built-in sequence types are `list`{.interpreted-text role="class"}, `str`{.interpreted-text role="class"}, `tuple`{.interpreted-text role="class"}, and `bytes`{.interpreted-text role="class"}. Note that `dict`{.interpreted-text role="class"} also supports `~object.__getitem__`{.interpreted-text role="meth"} and `!__len__`{.interpreted-text role="meth"}, but is considered a mapping rather than a sequence because the lookups use arbitrary `hashable`{.interpreted-text role="term"} keys rather than integers.

    The `collections.abc.Sequence`{.interpreted-text role="class"} abstract base class defines a much richer interface that goes beyond just `~object.__getitem__`{.interpreted-text role="meth"} and `~object.__len__`{.interpreted-text role="meth"}, adding `~sequence.count`{.interpreted-text role="meth"}, `~sequence.index`{.interpreted-text role="meth"}, `~object.__contains__`{.interpreted-text role="meth"}, and `~object.__reversed__`{.interpreted-text role="meth"}. Types that implement this expanded interface can be registered explicitly using `~abc.ABCMeta.register`{.interpreted-text role="func"}. For more documentation on sequence methods generally, see `Common Sequence Operations <typesseq-common>`{.interpreted-text role="ref"}.

set comprehension

:   A compact way to process all or part of the elements in an iterable and return a set with the results. `results = {c for c in 'abracadabra' if c not in 'abc'}` generates the set of strings `{'r', 'd'}`. See `comprehensions`{.interpreted-text role="ref"}.

single dispatch

:   A form of `generic function`{.interpreted-text role="term"} dispatch where the implementation is chosen based on the type of a single argument.

slice

:   An object of type `slice`{.interpreted-text role="class"}, used to describe a portion of a `sequence`{.interpreted-text role="term"}. A slice object is created when using the `slicing <slicings>`{.interpreted-text role="ref"} form of `subscript notation <subscriptions>`{.interpreted-text role="ref"}, with colons inside square brackets, such as in `variable_name[1:3:5]`.

soft deprecated

:   A soft deprecated API should not be used in new code, but it is safe for already existing code to use it. The API remains documented and tested, but will not be enhanced further.

    Soft deprecation, unlike normal deprecation, does not plan on removing the API and will not emit warnings.

    See [PEP 387: Soft Deprecation](https://peps.python.org/pep-0387/#soft-deprecation).

special method

:   ::: index
    pair: special; method
    :::

    A method that is called implicitly by Python to execute a certain operation on a type, such as addition. Such methods have names starting and ending with double underscores. Special methods are documented in `specialnames`{.interpreted-text role="ref"}.

standard library

:   The collection of `packages <package>`{.interpreted-text role="term"}, `modules <module>`{.interpreted-text role="term"} and `extension modules <extension module>`{.interpreted-text role="term"} distributed as a part of the official Python interpreter package. The exact membership of the collection may vary based on platform, available system libraries, or other criteria. Documentation can be found at `library-index`{.interpreted-text role="ref"}.

    See also `sys.stdlib_module_names`{.interpreted-text role="data"} for a list of all possible standard library module names.

statement

:   A statement is part of a suite (a \"block\" of code). A statement is either an `expression`{.interpreted-text role="term"} or one of several constructs with a keyword, such as `if`{.interpreted-text role="keyword"}, `while`{.interpreted-text role="keyword"} or `for`{.interpreted-text role="keyword"}.

static type checker

:   An external tool that reads Python code and analyzes it, looking for issues such as incorrect types. See also `type hints <type hint>`{.interpreted-text role="term"} and the `typing`{.interpreted-text role="mod"} module.

stdlib

:   An abbreviation of `standard library`{.interpreted-text role="term"}.

strong reference

:   In Python\'s C API, a strong reference is a reference to an object which is owned by the code holding the reference. The strong reference is taken by calling `Py_INCREF`{.interpreted-text role="c:func"} when the reference is created and released with `Py_DECREF`{.interpreted-text role="c:func"} when the reference is deleted.

    The `Py_NewRef`{.interpreted-text role="c:func"} function can be used to create a strong reference to an object. Usually, the `Py_DECREF`{.interpreted-text role="c:func"} function must be called on the strong reference before exiting the scope of the strong reference, to avoid leaking one reference.

    See also `borrowed reference`{.interpreted-text role="term"}.

subscript

:   The expression in square brackets of a `subscription expression <subscriptions>`{.interpreted-text role="ref"}, for example, the `3` in `items[3]`. Usually used to select an element of a container. Also called a `key`{.interpreted-text role="term"} when subscripting a `mapping`{.interpreted-text role="term"}, or an `index`{.interpreted-text role="term"} when subscripting a `sequence`{.interpreted-text role="term"}.

synchronization primitive

:   A basic building block for coordinating (synchronizing) the execution of multiple threads to ensure `thread-safe`{.interpreted-text role="term"} access to shared resources. Python\'s `threading`{.interpreted-text role="mod"} module provides several synchronization primitives including `~threading.Lock`{.interpreted-text role="class"}, `~threading.RLock`{.interpreted-text role="class"}, `~threading.Semaphore`{.interpreted-text role="class"}, `~threading.Condition`{.interpreted-text role="class"}, `~threading.Event`{.interpreted-text role="class"}, and `~threading.Barrier`{.interpreted-text role="class"}. Additionally, the `queue`{.interpreted-text role="mod"} module provides multi-producer, multi-consumer queues that are especially useful in multithreaded programs. These primitives help prevent `race conditions <race condition>`{.interpreted-text role="term"} and coordinate thread execution. See also `lock`{.interpreted-text role="term"}.

t-string t-strings String literals prefixed with `t` or `T` are commonly called \"t-strings\" which is short for `template string literals <t-strings>`{.interpreted-text role="ref"}.

text encoding

:   A string in Python is a sequence of Unicode code points (in range `U+0000`\--`U+10FFFF`). To store or transfer a string, it needs to be serialized as a sequence of bytes.

    Serializing a string into a sequence of bytes is known as \"encoding\", and recreating the string from the sequence of bytes is known as \"decoding\".

    There are a variety of different text serialization `codecs <standard-encodings>`{.interpreted-text role="ref"}, which are collectively referred to as \"text encodings\".

text file

:   A `file object`{.interpreted-text role="term"} able to read and write `str`{.interpreted-text role="class"} objects. Often, a text file actually accesses a byte-oriented datastream and handles the `text encoding`{.interpreted-text role="term"} automatically. Examples of text files are files opened in text mode (`'r'` or `'w'`), `sys.stdin`{.interpreted-text role="data"}, `sys.stdout`{.interpreted-text role="data"}, and instances of `io.StringIO`{.interpreted-text role="class"}.

    See also `binary file`{.interpreted-text role="term"} for a file object able to read and write `bytes-like objects <bytes-like object>`{.interpreted-text role="term"}.

thread state

> The information used by the `CPython`{.interpreted-text role="term"} runtime to run in an OS thread. For example, this includes the current exception, if any, and the state of the bytecode interpreter.
>
> Each thread state is bound to a single OS thread, but threads may have many thread states available. At most, one of them may be `attached <attached thread state>`{.interpreted-text role="term"} at once.
>
> An `attached thread state`{.interpreted-text role="term"} is required to call most of Python\'s C API, unless a function explicitly documents otherwise. The bytecode interpreter only runs under an attached thread state.
>
> Each thread state belongs to a single interpreter, but each interpreter may have many thread states, including multiple for the same OS thread. Thread states from multiple interpreters may be bound to the same thread, but only one can be `attached <attached thread state>`{.interpreted-text role="term"} in that thread at any given moment.
>
> See `Thread State and the Global Interpreter Lock <threads>`{.interpreted-text role="ref"} for more information.

thread-safe

:   A module, function, or class that behaves correctly when used by multiple threads concurrently. Thread-safe code uses appropriate `synchronization primitives <synchronization primitive>`{.interpreted-text role="term"} like `locks <lock>`{.interpreted-text role="term"} to protect shared mutable state, or is designed to avoid shared mutable state entirely. In the `free-threaded <free threading>`{.interpreted-text role="term"} build, built-in types like `dict`{.interpreted-text role="class"}, `list`{.interpreted-text role="class"}, and `set`{.interpreted-text role="class"} use internal locking to make many operations thread-safe, although thread safety is not necessarily guaranteed. Code that is not thread-safe may experience `race conditions <race condition>`{.interpreted-text role="term"} and `data races <data race>`{.interpreted-text role="term"} when used in multi-threaded programs.

token

> A small unit of source code, generated by the `lexical analyzer <lexical>`{.interpreted-text role="ref"} (also called the *tokenizer*). Names, numbers, strings, operators, newlines and similar are represented by tokens.
>
> The `tokenize`{.interpreted-text role="mod"} module exposes Python\'s lexical analyzer. The `token`{.interpreted-text role="mod"} module contains information on the various types of tokens.

triple-quoted string

:   A string which is bound by three instances of either a quotation mark (\") or an apostrophe (\'). While they don\'t provide any functionality not available with single-quoted strings, they are useful for a number of reasons. They allow you to include unescaped single and double quotes within a string and they can span multiple lines without the use of the continuation character, making them especially useful when writing docstrings.

type

:   The type of a Python object determines what kind of object it is; every object has a type. An object\'s type is accessible as its `~object.__class__`{.interpreted-text role="attr"} attribute or can be retrieved with `type(obj)`.

type alias

:   A synonym for a type, created by assigning the type to an identifier.

    Type aliases are useful for simplifying `type hints <type hint>`{.interpreted-text role="term"}. For example:

        def remove_gray_shades(
                colors: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
            pass

    could be made more readable like this:

        Color = tuple[int, int, int]

        def remove_gray_shades(colors: list[Color]) -> list[Color]:
            pass

    See `typing`{.interpreted-text role="mod"} and `484`{.interpreted-text role="pep"}, which describe this functionality.

type hint

:   An `annotation`{.interpreted-text role="term"} that specifies the expected type for a variable, a class attribute, or a function parameter or return value.

    Type hints are optional and are not enforced by Python but they are useful to `static type checkers <static type checker>`{.interpreted-text role="term"}. They can also aid IDEs with code completion and refactoring.

    Type hints of global variables, class attributes, and functions, but not local variables, can be accessed using `typing.get_type_hints`{.interpreted-text role="func"}.

    See `typing`{.interpreted-text role="mod"} and `484`{.interpreted-text role="pep"}, which describe this functionality.

universal newlines

:   A manner of interpreting text streams in which all of the following are recognized as ending a line: the Unix end-of-line convention `'\n'`, the Windows convention `'\r\n'`, and the old Macintosh convention `'\r'`. See `278`{.interpreted-text role="pep"} and `3116`{.interpreted-text role="pep"}, as well as `bytes.splitlines`{.interpreted-text role="func"} for an additional use.

variable annotation

:   An `annotation`{.interpreted-text role="term"} of a variable or a class attribute.

    When annotating a variable or a class attribute, assignment is optional:

        class C:
            field: 'annotation'

    Variable annotations are usually used for `type hints <type hint>`{.interpreted-text role="term"}: for example this variable is expected to take `int`{.interpreted-text role="class"} values:

        count: int = 0

    Variable annotation syntax is explained in section `annassign`{.interpreted-text role="ref"}.

    See `function annotation`{.interpreted-text role="term"}, `484`{.interpreted-text role="pep"} and `526`{.interpreted-text role="pep"}, which describe this functionality. Also see `annotations-howto`{.interpreted-text role="ref"} for best practices on working with annotations.

virtual environment

:   A cooperatively isolated runtime environment that allows Python users and applications to install and upgrade Python distribution packages without interfering with the behaviour of other Python applications running on the same system.

    See also `venv`{.interpreted-text role="mod"}.

virtual machine

:   A computer defined entirely in software. Python\'s virtual machine executes the `bytecode`{.interpreted-text role="term"} emitted by the bytecode compiler.

walrus operator

:   A light-hearted way to refer to the `assignment expression
    <assignment-expressions>`{.interpreted-text role="ref"} operator `:=` because it looks a bit like a walrus if you turn your head.

Zen of Python

:   Listing of Python design principles and philosophies that are helpful in understanding and using the language. The listing can be found by typing \"`import this`\" at the interactive prompt.
:::
