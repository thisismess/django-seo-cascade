from django import template
from django.template import VariableNode, FilterExpression, Parser
from django.template.base import TemplateSyntaxError, StringOrigin, UNKNOWN_SOURCE
from django.template.loader_tags import BlockNode, BLOCK_CONTEXT_KEY
from django.utils.safestring import mark_safe

from lxml import etree

from ..util import unique_by, first_of
from ..models import SEOPageOverride

register = template.Library()

class MetaNode(BlockNode):
	def __init__(self, nodelist, parent=None):
		# prepend {{ block.super }} to meta tag
		p = Parser('')
		t = 'block.super'
		fe = FilterExpression(t, p)
		vn = VariableNode(fe)
		# i don't even know
		vn.source = (StringOrigin(UNKNOWN_SOURCE), ('a',{} ))
		nodelist.insert(0, vn)

		# build block tag with block name "meta"
		super(MetaNode, self).__init__("meta-cascade", nodelist, parent)

	def render(self, context):
		raw = super(MetaNode, self).render(context)

		request = context.get('request')
		path = request.get_full_path()

		admin_path_override = first_of(SEOPageOverride.objects.filter(path=path))

		if admin_path_override:
			raw += admin_path_override.title_tags
			raw += admin_path_override.description_tags
			raw += admin_path_override.image_tags
			raw += admin_path_override.meta

		root = etree.XML('<root>%s</root>' % raw)
		children = root.getchildren()
		children.reverse()
		children = unique_by(children, lambda x: [x.tag, x.get('name'), x.get('property')])
		children.reverse()

		if len(children):
			ret = reduce(lambda x, y: x+y, map(lambda z: (etree.tostring(z)), children))
		else:
			ret = ""

		return ret

	def super(self):
		if not hasattr(self, 'context'):
			return ''
		render_context = self.context.render_context
		if (BLOCK_CONTEXT_KEY in render_context and
				render_context[BLOCK_CONTEXT_KEY].get_block(self.name) is not None):
				return mark_safe(self.render(self.context))
		return ''


def do_meta(parser, token):
	"""
	Define a meta block that can be overridden by child templates.
	"""
	bits = token.contents.split()
	if len(bits) != 1:
		raise TemplateSyntaxError("'%s' tag takes no arguments" % bits[0])
	block_name = bits[0]
	# Keep track of the names of MetaNodes found in this template, so we can
	# check for duplication.
	try:
		if block_name in parser.__loaded_blocks:
			raise TemplateSyntaxError("'%s' tag appears more than once" % bits[0])
		parser.__loaded_blocks.append(block_name)
	except AttributeError: # parser.__loaded_blocks isn't a list yet
		parser.__loaded_blocks = [block_name]
	nodelist = parser.parse(('endmeta', 'endmeta %s' % block_name))

	parser.delete_first_token()
	return MetaNode(nodelist)


register.tag('meta', do_meta)
