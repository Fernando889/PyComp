# `!socket`{.interpreted-text role="mod"} \-\-- Low-level networking interface

::: {.module synopsis="Low-level networking interface."}
socket
:::

**Source code:** `Lib/socket.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module provides access to the BSD *socket* interface. It is available on all modern Unix systems, Windows, MacOS, and probably additional platforms.

:::: note
::: title
Note
:::

Some behavior may be platform dependent, since calls are made to the operating system socket APIs.
::::

::: availability
not WASI.

This module does not work or is not available on WebAssembly. See `wasm-availability`{.interpreted-text role="ref"} for more information.
:::

::: index
pair: object; socket
:::

The Python interface is a straightforward transliteration of the Unix system call and library interface for sockets to Python\'s object-oriented style: the `~socket.socket`{.interpreted-text role="func"} function returns a `socket object`{.interpreted-text role="dfn"} whose methods implement the various socket system calls. Parameter types are somewhat higher-level than in the C interface: as with `read`{.interpreted-text role="meth"} and `write`{.interpreted-text role="meth"} operations on Python files, buffer allocation on receive operations is automatic, and buffer length is implicit on send operations.

::: seealso

Module `socketserver`{.interpreted-text role="mod"}

:   Classes that simplify writing network servers.

Module `ssl`{.interpreted-text role="mod"}

:   A TLS/SSL wrapper for socket objects.
:::

## Socket families

Depending on the system and the build options, various socket families are supported by this module.

The address format required by a particular socket object is automatically selected based on the address family specified when the socket object was created. Socket addresses are represented as follows:

- The address of an `AF_UNIX`{.interpreted-text role="const"} socket bound to a file system node is represented as a string, using the file system encoding and the `'surrogateescape'` error handler (see `383`{.interpreted-text role="pep"}). An address in Linux\'s abstract namespace is returned as a `bytes-like object`{.interpreted-text role="term"} with an initial null byte; note that sockets in this namespace can communicate with normal file system sockets, so programs intended to run on Linux may need to deal with both types of address. A string or bytes-like object can be used for either type of address when passing it as an argument.

  ::: versionchanged
  3.3 Previously, `AF_UNIX`{.interpreted-text role="const"} socket paths were assumed to use UTF-8 encoding.
  :::

  ::: versionchanged
  3.5 Writable `bytes-like object`{.interpreted-text role="term"} is now accepted.
  :::

::: {#host_port}
- A pair `(host, port)` is used for the `AF_INET`{.interpreted-text role="const"} address family, where *host* is a string representing either a hostname in internet domain notation like `'daring.cwi.nl'` or an IPv4 address like `'100.50.200.5'`, and *port* is an integer.

  - For IPv4 addresses, two special forms are accepted instead of a host address: `''` represents `INADDR_ANY`{.interpreted-text role="const"}, which is used to bind to all interfaces, and the string `'<broadcast>'` represents `INADDR_BROADCAST`{.interpreted-text role="const"}. This behavior is not compatible with IPv6, therefore, you may want to avoid these if you intend to support IPv6 with your Python programs.

- For `AF_INET6`{.interpreted-text role="const"} address family, a four-tuple `(host, port, flowinfo, scope_id)` is used, where *flowinfo* and *scope_id* represent the `sin6_flowinfo` and `sin6_scope_id` members in `struct sockaddr_in6`{.interpreted-text role="const"} in C. For `!socket`{.interpreted-text role="mod"} module methods, *flowinfo* and *scope_id* can be omitted just for backward compatibility. Note, however, omission of *scope_id* can cause problems in manipulating scoped IPv6 addresses.

  ::: versionchanged
  3.7 For multicast addresses (with *scope_id* meaningful) *address* may not contain `%scope_id` (or `zone id`) part. This information is superfluous and may be safely omitted (recommended).
  :::

- `AF_NETLINK`{.interpreted-text role="const"} sockets are represented as pairs `(pid, groups)`.

- Linux-only support for TIPC is available using the `AF_TIPC`{.interpreted-text role="const"} address family. TIPC is an open, non-IP based networked protocol designed for use in clustered computer environments. Addresses are represented by a tuple, and the fields depend on the address type. The general tuple form is `(addr_type, v1, v2, v3 [, scope])`, where:

  - *addr_type* is one of `TIPC_ADDR_NAMESEQ`{.interpreted-text role="const"}, `TIPC_ADDR_NAME`{.interpreted-text role="const"}, or `TIPC_ADDR_ID`{.interpreted-text role="const"}.

  - *scope* is one of `TIPC_ZONE_SCOPE`{.interpreted-text role="const"}, `TIPC_CLUSTER_SCOPE`{.interpreted-text role="const"}, and `TIPC_NODE_SCOPE`{.interpreted-text role="const"}.

  - If *addr_type* is `TIPC_ADDR_NAME`{.interpreted-text role="const"}, then *v1* is the server type, *v2* is the port identifier, and *v3* should be 0.

    If *addr_type* is `TIPC_ADDR_NAMESEQ`{.interpreted-text role="const"}, then *v1* is the server type, *v2* is the lower port number, and *v3* is the upper port number.

    If *addr_type* is `TIPC_ADDR_ID`{.interpreted-text role="const"}, then *v1* is the node, *v2* is the reference, and *v3* should be set to 0.

- A tuple `(interface, )` is used for the `AF_CAN`{.interpreted-text role="const"} address family, where *interface* is a string representing a network interface name like `'can0'`. The network interface name `''` can be used to receive packets from all network interfaces of this family.

  - `CAN_ISOTP`{.interpreted-text role="const"} protocol requires a tuple `(interface, rx_addr, tx_addr)` where both additional parameters are unsigned long integer that represent a CAN identifier (standard or extended).
  - `CAN_J1939`{.interpreted-text role="const"} protocol requires a tuple `(interface, name, pgn, addr)` where additional parameters are 64-bit unsigned integer representing the ECU name, a 32-bit unsigned integer representing the Parameter Group Number (PGN), and an 8-bit integer representing the address.

- A string or a tuple `(id, unit)` is used for the `SYSPROTO_CONTROL`{.interpreted-text role="const"} protocol of the `PF_SYSTEM`{.interpreted-text role="const"} family. The string is the name of a kernel control using a dynamically assigned ID. The tuple can be used if ID and unit number of the kernel control are known or if a registered ID is used.

  ::: versionadded
  3.3
  :::

- `AF_BLUETOOTH`{.interpreted-text role="const"} supports the following protocols and address formats:

  - `BTPROTO_L2CAP`{.interpreted-text role="const"} accepts a tuple `(bdaddr, psm[, cid[, bdaddr_type]])` where:

    - `bdaddr` is a string specifying the Bluetooth address.
    - `psm` is an integer specifying the Protocol/Service Multiplexer.
    - `cid` is an optional integer specifying the Channel Identifier. If not given, defaults to zero.
    - `bdaddr_type` is an optional integer specifying the address type; one of `BDADDR_BREDR`{.interpreted-text role="const"} (default), `BDADDR_LE_PUBLIC`{.interpreted-text role="const"}, `BDADDR_LE_RANDOM`{.interpreted-text role="const"}.

    ::: versionchanged
    3.14 Added `cid` and `bdaddr_type` fields.
    :::

  - `BTPROTO_RFCOMM`{.interpreted-text role="const"} accepts `(bdaddr, channel)` where `bdaddr` is the Bluetooth address as a string and `channel` is an integer.

  - `BTPROTO_HCI`{.interpreted-text role="const"} accepts a format that depends on your OS.

    - On Linux it accepts an integer `device_id` or a tuple `(device_id, [channel])` where `device_id` specifies the number of the Bluetooth device, and `channel` is an optional integer specifying the HCI channel (`HCI_CHANNEL_RAW`{.interpreted-text role="const"} by default).
    - On FreeBSD, NetBSD and DragonFly BSD it accepts `bdaddr` where `bdaddr` is the Bluetooth address as a string.

    ::: versionchanged
    3.2 NetBSD and DragonFlyBSD support added.
    :::

    ::: versionchanged
    3.13.3 FreeBSD support added.
    :::

    ::: versionchanged
    3.14 Added `channel` field. `device_id` not packed in a tuple is now accepted.
    :::

  - `BTPROTO_SCO`{.interpreted-text role="const"} accepts `bdaddr` where `bdaddr` is the Bluetooth address as a string or a `bytes`{.interpreted-text role="class"} object. (ex. `'12:23:34:45:56:67'` or `b'12:23:34:45:56:67'`)

    ::: versionchanged
    3.14 FreeBSD support added.
    :::

- `AF_ALG`{.interpreted-text role="const"} is a Linux-only socket based interface to Kernel cryptography. An algorithm socket is configured with a tuple of two to four elements `(type, name [, feat [, mask]])`, where:

  - *type* is the algorithm type as string, e.g. `aead`, `hash`, `skcipher` or `rng`.
  - *name* is the algorithm name and operation mode as string, e.g. `sha256`, `hmac(sha256)`, `cbc(aes)` or `drbg_nopr_ctr_aes256`.
  - *feat* and *mask* are unsigned 32bit integers.

  ::: availability
  Linux \>= 2.6.38.

  Some algorithm types require more recent Kernels.
  :::

  ::: versionadded
  3.6
  :::

- `AF_VSOCK`{.interpreted-text role="const"} allows communication between virtual machines and their hosts. The sockets are represented as a `(CID, port)` tuple where the context ID or CID and port are integers.

  ::: availability
  Linux \>= 3.9

  See `vsock(7)`{.interpreted-text role="manpage"}
  :::

  ::: versionadded
  3.7
  :::

- `AF_PACKET`{.interpreted-text role="const"} is a low-level interface directly to network devices. The addresses are represented by the tuple `(ifname, proto[, pkttype[, hatype[, addr]]])` where:

  - *ifname* - String specifying the device name.
  - *proto* - The Ethernet protocol number. May be `ETH_P_ALL`{.interpreted-text role="data"} to capture all protocols, one of the `ETHERTYPE_* constants <socket-ethernet-types>`{.interpreted-text role="ref"} or any other Ethernet protocol number.
  - *pkttype* - Optional integer specifying the packet type:
    - `PACKET_HOST` (the default) - Packet addressed to the local host.
    - `PACKET_BROADCAST` - Physical-layer broadcast packet.
    - `PACKET_MULTICAST` - Packet sent to a physical-layer multicast address.
    - `PACKET_OTHERHOST` - Packet to some other host that has been caught by a device driver in promiscuous mode.
    - `PACKET_OUTGOING` - Packet originating from the local host that is looped back to a packet socket.
  - *hatype* - Optional integer specifying the ARP hardware address type.
  - *addr* - Optional bytes-like object specifying the hardware physical address, whose interpretation depends on the device.

  ::: availability
  Linux \>= 2.2.
  :::

- `AF_QIPCRTR`{.interpreted-text role="const"} is a Linux-only socket based interface for communicating with services running on co-processors in Qualcomm platforms. The address family is represented as a `(node, port)` tuple where the *node* and *port* are non-negative integers.

  ::: availability
  Linux \>= 4.7.
  :::

  ::: versionadded
  3.8
  :::

- `IPPROTO_UDPLITE`{.interpreted-text role="const"} is a variant of UDP which allows you to specify what portion of a packet is covered with the checksum. It adds two socket options that you can change. `self.setsockopt(IPPROTO_UDPLITE, UDPLITE_SEND_CSCOV, length)` will change what portion of outgoing packets are covered by the checksum and `self.setsockopt(IPPROTO_UDPLITE, UDPLITE_RECV_CSCOV, length)` will filter out packets which cover too little of their data. In both cases `length` should be in `range(8, 2**16, 8)`.

  Such a socket should be constructed with `socket(AF_INET, SOCK_DGRAM, IPPROTO_UDPLITE)` for IPv4 or `socket(AF_INET6, SOCK_DGRAM, IPPROTO_UDPLITE)` for IPv6.

  ::: availability
  Linux \>= 2.6.20, FreeBSD \>= 10.1
  :::

  ::: versionadded
  3.9
  :::

- `AF_HYPERV`{.interpreted-text role="const"} is a Windows-only socket based interface for communicating with Hyper-V hosts and guests. The address family is represented as a `(vm_id, service_id)` tuple where the `vm_id` and `service_id` are UUID strings.

  The `vm_id` is the virtual machine identifier or a set of known VMID values if the target is not a specific virtual machine. Known VMID constants defined on `socket` are:

  - `HV_GUID_ZERO`
  - `HV_GUID_BROADCAST`
  - `HV_GUID_WILDCARD` - Used to bind on itself and accept connections from all partitions.
  - `HV_GUID_CHILDREN` - Used to bind on itself and accept connection from child partitions.
  - `HV_GUID_LOOPBACK` - Used as a target to itself.
  - `HV_GUID_PARENT` - When used as a bind accepts connection from the parent partition. When used as an address target it will connect to the parent partition.

  The `service_id` is the service identifier of the registered service.

  ::: versionadded
  3.12
  :::
:::

If you use a hostname in the *host* portion of IPv4/v6 socket address, the program may show a nondeterministic behavior, as Python uses the first address returned from the DNS resolution. The socket address will be resolved differently into an actual IPv4/v6 address, depending on the results from DNS resolution and/or the host configuration. For deterministic behavior use a numeric address in *host* portion.

All errors raise exceptions. The normal exceptions for invalid argument types and out-of-memory conditions can be raised. Errors related to socket or address semantics raise `OSError`{.interpreted-text role="exc"} or one of its subclasses.

Non-blocking mode is supported through `~socket.setblocking`{.interpreted-text role="meth"}. A generalization of this based on timeouts is supported through `~socket.settimeout`{.interpreted-text role="meth"}.

## Module contents

The module `!socket`{.interpreted-text role="mod"} exports the following elements.

### Exceptions

:::: exception
error

A deprecated alias of `OSError`{.interpreted-text role="exc"}.

::: versionchanged
3.3 Following `3151`{.interpreted-text role="pep"}, this class was made an alias of `OSError`{.interpreted-text role="exc"}.
:::
::::

:::: exception
herror

A subclass of `OSError`{.interpreted-text role="exc"}, this exception is raised for address-related errors, i.e. for functions that use *h_errno* in the POSIX C API, including `gethostbyname_ex`{.interpreted-text role="func"} and `gethostbyaddr`{.interpreted-text role="func"}. The accompanying value is a pair `(h_errno, string)` representing an error returned by a library call. *h_errno* is a numeric value, while *string* represents the description of *h_errno*, as returned by the `hstrerror`{.interpreted-text role="c:func"} C function.

::: versionchanged
3.3 This class was made a subclass of `OSError`{.interpreted-text role="exc"}.
:::
::::

:::: exception
gaierror

A subclass of `OSError`{.interpreted-text role="exc"}, this exception is raised for address-related errors by `getaddrinfo`{.interpreted-text role="func"} and `getnameinfo`{.interpreted-text role="func"}. The accompanying value is a pair `(error, string)` representing an error returned by a library call. *string* represents the description of *error*, as returned by the `gai_strerror`{.interpreted-text role="c:func"} C function. The numeric *error* value will match one of the `!EAI_\*`{.interpreted-text role="const"} constants defined in this module.

::: versionchanged
3.3 This class was made a subclass of `OSError`{.interpreted-text role="exc"}.
:::
::::

::::: exception
timeout

A deprecated alias of `TimeoutError`{.interpreted-text role="exc"}.

A subclass of `OSError`{.interpreted-text role="exc"}, this exception is raised when a timeout occurs on a socket which has had timeouts enabled via a prior call to `~socket.settimeout`{.interpreted-text role="meth"} (or implicitly through `~socket.setdefaulttimeout`{.interpreted-text role="func"}). The accompanying value is a string whose value is currently always \"timed out\".

::: versionchanged
3.3 This class was made a subclass of `OSError`{.interpreted-text role="exc"}.
:::

::: versionchanged
3.10 This class was made an alias of `TimeoutError`{.interpreted-text role="exc"}.
:::
:::::

### Constants

The [AF]()\* and [SOCK]()\* constants are now `AddressFamily`{.interpreted-text role="class"} and `SocketKind`{.interpreted-text role="class"} `.IntEnum`{.interpreted-text role="class"} collections.

::: versionadded
3.4
:::

::: data
AF_UNIX AF_INET AF_INET6

These constants represent the address (and protocol) families, used for the first argument to `~socket.socket`{.interpreted-text role="func"}. If the `AF_UNIX`{.interpreted-text role="const"} constant is not defined then this protocol is unsupported. More constants may be available depending on the system.
:::

::: data
AF_UNSPEC

`AF_UNSPEC`{.interpreted-text role="const"} means that `getaddrinfo`{.interpreted-text role="func"} should return socket addresses for any address family (either IPv4, IPv6, or any other) that can be used.
:::

::: data
SOCK_STREAM SOCK_DGRAM SOCK_RAW SOCK_RDM SOCK_SEQPACKET

These constants represent the socket types, used for the second argument to `~socket.socket`{.interpreted-text role="func"}. More constants may be available depending on the system. (Only `SOCK_STREAM`{.interpreted-text role="const"} and `SOCK_DGRAM`{.interpreted-text role="const"} appear to be generally useful.)
:::

:::::: data
SOCK_CLOEXEC SOCK_NONBLOCK

These two constants, if defined, can be combined with the socket types and allow you to set some flags atomically (thus avoiding possible race conditions and the need for separate calls).

::: seealso
[Secure File Descriptor Handling](https://udrepper.livejournal.com/20407.html) for a more thorough explanation.
:::

::: availability
Linux \>= 2.6.27.
:::

::: versionadded
3.2
:::
::::::

:::::::::::::: {#socket-unix-constants}
::::::::::::: data
[SO]()\* SOMAXCONN [MSG]()\* [SOL]()\* [SCM]()\* [IPPROTO]()\* [IPPORT]()\* [INADDR]()\* [IP]()\* [IPV6]()\* [EAI]()\* [AI]()\* [NI]()\* [TCP]()\*

Many constants of these forms, documented in the Unix documentation on sockets and/or the IP protocol, are also defined in the socket module. They are generally used in arguments to the `~socket.setsockopt`{.interpreted-text role="meth"} and `~socket.getsockopt`{.interpreted-text role="meth"} methods of socket objects. In most cases, only those symbols that are defined in the Unix header files are defined; for a few symbols, default values are provided.

::: versionchanged
3.6 `SO_DOMAIN`, `SO_PROTOCOL`, `SO_PEERSEC`, `SO_PASSSEC`, `TCP_USER_TIMEOUT`, `TCP_CONGESTION` were added.
:::

::: versionchanged
3.6.5 Added support for `TCP_FASTOPEN`, `TCP_KEEPCNT` on Windows platforms when available.
:::

::: versionchanged
3.7 `TCP_NOTSENT_LOWAT` was added.

Added support for `TCP_KEEPIDLE`, `TCP_KEEPINTVL` on Windows platforms when available.
:::

::: versionchanged
3.10 `IP_RECVTOS` was added. Added `TCP_KEEPALIVE`. On MacOS this constant can be used in the same way that `TCP_KEEPIDLE` is used on Linux.
:::

::: versionchanged
3.11 Added `TCP_CONNECTION_INFO`. On MacOS this constant can be used in the same way that `TCP_INFO` is used on Linux and BSD.
:::

::: versionchanged
3.12 Added `SO_RTABLE` and `SO_USER_COOKIE`. On OpenBSD and FreeBSD respectively those constants can be used in the same way that `SO_MARK` is used on Linux. Also added missing TCP socket options from Linux: `TCP_MD5SIG`, `TCP_THIN_LINEAR_TIMEOUTS`, `TCP_THIN_DUPACK`, `TCP_REPAIR`, `TCP_REPAIR_QUEUE`, `TCP_QUEUE_SEQ`, `TCP_REPAIR_OPTIONS`, `TCP_TIMESTAMP`, `TCP_CC_INFO`, `TCP_SAVE_SYN`, `TCP_SAVED_SYN`, `TCP_REPAIR_WINDOW`, `TCP_FASTOPEN_CONNECT`, `TCP_ULP`, `TCP_MD5SIG_EXT`, `TCP_FASTOPEN_KEY`, `TCP_FASTOPEN_NO_COOKIE`, `TCP_ZEROCOPY_RECEIVE`, `TCP_INQ`, `TCP_TX_DELAY`. Added `IP_PKTINFO`, `IP_UNBLOCK_SOURCE`, `IP_BLOCK_SOURCE`, `IP_ADD_SOURCE_MEMBERSHIP`, `IP_DROP_SOURCE_MEMBERSHIP`.
:::

::: versionchanged
3.13 Added `SO_BINDTOIFINDEX`. On Linux this constant can be used in the same way that `SO_BINDTODEVICE` is used, but with the index of a network interface instead of its name.
:::

::: versionchanged
3.14 Added missing `IP_FREEBIND`, `IP_RECVERR`, `IPV6_RECVERR`, `IP_RECVTTL`, and `IP_RECVORIGDSTADDR` on Linux.
:::

::: versionchanged
3.14 Added support for `TCP_QUICKACK` on Windows platforms when available.
:::

::: versionchanged
3.15 `IPV6_HDRINCL` was added.
:::
:::::::::::::
::::::::::::::

::::::: data
AF_CAN PF_CAN [SOL_CAN]()\* [CAN]()\*

Many constants of these forms, documented in the Linux documentation, are also defined in the socket module.

::: availability
Linux \>= 2.6.25, NetBSD \>= 8.
:::

::: versionadded
3.3
:::

::: versionchanged
3.11 NetBSD support was added.
:::

::: versionchanged
3.14 Restored missing `CAN_RAW_ERR_FILTER` on Linux.
:::
:::::::

::::::: data
CAN_BCM [CAN_BCM]()\*

CAN_BCM, in the CAN protocol family, is the broadcast manager (BCM) protocol. Broadcast manager constants, documented in the Linux documentation, are also defined in the socket module.

::: availability
Linux \>= 2.6.25.
:::

:::: note
::: title
Note
:::

The `CAN_BCM_CAN_FD_FRAME`{.interpreted-text role="data"} flag is only available on Linux \>= 4.8.
::::

::: versionadded
3.4
:::
:::::::

::::: data
CAN_RAW_FD_FRAMES

Enables CAN FD support in a CAN_RAW socket. This is disabled by default. This allows your application to send both CAN and CAN FD frames; however, you must accept both CAN and CAN FD frames when reading from the socket.

This constant is documented in the Linux documentation.

::: availability
Linux \>= 3.6.
:::

::: versionadded
3.5
:::
:::::

::::: data
CAN_RAW_JOIN_FILTERS

Joins the applied CAN filters such that only CAN frames that match all given CAN filters are passed to user space.

This constant is documented in the Linux documentation.

::: availability
Linux \>= 4.1.
:::

::: versionadded
3.9
:::
:::::

::::: data
CAN_ISOTP

CAN_ISOTP, in the CAN protocol family, is the ISO-TP (ISO 15765-2) protocol. ISO-TP constants, documented in the Linux documentation.

::: availability
Linux \>= 2.6.25.
:::

::: versionadded
3.7
:::
:::::

::::: data
CAN_J1939

CAN_J1939, in the CAN protocol family, is the SAE J1939 protocol. J1939 constants, documented in the Linux documentation.

::: availability
Linux \>= 5.4.
:::

::: versionadded
3.9
:::
:::::

::::: data
AF_DIVERT PF_DIVERT

These two constants, documented in the FreeBSD divert(4) manual page, are also defined in the socket module.

::: availability
FreeBSD \>= 14.0.
:::

::: versionadded
3.12
:::
:::::

:::: data
AF_PACKET PF_PACKET [PACKET]()\*

Many constants of these forms, documented in the Linux documentation, are also defined in the socket module.

::: availability
Linux \>= 2.2.
:::
::::

::::: data
ETH_P_ALL

`!ETH_P_ALL`{.interpreted-text role="data"} can be used in the `~socket.socket`{.interpreted-text role="class"} constructor as *proto* for the `AF_PACKET`{.interpreted-text role="const"} family in order to capture every packet, regardless of protocol.

For more information, see the `packet(7)`{.interpreted-text role="manpage"} manpage.

::: availability
Linux.
:::

::: versionadded
3.12
:::
:::::

::::: data
AF_RDS PF_RDS SOL_RDS [RDS]()\*

Many constants of these forms, documented in the Linux documentation, are also defined in the socket module.

::: availability
Linux \>= 2.6.30.
:::

::: versionadded
3.3
:::
:::::

:::: data
SIO_RCVALL SIO_KEEPALIVE_VALS SIO_LOOPBACK_FAST_PATH [RCVALL]()\*

Constants for Windows\' WSAIoctl(). The constants are used as arguments to the `~socket.socket.ioctl`{.interpreted-text role="meth"} method of socket objects.

::: versionchanged
3.6 `SIO_LOOPBACK_FAST_PATH` was added.
:::
::::

::: data
[TIPC]()\*

TIPC related constants, matching the ones exported by the C socket API. See the TIPC documentation for more information.
:::

::::: data
AF_ALG SOL_ALG [ALG]()\*

Constants for Linux Kernel cryptography.

::: availability
Linux \>= 2.6.38.
:::

::: versionadded
3.6
:::
:::::

::::: data
AF_VSOCK IOCTL_VM_SOCKETS_GET_LOCAL_CID VMADDR\* SO_VM\*

Constants for Linux host/guest communication.

::: availability
Linux \>= 4.8.
:::

::: versionadded
3.7
:::
:::::

::::: data
AF_LINK

::: availability
BSD, macOS.
:::

::: versionadded
3.4
:::
:::::

::: data
has_ipv6

This constant contains a boolean value which indicates if IPv6 is supported on this platform.
:::

::: data
AF_BLUETOOTH BTPROTO_L2CAP BTPROTO_RFCOMM BTPROTO_HCI BTPROTO_SCO

Integer constants for use with Bluetooth addresses.
:::

::: data
BDADDR_ANY BDADDR_LOCAL

These are string constants containing Bluetooth addresses with special meanings. For example, `BDADDR_ANY`{.interpreted-text role="const"} can be used to indicate any address when specifying the binding socket with `BTPROTO_RFCOMM`{.interpreted-text role="const"}.
:::

::::: data
BDADDR_BREDR BDADDR_LE_PUBLIC BDADDR_LE_RANDOM

These constants describe the Bluetooth address type when binding or connecting a `BTPROTO_L2CAP`{.interpreted-text role="const"} socket.

::: availability
Linux, FreeBSD
:::

::: versionadded
3.14
:::
:::::

::: data
SOL_RFCOMM SOL_L2CAP SOL_HCI SOL_SCO SOL_BLUETOOTH

Used in the level argument to the `~socket.setsockopt`{.interpreted-text role="meth"} and `~socket.getsockopt`{.interpreted-text role="meth"} methods of Bluetooth socket objects.

`SOL_BLUETOOTH`{.interpreted-text role="const"} is only available on Linux. Other constants are available if the corresponding protocol is supported.
:::

:::: data
[SO_L2CAP]()\* L2CAP_LM [L2CAP_LM]()\* [SO_RFCOMM]()\* [RFCOMM_LM]()\* [SO_SCO]()\* [SO_BTH]()\* [BT]()\*

Used in the option name and value argument to the `~socket.setsockopt`{.interpreted-text role="meth"} and `~socket.getsockopt`{.interpreted-text role="meth"} methods of Bluetooth socket objects.

`!BT_*`{.interpreted-text role="const"} and `L2CAP_LM`{.interpreted-text role="const"} are only available on Linux. `!SO_BTH_*`{.interpreted-text role="const"} are only available on Windows. Other constants may be available on Linux and various BSD platforms.

::: versionadded
3.14
:::
::::

:::: data
HCI_FILTER HCI_TIME_STAMP HCI_DATA_DIR SO_HCI_EVT_FILTER SO_HCI_PKT_FILTER

Option names for use with `BTPROTO_HCI`{.interpreted-text role="const"}. Availability and format of the option values depend on platform.

::: versionchanged
3.14 Added `!SO_HCI_EVT_FILTER`{.interpreted-text role="const"} and `!SO_HCI_PKT_FILTER`{.interpreted-text role="const"} on NetBSD and DragonFly BSD. Added `!HCI_DATA_DIR`{.interpreted-text role="const"} on FreeBSD, NetBSD and DragonFly BSD.
:::
::::

::::: data
HCI_DEV_NONE

The `device_id` value used to create an HCI socket that isn\'t specific to a single Bluetooth adapter.

::: availability
Linux
:::

::: versionadded
3.14
:::
:::::

::::: data
HCI_CHANNEL_RAW HCI_CHANNEL_USER HCI_CHANNEL_MONITOR HCI_CHANNEL_CONTROL HCI_CHANNEL_LOGGING

Possible values for `channel` field in the `BTPROTO_HCI`{.interpreted-text role="const"} address.

::: availability
Linux
:::

::: versionadded
3.14
:::
:::::

:::: data
AF_QIPCRTR

Constant for Qualcomm\'s IPC router protocol, used to communicate with service providing remote processors.

::: availability
Linux \>= 4.7.
:::
::::

::::: data
SCM_CREDS2 LOCAL_CREDS LOCAL_CREDS_PERSISTENT

LOCAL_CREDS and LOCAL_CREDS_PERSISTENT can be used with SOCK_DGRAM, SOCK_STREAM sockets, equivalent to Linux/DragonFlyBSD SO_PASSCRED, while LOCAL_CREDS sends the credentials at first read, LOCAL_CREDS_PERSISTENT sends for each read, SCM_CREDS2 must be then used for the latter for the message type.

::: versionadded
3.11
:::

::: availability
FreeBSD.
:::
:::::

::::: data
SO_INCOMING_CPU

Constant to optimize CPU locality, to be used in conjunction with `SO_REUSEPORT`{.interpreted-text role="data"}.

::: versionadded
3.11
:::

::: availability
Linux \>= 3.9
:::
:::::

::::: data
SO_REUSEPORT_LB

Constant to enable duplicate address and port bindings with load balancing.

::: versionadded
3.14
:::

::: availability
FreeBSD \>= 12.0
:::
:::::

::::: data
AF_HYPERV HV_PROTOCOL_RAW HVSOCKET_CONNECT_TIMEOUT HVSOCKET_CONNECT_TIMEOUT_MAX HVSOCKET_CONNECTED_SUSPEND HVSOCKET_ADDRESS_FLAG_PASSTHRU HV_GUID_ZERO HV_GUID_WILDCARD HV_GUID_BROADCAST HV_GUID_CHILDREN HV_GUID_LOOPBACK HV_GUID_PARENT

Constants for Windows Hyper-V sockets for host/guest communications.

::: availability
Windows.
:::

::: versionadded
3.12
:::
:::::

:::::: {#socket-ethernet-types}
::::: data
ETHERTYPE_ARP ETHERTYPE_IP ETHERTYPE_IPV6 ETHERTYPE_VLAN

[IEEE 802.3 protocol number](https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.txt). constants.

::: availability
Linux, FreeBSD, macOS.
:::

::: versionadded
3.12
:::
:::::
::::::

:::: data
SHUT_RD SHUT_WR SHUT_RDWR

These constants are used by the `~socket.socket.shutdown`{.interpreted-text role="meth"} method of socket objects.

::: availability
not WASI.
:::
::::

### Functions

#### Creating sockets

The following functions all create `socket objects <socket-objects>`{.interpreted-text role="ref"}.

::::::::::: {.socket(family=AF_INET, .type=SOCK_STREAM, .proto=0, .fileno=None)}
Create a new socket using the given address family, socket type and protocol number. The address family should be `AF_INET`{.interpreted-text role="const"} (the default), `AF_INET6`{.interpreted-text role="const"}, `AF_UNIX`{.interpreted-text role="const"}, `AF_CAN`{.interpreted-text role="const"}, `AF_PACKET`{.interpreted-text role="const"}, or `AF_RDS`{.interpreted-text role="const"}. The socket type should be `SOCK_STREAM`{.interpreted-text role="const"} (the default), `SOCK_DGRAM`{.interpreted-text role="const"}, `SOCK_RAW`{.interpreted-text role="const"} or perhaps one of the other `SOCK_` constants. The protocol number is usually zero and may be omitted or in the case where the address family is `AF_CAN`{.interpreted-text role="const"} the protocol should be one of `CAN_RAW`{.interpreted-text role="const"}, `CAN_BCM`{.interpreted-text role="const"}, `CAN_ISOTP`{.interpreted-text role="const"} or `CAN_J1939`{.interpreted-text role="const"}.

If *fileno* is specified, the values for *family*, *type*, and *proto* are auto-detected from the specified file descriptor. Auto-detection can be overruled by calling the function with explicit *family*, *type*, or *proto* arguments. This only affects how Python represents e.g. the return value of `socket.getpeername`{.interpreted-text role="meth"} but not the actual OS resource. Unlike `socket.fromfd`{.interpreted-text role="func"}, *fileno* will return the same socket and not a duplicate. This may help close a detached socket using `socket.close`{.interpreted-text role="meth"}.

The newly created socket is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

::: audit-event
socket.\_\_new\_\_ self,family,type,protocol socket.socket
:::

::: versionchanged
3.3 The AF_CAN family was added. The AF_RDS family was added.
:::

::: versionchanged
3.4 The CAN_BCM protocol was added.
:::

::: versionchanged
3.4 The returned socket is now non-inheritable.
:::

::: versionchanged
3.7 The CAN_ISOTP protocol was added.
:::

::: versionchanged
3.7 When `SOCK_NONBLOCK`{.interpreted-text role="const"} or `SOCK_CLOEXEC`{.interpreted-text role="const"} bit flags are applied to *type* they are cleared, and `socket.type`{.interpreted-text role="attr"} will not reflect them. They are still passed to the underlying system `socket()` call. Therefore,

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM | socket.SOCK_NONBLOCK)

will still create a non-blocking socket on OSes that support `SOCK_NONBLOCK`, but `sock.type` will be set to `socket.SOCK_STREAM`.
:::

::: versionchanged
3.9 The CAN_J1939 protocol was added.
:::

::: versionchanged
3.10 The IPPROTO_MPTCP protocol was added.
:::
:::::::::::

:::::: function
socketpair(\[family\[, type\[, proto\]\]\])

Build a pair of connected socket objects using the given address family, socket type, and protocol number. Address family, socket type, and protocol number are as for the `~socket.socket`{.interpreted-text role="func"} function above. The default family is `AF_UNIX`{.interpreted-text role="const"} if defined on the platform; otherwise, the default is `AF_INET`{.interpreted-text role="const"}.

The newly created sockets are `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

