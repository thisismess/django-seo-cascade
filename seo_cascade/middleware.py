import re
from django.core.exceptions import MiddlewareNotUsed
from django.contrib.sitemaps import GenericSitemap
from django.db import models
from django.core import urlresolvers
from django.conf.urls.defaults import url

from models import SEOModelDefault, SEOPageOverride
from util import first_of

class SEOMiddleware(object):
	def __init__(self):
		generate_sitemap()
		raise MiddlewareNotUsed('Sitemap generation complete.')

def generate_sitemap():
	valid_models = filter(lambda m: hasattr(m, 'get_absolute_url'), models.get_models())
	all_overrides = SEOPageOverride.objects.all()
	all_omissions = map(lambda x: x.path, all_overrides.filter(omit=True))

	sitemaps = {}

	for model in valid_models:
		model_str = "%s.%s" % (model.__module__, model.__name__)
		defaults = first_of(SEOModelDefault.objects.filter(model=model_str))
		# TODO: make this a setting
		priority = .5

		if defaults:
			if defaults.omit:
				continue

			if defaults.priority:
				priority = defaults.priority

		allowed_items = model.objects.all()

		# remove items that match omission regexes
		for omission in all_omissions:
			rx = re.compile('^%s$' % omission)
			allowed_items = map(lambda i: i.pk, filter(lambda x: not rx.match(x.get_absolute_url()), allowed_items))

		queryset = model.objects.filter(pk__in=allowed_items)

		info_dict = {
			'queryset': queryset
		}

		sitemaps[model_str] = GenericSitemap(info_dict, priority=priority)

	resolver = urlresolvers.get_resolver(None)
	resolver.url_patterns.append(url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}))
