#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

readme = """
JSONLang is a programming language written in JSON format.
"""


requirements = [
]

test_requirements = [
    'pytest==2.9.1',
]

setup(
    name='jsonlang',
    version='0.1.1',
    description="JSONLang Python Implement.",
    long_description=readme,
    author="Ju Lin",
    author_email='soasme@gmail.com',
    url='https://github.com/soasme/jsonlang',
    packages=find_packages(exclude=('tests', 'tests.*', '*.tests', '*.tests.*', )),
    py_modules=['jsonlang'],
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='jsonlang',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'jsonlang= jsonlang:eval_jsonlang'
        ]
    },
)
