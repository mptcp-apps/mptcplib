from distutils.core import setup, Extension
linux_modules = Extension("mptcplib._mptcplib_linux", 
                    include_dirs=["mptcplib/include"],
                    sources=["mptcplib/src/_mptcplib_linux.c"]
                )
long_description = ""
with open('README.md') as file:
    long_description = file.read()

CLASSIFIERS = """\
Development Status :: 1 - Planning
License :: OSI Approved :: MIT License
Programming Language :: C
Programming Language :: Python
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: Implementation :: CPython
Topic :: System :: Networking
Topic :: System :: Operating System Kernels :: Linux
Typing :: Typed
Operating System :: POSIX
Operating System :: Unix
Operating System :: POSIX :: Linux
"""

setup(
    name="mptcplib", 
    version="0.1.1", 
    description="A Multipath TCP python support library",
    ext_modules=[linux_modules],
    packages=['mptcplib'],
    package_data={
        "mptcplib": ["py.typed", "*.pyi", "**/*.pyi"]
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms=["Linux"], 
    classifiers=CLASSIFIERS,
    python_requires='>=3.7', 
    url="https://github.com/mptcp-apps/mptcplib"
)