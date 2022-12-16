from distutils.core import setup, Extension
from pathlib import Path

linux_modules = Extension("mptcplib._mptcplib_linux", 
                    include_dirs=["mptcplib/include"],
                    sources=["mptcplib/src/_mptcplib_linux.c"]
                )

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mptcplib", 
    version="0.1.2", 
    description="A Multipath TCP python support library",
    ext_modules=[linux_modules],
    packages=['mptcplib'],
    package_data={
        "mptcplib": ["py.typed", "*.pyi", "**/*.pyi"]
    },
    long_description_content_type='text/markdown',
    long_description=long_description,
    platforms=["Linux"], 
    python_requires='>=3.7', 
    url="https://github.com/mptcp-apps/mptcplib"
)