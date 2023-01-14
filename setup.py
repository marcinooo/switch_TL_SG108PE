import os
from setuptools import find_packages, setup


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError('Unable to find version string.')


setup(
    name='switch_TL_SG108PE',
    version=get_version('src/switch_TL_SG108PE/__init__.py'),
    description='Library to control tp-link switch TL-SG108PE',
    long_description=read('README.rst'),
    author='Marcin Wachacki',
    license='MIT',
    url='https://github.com/marcinooo/switch_TL_SG108PE/tree/main',
    package_dir={'': 'src'},
    packages=find_packages(
        where='src',
        exclude=['tests*'],
    ),
    install_requires=[
        'selenium'
    ],
    py_modules=['switch_TL_SG108PE'],
)
