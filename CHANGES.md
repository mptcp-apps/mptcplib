# Version 0.1.3 - Date : February 5, 2023
- Remove all the C-extensions files.
- Moved package distribution from source distribution to wheels.
- Changed the API of the library to take the socket object instead of jus the file descriptor.
- Added check to see if MPTCP module is present.
- Refactoring and error fixing.

# Version 0.1.2 - Date : December 15, 2022
- Fixing errors.
- Reliable implementation of "used_subflows".
- Addition used_flows tests in the "test_io".
- Clear "used_subflows" function docstring. 

# Version 0.1.1 - Date : December 13, 2022
- First successful publish to PyPi.