# `!__future__`{.interpreted-text role="mod"} \-\-- Future statement definitions

::: {.module synopsis="Future statement definitions"}
\_\_future\_\_
:::

**Source code:** `Lib/__future__.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

Imports of the form `from __future__ import feature` are called `future statements <future>`{.interpreted-text role="ref"}. These are special-cased by the Python compiler to allow the use of new Python features in modules containing the future statement before the release in which the feature becomes standard.

While these future statements are given additional special meaning by the Python compiler, they are still executed like any other import statement and the `!__future__`{.interpreted-text role="mod"} exists and is handled by the import system the same way any other Python module would be. This design serves three purposes:

- To avoid confusing existing tools that analyze import statements and expect to find the modules they\'re importing.
- To document when incompatible changes were introduced, and when they will be \-\-- or were \-\-- made mandatory. This is a form of executable documentation, and can be inspected programmatically via importing `!__future__`{.interpreted-text role="mod"} and examining its contents.
- To ensure that `future statements <future>`{.interpreted-text role="ref"} run under releases prior to Python 2.1 at least yield runtime exceptions (the import of `!__future__`{.interpreted-text role="mod"} will fail, because there was no module of that name prior to 2.1).

## Module Contents

No feature description will ever be deleted from `!__future__`{.interpreted-text role="mod"}. Since its introduction in Python 2.1 the following features have found their way into the language using this mechanism:

+------------------+-------------+--------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| feature          | optional in | mandatory in | effect                                                                                                                                                                  |
+==================+=============+==============+=========================================================================================================================================================================+
| ::: data         | 2.1.0b1     | 2.2          | `227`{.interpreted-text role="pep"}: *Statically Nested Scopes*                                                                                                         |
| nested_scopes    |             |              |                                                                                                                                                                         |
| :::              |             |              |                                                                                                                                                                         |
+------------------+-------------+--------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: data         | 2.2.0a1     | 2.3          | `255`{.interpreted-text role="pep"}: *Simple Generators*                                                                                                                |
| generators       |             |              |                                                                                                                                                                         |
| :::              |             |              |                                                                                                                                                                         |
+------------------+-------------+--------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: data         | 2.2.0a2     | 3.0          | `238`{.interpreted-text role="pep"}: *Changing the Division Operator*                                                                                                   |
| division         |             |              |                                                                                                                                                                         |
| :::              |             |              |                                                                                                                                                                         |
+------------------+-------------+--------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: data         | 2.5.0a1     | 3.0          | `328`{.interpreted-text role="pep"}: *Imports: Multi-Line and Absolute/Relative*                                                                                        |
| absolute_import  |             |              |                                                                                                                                                                         |
| :::              |             |              |                                                                                                                                                                         |
+------------------+-------------+--------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: data         | 2.5.0a1     | 2.6          | `343`{.interpreted-text role="pep"}: *The "with" Statement*                                                                                                             |
| with_statement   |             |              |                                                                                                                                                                         |
| :::              |             |              |                                                                                                                                                                         |
+------------------+-------------+--------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: data         | 2.6.0a2     | 3.0          | `3105`{.interpreted-text role="pep"}: *Make print a function*                                                                                                           |
| print_function   |             |              |                                                                                                                                                                         |
| :::              |             |              |                                                                                                                                                                         |
+------------------+-------------+--------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: data         | 2.6.0a2     | 3.0          | `3112`{.interpreted-text role="pep"}: *Bytes literals in Python 3000*                                                                                                   |
| unicode_literals |             |              |                                                                                                                                                                         |
| :::              |             |              |                                                                                                                                                                         |
+------------------+-------------+--------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: data         | 3.5.0b1     | 3.7          | `479`{.interpreted-text role="pep"}: *StopIteration handling inside generators*                                                                                         |
| generator_stop   |             |              |                                                                                                                                                                         |
| :::              |             |              |                                                                                                                                                                         |
+------------------+-------------+--------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: data         | 3.7.0b1     | Never[^1]    | `563`{.interpreted-text role="pep"}: *Postponed evaluation of annotations*, `649`{.interpreted-text role="pep"}: *Deferred evaluation of annotations using descriptors* |
| annotations      |             |              |                                                                                                                                                                         |
| :::              |             |              |                                                                                                                                                                         |
+------------------+-------------+--------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

:::: {#future-classes}
::: _Feature
Each statement in `__future__.py`{.interpreted-text role="file"} is of the form:

    FeatureName = _Feature(OptionalRelease, MandatoryRelease,
                           CompilerFlag)

where, normally, *OptionalRelease* is less than *MandatoryRelease*, and both are 5-tuples of the same form as `sys.version_info`{.interpreted-text role="data"}:

    (PY_MAJOR_VERSION, # the 2 in 2.1.0a3; an int
     PY_MINOR_VERSION, # the 1; an int
     PY_MICRO_VERSION, # the 0; an int
     PY_RELEASE_LEVEL, # "alpha", "beta", "candidate" or "final"; string
     PY_RELEASE_SERIAL # the 3; an int
    )
:::
::::

::: method
[Feature.getOptionalRelease]{#feature.getoptionalrelease}()

*OptionalRelease* records the first release in which the feature was accepted.
:::

::: method
[Feature.getMandatoryRelease]{#feature.getmandatoryrelease}()

In the case of a *MandatoryRelease* that has not yet occurred, *MandatoryRelease* predicts the release in which the feature will become part of the language.

Else *MandatoryRelease* records when the feature became part of the language; in releases at or after that, modules no longer need a future statement to use the feature in question, but may continue to use such imports.

*MandatoryRelease* may also be `None`, meaning that a planned feature got dropped or that it is not yet decided.
:::

::: attribute
[Feature.compiler_flag]{#feature.compiler_flag}

*CompilerFlag* is the (bitfield) flag that should be passed in the fourth argument to the built-in function `compile`{.interpreted-text role="func"} to enable the feature in dynamically compiled code. This flag is stored in the `_Feature.compiler_flag`{.interpreted-text role="attr"} attribute on `_Feature`{.interpreted-text role="class"} instances.
:::

::: seealso

`future`{.interpreted-text role="ref"}

:   How the compiler treats future imports.

`236`{.interpreted-text role="pep"} - Back to the \_\_future\_\_

:   The original proposal for the \_\_future\_\_ mechanism.
:::

[^1]: `from __future__ import annotations` was previously scheduled to become mandatory in Python 3.10, but the change was delayed and ultimately canceled. This feature will eventually be deprecated and removed. See `649`{.interpreted-text role="pep"} and `749`{.interpreted-text role="pep"}.
