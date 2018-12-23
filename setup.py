import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='algotrader',
    version=open("algotrader/_version.py").readlines()[-1].split()[-1].strip("\"'"),
    packages=['algotrader'],
    python_requires='>=3.5.2',
    install_requires=required,
    include_package_data=True,
    license='BSD License',
    description='Algorithmic trader.',
    long_description=README,
    url='https://github.com/muraty/algotrader',
    author='Omer Murat Yildirim',
    author_email='omermuratyildirim@gmail.com',
    entry_points={
        'console_scripts': [
            'algotrader = algotrader.cli:main',
        ]
    }
)
