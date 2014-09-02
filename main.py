template = "<abc>{{ def.abc }}</abc>"
conf = {'abc': 42, 'def': {'abc': True}}

import re

class Template(object):
	def __init__(self, template, conf):
		self.lsep = '{{'
		self.rsep = '}}'
		self.template = template
		self.conf = conf
		self.pos = 0

	def render(self):
		output = []
		while True:
			try:
				tag = self.getNextTag()
			except:
				break
			else:
				output.append(self.template[:tag['start']])
				tag_content = self.execute(tag['tokens'])
				output.append(tag_content)
		output.append(self.template[self.pos:])
		return ''.join(output)

	def execute(self, tokens):
		if len(tokens) == 1:
			path = tokens[0]
			return str(self.find_path(path, self.conf))

	def find_path(self, path, conf):
		if path.find('.') == -1:
			return conf[path]
		first, rest = path.split('.', 1)
		return self.find_path(rest, conf[first])


	def getNextTag(self):
		start_tag = self.template.find(self.lsep, self.pos)
		if start_tag == -1:
			raise Exception
		end_tag = self.template.find(self.rsep, start_tag)
		self.pos = end_tag + len(self.rsep)
		content = self.template[start_tag + len(self.lsep) : end_tag]
		tokens = content.strip().split(' ')
		return {'start': start_tag, 'end': end_tag, 'tokens': tokens}


aaa = Template(template, conf)
print aaa.render()