# `!email`{.interpreted-text role="mod"} \-\-- An email and MIME handling package

::: {.module synopsis="Package supporting the parsing, manipulating, and generating
email messages."}
email
:::

**Source code:** `Lib/email/__init__.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!email`{.interpreted-text role="mod"} package is a library for managing email messages. It is specifically *not* designed to do any sending of email messages to SMTP (`2821`{.interpreted-text role="rfc"}), NNTP, or other servers; those are functions of modules such as `smtplib`{.interpreted-text role="mod"}. The `!email`{.interpreted-text role="mod"} package attempts to be as RFC-compliant as possible, supporting `5322`{.interpreted-text role="rfc"} and `6532`{.interpreted-text role="rfc"}, as well as such MIME-related RFCs as `2045`{.interpreted-text role="rfc"}, `2046`{.interpreted-text role="rfc"}, `2047`{.interpreted-text role="rfc"}, `2183`{.interpreted-text role="rfc"}, and `2231`{.interpreted-text role="rfc"}.

The overall structure of the email package can be divided into three major components, plus a fourth component that controls the behavior of the other components.

The central component of the package is an \"object model\" that represents email messages. An application interacts with the package primarily through the object model interface defined in the `~email.message`{.interpreted-text role="mod"} sub-module. The application can use this API to ask questions about an existing email, to construct a new email, or to add or remove email subcomponents that themselves use the same object model interface. That is, following the nature of email messages and their MIME subcomponents, the email object model is a tree structure of objects that all provide the `~email.message.EmailMessage`{.interpreted-text role="class"} API.

The other two major components of the package are the `~email.parser`{.interpreted-text role="mod"} and the `~email.generator`{.interpreted-text role="mod"}. The parser takes the serialized version of an email message (a stream of bytes) and converts it into a tree of `~email.message.EmailMessage`{.interpreted-text role="class"} objects. The generator takes an `~email.message.EmailMessage`{.interpreted-text role="class"} and turns it back into a serialized byte stream. (The parser and generator also handle streams of text characters, but this usage is discouraged as it is too easy to end up with messages that are not valid in one way or another.)

The control component is the `~email.policy`{.interpreted-text role="mod"} module. Every `~email.message.EmailMessage`{.interpreted-text role="class"}, every `~email.generator`{.interpreted-text role="mod"}, and every `~email.parser`{.interpreted-text role="mod"} has an associated `~email.policy`{.interpreted-text role="mod"} object that controls its behavior. Usually an application only needs to specify the policy when an `~email.message.EmailMessage`{.interpreted-text role="class"} is created, either by directly instantiating an `~email.message.EmailMessage`{.interpreted-text role="class"} to create a new email, or by parsing an input stream using a `~email.parser`{.interpreted-text role="mod"}. But the policy can be changed when the message is serialized using a `~email.generator`{.interpreted-text role="mod"}. This allows, for example, a generic email message to be parsed from disk, but to serialize it using standard SMTP settings when sending it to an email server.

The email package does its best to hide the details of the various governing RFCs from the application. Conceptually the application should be able to treat the email message as a structured tree of unicode text and binary attachments, without having to worry about how these are represented when serialized. In practice, however, it is often necessary to be aware of at least some of the rules governing MIME messages and their structure, specifically the names and nature of the MIME \"content types\" and how they identify multipart documents. For the most part this knowledge should only be required for more complex applications, and even then it should only be the high level structure in question, and not the details of how those structures are represented. Since MIME content types are used widely in modern internet software (not just email), this will be a familiar concept to many programmers.

The following sections describe the functionality of the `!email`{.interpreted-text role="mod"} package. We start with the `~email.message`{.interpreted-text role="mod"} object model, which is the primary interface an application will use, and follow that with the `~email.parser`{.interpreted-text role="mod"} and `~email.generator`{.interpreted-text role="mod"} components. Then we cover the `~email.policy`{.interpreted-text role="mod"} controls, which completes the treatment of the main components of the library.

The next three sections cover the exceptions the package may raise and the defects (non-compliance with the RFCs) that the `~email.parser`{.interpreted-text role="mod"} may detect. Then we cover the `~email.headerregistry`{.interpreted-text role="mod"} and the `~email.contentmanager`{.interpreted-text role="mod"} sub-components, which provide tools for doing more detailed manipulation of headers and payloads, respectively. Both of these components contain features relevant to consuming and producing non-trivial messages, but also document their extensibility APIs, which will be of interest to advanced applications.

Following those is a set of examples of using the fundamental parts of the APIs covered in the preceding sections.

The foregoing represent the modern (unicode friendly) API of the email package. The remaining sections, starting with the `~email.message.Message`{.interpreted-text role="class"} class, cover the legacy `~email.policy.compat32`{.interpreted-text role="data"} API that deals much more directly with the details of how email messages are represented. The `~email.policy.compat32`{.interpreted-text role="data"} API does *not* hide the details of the RFCs from the application, but for applications that need to operate at that level, they can be useful tools. This documentation is also relevant for applications that are still using the `~email.policy.compat32`{.interpreted-text role="mod"} API for backward compatibility reasons.

::: versionchanged
3.6 Docs reorganized and rewritten to promote the new `~email.message.EmailMessage`{.interpreted-text role="class"}/`~email.policy.EmailPolicy`{.interpreted-text role="class"} API.
:::

Contents of the `!email`{.interpreted-text role="mod"} package documentation:

::: toctree
email.message.rst email.parser.rst email.generator.rst email.policy.rst

email.errors.rst email.headerregistry.rst email.contentmanager.rst

email.examples.rst
:::

Legacy API:

::: toctree
email.compat32-message.rst email.mime.rst email.header.rst email.charset.rst email.encoders.rst email.utils.rst email.iterators.rst
:::

::: seealso

Module `smtplib`{.interpreted-text role="mod"}

:   SMTP (Simple Mail Transport Protocol) client

Module `poplib`{.interpreted-text role="mod"}

:   POP (Post Office Protocol) client

Module `imaplib`{.interpreted-text role="mod"}

:   IMAP (Internet Message Access Protocol) client

Module `mailbox`{.interpreted-text role="mod"}

:   Tools for creating, reading, and managing collections of messages on disk using a variety standard formats.
:::
