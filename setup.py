#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# License: MIT
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

__author__ = "Guillaume Luchet <guillaume@geelweb.org>"
__version__ = "0.1"

import os, sys
from setuptools import setup, find_packages

author_data = __author__.split(" ")
maintainer = " ".join(author_data[0:-1])
maintainer_email = author_data[-1]
README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

if __name__ == "__main__":
    setup(
        name="django ratings with comments",
        version=__version__,
        description="Basic app to use django-ratings adding comments and with stars",
        long_description=README,
        author=maintainer,
        author_email=maintainer_email,
        maintainer=maintainer,
        maintainer_email=maintainer_email,
        url="https://github.com/geelweb/django-ratings-with-comments",
        download_url="https://github.com/geelweb/django-ratings-with-comments/tarball/master",
        license='MIT',
        namespace_packages = ['geelweb', 'geelweb.django'],
        packages=find_packages('src'),
        package_dir = {'':'src'},
        package_data = {
            'geelweb.django.ratings': [
                'templates/ratings/*.html',
                'static/star-rating/*.*'
                ],
        },
        keywords = ['django', 'form', 'rating', 'comment'],
        )


