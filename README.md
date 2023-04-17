# :memo: template.py

`template.py` is a simple python-based templating engine. It allows you to define templates for configuration files,
which can be customized with values from environment variables or a variable file. Additionally, it provides the option
to encrypt and decrypt the resulting files.

## 🚀 Usage

```bash
template.py [-h] [-i DIR/FILE] [-o DIR/FILE] [-e ENC_KEY] [-d ENC_KEY] [--var-file VAR_FILE] [--create-encryption-key]
```

### Arguments

* `-h, --help`: show help message and exit
* `-i DIR/FILE, --input DIR/FILE`: set input directory or single file
* `-o DIR/FILE, --output DIR/FILE`: set output directory or single file
* `-e ENC_KEY, --encrypt ENC_KEY`: set mode to encrypt after templating (parameter: encryption key)
* `-d ENC_KEY, --decrypt ENC_KEY`: set mode to decrypt an encrypted file (parameter: encryption key)
* `--var-file VAR_FILE`: provide variable file instead of using environment variables
* `--create-encryption-key`: generate new encryption key and print to console

### Examples

```bash
template.py -i <Input> -o <Output>
```

```bash
template.py -e <encryption_key> -i <Input> -o <Output>
```

```bash
template.py -d <encryption_key> -i <Input> -o <Output>
```

## :whale: Using `template.py` with Docker

`template.py` is also available as a Docker image. This allows you to use the tool without having to install it on your
local machine.

To use `template.py` with Docker, you can pull the latest image from Docker Hub:

```bash
docker pull larskghf/template.py:latest
```

You can then run the image using the `docker run` command. For example, to use `template.py` to render a template file
and write the output to a file on your local machine, you can use the following command:

```bash
docker run --rm -v /path/to/input:/input -v /path/to/output:/output larskghf/template.py:latest -i /input/template.tpl -o /output/output.txt
```

This command mounts two volumes (`/path/to/input` and `/path/to/output`) to the Docker container, which
allows `template.py` to access the input and output files on your local machine.

Note that the `--rm` flag removes the container after it has finished running, which helps to keep your Docker
environment clean.

You can also pass other command-line arguments to `template.py` as part of the `docker run` command. For example, to
encrypt the output file using an encryption key, you can use the following command:

```bash
docker run --rm -v /path/to/input:/input -v /path/to/output:/output larskghf/template.py:latest -i /input/template.tpl -o /output/output.txt -e <encryption_key>
```

Again, make sure to replace `/path/to/input`, `/path/to/output`, and `<encryption_key>` with the appropriate values for
your environment.

## 🔑 How to create a new encryption key

`template.py` provides an option to create a new encryption key. This is useful if you want to encrypt the resulting
files and you don't have a key yet. To create a new encryption key, run `template.py` with the `--create-encryption-key`
argument:

```bash
template.py --create-encryption-key
```

This will generate a new encryption key and print it to the console. You can then copy the key and use it to encrypt
your files by running `template.py` with the `-e` argument followed by the key:

```bash
template.py -e <encryption_key> -i <Input> -o <Output>
```

Note that the encryption key should be kept secret and not shared with anyone who should not have access to the
encrypted files.

## 🔧 How it works

`template.py` reads a template file and searches for undeclared variables. These variables can be defined either in the
environment variables or a variable file. If a variable is not set, the program terminates with an error message.

After all variables have been filled, the program renders the template file using
the [Jinja2](https://palletsprojects.com/p/jinja/) templating engine. If the encryption mode is enabled, the program
encrypts the resulting file using the [cryptography](https://cryptography.io/en/latest/) library.

The resulting file is then written to the output directory with the same filename as the input file. If the encryption
mode is enabled, the filename is suffixed with ".enc".

## 🎉 Conclusion

`template.py` is a simple yet powerful tool for generating configuration files based on templates. Its support for
environment variables and variable files makes it easy to customize the resulting files, while its encryption mode
allows you to keep sensitive information secure. Whether you use it locally or in a Docker container, `template.py` is a
valuable addition to your DevOps toolbox.
