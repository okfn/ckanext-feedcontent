from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-feedcontent',
	version=version,
	description="Content for the templates from Atom/RSS feeds",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Open Knowledge Foundation',
	author_email='info@okfn.org',
	url='http://okfn.org',
	license='GPL',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.feedcontent'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
		'feedparser==5.1.2'
	],
	entry_points=\
	"""
    [ckan.plugins]
	feed_content = ckanext.feedcontent.plugin:FeedContent
	""",
)