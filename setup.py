
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import namesimilarity

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(
    name="NameSimilarity",
    version=namesimilarity.__version__,
    author="Oleg Bagretsov",
    author_email="kamagan@yandex.ru",
    url="hhttps://github.com/kamagan/namesimilarity",
    # tests_require=["pytest"],
    py_modules=["namesimilarity"],
    # packages=['namesimilarity'],
    description="NameSimilarity",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="GPLv3",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    # python_requires=">=3.4",
)
