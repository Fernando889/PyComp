# `!cmd`{.interpreted-text role="mod"} \-\-- Support for line-oriented command interpreters

::: {.module synopsis="Build line-oriented command interpreters."}
cmd
:::

**Source code:** `Lib/cmd.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `Cmd`{.interpreted-text role="class"} class provides a simple framework for writing line-oriented command interpreters. These are often useful for test harnesses, administrative tools, and prototypes that will later be wrapped in a more sophisticated interface.

:::: {.Cmd(completekey='tab', .stdin=None, .stdout=None)}
A `Cmd`{.interpreted-text role="class"} instance or subclass instance is a line-oriented interpreter framework. There is no good reason to instantiate `Cmd`{.interpreted-text role="class"} itself; rather, it\'s useful as a superclass of an interpreter class you define yourself in order to inherit `Cmd`{.interpreted-text role="class"}\'s methods and encapsulate action methods.

The optional argument *completekey* is the `readline`{.interpreted-text role="mod"} name of a completion key; it defaults to `Tab`{.interpreted-text role="kbd"}. If *completekey* is not `None`{.interpreted-text role="const"} and `readline`{.interpreted-text role="mod"} is available, command completion is done automatically.

The default, `'tab'`, is treated specially, so that it refers to the `Tab`{.interpreted-text role="kbd"} key on every `readline.backend`{.interpreted-text role="data"}. Specifically, if `readline.backend`{.interpreted-text role="data"} is `editline`, `Cmd` will use `'^I'` instead of `'tab'`. Note that other values are not treated this way, and might only work with a specific backend.

The optional arguments *stdin* and *stdout* specify the input and output file objects that the Cmd instance or subclass instance will use for input and output. If not specified, they will default to `sys.stdin`{.interpreted-text role="data"} and `sys.stdout`{.interpreted-text role="data"}.

If you want a given *stdin* to be used, make sure to set the instance\'s `use_rawinput`{.interpreted-text role="attr"} attribute to `False`, otherwise *stdin* will be ignored.

::: versionchanged
3.13 `completekey='tab'` is replaced by `'^I'` for `editline`.
:::
::::

## Cmd Objects

A `Cmd`{.interpreted-text role="class"} instance has the following methods:

:::: method
Cmd.cmdloop(intro=None)

Repeatedly issue a prompt, accept input, parse an initial prefix off the received input, and dispatch to action methods, passing them the remainder of the line as argument.

The optional argument is a banner or intro string to be issued before the first prompt (this overrides the `intro`{.interpreted-text role="attr"} class attribute).

If the `readline`{.interpreted-text role="mod"} module is loaded, input will automatically inherit `bash`{.interpreted-text role="program"}-like history-list editing (e.g. `Control-P`{.interpreted-text role="kbd"} scrolls back to the last command, `Control-N`{.interpreted-text role="kbd"} forward to the next one, `Control-F`{.interpreted-text role="kbd"} moves the cursor to the right non-destructively, `Control-B`{.interpreted-text role="kbd"} moves the cursor to the left non-destructively, etc.).

An end-of-file on input is passed back as the string `'EOF'`.

::: index
single: ? (question mark); in a command interpreter single: ! (exclamation); in a command interpreter
:::

An interpreter instance will recognize a command name `foo` if and only if it has a method `!do_foo`{.interpreted-text role="meth"}. As a special case, a line beginning with the character `'?'` is dispatched to the method `do_help`{.interpreted-text role="meth"}. As another special case, a line beginning with the character `'!'` is dispatched to the method `!do_shell`{.interpreted-text role="meth"} (if such a method is defined).

This method will return when the `postcmd`{.interpreted-text role="meth"} method returns a true value. The *stop* argument to `postcmd`{.interpreted-text role="meth"} is the return value from the command\'s corresponding `!do_\*`{.interpreted-text role="meth"} method.

If completion is enabled, completing commands will be done automatically, and completing of commands args is done by calling `!complete_foo`{.interpreted-text role="meth"} with arguments *text*, *line*, *begidx*, and *endidx*. *text* is the string prefix we are attempting to match: all returned matches must begin with it. *line* is the current input line with leading whitespace removed, *begidx* and *endidx* are the beginning and ending indexes of the prefix text, which could be used to provide different completion depending upon which position the argument is in.
::::

::: method
Cmd.do_help(arg)

All subclasses of `Cmd`{.interpreted-text role="class"} inherit a predefined `!do_help`{.interpreted-text role="meth"}. This method, called with an argument `'bar'`, invokes the corresponding method `!help_bar`{.interpreted-text role="meth"}, and if that is not present, prints the docstring of `!do_bar`{.interpreted-text role="meth"}, if available. With no argument, `!do_help`{.interpreted-text role="meth"} lists all available help topics (that is, all commands with corresponding `!help_\*`{.interpreted-text role="meth"} methods or commands that have docstrings), and also lists any undocumented commands.
:::

::: method
Cmd.onecmd(str)

Interpret the argument as though it had been typed in response to the prompt. This may be overridden, but should not normally need to be; see the `precmd`{.interpreted-text role="meth"} and `postcmd`{.interpreted-text role="meth"} methods for useful execution hooks. The return value is a flag indicating whether interpretation of commands by the interpreter should stop. If there is a `!do_\*`{.interpreted-text role="meth"} method for the command *str*, the return value of that method is returned, otherwise the return value from the `default`{.interpreted-text role="meth"} method is returned.
:::

::: method
Cmd.emptyline()

Method called when an empty line is entered in response to the prompt. If this method is not overridden, it repeats the last nonempty command entered.
:::

::: method
Cmd.default(line)

Method called on an input line when the command prefix is not recognized. If this method is not overridden, it prints an error message and returns.
:::

::: method
Cmd.completedefault(text, line, begidx, endidx)

Method called to complete an input line when no command-specific `!complete_\*`{.interpreted-text role="meth"} method is available. By default, it returns an empty list.
:::

::: method
Cmd.columnize(list, displaywidth=80)

Method called to display a list of strings as a compact set of columns. Each column is only as wide as necessary. Columns are separated by two spaces for readability.
:::

::: method
Cmd.precmd(line)

Hook method executed just before the command line *line* is interpreted, but after the input prompt is generated and issued. This method is a stub in `Cmd`{.interpreted-text role="class"}; it exists to be overridden by subclasses. The return value is used as the command which will be executed by the `onecmd`{.interpreted-text role="meth"} method; the `precmd`{.interpreted-text role="meth"} implementation may re-write the command or simply return *line* unchanged.
:::

::: method
Cmd.postcmd(stop, line)

Hook method executed just after a command dispatch is finished. This method is a stub in `Cmd`{.interpreted-text role="class"}; it exists to be overridden by subclasses. *line* is the command line which was executed, and *stop* is a flag which indicates whether execution will be terminated after the call to `postcmd`{.interpreted-text role="meth"}; this will be the return value of the `onecmd`{.interpreted-text role="meth"} method. The return value of this method will be used as the new value for the internal flag which corresponds to *stop*; returning false will cause interpretation to continue.
:::

::: method
Cmd.preloop()

Hook method executed once when `cmdloop`{.interpreted-text role="meth"} is called. This method is a stub in `Cmd`{.interpreted-text role="class"}; it exists to be overridden by subclasses.
:::

::: method
Cmd.postloop()

Hook method executed once when `cmdloop`{.interpreted-text role="meth"} is about to return. This method is a stub in `Cmd`{.interpreted-text role="class"}; it exists to be overridden by subclasses.
:::

Instances of `Cmd`{.interpreted-text role="class"} subclasses have some public instance variables:

::: attribute
Cmd.prompt

The prompt issued to solicit input.
:::

::: attribute
Cmd.identchars

The string of characters accepted for the command prefix.
:::

::: attribute
Cmd.lastcmd

The last nonempty command prefix seen.
:::

::: attribute
Cmd.cmdqueue

A list of queued input lines. The cmdqueue list is checked in `cmdloop`{.interpreted-text role="meth"} when new input is needed; if it is nonempty, its elements will be processed in order, as if entered at the prompt.
:::

::: attribute
Cmd.intro

A string to issue as an intro or banner. May be overridden by giving the `cmdloop`{.interpreted-text role="meth"} method an argument.
:::

::: attribute
Cmd.doc_header

The header to issue if the help output has a section for documented commands.
:::

::: attribute
Cmd.misc_header

The header to issue if the help output has a section for miscellaneous help topics (that is, there are `!help_\*`{.interpreted-text role="meth"} methods without corresponding `!do_\*`{.interpreted-text role="meth"} methods).
:::

::: attribute
Cmd.undoc_header

The header to issue if the help output has a section for undocumented commands (that is, there are `!do_\*`{.interpreted-text role="meth"} methods without corresponding `!help_\*`{.interpreted-text role="meth"} methods).
:::

::: attribute
Cmd.ruler

The character used to draw separator lines under the help-message headers. If empty, no ruler line is drawn. It defaults to `'='`.
:::

::: attribute
Cmd.use_rawinput

A flag, defaulting to true. If true, `cmdloop`{.interpreted-text role="meth"} uses `input`{.interpreted-text role="func"} to display a prompt and read the next command; if false, `sys.stdout.write() <sys.stdout>`{.interpreted-text role="data"} and `sys.stdin.readline() <sys.stdin>`{.interpreted-text role="data"} are used. (This means that by importing `readline`{.interpreted-text role="mod"}, on systems that support it, the interpreter will automatically support `Emacs`{.interpreted-text role="program"}-like line editing and command-history keystrokes.)
:::

## Cmd Example

The `!cmd`{.interpreted-text role="mod"} module is mainly useful for building custom shells that let a user work with a program interactively.

This section presents a simple example of how to build a shell around a few of the commands in the `turtle`{.interpreted-text role="mod"} module.

Basic turtle commands such as `~turtle.forward`{.interpreted-text role="meth"} are added to a `Cmd`{.interpreted-text role="class"} subclass with method named `!do_forward`{.interpreted-text role="meth"}. The argument is converted to a number and dispatched to the turtle module. The docstring is used in the help utility provided by the shell.

The example also includes a basic record and playback facility implemented with the `~Cmd.precmd`{.interpreted-text role="meth"} method which is responsible for converting the input to lowercase and writing the commands to a file. The `!do_playback`{.interpreted-text role="meth"} method reads the file and adds the recorded commands to the `~Cmd.cmdqueue`{.interpreted-text role="attr"} for immediate playback:

    import cmd, sys
    from turtle import *

    class TurtleShell(cmd.Cmd):
        intro = 'Welcome to the turtle shell.   Type help or ? to list commands.\n'
        prompt = '(turtle) '
        file = None

        # ----- basic turtle commands -----
        def do_forward(self, arg):
            'Move the turtle forward by the specified distance:  FORWARD 10'
            forward(*parse(arg))
        def do_right(self, arg):
            'Turn turtle right by given number of degrees:  RIGHT 20'
            right(*parse(arg))
        def do_left(self, arg):
            'Turn turtle left by given number of degrees:  LEFT 90'
            left(*parse(arg))
        def do_goto(self, arg):
            'Move turtle to an absolute position with changing orientation.  GOTO 100 200'
            goto(*parse(arg))
        def do_home(self, arg):
            'Return turtle to the home position:  HOME'
            home()
        def do_circle(self, arg):
            'Draw circle with given radius an options extent and steps:  CIRCLE 50'
            circle(*parse(arg))
        def do_position(self, arg):
            'Print the current turtle position:  POSITION'
            print('Current position is %d %d\n' % position())
        def do_heading(self, arg):
            'Print the current turtle heading in degrees:  HEADING'
            print('Current heading is %d\n' % (heading(),))
        def do_color(self, arg):
            'Set the color:  COLOR BLUE'
            color(arg.lower())
        def do_undo(self, arg):
            'Undo (repeatedly) the last turtle action(s):  UNDO'
        def do_reset(self, arg):
            'Clear the screen and return turtle to center:  RESET'
            reset()
        def do_bye(self, arg):
            'Stop recording, close the turtle window, and exit:  BYE'
            print('Thank you for using Turtle')
            self.close()
            bye()
            return True

        # ----- record and playback -----
        def do_record(self, arg):
            'Save future commands to filename:  RECORD rose.cmd'
            self.file = open(arg, 'w')
        def do_playback(self, arg):
            'Playback commands from a file:  PLAYBACK rose.cmd'
            self.close()
            with open(arg) as f:
                self.cmdqueue.extend(f.read().splitlines())
        def precmd(self, line):
            line = line.lower()
            if self.file and 'playback' not in line:
                print(line, file=self.file)
            return line
        def close(self):
            if self.file:
                self.file.close()
                self.file = None

    def parse(arg):
        'Convert a series of zero or more numbers to an argument tuple'
        return tuple(map(int, arg.split()))

    if __name__ == '__main__':
        TurtleShell().cmdloop()

Here is a sample session with the turtle shell showing the help functions, using blank lines to repeat commands, and the simple record and playback facility:

``` none
Welcome to the turtle shell.   Type help or ? to list commands.

(turtle) ?

Documented commands (type help <topic>):
========================================
bye     color    goto     home  playback  record  right
circle  forward  heading  left  position  reset   undo

(turtle) help forward
Move the turtle forward by the specified distance:  FORWARD 10
(turtle) record spiral.cmd
(turtle) position
Current position is 0 0

(turtle) heading
Current heading is 0

(turtle) reset
(turtle) circle 20
(turtle) right 30
(turtle) circle 40
(turtle) right 30
(turtle) circle 60
(turtle) right 30
(turtle) circle 80
(turtle) right 30
(turtle) circle 100
(turtle) right 30
(turtle) circle 120
(turtle) right 30
(turtle) circle 120
(turtle) heading
Current heading is 180

(turtle) forward 100
(turtle)
(turtle) right 90
(turtle) forward 100
(turtle)
(turtle) right 90
(turtle) forward 400
(turtle) right 90
(turtle) forward 500
(turtle) right 90
(turtle) forward 400
(turtle) right 90
(turtle) forward 300
(turtle) playback spiral.cmd
Current position is 0 0

Current heading is 0

Current heading is 180

(turtle) bye
Thank you for using Turtle
```