::: versionchanged
3.2 The returned socket objects now support the whole socket API, rather than a subset.
:::

::: versionchanged
3.4 The returned sockets are now non-inheritable.
:::

::: versionchanged
3.5 Windows support added.
:::
::::::

::::: function
create_connection(address, timeout=GLOBAL_DEFAULT, source_address=None, \*, all_errors=False)

Connect to a TCP service listening on the internet *address* (a 2-tuple `(host, port)`), and return the socket object. This is a higher-level function than `socket.connect`{.interpreted-text role="meth"}: if *host* is a non-numeric hostname, it will try to resolve it for both `AF_INET`{.interpreted-text role="data"} and `AF_INET6`{.interpreted-text role="data"}, and then try to connect to all possible addresses in turn until a connection succeeds. This makes it easy to write clients that are compatible to both IPv4 and IPv6.

Passing the optional *timeout* parameter will set the timeout on the socket instance before attempting to connect. If no *timeout* is supplied, the global default timeout setting returned by `getdefaulttimeout`{.interpreted-text role="func"} is used.

If supplied, *source_address* must be a 2-tuple `(host, port)` for the socket to bind to as its source address before connecting. If host or port are \'\' or 0 respectively the OS default behavior will be used.

When a connection cannot be created, an exception is raised. By default, it is the exception from the last address in the list. If *all_errors* is `True`, it is an `ExceptionGroup`{.interpreted-text role="exc"} containing the errors of all attempts.

