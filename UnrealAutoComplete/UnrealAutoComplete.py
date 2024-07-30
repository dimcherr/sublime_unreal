# -*- encoding: utf-8 -*-
import os
import re
import json
import sublime
import sublime_plugin

class UnrealAutoCompleteListener(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        pass