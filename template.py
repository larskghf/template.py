#!/usr/bin/env python3
import os
import getopt
import sys
from jinja2 import Template, Environment, meta

class TemplateFile:
    def __init__(self, file, outputDir):
        self.path =  file
        # read file content
        readFile = open(self.path, 'r')
        self.inputContent = readFile.read()
        self.outputDir = outputDir
        readFile.close()
        return None
    def template(self):
        # get all undeclared variables
        env = Environment()
        ast = env.parse(self.inputContent)
        variables = (meta.find_undeclared_variables(ast))
        variablesFilled = {}
        # read undeclared variables from os environment
        for var in variables:
            varValue = str(os.getenv(var))
            if varValue == 'None' or varValue == '':
                print(f"ERROR: Variable {var} not set!")
                sys.exit(3)
            variablesFilled[var] = varValue
        # render template with jinja2
        tm = Template(self.inputContent)
        print(f"Rendering template file {self.path}")
        # set output
        self.output = tm.render(variablesFilled)
        # get filename and remove ".tpl" from string
        self.outputFilename = self.getFilename()
        if ".tpl" in self.outputFilename:
            self.outputFilename = self.outputFilename.replace(".tpl", "")
        return self.output
    def templateEncrypt(self, key):
        # first template input file
        self.template()
        # encrypt rendered content
        from cryptography.fernet import Fernet
        fernet = Fernet(key.encode())
        encrypted = fernet.encrypt(self.output.encode())
        # set output
        self.output = encrypted.decode()
        # get filename and add ".enc" to string
        self.outputFilename = self.getFilename()
        self.outputFilename = f"{self.outputFilename}.enc"
        return self.output
    def decrypt(self, key):
        # decrypt content
        print(f"Decrypting file {self.path}")
        from cryptography.fernet import Fernet
        fernet = Fernet(key.encode())
        decrypted = fernet.decrypt(self.inputContent.encode())
        # set output
        self.output = decrypted.decode()
        # get filename and remove ".enc" from string
        self.outputFilename = self.getFilename()
        if ".enc" in self.outputFilename:
            self.outputFilename = self.outputFilename.replace(".enc", "")
        return self.output
    def write(self):
        # check if outputdir exists
        if not os.path.exists(self.outputDir):
            os.makedirs(self.outputDir)
        # write self.output to output directory with self.outputFilename as filename
        outputFile = open(f"{self.outputDir}/{self.outputFilename}", "w")
        print(f"Write file {self.outputFilename} to output directory")
        outputFile.write(self.output)
        return None
    def getFilename(self):
        # get filename from self.path
        filename = os.path.basename(self.path)
        return filename


##Debugging
test = TemplateFile("./input/test.txt", "./output")
print(test.template())
#print(test.templateEncrypt("tTb1gwfBaDCQ7n7lOWkA1Fv/TQ8FIAojb2w9K9A25V0="))
#print(test.decrypt("tTb1gwfBaDCQ7n7lOWkA1Fv/TQ8FIAojb2w9K9A25V0="))
test.write()