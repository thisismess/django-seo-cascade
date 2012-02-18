import re
from django.core.exceptions import MiddlewareNotUsed
from django.contrib.sitemaps import GenericSitemap
from django.db import models
from django.core import urlresolvers
from django.conf.urls.defaults import url
from django.db.models.signals import post_save

from models import SEOModelDefault, SEOPageOverride
from util import first_of

class SEOMiddleware(object):
	def __init__(self):
		detach_signals()
		generate_sitemap()
		attach_signals()
		raise MiddlewareNotUsed('Sitemap generation complete.')

def detach_signals():
	print "@-->detaching signals"
	valid_models = filter(lambda m: hasattr(m, 'get_absolute_url'), models.get_models())
	valid_models.append(SEOModelDefault)
	valid_models.append(SEOPageOverride)
	[post_save.disconnect(update_sitemap, sender=m) for m in valid_models]

def attach_signals():
	print "@-->attaching signals"
	valid_models = filter(lambda m: hasattr(m, 'get_absolute_url'), models.get_models())
	valid_models.append(SEOModelDefault)
	valid_models.append(SEOPageOverride)

	for m in valid_models:
		model_str = "%s.%s" % (m.__module__, m.__name__)
		if first_of(SEOModelDefault.objects.filter(model=model_str).filter(omit=True)):
			continue
		post_save.connect(update_sitemap, sender=m)


# for signals
def update_sitemap(sender, **kwargs):
	print "@--->updating sitemap"
	generate_sitemap()


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
		changefreq = "weekly"

		if defaults:
			if defaults.omit:
				continue

			if defaults.priority:
				priority = defaults.priority

			if defaults.changefreq:
				changefreq = defaults.changefreq

		allowed_items = model.objects.all()

		# remove items that match omission regexes
		for omission in all_omissions:
			rx = re.compile('^%s$' % omission)
			allowed_items = map(lambda i: i.pk, filter(lambda x: not rx.match(x.get_absolute_url()), allowed_items))

		queryset = model.objects.filter(pk__in=allowed_items)

		info_dict = {
			'queryset': queryset
		}

		sitemaps[model_str] = GenericSitemap(info_dict, priority=priority, changefreq=changefreq)

	resolver = urlresolvers.get_resolver(None)

	# clear previous sitemap.xml entries
	current_map = filter(lambda y: y.regex.pattern == '^sitemap\\.xml$', resolver.url_patterns)
	map(lambda x: resolver.url_patterns.remove(x), current_map)

	# append our new sitemap
	resolver.url_patterns.append(url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name="seo-cascade-sitemap"))
