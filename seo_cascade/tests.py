"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.template import Template
from django.test.client import Client
import logging

from ticketing.models import Location

logger = logging.getLogger(__name__)

class MetaTagsTestCase(TestCase):
	#for quick tests
	def _pre_setup(self):
		pass

	def setUp(self):
		self.t1 = Template("\n\
			{% load meta %}\n\
			{% meta %}\n\
				<title>{% block pagetitle %}Blue Man Group{% endblock %}</title>\n\
				<meta name='description' content='' />\n\
				<meta name='author' content='xxx' />\n\
			{% endmeta %}")

		self.t2 = Template("\n\
			{% extends t1 %}\n\
			{% load meta %}\n\
			{% meta %}\n\
				<meta name='test' content='lol' />\n\
				<meta name='author' content='yyy' />\n\
			{% endmeta %}")

	def test_view_for_meta(self):

		l = Location.objects.get(slug='las-vegas')
		c = Client()
		response = c.head(l.get_absolute_url())

		print "@-->response %r" % dir(response)

		print "@-->location %r" % l.get_absolute_url()

		print "@-->context %r" % response.request.get('PATH_INFO')
		#print "@-->request %r" % response.context.get('request')
		request = response.context.get('request')
		print "@-->path %r" % request.get_full_path()

		self.assertEqual(1, 0)
