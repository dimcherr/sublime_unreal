import sublime
import sublime_plugin

class InsertMySnippetCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.run_command("insert_snippet", { "contents": "void ${1}();" })
