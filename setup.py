import os
from setuptools import setup


setup(
    name='algotrader',
    version=0.1,  # TODO: Make variable
    packages=['algotrader'],
    python_requires='>=3.5.2',
    install_requires=[
        'requests>=2',
        'Flask>=0.12',
        'psutil>=2',
        'terminaltables>=3',
        'mysql-connector>=2.1,<2.2',
        'waitress>=1',
    ],
    include_package_data=True,
    license='BSD License',
    description='algotrader',
    long_description='algotrader',
    author='Omer Murat Yildirim',
    author_email='omermuratyildirim@gmail.com',
    entry_points={
        'console_scripts': [
            'consumer = kimo.consumer:main',
            'checker = kimo.checker:main',
        ]
    }
)