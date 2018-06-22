import re
import ast
from setuptools import setup, find_packages


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('healthchecker/__init__.py', 'rb') as f:
    __version__ = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='healthchecker',
    version=__version__,
    description='Utility for handling nlb healthchecks',
    long_description=open('README.md', 'r').read(),
    maintainer='RhoAI',
    license='',
    url='',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'healthcheck=healthchecker.checker:main'
        ]
    },
    install_requires=[
        'gevent==1.2.2'
    ],
    extras_require={
        'dev': [
            'honcho==0.5.0'
        ],
    }
)
