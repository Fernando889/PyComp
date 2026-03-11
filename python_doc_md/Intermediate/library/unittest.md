# `!unittest`{.interpreted-text role="mod"} \-\-- Unit testing framework

::: {.module synopsis="Unit testing framework for Python."}
unittest
:::

**Source code:** `Lib/unittest/__init__.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

(If you are already familiar with the basic concepts of testing, you might want to skip to `the list of assert methods <assert-methods>`{.interpreted-text role="ref"}.)

The `!unittest`{.interpreted-text role="mod"} unit testing framework was originally inspired by JUnit and has a similar flavor as major unit testing frameworks in other languages. It supports test automation, sharing of setup and shutdown code for tests, aggregation of tests into collections, and independence of the tests from the reporting framework.

To achieve this, `!unittest`{.interpreted-text role="mod"} supports some important concepts in an object-oriented way:

test fixture

:   A `test fixture`{.interpreted-text role="dfn"} represents the preparation needed to perform one or more tests, and any associated cleanup actions. This may involve, for example, creating temporary or proxy databases, directories, or starting a server process.

test case

:   A `test case`{.interpreted-text role="dfn"} is the individual unit of testing. It checks for a specific response to a particular set of inputs. `!unittest`{.interpreted-text role="mod"} provides a base class, `TestCase`{.interpreted-text role="class"}, which may be used to create new test cases.

test suite

:   A `test suite`{.interpreted-text role="dfn"} is a collection of test cases, test suites, or both. It is used to aggregate tests that should be executed together.

test runner

:   A `test runner`{.interpreted-text role="dfn"} is a component which orchestrates the execution of tests and provides the outcome to the user. The runner may use a graphical interface, a textual interface, or return a special value to indicate the results of executing the tests.

::: seealso

Module `doctest`{.interpreted-text role="mod"}

:   Another test-support module with a very different flavor.

[Simple Smalltalk Testing: With Patterns](https://web.archive.org/web/20150315073817/http://www.xprogramming.com/testfram.htm)

:   Kent Beck\'s original paper on testing frameworks using the pattern shared by `!unittest`{.interpreted-text role="mod"}.

[pytest](https://docs.pytest.org/)

:   Third-party unittest framework with a lighter-weight syntax for writing tests. For example, `assert func(10) == 42`.

[The Python Testing Tools Taxonomy](https://wiki.python.org/moin/PythonTestingToolsTaxonomy)

:   An extensive list of Python testing tools including functional testing frameworks and mock object libraries.

[Testing in Python Mailing List](http://lists.idyll.org/listinfo/testing-in-python)

:   A special-interest-group for discussion of testing, and testing tools, in Python.

The script `Tools/unittestgui/unittestgui.py`{.interpreted-text role="file"} in the Python source distribution is a GUI tool for test discovery and execution. This is intended largely for ease of use for those new to unit testing. For production environments it is recommended that tests be driven by a continuous integration system such as [Buildbot](https://buildbot.net/), [Jenkins](https://www.jenkins.io/), [GitHub Actions](https://github.com/features/actions), or [AppVeyor](https://www.appveyor.com/).
:::

## Basic example {#unittest-minimal-example}

The `!unittest`{.interpreted-text role="mod"} module provides a rich set of tools for constructing and running tests. This section demonstrates that a small subset of the tools suffice to meet the needs of most users.

Here is a short script to test three string methods:

    import unittest

    class TestStringMethods(unittest.TestCase):

        def test_upper(self):
            self.assertEqual('foo'.upper(), 'FOO')

        def test_isupper(self):
            self.assertTrue('FOO'.isupper())
            self.assertFalse('Foo'.isupper())

        def test_split(self):
            s = 'hello world'
            self.assertEqual(s.split(), ['hello', 'world'])
            # check that s.split fails when the separator is not a string
            with self.assertRaises(TypeError):
                s.split(2)

    if __name__ == '__main__':
        unittest.main()

A test case is created by subclassing `unittest.TestCase`{.interpreted-text role="class"}. The three individual tests are defined with methods whose names start with the letters `test`. This naming convention informs the test runner about which methods represent tests.

The crux of each test is a call to `~TestCase.assertEqual`{.interpreted-text role="meth"} to check for an expected result; `~TestCase.assertTrue`{.interpreted-text role="meth"} or `~TestCase.assertFalse`{.interpreted-text role="meth"} to verify a condition; or `~TestCase.assertRaises`{.interpreted-text role="meth"} to verify that a specific exception gets raised. These methods are used instead of the `assert`{.interpreted-text role="keyword"} statement so the test runner can accumulate all test results and produce a report.

The `~TestCase.setUp`{.interpreted-text role="meth"} and `~TestCase.tearDown`{.interpreted-text role="meth"} methods allow you to define instructions that will be executed before and after each test method. They are covered in more detail in the section `organizing-tests`{.interpreted-text role="ref"}.

The final block shows a simple way to run the tests. `unittest.main`{.interpreted-text role="func"} provides a command-line interface to the test script. When run from the command line, the above script produces an output that looks like this:

    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.000s

    OK

Passing the `-v` option to your test script will instruct `unittest.main`{.interpreted-text role="func"} to enable a higher level of verbosity, and produce the following output:

    test_isupper (__main__.TestStringMethods.test_isupper) ... ok
    test_split (__main__.TestStringMethods.test_split) ... ok
    test_upper (__main__.TestStringMethods.test_upper) ... ok

    ----------------------------------------------------------------------
    Ran 3 tests in 0.001s

    OK

The above examples show the most commonly used `!unittest`{.interpreted-text role="mod"} features which are sufficient to meet many everyday testing needs. The remainder of the documentation explores the full feature set from first principles.

::: versionchanged
3.11 The behavior of returning a value from a test method (other than the default `None` value), is now deprecated.
:::

## Command-Line Interface {#unittest-command-line-interface}

The unittest module can be used from the command line to run tests from modules, classes or even individual test methods:

    python -m unittest test_module1 test_module2
    python -m unittest test_module.TestClass
    python -m unittest test_module.TestClass.test_method

You can pass in a list with any combination of module names, and fully qualified class or method names.

Test modules can be specified by file path as well:

    python -m unittest tests/test_something.py

This allows you to use the shell filename completion to specify the test module. The file specified must still be importable as a module. The path is converted to a module name by removing the \'.py\' and converting path separators into \'.\'. If you want to execute a test file that isn\'t importable as a module you should execute the file directly instead.

You can run tests with more detail (higher verbosity) by passing in the -v flag:

    python -m unittest -v test_module

When executed without arguments `unittest-test-discovery`{.interpreted-text role="ref"} is started:

    python -m unittest

For a list of all the command-line options:

    python -m unittest -h

::: versionchanged
3.2 In earlier versions it was only possible to run individual test methods and not modules or classes.
:::

::: versionadded
3.14 Output is colorized by default and can be `controlled using environment variables <using-on-controlling-color>`{.interpreted-text role="ref"}.
:::

### Command-line options

`unittest`{.interpreted-text role="program"} supports these command-line options:

::: program
unittest
:::

::: option

`-b, --buffer`

:   

The standard output and standard error streams are buffered during the test run. Output during a passing test is discarded. Output is echoed normally on test fail or error and is added to the failure messages.
:::

::: option

`-c, --catch`

:   

`Control-C`{.interpreted-text role="kbd"} during the test run waits for the current test to end and then reports all the results so far. A second `Control-C`{.interpreted-text role="kbd"} raises the normal `KeyboardInterrupt`{.interpreted-text role="exc"} exception.

See [Signal Handling](#signal-handling) for the functions that provide this functionality.
:::

::: option

`-f, --failfast`

:   

Stop the test run on the first error or failure.
:::

::: option

`-k`

:   

Only run test methods and classes that match the pattern or substring. This option may be used multiple times, in which case all test cases that match any of the given patterns are included.

Patterns that contain a wildcard character (`*`) are matched against the test name using `fnmatch.fnmatchcase`{.interpreted-text role="meth"}; otherwise simple case-sensitive substring matching is used.

Patterns are matched against the fully qualified test method name as imported by the test loader.

For example, `-k foo` matches `foo_tests.SomeTest.test_something`, `bar_tests.SomeTest.test_foo`, but not `bar_tests.FooTest.test_something`.
:::

::: option

`--locals`

:   

Show local variables in tracebacks.
:::

::: option

`--durations N`

:   

Show the N slowest test cases (N=0 for all).
:::

::: versionadded
3.2 The command-line options `-b`, `-c` and `-f` were added.
:::

::: versionadded
3.5 The command-line option `--locals`.
:::

::: versionadded
3.7 The command-line option `-k`.
:::

::: versionadded
3.12 The command-line option `--durations`.
:::

The command line can also be used for test discovery, for running all of the tests in a project or just a subset.

## Test Discovery {#unittest-test-discovery}

::: versionadded
3.2
:::

Unittest supports simple test discovery. In order to be compatible with test discovery, all of the test files must be `modules <tut-modules>`{.interpreted-text role="ref"} or `packages <tut-packages>`{.interpreted-text role="ref"} importable from the top-level directory of the project (this means that their filenames must be valid `identifiers
<identifiers>`{.interpreted-text role="ref"}).

Test discovery is implemented in `TestLoader.discover`{.interpreted-text role="meth"}, but can also be used from the command line. The basic command-line usage is:

    cd project_directory
    python -m unittest discover

:::: note
::: title
Note
:::

As a shortcut, `python -m unittest` is the equivalent of `python -m unittest discover`. If you want to pass arguments to test discovery the `discover` sub-command must be used explicitly.
::::

The `discover` sub-command has the following options:

::: program
unittest discover
:::

::: option

`-v, --verbose`

:   

Verbose output
:::

::: option

`-s, --start-directory directory`

:   

Directory to start discovery (`.` default)
:::

::: option

`-p, --pattern pattern`

:   

Pattern to match test files (`test*.py` default)
:::

::: option

`-t, --top-level-directory directory`

:   

Top level directory of project (defaults to start directory)
:::

The `-s`{.interpreted-text role="option"}, `-p`{.interpreted-text role="option"}, and `-t`{.interpreted-text role="option"} options can be passed in as positional arguments in that order. The following two command lines are equivalent:

    python -m unittest discover -s project_directory -p "*_test.py"
    python -m unittest discover project_directory "*_test.py"

As well as being a path it is possible to pass a package name, for example `myproject.subpackage.test`, as the start directory. The package name you supply will then be imported and its location on the filesystem will be used as the start directory.

:::: caution
::: title
Caution
:::

Test discovery loads tests by importing them. Once test discovery has found all the test files from the start directory you specify it turns the paths into package names to import. For example `foo/bar/baz.py`{.interpreted-text role="file"} will be imported as `foo.bar.baz`.

If you have a package installed globally and attempt test discovery on a different copy of the package then the import *could* happen from the wrong place. If this happens test discovery will warn you and exit.

If you supply the start directory as a package name rather than a path to a directory then discover assumes that whichever location it imports from is the location you intended, so you will not get the warning.
::::

Test modules and packages can customize test loading and discovery by through the [load_tests protocol](#load_tests-protocol).

::: versionchanged
3.4 Test discovery supports `namespace packages <namespace package>`{.interpreted-text role="term"}.
:::

::: versionchanged
3.11 Test discovery dropped the `namespace packages <namespace package>`{.interpreted-text role="term"} support. It has been broken since Python 3.7. Start directory and its subdirectories containing tests must be regular package that have `__init__.py` file.

If the start directory is the dotted name of the package, the ancestor packages can be namespace packages.
:::

::: versionchanged
3.14 Test discovery supports `namespace package`{.interpreted-text role="term"} as start directory again. To avoid scanning directories unrelated to Python, tests are not searched in subdirectories that do not contain `__init__.py`.
:::

## Organizing test code {#organizing-tests}

The basic building blocks of unit testing are `test cases`{.interpreted-text role="dfn"} \-\-- single scenarios that must be set up and checked for correctness. In `!unittest`{.interpreted-text role="mod"}, test cases are represented by `unittest.TestCase`{.interpreted-text role="class"} instances. To make your own test cases you must write subclasses of `TestCase`{.interpreted-text role="class"} or use `FunctionTestCase`{.interpreted-text role="class"}.

The testing code of a `TestCase`{.interpreted-text role="class"} instance should be entirely self contained, such that it can be run either in isolation or in arbitrary combination with any number of other test cases.

The simplest `TestCase`{.interpreted-text role="class"} subclass will simply implement a test method (i.e. a method whose name starts with `test`) in order to perform specific testing code:

    import unittest

    class DefaultWidgetSizeTestCase(unittest.TestCase):
        def test_default_widget_size(self):
            widget = Widget('The widget')
            self.assertEqual(widget.size(), (50, 50))

Note that in order to test something, we use one of the `assert\* methods <assert-methods>`{.interpreted-text role="ref"} provided by the `TestCase`{.interpreted-text role="class"} base class. If the test fails, an exception will be raised with an explanatory message, and `!unittest`{.interpreted-text role="mod"} will identify the test case as a `failure`{.interpreted-text role="dfn"}. Any other exceptions will be treated as `errors`{.interpreted-text role="dfn"}.

Tests can be numerous, and their set-up can be repetitive. Luckily, we can factor out set-up code by implementing a method called `~TestCase.setUp`{.interpreted-text role="meth"}, which the testing framework will automatically call for every single test we run:

    import unittest

    class WidgetTestCase(unittest.TestCase):
        def setUp(self):
            self.widget = Widget('The widget')

        def test_default_widget_size(self):
            self.assertEqual(self.widget.size(), (50,50),
                             'incorrect default size')

        def test_widget_resize(self):
            self.widget.resize(100,150)
            self.assertEqual(self.widget.size(), (100,150),
                             'wrong size after resize')

:::: note
::: title
Note
:::

The order in which the various tests will be run is determined by sorting the test method names with respect to the built-in ordering for strings.
::::

If the `~TestCase.setUp`{.interpreted-text role="meth"} method raises an exception while the test is running, the framework will consider the test to have suffered an error, and the test method will not be executed.

Similarly, we can provide a `~TestCase.tearDown`{.interpreted-text role="meth"} method that tidies up after the test method has been run:

    import unittest

    class WidgetTestCase(unittest.TestCase):
        def setUp(self):
            self.widget = Widget('The widget')

        def tearDown(self):
            self.widget.dispose()

If `~TestCase.setUp`{.interpreted-text role="meth"} succeeded, `~TestCase.tearDown`{.interpreted-text role="meth"} will be run whether the test method succeeded or not.

Such a working environment for the testing code is called a `test fixture`{.interpreted-text role="dfn"}. A new TestCase instance is created as a unique test fixture used to execute each individual test method. Thus `~TestCase.setUp`{.interpreted-text role="meth"}, `~TestCase.tearDown`{.interpreted-text role="meth"}, and `!TestCase.__init__`{.interpreted-text role="meth"} will be called once per test.

It is recommended that you use TestCase implementations to group tests together according to the features they test. `!unittest`{.interpreted-text role="mod"} provides a mechanism for this: the `test suite`{.interpreted-text role="dfn"}, represented by `!unittest`{.interpreted-text role="mod"}\'s `TestSuite`{.interpreted-text role="class"} class. In most cases, calling `unittest.main`{.interpreted-text role="func"} will do the right thing and collect all the module\'s test cases for you and execute them.

However, should you want to customize the building of your test suite, you can do it yourself:

    def suite():
        suite = unittest.TestSuite()
        suite.addTest(WidgetTestCase('test_default_widget_size'))
        suite.addTest(WidgetTestCase('test_widget_resize'))
        return suite

    if __name__ == '__main__':
        runner = unittest.TextTestRunner()
        runner.run(suite())

You can place the definitions of test cases and test suites in the same modules as the code they are to test (such as `widget.py`{.interpreted-text role="file"}), but there are several advantages to placing the test code in a separate module, such as `test_widget.py`{.interpreted-text role="file"}:

- The test module can be run standalone from the command line.
- The test code can more easily be separated from shipped code.
- There is less temptation to change test code to fit the code it tests without a good reason.
- Test code should be modified much less frequently than the code it tests.
- Tested code can be refactored more easily.
- Tests for modules written in C must be in separate modules anyway, so why not be consistent?
- If the testing strategy changes, there is no need to change the source code.

## Re-using old test code {#legacy-unit-tests}

Some users will find that they have existing test code that they would like to run from `!unittest`{.interpreted-text role="mod"}, without converting every old test function to a `TestCase`{.interpreted-text role="class"} subclass.

For this reason, `!unittest`{.interpreted-text role="mod"} provides a `FunctionTestCase`{.interpreted-text role="class"} class. This subclass of `TestCase`{.interpreted-text role="class"} can be used to wrap an existing test function. Set-up and tear-down functions can also be provided.

Given the following test function:

    def testSomething():
        something = makeSomething()
        assert something.name is not None
        # ...

one can create an equivalent test case instance as follows, with optional set-up and tear-down methods:

    testcase = unittest.FunctionTestCase(testSomething,
                                         setUp=makeSomethingDB,
                                         tearDown=deleteSomethingDB)

:::: note
::: title
Note
:::

Even though `FunctionTestCase`{.interpreted-text role="class"} can be used to quickly convert an existing test base over to a `!unittest`{.interpreted-text role="mod"}-based system, this approach is not recommended. Taking the time to set up proper `TestCase`{.interpreted-text role="class"} subclasses will make future test refactorings infinitely easier.
::::

In some cases, the existing tests may have been written using the `doctest`{.interpreted-text role="mod"} module. If so, `doctest`{.interpreted-text role="mod"} provides a `~doctest.DocTestSuite`{.interpreted-text role="class"} class that can automatically build `unittest.TestSuite`{.interpreted-text role="class"} instances from the existing `doctest`{.interpreted-text role="mod"}-based tests.

## Skipping tests and expected failures {#unittest-skipping}

::: versionadded
3.1
:::

Unittest supports skipping individual test methods and even whole classes of tests. In addition, it supports marking a test as an \"expected failure,\" a test that is broken and will fail, but shouldn\'t be counted as a failure on a `TestResult`{.interpreted-text role="class"}.

Skipping a test is simply a matter of using the `skip`{.interpreted-text role="func"} `decorator`{.interpreted-text role="term"} or one of its conditional variants, calling `TestCase.skipTest`{.interpreted-text role="meth"} within a `~TestCase.setUp`{.interpreted-text role="meth"} or test method, or raising `SkipTest`{.interpreted-text role="exc"} directly.

Basic skipping looks like this:

    class MyTestCase(unittest.TestCase):

        @unittest.skip("demonstrating skipping")
        def test_nothing(self):
            self.fail("shouldn't happen")

        @unittest.skipIf(mylib.__version__ < (1, 3),
                         "not supported in this library version")
        def test_format(self):
            # Tests that work for only a certain version of the library.
            pass

        @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
        def test_windows_support(self):
            # windows specific testing code
            pass

        def test_maybe_skipped(self):
            if not external_resource_available():
                self.skipTest("external resource not available")
            # test code that depends on the external resource
            pass

This is the output of running the example above in verbose mode:

    test_format (__main__.MyTestCase.test_format) ... skipped 'not supported in this library version'
    test_nothing (__main__.MyTestCase.test_nothing) ... skipped 'demonstrating skipping'
    test_maybe_skipped (__main__.MyTestCase.test_maybe_skipped) ... skipped 'external resource not available'
    test_windows_support (__main__.MyTestCase.test_windows_support) ... skipped 'requires Windows'

    ----------------------------------------------------------------------
    Ran 4 tests in 0.005s

    OK (skipped=4)

Classes can be skipped just like methods:

    @unittest.skip("showing class skipping")
    class MySkippedTestCase(unittest.TestCase):
        def test_not_run(self):
            pass

`TestCase.setUp`{.interpreted-text role="meth"} can also skip the test. This is useful when a resource that needs to be set up is not available.

Expected failures use the `expectedFailure`{.interpreted-text role="func"} decorator. :

    class ExpectedFailureTestCase(unittest.TestCase):
        @unittest.expectedFailure
        def test_fail(self):
            self.assertEqual(1, 0, "broken")

It\'s easy to roll your own skipping decorators by making a decorator that calls `skip`{.interpreted-text role="func"} on the test when it wants it to be skipped. This decorator skips the test unless the passed object has a certain attribute:

    def skipUnlessHasattr(obj, attr):
        if hasattr(obj, attr):
            return lambda func: func
        return unittest.skip("{!r} doesn't have {!r}".format(obj, attr))

The following decorators and exception implement test skipping and expected failures:

::: decorator
skip(reason)

Unconditionally skip the decorated test. *reason* should describe why the test is being skipped.
:::

::: decorator
skipIf(condition, reason)

Skip the decorated test if *condition* is true.
:::

::: decorator
skipUnless(condition, reason)

Skip the decorated test unless *condition* is true.
:::

::: decorator
expectedFailure

Mark the test as an expected failure or error. If the test fails or errors in the test function itself (rather than in one of the `test fixture`{.interpreted-text role="dfn"} methods) then it will be considered a success. If the test passes, it will be considered a failure.
:::

::: exception
SkipTest(reason)

This exception is raised to skip a test.

Usually you can use `TestCase.skipTest`{.interpreted-text role="meth"} or one of the skipping decorators instead of raising this directly.
:::

Skipped tests will not have `~TestCase.setUp`{.interpreted-text role="meth"} or `~TestCase.tearDown`{.interpreted-text role="meth"} run around them. Skipped classes will not have `~TestCase.setUpClass`{.interpreted-text role="meth"} or `~TestCase.tearDownClass`{.interpreted-text role="meth"} run. Skipped modules will not have `setUpModule`{.interpreted-text role="func"} or `tearDownModule`{.interpreted-text role="func"} run.

## Distinguishing test iterations using subtests {#subtests}

::: versionadded
3.4
:::

When there are very small differences among your tests, for instance some parameters, unittest allows you to distinguish them inside the body of a test method using the `~TestCase.subTest`{.interpreted-text role="meth"} context manager.

For example, the following test:

    class NumbersTest(unittest.TestCase):

        def test_even(self):
            """
            Test that numbers between 0 and 5 are all even.
            """
            for i in range(0, 6):
                with self.subTest(i=i):
                    self.assertEqual(i % 2, 0)

will produce the following output:

    ======================================================================
    FAIL: test_even (__main__.NumbersTest.test_even) (i=1)
    Test that numbers between 0 and 5 are all even.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "subtests.py", line 11, in test_even
        self.assertEqual(i % 2, 0)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError: 1 != 0

    ======================================================================
    FAIL: test_even (__main__.NumbersTest.test_even) (i=3)
    Test that numbers between 0 and 5 are all even.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "subtests.py", line 11, in test_even
        self.assertEqual(i % 2, 0)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError: 1 != 0

    ======================================================================
    FAIL: test_even (__main__.NumbersTest.test_even) (i=5)
    Test that numbers between 0 and 5 are all even.
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "subtests.py", line 11, in test_even
        self.assertEqual(i % 2, 0)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError: 1 != 0

Without using a subtest, execution would stop after the first failure, and the error would be less easy to diagnose because the value of `i` wouldn\'t be displayed:

    ======================================================================
    FAIL: test_even (__main__.NumbersTest.test_even)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "subtests.py", line 32, in test_even
        self.assertEqual(i % 2, 0)
    AssertionError: 1 != 0

## Classes and functions {#unittest-contents}

This section describes in depth the API of `!unittest`{.interpreted-text role="mod"}.

### Test cases {#testcase-objects}

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: TestCase(methodName='runTest')
Instances of the `TestCase`{.interpreted-text role="class"} class represent the logical test units in the `!unittest`{.interpreted-text role="mod"} universe. This class is intended to be used as a base class, with specific tests being implemented by concrete subclasses. This class implements the interface needed by the test runner to allow it to drive the tests, and methods that the test code can use to check for and report various kinds of failure.

Each instance of `TestCase`{.interpreted-text role="class"} will run a single base method: the method named *methodName*. In most uses of `TestCase`{.interpreted-text role="class"}, you will neither change the *methodName* nor reimplement the default `runTest()` method.

::: versionchanged
3.2 `TestCase`{.interpreted-text role="class"} can be instantiated successfully without providing a *methodName*. This makes it easier to experiment with `TestCase`{.interpreted-text role="class"} from the interactive interpreter.
:::

`TestCase`{.interpreted-text role="class"} instances provide three groups of methods: one group used to run the test, another used by the test implementation to check conditions and report failures, and some inquiry methods allowing information about the test itself to be gathered.

Methods in the first group (running the test) are:

::: method
setUp()

Method called to prepare the test fixture. This is called immediately before calling the test method; other than `AssertionError`{.interpreted-text role="exc"} or `SkipTest`{.interpreted-text role="exc"}, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
:::

::: method
tearDown()

Method called immediately after the test method has been called and the result recorded. This is called even if the test method raised an exception, so the implementation in subclasses may need to be particularly careful about checking internal state. Any exception, other than `AssertionError`{.interpreted-text role="exc"} or `SkipTest`{.interpreted-text role="exc"}, raised by this method will be considered an additional error rather than a test failure (thus increasing the total number of reported errors). This method will only be called if the `setUp`{.interpreted-text role="meth"} succeeds, regardless of the outcome of the test method. The default implementation does nothing.
:::

:::: method
setUpClass()

A class method called before tests in an individual class are run. `setUpClass` is called with the class as the only argument and must be decorated as a `classmethod`{.interpreted-text role="func"}:

    @classmethod
    def setUpClass(cls):
        ...

See [Class and Module Fixtures](#class-and-module-fixtures) for more details.

::: versionadded
3.2
:::
::::

:::: method
tearDownClass()

A class method called after tests in an individual class have run. `tearDownClass` is called with the class as the only argument and must be decorated as a `classmethod`{.interpreted-text role="meth"}:

    @classmethod
    def tearDownClass(cls):
        ...

See [Class and Module Fixtures](#class-and-module-fixtures) for more details.

::: versionadded
3.2
:::
::::

:::: method
run(result=None)

Run the test, collecting the result into the `TestResult`{.interpreted-text role="class"} object passed as *result*. If *result* is omitted or `None`, a temporary result object is created (by calling the `defaultTestResult`{.interpreted-text role="meth"} method) and used. The result object is returned to `run`{.interpreted-text role="meth"}\'s caller.

The same effect may be had by simply calling the `TestCase`{.interpreted-text role="class"} instance.

::: versionchanged
3.3 Previous versions of `run` did not return the result. Neither did calling an instance.
:::
::::

:::: method
skipTest(reason)

Calling this during a test method or `setUp`{.interpreted-text role="meth"} skips the current test. See `unittest-skipping`{.interpreted-text role="ref"} for more information.

::: versionadded
3.1
:::
::::

:::: method
subTest(msg=None, \*\*params)

Return a context manager which executes the enclosed code block as a subtest. *msg* and *params* are optional, arbitrary values which are displayed whenever a subtest fails, allowing you to identify them clearly.

A test case can contain any number of subtest declarations, and they can be arbitrarily nested.

See `subtests`{.interpreted-text role="ref"} for more information.

::: versionadded
3.4
:::
::::

::: method
debug()

Run the test without collecting the result. This allows exceptions raised by the test to be propagated to the caller, and can be used to support running tests under a debugger.
:::

::: {#assert-methods}
The `TestCase`{.interpreted-text role="class"} class provides several assert methods to check for and report failures. The following table lists the most commonly used methods (see the tables below for more assert methods):
:::

  ------------------------------------------------------------------------------------------------------
  Method                                                           Checks that              New in
  ---------------------------------------------------------------- ------------------------ ------------
  `assertEqual(a, b)                                               `a == b`                 
  <TestCase.assertEqual>`{.interpreted-text role="meth"}                                    

  `assertNotEqual(a, b)                                            `a != b`                 
  <TestCase.assertNotEqual>`{.interpreted-text role="meth"}                                 

  `assertTrue(x)                                                   `bool(x) is True`        
  <TestCase.assertTrue>`{.interpreted-text role="meth"}                                     

  `assertFalse(x)                                                  `bool(x) is False`       
  <TestCase.assertFalse>`{.interpreted-text role="meth"}                                    

  `assertIs(a, b)                                                  `a is b`                 3.1
  <TestCase.assertIs>`{.interpreted-text role="meth"}                                       

  `assertIsNot(a, b)                                               `a is not b`             3.1
  <TestCase.assertIsNot>`{.interpreted-text role="meth"}                                    

  `assertIsNone(x)                                                 `x is None`              3.1
  <TestCase.assertIsNone>`{.interpreted-text role="meth"}                                   

  `assertIsNotNone(x)                                              `x is not None`          3.1
  <TestCase.assertIsNotNone>`{.interpreted-text role="meth"}                                

  `assertIn(a, b)                                                  `a in b`                 3.1
  <TestCase.assertIn>`{.interpreted-text role="meth"}                                       

  `assertNotIn(a, b)                                               `a not in b`             3.1
  <TestCase.assertNotIn>`{.interpreted-text role="meth"}                                    

  `assertIsInstance(a, b)                                          `isinstance(a, b)`       3.2
  <TestCase.assertIsInstance>`{.interpreted-text role="meth"}                               

  `assertNotIsInstance(a, b)                                       `not isinstance(a, b)`   3.2
  <TestCase.assertNotIsInstance>`{.interpreted-text role="meth"}                            

  `assertIsSubclass(a, b)                                          `issubclass(a, b)`       3.14
  <TestCase.assertIsSubclass>`{.interpreted-text role="meth"}                               

  `assertNotIsSubclass(a, b)                                       `not issubclass(a, b)`   3.14
  <TestCase.assertNotIsSubclass>`{.interpreted-text role="meth"}                            
  ------------------------------------------------------------------------------------------------------

All the assert methods accept a *msg* argument that, if specified, is used as the error message on failure (see also `longMessage`{.interpreted-text role="data"}). Note that the *msg* keyword argument can be passed to `assertRaises`{.interpreted-text role="meth"}, `assertRaisesRegex`{.interpreted-text role="meth"}, `assertWarns`{.interpreted-text role="meth"}, `assertWarnsRegex`{.interpreted-text role="meth"} only when they are used as a context manager.

::::: method
assertEqual(first, second, msg=None)

Test that *first* and *second* are equal. If the values do not compare equal, the test will fail.

In addition, if *first* and *second* are the exact same type and one of list, tuple, dict, set, frozenset or str or any type that a subclass registers with `addTypeEqualityFunc`{.interpreted-text role="meth"} the type-specific equality function will be called in order to generate a more useful default error message (see also the `list of type-specific methods
<type-specific-methods>`{.interpreted-text role="ref"}).

::: versionchanged
3.1 Added the automatic calling of type-specific equality function.
:::

::: versionchanged
3.2 `assertMultiLineEqual`{.interpreted-text role="meth"} added as the default type equality function for comparing strings.
:::
:::::

::: method
assertNotEqual(first, second, msg=None)

Test that *first* and *second* are not equal. If the values do compare equal, the test will fail.
:::

::: method
assertTrue(expr, msg=None) assertFalse(expr, msg=None)

Test that *expr* is true (or false).

Note that this is equivalent to `bool(expr) is True` and not to `expr is True` (use `assertIs(expr, True)` for the latter). This method should also be avoided when more specific methods are available (e.g. `assertEqual(a, b)` instead of `assertTrue(a == b)`), because they provide a better error message in case of failure.
:::

:::: method
assertIs(first, second, msg=None) assertIsNot(first, second, msg=None)

Test that *first* and *second* are (or are not) the same object.

::: versionadded
3.1
:::
::::

:::: method
assertIsNone(expr, msg=None) assertIsNotNone(expr, msg=None)

Test that *expr* is (or is not) `None`.

::: versionadded
3.1
:::
::::

:::: method
assertIn(member, container, msg=None) assertNotIn(member, container, msg=None)

Test that *member* is (or is not) in *container*.

::: versionadded
3.1
:::
::::

:::: method
assertIsInstance(obj, cls, msg=None) assertNotIsInstance(obj, cls, msg=None)

Test that *obj* is (or is not) an instance of *cls* (which can be a class or a tuple of classes, as supported by `isinstance`{.interpreted-text role="func"}). To check for the exact type, use `assertIs(type(obj), cls) <assertIs>`{.interpreted-text role="func"}.

::: versionadded
3.2
:::
::::

:::: method
assertIsSubclass(cls, superclass, msg=None) assertNotIsSubclass(cls, superclass, msg=None)

Test that *cls* is (or is not) a subclass of *superclass* (which can be a class or a tuple of classes, as supported by `issubclass`{.interpreted-text role="func"}). To check for the exact type, use `assertIs(cls, superclass) <assertIs>`{.interpreted-text role="func"}.

::: versionadded
3.14
:::
::::

It is also possible to check the production of exceptions, warnings, and log messages using the following methods:

+--------------------------------------------------------------+----------------------------------------------------------------------+--------+
| Method                                                       | Checks that                                                          | New in |
+==============================================================+======================================================================+========+
| `assertRaises(exc, fun, *args, **kwds)                       | `fun(*args, **kwds)` raises *exc*                                    |        |
| <TestCase.assertRaises>`{.interpreted-text role="meth"}      |                                                                      |        |
+--------------------------------------------------------------+----------------------------------------------------------------------+--------+
| `assertRaisesRegex(exc, r, fun, *args, **kwds)               | `fun(*args, **kwds)` raises *exc* and the message matches regex *r*  | 3.1    |
| <TestCase.assertRaisesRegex>`{.interpreted-text role="meth"} |                                                                      |        |
+--------------------------------------------------------------+----------------------------------------------------------------------+--------+
| `assertWarns(warn, fun, *args, **kwds)                       | `fun(*args, **kwds)` raises *warn*                                   | 3.2    |
| <TestCase.assertWarns>`{.interpreted-text role="meth"}       |                                                                      |        |
+--------------------------------------------------------------+----------------------------------------------------------------------+--------+
| `assertWarnsRegex(warn, r, fun, *args, **kwds)               | `fun(*args, **kwds)` raises *warn* and the message matches regex *r* | 3.2    |
| <TestCase.assertWarnsRegex>`{.interpreted-text role="meth"}  |                                                                      |        |
+--------------------------------------------------------------+----------------------------------------------------------------------+--------+
| `assertLogs(logger, level)                                   | The `with` block logs on *logger* with minimum *level*               | 3.4    |
| <TestCase.assertLogs>`{.interpreted-text role="meth"}        |                                                                      |        |
+--------------------------------------------------------------+----------------------------------------------------------------------+--------+
| `assertNoLogs(logger, level)                                 | The `with` block does not log on                                     | 3.10   |
| <TestCase.assertNoLogs>`{.interpreted-text role="meth"}      |                                                                      |        |
|                                                              | :   *logger* with minimum *level*                                    |        |
+--------------------------------------------------------------+----------------------------------------------------------------------+--------+

:::::: method
assertRaises(exception, callable, *args,kwds) assertRaises(exception,*, msg=None)

Test that an exception is raised when *callable* is called with any positional or keyword arguments that are also passed to `assertRaises`{.interpreted-text role="meth"}. The test passes if *exception* is raised, is an error if another exception is raised, or fails if no exception is raised. To catch any of a group of exceptions, a tuple containing the exception classes may be passed as *exception*.

If only the *exception* and possibly the *msg* arguments are given, return a context manager so that the code under test can be written inline rather than as a function:

    with self.assertRaises(SomeException):
        do_something()

When used as a context manager, `assertRaises`{.interpreted-text role="meth"} accepts the additional keyword argument *msg*.

The context manager will store the caught exception object in its `!exception`{.interpreted-text role="attr"} attribute. This can be useful if the intention is to perform additional checks on the exception raised:

    with self.assertRaises(SomeException) as cm:
        do_something()

    the_exception = cm.exception
    self.assertEqual(the_exception.error_code, 3)

::: versionchanged
3.1 Added the ability to use `assertRaises`{.interpreted-text role="meth"} as a context manager.
:::

::: versionchanged
3.2 Added the `!exception`{.interpreted-text role="attr"} attribute.
:::

::: versionchanged
3.3 Added the *msg* keyword argument when used as a context manager.
:::
::::::

:::::: method
assertRaisesRegex(exception, regex, callable, *args,kwds) assertRaisesRegex(exception, regex,*, msg=None)

Like `assertRaises`{.interpreted-text role="meth"} but also tests that *regex* matches on the string representation of the raised exception. *regex* may be a regular expression object or a string containing a regular expression suitable for use by `re.search`{.interpreted-text role="func"}. Examples:

    self.assertRaisesRegex(ValueError, "invalid literal for.*XYZ'$",
                           int, 'XYZ')

or:

    with self.assertRaisesRegex(ValueError, 'literal'):
       int('XYZ')

::: versionadded
3.1 Added under the name `assertRaisesRegexp`.
:::

::: versionchanged
3.2 Renamed to `assertRaisesRegex`{.interpreted-text role="meth"}.
:::

::: versionchanged
3.3 Added the *msg* keyword argument when used as a context manager.
:::
::::::

::::: method
assertWarns(warning, callable, *args,kwds) assertWarns(warning,*, msg=None)

Test that a warning is triggered when *callable* is called with any positional or keyword arguments that are also passed to `assertWarns`{.interpreted-text role="meth"}. The test passes if *warning* is triggered and fails if it isn\'t. Any exception is an error. To catch any of a group of warnings, a tuple containing the warning classes may be passed as *warnings*.

If only the *warning* and possibly the *msg* arguments are given, return a context manager so that the code under test can be written inline rather than as a function:

    with self.assertWarns(SomeWarning):
        do_something()

When used as a context manager, `assertWarns`{.interpreted-text role="meth"} accepts the additional keyword argument *msg*.

The context manager will store the caught warning object in its `!warning`{.interpreted-text role="attr"} attribute, and the source line which triggered the warnings in the `!filename`{.interpreted-text role="attr"} and `!lineno`{.interpreted-text role="attr"} attributes. This can be useful if the intention is to perform additional checks on the warning caught:

    with self.assertWarns(SomeWarning) as cm:
        do_something()

    self.assertIn('myfile.py', cm.filename)
    self.assertEqual(320, cm.lineno)

This method works regardless of the warning filters in place when it is called.

::: versionadded
3.2
:::

::: versionchanged
3.3 Added the *msg* keyword argument when used as a context manager.
:::
:::::

::::: method
assertWarnsRegex(warning, regex, callable, *args,kwds) assertWarnsRegex(warning, regex,*, msg=None)

Like `assertWarns`{.interpreted-text role="meth"} but also tests that *regex* matches on the message of the triggered warning. *regex* may be a regular expression object or a string containing a regular expression suitable for use by `re.search`{.interpreted-text role="func"}. Example:

    self.assertWarnsRegex(DeprecationWarning,
                          r'legacy_function\(\) is deprecated',
                          legacy_function, 'XYZ')

or:

    with self.assertWarnsRegex(RuntimeWarning, 'unsafe frobnicating'):
        frobnicate('/etc/passwd')

::: versionadded
3.2
:::

::: versionchanged
3.3 Added the *msg* keyword argument when used as a context manager.
:::
:::::

::::::: method
assertLogs(logger=None, level=None, formatter=None)

A context manager to test that at least one message is logged on the *logger* or one of its children, with at least the given *level*.

If given, *logger* should be a `logging.Logger`{.interpreted-text role="class"} object or a `str`{.interpreted-text role="class"} giving the name of a logger. The default is the root logger, which will catch all messages that were not blocked by a non-propagating descendent logger.

If given, *level* should be either a numeric logging level or its string equivalent (for example either `"ERROR"` or `logging.ERROR`{.interpreted-text role="const"}). The default is `logging.INFO`{.interpreted-text role="const"}.

If given, *formatter* should be a `logging.Formatter`{.interpreted-text role="class"} object. The default is a formatter with format string `"%(levelname)s:%(name)s:%(message)s"`

The test passes if at least one message emitted inside the `with` block matches the *logger* and *level* conditions, otherwise it fails.

The object returned by the context manager is a recording helper which keeps tracks of the matching log messages. It has two attributes:

::: attribute
records

A list of `logging.LogRecord`{.interpreted-text role="class"} objects of the matching log messages.
:::

::: attribute
output

A list of `str`{.interpreted-text role="class"} objects with the formatted output of matching messages.
:::

Example:

    with self.assertLogs('foo', level='INFO') as cm:
        logging.getLogger('foo').info('first message')
        logging.getLogger('foo.bar').error('second message')
    self.assertEqual(cm.output, ['INFO:foo:first message',
                                 'ERROR:foo.bar:second message'])

::: versionadded
3.4
:::

::: versionchanged
3.15 Now accepts a *formatter* to control how messages are formatted.
:::
:::::::

:::: method
assertNoLogs(logger=None, level=None)

A context manager to test that no messages are logged on the *logger* or one of its children, with at least the given *level*.

If given, *logger* should be a `logging.Logger`{.interpreted-text role="class"} object or a `str`{.interpreted-text role="class"} giving the name of a logger. The default is the root logger, which will catch all messages.

If given, *level* should be either a numeric logging level or its string equivalent (for example either `"ERROR"` or `logging.ERROR`{.interpreted-text role="const"}). The default is `logging.INFO`{.interpreted-text role="const"}.

Unlike `assertLogs`{.interpreted-text role="meth"}, nothing will be returned by the context manager.

::: versionadded
3.10
:::
::::

There are also other methods used to perform more specific checks, such as:

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------
  Method                                                            Checks that                                                                         New in
  ----------------------------------------------------------------- ----------------------------------------------------------------------------------- -----------
  `assertAlmostEqual(a, b)                                          `round(a-b, 7) == 0`                                                                
  <TestCase.assertAlmostEqual>`{.interpreted-text role="meth"}                                                                                          

  `assertNotAlmostEqual(a, b)                                       `round(a-b, 7) != 0`                                                                
  <TestCase.assertNotAlmostEqual>`{.interpreted-text role="meth"}                                                                                       

  `assertGreater(a, b)                                              `a > b`                                                                             3.1
  <TestCase.assertGreater>`{.interpreted-text role="meth"}                                                                                              

  `assertGreaterEqual(a, b)                                         `a >= b`                                                                            3.1
  <TestCase.assertGreaterEqual>`{.interpreted-text role="meth"}                                                                                         

  `assertLess(a, b)                                                 `a < b`                                                                             3.1
  <TestCase.assertLess>`{.interpreted-text role="meth"}                                                                                                 

  `assertLessEqual(a, b)                                            `a <= b`                                                                            3.1
  <TestCase.assertLessEqual>`{.interpreted-text role="meth"}                                                                                            

  `assertRegex(s, r)                                                `r.search(s)`                                                                       3.1
  <TestCase.assertRegex>`{.interpreted-text role="meth"}                                                                                                

  `assertNotRegex(s, r)                                             `not r.search(s)`                                                                   3.2
  <TestCase.assertNotRegex>`{.interpreted-text role="meth"}                                                                                             

  `assertCountEqual(a, b)                                           *a* and *b* have the same elements in the same number, regardless of their order.   3.2
  <TestCase.assertCountEqual>`{.interpreted-text role="meth"}                                                                                           

  `assertStartsWith(a, b)                                           `a.startswith(b)`                                                                   3.14
  <TestCase.assertStartsWith>`{.interpreted-text role="meth"}                                                                                           

  `assertNotStartsWith(a, b)                                        `not a.startswith(b)`                                                               3.14
  <TestCase.assertNotStartsWith>`{.interpreted-text role="meth"}                                                                                        

  `assertEndsWith(a, b)                                             `a.endswith(b)`                                                                     3.14
  <TestCase.assertEndsWith>`{.interpreted-text role="meth"}                                                                                             

  `assertNotEndsWith(a, b)                                          `not a.endswith(b)`                                                                 3.14
  <TestCase.assertNotEndsWith>`{.interpreted-text role="meth"}                                                                                          

  `assertHasAttr(a, b)                                              `hastattr(a, b)`                                                                    3.14
  <TestCase.assertHasAttr>`{.interpreted-text role="meth"}                                                                                              

  `assertNotHasAttr(a, b)                                           `not hastattr(a, b)`                                                                3.14
  <TestCase.assertNotHasAttr>`{.interpreted-text role="meth"}                                                                                           
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------

:::: method
assertAlmostEqual(first, second, places=7, msg=None, delta=None) assertNotAlmostEqual(first, second, places=7, msg=None, delta=None)

Test that *first* and *second* are approximately (or not approximately) equal by computing the difference, rounding to the given number of decimal *places* (default 7), and comparing to zero. Note that these methods round the values to the given number of *decimal places* (i.e. like the `round`{.interpreted-text role="func"} function) and not *significant digits*.

If *delta* is supplied instead of *places* then the difference between *first* and *second* must be less or equal to (or greater than) *delta*.

Supplying both *delta* and *places* raises a `TypeError`{.interpreted-text role="exc"}.

::: versionchanged
3.2 `assertAlmostEqual`{.interpreted-text role="meth"} automatically considers almost equal objects that compare equal. `assertNotAlmostEqual`{.interpreted-text role="meth"} automatically fails if the objects compare equal. Added the *delta* keyword argument.
:::
::::

:::: method
assertGreater(first, second, msg=None) assertGreaterEqual(first, second, msg=None) assertLess(first, second, msg=None) assertLessEqual(first, second, msg=None)

Test that *first* is respectively \>, \>=, \< or \<= than *second* depending on the method name. If not, the test will fail:

    >>> self.assertGreaterEqual(3, 4)
    AssertionError: "3" unexpectedly not greater than or equal to "4"

::: versionadded
3.1
:::
::::

:::::: method
assertRegex(text, regex, msg=None) assertNotRegex(text, regex, msg=None)

Test that a *regex* search matches (or does not match) *text*. In case of failure, the error message will include the pattern and the *text* (or the pattern and the part of *text* that unexpectedly matched). *regex* may be a regular expression object or a string containing a regular expression suitable for use by `re.search`{.interpreted-text role="func"}.

::: versionadded
3.1 Added under the name `assertRegexpMatches`.
:::

::: versionchanged
3.2 The method `assertRegexpMatches()` has been renamed to `.assertRegex`{.interpreted-text role="meth"}.
:::

::: versionadded
3.2 `.assertNotRegex`{.interpreted-text role="meth"}.
:::
::::::

:::: method
assertCountEqual(first, second, msg=None)

Test that sequence *first* contains the same elements as *second*, regardless of their order. When they don\'t, an error message listing the differences between the sequences will be generated.

Duplicate elements are *not* ignored when comparing *first* and *second*. It verifies whether each element has the same count in both sequences. Equivalent to: `assertEqual(Counter(list(first)), Counter(list(second)))` but works with sequences of unhashable objects as well.

::: versionadded
3.2
:::
::::

::: method
assertStartsWith(s, prefix, msg=None)
:::

:::: method
assertNotStartsWith(s, prefix, msg=None)

Test that the Unicode or byte string *s* starts (or does not start) with a *prefix*. *prefix* can also be a tuple of strings to try.

::: versionadded
3.14
:::
::::

::: method
assertEndsWith(s, suffix, msg=None)
:::

:::: method
assertNotEndsWith(s, suffix, msg=None)

Test that the Unicode or byte string *s* ends (or does not end) with a *suffix*. *suffix* can also be a tuple of strings to try.

::: versionadded
3.14
:::
::::

::: method
assertHasAttr(obj, name, msg=None)
:::

:::: method
assertNotHasAttr(obj, name, msg=None)

Test that the object *obj* has (or has not) an attribute *name*.

::: versionadded
3.14
:::
::::

::: {#type-specific-methods}
The `assertEqual`{.interpreted-text role="meth"} method dispatches the equality check for objects of the same type to different type-specific methods. These methods are already implemented for most of the built-in types, but it\'s also possible to register new methods using `addTypeEqualityFunc`{.interpreted-text role="meth"}:
:::

:::: method
addTypeEqualityFunc(typeobj, function)

Registers a type-specific method called by `assertEqual`{.interpreted-text role="meth"} to check if two objects of exactly the same *typeobj* (not subclasses) compare equal. *function* must take two positional arguments and a third msg=None keyword argument just as `assertEqual`{.interpreted-text role="meth"} does. It must raise `self.failureException(msg) <failureException>`{.interpreted-text role="data"} when inequality between the first two parameters is detected \-- possibly providing useful information and explaining the inequalities in details in the error message.

::: versionadded
3.1
:::
::::

The list of type-specific methods automatically used by `~TestCase.assertEqual`{.interpreted-text role="meth"} are summarized in the following table. Note that it\'s usually not necessary to invoke these methods directly.

  -------------------------------------------------------------------------------------------------------
  Method                                                            Used to compare          New in
  ----------------------------------------------------------------- ------------------------ ------------
  `assertMultiLineEqual(a, b)                                       strings                  3.1
  <TestCase.assertMultiLineEqual>`{.interpreted-text role="meth"}                            

  `assertSequenceEqual(a, b)                                        sequences                3.1
  <TestCase.assertSequenceEqual>`{.interpreted-text role="meth"}                             

  `assertListEqual(a, b)                                            lists                    3.1
  <TestCase.assertListEqual>`{.interpreted-text role="meth"}                                 

  `assertTupleEqual(a, b)                                           tuples                   3.1
  <TestCase.assertTupleEqual>`{.interpreted-text role="meth"}                                

  `assertSetEqual(a, b)                                             sets or frozensets       3.1
  <TestCase.assertSetEqual>`{.interpreted-text role="meth"}                                  

  `assertDictEqual(a, b)                                            dicts                    3.1
  <TestCase.assertDictEqual>`{.interpreted-text role="meth"}                                 
  -------------------------------------------------------------------------------------------------------

:::: method
assertMultiLineEqual(first, second, msg=None)

Test that the multiline string *first* is equal to the string *second*. When not equal a diff of the two strings highlighting the differences will be included in the error message. This method is used by default when comparing strings with `assertEqual`{.interpreted-text role="meth"}.

::: versionadded
3.1
:::
::::

:::: method
assertSequenceEqual(first, second, msg=None, seq_type=None)

Tests that two sequences are equal. If a *seq_type* is supplied, both *first* and *second* must be instances of *seq_type* or a failure will be raised. If the sequences are different an error message is constructed that shows the difference between the two.

This method is not called directly by `assertEqual`{.interpreted-text role="meth"}, but it\'s used to implement `assertListEqual`{.interpreted-text role="meth"} and `assertTupleEqual`{.interpreted-text role="meth"}.

::: versionadded
3.1
:::
::::

:::: method
assertListEqual(first, second, msg=None) assertTupleEqual(first, second, msg=None)

Tests that two lists or tuples are equal. If not, an error message is constructed that shows only the differences between the two. An error is also raised if either of the parameters are of the wrong type. These methods are used by default when comparing lists or tuples with `assertEqual`{.interpreted-text role="meth"}.

::: versionadded
3.1
:::
::::

:::: method
assertSetEqual(first, second, msg=None)

Tests that two sets are equal. If not, an error message is constructed that lists the differences between the sets. This method is used by default when comparing sets or frozensets with `assertEqual`{.interpreted-text role="meth"}.

Fails if either of *first* or *second* does not have a `~frozenset.difference`{.interpreted-text role="meth"} method.

::: versionadded
3.1
:::
::::

:::: method
assertDictEqual(first, second, msg=None)

Test that two dictionaries are equal. If not, an error message is constructed that shows the differences in the dictionaries. This method will be used by default to compare dictionaries in calls to `assertEqual`{.interpreted-text role="meth"}.

::: versionadded
3.1
:::
::::

::: {#other-methods-and-attrs}
Finally the `TestCase`{.interpreted-text role="class"} provides the following methods and attributes:
:::

::: method
fail(msg=None)

Signals a test failure unconditionally, with *msg* or `None` for the error message.
:::

::: attribute
failureException

This class attribute gives the exception raised by the test method. If a test framework needs to use a specialized exception, possibly to carry additional information, it must subclass this exception in order to \"play fair\" with the framework. The initial value of this attribute is `AssertionError`{.interpreted-text role="exc"}.
:::

:::: attribute
longMessage

This class attribute determines what happens when a custom failure message is passed as the msg argument to an assertXYY call that fails. `True` is the default value. In this case, the custom message is appended to the end of the standard failure message. When set to `False`, the custom message replaces the standard message.

The class setting can be overridden in individual test methods by assigning an instance attribute, self.longMessage, to `True` or `False` before calling the assert methods.

The class setting gets reset before each test call.

::: versionadded
3.1
:::
::::

:::: attribute
maxDiff

This attribute controls the maximum length of diffs output by assert methods that report diffs on failure. It defaults to 80\*8 characters. Assert methods affected by this attribute are `assertSequenceEqual`{.interpreted-text role="meth"} (including all the sequence comparison methods that delegate to it), `assertDictEqual`{.interpreted-text role="meth"} and `assertMultiLineEqual`{.interpreted-text role="meth"}.

Setting `maxDiff` to `None` means that there is no maximum length of diffs.

::: versionadded
3.2
:::
::::

Testing frameworks can use the following methods to collect information on the test:

::: method
countTestCases()

Return the number of tests represented by this test object. For `TestCase`{.interpreted-text role="class"} instances, this will always be `1`.
:::

::: method
defaultTestResult()

Return an instance of the test result class that should be used for this test case class (if no other result instance is provided to the `run`{.interpreted-text role="meth"} method).

For `TestCase`{.interpreted-text role="class"} instances, this will always be an instance of `TestResult`{.interpreted-text role="class"}; subclasses of `TestCase`{.interpreted-text role="class"} should override this as necessary.
:::

::: method
id()

Return a string identifying the specific test case. This is usually the full name of the test method, including the module and class name.
:::

:::: method
shortDescription()

Returns a description of the test, or `None` if no description has been provided. The default implementation of this method returns the first line of the test method\'s docstring, if available, or `None`.

::: versionchanged
3.1 In 3.1 this was changed to add the test name to the short description even in the presence of a docstring. This caused compatibility issues with unittest extensions and adding the test name was moved to the `TextTestResult`{.interpreted-text role="class"} in Python 3.2.
:::
::::

:::: method
addCleanup(function, /, *args,*\*kwargs)

Add a function to be called after `tearDown`{.interpreted-text role="meth"} to cleanup resources used during the test. Functions will be called in reverse order to the order they are added (`LIFO (last-in, first-out)`{.interpreted-text role="abbr"}). They are called with any arguments and keyword arguments passed into `addCleanup`{.interpreted-text role="meth"} when they are added.

If `setUp`{.interpreted-text role="meth"} fails, meaning that `tearDown`{.interpreted-text role="meth"} is not called, then any cleanup functions added will still be called.

::: versionadded
3.1
:::
::::

:::: method
enterContext(cm)

Enter the supplied `context manager`{.interpreted-text role="term"}. If successful, also add its `~object.__exit__`{.interpreted-text role="meth"} method as a cleanup function by `addCleanup`{.interpreted-text role="meth"} and return the result of the `~object.__enter__`{.interpreted-text role="meth"} method.

::: versionadded
3.11
:::
::::

:::: method
doCleanups()

This method is called unconditionally after `tearDown`{.interpreted-text role="meth"}, or after `setUp`{.interpreted-text role="meth"} if `setUp`{.interpreted-text role="meth"} raises an exception.

It is responsible for calling all the cleanup functions added by `addCleanup`{.interpreted-text role="meth"}. If you need cleanup functions to be called *prior* to `tearDown`{.interpreted-text role="meth"} then you can call `doCleanups`{.interpreted-text role="meth"} yourself.

`doCleanups`{.interpreted-text role="meth"} pops methods off the stack of cleanup functions one at a time, so it can be called at any time.

::: versionadded
3.1
:::
::::

:::: classmethod
addClassCleanup(function, /, *args,*\*kwargs)

Add a function to be called after `tearDownClass`{.interpreted-text role="meth"} to cleanup resources used during the test class. Functions will be called in reverse order to the order they are added (`LIFO (last-in, first-out)`{.interpreted-text role="abbr"}). They are called with any arguments and keyword arguments passed into `addClassCleanup`{.interpreted-text role="meth"} when they are added.

If `setUpClass`{.interpreted-text role="meth"} fails, meaning that `tearDownClass`{.interpreted-text role="meth"} is not called, then any cleanup functions added will still be called.

::: versionadded
3.8
:::
::::

:::: classmethod
enterClassContext(cm)

Enter the supplied `context manager`{.interpreted-text role="term"}. If successful, also add its `~object.__exit__`{.interpreted-text role="meth"} method as a cleanup function by `addClassCleanup`{.interpreted-text role="meth"} and return the result of the `~object.__enter__`{.interpreted-text role="meth"} method.

::: versionadded
3.11
:::
::::

:::: classmethod
doClassCleanups()

This method is called unconditionally after `tearDownClass`{.interpreted-text role="meth"}, or after `setUpClass`{.interpreted-text role="meth"} if `setUpClass`{.interpreted-text role="meth"} raises an exception.

It is responsible for calling all the cleanup functions added by `addClassCleanup`{.interpreted-text role="meth"}. If you need cleanup functions to be called *prior* to `tearDownClass`{.interpreted-text role="meth"} then you can call `doClassCleanups`{.interpreted-text role="meth"} yourself.

`doClassCleanups`{.interpreted-text role="meth"} pops methods off the stack of cleanup functions one at a time, so it can be called at any time.

::: versionadded
3.8
:::
::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::: IsolatedAsyncioTestCase(methodName='runTest')
This class provides an API similar to `TestCase`{.interpreted-text role="class"} and also accepts coroutines as test functions.

::: versionadded
3.8
:::

:::: attribute
loop_factory

The *loop_factory* passed to `asyncio.Runner`{.interpreted-text role="class"}. Override in subclasses with `asyncio.EventLoop`{.interpreted-text role="class"} to avoid using the asyncio policy system.

::: versionadded
3.13
:::
::::

::: {.method async=""}
asyncSetUp()

Method called to prepare the test fixture. This is called after `TestCase.setUp`{.interpreted-text role="meth"}. This is called immediately before calling the test method; other than `AssertionError`{.interpreted-text role="exc"} or `SkipTest`{.interpreted-text role="exc"}, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
:::

::: {.method async=""}
asyncTearDown()

Method called immediately after the test method has been called and the result recorded. This is called before `~TestCase.tearDown`{.interpreted-text role="meth"}. This is called even if the test method raised an exception, so the implementation in subclasses may need to be particularly careful about checking internal state. Any exception, other than `AssertionError`{.interpreted-text role="exc"} or `SkipTest`{.interpreted-text role="exc"}, raised by this method will be considered an additional error rather than a test failure (thus increasing the total number of reported errors). This method will only be called if the `asyncSetUp`{.interpreted-text role="meth"} succeeds, regardless of the outcome of the test method. The default implementation does nothing.
:::

::: method
addAsyncCleanup(function, /, *args,*\*kwargs)

This method accepts a coroutine that can be used as a cleanup function.
:::

:::: {.method async=""}
enterAsyncContext(cm)

Enter the supplied `asynchronous context manager`{.interpreted-text role="term"}. If successful, also add its `~object.__aexit__`{.interpreted-text role="meth"} method as a cleanup function by `addAsyncCleanup`{.interpreted-text role="meth"} and return the result of the `~object.__aenter__`{.interpreted-text role="meth"} method.

::: versionadded
3.11
:::
::::

::: method
run(result=None)

Sets up a new event loop to run the test, collecting the result into the `TestResult`{.interpreted-text role="class"} object passed as *result*. If *result* is omitted or `None`, a temporary result object is created (by calling the `~TestCase.defaultTestResult`{.interpreted-text role="meth"} method) and used. The result object is returned to `run`{.interpreted-text role="meth"}\'s caller. At the end of the test all the tasks in the event loop are cancelled.
:::

An example illustrating the order:

    from unittest import IsolatedAsyncioTestCase

    events = []


    class Test(IsolatedAsyncioTestCase):


        def setUp(self):
            events.append("setUp")

        async def asyncSetUp(self):
            self._async_connection = await AsyncConnection()
            events.append("asyncSetUp")

        async def test_response(self):
            events.append("test_response")
            response = await self._async_connection.get("https://example.com")
            self.assertEqual(response.status_code, 200)
            self.addAsyncCleanup(self.on_cleanup)

        def tearDown(self):
            events.append("tearDown")

        async def asyncTearDown(self):
            await self._async_connection.close()
            events.append("asyncTearDown")

        async def on_cleanup(self):
            events.append("cleanup")

    if __name__ == "__main__":
        unittest.main()

After running the test, `events` would contain `["setUp", "asyncSetUp", "test_response", "asyncTearDown", "tearDown", "cleanup"]`.
::::::::::::

::: {.FunctionTestCase(testFunc, .setUp=None, .tearDown=None, .description=None)}
This class implements the portion of the `TestCase`{.interpreted-text role="class"} interface which allows the test runner to drive the test, but does not provide the methods which test code can use to check and report errors. This is used to create test cases using legacy test code, allowing it to be integrated into a `!unittest`{.interpreted-text role="mod"}-based test framework.
:::

### Grouping tests {#testsuite-objects}

::::::::::: TestSuite(tests=())
This class represents an aggregation of individual test cases and test suites. The class presents the interface needed by the test runner to allow it to be run as any other test case. Running a `TestSuite`{.interpreted-text role="class"} instance is the same as iterating over the suite, running each test individually.

If *tests* is given, it must be an iterable of individual test cases or other test suites that will be used to build the suite initially. Additional methods are provided to add test cases and suites to the collection later on.

`TestSuite`{.interpreted-text role="class"} objects behave much like `TestCase`{.interpreted-text role="class"} objects, except they do not actually implement a test. Instead, they are used to aggregate tests into groups of tests that should be run together. Some additional methods are available to add tests to `TestSuite`{.interpreted-text role="class"} instances:

::: method
TestSuite.addTest(test)

Add a `TestCase`{.interpreted-text role="class"} or `TestSuite`{.interpreted-text role="class"} to the suite.
:::

::: method
TestSuite.addTests(tests)

Add all the tests from an iterable of `TestCase`{.interpreted-text role="class"} and `TestSuite`{.interpreted-text role="class"} instances to this test suite.

This is equivalent to iterating over *tests*, calling `addTest`{.interpreted-text role="meth"} for each element.
:::

`TestSuite`{.interpreted-text role="class"} shares the following methods with `TestCase`{.interpreted-text role="class"}:

::: method
run(result)

Run the tests associated with this suite, collecting the result into the test result object passed as *result*. Note that unlike `TestCase.run`{.interpreted-text role="meth"}, `TestSuite.run`{.interpreted-text role="meth"} requires the result object to be passed in.
:::

::: method
debug()

Run the tests associated with this suite without collecting the result. This allows exceptions raised by the test to be propagated to the caller and can be used to support running tests under a debugger.
:::

::: method
countTestCases()

Return the number of tests represented by this test object, including all individual tests and sub-suites.
:::

::::: method
\_\_iter\_\_()

Tests grouped by a `TestSuite`{.interpreted-text role="class"} are always accessed by iteration. Subclasses can lazily provide tests by overriding `!__iter__`{.interpreted-text role="meth"}. Note that this method may be called several times on a single suite (for example when counting tests or comparing for equality) so the tests returned by repeated iterations before `TestSuite.run`{.interpreted-text role="meth"} must be the same for each call iteration. After `TestSuite.run`{.interpreted-text role="meth"}, callers should not rely on the tests returned by this method unless the caller uses a subclass that overrides `!TestSuite._removeTestAtIndex`{.interpreted-text role="meth"} to preserve test references.

::: versionchanged
3.2 In earlier versions the `TestSuite`{.interpreted-text role="class"} accessed tests directly rather than through iteration, so overriding `!__iter__`{.interpreted-text role="meth"} wasn\'t sufficient for providing tests.
:::

::: versionchanged
3.4 In earlier versions the `TestSuite`{.interpreted-text role="class"} held references to each `TestCase`{.interpreted-text role="class"} after `TestSuite.run`{.interpreted-text role="meth"}. Subclasses can restore that behavior by overriding `!TestSuite._removeTestAtIndex`{.interpreted-text role="meth"}.
:::
:::::

In the typical usage of a `TestSuite`{.interpreted-text role="class"} object, the `run`{.interpreted-text role="meth"} method is invoked by a `!TestRunner`{.interpreted-text role="class"} rather than by the end-user test harness.
:::::::::::

### Loading and running tests

:::::::::::::::::::::::::::: TestLoader()
The `TestLoader`{.interpreted-text role="class"} class is used to create test suites from classes and modules. Normally, there is no need to create an instance of this class; the `!unittest`{.interpreted-text role="mod"} module provides an instance that can be shared as `unittest.defaultTestLoader`{.interpreted-text role="data"}. Using a subclass or instance, however, allows customization of some configurable properties.

`TestLoader`{.interpreted-text role="class"} objects have the following attributes:

:::: attribute
errors

A list of the non-fatal errors encountered while loading tests. Not reset by the loader at any point. Fatal errors are signalled by the relevant method raising an exception to the caller. Non-fatal errors are also indicated by a synthetic test that will raise the original error when run.

::: versionadded
3.5
:::
::::

`TestLoader`{.interpreted-text role="class"} objects have the following methods:

::: method
loadTestsFromTestCase(testCaseClass)

Return a suite of all test cases contained in the `TestCase`{.interpreted-text role="class"}-derived `!testCaseClass`{.interpreted-text role="class"}.

A test case instance is created for each method named by `getTestCaseNames`{.interpreted-text role="meth"}. By default these are the method names beginning with `test`. If `getTestCaseNames`{.interpreted-text role="meth"} returns no methods, but the `!runTest`{.interpreted-text role="meth"} method is implemented, a single test case is created for that method instead.
:::

:::::::: method
loadTestsFromModule(module, \*, pattern=None)

Return a suite of all test cases contained in the given module. This method searches *module* for classes derived from `TestCase`{.interpreted-text role="class"} and creates an instance of the class for each test method defined for the class.

:::: note
::: title
Note
:::

While using a hierarchy of `TestCase`{.interpreted-text role="class"}-derived classes can be convenient in sharing fixtures and helper functions, defining test methods on base classes that are not intended to be instantiated directly does not play well with this method. Doing so, however, can be useful when the fixtures are different and defined in subclasses.
::::

If a module provides a `load_tests` function it will be called to load the tests. This allows modules to customize test loading. This is the [load_tests protocol](#load_tests-protocol). The *pattern* argument is passed as the third argument to `load_tests`.

::: versionchanged
3.2 Support for `load_tests` added.
:::

::: versionchanged
3.5 Support for a keyword-only argument *pattern* has been added.
:::

::: versionchanged
3.12 The undocumented and unofficial *use_load_tests* parameter has been removed.
:::
::::::::

:::: method
loadTestsFromName(name, module=None)

Return a suite of all test cases given a string specifier.

The specifier *name* is a \"dotted name\" that may resolve either to a module, a test case class, a test method within a test case class, a `TestSuite`{.interpreted-text role="class"} instance, or a callable object which returns a `TestCase`{.interpreted-text role="class"} or `TestSuite`{.interpreted-text role="class"} instance. These checks are applied in the order listed here; that is, a method on a possible test case class will be picked up as \"a test method within a test case class\", rather than \"a callable object\".

For example, if you have a module `!SampleTests`{.interpreted-text role="mod"} containing a `TestCase`{.interpreted-text role="class"}-derived class `!SampleTestCase`{.interpreted-text role="class"} with three test methods (`!test_one`{.interpreted-text role="meth"}, `!test_two`{.interpreted-text role="meth"}, and `!test_three`{.interpreted-text role="meth"}), the specifier `'SampleTests.SampleTestCase'` would cause this method to return a suite which will run all three test methods. Using the specifier `'SampleTests.SampleTestCase.test_two'` would cause it to return a test suite which will run only the `!test_two`{.interpreted-text role="meth"} test method. The specifier can refer to modules and packages which have not been imported; they will be imported as a side-effect.

The method optionally resolves *name* relative to the given *module*.

::: versionchanged
3.5 If an `ImportError`{.interpreted-text role="exc"} or `AttributeError`{.interpreted-text role="exc"} occurs while traversing *name* then a synthetic test that raises that error when run will be returned. These errors are included in the errors accumulated by self.errors.
:::
::::

::: method
loadTestsFromNames(names, module=None)

Similar to `loadTestsFromName`{.interpreted-text role="meth"}, but takes a sequence of names rather than a single name. The return value is a test suite which supports all the tests defined for each name.
:::

::: method
getTestCaseNames(testCaseClass)

Return a sorted sequence of method names found within *testCaseClass*; this should be a subclass of `TestCase`{.interpreted-text role="class"}.
:::

::::::::: method
discover(start_dir, pattern=\'test\*.py\', top_level_dir=None)

Find all the test modules by recursing into subdirectories from the specified start directory, and return a TestSuite object containing them. Only test files that match *pattern* will be loaded. (Using shell style pattern matching.) Only module names that are importable (i.e. are valid Python identifiers) will be loaded.

All test modules must be importable from the top level of the project. If the start directory is not the top level directory then *top_level_dir* must be specified separately.

If importing a module fails, for example due to a syntax error, then this will be recorded as a single error and discovery will continue. If the import failure is due to `SkipTest`{.interpreted-text role="exc"} being raised, it will be recorded as a skip instead of an error.

If a package (a directory containing a file named `__init__.py`{.interpreted-text role="file"}) is found, the package will be checked for a `load_tests` function. If this exists then it will be called `package.load_tests(loader, tests, pattern)`. Test discovery takes care to ensure that a package is only checked for tests once during an invocation, even if the load_tests function itself calls `loader.discover`.

If `load_tests` exists then discovery does *not* recurse into the package, `load_tests` is responsible for loading all tests in the package.

The pattern is deliberately not stored as a loader attribute so that packages can continue discovery themselves.

*top_level_dir* is stored internally, and used as a default to any nested calls to `discover()`. That is, if a package\'s `load_tests` calls `loader.discover()`, it does not need to pass this argument.

*start_dir* can be a dotted module name as well as a directory.

::: versionadded
3.2
:::

::: versionchanged
3.4 Modules that raise `SkipTest`{.interpreted-text role="exc"} on import are recorded as skips, not errors.

*start_dir* can be a `namespace packages <namespace package>`{.interpreted-text role="term"}.

Paths are sorted before being imported so that execution order is the same even if the underlying file system\'s ordering is not dependent on file name.
:::

::: versionchanged
3.5 Found packages are now checked for `load_tests` regardless of whether their path matches *pattern*, because it is impossible for a package name to match the default pattern.
:::

::: versionchanged
3.11 *start_dir* can not be a `namespace packages <namespace package>`{.interpreted-text role="term"}. It has been broken since Python 3.7, and Python 3.11 officially removes it.
:::

::: versionchanged
3.13 *top_level_dir* is only stored for the duration of *discover* call.
:::

::: versionchanged
3.14 *start_dir* can once again be a `namespace package`{.interpreted-text role="term"}.
:::
:::::::::

The following attributes of a `TestLoader`{.interpreted-text role="class"} can be configured either by subclassing or assignment on an instance:

::: attribute
testMethodPrefix

String giving the prefix of method names which will be interpreted as test methods. The default value is `'test'`.

This affects `getTestCaseNames`{.interpreted-text role="meth"} and all the `loadTestsFrom*` methods.
:::

::: attribute
sortTestMethodsUsing

Function to be used to compare method names when sorting them in `getTestCaseNames`{.interpreted-text role="meth"} and all the `loadTestsFrom*` methods.
:::

::: attribute
suiteClass

Callable object that constructs a test suite from a list of tests. No methods on the resulting object are needed. The default value is the `TestSuite`{.interpreted-text role="class"} class.

This affects all the `loadTestsFrom*` methods.
:::

:::: attribute
testNamePatterns

List of Unix shell-style wildcard test name patterns that test methods have to match to be included in test suites (see `-k` option).

If this attribute is not `None` (the default), all test methods to be included in test suites must match one of the patterns in this list. Note that matches are always performed using `fnmatch.fnmatchcase`{.interpreted-text role="meth"}, so unlike patterns passed to the `-k` option, simple substring patterns will have to be converted using `*` wildcards.

This affects all the `loadTestsFrom*` methods.

::: versionadded
3.7
:::
::::
::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::: TestResult
This class is used to compile information about which tests have succeeded and which have failed.

A `TestResult`{.interpreted-text role="class"} object stores the results of a set of tests. The `TestCase`{.interpreted-text role="class"} and `TestSuite`{.interpreted-text role="class"} classes ensure that results are properly recorded; test authors do not need to worry about recording the outcome of tests.

Testing frameworks built on top of `!unittest`{.interpreted-text role="mod"} may want access to the `TestResult`{.interpreted-text role="class"} object generated by running a set of tests for reporting purposes; a `TestResult`{.interpreted-text role="class"} instance is returned by the `!TestRunner.run`{.interpreted-text role="meth"} method for this purpose.

`TestResult`{.interpreted-text role="class"} instances have the following attributes that will be of interest when inspecting the results of running a set of tests:

::: attribute
errors

A list containing 2-tuples of `TestCase`{.interpreted-text role="class"} instances and strings holding formatted tracebacks. Each tuple represents a test which raised an unexpected exception.
:::

::: attribute
failures

A list containing 2-tuples of `TestCase`{.interpreted-text role="class"} instances and strings holding formatted tracebacks. Each tuple represents a test where a failure was explicitly signalled using the `assert\* methods <assert-methods>`{.interpreted-text role="ref"}.
:::

:::: attribute
skipped

A list containing 2-tuples of `TestCase`{.interpreted-text role="class"} instances and strings holding the reason for skipping the test.

::: versionadded
3.1
:::
::::

::: attribute
expectedFailures

A list containing 2-tuples of `TestCase`{.interpreted-text role="class"} instances and strings holding formatted tracebacks. Each tuple represents an expected failure or error of the test case.
:::

::: attribute
unexpectedSuccesses

A list containing `TestCase`{.interpreted-text role="class"} instances that were marked as expected failures, but succeeded.
:::

:::: attribute
collectedDurations

A list containing 2-tuples of test case names and floats representing the elapsed time of each test which was run.

::: versionadded
3.12
:::
::::

::: attribute
shouldStop

Set to `True` when the execution of tests should stop by `stop`{.interpreted-text role="meth"}.
:::

::: attribute
testsRun

The total number of tests run so far.
:::

:::: attribute
buffer

If set to true, `sys.stdout` and `sys.stderr` will be buffered in between `startTest`{.interpreted-text role="meth"} and `stopTest`{.interpreted-text role="meth"} being called. Collected output will only be echoed onto the real `sys.stdout` and `sys.stderr` if the test fails or errors. Any output is also attached to the failure / error message.

::: versionadded
3.2
:::
::::

:::: attribute
failfast

If set to true `stop`{.interpreted-text role="meth"} will be called on the first failure or error, halting the test run.

::: versionadded
3.2
:::
::::

:::: attribute
tb_locals

If set to true then local variables will be shown in tracebacks.

::: versionadded
3.5
:::
::::

:::: method
wasSuccessful()

Return `True` if all tests run so far have passed, otherwise returns `False`.

::: versionchanged
3.4 Returns `False` if there were any `unexpectedSuccesses`{.interpreted-text role="attr"} from tests marked with the `expectedFailure`{.interpreted-text role="func"} decorator.
:::
::::

::: method
stop()

This method can be called to signal that the set of tests being run should be aborted by setting the `shouldStop`{.interpreted-text role="attr"} attribute to `True`. `!TestRunner`{.interpreted-text role="class"} objects should respect this flag and return without running any additional tests.

For example, this feature is used by the `TextTestRunner`{.interpreted-text role="class"} class to stop the test framework when the user signals an interrupt from the keyboard. Interactive tools which provide `!TestRunner`{.interpreted-text role="class"} implementations can use this in a similar manner.
:::

The following methods of the `TestResult`{.interpreted-text role="class"} class are used to maintain the internal data structures, and may be extended in subclasses to support additional reporting requirements. This is particularly useful in building tools which support interactive reporting while tests are being run.

::: method
startTest(test)

Called when the test case *test* is about to be run.
:::

::: method
stopTest(test)

Called after the test case *test* has been executed, regardless of the outcome.
:::

:::: method
startTestRun()

Called once before any tests are executed.

::: versionadded
3.1
:::
::::

:::: method
stopTestRun()

Called once after all tests are executed.

::: versionadded
3.1
:::
::::

::: method
addError(test, err)

Called when the test case *test* raises an unexpected exception. *err* is a tuple of the form returned by `sys.exc_info`{.interpreted-text role="func"}: `(type, value, traceback)`.

The default implementation appends a tuple `(test, formatted_err)` to the instance\'s `errors`{.interpreted-text role="attr"} attribute, where *formatted_err* is a formatted traceback derived from *err*.
:::

::: method
addFailure(test, err)

Called when the test case *test* signals a failure. *err* is a tuple of the form returned by `sys.exc_info`{.interpreted-text role="func"}: `(type, value, traceback)`.

The default implementation appends a tuple `(test, formatted_err)` to the instance\'s `failures`{.interpreted-text role="attr"} attribute, where *formatted_err* is a formatted traceback derived from *err*.
:::

::: method
addSuccess(test)

Called when the test case *test* succeeds.

The default implementation does nothing.
:::

::: method
addSkip(test, reason)

Called when the test case *test* is skipped. *reason* is the reason the test gave for skipping.

The default implementation appends a tuple `(test, reason)` to the instance\'s `skipped`{.interpreted-text role="attr"} attribute.
:::

::: method
addExpectedFailure(test, err)

Called when the test case *test* fails or errors, but was marked with the `expectedFailure`{.interpreted-text role="func"} decorator.

The default implementation appends a tuple `(test, formatted_err)` to the instance\'s `expectedFailures`{.interpreted-text role="attr"} attribute, where *formatted_err* is a formatted traceback derived from *err*.
:::

::: method
addUnexpectedSuccess(test)

Called when the test case *test* was marked with the `expectedFailure`{.interpreted-text role="func"} decorator, but succeeded.

The default implementation appends the test to the instance\'s `unexpectedSuccesses`{.interpreted-text role="attr"} attribute.
:::

:::: method
addSubTest(test, subtest, outcome)

Called when a subtest finishes. *test* is the test case corresponding to the test method. *subtest* is a custom `TestCase`{.interpreted-text role="class"} instance describing the subtest.

If *outcome* is `None`{.interpreted-text role="const"}, the subtest succeeded. Otherwise, it failed with an exception where *outcome* is a tuple of the form returned by `sys.exc_info`{.interpreted-text role="func"}: `(type, value, traceback)`.

The default implementation does nothing when the outcome is a success, and records subtest failures as normal failures.

::: versionadded
3.4
:::
::::

:::: method
addDuration(test, elapsed)

Called when the test case finishes. *elapsed* is the time represented in seconds, and it includes the execution of cleanup functions.

::: versionadded
3.12
:::
::::
::::::::::::::::::::::::::::::::::::::

::::: {.TextTestResult(stream, .descriptions, .verbosity, .*, .durations=None)}
A concrete implementation of `TestResult`{.interpreted-text role="class"} used by the `TextTestRunner`{.interpreted-text role="class"}. Subclasses should accept `**kwargs` to ensure compatibility as the interface changes.

::: versionadded
3.2
:::

::: versionchanged
3.12 Added the *durations* keyword parameter.
:::
:::::

::: data
defaultTestLoader

Instance of the `TestLoader`{.interpreted-text role="class"} class intended to be shared. If no customization of the `TestLoader`{.interpreted-text role="class"} is needed, this instance can be used instead of repeatedly creating new instances.
:::

::::::::: {.TextTestRunner(stream=None, .descriptions=True, .verbosity=1, .failfast=False, .\\ .buffer=False, .resultclass=None, .warnings=None, .*, .\\ .tb_locals=False, .durations=None)}
A basic test runner implementation that outputs results to a stream. If *stream* is `None`, the default, `sys.stderr`{.interpreted-text role="data"} is used as the output stream. This class has a few configurable parameters, but is essentially very simple. Graphical applications which run test suites should provide alternate implementations. Such implementations should accept `**kwargs` as the interface to construct runners changes when features are added to unittest.

By default this runner shows `DeprecationWarning`{.interpreted-text role="exc"}, `PendingDeprecationWarning`{.interpreted-text role="exc"}, `ResourceWarning`{.interpreted-text role="exc"} and `ImportWarning`{.interpreted-text role="exc"} even if they are `ignored by default
<warning-ignored>`{.interpreted-text role="ref"}. This behavior can be overridden using Python\'s `!-Wd`{.interpreted-text role="option"} or `!-Wa`{.interpreted-text role="option"} options (see `Warning control <using-on-warnings>`{.interpreted-text role="ref"}) and leaving *warnings* to `None`.

::: versionchanged
3.2 Added the *warnings* parameter.
:::

::: versionchanged
3.2 The default stream is set to `sys.stderr`{.interpreted-text role="data"} at instantiation time rather than import time.
:::

::: versionchanged
3.5 Added the *tb_locals* parameter.
:::

::: versionchanged
3.12 Added the *durations* parameter.
:::

::: method
[makeResult]{#makeresult}()

This method returns the instance of `TestResult` used by `run`{.interpreted-text role="meth"}. It is not intended to be called directly, but can be overridden in subclasses to provide a custom `TestResult`.

`_makeResult()` instantiates the class or callable passed in the `TextTestRunner` constructor as the `resultclass` argument. It defaults to `TextTestResult`{.interpreted-text role="class"} if no `resultclass` is provided. The result class is instantiated with the following arguments:

    stream, descriptions, verbosity
:::

::: method
run(test)

This method is the main public interface to the `TextTestRunner`. This method takes a `TestSuite`{.interpreted-text role="class"} or `TestCase`{.interpreted-text role="class"} instance. A `TestResult`{.interpreted-text role="class"} is created by calling `_makeResult`{.interpreted-text role="func"} and the test(s) are run and the results printed to stdout.
:::
:::::::::

:::::: function
main(module=\'\_\_main\_\_\', defaultTest=None, argv=None, testRunner=None, testLoader=unittest.defaultTestLoader, exit=True, verbosity=1, failfast=None, catchbreak=None, buffer=None, warnings=None)

A command-line program that loads a set of tests from *module* and runs them; this is primarily for making test modules conveniently executable. The simplest use for this function is to include the following line at the end of a test script:

    if __name__ == '__main__':
        unittest.main()

You can run tests with more detailed information by passing in the verbosity argument:

    if __name__ == '__main__':
        unittest.main(verbosity=2)

The *defaultTest* argument is either the name of a single test or an iterable of test names to run if no test names are specified via *argv*. If not specified or `None` and no test names are provided via *argv*, all tests found in *module* are run.

The *argv* argument can be a list of options passed to the program, with the first element being the program name. If not specified or `None`, the values of `sys.argv`{.interpreted-text role="data"} are used.

The *testRunner* argument can either be a test runner class or an already created instance of it. By default `main` calls `sys.exit`{.interpreted-text role="func"} with an exit code indicating success (0) or failure (1) of the tests run. An exit code of 5 indicates that no tests were run or skipped.

The *testLoader* argument has to be a `TestLoader`{.interpreted-text role="class"} instance, and defaults to `defaultTestLoader`{.interpreted-text role="data"}.

`main` supports being used from the interactive interpreter by passing in the argument `exit=False`. This displays the result on standard output without calling `sys.exit`{.interpreted-text role="func"}:

    >>> from unittest import main
    >>> main(module='test_module', exit=False)

The *failfast*, *catchbreak* and *buffer* parameters have the same effect as the same-name [command-line options](#command-line-options).

The *warnings* argument specifies the `warning filter <warning-filter>`{.interpreted-text role="ref"} that should be used while running the tests. If it\'s not specified, it will remain `None` if a `!-W`{.interpreted-text role="option"} option is passed to `python`{.interpreted-text role="program"} (see `Warning control <using-on-warnings>`{.interpreted-text role="ref"}), otherwise it will be set to `'default'`.

Calling `main` returns an object with the `result` attribute that contains the result of the tests run as a `unittest.TestResult`{.interpreted-text role="class"}.

::: versionchanged
3.1 The *exit* parameter was added.
:::

::: versionchanged
3.2 The *verbosity*, *failfast*, *catchbreak*, *buffer* and *warnings* parameters were added.
:::

::: versionchanged
3.4 The *defaultTest* parameter was changed to also accept an iterable of test names.
:::
::::::

#### load_tests Protocol

::: versionadded
3.2
:::

Modules or packages can customize how tests are loaded from them during normal test runs or test discovery by implementing a function called `load_tests`.

If a test module defines `load_tests` it will be called by `TestLoader.loadTestsFromModule`{.interpreted-text role="meth"} with the following arguments:

    load_tests(loader, standard_tests, pattern)

where *pattern* is passed straight through from `loadTestsFromModule`. It defaults to `None`.

It should return a `TestSuite`{.interpreted-text role="class"}.

*loader* is the instance of `TestLoader`{.interpreted-text role="class"} doing the loading. *standard_tests* are the tests that would be loaded by default from the module. It is common for test modules to only want to add or remove tests from the standard set of tests. The third argument is used when loading packages as part of test discovery.

A typical `load_tests` function that loads tests from a specific set of `TestCase`{.interpreted-text role="class"} classes may look like:

    test_cases = (TestCase1, TestCase2, TestCase3)

    def load_tests(loader, tests, pattern):
        suite = TestSuite()
        for test_class in test_cases:
            tests = loader.loadTestsFromTestCase(test_class)
            suite.addTests(tests)
        return suite

If discovery is started in a directory containing a package, either from the command line or by calling `TestLoader.discover`{.interpreted-text role="meth"}, then the package `__init__.py`{.interpreted-text role="file"} will be checked for `load_tests`. If that function does not exist, discovery will recurse into the package as though it were just another directory. Otherwise, discovery of the package\'s tests will be left up to `load_tests` which is called with the following arguments:

    load_tests(loader, standard_tests, pattern)

This should return a `TestSuite`{.interpreted-text role="class"} representing all the tests from the package. (`standard_tests` will only contain tests collected from `__init__.py`{.interpreted-text role="file"}.)

Because the pattern is passed into `load_tests` the package is free to continue (and potentially modify) test discovery. A \'do nothing\' `load_tests` function for a test package would look like:

    def load_tests(loader, standard_tests, pattern):
        # top level directory cached on loader instance
        this_dir = os.path.dirname(__file__)
        package_tests = loader.discover(start_dir=this_dir, pattern=pattern)
        standard_tests.addTests(package_tests)
        return standard_tests

::: versionchanged
3.5 Discovery no longer checks package names for matching *pattern* due to the impossibility of package names matching the default pattern.
:::

## Class and Module Fixtures

Class and module level fixtures are implemented in `TestSuite`{.interpreted-text role="class"}. When the test suite encounters a test from a new class then `~TestCase.tearDownClass`{.interpreted-text role="meth"} from the previous class (if there is one) is called, followed by `~TestCase.setUpClass`{.interpreted-text role="meth"} from the new class.

Similarly if a test is from a different module from the previous test then `tearDownModule` from the previous module is run, followed by `setUpModule` from the new module.

After all the tests have run the final `tearDownClass` and `tearDownModule` are run.

Note that shared fixtures do not play well with \[potential\] features like test parallelization and they break test isolation. They should be used with care.

The default ordering of tests created by the unittest test loaders is to group all tests from the same modules and classes together. This will lead to `setUpClass` / `setUpModule` (etc) being called exactly once per class and module. If you randomize the order, so that tests from different modules and classes are adjacent to each other, then these shared fixture functions may be called multiple times in a single test run.

Shared fixtures are not intended to work with suites with non-standard ordering. A `BaseTestSuite` still exists for frameworks that don\'t want to support shared fixtures.

If there are any exceptions raised during one of the shared fixture functions the test is reported as an error. Because there is no corresponding test instance an `_ErrorHolder` object (that has the same interface as a `TestCase`{.interpreted-text role="class"}) is created to represent the error. If you are just using the standard unittest test runner then this detail doesn\'t matter, but if you are a framework author it may be relevant.

### setUpClass and tearDownClass

These must be implemented as class methods:

    import unittest

    class Test(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            cls._connection = createExpensiveConnectionObject()

        @classmethod
        def tearDownClass(cls):
            cls._connection.destroy()

If you want the `setUpClass` and `tearDownClass` on base classes called then you must call up to them yourself. The implementations in `TestCase`{.interpreted-text role="class"} are empty.

If an exception is raised during a `setUpClass` then the tests in the class are not run and the `tearDownClass` is not run. Skipped classes will not have `setUpClass` or `tearDownClass` run. If the exception is a `SkipTest`{.interpreted-text role="exc"} exception then the class will be reported as having been skipped instead of as an error.

### setUpModule and tearDownModule

::: {.function no-typesetting=""}
setUpModule tearDownModule
:::

These should be implemented as functions:

    def setUpModule():
        createConnection()

    def tearDownModule():
        closeConnection()

If an exception is raised in a `setUpModule` then none of the tests in the module will be run and the `tearDownModule` will not be run. If the exception is a `SkipTest`{.interpreted-text role="exc"} exception then the module will be reported as having been skipped instead of as an error.

To add cleanup code that must be run even in the case of an exception, use `addModuleCleanup`:

:::: function
addModuleCleanup(function, /, *args,*\*kwargs)

Add a function to be called after `tearDownModule`{.interpreted-text role="func"} to cleanup resources used during the test class. Functions will be called in reverse order to the order they are added (`LIFO (last-in, first-out)`{.interpreted-text role="abbr"}). They are called with any arguments and keyword arguments passed into `addModuleCleanup`{.interpreted-text role="meth"} when they are added.

If `setUpModule`{.interpreted-text role="meth"} fails, meaning that `tearDownModule`{.interpreted-text role="func"} is not called, then any cleanup functions added will still be called.

::: versionadded
3.8
:::
::::

:::: function
enterModuleContext(cm)

Enter the supplied `context manager`{.interpreted-text role="term"}. If successful, also add its `~object.__exit__`{.interpreted-text role="meth"} method as a cleanup function by `addModuleCleanup`{.interpreted-text role="func"} and return the result of the `~object.__enter__`{.interpreted-text role="meth"} method.

::: versionadded
3.11
:::
::::

:::: function
doModuleCleanups()

This function is called unconditionally after `tearDownModule`{.interpreted-text role="func"}, or after `setUpModule`{.interpreted-text role="func"} if `setUpModule`{.interpreted-text role="func"} raises an exception.

It is responsible for calling all the cleanup functions added by `addModuleCleanup`{.interpreted-text role="func"}. If you need cleanup functions to be called *prior* to `tearDownModule`{.interpreted-text role="func"} then you can call `doModuleCleanups`{.interpreted-text role="func"} yourself.

`doModuleCleanups`{.interpreted-text role="func"} pops methods off the stack of cleanup functions one at a time, so it can be called at any time.

::: versionadded
3.8
:::
::::

## Signal Handling

::: versionadded
3.2
:::

The `-c/--catch <unittest -c>`{.interpreted-text role="option"} command-line option to unittest, along with the `catchbreak` parameter to `unittest.main`{.interpreted-text role="func"}, provide more friendly handling of control-C during a test run. With catch break behavior enabled control-C will allow the currently running test to complete, and the test run will then end and report all the results so far. A second control-c will raise a `KeyboardInterrupt`{.interpreted-text role="exc"} in the usual way.

The control-c handling signal handler attempts to remain compatible with code or tests that install their own `signal.SIGINT`{.interpreted-text role="const"} handler. If the `unittest` handler is called but *isn\'t* the installed `signal.SIGINT`{.interpreted-text role="const"} handler, i.e. it has been replaced by the system under test and delegated to, then it calls the default handler. This will normally be the expected behavior by code that replaces an installed handler and delegates to it. For individual tests that need `unittest` control-c handling disabled the `removeHandler`{.interpreted-text role="func"} decorator can be used.

There are a few utility functions for framework authors to enable control-c handling functionality within test frameworks.

::: function
installHandler()

Install the control-c handler. When a `signal.SIGINT`{.interpreted-text role="const"} is received (usually in response to the user pressing control-c) all registered results have `~TestResult.stop`{.interpreted-text role="meth"} called.
:::

::: function
registerResult(result)

Register a `TestResult`{.interpreted-text role="class"} object for control-c handling. Registering a result stores a weak reference to it, so it doesn\'t prevent the result from being garbage collected.

Registering a `TestResult`{.interpreted-text role="class"} object has no side-effects if control-c handling is not enabled, so test frameworks can unconditionally register all results they create independently of whether or not handling is enabled.
:::

::: function
removeResult(result)

Remove a registered result. Once a result has been removed then `~TestResult.stop`{.interpreted-text role="meth"} will no longer be called on that result object in response to a control-c.
:::

::: function
removeHandler(function=None)

When called without arguments this function removes the control-c handler if it has been installed. This function can also be used as a test decorator to temporarily remove the handler while the test is being executed:

    @unittest.removeHandler
    def test_signal_handling(self):
        ...
:::
