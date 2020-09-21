from __future__ import print_function

from setuptools import setup, find_packages


__version__ = '0.0.1'
name = 'restaurant_simulation'


def read_long_description(filename="README.md"):
    with open(filename) as f:
        return f.read().strip()


setup(
    name=name,
    version=__version__,
    author='xfrnk2',
    author_email='xfrnk2@gmail.com',
    url='https://github.com/xfrnk2/restaurant_simulation',
    description='1 day 1 coding',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    package_data={
        name: [
        ],
    },
    license='MIT',
    keywords='1 day 1 coding',
    long_description=read_long_description(),
    install_requires=[
            'expects',
            'coveralls',
            'coverage',
            'pytest',
            'pytest-bdd',
            'pytest-runner',
            'pytest-cov',
            'py',                
            'flake8',
            'pyflakes',
            'pep8',
    ],
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8.1',
    ],
    test_suite='tests',
    extras_require={
        'tests': [
        ],
    }
)