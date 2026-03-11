# `!wave`{.interpreted-text role="mod"} \-\-- Read and write WAV files

::: {.module synopsis="Provide an interface to the WAV sound format."}
wave
:::

**Source code:** `Lib/wave.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!wave`{.interpreted-text role="mod"} module provides a convenient interface to the Waveform Audio \"WAVE\" (or \"WAV\") file format. Only uncompressed PCM encoded wave files are supported.

::: versionchanged
3.12

Support for `WAVE_FORMAT_EXTENSIBLE` headers was added, provided that the extended format is `KSDATAFORMAT_SUBTYPE_PCM`.
:::

The `!wave`{.interpreted-text role="mod"} module defines the following function and exception:

::::: function
open(file, mode=None)

If *file* is a string, a `path-like object`{.interpreted-text role="term"} or a `bytes-like object`{.interpreted-text role="term"} open the file by that name, otherwise treat it as a file-like object. *mode* can be:

`'rb'`

:   Read only mode.

`'wb'`

:   Write only mode.

Note that it does not allow read/write WAV files.

A *mode* of `'rb'` returns a `Wave_read`{.interpreted-text role="class"} object, while a *mode* of `'wb'` returns a `Wave_write`{.interpreted-text role="class"} object. If *mode* is omitted and a file-like object is passed as *file*, `file.mode` is used as the default value for *mode*.

If you pass in a file-like object, the wave object will not close it when its `close()` method is called; it is the caller\'s responsibility to close the file object.

The `.open`{.interpreted-text role="func"} function may be used in a `with`{.interpreted-text role="keyword"} statement. When the `!with`{.interpreted-text role="keyword"} block completes, the `Wave_read.close`{.interpreted-text role="meth"} or `Wave_write.close`{.interpreted-text role="meth"} method is called.

::: versionchanged
3.4 Added support for unseekable files.
:::

::: versionchanged
3.15 Added support for `path-like objects <path-like object>`{.interpreted-text role="term"} and `bytes-like objects <bytes-like object>`{.interpreted-text role="term"}.
:::
:::::

::: exception
Error

An error raised when something is impossible because it violates the WAV specification or hits an implementation deficiency.
:::

## Wave_read Objects {#wave-read-objects}

::::::::::::::: Wave_read
Read a WAV file.

Wave_read objects, as returned by `.open`{.interpreted-text role="func"}, have the following methods:

::: method
close()

Close the stream if it was opened by `!wave`{.interpreted-text role="mod"}, and make the instance unusable. This is called automatically on object collection.
:::

::: method
getnchannels()

Returns number of audio channels (`1` for mono, `2` for stereo).
:::

::: method
getsampwidth()

Returns sample width in bytes.
:::

::: method
getframerate()

Returns sampling frequency.
:::

::: method
getnframes()

Returns number of audio frames.
:::

::: method
getcomptype()

Returns compression type (`'NONE'` is the only supported type).
:::

::: method
getcompname()

Human-readable version of `getcomptype`{.interpreted-text role="meth"}. Usually `'not compressed'` parallels `'NONE'`.
:::

::: method
getparams()

Returns a `~collections.namedtuple`{.interpreted-text role="func"} `(nchannels, sampwidth, framerate, nframes, comptype, compname)`, equivalent to output of the `get*()` methods.
:::

::: method
readframes(n)

Reads and returns at most *n* frames of audio, as a `bytes`{.interpreted-text role="class"} object.
:::

::: method
rewind()

Rewind the file pointer to the beginning of the audio stream.
:::

The following two methods define a term \"position\" which is compatible between them, and is otherwise implementation dependent.

::: method
setpos(pos)

Set the file pointer to the specified position.
:::

::: method
tell()

Return current file pointer position.
:::
:::::::::::::::

## Wave_write Objects {#wave-write-objects}

::::::::::::::::: Wave_write
Write a WAV file.

Wave_write objects, as returned by `.open`{.interpreted-text role="func"}.

For seekable output streams, the `wave` header will automatically be updated to reflect the number of frames actually written. For unseekable streams, the *nframes* value must be accurate when the first frame data is written. An accurate *nframes* value can be achieved either by calling `setnframes`{.interpreted-text role="meth"} or `setparams`{.interpreted-text role="meth"} with the number of frames that will be written before `close`{.interpreted-text role="meth"} is called and then using `writeframesraw`{.interpreted-text role="meth"} to write the frame data, or by calling `writeframes`{.interpreted-text role="meth"} with all of the frame data to be written. In the latter case `writeframes`{.interpreted-text role="meth"} will calculate the number of frames in the data and set *nframes* accordingly before writing the frame data.

::: versionchanged
3.4 Added support for unseekable files.
:::

Wave_write objects have the following methods:

::: method
close()

Make sure *nframes* is correct, and close the file if it was opened by `!wave`{.interpreted-text role="mod"}. This method is called upon object collection. It will raise an exception if the output stream is not seekable and *nframes* does not match the number of frames actually written.
:::

::: method
setnchannels(n)

Set the number of channels.
:::

::: method
setsampwidth(n)

Set the sample width to *n* bytes.
:::

:::: method
setframerate(n)

Set the frame rate to *n*.

::: versionchanged
3.2 A non-integral input to this method is rounded to the nearest integer.
:::
::::

::: method
setnframes(n)

Set the number of frames to *n*. This will be changed later if the number of frames actually written is different (this update attempt will raise an error if the output stream is not seekable).
:::

::: method
setcomptype(type, name)

Set the compression type and description. At the moment, only compression type `NONE` is supported, meaning no compression.
:::

::: method
setparams(tuple)

The *tuple* should be `(nchannels, sampwidth, framerate, nframes, comptype, compname)`, with values valid for the `set*()` methods. Sets all parameters.
:::

::: method
tell()

Return current position in the file, with the same disclaimer for the `Wave_read.tell`{.interpreted-text role="meth"} and `Wave_read.setpos`{.interpreted-text role="meth"} methods.
:::

:::: method
writeframesraw(data)

Write audio frames, without correcting *nframes*.

::: versionchanged
3.4 Any `bytes-like object`{.interpreted-text role="term"} is now accepted.
:::
::::

:::: method
writeframes(data)

Write audio frames and make sure *nframes* is correct. It will raise an error if the output stream is not seekable and the total number of frames that have been written after *data* has been written does not match the previously set value for *nframes*.

::: versionchanged
3.4 Any `bytes-like object`{.interpreted-text role="term"} is now accepted.
:::

Note that it is invalid to set any parameters after calling `writeframes`{.interpreted-text role="meth"} or `writeframesraw`{.interpreted-text role="meth"}, and any attempt to do so will raise `wave.Error`{.interpreted-text role="exc"}.
::::
:::::::::::::::::
