# `!xml.sax`{.interpreted-text role="mod"} \-\-- Support for SAX2 parsers

::: {.module synopsis="Package containing SAX2 base classes and convenience functions."}
xml.sax
:::

**Source code:** `Lib/xml/sax/__init__.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!xml.sax`{.interpreted-text role="mod"} package provides a number of modules which implement the Simple API for XML (SAX) interface for Python. The package itself provides the SAX exceptions and the convenience functions which will be most used by users of the SAX API.

:::: note
::: title
Note
:::

If you need to parse untrusted or unauthenticated data, see `xml-security`{.interpreted-text role="ref"}.
::::

::: versionchanged
3.7.1

The SAX parser no longer processes general external entities by default to increase security. Before, the parser created network connections to fetch remote files or loaded local files from the file system for DTD and entities. The feature can be enabled again with method `~xml.sax.xmlreader.XMLReader.setFeature`{.interpreted-text role="meth"} on the parser object and argument `~xml.sax.handler.feature_external_ges`{.interpreted-text role="data"}.
:::

The convenience functions are:

:::: function
make_parser(parser_list=\[\])

Create and return a SAX `~xml.sax.xmlreader.XMLReader`{.interpreted-text role="class"} object. The first parser found will be used. If *parser_list* is provided, it must be an iterable of strings which name modules that have a function named `create_parser`{.interpreted-text role="func"}. Modules listed in *parser_list* will be used before modules in the default list of parsers.

::: versionchanged
3.8 The *parser_list* argument can be any iterable, not just a list.
:::
::::

::: function
parse(filename_or_stream, handler, error_handler=handler.ErrorHandler())

Create a SAX parser and use it to parse a document. The document, passed in as *filename_or_stream*, can be a filename or a file object. The *handler* parameter needs to be a SAX `~handler.ContentHandler`{.interpreted-text role="class"} instance. If *error_handler* is given, it must be a SAX `~handler.ErrorHandler`{.interpreted-text role="class"} instance; if omitted, `SAXParseException`{.interpreted-text role="exc"} will be raised on all errors. There is no return value; all work must be done by the *handler* passed in.
:::

:::: function
parseString(string, handler, error_handler=handler.ErrorHandler())

Similar to `parse`{.interpreted-text role="func"}, but parses from a buffer *string* received as a parameter. *string* must be a `str`{.interpreted-text role="class"} instance or a `bytes-like object`{.interpreted-text role="term"}.

::: versionchanged
3.5 Added support of `str`{.interpreted-text role="class"} instances.
:::
::::

A typical SAX application uses three kinds of objects: readers, handlers and input sources. \"Reader\" in this context is another term for parser, i.e. some piece of code that reads the bytes or characters from the input source, and produces a sequence of events. The events then get distributed to the handler objects, i.e. the reader invokes a method on the handler. A SAX application must therefore obtain a reader object, create or open the input sources, create the handlers, and connect these objects all together. As the final step of preparation, the reader is called to parse the input. During parsing, methods on the handler objects are called based on structural and syntactic events from the input data.

For these objects, only the interfaces are relevant; they are normally not instantiated by the application itself. Since Python does not have an explicit notion of interface, they are formally introduced as classes, but applications may use implementations which do not inherit from the provided classes. The `~xml.sax.xmlreader.InputSource`{.interpreted-text role="class"}, `~xml.sax.xmlreader.Locator`{.interpreted-text role="class"}, `~xml.sax.xmlreader.Attributes`{.interpreted-text role="class"}, `~xml.sax.xmlreader.AttributesNS`{.interpreted-text role="class"}, and `~xml.sax.xmlreader.XMLReader`{.interpreted-text role="class"} interfaces are defined in the module `xml.sax.xmlreader`{.interpreted-text role="mod"}. The handler interfaces are defined in `xml.sax.handler`{.interpreted-text role="mod"}. For convenience, `~xml.sax.xmlreader.InputSource`{.interpreted-text role="class"} (which is often instantiated directly) and the handler classes are also available from `!xml.sax`{.interpreted-text role="mod"}. These interfaces are described below.

In addition to these classes, `!xml.sax`{.interpreted-text role="mod"} provides the following exception classes.

::: exception
SAXException(msg, exception=None)

Encapsulate an XML error or warning. This class can contain basic error or warning information from either the XML parser or the application: it can be subclassed to provide additional functionality or to add localization. Note that although the handlers defined in the `~xml.sax.handler.ErrorHandler`{.interpreted-text role="class"} interface receive instances of this exception, it is not required to actually raise the exception \-\-- it is also useful as a container for information.

When instantiated, *msg* should be a human-readable description of the error. The optional *exception* parameter, if given, should be `None` or an exception that was caught by the parsing code and is being passed along as information.

This is the base class for the other SAX exception classes.
:::

::: exception
SAXParseException(msg, exception, locator)

Subclass of `SAXException`{.interpreted-text role="exc"} raised on parse errors. Instances of this class are passed to the methods of the SAX `~xml.sax.handler.ErrorHandler`{.interpreted-text role="class"} interface to provide information about the parse error. This class supports the SAX `~xml.sax.xmlreader.Locator`{.interpreted-text role="class"} interface as well as the `SAXException`{.interpreted-text role="class"} interface.
:::

::: exception
SAXNotRecognizedException(msg, exception=None)

Subclass of `SAXException`{.interpreted-text role="exc"} raised when a SAX `~xml.sax.xmlreader.XMLReader`{.interpreted-text role="class"} is confronted with an unrecognized feature or property. SAX applications and extensions may use this class for similar purposes.
:::

::: exception
SAXNotSupportedException(msg, exception=None)

Subclass of `SAXException`{.interpreted-text role="exc"} raised when a SAX `~xml.sax.xmlreader.XMLReader`{.interpreted-text role="class"} is asked to enable a feature that is not supported, or to set a property to a value that the implementation does not support. SAX applications and extensions may use this class for similar purposes.
:::

::: seealso

[SAX: The Simple API for XML](http://www.saxproject.org/)

:   This site is the focal point for the definition of the SAX API. It provides a Java implementation and online documentation. Links to implementations and historical information are also available.

Module `xml.sax.handler`{.interpreted-text role="mod"}

:   Definitions of the interfaces for application-provided objects.

Module `xml.sax.saxutils`{.interpreted-text role="mod"}

:   Convenience functions for use in SAX applications.

Module `xml.sax.xmlreader`{.interpreted-text role="mod"}

:   Definitions of the interfaces for parser-provided objects.
:::

## SAXException Objects {#sax-exception-objects}

The `SAXException`{.interpreted-text role="class"} exception class supports the following methods:

::: method
SAXException.getMessage()

Return a human-readable message describing the error condition.
:::

::: method
SAXException.getException()

Return an encapsulated exception object, or `None`.
:::
