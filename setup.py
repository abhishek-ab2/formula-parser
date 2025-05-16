from Cython.Build import cythonize
from setuptools import setup, Extension

ext_modules = [
    Extension('formula_parser.parser', ['formula_parser/parser.pyx']),
    Extension('formula_parser.utils', ['formula_parser/utils.pyx'])
]

setup(
        name="formula_parser",
        version='1.0.0',
        packages=['formula_parser',],
        ext_modules=cythonize(ext_modules, language_level='3'),
        install_requires=[
            'ordered-set==4.1.0',
            ],
        setup_requires=[
            'Cython==3.0.12',
            'setuptools>=75.8.0',
            ],
        zip_safe=False,
        package_data={
            'formula_parser': ['py.typed']
        }
        )
