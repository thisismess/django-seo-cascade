import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
		name                 = "django-seo-cascade",
		version              = "0.5",
		include_package_data = True,
		packages             = find_packages(),
		author               = "Lynn Dylan Hurley, Jack Shedd",
		author_email         = "lynn.dylan.hurley@gmail.com",
		description          = "Django SEO manager. Automatic sitemap generation, cascading meta tag blocks, and overrides via the django admin.",
		url                  = "https://github.com/thisismess/django-seo-cascade",
		install_requires     = ['Django>=1.3.1', 'lxml>=2.3.3', 'ez_setup']
)
