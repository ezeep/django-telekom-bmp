import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def read_that_file(path):
    with open(path) as open_file:
        return open_file.read()

long_description = '\n'.join((read_that_file('README.rst'),
                              read_that_file('LICENSE.txt')))

version = '0.0.1'


setup(name='django-telekom-bmp',
      version=version,
      description='',
      author='Jose A. Martin',
      author_email='jose.sanchez@ezeep.com',
      url='https://github.com/ezeep/django-telekom-bmp',
      license='Apache Software License',
      packages=['telekom_bmp'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'python-social-auth',
          'django-extensions'
          'minidom',
          'flufl.enum',
      ],
      tests_require=[
          'pytest',
          'pytest-cov',
          'coveralls',
      ],
      cmdclass={'test': PyTest},
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
      ]
      )
