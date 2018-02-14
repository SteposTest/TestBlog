from setuptools import setup
from os.path import join, dirname

setup(
    name='test_blog',
    install_requires=[
        'Django<1.11',
        'jsonfield < 2.1',
        'wrapt < 1.11',
    ],
    version='1.0',
    author='Stepos',
    author_email='s.poshibaylov@gmail.com',
    description='This is a simple blog.',
    long_description=open(join(dirname(__file__), 'README.md')).read()
)
