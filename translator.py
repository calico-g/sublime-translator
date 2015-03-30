import sublime, sublime_plugin
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "PyYAML-3.11"))
import yaml
import re

class TranslatorCommand(sublime_plugin.TextCommand):
  def __init__(self, view):
    self.view = view
    self.selection = ''

  def run(self, edit, **args):
    # get selection
    for region in self.view.sel():
      if region.empty():
        sublime.error_message("please select some text")
      else:
        self.selection = str(self.view.substr(region))
        suggested_key = re.sub(r'([^\s\w]|_)+', '', self.selection)

    # get new key
    message = "create a new key for this text:"
    sublime.active_window().show_input_panel(message, suggested_key, self.on_done, None, None)

  def on_done(self, input):
    try:
      new_key = input
      self.view.run_command("write_to_dict", {"new_key": new_key, "selection": self.selection} )
    except ValueError:
      pass

class writeToDictCommand(sublime_plugin.TextCommand):
  def run(self, edit, **args):

    new_key = str(args['new_key'])
    selection = str(args['selection'])
    
    # if a human has added a % to the key, treat this as text within a rails tag
    in_rails_tag = False
    selection, new_key, in_rails_tag = checkRailsTag(selection, new_key, in_rails_tag)
    
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

    #decide if rails or js
    if ".rb" in self.view.file_name() or "html.erb" in self.view.file_name():
      print "It's rails!!!"
      key = createRailsKey(in_rails_tag, new_key)

    elif ".js" in self.view.file_name() or "jst.hbs" in self.view.file_name():
      print "It's javascript!!!"
      key = createJsKey(new_key)

    else:
      print "It's something neither rails nor js, neither beast nor burden, neither fish nor fry"

    # replaces original text with translation key
    for region in self.view.sel():
      if not region.empty():
        self.view.replace(edit, region, key)


def createRailsKey(in_rails_tag, new_key):
  #for RAILS VIEW
  # long version
  # if "app" in path_name and "views" in path_name:
  #   mustache = "<%= t \""
  #   for p in path_name[1:]:
  #     mustache = mustache + p + "."
  #   mustache = mustache + new_key + "\" %>"

  # short version, uses a in-app helper
  if in_rails_tag:
    mustache = "translate('" + new_key + "')"
  else:
    mustache = "<%= translate('" + new_key + "') %>"
  return mustache

def createJsKey(new_key):
  # for HANDLEBARS
  # this makes the long version, which sucks to read
  # if "templates" in path_name:
  #   mustache = "{{ t '"
  #   for p in path_name[1:]:
  #     mustache = mustache + p + "."
  #   mustache = mustache + new_key + "' }}"

  #this makes the short version, which is preprocessed into the uglier version on the fly
  mustache = "$translate('" + new_key + "')$"
  return mustache

def checkRailsTag(selection, new_key, in_rails_tag):
  if new_key[-1] == "%":
    in_rails_tag = True
    new_key = new_key.strip("%")
    selection = selection.strip("'")
    selection = selection.strip('"')
  return selection, new_key, in_rails_tag

def formatPath(path):
  # this assumes the path will be 'Users/someone/something/CXROR/app/blah/blah/blah'
  p = path.partition('CXROR')[2]
  p = p.split('/')[1:]
  p.insert(0, 'en')
  p[-1] = p[-1].partition('.')[0]
  return p
