print("Importing modules")
import os
import json
from pathlib import Path
import shutil

print("Import complete")


def main():
    print("Finding information from manifests")
    # Find all the manifests, parse, present options, then implement
    manifests = []
    for possiblefolder in os.listdir(os.getcwd() + "/templates/"):
        folderPath = os.getcwd() + "/templates/" + possiblefolder
        if os.path.isdir(folderPath):
            if os.path.isfile(folderPath + "/manifest.json"):
                with open(folderPath + "/manifest.json") as manifestfile:
                    manifests.append(json.loads(manifestfile.read()))

    print("Manifest information found")
    print("------------------------")
    # Present options
    for manifest in manifests:
        print("Name:           " + manifest["name"])
        print("Description:    " + manifest["description"])
        print("------------------------")

    while True:
        # Get input
        print("Which would you like to use? ")
        resp = input("> ")

        if resp in [manifest["name"] for manifest in manifests]:
            print("Using " + resp)
            break
        else:
            print("Invalid input")

    # Ask for details
    # side note, I love this syntax
    manifest = [manifest for manifest in manifests if manifest["name"] == resp][0]
    args = {}

    validArgTypes = ["string", "int", "float", "bool", "port", "color"]

    for arg in manifest["args"]:
        if arg["type"] not in validArgTypes:
            print("Invalid arg type for " + str(arg))

    for arg in manifest["args"]:
        while True:
            print(arg["question"])
            print("(Type: " + arg["type"] + ")")
            resp = input("> ")
            if arg["type"] == "string":
                args[arg["key"]] = resp
                break

            elif arg["type"] == "int":
                try:
                    args[arg["key"]] = int(resp)
                    break
                except ValueError:
                    print("Invalid input")
                    continue

            elif arg["type"] == "float":
                try:
                    args[arg["key"]] = float(resp)
                    break
                except ValueError:
                    print("Invalid input")
                    continue

            elif arg["type"] == "bool":
                if resp.upper() in ["TRUE", "YES", "Y", "1"]:
                    args[arg["key"]] = True
                    break
                elif resp.upper() in ["FALSE", "NO", "N", "0"]:
                    args[arg["key"]] = False
                    break
                else:
                    print("Invalid input")
                    continue

            elif arg["type"] == "port":
                try:
                    int(resp)
                    if int(resp) > 65536 or int(resp) < 1024:
                        print("Invalid port - ports should be between 1024-65536 inclusive")

                    args[arg["key"]] = resp
                    break

                except ValueError:
                    print("Input isn't an int, let alone a valid port")
                    continue

            elif arg["type"] == "color":
                # validate that the arg["type"] is a valid html colour. Allow text like 'red' as well as rgb() and hex
                if resp.startswith("#") and len(resp) == 7:
                    args[arg["key"]] = resp
                    break

                elif resp.startswith("rgb("):
                    if resp.endswith(")"):
                        args[arg["key"]] = resp
                        break

                elif resp.lower() in ["red", "green", "blue", "yellow", "orange", "purple", "pink", "cyan", "white",
                                      "black", "grey"]:
                    args[arg["key"]] = resp
                    break

                else:
                    print("Invalid input")
                    continue

    # now create from template
    # first, request path
    print("Where would you like to create the project? ")
    dstpath = input("> ").strip()
    """
    
    Not needed, as the shutil copies it
    
    if not os.path.isdir(dstpath):
        try:
            os.mkdir(dstpath)
        except FileNotFoundError:
            segments = Path(dstpath).parts
            sofar = ""
            for segment in segments:
                try:
                    os.mkdir(sofar + segment)
                except FileExistsError:
                    pass

                sofar += segment + "/"

        except FileExistsError:
            pass
            
    """

    create_in_folder(dstpath, os.getcwd() + "/templates/" + manifest["name"], args)


def create_in_folder(dstpath, srcpath, args):
    print("Beginning creation")

    def replace_contents(args, contents):
        for key, value in args.items():
            contents = contents.replace("{{" + key.lower() + "}}", value)
            contents = contents.replace("{{ " + key.lower() + " }}", value)
            contents = contents.replace("{{" + key.upper() + "}}", value)
            contents = contents.replace("{{ " + key.upper() + " }}", value)
            contents = contents.replace("$" + key.upper(), value)
            contents = contents.replace("$" + key.lower(), value)

        return contents

    # copy over to dst folder
    shutil.copytree(srcpath, dstpath)
    # iterate over dst folder
    for root, dirs, files in os.walk(dstpath):
        for file in files:
            filepath = root + "/" + file
            print("Processing " + filepath)

            with open(filepath, "r") as f:
                contents = f.read()

                contents = replace_contents(args, contents)

            with open(filepath, "w") as f:
                f.write(contents)

            print("Done!")

    print("Would you like to run it?")
    resp = input("> ").strip()
    if resp.upper() in ["YES", "Y", "TRUE"]:
        print("Running start.sh...")
        os.system("cd " + dstpath + " && chmod +x ./start.sh && ./start.sh")

#create_in_folder("/home/user/programming/flask-generator/thing", "/home/user/programming/flask-generator/templates/Report", {"port": "8091", "title": "Testing", "primary-color": "orange", "background-color": "black", "text-color": "white"})

if __name__ == "__main__":
    main()