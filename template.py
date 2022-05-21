#!/usr/bin/env python3
import os
import getopt
import sys
import base64
import argparse
from argparse import RawTextHelpFormatter
from jinja2 import Template, Environment, meta

encryption_mode = encryption_key = input_dir = output_dir = var_file = None


class TemplateFile:
    def __init__(self, file, output_dir, var_file):
        self.output_filename = None
        self.output = None
        self.var_file_content = None
        self.path = file
        self.output_dir = output_dir
        # read file content
        read_file = open(self.path, 'r')
        self.input_file_content = read_file.read()
        read_file.close()
        # read var file content
        if var_file is not None:
            read_var_file = open(var_file, 'r')
            self.var_file_content = read_var_file.read().splitlines()
            read_var_file.close()

    def template(self):
        # get all undeclared variables
        env = Environment()
        ast = env.parse(self.input_file_content)
        variables = (meta.find_undeclared_variables(ast))
        variables_filled = {}
        # read variables from var_file (if var file argument is passed)
        if self.var_file_content is not None:
            for var_file_variable in self.var_file_content:
                splitted = var_file_variable.split('=')
                variables_filled[splitted[0]] = splitted[1]
        else:
            # read undeclared variables from os environment
            for var in variables:
                # read variables from environment
                var_value = str(os.getenv(var))
                variables_filled[var] = var_value
        # check if all needed variables are set
        for var in variables:
            if var in variables_filled:
                if variables_filled[var] == 'None' or variables_filled[var] == '':
                    print(f"ERROR: Variable {var} not set!")
                    sys.exit(3)
            else:
                print(f"ERROR: Variable {var} not set!")
                sys.exit(3)
        # render template with jinja2
        tm = Template(self.input_file_content)
        print(f"Rendering template file {self.path}")
        # set output
        self.output = tm.render(variables_filled)
        # get filename and remove ".tpl" from string
        self.output_filename = self.getFilename()
        if ".tpl" in self.output_filename:
            self.output_filename = self.output_filename.replace(".tpl", "")
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
        self.output_filename = f"{self.output_filename}.enc"
        return self.output

    def decrypt(self, key):
        # decrypt content
        print(f"Decrypting file {self.path}")
        from cryptography.fernet import Fernet
        fernet = Fernet(key.encode())
        decrypted = fernet.decrypt(self.input_file_content.encode())
        # set output
        self.output = decrypted.decode()
        # get filename and remove ".enc" from string
        self.output_filename = self.getFilename()
        if ".enc" in self.output_filename:
            self.output_filename = self.output_filename.replace(".enc", "")
        return self.output

    def write(self):
        # check if output_dir exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        # write self.output to output directory with self.output_filename as filename
        output_file = open(f"{self.output_dir}/{self.output_filename}", "w")
        print(f"Write file {self.output_filename} to output directory")
        output_file.write(self.output)
        return None

    def getFilename(self):
        # get filename from self.path
        filename = os.path.basename(self.path)
        return filename


def parseAndValidateArguments():
    # define global variables
    global encryption_mode, encryption_key, input_dir, output_dir, var_file
    formatter = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=40)
    examples = \
        '''examples:
      template.py -i <Input> -o <Output>
      template.py -e <encryption_key> -i <Input> -o <Output>
      template.py -d <encryption_key> -i <Input> -o <Output>'''
    parser = argparse.ArgumentParser(description="A simple python based templating engine", epilog=examples,
                                     formatter_class=formatter)
    parser.add_argument("-i", "--input", help="set input directory or single file",
                        required="--create-encryption-key" not in sys.argv, action="store", metavar="DIR/FILE")
    parser.add_argument("-o", "--output", help="set input directory or single file",
                        required="--create-encryption-key" not in sys.argv, action="store", metavar="DIR/FILE")
    cryptgroup = parser.add_mutually_exclusive_group(required=False)
    cryptgroup.add_argument("-e", "--encrypt", help="set mode to encrypt after templating (parameter: encryption key)",
                            required=False, action="store", metavar="ENC_KEY")
    cryptgroup.add_argument("-d", "--decrypt", help="set mode to decrypt a encrypted file (parameter: encryption key)",
                            required=False, action="store", metavar="ENC_KEY")
    parser.add_argument("--var-file", help="provide variable file instead of using environment variables",
                        required=False, action="store")
    parser.add_argument("--create-encryption-key", help="generate new encryption key and print to console",
                        required=False, action="store_true")
    args = parser.parse_args()
    if len(args.input) > 0:
        encryption_mode = "none"
        input_dir = args.input
    if len(args.output) > 0:
        encryption_mode = "none"
        output_dir = args.output
    if args.encrypt is not None:
        encryption_mode = "encrypt"
        encryption_key = args.encrypt
    if args.decrypt is not None:
        encryption_mode = "decrypt"
        encryption_key = args.decrypt
    if args.var_file is not None:
        var_file = args.var_file
    if args.create_encryption_key:
        encryption_key = base64.urlsafe_b64encode(os.urandom(32)).decode()
        print("------------------------------------------------------------------")
        print(f"Encryption key: {encryption_key}")
        print("------------------------------------------------------------------")
        sys.exit(0)


def createFileList(input):
    # create empty files list
    files = []
    # check if input is file or directory and create list with input files
    if os.path.isfile(input):
        files.append(input)
    elif os.path.isdir(input):
        for file in os.listdir(input):
            files.append(os.path.join(input, file))
    return files


def main():
    global encryption_mode, encryption_key, input_dir, output_dir, var_file
    parseAndValidateArguments()

    file_list = createFileList(input_dir)

    for file in file_list:
        # create temp_file object from class TemplateFile
        temp_file = TemplateFile(file, output_dir, var_file)
        # use temp_file object functions
        if encryption_mode == "encrypt":
            temp_file.templateEncrypt(encryption_key)
            temp_file.write()
        elif encryption_mode == "decrypt":
            temp_file.decrypt(encryption_key)
            temp_file.write()
        elif encryption_mode == "none":
            temp_file.template()
            temp_file.write()
        else:
            print("unknown error")
            sys.exit(4)
        # delete object temp_file
        del temp_file
        # print empty line after each files
        print("")


if __name__ == "__main__":
    main()
