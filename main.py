import xml.etree.ElementTree as ET
import machine
import time
import os
import errno
import netjob
import creator.validation, creator.scenario


class Run:

    def __init__(self, machineXMLFilePath):

        if os.path.exists(machineXMLFilePath):
            machineslist = self.getMachinesFromFile(machineXMLFilePath)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), machineXMLFilePath)
        s = creator.scenario.Scenario(r"Path\Basic.xml")
        for m in machineslist:
            s.set_main_script(m)  # machine file = (file)
            m.createFileScript(Path + str(m.name) + str('.sh'))
        for m in machineslist:
            print(f'[*] {m.name} -> {m.ip}')
        for m in machineslist:
            self.sendAndRun(m)
        for m in machineslist:
            s.validate(m)
            
        self.create_xml_from_machines(machineslist)
    
    def sendAndRun(self, host: machine.Machine):
        dastFileName = str(host.name) + str('.sh')
        dast_path = '/home/admin/' + dastFileName
        command_A = 'chmod 755 /home/admin/' + dastFileName
        command_B = "dos2unix " + dast_path + " ; " + dast_path + " > /home/admin/output.txt "
        command_C = "grep EndOfFileIndicator output.txt >/dev/null  && echo true || echo false"
        command_D = "cat /home/admin/output.txt"

        send = netjob.sendFileToMachine(host, host.file_path, dast_path)
        if send:
            print(f"Succeeded send {host.name + str('.sh')}  -> {host.ip}")
            commA = netjob.runCommandOnMachine(host, command_A)[0]
            if commA:
                print(f'command A passed {commA} -> {host.ip}')
                commB = netjob.runCommandOnMachine(host, command_B)[0]
                if commB:
                    print(f'command B passed {commB} -> {host.ip}')
                    commC = netjob.runCommandOnMachine(host, command_C)[0]
                    for i in range(3):
                        if commC:
                            break
                        else:
                            time.sleep(5)
                            commC = netjob.runCommandOnMachine(host, command_C)[0]
                    if commC:
                        print(f'command C passed {commC} -> {host.ip}')
                        commD = netjob.runCommandOnMachine(host, command_D)
                        if commD[0]:
                            host.output = commD[1]
                        else:
                            print(f'command D Failed -> {host.ip}')
                    else:
                        print(f'command C Failed -> {host.ip}')
                else:
                    print(f'command B Failed -> {host.ip}')
            else:
                print(f'command A Failed -> {host.ip}')
        else:
            print(f'Failed Send the file -> {host.ip}')

    def getMachinesFromFile(self, machineXMLFilePath):
        machineList = []  # value to return
        try:
            tree = ET.parse(machineXMLFilePath)
            root = tree.getroot()
        except:
            print(f"Failed where: parsing the file {machineXMLFilePath}")
            return None
        filelements = []  # all the <machine name="?">
        for elem in root:
            filelements.append(elem)
        for child in filelements:
            tags = ['interfaces/Interface[@name=\"eth0\"]/ipv4Address', 'userName', 'password', 'roles/role']
            data = []
            data.append(child.attrib['name'])
            for cc in tags:
                data.append(child.find(cc).text)
            machineList.append(machine.Machine(data[0], data[1], data[2], data[3], data[4]))
        return machineList

    def indent(self, elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def create_xml_from_machines(self, machines):
        root = ET.Element("root")
        doc = ET.SubElement(root, "doc")
        for machine in machines:
            machine_node = ET.SubElement(doc, f'{machine.name}')
            for obj in machine.validations:
                validation_node = ET.SubElement(machine_node, 'Validation')
                validation_node.set('Description', f'{obj.description}')
                result_node = ET.SubElement(validation_node, 'Result')
                result_node.set('Value', f'{obj.result}')
                action_node = ET.SubElement(validation_node, 'script_content')
                action_node.text = obj.script_contents
                output_node = ET.SubElement(validation_node, 'Output')
                output_node.text = obj.output
                logic = ET.SubElement(validation_node, 'Logic')
                logic.text = obj.validation_action
                expected = ET.SubElement(validation_node, 'Expected_output')
                expected.text = '\n'.join(obj.validation_strings)
        tree = ET.ElementTree(root)
        self.indent(root)
        tree.write('env_report.xml')

Run('TestMachines.xml')
