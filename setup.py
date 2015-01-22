from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='montepetro',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.3',

    description='Probabilistic Reserve Estimates in Python',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/LukasMosser/MontePetro',
    download_url = 'https://github.com/LukasMosser/MontePetro/tarball/0.3',
    # Author details
    author='Lukas Mosser',
    author_email='lukas.mosser@gmail.com',

    # Choose your license
    license='GPL',

    # What does your project relate to?
    keywords=['montecarlo', 'probabilistic', 'oil', 'gas'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['numpy', 'scipy', 'matplotlib'],

    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require = {
        'dev': ['check-manifest'],
        'test': ['coverage', 'nose'],
                     }
)