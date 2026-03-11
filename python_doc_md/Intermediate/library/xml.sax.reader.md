# `!xml.sax.xmlreader`{.interpreted-text role="mod"} \-\-- Interface for XML parsers

::: {.module synopsis="Interface which SAX-compliant XML parsers must implement."}
xml.sax.xmlreader
:::

**Source code:** `Lib/xml/sax/xmlreader.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

SAX parsers implement the `XMLReader`{.interpreted-text role="class"} interface. They are implemented in a Python module, which must provide a function `create_parser`{.interpreted-text role="func"}. This function is invoked by `xml.sax.make_parser`{.interpreted-text role="func"} with no arguments to create a new parser object.

::: XMLReader()
Base class which can be inherited by SAX parsers.
:::

::: IncrementalParser()
In some cases, it is desirable not to parse an input source at once, but to feed chunks of the document as they get available. Note that the reader will normally not read the entire file, but read it in chunks as well; still `parse`{.interpreted-text role="meth"} won\'t return until the entire document is processed. So these interfaces should be used if the blocking behaviour of `parse`{.interpreted-text role="meth"} is not desirable.

When the parser is instantiated it is ready to begin accepting data from the feed method immediately. After parsing has been finished with a call to close the reset method must be called to make the parser ready to accept new data, either from feed or using the parse method.

Note that these methods must *not* be called during parsing, that is, after parse has been called and before it returns.

By default, the class also implements the parse method of the XMLReader interface using the feed, close and reset methods of the IncrementalParser interface as a convenience to SAX 2.0 driver writers.
:::

::: Locator()
Interface for associating a SAX event with a document location. A locator object will return valid results only during calls to DocumentHandler methods; at any other time, the results are unpredictable. If information is not available, methods may return `None`.
:::

::: InputSource(system_id=None)
Encapsulation of the information needed by the `XMLReader`{.interpreted-text role="class"} to read entities.

This class may include information about the public identifier, system identifier, byte stream (possibly with character encoding information) and/or the character stream of an entity.

Applications will create objects of this class for use in the `XMLReader.parse`{.interpreted-text role="meth"} method and for returning from EntityResolver.resolveEntity.

An `InputSource`{.interpreted-text role="class"} belongs to the application, the `XMLReader`{.interpreted-text role="class"} is not allowed to modify `InputSource`{.interpreted-text role="class"} objects passed to it from the application, although it may make copies and modify those.
:::

::: AttributesImpl(attrs)
This is an implementation of the `Attributes`{.interpreted-text role="class"} interface (see section `attributes-objects`{.interpreted-text role="ref"}). This is a dictionary-like object which represents the element attributes in a `startElement`{.interpreted-text role="meth"} call. In addition to the most useful dictionary operations, it supports a number of other methods as described by the interface. Objects of this class should be instantiated by readers; *attrs* must be a dictionary-like object containing a mapping from attribute names to attribute values.
:::

::: {.AttributesNSImpl(attrs, .qnames)}
Namespace-aware variant of `AttributesImpl`{.interpreted-text role="class"}, which will be passed to `startElementNS`{.interpreted-text role="meth"}. It is derived from `AttributesImpl`{.interpreted-text role="class"}, but understands attribute names as two-tuples of *namespaceURI* and *localname*. In addition, it provides a number of methods expecting qualified names as they appear in the original document. This class implements the `AttributesNS`{.interpreted-text role="class"} interface (see section `attributes-ns-objects`{.interpreted-text role="ref"}).
:::

## XMLReader Objects

The `XMLReader`{.interpreted-text role="class"} interface supports the following methods:

::::: method
XMLReader.parse(source)

Process an input source, producing SAX events. The *source* object can be a system identifier (a string identifying the input source \-- typically a file name or a URL), a `pathlib.Path`{.interpreted-text role="class"} or `path-like <path-like object>`{.interpreted-text role="term"} object, or an `InputSource`{.interpreted-text role="class"} object. When `parse`{.interpreted-text role="meth"} returns, the input is completely processed, and the parser object can be discarded or reset.

::: versionchanged
3.5 Added support of character streams.
:::

::: versionchanged
3.8 Added support of path-like objects.
:::
:::::

::: method
XMLReader.getContentHandler()

Return the current `~xml.sax.handler.ContentHandler`{.interpreted-text role="class"}.
:::

::: method
XMLReader.setContentHandler(handler)

Set the current `~xml.sax.handler.ContentHandler`{.interpreted-text role="class"}. If no `~xml.sax.handler.ContentHandler`{.interpreted-text role="class"} is set, content events will be discarded.
:::

::: method
XMLReader.getDTDHandler()

Return the current `~xml.sax.handler.DTDHandler`{.interpreted-text role="class"}.
:::

::: method
XMLReader.setDTDHandler(handler)

Set the current `~xml.sax.handler.DTDHandler`{.interpreted-text role="class"}. If no `~xml.sax.handler.DTDHandler`{.interpreted-text role="class"} is set, DTD events will be discarded.
:::

::: method
XMLReader.getEntityResolver()

Return the current `~xml.sax.handler.EntityResolver`{.interpreted-text role="class"}.
:::

::: method
XMLReader.setEntityResolver(handler)

Set the current `~xml.sax.handler.EntityResolver`{.interpreted-text role="class"}. If no `~xml.sax.handler.EntityResolver`{.interpreted-text role="class"} is set, attempts to resolve an external entity will result in opening the system identifier for the entity, and fail if it is not available.
:::

::: method
XMLReader.getErrorHandler()

Return the current `~xml.sax.handler.ErrorHandler`{.interpreted-text role="class"}.
:::

::: method
XMLReader.setErrorHandler(handler)

Set the current error handler. If no `~xml.sax.handler.ErrorHandler`{.interpreted-text role="class"} is set, errors will be raised as exceptions, and warnings will be printed.
:::

::: method
XMLReader.setLocale(locale)

Allow an application to set the locale for errors and warnings.

SAX parsers are not required to provide localization for errors and warnings; if they cannot support the requested locale, however, they must raise a SAX exception. Applications may request a locale change in the middle of a parse.
:::

::: method
XMLReader.getFeature(featurename)

Return the current setting for feature *featurename*. If the feature is not recognized, `SAXNotRecognizedException`{.interpreted-text role="exc"} is raised. The well-known featurenames are listed in the module `xml.sax.handler`{.interpreted-text role="mod"}.
:::

::: method
XMLReader.setFeature(featurename, value)

Set the *featurename* to *value*. If the feature is not recognized, `SAXNotRecognizedException`{.interpreted-text role="exc"} is raised. If the feature or its setting is not supported by the parser, *SAXNotSupportedException* is raised.
:::

::: method
XMLReader.getProperty(propertyname)

Return the current setting for property *propertyname*. If the property is not recognized, a `SAXNotRecognizedException`{.interpreted-text role="exc"} is raised. The well-known propertynames are listed in the module `xml.sax.handler`{.interpreted-text role="mod"}.
:::

::: method
XMLReader.setProperty(propertyname, value)

Set the *propertyname* to *value*. If the property is not recognized, `SAXNotRecognizedException`{.interpreted-text role="exc"} is raised. If the property or its setting is not supported by the parser, *SAXNotSupportedException* is raised.
:::

## IncrementalParser Objects {#incremental-parser-objects}

Instances of `IncrementalParser`{.interpreted-text role="class"} offer the following additional methods:

::: method
IncrementalParser.feed(data)

Process a chunk of *data*.
:::

::: method
IncrementalParser.close()

Assume the end of the document. That will check well-formedness conditions that can be checked only at the end, invoke handlers, and may clean up resources allocated during parsing.
:::

::: method
IncrementalParser.reset()

This method is called after close has been called to reset the parser so that it is ready to parse new documents. The results of calling parse or feed after close without calling reset are undefined.
:::

## Locator Objects

Instances of `Locator`{.interpreted-text role="class"} provide these methods:

::: method
Locator.getColumnNumber()

Return the column number where the current event begins.
:::

::: method
Locator.getLineNumber()

Return the line number where the current event begins.
:::

::: method
Locator.getPublicId()

Return the public identifier for the current event.
:::

::: method
Locator.getSystemId()

Return the system identifier for the current event.
:::

## InputSource Objects {#input-source-objects}

::: method
InputSource.setPublicId(id)

Sets the public identifier of this `InputSource`{.interpreted-text role="class"}.
:::

::: method
InputSource.getPublicId()

Returns the public identifier of this `InputSource`{.interpreted-text role="class"}.
:::

::: method
InputSource.setSystemId(id)

Sets the system identifier of this `InputSource`{.interpreted-text role="class"}.
:::

::: method
InputSource.getSystemId()

Returns the system identifier of this `InputSource`{.interpreted-text role="class"}.
:::

::: method
InputSource.setEncoding(encoding)

Sets the character encoding of this `InputSource`{.interpreted-text role="class"}.

The encoding must be a string acceptable for an XML encoding declaration (see section 4.3.3 of the XML recommendation).

The encoding attribute of the `InputSource`{.interpreted-text role="class"} is ignored if the `InputSource`{.interpreted-text role="class"} also contains a character stream.
:::

::: method
InputSource.getEncoding()

Get the character encoding of this InputSource.
:::

::: method
InputSource.setByteStream(bytefile)

Set the byte stream (a `binary file`{.interpreted-text role="term"}) for this input source.

The SAX parser will ignore this if there is also a character stream specified, but it will use a byte stream in preference to opening a URI connection itself.

If the application knows the character encoding of the byte stream, it should set it with the setEncoding method.
:::

::: method
InputSource.getByteStream()

Get the byte stream for this input source.

The getEncoding method will return the character encoding for this byte stream, or `None` if unknown.
:::

::: method
InputSource.setCharacterStream(charfile)

Set the character stream (a `text file`{.interpreted-text role="term"}) for this input source.

If there is a character stream specified, the SAX parser will ignore any byte stream and will not attempt to open a URI connection to the system identifier.
:::

::: method
InputSource.getCharacterStream()

Get the character stream for this input source.
:::

## The `Attributes`{.interpreted-text role="class"} Interface {#attributes-objects}

`Attributes`{.interpreted-text role="class"} objects implement a portion of the `mapping protocol
<mapping>`{.interpreted-text role="term"}, including the methods `~collections.abc.Mapping.copy`{.interpreted-text role="meth"}, `~collections.abc.Mapping.get`{.interpreted-text role="meth"}, `~object.__contains__`{.interpreted-text role="meth"}, `~collections.abc.Mapping.items`{.interpreted-text role="meth"}, `~collections.abc.Mapping.keys`{.interpreted-text role="meth"}, and `~collections.abc.Mapping.values`{.interpreted-text role="meth"}. The following methods are also provided:

::: method
Attributes.getLength()

Return the number of attributes.
:::

::: method
Attributes.getNames()

Return the names of the attributes.
:::

::: method
Attributes.getType(name)

Returns the type of the attribute *name*, which is normally `'CDATA'`.
:::

::: method
Attributes.getValue(name)

Return the value of attribute *name*.
:::

## The `AttributesNS`{.interpreted-text role="class"} Interface {#attributes-ns-objects}

This interface is a subtype of the `Attributes`{.interpreted-text role="class"} interface (see section `attributes-objects`{.interpreted-text role="ref"}). All methods supported by that interface are also available on `AttributesNS`{.interpreted-text role="class"} objects.

The following methods are also available:

::: method
AttributesNS.getValueByQName(name)

Return the value for a qualified name.
:::

::: method
AttributesNS.getNameByQName(name)

Return the `(namespace, localname)` pair for a qualified *name*.
:::

::: method
AttributesNS.getQNameByName(name)

Return the qualified name for a `(namespace, localname)` pair.
:::

::: method
AttributesNS.getQNames()

Return the qualified names of all attributes.
:::
