# Interactive Input Editing and History Substitution {#tut-interacting}

Some versions of the Python interpreter support editing of the current input line and history substitution, similar to facilities found in the Korn shell and the GNU Bash shell. This is implemented using the [GNU Readline](https://tiswww.case.edu/php/chet/readline/rltop.html) library, which supports various styles of editing. This library has its own documentation which we won\'t duplicate here.

## Tab Completion and History Editing {#tut-keybindings}

Completion of variable and module names is `automatically enabled <rlcompleter-config>`{.interpreted-text role="ref"} at interpreter startup so that the `Tab`{.interpreted-text role="kbd"} key invokes the completion function; it looks at Python statement names, the current local variables, and the available module names. For dotted expressions such as `string.a`, it will evaluate the expression up to the final `'.'` and then suggest completions from the attributes of the resulting object. Note that this may execute application-defined code if an object with a `~object.__getattr__`{.interpreted-text role="meth"} method is part of the expression. The default configuration also saves your history into a file named `.python_history`{.interpreted-text role="file"} in your user directory. The history will be available again during the next interactive interpreter session.

## Alternatives to the Interactive Interpreter {#tut-commentary}

This facility is an enormous step forward compared to earlier versions of the interpreter; however, some wishes are left: It would be nice if the proper indentation were suggested on continuation lines (the parser knows if an `~token.INDENT`{.interpreted-text role="data"} token is required next). The completion mechanism might use the interpreter\'s symbol table. A command to check (or even suggest) matching parentheses, quotes, etc., would also be useful.

One alternative enhanced interactive interpreter that has been around for quite some time is [IPython](https://ipython.org/), which features tab completion, object exploration and advanced history management. It can also be thoroughly customized and embedded into other applications. Another similar enhanced interactive environment is [bpython](https://bpython-interpreter.org/).