::: versionchanged
3.2 *source_address* was added.
:::

::: versionchanged
3.11 *all_errors* was added.
:::
:::::

:::::: function
create_server(address, \*, family=AF_INET, backlog=None, reuse_port=False, dualstack_ipv6=False)

Convenience function which creates a TCP socket bound to *address* (a 2-tuple `(host, port)`) and returns the socket object.

*family* should be either `AF_INET`{.interpreted-text role="data"} or `AF_INET6`{.interpreted-text role="data"}. *backlog* is the queue size passed to `socket.listen`{.interpreted-text role="meth"}; if not specified , a default reasonable value is chosen. *reuse_port* dictates whether to set the `SO_REUSEPORT`{.interpreted-text role="data"} socket option.

If *dualstack_ipv6* is true, *family* is `AF_INET6`{.interpreted-text role="data"} and the platform supports it the socket will be able to accept both IPv4 and IPv6 connections, else it will raise `ValueError`{.interpreted-text role="exc"}. Most POSIX platforms and Windows are supposed to support this functionality. When this functionality is enabled the address returned by `socket.getpeername`{.interpreted-text role="meth"} when an IPv4 connection occurs will be an IPv6 address represented as an IPv4-mapped IPv6 address. If *dualstack_ipv6* is false it will explicitly disable this functionality on platforms that enable it by default (e.g. Linux). This parameter can be used in conjunction with `has_dualstack_ipv6`{.interpreted-text role="func"}:

    import socket

    addr = ("", 8080)  # all interfaces, port 8080
    if socket.has_dualstack_ipv6():
        s = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
    else:
        s = socket.create_server(addr)

