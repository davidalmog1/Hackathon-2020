import xml.etree.ElementTree as ET

def get_script_contensts():
    pass


def get_commands():
    pass


class Validation:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        self.script_to_run = self.get_script()
        self.supported_machines = self.get_supported_machines()
        self.description = self.get_description()
        self.validation_action = self.get_validation_action()
        self.validation_strings = self.get_validation_strings()
        self.commands = self.get_commands()
        self.script_contents = None
        self.result = None  # True False
        self.output = None

    def get_script(self):
        return self.root.find("./general/script").attrib["name"]

    def get_supported_machines(self):
        return [x.attrib["type"].upper() for x in self.root.findall("./general/supported_machine")]

    def get_description(self):
        return self.root.find("./general/description").attrib["value"]

    def get_validation_action(self):
        return self.root.find("./validations_list/action").attrib["value"].upper()

    def get_validation_strings(self):
        return [x.attrib["value"] for x in self.root.findall("./validations_list/result_string")]

    def validate(self, output):
        self.output = output
        if self.validation_action == "NOT":
            for vs in self.validation_strings:
                if vs in output:
                    return False
            return True

        elif self.validation_action == "AND":
            for vs in self.validation_strings:
                if not vs in output:
                    return False
            return True

        elif self.validation_action == "OR":
            for vs in self.validation_strings:
                if vs in output:
                    return True
            return False

        elif self.validation_action == "ABOVE":
            if not output.isnumeric():
                return False
            for vs in self.validation_strings:
                return int(output) > int(vs)
        elif self.validation_action == "BELOW":
            if not output.isnumeric():
                return False
            for vs in self.validation_strings:
                return int(output) < int(vs)

        elif self.validation_action == "REG_NOT":
            pass
        elif self.validation_action == "REG_AND":
            pass
        elif self.validation_action == "REG_OR":
            pass

    def is_supported(self, machine_type):
        return machine_type in self.supported_machines

    def set_result(self, result):
        self.result = result

    def set_output(self, output):
        self.output = output

    def __str__(self):
        tmp = ""
        tmp = tmp + "Desc:\n" + self.get_description() + "\n"
        tmp = tmp + "***********************************\n"
        tmp = tmp + "result: \n" + self.script_to_run + "\n"
        tmp = tmp + "***********************************\n"
        tmp = tmp + "script contents: \n" + self.script_contents + "\n"
        tmp = tmp + "***********************************\n"
        tmp = tmp + "result: \n" + str(self.result) + "\n"
        tmp = tmp + "***********************************\n"
        tmp = tmp + "output: \n" + self.output + "\n"
        tmp = tmp + "***********************************\n"
        tmp = tmp + "action: \n" + self.get_validation_action() + "\n"
        tmp = tmp + "***********************************\n"

        tmp = tmp + "result strings:\n"
        for s in self.validation_strings:
            tmp += s + "\n"

        return tmp

    def get_commands(self):
        return [x.attrib["value"] for x in self.root.findall("./general/command")]
