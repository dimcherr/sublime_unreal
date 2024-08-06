# -*- encoding: utf-8 -*-
import os
import re
import json
import sublime
import sublime_plugin

color_alias = "2"
color_function = "3"
color_table_path = "C:\\Users\\Dimka\\Desktop\\dev\\MyDearProject\\gitrep\\MyDear\\RawAssets\\Conversations\\CharacterColorTable.json" 
subtitle_dir_path = "C:\\Users\\Dimka\\Desktop\\dev\\MyDearProject\\gitrep\\MyDear\\RawAssets\\Conversations\\Sound"
canvas_path = "C:\\Users\\Dimka\\My Drive\\MainVault\\MainVault\\Conversation\\Galina.canvas"
target_path = "C:\\Users\\Dimka\\Desktop\\dev\\MyDearProject\\gitrep\\MyDear\\RawAssets\\Conversations\\Galina.json" 
test_path = "C:\\Users\\Dimka\\Desktop\\dev\\MyDearProject\\gitrep\\MyDear\\RawAssets\\Conversations\\Test.json"

class ConvertConversationCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        f = open(color_table_path, 'r', encoding="utf-8")
        color_table = json.load(f)
        f.close()

        f = open(canvas_path, 'r', encoding="utf-8")
        canvas = json.load(f) 

        nodes = {}
        alias_map = {}
        cues_set = set()
        functions_set = set()
        main_aliases_set = set() 

        for node in canvas["nodes"]:
            del node["type"]
            del node["y"]
            del node["x"]
            del node["height"]
            del node["width"]
            nodes[node["id"]] = {
                "content": node,
                "next": {},
                "prev": {}
            }
            if "color" not in node:
                if node["text"] not in alias_map:
                    alias_map[node["text"]] = []
                alias_map[node["text"]].append(node["id"])
            elif node["color"] == color_function:
                functions_set.add(node["id"])
            elif node["color"] == color_alias:
                main_aliases_set.add(node["id"])
                if node["text"] not in alias_map:
                    alias_map[node["text"]] = []
                alias_map[node["text"]].append(node["id"])
            else:
                cues_set.add(node["id"])

        for edge in canvas["edges"]:
            a = edge["fromNode"]
            b = edge["toNode"]
            nextnode = {"text": nodes[b]["content"]["text"]}
            if "label" in edge:
                nextnode["condition"] = edge["label"]
            prevnode = {"text": nodes[a]["content"]["text"]}
            if "label" in edge:
                prevnode["condition"] = edge["label"]
            nodes[a]["next"][b] = nextnode
            nodes[b]["prev"][a] = prevnode


        #print(alias_map)

        #for main_alias_id in main_aliases_set:
            #print(nodes[main_alias_id])



        # replacing aliases
        for main_alias_id in main_aliases_set:
            main_alias_text = nodes[main_alias_id]["content"]["text"]
            print(main_alias_text, alias_map[main_alias_text])

            alias_map[main_alias_text] = list(filter(lambda x: x != main_alias_id, alias_map[main_alias_text]))
            alias_map[main_alias_text].append(main_alias_id)

            print("iterating through {a}".format(a=main_alias_text))
            for alias_id in alias_map[main_alias_text]:
                #if alias_id == main_alias_id:
                    #continue
                for prev_node_id in nodes[alias_id]["prev"]:
                    prev_node = nodes[prev_node_id]

                    # remove link to alias node from previous node
                    if alias_id in prev_node["next"]:
                        del prev_node["next"][alias_id]

                    for next_node_id in nodes[main_alias_id]["next"]:
                        next_node = nodes[next_node_id]
                        prev_node["next"][next_node_id] = nodes[main_alias_id]["next"][next_node_id]
                        if main_alias_id in next_node["prev"]:
                            del next_node["prev"][main_alias_id]
                        next_node["prev"][prev_node_id] = nodes[alias_id]["prev"][prev_node_id]
                del nodes[alias_id]

        # replacing functions
        for function_id in functions_set:
            node_text = nodes[function_id]["content"]["text"]
            print(node_text)
            set_function_reg = re.findall(r"^\s*(\w+)\s*=\s*(\d*\.*\d*|\w*)\s*$", node_text, re.M)
            call_function_reg = re.findall(r"^\s*([A-Za-z][A-Za-z0-9]+)$", node_text, re.M)
            narrator_function_reg = re.findall(r"\((.*)\)", node_text, re.M)

            print(set_function_reg)

            node_content = nodes[function_id]["content"]
            if len(set_function_reg) > 0:
                node_content["function_name"] = "Set" + set_function_reg[0][0]
                if set_function_reg[0][1].lower() == "true":
                    node_content["parameter_value"] = "1"
                elif set_function_reg[0][1].lower() == "false":
                    node_content["parameter_value"] = "0"
                else:
                    node_content["parameter_value"] = set_function_reg[0][1]
            elif len(call_function_reg) > 0:
                node_content["function_name"] = call_function_reg[0]
            if len(narrator_function_reg) > 0:
                node_content["text"] = narrator_function_reg[0]
            else:
                node_content["text"] = ""

        with open(test_path, 'w', encoding='utf-8') as f:
            json.dump(nodes, f, indent=4, ensure_ascii=False) 


        head_cue = {}
        cues = []
        for node_id in nodes:
            node = nodes[node_id]

            node_color = node["content"]["color"]
            speaker_type = color_table["ColorsToSpeakerType"][node_color]
            speaker_name = color_table["ColorsToSpeakerName"][node_color]

            summary = node["content"]["text"].split(":::")[0]
            text = node["content"]["text"].replace(":::", "")
            subtitles = []
            try:
                sf = open(subtitle_dir_path + "\\{id}.srt".format(id=node_id), encoding="utf-8")
                sf_lines = sf.readlines() 
                i = 0
                while True:
                    if i+2 >= len(sf_lines):
                        break
                    timestr = sf_lines[i+1]
                    timereg = re.findall(r"\d+", timestr)
                    start_time = int(timereg[0]) * 60 * 60 + int(timereg[1]) * 60 + int(timereg[2]) + int(timereg[3]) / 1000
                    end_time = int(timereg[4]) * 60 * 60 + int(timereg[5]) * 60 + int(timereg[6]) + int(timereg[7]) / 1000
                    textstr = sf_lines[i+2]
                    subtitles.append({
                        "Text": textstr.strip(),
                        "StartTime": start_time,
                        "EndTime": end_time 
                    })
                    i = i + 4
            except:
                pass

            anim_sequence = ""
            sound_wave = ""
            if len(text) > 0:
                if speaker_name != "Narrator":
                    anim_sequence = "/Script/Engine.AnimSequence'/Game/VoiceActing/Animation/{id}.{id}'".format(id=node_id)
                sound_wave = "/Script/Engine.SoundWave'/Game/VoiceActing/Sound/{id}.{id}'".format(id=node_id)

            function_name = ""
            parameter_value = ""

            if "function_name" in node["content"]:
                function_name = node["content"]["function_name"]
            if "parameter_value" in node["content"]:
                parameter_value = node["content"]["parameter_value"]

            possible_next_cues = {}
            for next_node_id in node["next"]:
                if "condition" in node["next"][next_node_id]:
                    condition = node["next"][next_node_id]["condition"]
                    is_negative = condition[0] == "!"
                    condition_body = condition[1:] if is_negative else condition
                    new_cue = {
                        "ConditionFunctionName": "Is" + condition_body,
                        "bIsConditionNegative": is_negative
                    }
                    possible_next_cues[next_node_id] = new_cue
                else:
                    possible_next_cues[next_node_id] = {
                        "ConditionFunctionName": "",
                        "bIsConditionNegative": False
                    }

            cue = {
                "Name": node_id,
                "SpeakerName": speaker_name,
                "SpeakerType": speaker_type,
                "Summary": summary,
                "Text": text,
                "Subtitles": subtitles,
                "SoundWave": sound_wave,
                "AnimSequence": anim_sequence,
                "FunctionName": function_name,
                "FunctionParameterValue": parameter_value,
                "PossibleNextCues": possible_next_cues,
                "bIsHead": False
            }
            if len(node["prev"]) == 0:
                head_cue = cue
            cues.append(cue)

        cues.remove(head_cue)
        cues.insert(0, head_cue)
        head_cue["bIsHead"] = True

        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(cues, f, indent=4, ensure_ascii=False) 

        #result = []
        #for cue in cues:
            #result.append(cues[cue])
