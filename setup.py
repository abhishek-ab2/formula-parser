from setuptools import find_packages, setup

setup(
        name="formula_parser",
        version='1.0.3',
        packages=find_packages(include=['formula_parser', 'formula_parser.*']),
        install_requires=[
            'ordered-set==4.1.0',
            ],
        setup_requires=[
            'setuptools>=75.8.0',
            ],
        zip_safe=False,
        )
