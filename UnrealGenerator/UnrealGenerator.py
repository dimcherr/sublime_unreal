# -*- encoding: utf-8 -*-
import os
import glob
import re
import shutil
import sublime
import sublime_plugin

templates_dir = os.path.join(sublime.packages_path(), "UnrealGenerator", "UnrealGeneratorTemplates")

class UImplementInterfaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view;
        line = view.substr(view.line(view.sel()[0])).strip()
        print(line)
        print(view.substr(view.word(view.sel()[0])).strip())
        interface_file_name = view.substr(view.word(view.sel()[0])).strip()[1:] + ".h"
        interface_file_path = view.file_name().split("\\Public")[0] + "\\Public\\" + interface_file_name
        f = open(interface_file_path, "r")
        pattern = re.compile(r'[\w\s]+\(.*\).*\;', re.MULTILINE)
        interface_functions_raw = [reg for reg in re.findall(pattern, f.read())]
        interface_functions = []
        for func in interface_functions_raw:
            s = func.split("(")
            interface_functions.append(s[0] + "(" + s[1][:-1] + " override;")

        insert_pos = view.find(r'};', view.sel()[0].a).a - 1
        for func in interface_functions:
            view.insert(edit, insert_pos, func)

        print(view.find(r'};', view.sel()[0].a).a - 1)

class UDefineFunctionEventListener(sublime_plugin.EventListener):
    def on_load(self, view):
        global tokens
        if len(tokens) > 0:
            view.window().run_command(
                "u_define_function_internal"
            )

class UDefineFunctionInternalCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global tokens
        view = self.view
        line_count = len(view.lines(sublime.Region(0, view.size())))
        template = '''

{retval} {name}{params}{const}
{{
    
}}'''
        for t in tokens:
            if len(t) < 3:
                continue
            view.insert(edit, view.size(), template.format(retval=t[0], name=t[1], params=t[2], const=(" " + t[3]) if len(t) > 3 else ""))
            view.sel().clear()
            view.sel().add(sublime.Region(view.size() - 2))
            view.show_at_center(view.size() - 2)

        tokens = []

class UDefineFunctionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global tokens
        tokens = []
        view = self.view
        lines = view.substr(view.line(view.sel()[0])).strip()
        print("LINES")
        print(lines)

        # find classname
        all_file_content = view.substr(sublime.Region(0, view.size()))
        beforeline = all_file_content.split(lines)[0]
        afterclass = beforeline.split("class ")
        afterstruct = beforeline.split("struct ")
        classname_withstuff = ""
        if len(afterclass) > 1:
            classname_withstuff = afterclass[1]
        else:
            classname_withstuff = afterstruct[1]

        if "_API" in classname_withstuff:
            classname = re.split(' |\n', classname_withstuff)[1].strip()
        else:
            classname = re.split(' |\n', classname_withstuff)[0].strip()

        for line in lines.split("\n"):
            print("LINE", line)
            t = re.compile(r'[a-zA-Z0-9_&*<>]+|\(.*\)').findall(line.strip())
            print(t)
            t = list(filter(lambda x: x != 'virtual' and x != 'override', t))
            if len(t) < 2:
                continue
            t[1] = classname + "::" + t[1]
            tokens.append(t)

        res_file_path = view.file_name().replace("\\Public\\", "\\Private\\").replace(".h", ".cpp")
        cppview = view.window().open_file(res_file_path)

        if not cppview.is_loading():
            view.window().run_command(
                "u_define_function_internal"
            )

class UCopyEntityCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.window = self.view.window()
        #self.projectname = self.window.folders()[0].replace("\\Source", "").split("\\")[-1]
        self.window.show_input_panel("Entity Name: ", "", self.choose_entity_name, None, None)
    def choose_entity_name(self, entity_name):
        self.entity_name = entity_name
        self.window.show_input_panel("Target Name: ", "", self.choose_target_name, None, None)
    def choose_target_name(self, target_name):
        self.target_name = target_name
        self.sourcepath = self.window.folders()[0]
        for root, dirs, files in os.walk(self.sourcepath):
            for file in files:
                if file.endswith(self.entity_name + ".h") or file.endswith(self.entity_name + ".cpp"):
                    print(root + "\\" + file)
                    f = open(os.path.join(root, file), "r", encoding="utf-8")
                    ff = open(os.path.join(root, file.replace(self.entity_name, self.target_name)), "w", encoding="utf-8")
                    for line in f:
                        ff.write(line.replace(self.entity_name, self.target_name))

class UCreateEntityCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.window = self.view.window()
        self.projectname = self.window.folders()[0].replace("\\Source", "").split("\\")[-1]
        self.sourcepath = self.window.folders()[0]
        self.window.show_input_panel("Entity Type: ", "", self.choose_entity_type, None, None)

    def choose_entity_type(self, entity_type):
        self.entity_type = entity_type
        self.window.show_input_panel('{entity_type} Name: '.format(entity_type=self.entity_type), "", self.create_entity, None, None)

    def create_entity(self, name):
        self.entityname = name
        if self.entity_type == "Component":
            self.entityname = self.entityname + "Component"
        if self.entity_type == "GameMode":
            self.entityname = self.entityname + "GameMode"
        if self.entity_type == "Interface":
            self.entityname = self.entityname + "Interface"
        if self.entity_type == "Widget":
            self.entityname = self.entityname + "Widget"
        if self.entity_type == "PlayerController":
            self.entityname = self.entityname + "PlayerController"
        self.window.show_input_panel("Path: ", "", self.save_entity, None, None)

    def open_entity_file(self, template_file, cppfiletype, path):
        cpp_path = os.path.join(self.sourcepath, self.projectname, cppfiletype, path.replace("/", "\\"))
        template = template_file.read()
        includename = path + "/" + self.entityname if len(path) > 0 else self.entityname
        res = template.format(name=self.entityname, projectname=self.projectname.upper(), includename=includename)
        if not os.path.exists(cpp_path):
            os.makedirs(cpp_path)
        self.window.run_command(
            "open_file",
            {
                "file": os.path.join(cpp_path, self.entityname + (".h" if cppfiletype == "Public" else ".cpp")),
                "contents": res,
            },
        )

    def save_entity(self, path):
        entity_type_lower = self.entity_type.lower()
        with open(os.path.join(templates_dir, '{entity_type_lower}.h'.format(entity_type_lower=entity_type_lower)), 'r') as public_template_file:
            self.open_entity_file(public_template_file, "Public", path)
        with open(os.path.join(templates_dir, '{entity_type_lower}.cpp'.format(entity_type_lower=entity_type_lower)), 'r') as private_template_file:
            self.open_entity_file(private_template_file, "Private", path)