from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='bug-fix-py',
    version='5.0.0',
    description='SCW automated bug fixing program',
    long_description=readme,
    author='Matt Proctor',
    author_email='mproctor@securecodewarrior.com',
    url='https://github.com/proctorinc/bug-fix-py',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
    # install_requires=[
    #   'GitPython==3.1.27',
    #   'python-dotenv==0.20.0'
    # ],
    # entry_points={"console_scripts": ["bugfix=bugfix.__main__:main"]},
)