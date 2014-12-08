import sublime, sublime_plugin
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "PyYAML-3.11"))
import yaml

class TranslatorCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):

		# get new key
		message = "create a new key for this text:"
		sublime.active_window().show_input_panel(message, "", self.on_done, None, None)

	def on_done(self, input):
		try:
			new_key = input
			self.view.run_command("write_to_dict", {"new_key": new_key} )
		except ValueError:
			pass


class writeToDictCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):

		new_key = str(args['new_key'])

		# get selection
		for region in self.view.sel():
			if region.empty():
				sublime.error_message("please select some text")
			else:
				selection = str(self.view.substr(region))
		
		# get path name
		path_name = formatPath(self.view.file_name())

		f = open('/Users/calico//cx/CXROR/config/locales/en.yml')
		lang_file = yaml.safe_load(f)			

		placeholder = lang_file
		for index in range(len(path_name)):
			path_name[index] = str(path_name[index])
			if path_name[index] in placeholder.keys():
				placeholder = placeholder[path_name[index]]
			else:
				placeholder[path_name[index]] = {}
				placeholder = placeholder[path_name[index]]
		placeholder[new_key] = selection

		stream = file('/Users/calico//cx/CXROR/config/locales/en.yml', 'w')
		yaml.dump(lang_file, stream)

		f.close()

		#replace selection with translation key

		#for handlebars
		if "templates" in path_name:
			mustache = "{{ t '"
			for p in path_name[1:]:
				mustache = mustache + p + "."
			mustache = mustache + new_key + "' }}"

		#for rails view
		if "app" in path_name and "views" in path_name:
			mustache = "<%= \"#{t '"
			for p in path_name[1:]:
				mustache = mustache + p + "."
			mustache = mustache + new_key + "' }\" %>"

		for region in self.view.sel():
			if not region.empty():
				self.view.replace(edit, region, mustache)


def formatPath(path):
	# this assumes the path will be 'Users/someone/something/CXROR/app/blah/blah/blah'
	p = path.partition('CXROR')[2]
	p = p.split('/')[1:]
	p.insert(0, unicode('en'))
	p[-1] = p[-1].partition('.')[0]
	return p