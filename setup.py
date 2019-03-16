from setuptools import setup

setup(
    name='COBOML',
    version='1.0.0',
    packages=['coboml'],
    package_dir={'': 'src'},
    package_data={
        '': ['LICENSE']
    },
    entry_points={
        'console_scripts': [
            'coboml = coboml.__init__:main'
        ]
    },

    license='Apache-2.0'
)
