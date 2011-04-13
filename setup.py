import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

requires = [
    'pyramid',
    'sqlalchemy',
    'zope.sqlalchemy',
    'WebError',
    "formencode",
    "tw2.jit>=0.2.8b26",
    "tw2.jqplugins.ui",
    "kitchen",
    "docutils",
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='leafymiracle',
      version='0.0',
      description='leafymiracle',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Luke Macken',
      author_email='lmacken@redhat.com',
      url='',
      license='AGPLv3+',
      keywords='fedora web pyramid jit tw2',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require = requires,
      test_suite="leafymiracle",
      entry_points = """\
      [paste.app_factory]
      main = leafymiracle:main
      """,
      paster_plugins=['pyramid'],
      )

