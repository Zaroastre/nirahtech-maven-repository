#/usr/bin/python

import os
import sys
import re

def are_valid_arguments(ARGUMENTS):
    if (len(ARGUMENTS) == 2):
        if (str(ARGUMENTS[-1]).endswith(".jar")):
            return True
    return False

def extract_artifact_id_and_version(url):
    splited_path = str(str(url).replace("\\", "/").replace("//", "/").replace("//", "/")).split("/")
    jar_file = str(splited_path[-1])
    if (jar_file.endswith(".jar")):
        jar_file = jar_file.replace(".jar", '')
        # json-geco-0.0.1-SNAPSHOT
        informations = jar_file.split('-')
        VERSION = re.search(r'([0-9]){1,}([.]([0-9]){1,}){0,}.+',jar_file).group(0)
        ARTIFACT_ID = jar_file.replace("-"+VERSION, '')
        return {"artifact": ARTIFACT_ID, "version": VERSION}
    exit(1)

def execute_maven_install_command(url, data):
    maven_install_command = "mvn install:install-file -DgroupId=io.nirahtech -DartifactId="+data["artifact"]+" -Dversion="+data["version"]+" -Dfile="+url+" -Dpackaging=jar -DgeneratePom=true -DlocalRepositoryPath=.  -DcreateChecksum=true"
    os.system(maven_install_command)

def execute_maven_build_command():
    maven_install_command = "mvn clean install -U"
    os.system(maven_install_command)

def process():
    ARGUMENTS = sys.argv
    if (are_valid_arguments(ARGUMENTS)):
        # Manual
        URL = str(ARGUMENTS[1])
        data = extract_artifact_id_and_version(URL)
        execute_maven_install_command(URL, data)
        return

    # Automatic: PROS-WORKSTATION-WINDOWS
    # workspace_root_base = "C:\\Users\\nmetivier\\Documents\\Programmation\\NIRAHTECH\\"
    
    # Automatic: PROS-WORKSTATION-LINUX
    # workspace_root_base = "/mnt/c/Users/nmetivier/Documents/Programmation/NIRAHTECH/"
    
    # Automatic: NIRAH-WORKSTATION-WINDOWS
    # workspace_root_base = str(ARGUMENTS[1])
    
    # Automatic: NIRAH-WORKSTATION-LINUX
    # workspace_root_base = str(ARGUMENTS[1])
    
    # Automatic: NIRAH-LAPTOP-LINUX
    workspace_root_base = "/home/z4r045tr3/nirahtech-workspace/"

    workspace_root_base = workspace_root_base.replace("\\", "/").replace("//", "/").replace("//", "/")
    projects = os.listdir(workspace_root_base)
    for project in projects:
        execute_maven_build_command()
        url = str(str(workspace_root_base) + str(project) + "/target/")
        if (os.path.exists(url) and os.path.isdir(url)):
            for potential_jar_file in os.listdir(url):
                if (str(potential_jar_file).endswith(".jar")):
                    url = str(url + str(potential_jar_file))
                    data = extract_artifact_id_and_version(url)
                    execute_maven_install_command(url, data)
def main():
    process()

if __name__ == "__main__":
    main()