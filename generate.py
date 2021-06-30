print("Importing modules")
from enum import Enum
from dataclasses import dataclass
import re
import os
print("Import complete")

class ValidationResponse(Enum):
    FAILURE = 0
    SUCCESS = 1

@dataclass
class Configuration():
    path: str
    port: int
    color: str
    fancyJS: bool
    title: str

    def display(self):
        print("Path: ".rjust(25) + self.path)
        print("Port: ".rjust(25) + str(self.port))
        print("Colour: ".rjust(25) + self.color)
        print("Include Fancy JS: ".rjust(25) + str(self.fancyJS))
        print("Title: ".rjust(25) + self.title)

        print("----------------------------------------------------")

def query_validate(text, validate_function):
    print(text)

    while True:
        inp = input("> ")
        validationResponse, output = validate_function(inp)

        if validationResponse == ValidationResponse.SUCCESS:
            return output
        
        else:
            print("Invalid input.")

def path_validate(path):
    try:
        allowedDriveNames = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        if path[0] == "/" or path[0] in allowedDriveNames:
            if path[-1] != "/":
                path = path + "/"

            return ValidationResponse.SUCCESS, path

    except:
        return ValidationResponse.FAILURE, None

    return ValidationResponse.FAILURE, None

def port_validate(port):
    try:
        if int(port) > 0 and int(port) < 65537:
            return ValidationResponse.SUCCESS, int(port)
            
    except:
        return ValidationResponse.FAILURE, False

    return ValidationResponse.FAILURE, False

def bool_validate(inp):
    try:
        yesPhrases = ["1", "y", "ok", "true"]
        noPhrases = ["0", "n", "false"]

        inp = inp.lower()

        for phrase in yesPhrases:
            if phrase in inp:
                return ValidationResponse.SUCCESS, True

        for phrase in noPhrases:
            if phrase in inp:
                return ValidationResponse.SUCCESS, False
    except:
        return ValidationResponse.FAILURE, None

    return ValidationResponse.FAILURE, None

def color_validate(hex_code):
    try:
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_code)

        if match:
            return ValidationResponse.SUCCESS, hex_code
    except:
        return ValidationResponse.FAILURE, None

    return ValidationResponse.FAILURE, None

def title_validate(title):
    return ValidationResponse.SUCCESS, title

def get_initial_input():
    path = query_validate("Please enter the _absolute_ path.", path_validate)

    port = query_validate("Please enter the initial port.", port_validate)

    color = query_validate("Enter the hex code for the theme colour", color_validate)

    doFancyJS = query_validate("Automatically include fancy JS?", bool_validate)

    title = query_validate("Please enter the title of the project.", title_validate)

    return Configuration(path, port, color, doFancyJS, title)

def create_or_reuse_directory(path):
    if not os.path.isdir(path):
        print(f"Directory {path} not found. Automatically generating...")
        os.makedirs(path)

    else:
        print(f"Directory {path} already exists! Not creating a new one.")

def create_from_template(filename, placeIn, **kwargs):
    print(f"Processing {filename}.template destined for {placeIn} with replacement: {str(kwargs)}")

    with open(filename + ".template", "r") as f:
        sourceText = f.read()

        for key, value in kwargs.items():
            key = f"$${key}$$"
            sourceText = sourceText.replace(key, value)
            print(f"Replacing {key} with {value} in {filename} destined for {placeIn}")

        with open(placeIn, "w") as f:
            f.write(sourceText)

def generate(config):
    create_or_reuse_directory(config.path)

    create_or_reuse_directory(config.path + "templates")
    create_or_reuse_directory(config.path + "assets")

    if config.fancyJS:
        fancyJS = "<script src=\"/assets/fancy.js\"></script>"
    else:
        fancyJS = "<!--Fancy JS could have gone here, but was not added because of user configuration. -->"

    create_from_template("index.html", config.path + "templates/index.html", FANCY_JS_IMPORT=fancyJS, TITLE=config.title)
    create_from_template("main.js", config.path + "assets/main.js")
    
    if config.fancyJS:
        create_from_template("fancy.js", config.path + "assets/fancy.js")

    create_from_template("styles.css", config.path + "assets/styles.css", ACCENT_COLOR=config.color)

    create_from_template("main.py", config.path + "main.py", PORT=str(config.port))

    print("\n----------------------------------------------------\n")
    print("Generation complete. Have a nice day.")

def main():
    initInp = get_initial_input()
    #for debug purposes
    #initInp = Configuration("C:/Users/alexc/Documents/GitHub/flask-generator/test_project/", 500, "#ce0000", True, "Test Project")

    initInp.display()

    print("If you are unhappy with this configuration, re run the tool now. If you are happy with this configuration, click enter to begin setup process.")
    input("> ")

    generate(initInp)

if __name__ == "__main__":
    main()