:::: note
::: title
Note
:::

On POSIX platforms the `SO_REUSEADDR`{.interpreted-text role="data"} socket option is set in order to immediately reuse previous sockets which were bound on the same *address* and remained in TIME_WAIT state.
::::

::: versionadded
3.8
:::
::::::

:::: function
has_dualstack_ipv6()

Return `True` if the platform supports creating a TCP socket which can handle both IPv4 and IPv6 connections.

::: versionadded
3.8
:::
::::

:::: function
fromfd(fd, family, type, proto=0)

Duplicate the file descriptor *fd* (an integer as returned by a file object\'s `~io.IOBase.fileno`{.interpreted-text role="meth"} method) and build a socket object from the result. Address family, socket type and protocol number are as for the `~socket.socket`{.interpreted-text role="func"} function above. The file descriptor should refer to a socket, but this is not checked \-\-- subsequent operations on the object may fail if the file descriptor is invalid. This function is rarely needed, but can be used to get or set socket options on a socket passed to a program as standard input or output (such as a server started by the Unix inet daemon). The socket is assumed to be in blocking mode.

The newly created socket is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

::: versionchanged
3.4 The returned socket is now non-inheritable.
:::
::::

::::: function
fromshare(data)

Instantiate a socket from data obtained from the `socket.share`{.interpreted-text role="meth"} method. The socket is assumed to be in blocking mode.

::: availability
Windows.
:::

::: versionadded
3.3
:::
:::::

::: data
SocketType

This is a Python type object that represents the socket object type. It is the same as `type(socket(...))`.
:::

#### Other functions

The `!socket`{.interpreted-text role="mod"} module also offers various network-related services:

:::: function
close(fd)

Close a socket file descriptor. This is like `os.close`{.interpreted-text role="func"}, but for sockets. On some platforms (most notably Windows) `os.close`{.interpreted-text role="func"} does not work for socket file descriptors.

::: versionadded
3.7
:::
::::

:::::::: function
getaddrinfo(host, port, family=AF_UNSPEC, type=0, proto=0, flags=0)

This function wraps the C function `getaddrinfo` of the underlying system.

Translate the *host*/\*port\* argument into a sequence of 5-tuples that contain all the necessary arguments for creating a socket connected to that service. *host* is a domain name, a string representation of an IPv4/v6 address or `None`. *port* is a string service name such as `'http'`, a numeric port number or `None`. By passing `None` as the value of *host* and *port*, you can pass `NULL` to the underlying C API.

The *family*, *type* and *proto* arguments can be optionally specified in order to provide options and limit the list of addresses returned. Pass their default values (`AF_UNSPEC`{.interpreted-text role="data"}, 0, and 0, respectively) to not limit the results. See the note below for details.

The *flags* argument can be one or several of the `AI_*` constants, and will influence how results are computed and returned. For example, `AI_NUMERICHOST`{.interpreted-text role="const"} will disable domain name resolution and will raise an error if *host* is a domain name.

The function returns a list of 5-tuples with the following structure:

`(family, type, proto, canonname, sockaddr)`

In these tuples, *family*, *type*, *proto* are all integers and are meant to be passed to the `~socket.socket`{.interpreted-text role="func"} function. *canonname* will be a string representing the canonical name of the *host* if `AI_CANONNAME`{.interpreted-text role="const"} is part of the *flags* argument; else *canonname* will be empty. *sockaddr* is a tuple describing a socket address, whose format depends on the returned *family* and flags Python was compiled with, and is meant to be passed to the `socket.connect`{.interpreted-text role="meth"} method.

*sockaddr* can be one of the following:

- a `(address, port)` 2-tuple for `AF_INET`{.interpreted-text role="const"}
- a `(address, port, flowinfo, scope_id)` 4-tuple for `AF_INET6`{.interpreted-text role="const"} if Python was compiled with `--enable-ipv6` (the default)
- a 2-tuple containing raw data for `AF_INET6`{.interpreted-text role="const"} if Python was compiled with `--disable-ipv6`

:::: note
::: title
Note
:::

If you intend to use results from `!getaddrinfo`{.interpreted-text role="func"} to create a socket (rather than, for example, retrieve *canonname*), consider limiting the results by *type* (e.g. `SOCK_STREAM`{.interpreted-text role="data"} or `SOCK_DGRAM`{.interpreted-text role="data"}) and/or *proto* (e.g. `IPPROTO_TCP`{.interpreted-text role="data"} or `IPPROTO_UDP`{.interpreted-text role="data"}) that your application can handle.

The behavior with default values of *family*, *type*, *proto* and *flags* is system-specific.

Many systems (for example, most Linux configurations) will return a sorted list of all matching addresses. These addresses should generally be tried in order until a connection succeeds (possibly tried in parallel, for example, using a [Happy Eyeballs](https://en.wikipedia.org/wiki/Happy_Eyeballs) algorithm). In these cases, limiting the *type* and/or *proto* can help eliminate unsuccessful or unusable connection attempts.

Some systems will, however, only return a single address. (For example, this was reported on Solaris and AIX configurations.) On these systems, limiting the *type* and/or *proto* helps ensure that this address is usable.
::::

::: audit-event
socket.getaddrinfo host,port,family,type,protocol socket.getaddrinfo
:::

The following example fetches address information for a hypothetical TCP connection to `example.org` on port 80 (results may differ on your system if IPv6 isn\'t enabled):

    >>> socket.getaddrinfo("example.org", 80, proto=socket.IPPROTO_TCP)
    [(socket.AF_INET6, socket.SOCK_STREAM,
     6, '', ('2606:2800:220:1:248:1893:25c8:1946', 80, 0, 0)),
     (socket.AF_INET, socket.SOCK_STREAM,
     6, '', ('93.184.216.34', 80))]

::: versionchanged
3.2 parameters can now be passed using keyword arguments.
:::

::: versionchanged
3.7 for IPv6 multicast addresses, string representing an address will not contain `%scope_id` part.
:::
::::::::

::: function
getfqdn(\[name\])

Return a fully qualified domain name for *name*. If *name* is omitted or empty, it is interpreted as the local host. To find the fully qualified name, the hostname returned by `gethostbyaddr`{.interpreted-text role="func"} is checked, followed by aliases for the host, if available. The first name which includes a period is selected. In case no fully qualified domain name is available and *name* was provided, it is returned unchanged. If *name* was empty or equal to `'0.0.0.0'`, the hostname from `gethostname`{.interpreted-text role="func"} is returned.
:::

::::: function
gethostbyname(hostname)

Translate a host name to IPv4 address format. The IPv4 address is returned as a string, such as `'100.50.200.5'`. If the host name is an IPv4 address itself it is returned unchanged. See `gethostbyname_ex`{.interpreted-text role="func"} for a more complete interface. `gethostbyname`{.interpreted-text role="func"} does not support IPv6 name resolution, and `getaddrinfo`{.interpreted-text role="func"} should be used instead for IPv4/v6 dual stack support.

::: audit-event
socket.gethostbyname hostname socket.gethostbyname
:::

::: availability
not WASI.
:::
:::::

::::: function
gethostbyname_ex(hostname)

Translate a host name to IPv4 address format, extended interface. Return a 3-tuple `(hostname, aliaslist, ipaddrlist)` where *hostname* is the host\'s primary host name, *aliaslist* is a (possibly empty) list of alternative host names for the same address, and *ipaddrlist* is a list of IPv4 addresses for the same interface on the same host (often but not always a single address). `gethostbyname_ex`{.interpreted-text role="func"} does not support IPv6 name resolution, and `getaddrinfo`{.interpreted-text role="func"} should be used instead for IPv4/v6 dual stack support.

::: audit-event
socket.gethostbyname hostname socket.gethostbyname_ex
:::

::: availability
not WASI.
:::
:::::

::::: function
gethostname()

Return a string containing the hostname of the machine where the Python interpreter is currently executing.

::: audit-event
socket.gethostname \"\" socket.gethostname
:::

Note: `gethostname`{.interpreted-text role="func"} doesn\'t always return the fully qualified domain name; use `getfqdn`{.interpreted-text role="func"} for that.

::: availability
not WASI.
:::
:::::

::::: function
gethostbyaddr(ip_address)

Return a 3-tuple `(hostname, aliaslist, ipaddrlist)` where *hostname* is the primary host name responding to the given *ip_address*, *aliaslist* is a (possibly empty) list of alternative host names for the same address, and *ipaddrlist* is a list of IPv4/v6 addresses for the same interface on the same host (most likely containing only a single address). To find the fully qualified domain name, use the function `getfqdn`{.interpreted-text role="func"}. `gethostbyaddr`{.interpreted-text role="func"} supports both IPv4 and IPv6.

::: audit-event
socket.gethostbyaddr ip_address socket.gethostbyaddr
:::

::: availability
not WASI.
:::
:::::

::::: function
getnameinfo(sockaddr, flags)

Translate a socket address *sockaddr* into a 2-tuple `(host, port)`. Depending on the settings of *flags*, the result can contain a fully qualified domain name or numeric address representation in *host*. Similarly, *port* can contain a string port name or a numeric port number.

For IPv6 addresses, `%scope_id` is appended to the host part if *sockaddr* contains meaningful *scope_id*. Usually this happens for multicast addresses.

For more information about *flags* you can consult `getnameinfo(3)`{.interpreted-text role="manpage"}.

::: audit-event
socket.getnameinfo sockaddr socket.getnameinfo
:::

::: availability
not WASI.
:::
:::::

:::: function
getprotobyname(protocolname)

Translate an internet protocol name (for example, `'icmp'`) to a constant suitable for passing as the (optional) third argument to the `~socket.socket`{.interpreted-text role="func"} function. This is usually only needed for sockets opened in \"raw\" mode (`SOCK_RAW`{.interpreted-text role="const"}); for the normal socket modes, the correct protocol is chosen automatically if the protocol is omitted or zero.

::: availability
not WASI.
:::
::::

::::: function
getservbyname(servicename\[, protocolname\])

Translate an internet service name and protocol name to a port number for that service. The optional protocol name, if given, should be `'tcp'` or `'udp'`, otherwise any protocol will match.

::: audit-event
socket.getservbyname servicename,protocolname socket.getservbyname
:::

::: availability
not WASI.
:::
:::::

::::: function
getservbyport(port\[, protocolname\])

Translate an internet port number and protocol name to a service name for that service. The optional protocol name, if given, should be `'tcp'` or `'udp'`, otherwise any protocol will match.

::: audit-event
socket.getservbyport port,protocolname socket.getservbyport
:::

::: availability
not WASI.
:::
:::::

::: function
ntohl(x)

Convert 32-bit positive integers from network to host byte order. On machines where the host byte order is the same as network byte order, this is a no-op; otherwise, it performs a 4-byte swap operation.
:::

:::: function
ntohs(x)

Convert 16-bit positive integers from network to host byte order. On machines where the host byte order is the same as network byte order, this is a no-op; otherwise, it performs a 2-byte swap operation.

::: versionchanged
3.10 Raises `OverflowError`{.interpreted-text role="exc"} if *x* does not fit in a 16-bit unsigned integer.
:::
::::

::: function
htonl(x)

Convert 32-bit positive integers from host to network byte order. On machines where the host byte order is the same as network byte order, this is a no-op; otherwise, it performs a 4-byte swap operation.
:::

:::: function
htons(x)

Convert 16-bit positive integers from host to network byte order. On machines where the host byte order is the same as network byte order, this is a no-op; otherwise, it performs a 2-byte swap operation.

::: versionchanged
3.10 Raises `OverflowError`{.interpreted-text role="exc"} if *x* does not fit in a 16-bit unsigned integer.
:::
::::

::: function
inet_aton(ip_string)

Convert an IPv4 address from dotted-quad string format (for example, \'123.45.67.89\') to 32-bit packed binary format, as a bytes object four characters in length. This is useful when conversing with a program that uses the standard C library and needs objects of type `in_addr`{.interpreted-text role="c:struct"}, which is the C type for the 32-bit packed binary this function returns.

`inet_aton`{.interpreted-text role="func"} also accepts strings with less than three dots; see the Unix manual page `inet(3)`{.interpreted-text role="manpage"} for details.

If the IPv4 address string passed to this function is invalid, `OSError`{.interpreted-text role="exc"} will be raised. Note that exactly what is valid depends on the underlying C implementation of `inet_aton`{.interpreted-text role="c:func"}.

`inet_aton`{.interpreted-text role="func"} does not support IPv6, and `inet_pton`{.interpreted-text role="func"} should be used instead for IPv4/v6 dual stack support.
:::

:::: function
inet_ntoa(packed_ip)

Convert a 32-bit packed IPv4 address (a `bytes-like object`{.interpreted-text role="term"} four bytes in length) to its standard dotted-quad string representation (for example, \'123.45.67.89\'). This is useful when conversing with a program that uses the standard C library and needs objects of type `in_addr`{.interpreted-text role="c:struct"}, which is the C type for the 32-bit packed binary data this function takes as an argument.

If the byte sequence passed to this function is not exactly 4 bytes in length, `OSError`{.interpreted-text role="exc"} will be raised. `inet_ntoa`{.interpreted-text role="func"} does not support IPv6, and `inet_ntop`{.interpreted-text role="func"} should be used instead for IPv4/v6 dual stack support.

::: versionchanged
3.5 Writable `bytes-like object`{.interpreted-text role="term"} is now accepted.
:::
::::

::::: function
inet_pton(address_family, ip_string)

Convert an IP address from its family-specific string format to a packed, binary format. `inet_pton`{.interpreted-text role="func"} is useful when a library or network protocol calls for an object of type `in_addr`{.interpreted-text role="c:struct"} (similar to `inet_aton`{.interpreted-text role="func"}) or `in6_addr`{.interpreted-text role="c:struct"}.

Supported values for *address_family* are currently `AF_INET`{.interpreted-text role="const"} and `AF_INET6`{.interpreted-text role="const"}. If the IP address string *ip_string* is invalid, `OSError`{.interpreted-text role="exc"} will be raised. Note that exactly what is valid depends on both the value of *address_family* and the underlying implementation of `inet_pton`{.interpreted-text role="c:func"}.

::: availability
Unix, Windows.
:::

::: versionchanged
3.4 Windows support added
:::
:::::

:::::: function
inet_ntop(address_family, packed_ip)

Convert a packed IP address (a `bytes-like object`{.interpreted-text role="term"} of some number of bytes) to its standard, family-specific string representation (for example, `'7.10.0.5'` or `'5aef:2b::8'`). `inet_ntop`{.interpreted-text role="func"} is useful when a library or network protocol returns an object of type `in_addr`{.interpreted-text role="c:struct"} (similar to `inet_ntoa`{.interpreted-text role="func"}) or `in6_addr`{.interpreted-text role="c:struct"}.

Supported values for *address_family* are currently `AF_INET`{.interpreted-text role="const"} and `AF_INET6`{.interpreted-text role="const"}. If the bytes object *packed_ip* is not the correct length for the specified address family, `ValueError`{.interpreted-text role="exc"} will be raised. `OSError`{.interpreted-text role="exc"} is raised for errors from the call to `inet_ntop`{.interpreted-text role="func"}.

::: availability
Unix, Windows.
:::

::: versionchanged
3.4 Windows support added
:::

::: versionchanged
3.5 Writable `bytes-like object`{.interpreted-text role="term"} is now accepted.
:::
::::::

::::: function
CMSG_LEN(length)

Return the total length, without trailing padding, of an ancillary data item with associated data of the given *length*. This value can often be used as the buffer size for `~socket.recvmsg`{.interpreted-text role="meth"} to receive a single item of ancillary data, but `3542`{.interpreted-text role="rfc"} requires portable applications to use `CMSG_SPACE`{.interpreted-text role="func"} and thus include space for padding, even when the item will be the last in the buffer. Raises `OverflowError`{.interpreted-text role="exc"} if *length* is outside the permissible range of values.

::: availability
Unix, not WASI.

Most Unix platforms.
:::

::: versionadded
3.3
:::
:::::

::::: function
CMSG_SPACE(length)

Return the buffer size needed for `~socket.recvmsg`{.interpreted-text role="meth"} to receive an ancillary data item with associated data of the given *length*, along with any trailing padding. The buffer space needed to receive multiple items is the sum of the `CMSG_SPACE`{.interpreted-text role="func"} values for their associated data lengths. Raises `OverflowError`{.interpreted-text role="exc"} if *length* is outside the permissible range of values.

Note that some systems might support ancillary data without providing this function. Also note that setting the buffer size using the results of this function may not precisely limit the amount of ancillary data that can be received, since additional data may be able to fit into the padding area.

::: availability
Unix, not WASI.

most Unix platforms.
:::

::: versionadded
3.3
:::
:::::

::: function
getdefaulttimeout()

Return the default timeout in seconds (float) for new socket objects. A value of `None` indicates that new socket objects have no timeout. When the socket module is first imported, the default is `None`.
:::

:::: function
setdefaulttimeout(timeout)

Set the default timeout in seconds (real number) for new socket objects. When the socket module is first imported, the default is `None`. See `~socket.settimeout`{.interpreted-text role="meth"} for possible values and their respective meanings.

::: versionchanged
3.15 Accepts any real number, not only integer or float.
:::
::::

:::::: function
sethostname(name)

Set the machine\'s hostname to *name*. This will raise an `OSError`{.interpreted-text role="exc"} if you don\'t have enough rights.

::: audit-event
socket.sethostname name socket.sethostname
:::

::: availability
Unix, not Android.
:::

::: versionadded
3.3
:::
::::::

:::::::: function
if_nameindex()

Return a list of network interface information (index int, name string) tuples. `OSError`{.interpreted-text role="exc"} if the system call fails.

::: availability
Unix, Windows, not WASI.
:::

::: versionadded
3.3
:::

::: versionchanged
3.8 Windows support was added.
:::

:::: note
::: title
Note
:::

On Windows network interfaces have different names in different contexts (all names are examples):

- UUID: `{FB605B73-AAC2-49A6-9A2F-25416AEA0573}`
- name: `ethernet_32770`
- friendly name: `vEthernet (nat)`
- description: `Hyper-V Virtual Ethernet Adapter`

This function returns names of the second form from the list, `ethernet_32770` in this example case.
::::
::::::::

::::::: function
if_nametoindex(if_name)

Return a network interface index number corresponding to an interface name. `OSError`{.interpreted-text role="exc"} if no interface with the given name exists.

::: availability
Unix, Windows, not WASI.
:::

::: versionadded
3.3
:::

::: versionchanged
3.8 Windows support was added.
:::

::: seealso
\"Interface name\" is a name as documented in `if_nameindex`{.interpreted-text role="func"}.
:::
:::::::

::::::: function
if_indextoname(if_index)

Return a network interface name corresponding to an interface index number. `OSError`{.interpreted-text role="exc"} if no interface with the given index exists.

::: availability
Unix, Windows, not WASI.
:::

::: versionadded
3.3
:::

::: versionchanged
3.8 Windows support was added.
:::

::: seealso
\"Interface name\" is a name as documented in `if_nameindex`{.interpreted-text role="func"}.
:::
:::::::

::::: function
send_fds(sock, buffers, fds\[, flags\[, address\]\])

Send the list of file descriptors *fds* over an `AF_UNIX`{.interpreted-text role="const"} socket *sock*. The *fds* parameter is a sequence of file descriptors. Consult `~socket.sendmsg`{.interpreted-text role="meth"} for the documentation of these parameters.

::: availability
Unix, not WASI.

Unix platforms supporting `~socket.sendmsg`{.interpreted-text role="meth"} and `SCM_RIGHTS`{.interpreted-text role="const"} mechanism.
:::

::: versionadded
3.9
:::
:::::

::::::: function
recv_fds(sock, bufsize, maxfds\[, flags\])

Receive up to *maxfds* file descriptors from an `AF_UNIX`{.interpreted-text role="const"} socket *sock*. Return `(msg, list(fds), flags, addr)`. Consult `~socket.recvmsg`{.interpreted-text role="meth"} for the documentation of these parameters.

::: availability
Unix, not WASI.

Unix platforms supporting `~socket.recvmsg`{.interpreted-text role="meth"} and `SCM_RIGHTS`{.interpreted-text role="const"} mechanism.
:::

::: versionadded
3.9
:::

:::: note
::: title
Note
:::

Any truncated integers at the end of the list of file descriptors.
::::
:::::::

## Socket Objects

Socket objects have the following methods. Except for `~socket.makefile`{.interpreted-text role="meth"}, these correspond to Unix system calls applicable to sockets.

::: versionchanged
3.2 Support for the `context manager`{.interpreted-text role="term"} protocol was added. Exiting the context manager is equivalent to calling `~socket.close`{.interpreted-text role="meth"}.
:::

::::: method
socket.accept()

Accept a connection. The socket must be bound to an address and listening for connections. The return value is a pair `(conn, address)` where *conn* is a *new* socket object usable to send and receive data on the connection, and *address* is the address bound to the socket on the other end of the connection.

The newly created socket is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

::: versionchanged
3.4 The socket is now non-inheritable.
:::

::: versionchanged
3.5 If the system call is interrupted and the signal handler does not raise an exception, the method now retries the system call instead of raising an `InterruptedError`{.interpreted-text role="exc"} exception (see `475`{.interpreted-text role="pep"} for the rationale).
:::
:::::

::::: method
socket.bind(address)

Bind the socket to *address*. The socket must not already be bound. (The format of *address* depends on the address family \-\-- see above.)

::: audit-event
socket.bind self,address socket.socket.bind
:::

::: availability
not WASI.
:::
:::::

:::::: method
socket.close()

Mark the socket closed. The underlying system resource (e.g. a file descriptor) is also closed when all file objects from `makefile`{.interpreted-text role="meth"} are closed. Once that happens, all future operations on the socket object will fail. The remote end will receive no more data (after queued data is flushed).

Sockets are automatically closed when they are garbage-collected, but it is recommended to `close`{.interpreted-text role="meth"} them explicitly, or to use a `with`{.interpreted-text role="keyword"} statement around them.

::: versionchanged
3.6 `OSError`{.interpreted-text role="exc"} is now raised if an error occurs when the underlying `close`{.interpreted-text role="c:func"} call is made.
:::

:::: note
::: title
Note
:::

`close`{.interpreted-text role="meth"} releases the resource associated with a connection but does not necessarily close the connection immediately. If you want to close the connection in a timely fashion, call `shutdown`{.interpreted-text role="meth"} before `close`{.interpreted-text role="meth"}.
::::
::::::

:::::: method
socket.connect(address)

Connect to a remote socket at *address*. (The format of *address* depends on the address family \-\-- see above.)

If the connection is interrupted by a signal, the method waits until the connection completes, or raises a `TimeoutError`{.interpreted-text role="exc"} on timeout, if the signal handler doesn\'t raise an exception and the socket is blocking or has a timeout. For non-blocking sockets, the method raises an `InterruptedError`{.interpreted-text role="exc"} exception if the connection is interrupted by a signal (or the exception raised by the signal handler).

::: audit-event
socket.connect self,address socket.socket.connect
:::

::: versionchanged
3.5 The method now waits until the connection completes instead of raising an `InterruptedError`{.interpreted-text role="exc"} exception if the connection is interrupted by a signal, the signal handler doesn\'t raise an exception and the socket is blocking or has a timeout (see the `475`{.interpreted-text role="pep"} for the rationale).
:::

::: availability
not WASI.
:::
::::::

::::: method
socket.connect_ex(address)

Like `connect(address)`, but return an error indicator instead of raising an exception for errors returned by the C-level `connect`{.interpreted-text role="c:func"} call (other problems, such as \"host not found,\" can still raise exceptions). The error indicator is `0` if the operation succeeded, otherwise the value of the `errno`{.interpreted-text role="c:data"} variable. This is useful to support, for example, asynchronous connects.

::: audit-event
socket.connect self,address socket.socket.connect_ex
:::

::: availability
not WASI.
:::
:::::

:::: method
socket.detach()

Put the socket object into closed state without actually closing the underlying file descriptor. The file descriptor is returned, and can be reused for other purposes.

::: versionadded
3.2
:::
::::

::::: method
socket.dup()

Duplicate the socket.

The newly created socket is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

::: versionchanged
3.4 The socket is now non-inheritable.
:::

::: availability
not WASI.
:::
:::::

::: method
socket.fileno()

Return the socket\'s file descriptor (a small integer), or -1 on failure. This is useful with `select.select`{.interpreted-text role="func"}.

Under Windows the small integer returned by this method cannot be used where a file descriptor can be used (such as `os.fdopen`{.interpreted-text role="func"}). Unix does not have this limitation.
:::

:::: method
socket.get_inheritable()

Get the `inheritable flag <fd_inheritance>`{.interpreted-text role="ref"} of the socket\'s file descriptor or socket\'s handle: `True` if the socket can be inherited in child processes, `False` if it cannot.

::: versionadded
3.4
:::
::::

::: method
socket.getpeername()

Return the remote address to which the socket is connected. This is useful to find out the port number of a remote IPv4/v6 socket, for instance. (The format of the address returned depends on the address family \-\-- see above.) On some systems this function is not supported.
:::

::: method
socket.getsockname()

Return the socket\'s own address. This is useful to find out the port number of an IPv4/v6 socket, for instance. (The format of the address returned depends on the address family \-\-- see above.)
:::

:::: method
socket.getsockopt(level, optname\[, buflen\])

Return the value of the given socket option (see the Unix man page `getsockopt(2)`{.interpreted-text role="manpage"}). The needed symbolic constants (`SO_\* etc. <socket-unix-constants>`{.interpreted-text role="ref"}) are defined in this module. If *buflen* is absent, an integer option is assumed and its integer value is returned by the function. If *buflen* is present, it specifies the maximum length of the buffer used to receive the option in, and this buffer is returned as a bytes object. It is up to the caller to decode the contents of the buffer (see the optional built-in module `struct`{.interpreted-text role="mod"} for a way to decode C structures encoded as byte strings).

::: availability
not WASI.
:::
::::

:::: method
socket.getblocking()

Return `True` if socket is in blocking mode, `False` if in non-blocking.

This is equivalent to checking `socket.gettimeout() != 0`.

::: versionadded
3.7
:::
::::

::: method
socket.gettimeout()

Return the timeout in seconds (float) associated with socket operations, or `None` if no timeout is set. This reflects the last call to `setblocking`{.interpreted-text role="meth"} or `settimeout`{.interpreted-text role="meth"}.
:::

::::: method
socket.ioctl(control, option)

The `ioctl`{.interpreted-text role="meth"} method is a limited interface to the WSAIoctl system interface. Please refer to the [Win32 documentation](https://msdn.microsoft.com/en-us/library/ms741621%28VS.85%29.aspx) for more information.

On other platforms, the generic `fcntl.fcntl`{.interpreted-text role="func"} and `fcntl.ioctl`{.interpreted-text role="func"} functions may be used; they accept a socket object as their first argument.

Currently only the following control codes are supported: `SIO_RCVALL`, `SIO_KEEPALIVE_VALS`, and `SIO_LOOPBACK_FAST_PATH`.

::: availability
Windows
:::

::: versionchanged
3.6 `SIO_LOOPBACK_FAST_PATH` was added.
:::
:::::

::::: method
socket.listen(\[backlog\])

Enable a server to accept connections. If *backlog* is specified, it must be at least 0 (if it is lower, it is set to 0); it specifies the number of unaccepted connections that the system will allow before refusing new connections. If not specified, a default reasonable value is chosen.

::: availability
not WASI.
:::

::: versionchanged
3.5 The *backlog* parameter is now optional.
:::
:::::

:::::: method
socket.makefile(mode=\'r\', buffering=None, \*, encoding=None, errors=None, newline=None)

::: index
single: I/O control; buffering
:::

Return a `file object`{.interpreted-text role="term"} associated with the socket. The exact returned type depends on the arguments given to `makefile`{.interpreted-text role="meth"}. These arguments are interpreted the same way as by the built-in `open`{.interpreted-text role="func"} function, except the only supported *mode* values are `'r'` (default), `'w'`, `'b'`, or a combination of those.

The socket must be in blocking mode; it can have a timeout, but the file object\'s internal buffer may end up in an inconsistent state if a timeout occurs.

Closing the file object returned by `makefile`{.interpreted-text role="meth"} won\'t close the original socket unless all other file objects have been closed and `socket.close`{.interpreted-text role="meth"} has been called on the socket object.

:::: note
::: title
Note
:::

On Windows, the file-like object created by `makefile`{.interpreted-text role="meth"} cannot be used where a file object with a file descriptor is expected, such as the stream arguments of `subprocess.Popen`{.interpreted-text role="meth"}.
::::
::::::

:::: method
socket.recv(bufsize\[, flags\])

Receive data from the socket. The return value is a bytes object representing the data received. The maximum amount of data to be received at once is specified by *bufsize*. A returned empty bytes object indicates that the client has disconnected. See the Unix manual page `recv(2)`{.interpreted-text role="manpage"} for the meaning of the optional argument *flags*; it defaults to zero.

::: versionchanged
3.5 If the system call is interrupted and the signal handler does not raise an exception, the method now retries the system call instead of raising an `InterruptedError`{.interpreted-text role="exc"} exception (see `475`{.interpreted-text role="pep"} for the rationale).
:::
::::

::::: method
socket.recvfrom(bufsize\[, flags\])

Receive data from the socket. The return value is a pair `(bytes, address)` where *bytes* is a bytes object representing the data received and *address* is the address of the socket sending the data. See the Unix manual page `recv(2)`{.interpreted-text role="manpage"} for the meaning of the optional argument *flags*; it defaults to zero. (The format of *address* depends on the address family \-\-- see above.)

::: versionchanged
3.5 If the system call is interrupted and the signal handler does not raise an exception, the method now retries the system call instead of raising an `InterruptedError`{.interpreted-text role="exc"} exception (see `475`{.interpreted-text role="pep"} for the rationale).
:::

::: versionchanged
3.7 For multicast IPv6 address, first item of *address* does not contain `%scope_id` part anymore. In order to get full IPv6 address use `getnameinfo`{.interpreted-text role="func"}.
:::
:::::

:::::: method
socket.recvmsg(bufsize\[, ancbufsize\[, flags\]\])

Receive normal data (up to *bufsize* bytes) and ancillary data from the socket. The *ancbufsize* argument sets the size in bytes of the internal buffer used to receive the ancillary data; it defaults to 0, meaning that no ancillary data will be received. Appropriate buffer sizes for ancillary data can be calculated using `CMSG_SPACE`{.interpreted-text role="func"} or `CMSG_LEN`{.interpreted-text role="func"}, and items which do not fit into the buffer might be truncated or discarded. The *flags* argument defaults to 0 and has the same meaning as for `recv`{.interpreted-text role="meth"}.

The return value is a 4-tuple: `(data, ancdata, msg_flags, address)`. The *data* item is a `bytes`{.interpreted-text role="class"} object holding the non-ancillary data received. The *ancdata* item is a list of zero or more tuples `(cmsg_level, cmsg_type, cmsg_data)` representing the ancillary data (control messages) received: *cmsg_level* and *cmsg_type* are integers specifying the protocol level and protocol-specific type respectively, and *cmsg_data* is a `bytes`{.interpreted-text role="class"} object holding the associated data. The *msg_flags* item is the bitwise OR of various flags indicating conditions on the received message; see your system documentation for details. If the receiving socket is unconnected, *address* is the address of the sending socket, if available; otherwise, its value is unspecified.

On some systems, `sendmsg`{.interpreted-text role="meth"} and `recvmsg`{.interpreted-text role="meth"} can be used to pass file descriptors between processes over an `AF_UNIX`{.interpreted-text role="const"} socket. When this facility is used (it is often restricted to `SOCK_STREAM`{.interpreted-text role="const"} sockets), `recvmsg`{.interpreted-text role="meth"} will return, in its ancillary data, items of the form `(socket.SOL_SOCKET, socket.SCM_RIGHTS, fds)`, where *fds* is a `bytes`{.interpreted-text role="class"} object representing the new file descriptors as a binary array of the native C `int`{.interpreted-text role="c:expr"} type. If `recvmsg`{.interpreted-text role="meth"} raises an exception after the system call returns, it will first attempt to close any file descriptors received via this mechanism.

Some systems do not indicate the truncated length of ancillary data items which have been only partially received. If an item appears to extend beyond the end of the buffer, `recvmsg`{.interpreted-text role="meth"} will issue a `RuntimeWarning`{.interpreted-text role="exc"}, and will return the part of it which is inside the buffer provided it has not been truncated before the start of its associated data.

On systems which support the `SCM_RIGHTS`{.interpreted-text role="const"} mechanism, the following function will receive up to *maxfds* file descriptors, returning the message data and a list containing the descriptors (while ignoring unexpected conditions such as unrelated control messages being received). See also `sendmsg`{.interpreted-text role="meth"}. :

    import socket, array

    def recv_fds(sock, msglen, maxfds):
        fds = array.array("i")   # Array of ints
        msg, ancdata, flags, addr = sock.recvmsg(msglen, socket.CMSG_LEN(maxfds * fds.itemsize))
        for cmsg_level, cmsg_type, cmsg_data in ancdata:
            if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
                # Append data, ignoring any truncated integers at the end.
                fds.frombytes(cmsg_data[:len(cmsg_data) - (len(cmsg_data) % fds.itemsize)])
        return msg, list(fds)

::: availability
Unix.

Most Unix platforms.
:::

::: versionadded
3.3
:::

::: versionchanged
3.5 If the system call is interrupted and the signal handler does not raise an exception, the method now retries the system call instead of raising an `InterruptedError`{.interpreted-text role="exc"} exception (see `475`{.interpreted-text role="pep"} for the rationale).
:::
::::::

::::: method
socket.recvmsg_into(buffers\[, ancbufsize\[, flags\]\])

Receive normal data and ancillary data from the socket, behaving as `recvmsg`{.interpreted-text role="meth"} would, but scatter the non-ancillary data into a series of buffers instead of returning a new bytes object. The *buffers* argument must be an iterable of objects that export writable buffers (e.g. `bytearray`{.interpreted-text role="class"} objects); these will be filled with successive chunks of the non-ancillary data until it has all been written or there are no more buffers. The operating system may set a limit (`~os.sysconf`{.interpreted-text role="func"} value `SC_IOV_MAX`) on the number of buffers that can be used. The *ancbufsize* and *flags* arguments have the same meaning as for `recvmsg`{.interpreted-text role="meth"}.

The return value is a 4-tuple: `(nbytes, ancdata, msg_flags, address)`, where *nbytes* is the total number of bytes of non-ancillary data written into the buffers, and *ancdata*, *msg_flags* and *address* are the same as for `recvmsg`{.interpreted-text role="meth"}.

Example:

    >>> import socket
    >>> s1, s2 = socket.socketpair()
    >>> b1 = bytearray(b'----')
    >>> b2 = bytearray(b'0123456789')
    >>> b3 = bytearray(b'--------------')
    >>> s1.send(b'Mary had a little lamb')
    22
    >>> s2.recvmsg_into([b1, memoryview(b2)[2:9], b3])
    (22, [], 0, None)
    >>> [b1, b2, b3]
    [bytearray(b'Mary'), bytearray(b'01 had a 9'), bytearray(b'little lamb---')]

::: availability
Unix.

Most Unix platforms.
:::

::: versionadded
3.3
:::
:::::

::: method
socket.recvfrom_into(buffer\[, nbytes\[, flags\]\])

Receive data from the socket, writing it into *buffer* instead of creating a new bytestring. The return value is a pair `(nbytes, address)` where *nbytes* is the number of bytes received and *address* is the address of the socket sending the data. See the Unix manual page `recv(2)`{.interpreted-text role="manpage"} for the meaning of the optional argument *flags*; it defaults to zero. (The format of *address* depends on the address family \-\-- see above.)
:::

::: method
socket.recv_into(buffer\[, nbytes\[, flags\]\])

Receive up to *nbytes* bytes from the socket, storing the data into a buffer rather than creating a new bytestring. If *nbytes* is not specified (or 0), receive up to the size available in the given buffer. Returns the number of bytes received. See the Unix manual page `recv(2)`{.interpreted-text role="manpage"} for the meaning of the optional argument *flags*; it defaults to zero.
:::

:::: method
socket.send(bytes\[, flags\])

Send data to the socket. The socket must be connected to a remote socket. The optional *flags* argument has the same meaning as for `recv`{.interpreted-text role="meth"} above. Returns the number of bytes sent. Applications are responsible for checking that all data has been sent; if only some of the data was transmitted, the application needs to attempt delivery of the remaining data. For further information on this topic, consult the `socket-howto`{.interpreted-text role="ref"}.

::: versionchanged
3.5 If the system call is interrupted and the signal handler does not raise an exception, the method now retries the system call instead of raising an `InterruptedError`{.interpreted-text role="exc"} exception (see `475`{.interpreted-text role="pep"} for the rationale).
:::
::::

::::: method
socket.sendall(bytes\[, flags\])

Send data to the socket. The socket must be connected to a remote socket. The optional *flags* argument has the same meaning as for `recv`{.interpreted-text role="meth"} above. Unlike `send`{.interpreted-text role="meth"}, this method continues to send data from *bytes* until either all data has been sent or an error occurs. `None` is returned on success. On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent.

::: versionchanged
3.5 The socket timeout is no longer reset each time data is sent successfully. The socket timeout is now the maximum total duration to send all data.
:::

::: versionchanged
3.5 If the system call is interrupted and the signal handler does not raise an exception, the method now retries the system call instead of raising an `InterruptedError`{.interpreted-text role="exc"} exception (see `475`{.interpreted-text role="pep"} for the rationale).
:::
:::::

::::: method
socket.sendto(bytes, address) socket.sendto(bytes, flags, address)

Send data to the socket. The socket should not be connected to a remote socket, since the destination socket is specified by *address*. The optional *flags* argument has the same meaning as for `recv`{.interpreted-text role="meth"} above. Return the number of bytes sent. (The format of *address* depends on the address family \-\-- see above.)

::: audit-event
socket.sendto self,address socket.socket.sendto
:::

::: versionchanged
3.5 If the system call is interrupted and the signal handler does not raise an exception, the method now retries the system call instead of raising an `InterruptedError`{.interpreted-text role="exc"} exception (see `475`{.interpreted-text role="pep"} for the rationale).
:::
:::::

::::::: method
socket.sendmsg(buffers\[, ancdata\[, flags\[, address\]\]\])

Send normal and ancillary data to the socket, gathering the non-ancillary data from a series of buffers and concatenating it into a single message. The *buffers* argument specifies the non-ancillary data as an iterable of `bytes-like objects <bytes-like object>`{.interpreted-text role="term"} (e.g. `bytes`{.interpreted-text role="class"} objects); the operating system may set a limit (`~os.sysconf`{.interpreted-text role="func"} value `SC_IOV_MAX`) on the number of buffers that can be used. The *ancdata* argument specifies the ancillary data (control messages) as an iterable of zero or more tuples `(cmsg_level, cmsg_type, cmsg_data)`, where *cmsg_level* and *cmsg_type* are integers specifying the protocol level and protocol-specific type respectively, and *cmsg_data* is a bytes-like object holding the associated data. Note that some systems (in particular, systems without `CMSG_SPACE`{.interpreted-text role="func"}) might support sending only one control message per call. The *flags* argument defaults to 0 and has the same meaning as for `send`{.interpreted-text role="meth"}. If *address* is supplied and not `None`, it sets a destination address for the message. The return value is the number of bytes of non-ancillary data sent.

The following function sends the list of file descriptors *fds* over an `AF_UNIX`{.interpreted-text role="const"} socket, on systems which support the `SCM_RIGHTS`{.interpreted-text role="const"} mechanism. See also `recvmsg`{.interpreted-text role="meth"}. :

    import socket, array

    def send_fds(sock, msg, fds):
        return sock.sendmsg([msg], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, array.array("i", fds))])

::: availability
Unix, not WASI.

Most Unix platforms.
:::

::: audit-event
socket.sendmsg self,address socket.socket.sendmsg
:::

::: versionadded
3.3
:::

::: versionchanged
3.5 If the system call is interrupted and the signal handler does not raise an exception, the method now retries the system call instead of raising an `InterruptedError`{.interpreted-text role="exc"} exception (see `475`{.interpreted-text role="pep"} for the rationale).
:::
:::::::

::::: method
socket.sendmsg_afalg(\[msg\], \*, op\[, iv\[, assoclen\[, flags\]\]\])

Specialized version of `~socket.sendmsg`{.interpreted-text role="meth"} for `AF_ALG`{.interpreted-text role="const"} socket. Set mode, IV, AEAD associated data length and flags for `AF_ALG`{.interpreted-text role="const"} socket.

::: availability
Linux \>= 2.6.38.
:::

::: versionadded
3.6
:::
:::::

:::: method
socket.sendfile(file, offset=0, count=None)

Send a file until EOF is reached by using high-performance `os.sendfile`{.interpreted-text role="mod"} and return the total number of bytes which were sent. *file* must be a regular file object opened in binary mode. If `os.sendfile`{.interpreted-text role="mod"} is not available (e.g. Windows) or *file* is not a regular file `send`{.interpreted-text role="meth"} will be used instead. *offset* tells from where to start reading the file. If specified, *count* is the total number of bytes to transmit as opposed to sending the file until EOF is reached. File position is updated on return or also in case of error in which case `file.tell() <io.IOBase.tell>`{.interpreted-text role="meth"} can be used to figure out the number of bytes which were sent. The socket must be of `SOCK_STREAM`{.interpreted-text role="const"} type. Non-blocking sockets are not supported.

::: versionadded
3.5
:::
::::

:::: method
socket.set_inheritable(inheritable)

Set the `inheritable flag <fd_inheritance>`{.interpreted-text role="ref"} of the socket\'s file descriptor or socket\'s handle.

::: versionadded
3.4
:::
::::

:::: method
socket.setblocking(flag)

Set blocking or non-blocking mode of the socket: if *flag* is false, the socket is set to non-blocking, else to blocking mode.

This method is a shorthand for certain `~socket.settimeout`{.interpreted-text role="meth"} calls:

- `sock.setblocking(True)` is equivalent to `sock.settimeout(None)`
- `sock.setblocking(False)` is equivalent to `sock.settimeout(0.0)`

::: versionchanged
3.7 The method no longer applies `SOCK_NONBLOCK`{.interpreted-text role="const"} flag on `socket.type`{.interpreted-text role="attr"}.
:::
::::

::::: method
socket.settimeout(value)

Set a timeout on blocking socket operations. The *value* argument can be a nonnegative real number expressing seconds, or `None`. If a non-zero value is given, subsequent socket operations will raise a `timeout`{.interpreted-text role="exc"} exception if the timeout period *value* has elapsed before the operation has completed. If zero is given, the socket is put in non-blocking mode. If `None` is given, the socket is put in blocking mode.

For further information, please consult the `notes on socket timeouts <socket-timeouts>`{.interpreted-text role="ref"}.

::: versionchanged
3.7 The method no longer toggles `SOCK_NONBLOCK`{.interpreted-text role="const"} flag on `socket.type`{.interpreted-text role="attr"}.
:::

::: versionchanged
3.15 Accepts any real number, not only integer or float.
:::
:::::

::::::: method
socket.setsockopt(level, optname, value: int \| Buffer) socket.setsockopt(level, optname, None, optlen: int)

::: index
pair: module; struct
:::

Set the value of the given socket option (see the Unix manual page `setsockopt(2)`{.interpreted-text role="manpage"}). The needed symbolic constants are defined in this module (`!SO_\* etc. <socket-unix-constants>`{.interpreted-text role="ref"}). The value can be an integer, `None` or a `bytes-like object`{.interpreted-text role="term"} representing a buffer. In the latter case it is up to the caller to ensure that the bytestring contains the proper bits (see the optional built-in module `struct`{.interpreted-text role="mod"} for a way to encode C structures as bytestrings). When *value* is set to `None`, *optlen* argument is required. It\'s equivalent to calling `setsockopt`{.interpreted-text role="c:func"} C function with `optval=NULL` and `optlen=optlen`.

::: versionchanged
3.5 Writable `bytes-like object`{.interpreted-text role="term"} is now accepted.
:::

::: versionchanged
3.6 setsockopt(level, optname, None, optlen: int) form added.
:::

::: availability
not WASI.
:::
:::::::

:::: method
socket.shutdown(how)

Shut down one or both halves of the connection. If *how* is `SHUT_RD`{.interpreted-text role="const"}, further receives are disallowed. If *how* is `SHUT_WR`{.interpreted-text role="const"}, further sends are disallowed. If *how* is `SHUT_RDWR`{.interpreted-text role="const"}, further sends and receives are disallowed.

::: availability
not WASI.
:::
::::

::::: method
socket.share(process_id)

Duplicate a socket and prepare it for sharing with a target process. The target process must be provided with *process_id*. The resulting bytes object can then be passed to the target process using some form of interprocess communication and the socket can be recreated there using `fromshare`{.interpreted-text role="func"}. Once this method has been called, it is safe to close the socket since the operating system has already duplicated it for the target process.

::: availability
Windows.
:::

::: versionadded
3.3
:::
:::::

Note that there are no methods `read`{.interpreted-text role="meth"} or `write`{.interpreted-text role="meth"}; use `~socket.recv`{.interpreted-text role="meth"} and `~socket.send`{.interpreted-text role="meth"} without *flags* argument instead.

Socket objects also have these (read-only) attributes that correspond to the values given to the `~socket.socket`{.interpreted-text role="class"} constructor.

::: attribute
socket.family

The socket family.
:::

::: attribute
socket.type

The socket type.
:::

::: attribute
socket.proto

The socket protocol.
:::

## Notes on socket timeouts {#socket-timeouts}

A socket object can be in one of three modes: blocking, non-blocking, or timeout. Sockets are by default always created in blocking mode, but this can be changed by calling `setdefaulttimeout`{.interpreted-text role="func"}.

- In *blocking mode*, operations block until complete or the system returns an error (such as connection timed out).
- In *non-blocking mode*, operations fail (with an error that is unfortunately system-dependent) if they cannot be completed immediately: functions from the `select`{.interpreted-text role="mod"} module can be used to know when and whether a socket is available for reading or writing.
- In *timeout mode*, operations fail if they cannot be completed within the timeout specified for the socket (they raise a `timeout`{.interpreted-text role="exc"} exception) or if the system returns an error.

:::: note
::: title
Note
:::

At the operating system level, sockets in *timeout mode* are internally set in non-blocking mode. Also, the blocking and timeout modes are shared between file descriptors and socket objects that refer to the same network endpoint. This implementation detail can have visible consequences if e.g. you decide to use the `~socket.fileno`{.interpreted-text role="meth"} of a socket.
::::

### Timeouts and the `connect` method

The `~socket.connect`{.interpreted-text role="meth"} operation is also subject to the timeout setting, and in general it is recommended to call `~socket.settimeout`{.interpreted-text role="meth"} before calling `~socket.connect`{.interpreted-text role="meth"} or pass a timeout parameter to `create_connection`{.interpreted-text role="meth"}. However, the system network stack may also return a connection timeout error of its own regardless of any Python socket timeout setting.

### Timeouts and the `accept` method

If `getdefaulttimeout`{.interpreted-text role="func"} is not `None`{.interpreted-text role="const"}, sockets returned by the `~socket.accept`{.interpreted-text role="meth"} method inherit that timeout. Otherwise, the behaviour depends on settings of the listening socket:

- if the listening socket is in *blocking mode* or in *timeout mode*, the socket returned by `~socket.accept`{.interpreted-text role="meth"} is in *blocking mode*;
- if the listening socket is in *non-blocking mode*, whether the socket returned by `~socket.accept`{.interpreted-text role="meth"} is in blocking or non-blocking mode is operating system-dependent. If you want to ensure cross-platform behaviour, it is recommended you manually override this setting.

## Example {#socket-example}

Here are four minimal example programs using the TCP/IP protocol: a server that echoes all data that it receives back (servicing only one client), and a client using it. Note that a server must perform the sequence `~socket.socket`{.interpreted-text role="func"}, `~socket.bind`{.interpreted-text role="meth"}, `~socket.listen`{.interpreted-text role="meth"}, `~socket.accept`{.interpreted-text role="meth"} (possibly repeating the `~socket.accept`{.interpreted-text role="meth"} to service more than one client), while a client only needs the sequence `~socket.socket`{.interpreted-text role="func"}, `~socket.connect`{.interpreted-text role="meth"}. Also note that the server does not `~socket.sendall`{.interpreted-text role="meth"}/`~socket.recv`{.interpreted-text role="meth"} on the socket it is listening on but on the new socket returned by `~socket.accept`{.interpreted-text role="meth"}.

The first two examples support IPv4 only. :

    # Echo server program
    import socket

    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data: break
                conn.sendall(data)

    # Echo client program
    import socket

    HOST = 'daring.cwi.nl'    # The remote host
    PORT = 50007              # The same port as used by the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hello, world')
        data = s.recv(1024)
    print('Received', repr(data))

The next two examples are identical to the above two, but support both IPv4 and IPv6. The server side will listen to the first address family available (it should listen to both instead). On most of IPv6-ready systems, IPv6 will take precedence and the server may not accept IPv4 traffic. The client side will try to connect to all the addresses returned as a result of the name resolution, and sends traffic to the first one connected successfully. :

    # Echo server program
    import socket
    import sys

    HOST = None               # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                  socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.bind(sa)
            s.listen(1)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print('could not open socket')
        sys.exit(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            conn.send(data)

    # Echo client program
    import socket
    import sys

    HOST = 'daring.cwi.nl'    # The remote host
    PORT = 50007              # The same port as used by the server
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print('could not open socket')
        sys.exit(1)
    with s:
        s.sendall(b'Hello, world')
        data = s.recv(1024)
    print('Received', repr(data))

The next example shows how to write a very simple network sniffer with raw sockets on Windows. The example requires administrator privileges to modify the interface:

    import socket

    # the public network interface
    HOST = socket.gethostbyname(socket.gethostname())

    # create a raw socket and bind it to the public interface
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    s.bind((HOST, 0))

    # Include IP headers
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # receive all packets
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    # receive a packet
    print(s.recvfrom(65565))

    # disabled promiscuous mode
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

The next example shows how to use the socket interface to communicate to a CAN network using the raw socket protocol. To use CAN with the broadcast manager protocol instead, open a socket with:

    socket.socket(socket.AF_CAN, socket.SOCK_DGRAM, socket.CAN_BCM)

After binding (`CAN_RAW`{.interpreted-text role="const"}) or connecting (`CAN_BCM`{.interpreted-text role="const"}) the socket, you can use the `socket.send`{.interpreted-text role="meth"} and `socket.recv`{.interpreted-text role="meth"} operations (and their counterparts) on the socket object as usual.

This last example might require special privileges:

    import socket
    import struct


    # CAN frame packing/unpacking (see 'struct can_frame' in <linux/can.h>)

    can_frame_fmt = "=IB3x8s"
    can_frame_size = struct.calcsize(can_frame_fmt)

    def build_can_frame(can_id, data):
        can_dlc = len(data)
        data = data.ljust(8, b'\x00')
        return struct.pack(can_frame_fmt, can_id, can_dlc, data)

    def dissect_can_frame(frame):
        can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
        return (can_id, can_dlc, data[:can_dlc])


    # create a raw socket and bind it to the 'vcan0' interface
    s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
    s.bind(('vcan0',))

    while True:
        cf, addr = s.recvfrom(can_frame_size)

        print('Received: can_id=%x, can_dlc=%x, data=%s' % dissect_can_frame(cf))

        try:
            s.send(cf)
        except OSError:
            print('Error sending CAN frame')

        try:
            s.send(build_can_frame(0x01, b'\x01\x02\x03'))
        except OSError:
            print('Error sending CAN frame')

Running an example several times with too small delay between executions, could lead to this error:

    OSError: [Errno 98] Address already in use

This is because the previous execution has left the socket in a `TIME_WAIT` state, and can\'t be immediately reused.

There is a `!socket`{.interpreted-text role="mod"} flag to set, in order to prevent this, `socket.SO_REUSEADDR`{.interpreted-text role="const"}:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))

the `SO_REUSEADDR`{.interpreted-text role="data"} flag tells the kernel to reuse a local socket in `TIME_WAIT` state, without waiting for its natural timeout to expire.

::: seealso
For an introduction to socket programming (in C), see the following papers:

- *An Introductory 4.3BSD Interprocess Communication Tutorial*, by Stuart Sechrest
- *An Advanced 4.3BSD Interprocess Communication Tutorial*, by Samuel J. Leffler et al,

both in the UNIX Programmer\'s Manual, Supplementary Documents 1 (sections PS1:7 and PS1:8). The platform-specific reference material for the various socket-related system calls are also a valuable source of information on the details of socket semantics. For Unix, refer to the manual pages; for Windows, see the WinSock (or Winsock 2) specification. For IPv6-ready APIs, readers may want to refer to `3493`{.interpreted-text role="rfc"} titled Basic Socket Interface Extensions for IPv6.
:::
