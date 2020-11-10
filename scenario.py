import re
import xml.etree.ElementTree as ET
import creator.validation as validation
import creator.scriptcreator as scriptcreator


class Scenario:
    def __init__(self, scenario_file):
        self.tree = ET.parse(scenario_file)
        self.root = self.tree.getroot()
        self.validations = self.get_validations()
        self.description = self.get_description()

    def get_validations(self):
        validations_names = [x.attrib["value"] for x in self.root.findall("./validation")]
        validations = []
        #print(validations_names) #DEBUG
        for v in validations_names:
            validations.append(validation.Validation(v))

        return validations

    def get_description(self):
        return self.root.find("./name").attrib["value"]

    def get_script_for_machine(self,machine):
        script_list = []
        for v in self.validations:
            if v.is_supported(machine.type):
                script_list.append(v.get_script())
        return script_list

    def set_main_script(self, machine):
        s = scriptcreator.ScriptCreator(self.get_script_for_machine(machine))
        machine.file = s.script_txt

    def validate(self, m):
        m.validations = []
        result = m.output
        for k in self.validations:
            v = validation.Validation(k.xml_file)
            #contents = re.search("echo " + v.get_script() + "([\S\s]*?)" + "echo " + v.get_script(), m.file) # Error incomplete escape \U at position 7
            # contents = re.search(v.get_script().split("\\")[-1] + "([\S\s]*?)" + "echo " + v.get_script().split("\\")[-1], m.file)
            # contents = contents.group(1)
            # v.script_contents = contents.strip()
            if v.is_supported(m.type):
                contents = re.search(
                v.get_script().split("\\")[-1] + "([\S\s]*?)" + "echo " + v.get_script().split("\\")[-1], m.file)
                contents = contents.group(1)
                v.script_contents = contents.strip()
                m.validations.append(v)
                #substring = re.search(v.get_script()+"([\S\s]*?)"+v.get_script(),result)
                substring = re.search(v.get_script().split("\\")[-1] +"([\S\s]*?)"+v.get_script().split("\\")[-1],result)
                substring = substring.group(1)#Exception
                substring = substring.strip()
                v.set_output(substring)
                if v.validate(substring):
                    #print(v.get_description() + " Succeeded")
                    v.set_result(True)
                else:
                    #print(v.get_description() + " Failed")
                    v.set_result(False)


