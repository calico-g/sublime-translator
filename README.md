Important things!!!!

* Right now this only works for sublime text2

* translator.py needs to live in a folder called Translator, inside sublime's Packages. Something like this:
/Users/calico/Library/Application Support/Sublime Text 2/Packages/Translator

* the file which is being written to is hard-coded as '/Users/calico//cx/CXROR/config/locales/en.yml', needs to be changed to whatever the local language file is. This file needs to have at least "en: {}" on the first line for it to grab onto.

* you may also need to install AAAPackageDev packages in sublime. 

to use:

1. go to the file you want to translate
2. select the text
3. hit control+~ to open the sublime console
4. type "view.run_command('translator')"
5. it should prompt you for a key for that text in the language file. make up a good one, type it and hit enter.
6. Profit.

You can assign this plugin a keyboard shortcut, but I forget how. you can look it up. :)
