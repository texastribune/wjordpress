from setuptools import setup

setup(
    name='wjordpress',
    # when bumping versions, also update __init__ and changelog
    version='0.2.0',
    author='Chris Chang',
    author_email='cchang@texastribune.org',
    url='https://github.com/texastribune/wjordpress',
    packages=['wjordpress'],
    include_package_data=True,  # automatically include things from MANIFEST.in
    license='Apache License, Version 2.0',
    description='Django integration with WordPress through the json-rest-api plugin',
    long_description=open('README.rst').read(),
    install_requires=[
        'six>=1.0.0',  # works in tox
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
