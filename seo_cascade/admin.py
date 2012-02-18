from django.contrib import admin
from models import SEOPageOverride, SEOModelDefault

class SEOPageOverrideAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('path',)
		}),
		('Meta Content', {
			'fields': ('title', 'description', 'image',)
			}),
		('Sitemap', {
			'fields': ('omit', )
		}),
		('Advanced', {
			'classes': ('collapse closed',),
			'fields': ('meta',)
			}),
	)

class SEOModelDefaultAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('model', 'omit', 'changefreq', )
		}),
	)

admin.site.register(SEOModelDefault, SEOModelDefaultAdmin)
admin.site.register(SEOPageOverride, SEOPageOverrideAdmin)
