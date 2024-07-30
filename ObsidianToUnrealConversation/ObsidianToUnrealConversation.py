# -*- encoding: utf-8 -*-
import os
import re
import json
import sublime
import sublime_plugin

canvas_path = "C:\\Users\\Dimka\\Desktop\\MainVault\\MainVault\\MyDear Conversation Tree.canvas"
target_path = "C:\\Users\\Dimka\\Desktop\\dev\\MyDearProject\\gitrep\\MyDear\\RawAssets\\Conversations\\Conversations.json" 
template_path = os.path.join(sublime.packages_path(), "ObsidianToUnrealConversation", "ConversationsTemplate.json")

class ConvertConversationCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("convert conversation")
        f = open(canvas_path, 'r', encoding="utf-8")
        canvas = json.load(f) 
        ff = open(template_path, 'r', encoding="utf-8")
        template = ff.read() 

        nodes = {}
        for node in canvas["nodes"]:
            speaker_name = node["text"].split(" to ")[0]
            other_speaker_name = node["text"].split(" to ")[1].split(" > ")[0]
            cue_text = node["text"].split(" > ")[1]
            nodes[node["id"]] = { 
                "conversation_id": node["id"],
                "speaker_name": speaker_name,
                "other_speaker_name": other_speaker_name,
                "cue_text": cue_text,
                "summary_text": cue_text,
                "possible_next_cues": "",
                "cues_list": []
                }

        for edge in canvas["edges"]:
            nodes[edge["fromNode"]]["cues_list"].append("\"{cue}\"".format(cue=edge["toNode"]))

        print(nodes)

        templates = []
        for node_id in nodes:
            if len(nodes[node_id]["cues_list"]) > 0:
                nodes[node_id]["possible_next_cues"] = ",".join(nodes[node_id]["cues_list"])
            templates.append(template.format(**nodes[node_id]))

        result = "[\n{temp}\n]".format(temp=",\n".join(templates))

        print(result)

        fff = open(target_path, 'w', encoding="utf-8")
        fff.write(result)