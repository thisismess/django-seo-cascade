from django.db import models
from lxml import etree
from django.contrib.sites.models import Site
from django.conf import settings


MODEL_CHOICES = [("%s.%s" % (m.__module__, m.__name__), ("%s.%s" % (m.__module__, m.__name__))) for m in filter(lambda x: hasattr(x, 'get_absolute_url'), models.get_models())]

CHANGEFREQ_CHOICES = [
	('always'  , 'Always')  ,
	('hourly'  , 'Hourly')  ,
	('daily'   , 'Daily')   ,
	('weekly'  , 'Weekly')  ,
	('monthly' , 'Monthly') ,
	('yearly'  , 'Yearly')  ,
	('never'   , 'Never')   ,
]


class SEOBase(models.Model):
	title       = models.CharField(max_length=255, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	meta        = models.TextField("Meta Override HTML", blank=True, null=True)
	omit        = models.BooleanField("Omit from sitemap", default=False)
	changefreq  = models.CharField("Change Frequency", max_length=50, blank=True, null=True, choices=CHANGEFREQ_CHOICES, default='weekly')

	class Meta:
		abstract = True

	@property
	def title_tags(self):
		if not self.title:
			return u""

		tags = []
		title_tag = etree.Element("title")
		title_tag.text = self.title
		tags.append(title_tag)
		tags.append(etree.Element("meta", content=self.title, property="og:title"))
		return u'%s' % reduce(lambda x, y: x+y, map(lambda x: etree.tostring(x, pretty_print=True), tags))

	@property
	def description_tags(self):
		if not self.description:
			return u""

		tags = []
		tags.append(etree.Element("meta", content=self.description, property="description"))
		tags.append(etree.Element("meta", content=self.description, property="og:description"))
		return u"%s" % reduce(lambda x, y: x+y, map(lambda x: etree.tostring(x, pretty_print=True), tags))


class SEOLocation(SEOBase):
	path     = models.CharField("Absolute Path", max_length=255, blank=False, null=False)
	priority = models.DecimalField(max_digits=2, decimal_places=1, default=0.5, null=True, blank=True)

	class Meta:
		ordering = ['path',]
		abstract = False

	def __unicode__(self):
		return u'%s' % self.path


class SEOModelDefault(SEOBase):
	model       = models.CharField(max_length=255, blank=False, unique=True, choices=MODEL_CHOICES)
	priority    = models.DecimalField(max_digits=2, decimal_places=1, default=0.5, null=True, blank=True)

	class Meta:
		ordering = ['model',]
		abstract = False

	def __unicode__(self):
		return u'%s' % self.model


class SEOPageOverride(SEOBase):
	path        = models.CharField("Absolute Path", max_length=255, blank=False, null=False)
	image       = models.ImageField(upload_to="meta", blank=True, null=True)

	class Meta:
		ordering = ['path',]
		abstract = False

	def __unicode__(self):
		return u'%s' % self.path

	@property
	def image_tags(self):
		current_site = Site.objects.get(id=settings.SITE_ID)
		if not self.image:
			return u""

		tags = []
		tags.append(etree.Element("meta", content="http://%s%s" % (current_site.domain, self.image.url), property="og:image"))
		tags.append(etree.Element("meta", content="%r" % self.image.width, property="og:image:width"))
		tags.append(etree.Element("meta", content="%r" % self.image.height, property="og:image:height"))
		return u'%s' % reduce(lambda x, y: x+y, map(lambda x: etree.tostring(x, pretty_print=True), tags))
