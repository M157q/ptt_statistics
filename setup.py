#!/usr/bin/env python3

from setuptools import find_packages, setup


try:
    import ptt_crawler
except ImportError:
    errmsg = [
        "Cannot find module 'ptt_crawler'",
        "Use the following command to install",
        "`pip3 install git+https://github.com/M157q/ptt-crawler`",
    ]
    l = max(map(len, errmsg))
    print('')
    print('='*l)
    print('\n'.join(errmsg))
    print('='*l)
    print('')
    raise

setup(
    packages=find_packages(exclude=['ptt_statistics.bin']),
    scripts=['ptt_statistics/bin/ptt_statistics'],
    install_requires=['pony'],
    name='ptt_statistics',
    version='0.0.1',
    author='Shun-Yi Jheng',
    author_email='M157q.tw@gmail.com',
    url="https://github.com/M157q/ptt-statistics",
    keywords="ptt, statistics",
    description="Get the statistics info of one ptt board.",
    platforms=['Linux'],
    license='GPLv3',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ],
)
