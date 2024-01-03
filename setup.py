from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        'fileunlocker',
        ['src/fileunlocker.cpp'],
        define_macros=[('UNICODE', '1')],
    ),
]

setup(
    name='fileunlocker',
    version='0.1.0',
    author='Author Name',
    description='Python bindings for file unlocker functionality using pybind11',
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)