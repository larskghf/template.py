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


helpText = "Usage without encryption: ./template.py -i <InputFolder> -o <OutputFolder>\n" \
           "                          ./template.py --inputdir <InputFolder> --outputdir <OutputFolder>\n" \
           "Usage with encryption: ./template.py --encrypt <EncryptionKey> --inputdir <InputFolder> --outputdir <OutputFolder>\n" \
           "                       ./template.py -e <EncryptionKey> -i <InputFolder> -o <OutputFolder>\n" \
           "                       ./template.py --decrypt <EncryptionKey> --inputdir <InputFolder> --outputdir <OutputFolder>\n" \
           "                       ./template.py -d <EncryptionKey> -i <InputFolder> -o <OutputFolder>\n"

# Get full command-line arguments
full_cmd_arguments = sys.argv
# Keep all but the first
argument_list = full_cmd_arguments[1:]
short_options = "he:d:i::o::"
long_options = ["help", "encrypt", "decrypt", "inputdir", "outputdir"]
try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    # print error, and return with an error code
    print(str(err))
    sys.exit(2)
for current_argument, current_value in arguments:
    if current_argument in ("-e", "--encrypt"):
        encryptionMode = "encrypt"
        encryptionKey = current_value
    if current_argument in ("-d", "--decrypt"):
        encryptionMode = "decrypt"
        encryptionKey = current_value
    if current_argument in ("-i", "--inputdir"):
        encryptionMode = "none"
        inputDir = current_value
    if current_argument in ("-o", "--outputdir"):
        encryptionMode = "none"
        outputDir = current_value
    if current_argument in ("-h", "--help"):
        print(helpText)
        sys.exit(2)

# check if inputDir and outputDir are set
if not inputDir or not outputDir:
    print(helpText)
    sys.exit(2)
# create empty files list
files = []
# check if input is file or directory and create list with input files
if os.path.isfile(inputDir):
    files.append(inputDir)
elif os.path.isdir(inputDir):
    for file in os.listdir(inputDir):
        files.append(os.path.join(inputDir, file))

for file in files:
    # create tempFile object from class TemplateFile
    tempFile = TemplateFile(file, outputDir)
    # use tempFile object functions
    if encryptionMode == "encrypt":
        tempFile.templateEncrypt(encryptionKey)
        tempFile.write()
    elif encryptionMode == "decrypt":
        tempFile.decrypt(encryptionKey)
        tempFile.write()
    elif encryptionMode == "none":
        tempFile.template()
        tempFile.write()
    else:
        print("error")
        sys.exit(4)
    # delete object tempFile
    del(tempFile)
    # print empty line after each files
    print("")