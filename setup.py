from setuptools import setup
# can also do this with .toml files
setup(
    name='cli-finance-tracker',
    version='0.0.0',
    description='Keep records of your finance',
    author='Edmond Chu',
    author_email='edmondchu10@hotmail.com',
    packages=['src'],
    entry_points={
        'console_scripts': ['finance-tracker=src.finance_tracker:main']
    },
    install_requires=[
        'tabulate'
    ]
)

