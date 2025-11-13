from setuptools import setup, find_packages

requires = [
    'pyramid',
    'waitress',
]

tests_require = [
    'pytest',
    'pytest-cov',
    'webtest',
]

setup(
    name='myapp',
    packages=find_packages(),
    install_requires=requires,
    extras_require={
        'testing': tests_require,
    },
    entry_points={
        'paste.app_factory': [
            'main = myapp:main',
        ],
    },
)