# `!mailbox`{.interpreted-text role="mod"} \-\-- Manipulate mailboxes in various formats

::: {.module synopsis="Manipulate mailboxes in various formats"}
mailbox
:::

**Source code:** `Lib/mailbox.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module defines two classes, `Mailbox`{.interpreted-text role="class"} and `Message`{.interpreted-text role="class"}, for accessing and manipulating on-disk mailboxes and the messages they contain. `!Mailbox`{.interpreted-text role="class"} offers a dictionary-like mapping from keys to messages. `!Message`{.interpreted-text role="class"} extends the `email.message`{.interpreted-text role="mod"} module\'s `~email.message.Message`{.interpreted-text role="class"} class with format-specific state and behavior. Supported mailbox formats are Maildir, mbox, MH, Babyl, and MMDF.

::: seealso

Module `email`{.interpreted-text role="mod"}

:   Represent and manipulate messages.
:::

## `!Mailbox`{.interpreted-text role="class"} objects

::::::::::::::::::::::::::::::::::::::: Mailbox
A mailbox, which may be inspected and modified.

The `!Mailbox`{.interpreted-text role="class"} class defines an interface and is not intended to be instantiated. Instead, format-specific subclasses should inherit from `!Mailbox`{.interpreted-text role="class"} and your code should instantiate a particular subclass.

The `!Mailbox`{.interpreted-text role="class"} interface is dictionary-like, with small keys corresponding to messages. Keys are issued by the `!Mailbox`{.interpreted-text role="class"} instance with which they will be used and are only meaningful to that `!Mailbox`{.interpreted-text role="class"} instance. A key continues to identify a message even if the corresponding message is modified, such as by replacing it with another message.

Messages may be added to a `!Mailbox`{.interpreted-text role="class"} instance using the set-like method `add`{.interpreted-text role="meth"} and removed using a `del` statement or the set-like methods `remove`{.interpreted-text role="meth"} and `discard`{.interpreted-text role="meth"}.

`!Mailbox`{.interpreted-text role="class"} interface semantics differ from dictionary semantics in some noteworthy ways. Each time a message is requested, a new representation (typically a `Message`{.interpreted-text role="class"} instance) is generated based upon the current state of the mailbox. Similarly, when a message is added to a `!Mailbox`{.interpreted-text role="class"} instance, the provided message representation\'s contents are copied. In neither case is a reference to the message representation kept by the `!Mailbox`{.interpreted-text role="class"} instance.

The default `!Mailbox`{.interpreted-text role="class"} `iterator`{.interpreted-text role="term"} iterates over message representations, not keys as the default `dictionary <dict>`{.interpreted-text role="class"} iterator does. Moreover, modification of a mailbox during iteration is safe and well-defined. Messages added to the mailbox after an iterator is created will not be seen by the iterator. Messages removed from the mailbox before the iterator yields them will be silently skipped, though using a key from an iterator may result in a `KeyError`{.interpreted-text role="exc"} exception if the corresponding message is subsequently removed.

:::: warning
::: title
Warning
:::

Be very cautious when modifying mailboxes that might be simultaneously changed by some other process. The safest mailbox format to use for such tasks is `Maildir`{.interpreted-text role="class"}; try to avoid using single-file formats such as `mbox`{.interpreted-text role="class"} for concurrent writing. If you\'re modifying a mailbox, you *must* lock it by calling the `lock`{.interpreted-text role="meth"} and `unlock`{.interpreted-text role="meth"} methods *before* reading any messages in the file or making any changes by adding or deleting a message. Failing to lock the mailbox runs the risk of losing messages or corrupting the entire mailbox.
::::

The `!Mailbox`{.interpreted-text role="class"} class supports the `with`{.interpreted-text role="keyword"} statement. When used as a context manager, `!Mailbox`{.interpreted-text role="class"} calls `lock`{.interpreted-text role="meth"} when the context is entered, returns the mailbox object as the context object, and at context end calls `close`{.interpreted-text role="meth"}, thereby releasing the lock.

::: versionchanged
next Support for the `with`{.interpreted-text role="keyword"} statement was added.
:::

`!Mailbox`{.interpreted-text role="class"} instances have the following methods:

:::: method
add(message)

Add *message* to the mailbox and return the key that has been assigned to it.

Parameter *message* may be a `Message`{.interpreted-text role="class"} instance, an `email.message.Message`{.interpreted-text role="class"} instance, a string, a byte string, or a file-like object (which should be open in binary mode). If *message* is an instance of the appropriate format-specific `Message`{.interpreted-text role="class"} subclass (e.g., if it\'s an `mboxMessage`{.interpreted-text role="class"} instance and this is an `mbox`{.interpreted-text role="class"} instance), its format-specific information is used. Otherwise, reasonable defaults for format-specific information are used.

::: versionchanged
3.2 Support for binary input was added.
:::
::::

::: method
remove(key) \_\_delitem\_\_(key) discard(key)

Delete the message corresponding to *key* from the mailbox.

If no such message exists, a `KeyError`{.interpreted-text role="exc"} exception is raised if the method was called as `remove`{.interpreted-text role="meth"} or `__delitem__`{.interpreted-text role="meth"} but no exception is raised if the method was called as `discard`{.interpreted-text role="meth"}. The behavior of `discard`{.interpreted-text role="meth"} may be preferred if the underlying mailbox format supports concurrent modification by other processes.
:::

::: method
\_\_setitem\_\_(key, message)

Replace the message corresponding to *key* with *message*. Raise a `KeyError`{.interpreted-text role="exc"} exception if no message already corresponds to *key*.

As with `add`{.interpreted-text role="meth"}, parameter *message* may be a `Message`{.interpreted-text role="class"} instance, an `email.message.Message`{.interpreted-text role="class"} instance, a string, a byte string, or a file-like object (which should be open in binary mode). If *message* is an instance of the appropriate format-specific `Message`{.interpreted-text role="class"} subclass (e.g., if it\'s an `mboxMessage`{.interpreted-text role="class"} instance and this is an `mbox`{.interpreted-text role="class"} instance), its format-specific information is used. Otherwise, the format-specific information of the message that currently corresponds to *key* is left unchanged.
:::

::: method
iterkeys()

Return an `iterator`{.interpreted-text role="term"} over all keys
:::

::: method
keys()

The same as `iterkeys`{.interpreted-text role="meth"}, except that a `list`{.interpreted-text role="class"} is returned rather than an `iterator`{.interpreted-text role="term"}
:::

::::: method
itervalues() \_\_iter\_\_()

Return an `iterator`{.interpreted-text role="term"} over representations of all messages. The messages are represented as instances of the appropriate format-specific `Message`{.interpreted-text role="class"} subclass unless a custom message factory was specified when the `!Mailbox`{.interpreted-text role="class"} instance was initialized.

:::: note
::: title
Note
:::

The behavior of `__iter__`{.interpreted-text role="meth"} is unlike that of dictionaries, which iterate over keys.
::::
:::::

::: method
values()

The same as `itervalues`{.interpreted-text role="meth"}, except that a `list`{.interpreted-text role="class"} is returned rather than an `iterator`{.interpreted-text role="term"}
:::

::: method
iteritems()

Return an `iterator`{.interpreted-text role="term"} over (*key*, *message*) pairs, where *key* is a key and *message* is a message representation. The messages are represented as instances of the appropriate format-specific `Message`{.interpreted-text role="class"} subclass unless a custom message factory was specified when the `!Mailbox`{.interpreted-text role="class"} instance was initialized.
:::

::: method
items()

The same as `iteritems`{.interpreted-text role="meth"}, except that a `list`{.interpreted-text role="class"} of pairs is returned rather than an `iterator`{.interpreted-text role="term"} of pairs.
:::

::: method
get(key, default=None) \_\_getitem\_\_(key)

Return a representation of the message corresponding to *key*. If no such message exists, *default* is returned if the method was called as `get`{.interpreted-text role="meth"} and a `KeyError`{.interpreted-text role="exc"} exception is raised if the method was called as `!__getitem__`{.interpreted-text role="meth"}. The message is represented as an instance of the appropriate format-specific `Message`{.interpreted-text role="class"} subclass unless a custom message factory was specified when the `!Mailbox`{.interpreted-text role="class"} instance was initialized.
:::

::: method
get_message(key)

Return a representation of the message corresponding to *key* as an instance of the appropriate format-specific `Message`{.interpreted-text role="class"} subclass, or raise a `KeyError`{.interpreted-text role="exc"} exception if no such message exists.
:::

:::: method
get_bytes(key)

Return a byte representation of the message corresponding to *key*, or raise a `KeyError`{.interpreted-text role="exc"} exception if no such message exists.

::: versionadded
3.2
:::
::::

::: method
get_string(key)

Return a string representation of the message corresponding to *key*, or raise a `KeyError`{.interpreted-text role="exc"} exception if no such message exists. The message is processed through `email.message.Message`{.interpreted-text role="class"} to convert it to a 7bit clean representation.
:::

:::::: method
get_file(key)

Return a `file-like <file-like object>`{.interpreted-text role="term"} representation of the message corresponding to *key*, or raise a `KeyError`{.interpreted-text role="exc"} exception if no such message exists. The file-like object behaves as if open in binary mode. This file should be closed once it is no longer needed.

::: versionchanged
3.2 The file object really is a `binary file`{.interpreted-text role="term"}; previously it was incorrectly returned in text mode. Also, the `file-like object`{.interpreted-text role="term"} now supports the `context manager`{.interpreted-text role="term"} protocol: you can use a `with`{.interpreted-text role="keyword"} statement to automatically close it.
:::

:::: note
::: title
Note
:::

Unlike other representations of messages, `file-like <file-like object>`{.interpreted-text role="term"} representations are not necessarily independent of the `!Mailbox`{.interpreted-text role="class"} instance that created them or of the underlying mailbox. More specific documentation is provided by each subclass.
::::
::::::

::: method
\_\_contains\_\_(key)

Return `True` if *key* corresponds to a message, `False` otherwise.
:::

::: method
\_\_len\_\_()

Return a count of messages in the mailbox.
:::

::: method
clear()

Delete all messages from the mailbox.
:::

::: method
pop(key, default=None)

Return a representation of the message corresponding to *key* and delete the message. If no such message exists, return *default*. The message is represented as an instance of the appropriate format-specific `Message`{.interpreted-text role="class"} subclass unless a custom message factory was specified when the `!Mailbox`{.interpreted-text role="class"} instance was initialized.
:::

::: method
popitem()

Return an arbitrary (*key*, *message*) pair, where *key* is a key and *message* is a message representation, and delete the corresponding message. If the mailbox is empty, raise a `KeyError`{.interpreted-text role="exc"} exception. The message is represented as an instance of the appropriate format-specific `Message`{.interpreted-text role="class"} subclass unless a custom message factory was specified when the `!Mailbox`{.interpreted-text role="class"} instance was initialized.
:::

::::: method
update(arg)

Parameter *arg* should be a *key*-to-*message* mapping or an iterable of (*key*, *message*) pairs. Updates the mailbox so that, for each given *key* and *message*, the message corresponding to *key* is set to *message* as if by using `__setitem__`{.interpreted-text role="meth"}. As with `__setitem__`{.interpreted-text role="meth"}, each *key* must already correspond to a message in the mailbox or else a `KeyError`{.interpreted-text role="exc"} exception will be raised, so in general it is incorrect for *arg* to be a `!Mailbox`{.interpreted-text role="class"} instance.

:::: note
::: title
Note
:::

Unlike with dictionaries, keyword arguments are not supported.
::::
:::::

::: method
flush()

Write any pending changes to the filesystem. For some `Mailbox`{.interpreted-text role="class"} subclasses, changes are always written immediately and `!flush`{.interpreted-text role="meth"} does nothing, but you should still make a habit of calling this method.
:::

::: method
lock()

Acquire an exclusive advisory lock on the mailbox so that other processes know not to modify it. An `ExternalClashError`{.interpreted-text role="exc"} is raised if the lock is not available. The particular locking mechanisms used depend upon the mailbox format. You should *always* lock the mailbox before making any modifications to its contents.
:::

::: method
unlock()

Release the lock on the mailbox, if any.
:::

::: method
close()

Flush the mailbox, unlock it if necessary, and close any open files. For some `!Mailbox`{.interpreted-text role="class"} subclasses, this method does nothing.
:::
:::::::::::::::::::::::::::::::::::::::

### `!Maildir`{.interpreted-text role="class"} objects {#mailbox-maildir}

::::::::::::::::::::::::::::: {.Maildir(dirname, .factory=None, .create=True)}
A subclass of `Mailbox`{.interpreted-text role="class"} for mailboxes in Maildir format. Parameter *factory* is a callable object that accepts a file-like message representation (which behaves as if opened in binary mode) and returns a custom representation. If *factory* is `None`, `MaildirMessage`{.interpreted-text role="class"} is used as the default message representation. If *create* is `True`, the mailbox is created if it does not exist.

If *create* is `True` and the *dirname* path exists, it will be treated as an existing maildir without attempting to verify its directory layout.

It is for historical reasons that *dirname* is named as such rather than *path*.

Maildir is a directory-based mailbox format invented for the qmail mail transfer agent and now widely supported by other programs. Messages in a Maildir mailbox are stored in separate files within a common directory structure. This design allows Maildir mailboxes to be accessed and modified by multiple unrelated programs without data corruption, so file locking is unnecessary.

Maildir mailboxes contain three subdirectories, namely: `tmp`{.interpreted-text role="file"}, `new`{.interpreted-text role="file"}, and `cur`{.interpreted-text role="file"}. Messages are created momentarily in the `tmp`{.interpreted-text role="file"} subdirectory and then moved to the `new`{.interpreted-text role="file"} subdirectory to finalize delivery. A mail user agent may subsequently move the message to the `cur`{.interpreted-text role="file"} subdirectory and store information about the state of the message in a special \"info\" section appended to its file name.

Folders of the style introduced by the Courier mail transfer agent are also supported. Any subdirectory of the main mailbox is considered a folder if `'.'` is the first character in its name. Folder names are represented by `!Maildir`{.interpreted-text role="class"} without the leading `'.'`. Each folder is itself a Maildir mailbox but should not contain other folders. Instead, a logical nesting is indicated using `'.'` to delimit levels, e.g., \"Archived.2005.07\".

::: attribute
Maildir.colon

The Maildir specification requires the use of a colon (`':'`) in certain message file names. However, some operating systems do not permit this character in file names, If you wish to use a Maildir-like format on such an operating system, you should specify another character to use instead. The exclamation point (`'!'`) is a popular choice. For example:

    import mailbox
    mailbox.Maildir.colon = '!'

The `!colon`{.interpreted-text role="attr"} attribute may also be set on a per-instance basis.
:::

::: versionchanged
3.13 `Maildir`{.interpreted-text role="class"} now ignores files with a leading dot.
:::

`!Maildir`{.interpreted-text role="class"} instances have all of the methods of `Mailbox`{.interpreted-text role="class"} in addition to the following:

::: method
list_folders()

Return a list of the names of all folders.
:::

::: method
get_folder(folder)

Return a `!Maildir`{.interpreted-text role="class"} instance representing the folder whose name is *folder*. A `NoSuchMailboxError`{.interpreted-text role="exc"} exception is raised if the folder does not exist.
:::

::: method
add_folder(folder)

Create a folder whose name is *folder* and return a `!Maildir`{.interpreted-text role="class"} instance representing it.
:::

::: method
remove_folder(folder)

Delete the folder whose name is *folder*. If the folder contains any messages, a `NotEmptyError`{.interpreted-text role="exc"} exception will be raised and the folder will not be deleted.
:::

::: method
clean()

Delete temporary files from the mailbox that have not been accessed in the last 36 hours. The Maildir specification says that mail-reading programs should do this occasionally.
:::

:::: method
get_flags(key)

Return as a string the flags that are set on the message corresponding to *key*. This is the same as `get_message(key).get_flags()` but much faster, because it does not open the message file. Use this method when iterating over the keys to determine which messages are interesting to get.

If you do have a `MaildirMessage`{.interpreted-text role="class"} object, use its `~MaildirMessage.get_flags`{.interpreted-text role="meth"} method instead, because changes made by the message\'s `~MaildirMessage.set_flags`{.interpreted-text role="meth"}, `~MaildirMessage.add_flag`{.interpreted-text role="meth"} and `~MaildirMessage.remove_flag`{.interpreted-text role="meth"} methods are not reflected here until the mailbox\'s `__setitem__`{.interpreted-text role="meth"} method is called.

::: versionadded
3.13
:::
::::

:::: method
set_flags(key, flags)

On the message corresponding to *key*, set the flags specified by *flags* and unset all others. Calling `some_mailbox.set_flags(key, flags)` is similar to :

    one_message = some_mailbox.get_message(key)
    one_message.set_flags(flags)
    some_mailbox[key] = one_message

but faster, because it does not open the message file.

If you do have a `MaildirMessage`{.interpreted-text role="class"} object, use its `~MaildirMessage.set_flags`{.interpreted-text role="meth"} method instead, because changes made with this mailbox method will not be visible to the message object\'s method, `~MaildirMessage.get_flags`{.interpreted-text role="meth"}.

::: versionadded
3.13
:::
::::

:::: method
add_flag(key, flag)

On the message corresponding to *key*, set the flags specified by *flag* without changing other flags. To add more than one flag at a time, *flag* may be a string of more than one character.

Considerations for using this method versus the message object\'s `~MaildirMessage.add_flag`{.interpreted-text role="meth"} method are similar to those for `set_flags`{.interpreted-text role="meth"}; see the discussion there.

::: versionadded
3.13
:::
::::

:::: method
remove_flag(key, flag)

On the message corresponding to *key*, unset the flags specified by *flag* without changing other flags. To remove more than one flag at a time, *flag* may be a string of more than one character.

Considerations for using this method versus the message object\'s `~MaildirMessage.remove_flag`{.interpreted-text role="meth"} method are similar to those for `set_flags`{.interpreted-text role="meth"}; see the discussion there.

::: versionadded
3.13
:::
::::

:::: method
get_info(key)

Return a string containing the info for the message corresponding to *key*. This is the same as `get_message(key).get_info()` but much faster, because it does not open the message file. Use this method when iterating over the keys to determine which messages are interesting to get.

If you do have a `MaildirMessage`{.interpreted-text role="class"} object, use its `~MaildirMessage.get_info`{.interpreted-text role="meth"} method instead, because changes made by the message\'s `~MaildirMessage.set_info`{.interpreted-text role="meth"} method are not reflected here until the mailbox\'s `__setitem__`{.interpreted-text role="meth"} method is called.

::: versionadded
3.13
:::
::::

:::: method
set_info(key, info)

Set the info of the message corresponding to *key* to *info*. Calling `some_mailbox.set_info(key, flags)` is similar to :

    one_message = some_mailbox.get_message(key)
    one_message.set_info(info)
    some_mailbox[key] = one_message

but faster, because it does not open the message file.

If you do have a `MaildirMessage`{.interpreted-text role="class"} object, use its `~MaildirMessage.set_info`{.interpreted-text role="meth"} method instead, because changes made with this mailbox method will not be visible to the message object\'s method, `~MaildirMessage.get_info`{.interpreted-text role="meth"}.

::: versionadded
3.13
:::
::::

Some `Mailbox`{.interpreted-text role="class"} methods implemented by `!Maildir`{.interpreted-text role="class"} deserve special remarks:

::::: method
add(message) \_\_setitem\_\_(key, message) update(arg)

:::: warning
::: title
Warning
:::

These methods generate unique file names based upon the current process ID. When using multiple threads, undetected name clashes may occur and cause corruption of the mailbox unless threads are coordinated to avoid using these methods to manipulate the same mailbox simultaneously.
::::
:::::

::: method
flush()

All changes to Maildir mailboxes are immediately applied, so this method does nothing.
:::

::: method
lock() unlock()

Maildir mailboxes do not support (or require) locking, so these methods do nothing.
:::

::: method
close()

`!Maildir`{.interpreted-text role="class"} instances do not keep any open files and the underlying mailboxes do not support locking, so this method does nothing.
:::

::: method
get_file(key)

Depending upon the host platform, it may not be possible to modify or remove the underlying message while the returned file remains open.
:::
:::::::::::::::::::::::::::::

::: seealso

[maildir man page from Courier](https://www.courier-mta.org/maildir.html)

:   A specification of the format. Describes a common extension for supporting folders.

[Using maildir format](https://cr.yp.to/proto/maildir.html)

:   Notes on Maildir by its inventor. Includes an updated name-creation scheme and details on \"info\" semantics.
:::

### `!mbox`{.interpreted-text role="class"} objects {#mailbox-mbox}

::::::: {.mbox(path, .factory=None, .create=True)}
A subclass of `Mailbox`{.interpreted-text role="class"} for mailboxes in mbox format. Parameter *factory* is a callable object that accepts a file-like message representation (which behaves as if opened in binary mode) and returns a custom representation. If *factory* is `None`, `mboxMessage`{.interpreted-text role="class"} is used as the default message representation. If *create* is `True`, the mailbox is created if it does not exist.

The mbox format is the classic format for storing mail on Unix systems. All messages in an mbox mailbox are stored in a single file with the beginning of each message indicated by a line whose first five characters are \"From \".

Several variations of the mbox format exist to address perceived shortcomings in the original. In the interest of compatibility, `!mbox`{.interpreted-text role="class"} implements the original format, which is sometimes referred to as `mboxo`{.interpreted-text role="dfn"}. This means that the `Content-Length`{.interpreted-text role="mailheader"} header, if present, is ignored and that any occurrences of \"From \" at the beginning of a line in a message body are transformed to \"\>From \" when storing the message, although occurrences of \"\>From \" are not transformed to \"From \" when reading the message.

Some `Mailbox`{.interpreted-text role="class"} methods implemented by `!mbox`{.interpreted-text role="class"} deserve special remarks:

::: method
get_bytes(key, [from]()=False)

Note: This method has an extra parameter (*from\_*) compared with other classes. The first line of an mbox file entry is the Unix \"From \" line. If *from\_* is False, the first line of the file is dropped.
:::

::: method
get_file(key, [from]()=False)

Using the file after calling `~Mailbox.flush`{.interpreted-text role="meth"} or `~Mailbox.close`{.interpreted-text role="meth"} on the `!mbox`{.interpreted-text role="class"} instance may yield unpredictable results or raise an exception.

Note: This method has an extra parameter (*from\_*) compared with other classes. The first line of an mbox file entry is the Unix \"From \" line. If *from\_* is False, the first line of the file is dropped.
:::

::: method
get_string(key, [from]()=False)

Note: This method has an extra parameter (*from\_*) compared with other classes. The first line of an mbox file entry is the Unix \"From \" line. If *from\_* is False, the first line of the file is dropped.
:::

::: method
lock() unlock()

Three locking mechanisms are used\-\--dot locking and, if available, the `!flock`{.interpreted-text role="c:func"} and `!lockf`{.interpreted-text role="c:func"} system calls.
:::
:::::::

::: seealso

[mbox man page from tin](http://www.tin.org/bin/man.cgi?section=5&topic=mbox)

:   A specification of the format, with details on locking.

[Configuring Netscape Mail on Unix: Why The Content-Length Format is Bad](https://www.jwz.org/doc/content-length.html)

:   An argument for using the original mbox format rather than a variation.

[\"mbox\" is a family of several mutually incompatible mailbox formats](https://www.loc.gov/preservation/digital/formats/fdd/fdd000383.shtml)

:   A history of mbox variations.
:::

### `!MH`{.interpreted-text role="class"} objects {#mailbox-mh}

:::::::::::::::::: {.MH(path, .factory=None, .create=True)}
A subclass of `Mailbox`{.interpreted-text role="class"} for mailboxes in MH format. Parameter *factory* is a callable object that accepts a file-like message representation (which behaves as if opened in binary mode) and returns a custom representation. If *factory* is `None`, `MHMessage`{.interpreted-text role="class"} is used as the default message representation. If *create* is `True`, the mailbox is created if it does not exist.

MH is a directory-based mailbox format invented for the MH Message Handling System, a mail user agent. Each message in an MH mailbox resides in its own file. An MH mailbox may contain other MH mailboxes (called `folders`{.interpreted-text role="dfn"}) in addition to messages. Folders may be nested indefinitely. MH mailboxes also support `sequences`{.interpreted-text role="dfn"}, which are named lists used to logically group messages without moving them to sub-folders. Sequences are defined in a file called `.mh_sequences`{.interpreted-text role="file"} in each folder.

The `!MH`{.interpreted-text role="class"} class manipulates MH mailboxes, but it does not attempt to emulate all of `mh`{.interpreted-text role="program"}\'s behaviors. In particular, it does not modify and is not affected by the `context`{.interpreted-text role="file"} or `.mh_profile`{.interpreted-text role="file"} files that are used by `mh`{.interpreted-text role="program"} to store its state and configuration.

`!MH`{.interpreted-text role="class"} instances have all of the methods of `Mailbox`{.interpreted-text role="class"} in addition to the following:

::: versionchanged
3.13

Supported folders that don\'t contain a `.mh_sequences`{.interpreted-text role="file"} file.
:::

::: method
list_folders()

Return a list of the names of all folders.
:::

::: method
get_folder(folder)

Return an `!MH`{.interpreted-text role="class"} instance representing the folder whose name is *folder*. A `NoSuchMailboxError`{.interpreted-text role="exc"} exception is raised if the folder does not exist.
:::

::: method
add_folder(folder)

Create a folder whose name is *folder* and return an `!MH`{.interpreted-text role="class"} instance representing it.
:::

::: method
remove_folder(folder)

Delete the folder whose name is *folder*. If the folder contains any messages, a `NotEmptyError`{.interpreted-text role="exc"} exception will be raised and the folder will not be deleted.
:::

::: method
get_sequences()

Return a dictionary of sequence names mapped to key lists. If there are no sequences, the empty dictionary is returned.
:::

::: method
set_sequences(sequences)

Re-define the sequences that exist in the mailbox based upon *sequences*, a dictionary of names mapped to key lists, like returned by `get_sequences`{.interpreted-text role="meth"}.
:::

::::: method
pack()

Rename messages in the mailbox as necessary to eliminate gaps in numbering. Entries in the sequences list are updated correspondingly.

:::: note
::: title
Note
:::

Already-issued keys are invalidated by this operation and should not be subsequently used.
::::
:::::

Some `Mailbox`{.interpreted-text role="class"} methods implemented by `!MH`{.interpreted-text role="class"} deserve special remarks:

::: method
remove(key) \_\_delitem\_\_(key) discard(key)

These methods immediately delete the message. The MH convention of marking a message for deletion by prepending a comma to its name is not used.
:::

::: method
lock() unlock()

Three locking mechanisms are used\-\--dot locking and, if available, the `!flock`{.interpreted-text role="c:func"} and `!lockf`{.interpreted-text role="c:func"} system calls. For MH mailboxes, locking the mailbox means locking the `.mh_sequences`{.interpreted-text role="file"} file and, only for the duration of any operations that affect them, locking individual message files.
:::

::: method
get_file(key)

Depending upon the host platform, it may not be possible to remove the underlying message while the returned file remains open.
:::

::: method
flush()

All changes to MH mailboxes are immediately applied, so this method does nothing.
:::

::: method
close()

`!MH`{.interpreted-text role="class"} instances do not keep any open files, so this method is equivalent to `unlock`{.interpreted-text role="meth"}.
:::
::::::::::::::::::

::: seealso

[nmh - Message Handling System](https://www.nongnu.org/nmh/)

:   Home page of `nmh`{.interpreted-text role="program"}, an updated version of the original `mh`{.interpreted-text role="program"}.

[MH & nmh: Email for Users & Programmers](https://rand-mh.sourceforge.io/book/)

:   A GPL-licensed book on `mh`{.interpreted-text role="program"} and `nmh`{.interpreted-text role="program"}, with some information on the mailbox format.
:::

### `!Babyl`{.interpreted-text role="class"} objects {#mailbox-babyl}

:::::::: {.Babyl(path, .factory=None, .create=True)}
A subclass of `Mailbox`{.interpreted-text role="class"} for mailboxes in Babyl format. Parameter *factory* is a callable object that accepts a file-like message representation (which behaves as if opened in binary mode) and returns a custom representation. If *factory* is `None`, `BabylMessage`{.interpreted-text role="class"} is used as the default message representation. If *create* is `True`, the mailbox is created if it does not exist.

Babyl is a single-file mailbox format used by the Rmail mail user agent included with Emacs. The beginning of a message is indicated by a line containing the two characters Control-Underscore (`'\037'`) and Control-L (`'\014'`). The end of a message is indicated by the start of the next message or, in the case of the last message, a line containing a Control-Underscore (`'\037'`) character.

Messages in a Babyl mailbox have two sets of headers, original headers and so-called visible headers. Visible headers are typically a subset of the original headers that have been reformatted or abridged to be more attractive. Each message in a Babyl mailbox also has an accompanying list of `labels`{.interpreted-text role="dfn"}, or short strings that record extra information about the message, and a list of all user-defined labels found in the mailbox is kept in the Babyl options section.

`!Babyl`{.interpreted-text role="class"} instances have all of the methods of `Mailbox`{.interpreted-text role="class"} in addition to the following:

::::: method
get_labels()

Return a list of the names of all user-defined labels used in the mailbox.

:::: note
::: title
Note
:::

The actual messages are inspected to determine which labels exist in the mailbox rather than consulting the list of labels in the Babyl options section, but the Babyl section is updated whenever the mailbox is modified.
::::
:::::

Some `Mailbox`{.interpreted-text role="class"} methods implemented by `!Babyl`{.interpreted-text role="class"} deserve special remarks:

::: method
get_file(key)

In Babyl mailboxes, the headers of a message are not stored contiguously with the body of the message. To generate a file-like representation, the headers and body are copied together into an `io.BytesIO`{.interpreted-text role="class"} instance, which has an API identical to that of a file. As a result, the file-like object is truly independent of the underlying mailbox but does not save memory compared to a string representation.
:::

::: method
lock() unlock()

Three locking mechanisms are used\-\--dot locking and, if available, the `!flock`{.interpreted-text role="c:func"} and `!lockf`{.interpreted-text role="c:func"} system calls.
:::
::::::::

::: seealso

[Format of Version 5 Babyl Files](https://quimby.gnus.org/notes/BABYL)

:   A specification of the Babyl format.

[Reading Mail with Rmail](https://www.gnu.org/software/emacs/manual/html_node/emacs/Rmail.html)

:   The Rmail manual, with some information on Babyl semantics.
:::

### `!MMDF`{.interpreted-text role="class"} objects {#mailbox-mmdf}

:::::: {.MMDF(path, .factory=None, .create=True)}
A subclass of `Mailbox`{.interpreted-text role="class"} for mailboxes in MMDF format. Parameter *factory* is a callable object that accepts a file-like message representation (which behaves as if opened in binary mode) and returns a custom representation. If *factory* is `None`, `MMDFMessage`{.interpreted-text role="class"} is used as the default message representation. If *create* is `True`, the mailbox is created if it does not exist.

MMDF is a single-file mailbox format invented for the Multichannel Memorandum Distribution Facility, a mail transfer agent. Each message is in the same form as an mbox message but is bracketed before and after by lines containing four Control-A (`'\001'`) characters. As with the mbox format, the beginning of each message is indicated by a line whose first five characters are \"From \", but additional occurrences of \"From \" are not transformed to \"\>From \" when storing messages because the extra message separator lines prevent mistaking such occurrences for the starts of subsequent messages.

Some `Mailbox`{.interpreted-text role="class"} methods implemented by `!MMDF`{.interpreted-text role="class"} deserve special remarks:

::: method
get_bytes(key, [from]()=False)

Note: This method has an extra parameter (*from\_*) compared with other classes. The first line of an mbox file entry is the Unix \"From \" line. If *from\_* is False, the first line of the file is dropped.
:::

::: method
get_file(key, [from]()=False)

Using the file after calling `~Mailbox.flush`{.interpreted-text role="meth"} or `~Mailbox.close`{.interpreted-text role="meth"} on the `!MMDF`{.interpreted-text role="class"} instance may yield unpredictable results or raise an exception.

Note: This method has an extra parameter (*from\_*) compared with other classes. The first line of an mbox file entry is the Unix \"From \" line. If *from\_* is False, the first line of the file is dropped.
:::

::: method
lock() unlock()

Three locking mechanisms are used\-\--dot locking and, if available, the `!flock`{.interpreted-text role="c:func"} and `!lockf`{.interpreted-text role="c:func"} system calls.
:::
::::::

::: seealso

[mmdf man page from tin](http://www.tin.org/bin/man.cgi?section=5&topic=mmdf)

:   A specification of MMDF format from the documentation of tin, a newsreader.

[MMDF](https://en.wikipedia.org/wiki/MMDF)

:   A Wikipedia article describing the Multichannel Memorandum Distribution Facility.
:::

## `!Message`{.interpreted-text role="class"} objects {#mailbox-message-objects}

::: Message(message=None)
A subclass of the `email.message`{.interpreted-text role="mod"} module\'s `~email.message.Message`{.interpreted-text role="class"}. Subclasses of `!mailbox.Message`{.interpreted-text role="class"} add mailbox-format-specific state and behavior.

If *message* is omitted, the new instance is created in a default, empty state. If *message* is an `email.message.Message`{.interpreted-text role="class"} instance, its contents are copied; furthermore, any format-specific information is converted insofar as possible if *message* is a `!Message`{.interpreted-text role="class"} instance. If *message* is a string, a byte string, or a file, it should contain an `5322`{.interpreted-text role="rfc"}-compliant message, which is read and parsed. Files should be open in binary mode, but text mode files are accepted for backward compatibility.

The format-specific state and behaviors offered by subclasses vary, but in general it is only the properties that are not specific to a particular mailbox that are supported (although presumably the properties are specific to a particular mailbox format). For example, file offsets for single-file mailbox formats and file names for directory-based mailbox formats are not retained, because they are only applicable to the original mailbox. But state such as whether a message has been read by the user or marked as important is retained, because it applies to the message itself.

There is no requirement that `!Message`{.interpreted-text role="class"} instances be used to represent messages retrieved using `Mailbox`{.interpreted-text role="class"} instances. In some situations, the time and memory required to generate `!Message`{.interpreted-text role="class"} representations might not be acceptable. For such situations, `!Mailbox`{.interpreted-text role="class"} instances also offer string and file-like representations, and a custom message factory may be specified when a `!Mailbox`{.interpreted-text role="class"} instance is initialized.
:::

### `!MaildirMessage`{.interpreted-text role="class"} objects {#mailbox-maildirmessage}

::::::::::::::: MaildirMessage(message=None)
A message with Maildir-specific behaviors. Parameter *message* has the same meaning as with the `Message`{.interpreted-text role="class"} constructor.

Typically, a mail user agent application moves all of the messages in the `new`{.interpreted-text role="file"} subdirectory to the `cur`{.interpreted-text role="file"} subdirectory after the first time the user opens and closes the mailbox, recording that the messages are old whether or not they\'ve actually been read. Each message in `cur`{.interpreted-text role="file"} has an \"info\" section added to its file name to store information about its state. (Some mail readers may also add an \"info\" section to messages in `new`{.interpreted-text role="file"}.) The \"info\" section may take one of two forms: it may contain \"2,\" followed by a list of standardized flags (e.g., \"2,FR\") or it may contain \"1,\" followed by so-called experimental information. Standard flags for Maildir messages are as follows:

  -------------------------------------------------
  Flag   Meaning   Explanation
  ------ --------- --------------------------------
  D      Draft     Under composition

  F      Flagged   Marked as important

  P      Passed    Forwarded, resent, or bounced

  R      Replied   Replied to

  S      Seen      Read

  T      Trashed   Marked for subsequent deletion
  -------------------------------------------------

`!MaildirMessage`{.interpreted-text role="class"} instances offer the following methods:

::::: method
get_subdir()

Return either \"new\" (if the message should be stored in the `new`{.interpreted-text role="file"} subdirectory) or \"cur\" (if the message should be stored in the `cur`{.interpreted-text role="file"} subdirectory).

:::: note
::: title
Note
:::

A message is typically moved from `new`{.interpreted-text role="file"} to `cur`{.interpreted-text role="file"} after its mailbox has been accessed, whether or not the message has been read. A message `msg` has been read if `"S" in msg.get_flags()` is `True`.
::::
:::::

::: method
set_subdir(subdir)

Set the subdirectory the message should be stored in. Parameter *subdir* must be either \"new\" or \"cur\".
:::

::: method
get_flags()

Return a string specifying the flags that are currently set. If the message complies with the standard Maildir format, the result is the concatenation in alphabetical order of zero or one occurrence of each of `'D'`, `'F'`, `'P'`, `'R'`, `'S'`, and `'T'`. The empty string is returned if no flags are set or if \"info\" contains experimental semantics.
:::

::: method
set_flags(flags)

Set the flags specified by *flags* and unset all others.
:::

::: method
add_flag(flag)

Set the flag(s) specified by *flag* without changing other flags. To add more than one flag at a time, *flag* may be a string of more than one character. The current \"info\" is overwritten whether or not it contains experimental information rather than flags.
:::

::: method
remove_flag(flag)

Unset the flag(s) specified by *flag* without changing other flags. To remove more than one flag at a time, *flag* may be a string of more than one character. If \"info\" contains experimental information rather than flags, the current \"info\" is not modified.
:::

::: method
get_date()

Return the delivery date of the message as a floating-point number representing seconds since the epoch.
:::

::: method
set_date(date)

Set the delivery date of the message to *date*, a floating-point number representing seconds since the epoch.
:::

::: method
get_info()

Return a string containing the \"info\" for a message. This is useful for accessing and modifying \"info\" that is experimental (i.e., not a list of flags).
:::

::: method
set_info(info)

Set \"info\" to *info*, which should be a string.
:::
:::::::::::::::

When a `!MaildirMessage`{.interpreted-text role="class"} instance is created based upon an `mboxMessage`{.interpreted-text role="class"} or `MMDFMessage`{.interpreted-text role="class"} instance, the `Status`{.interpreted-text role="mailheader"} and `X-Status`{.interpreted-text role="mailheader"} headers are omitted and the following conversions take place:

  -----------------------------------------------------------------------------------------------------------------------------
  Resulting state        `mboxMessage`{.interpreted-text role="class"} or `MMDFMessage`{.interpreted-text role="class"} state
  ---------------------- ------------------------------------------------------------------------------------------------------
  \"cur\" subdirectory   O flag

  F flag                 F flag

  R flag                 A flag

  S flag                 R flag

  T flag                 D flag
  -----------------------------------------------------------------------------------------------------------------------------

When a `!MaildirMessage`{.interpreted-text role="class"} instance is created based upon an `MHMessage`{.interpreted-text role="class"} instance, the following conversions take place:

  -------------------------------------------------------------------------------------
  Resulting state                   `MHMessage`{.interpreted-text role="class"} state
  --------------------------------- ---------------------------------------------------
  \"cur\" subdirectory              \"unseen\" sequence

  \"cur\" subdirectory and S flag   no \"unseen\" sequence

  F flag                            \"flagged\" sequence

  R flag                            \"replied\" sequence
  -------------------------------------------------------------------------------------

When a `!MaildirMessage`{.interpreted-text role="class"} instance is created based upon a `BabylMessage`{.interpreted-text role="class"} instance, the following conversions take place:

  ----------------------------------------------------------------------------------------
  Resulting state                   `BabylMessage`{.interpreted-text role="class"} state
  --------------------------------- ------------------------------------------------------
  \"cur\" subdirectory              \"unseen\" label

  \"cur\" subdirectory and S flag   no \"unseen\" label

  P flag                            \"forwarded\" or \"resent\" label

  R flag                            \"answered\" label

  T flag                            \"deleted\" label
  ----------------------------------------------------------------------------------------

### `!mboxMessage`{.interpreted-text role="class"} objects {#mailbox-mboxmessage}

::::::::: mboxMessage(message=None)
A message with mbox-specific behaviors. Parameter *message* has the same meaning as with the `Message`{.interpreted-text role="class"} constructor.

Messages in an mbox mailbox are stored together in a single file. The sender\'s envelope address and the time of delivery are typically stored in a line beginning with \"From \" that is used to indicate the start of a message, though there is considerable variation in the exact format of this data among mbox implementations. Flags that indicate the state of the message, such as whether it has been read or marked as important, are typically stored in `Status`{.interpreted-text role="mailheader"} and `X-Status`{.interpreted-text role="mailheader"} headers.

Conventional flags for mbox messages are as follows:

  --------------------------------------------------
  Flag   Meaning    Explanation
  ------ ---------- --------------------------------
  R      Read       Read

  O      Old        Previously detected by MUA

  D      Deleted    Marked for subsequent deletion

  F      Flagged    Marked as important

  A      Answered   Replied to
  --------------------------------------------------

The \"R\" and \"O\" flags are stored in the `Status`{.interpreted-text role="mailheader"} header, and the \"D\", \"F\", and \"A\" flags are stored in the `X-Status`{.interpreted-text role="mailheader"} header. The flags and headers typically appear in the order mentioned.

`!mboxMessage`{.interpreted-text role="class"} instances offer the following methods:

::: method
get_from()

Return a string representing the \"From \" line that marks the start of the message in an mbox mailbox. The leading \"From \" and the trailing newline are excluded.
:::

::: method
set_from([from](), [time]()=None)

Set the \"From \" line to *from\_*, which should be specified without a leading \"From \" or trailing newline. For convenience, *time\_* may be specified and will be formatted appropriately and appended to *from\_*. If *time\_* is specified, it should be a `time.struct_time`{.interpreted-text role="class"} instance, a tuple suitable for passing to `time.strftime`{.interpreted-text role="func"}, or `True` (to use `time.gmtime`{.interpreted-text role="func"}).
:::

::: method
get_flags()

Return a string specifying the flags that are currently set. If the message complies with the conventional format, the result is the concatenation in the following order of zero or one occurrence of each of `'R'`, `'O'`, `'D'`, `'F'`, and `'A'`.
:::

::: method
set_flags(flags)

Set the flags specified by *flags* and unset all others. Parameter *flags* should be the concatenation in any order of zero or more occurrences of each of `'R'`, `'O'`, `'D'`, `'F'`, and `'A'`.
:::

::: method
add_flag(flag)

Set the flag(s) specified by *flag* without changing other flags. To add more than one flag at a time, *flag* may be a string of more than one character.
:::

::: method
remove_flag(flag)

Unset the flag(s) specified by *flag* without changing other flags. To remove more than one flag at a time, *flag* may be a string of more than one character.
:::
:::::::::

When an `!mboxMessage`{.interpreted-text role="class"} instance is created based upon a `MaildirMessage`{.interpreted-text role="class"} instance, a \"From \" line is generated based upon the `MaildirMessage`{.interpreted-text role="class"} instance\'s delivery date, and the following conversions take place:

  --------------------------------------------------------------------------
  Resulting state   `MaildirMessage`{.interpreted-text role="class"} state
  ----------------- --------------------------------------------------------
  R flag            S flag

  O flag            \"cur\" subdirectory

  D flag            T flag

  F flag            F flag

  A flag            R flag
  --------------------------------------------------------------------------

When an `!mboxMessage`{.interpreted-text role="class"} instance is created based upon an `MHMessage`{.interpreted-text role="class"} instance, the following conversions take place:

  -----------------------------------------------------------------------
  Resulting state     `MHMessage`{.interpreted-text role="class"} state
  ------------------- ---------------------------------------------------
  R flag and O flag   no \"unseen\" sequence

  O flag              \"unseen\" sequence

  F flag              \"flagged\" sequence

  A flag              \"replied\" sequence
  -----------------------------------------------------------------------

When an `!mboxMessage`{.interpreted-text role="class"} instance is created based upon a `BabylMessage`{.interpreted-text role="class"} instance, the following conversions take place:

  --------------------------------------------------------------------------
  Resulting state     `BabylMessage`{.interpreted-text role="class"} state
  ------------------- ------------------------------------------------------
  R flag and O flag   no \"unseen\" label

  O flag              \"unseen\" label

  D flag              \"deleted\" label

  A flag              \"answered\" label
  --------------------------------------------------------------------------

When a `!mboxMessage`{.interpreted-text role="class"} instance is created based upon an `MMDFMessage`{.interpreted-text role="class"} instance, the \"From \" line is copied and all flags directly correspond:

  -----------------------------------------------------------------------
  Resulting state   `MMDFMessage`{.interpreted-text role="class"} state
  ----------------- -----------------------------------------------------
  R flag            R flag

  O flag            O flag

  D flag            D flag

  F flag            F flag

  A flag            A flag
  -----------------------------------------------------------------------

### `!MHMessage`{.interpreted-text role="class"} objects {#mailbox-mhmessage}

::::::: MHMessage(message=None)
A message with MH-specific behaviors. Parameter *message* has the same meaning as with the `Message`{.interpreted-text role="class"} constructor.

MH messages do not support marks or flags in the traditional sense, but they do support sequences, which are logical groupings of arbitrary messages. Some mail reading programs (although not the standard `mh`{.interpreted-text role="program"} and `nmh`{.interpreted-text role="program"}) use sequences in much the same way flags are used with other formats, as follows:

  -----------------------------------------------------
  Sequence   Explanation
  ---------- ------------------------------------------
  unseen     Not read, but previously detected by MUA

  replied    Replied to

  flagged    Marked as important
  -----------------------------------------------------

`!MHMessage`{.interpreted-text role="class"} instances offer the following methods:

::: method
get_sequences()

Return a list of the names of sequences that include this message.
:::

::: method
set_sequences(sequences)

Set the list of sequences that include this message.
:::

::: method
add_sequence(sequence)

Add *sequence* to the list of sequences that include this message.
:::

::: method
remove_sequence(sequence)

Remove *sequence* from the list of sequences that include this message.
:::
:::::::

When an `!MHMessage`{.interpreted-text role="class"} instance is created based upon a `MaildirMessage`{.interpreted-text role="class"} instance, the following conversions take place:

  -------------------------------------------------------------------------------
  Resulting state        `MaildirMessage`{.interpreted-text role="class"} state
  ---------------------- --------------------------------------------------------
  \"unseen\" sequence    no S flag

  \"replied\" sequence   R flag

  \"flagged\" sequence   F flag
  -------------------------------------------------------------------------------

When an `!MHMessage`{.interpreted-text role="class"} instance is created based upon an `mboxMessage`{.interpreted-text role="class"} or `MMDFMessage`{.interpreted-text role="class"} instance, the `Status`{.interpreted-text role="mailheader"} and `X-Status`{.interpreted-text role="mailheader"} headers are omitted and the following conversions take place:

  -----------------------------------------------------------------------------------------------------------------------------
  Resulting state        `mboxMessage`{.interpreted-text role="class"} or `MMDFMessage`{.interpreted-text role="class"} state
  ---------------------- ------------------------------------------------------------------------------------------------------
  \"unseen\" sequence    no R flag

  \"replied\" sequence   A flag

  \"flagged\" sequence   F flag
  -----------------------------------------------------------------------------------------------------------------------------

When an `!MHMessage`{.interpreted-text role="class"} instance is created based upon a `BabylMessage`{.interpreted-text role="class"} instance, the following conversions take place:

  -----------------------------------------------------------------------------
  Resulting state        `BabylMessage`{.interpreted-text role="class"} state
  ---------------------- ------------------------------------------------------
  \"unseen\" sequence    \"unseen\" label

  \"replied\" sequence   \"answered\" label
  -----------------------------------------------------------------------------

### `!BabylMessage`{.interpreted-text role="class"} objects {#mailbox-babylmessage}

:::::::::: BabylMessage(message=None)
A message with Babyl-specific behaviors. Parameter *message* has the same meaning as with the `Message`{.interpreted-text role="class"} constructor.

Certain message labels, called `attributes`{.interpreted-text role="dfn"}, are defined by convention to have special meanings. The attributes are as follows:

  ------------------------------------------------------
  Label       Explanation
  ----------- ------------------------------------------
  unseen      Not read, but previously detected by MUA

  deleted     Marked for subsequent deletion

  filed       Copied to another file or mailbox

  answered    Replied to

  forwarded   Forwarded

  edited      Modified by the user

  resent      Resent
  ------------------------------------------------------

By default, Rmail displays only visible headers. The `!BabylMessage`{.interpreted-text role="class"} class, though, uses the original headers because they are more complete. Visible headers may be accessed explicitly if desired.

`!BabylMessage`{.interpreted-text role="class"} instances offer the following methods:

::: method
get_labels()

Return a list of labels on the message.
:::

::: method
set_labels(labels)

Set the list of labels on the message to *labels*.
:::

::: method
add_label(label)

Add *label* to the list of labels on the message.
:::

::: method
remove_label(label)

Remove *label* from the list of labels on the message.
:::

::: method
get_visible()

Return a `Message`{.interpreted-text role="class"} instance whose headers are the message\'s visible headers and whose body is empty.
:::

::: method
set_visible(visible)

Set the message\'s visible headers to be the same as the headers in *message*. Parameter *visible* should be a `Message`{.interpreted-text role="class"} instance, an `email.message.Message`{.interpreted-text role="class"} instance, a string, or a file-like object (which should be open in text mode).
:::

::: method
update_visible()

When a `!BabylMessage`{.interpreted-text role="class"} instance\'s original headers are modified, the visible headers are not automatically modified to correspond. This method updates the visible headers as follows: each visible header with a corresponding original header is set to the value of the original header, each visible header without a corresponding original header is removed, and any of `Date`{.interpreted-text role="mailheader"}, `From`{.interpreted-text role="mailheader"}, `Reply-To`{.interpreted-text role="mailheader"}, `To`{.interpreted-text role="mailheader"}, `CC`{.interpreted-text role="mailheader"}, and `Subject`{.interpreted-text role="mailheader"} that are present in the original headers but not the visible headers are added to the visible headers.
:::
::::::::::

When a `!BabylMessage`{.interpreted-text role="class"} instance is created based upon a `MaildirMessage`{.interpreted-text role="class"} instance, the following conversions take place:

  ------------------------------------------------------------------------------
  Resulting state       `MaildirMessage`{.interpreted-text role="class"} state
  --------------------- --------------------------------------------------------
  \"unseen\" label      no S flag

  \"deleted\" label     T flag

  \"answered\" label    R flag

  \"forwarded\" label   P flag
  ------------------------------------------------------------------------------

When a `!BabylMessage`{.interpreted-text role="class"} instance is created based upon an `mboxMessage`{.interpreted-text role="class"} or `MMDFMessage`{.interpreted-text role="class"} instance, the `Status`{.interpreted-text role="mailheader"} and `X-Status`{.interpreted-text role="mailheader"} headers are omitted and the following conversions take place:

  ---------------------------------------------------------------------------------------------------------------------------
  Resulting state      `mboxMessage`{.interpreted-text role="class"} or `MMDFMessage`{.interpreted-text role="class"} state
  -------------------- ------------------------------------------------------------------------------------------------------
  \"unseen\" label     no R flag

  \"deleted\" label    D flag

  \"answered\" label   A flag
  ---------------------------------------------------------------------------------------------------------------------------

When a `!BabylMessage`{.interpreted-text role="class"} instance is created based upon an `MHMessage`{.interpreted-text role="class"} instance, the following conversions take place:

  ------------------------------------------------------------------------
  Resulting state      `MHMessage`{.interpreted-text role="class"} state
  -------------------- ---------------------------------------------------
  \"unseen\" label     \"unseen\" sequence

  \"answered\" label   \"replied\" sequence
  ------------------------------------------------------------------------

### `!MMDFMessage`{.interpreted-text role="class"} objects {#mailbox-mmdfmessage}

::::::::: MMDFMessage(message=None)
A message with MMDF-specific behaviors. Parameter *message* has the same meaning as with the `Message`{.interpreted-text role="class"} constructor.

As with message in an mbox mailbox, MMDF messages are stored with the sender\'s address and the delivery date in an initial line beginning with \"From \". Likewise, flags that indicate the state of the message are typically stored in `Status`{.interpreted-text role="mailheader"} and `X-Status`{.interpreted-text role="mailheader"} headers.

Conventional flags for MMDF messages are identical to those of mbox message and are as follows:

  --------------------------------------------------
  Flag   Meaning    Explanation
  ------ ---------- --------------------------------
  R      Read       Read

  O      Old        Previously detected by MUA

  D      Deleted    Marked for subsequent deletion

  F      Flagged    Marked as important

  A      Answered   Replied to
  --------------------------------------------------

The \"R\" and \"O\" flags are stored in the `Status`{.interpreted-text role="mailheader"} header, and the \"D\", \"F\", and \"A\" flags are stored in the `X-Status`{.interpreted-text role="mailheader"} header. The flags and headers typically appear in the order mentioned.

`!MMDFMessage`{.interpreted-text role="class"} instances offer the following methods, which are identical to those offered by `mboxMessage`{.interpreted-text role="class"}:

::: method
get_from()

Return a string representing the \"From \" line that marks the start of the message in an mbox mailbox. The leading \"From \" and the trailing newline are excluded.
:::

::: method
set_from([from](), [time]()=None)

Set the \"From \" line to *from\_*, which should be specified without a leading \"From \" or trailing newline. For convenience, *time\_* may be specified and will be formatted appropriately and appended to *from\_*. If *time\_* is specified, it should be a `time.struct_time`{.interpreted-text role="class"} instance, a tuple suitable for passing to `time.strftime`{.interpreted-text role="func"}, or `True` (to use `time.gmtime`{.interpreted-text role="func"}).
:::

::: method
get_flags()

Return a string specifying the flags that are currently set. If the message complies with the conventional format, the result is the concatenation in the following order of zero or one occurrence of each of `'R'`, `'O'`, `'D'`, `'F'`, and `'A'`.
:::

::: method
set_flags(flags)

Set the flags specified by *flags* and unset all others. Parameter *flags* should be the concatenation in any order of zero or more occurrences of each of `'R'`, `'O'`, `'D'`, `'F'`, and `'A'`.
:::

::: method
add_flag(flag)

Set the flag(s) specified by *flag* without changing other flags. To add more than one flag at a time, *flag* may be a string of more than one character.
:::

::: method
remove_flag(flag)

Unset the flag(s) specified by *flag* without changing other flags. To remove more than one flag at a time, *flag* may be a string of more than one character.
:::
:::::::::

When an `!MMDFMessage`{.interpreted-text role="class"} instance is created based upon a `MaildirMessage`{.interpreted-text role="class"} instance, a \"From \" line is generated based upon the `MaildirMessage`{.interpreted-text role="class"} instance\'s delivery date, and the following conversions take place:

  --------------------------------------------------------------------------
  Resulting state   `MaildirMessage`{.interpreted-text role="class"} state
  ----------------- --------------------------------------------------------
  R flag            S flag

  O flag            \"cur\" subdirectory

  D flag            T flag

  F flag            F flag

  A flag            R flag
  --------------------------------------------------------------------------

When an `!MMDFMessage`{.interpreted-text role="class"} instance is created based upon an `MHMessage`{.interpreted-text role="class"} instance, the following conversions take place:

  -----------------------------------------------------------------------
  Resulting state     `MHMessage`{.interpreted-text role="class"} state
  ------------------- ---------------------------------------------------
  R flag and O flag   no \"unseen\" sequence

  O flag              \"unseen\" sequence

  F flag              \"flagged\" sequence

  A flag              \"replied\" sequence
  -----------------------------------------------------------------------

When an `!MMDFMessage`{.interpreted-text role="class"} instance is created based upon a `BabylMessage`{.interpreted-text role="class"} instance, the following conversions take place:

  --------------------------------------------------------------------------
  Resulting state     `BabylMessage`{.interpreted-text role="class"} state
  ------------------- ------------------------------------------------------
  R flag and O flag   no \"unseen\" label

  O flag              \"unseen\" label

  D flag              \"deleted\" label

  A flag              \"answered\" label
  --------------------------------------------------------------------------

When an `!MMDFMessage`{.interpreted-text role="class"} instance is created based upon an `mboxMessage`{.interpreted-text role="class"} instance, the \"From \" line is copied and all flags directly correspond:

  -----------------------------------------------------------------------
  Resulting state   `mboxMessage`{.interpreted-text role="class"} state
  ----------------- -----------------------------------------------------
  R flag            R flag

  O flag            O flag

  D flag            D flag

  F flag            F flag

  A flag            A flag
  -----------------------------------------------------------------------

## Exceptions

The following exception classes are defined in the `!mailbox`{.interpreted-text role="mod"} module:

::: exception
Error()

The base class for all other module-specific exceptions.
:::

::: exception
NoSuchMailboxError()

Raised when a mailbox is expected but is not found, such as when instantiating a `Mailbox`{.interpreted-text role="class"} subclass with a path that does not exist (and with the *create* parameter set to `False`), or when opening a folder that does not exist.
:::

::: exception
NotEmptyError()

Raised when a mailbox is not empty but is expected to be, such as when deleting a folder that contains messages.
:::

::: exception
ExternalClashError()

Raised when some mailbox-related condition beyond the control of the program causes it to be unable to proceed, such as when failing to acquire a lock that another program already holds, or when a uniquely generated file name already exists.
:::

::: exception
FormatError()

Raised when the data in a file cannot be parsed, such as when an `MH`{.interpreted-text role="class"} instance attempts to read a corrupted `.mh_sequences`{.interpreted-text role="file"} file.
:::

## Examples {#mailbox-examples}

A simple example of printing the subjects of all messages in a mailbox that seem interesting:

    import mailbox
    for message in mailbox.mbox('~/mbox'):
        subject = message['subject']       # Could possibly be None.
        if subject and 'python' in subject.lower():
            print(subject)

To copy all mail from a Babyl mailbox to an MH mailbox, converting all of the format-specific information that can be converted:

    import mailbox
    destination = mailbox.MH('~/Mail')
    destination.lock()
    for message in mailbox.Babyl('~/RMAIL'):
        destination.add(mailbox.MHMessage(message))
    destination.flush()
    destination.unlock()

This example sorts mail from several mailing lists into different mailboxes, being careful to avoid mail corruption due to concurrent modification by other programs, mail loss due to interruption of the program, or premature termination due to malformed messages in the mailbox:

    import mailbox
    import email.errors

    list_names = ('python-list', 'python-dev', 'python-bugs')

    boxes = {name: mailbox.mbox('~/email/%s' % name) for name in list_names}
    inbox = mailbox.Maildir('~/Maildir', factory=None)

    for key in inbox.iterkeys():
        try:
            message = inbox[key]
        except email.errors.MessageParseError:
            continue                # The message is malformed. Just leave it.

        for name in list_names:
            list_id = message['list-id']
            if list_id and name in list_id:
                # Get mailbox to use
                box = boxes[name]

                # Write copy to disk before removing original.
                # If there's a crash, you might duplicate a message, but
                # that's better than losing a message completely.
                box.lock()
                box.add(message)
                box.flush()
                box.unlock()

                # Remove original message
                inbox.lock()
                inbox.discard(key)
                inbox.flush()
                inbox.unlock()
                break               # Found destination, so stop looking.

    for box in boxes.itervalues():
        box.close()
