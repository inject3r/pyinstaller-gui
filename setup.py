from io import open
from setuptools import setup
from pyinstaller_gui import __version__ as version

setup(
    name="PyInstaller GUI",
    version=version,
    url="https://github.com/inject3r/pyinstaller-gui",
    license="MIT",
    author="Abolfazl Hosseini",
    author_email="tryuzr@gmail.com",
    description="A powerful GUI wrapper for PyInstaller — convert your Python scripts into standalone executables for Windows, macOS, and Linux with ease.",
    long_description="".join(open("README.md", encoding="utf-8").readlines()),
    long_description_content_type="text/markdown",
    project_urls={
        "Source Code": "https://github.com/inject3r/pyinstaller-gui",
        "Bug Tracker": "https://github.com/inject3r/pyinstaller-gui/issues",
    },
    keywords = ["gui", "executable", "pyinstaller", "python", "converter", "cross-platform", "windows", "macos", "linux", "build tool", "script to exe", "python packaging", "application builder", "standalone app", "no coding", "desktop app", "code bundler"],
    packages=["pyinstaller_gui"],
    include_package_data=True,
    install_requires=["PyQt6>=6.8.1", "PyInstaller>=6.11.1"],
    python_requires=">=3.6",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["pyinstaller-gui=pyinstaller_gui.__main__:run", "pyinstallergui=pyinstaller_gui.__main__:run"],
    },
)