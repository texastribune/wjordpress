exit("NOPE!")

from setuptools import setup

setup(
    name='wjordpress',
    version='0.1.0',
    author='',
    author_email='c@crccheck.com',
    url='',
    packages=['wjordpress'],
    include_package_data=True,  # automatically include things from MANIFEST.in
    license='Apache License, Version 2.0',
    description='',
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
    ],
)
