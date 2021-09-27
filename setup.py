from setuptools import setup

setup(
    name='InCollege',
    version='0.1.0',
    author='Robert Andion, Dana Aljirudi, Daniel Arvelo Concepcion, Nathaniel Aldino, Saif Alkaabi',
    author_email='randion@usf.edu',
    packages=['src'],
    scripts=[],
    url='https://github.com/RobertAndion/InCollege',
    license='LICENSE.md',
    description='Main application package',
    long_description=open('README.md').read(),
    install_requires=[
         "pytest",
         "mock"
    ],
)
