# mptcplib
![license MIT badge](https://badgen.net/badge/license/MIT/blue)
![tests](https://github.com/mptcp-apps/mptcplib/actions/workflows/tests.yaml/badge.svg)

## About
A Multipath TCP Python library. We encourage users to actovate notifications since the library is still in it's early stages and the API may change. For certain functions are are availabke starting from a certain kernel release we encourage the user's to check the kernel implementation [changelog](https://github.com/multipath-tcp/mptcp_net-next/wiki#changelog).

For a deeper read about Multipath TCP, please consult this [webpage](https://obonaventure.github.io/mmtp-book/).

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
 
Below you see an example of a typical socket script :
```Python
import mptcplib
import socket 

socket = mptcplib.create_mptcp_socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
# Do things ...
if mptcplib.is_socket_mptcp(socket):
    # Do things in case of an MPTCP socket
    used_subflows = mptcplib.
else:
    # Handle fallback to standard TCP socket
socket.close()

```
 
There are other useful functions check if the os supports MPTCP and that it is enabled. We intend to add more kernel supported functions available. 

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