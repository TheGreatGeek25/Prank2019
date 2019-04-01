from setuptools import setup

setup(
    name='PlainEnglishMarkupLanguage',
    version='1.0.0',
    packages=['plainenglishmarkuplanguage'],
    package_dir={'': 'src'},
    package_data={
        '': ['LICENSE']
    },
    entry_points={
        'console_scripts': [
            'plainenglishmarkuplanguage = plainenglishmarkuplanguage.__init__:main'
        ]
    },

    license='Apache-2.0'
)
