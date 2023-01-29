# mptcplib
![license MIT badge](https://badgen.net/badge/license/MIT/blue)
![tests](https://github.com/mptcp-apps/mptcplib/actions/workflows/tests.yaml/badge.svg)

## About
A Multipath TCP Python extension module. The core of this library is written in C in order to provide support for Multipath TCP in Python faster than standard CPython. For a deeper read about Multipath TCP, please consult this [webpage](https://obonaventure.github.io/mmtp-book/).

## Table of content

- Example Usage
- Description
- License

## Example Usage
---

To be able to use the library we encourage to install using [PyPi](https://pypi.org/). Run the following command:
 
```
pip install mptcplib
```
 
In order to check if a socket is still a MPTCP socket, you can use the following example :
 
```py
import mptcplib

with mptcplib.create_mptcp_socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    ... # Do other things
    if mptcplib.socket_is_mptcp(sock):
        ... # Do things for MPTCP socket
    else:
        ... # Falled back to TCP
```
 
There are other useful functions such as getting the number of subflows used by a MPTCP connection, check if the os supports MPTCP and that it is enabled, etc. We intend to make a Sphinx doccumentation website available soon.

## Description
---

The library is currently supported on Linux kernels but the goal will be to extend it to MacOS. Below is a table containing operating systems that supports Multipath TCP their support in mptcplib.

| Operating System | mptcplib support | 
| ----------- | :-----------: |
| MacOS (Big Sur, Ventura) | Not yet |
| Ubuntu (>= 22.04) | Yes |
| CentOS | TBA |
| Debain | TBA |

## Contributing
---
Pull requests are more than welcome. For major changes, please open an issue discussing what you would like to change.

To install the library in developper mode run the following command in the root directory:
 
```
make dev-install
```
 
In order to run the tests, you have to first install the library in developper mode then you can follow up with:
 
```
make test
```
 
## License
---
The repository is under the MIT License, leaving enough freedom to enable wanting to play around with the code base.