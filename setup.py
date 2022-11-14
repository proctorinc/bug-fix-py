from distutils.core import setup

setup(name='bugfixpy',
      version='1.0.0',
      description='SCW automated bug fix program',
      author='Matt Proctor',
      author_email='matthewalanproctor@gmail.com',
      packages=['bugfixpy'],
      license="MIT",
      install_requires=[
        'GitPython==3.1.27',
        'python-dotenv==0.20.0'
      ],
      entry_points={"console_scripts": ["bugfix=bugfix.__main__:main"]},
)
