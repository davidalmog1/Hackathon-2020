
script_repository = "C:\\repository\\scripts\\" #DEBUG
class ScriptCreator:
    def __init__(self,scripts):
        script_txt = ""
        script_txt += "#!/bin/bash\n"
        for script in scripts:
            with open(script) as file:
                txt = file.read()
                txt = txt.replace("#!/bin/bash","")
                #script_txt += "\necho " + script + "\n"
                script_txt += "\necho " + script.split("\\")[-1] + "\n"
                script_txt += txt
                #script_txt += "\necho " + script + "\n"
                script_txt += "\necho " + script.split("\\")[-1] + "\n"
        script_txt += "\necho EndOfFileIndicator"
        self.script_txt = script_txt
