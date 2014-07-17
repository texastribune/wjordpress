from setuptools import setup

setup(
    name='wjordpress',
    version='0.1.0',
    author='Chris Chang',
    author_email='cchang@texastribune.org',
    url='https://github.com/texastribune/wjordpress',
    packages=['wjordpress'],
    include_package_data=True,  # automatically include things from MANIFEST.in
    license='Apache License, Version 2.0',
    description='Django integration with WordPress through the json-rest-api plugin',
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
    ],
)
