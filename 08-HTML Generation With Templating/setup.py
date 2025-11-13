from setuptools import setup, find_packages

requires = [
    'pyramid',
    'pyramid_chameleon',
    'waitress',
]

setup(
    name='myapp',
    packages=find_packages(),
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = myapp:main',
        ],
    },
)