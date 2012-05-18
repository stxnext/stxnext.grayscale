# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

version = open('src/stxnext/grayscale/version.txt').read()

setup (
    name='stxnext.grayscale',
    version=version,
    author='STX Next Sp. z o.o, Radosław Jankiewicz',
    author_email='info@stxnext.pl',
    description='Displays the web pages transformed to grayscale.',
    long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
    keywords='plone grayscale',
    platforms=['any'],
    url='http://www.stxnext.pl/open-source',
    license='Zope Public License, Version 2.1 (ZPL)',
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'':'src'},
    namespace_packages=['stxnext'],
    zip_safe=False,

    install_requires=[
        'setuptools',
       ],

    extras_require={
         'test': [
            'Plone',
            'plone.app.testing',
            ],
        'Zope2.10': ['ZPublisherEventsBackport'],
    },

    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Zope2',
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Programming Language :: Python',
        ]
    )
