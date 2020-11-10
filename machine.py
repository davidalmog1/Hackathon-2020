class Machine:
    name = None
    ip = None
    username = None
    password = None
    type = None
    status = None  # The current status of the machine
    file = None  # String script to run on the machine
    file_path = None  #
    output = None  # the output from the running the script
    result = None  # after analyze the output
    validations = None  # validations list

    def __init__(self, name, ip, username, password, type):
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password
        self.type = type.upper()

    def printAllParams(self):
        print(f"\nname: {self.name}\nIP: {self.ip}\nUserName: {self.username}"
              f"\nPassword: {self.password}\nType: {self.type}\nStatus: {self.status}\nFilePath: {self.file_path}"
              f"\nfile: {self.file}\nOutput: {self.output}\nResult: {self.result}\nValidation: {self.validations}")

    def createFileScript(self, path):
        try:
            with open(path, 'w') as f:
                f.writelines(self.file)
        except:
            print("Error creating a File Script")
        self.file_path = path
