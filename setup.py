try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from crediweb.version import __version__

setup(
    name='crediweb',
    version=__version__,
    author='Agris Ameriks',
    packages=['crediweb'],
    description='CrediWeb parser for Python',
    url='http://github.com/Ameriks/crediweb/',
    install_requires=[
        "requests >= 1.2.3",
        "beautifulsoup4 >= 4.2.1",
        "vatnumber >= 1.1",
        "suds >= 0.4",
        "html5lib >= 1.0b2",
    ],
)