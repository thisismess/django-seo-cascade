import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
		name                 = "django-seo-cascade",
		version              = "0.2",
		packages             = find_packages(),
		author               = "Lynn Dylan Hurley, Jack Shedd",
		author_email         = "lynn.dylan.hurley@gmail.com",
		description          = "Easy SEO management. Automatic sitemap + easy meta management.",
		url                  = "https://github.com/thisismess/django-seo-cascade",
		include_package_data = True,
		install_requires     = ['Django>=1.3.1', 'lxml>=2.3.3', 'ez_setup']
)
