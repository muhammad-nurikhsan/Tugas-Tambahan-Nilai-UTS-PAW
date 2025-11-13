from setuptools import setup, find_packages

setup(
    name='myapp',
    packages=find_packages(),
    install_requires=[
        'pyramid',
        'SQLAlchemy',
        'waitress',
    ],
    entry_points={
        'paste.app_factory': ['main = myapp:main'],
    },
)