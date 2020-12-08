#!/bin/env/python3
# functionName
from mosh import Shell
import re
# pls no touch
__names = []
shellName = ""
shellVersion = ""
shellLicense = ""
shellPrompt = ""

def runCommand(commandName=None,parameters=None, pipedInput=None):
    parameters = parameters.split(' ')[1:]
    __commands[commandName](parameters, pipedInput)
# end of pls no touch

# in order to define a function to interact with mosh properly, you MUST use a
# new line terminator and you MUST define only ONE function parameter in which
# you'll receive the user's parameters.
# What that means is that if the user types "ip link dev eth0" you'll receive
# the following array: ['link','dev','eth0'].
#
# Along with that, there's pipedInput which CAN be None (null) as the command
# may or may not be piped from a previous command. Whether you use it or not
# is up to you, but the premise of it is just to use what would otherwise 
# would be standard buffer input (stdin) but I'm too lazy to engineer it 
# otherwise.
# example of pipe: 
# echo "Hello world!" | tee file1.txt file2.txt
# in this case, parameters = ["file1.txt", "file2.txt"]
# and           pipedInput = "Hello world!"

# def exampleFunction(parameters=None, pipedInput=None):
#     print("Hi!")
#     print(f"We got the following parameters: {parameters}")
#     print(f"Through a pipe from a previous command we got this: {pipedInput}")
#     pass

# define your functions below
def helloWorld(parameters=None, pipedInput=None):
    print("heehee hoohoo") # heehee hoohoo peepee poopoo
    return 0


def testMe(parameters=None, pipedInput=None):
    print("Thanks for using mosh!")
    print(f"Got parameters: {parameters}")
    print(f"Got this pipe: {pipedInput}")
    return 0

def xdgOpen(parameters=None, pipedInput=None):
    print("stub function, will probably be *nix only")
    return -1

# Changed function definition because, if we check
# how it's invoked (line 14) the command's arguments
# are: functionName(parameters,pipe from previous)
# meaning that (self, parameters) actually gets
# the pipedInput as parameters
# def clearScreen(self, parameters=None):
def clearScreen(parameters=None, pipedInput=None):
    from sys import platform
    import os
    if platform == "linux" or platform == "darwin":
        os.system('clear')
    elif platform == "win32":
        os.system('cls')
    # Proudly YOINKED from StackOverflow :)

#def peckRegex(self, parameters=None): # pipedInput=Perhaps
def peckRegex(parameters=None, pipedInput=None):
    useRegex = False
    #print("Peck Regex placeholder. :(")
    # If we find -r or --regex
    if "-h" in parameters or "--help" in parameters:
        print("stub help")
        return
    if "-r" in parameters or "--regex" in parameters:
        # acknowledge it
        useRegex = True
        # remove either of the two  
        parameters.remove("-r") if "-r" in parameters else parameters.remove("--regex")
    if useRegex:
        # cat file | peck -r 'searchregex' 'substitution' 
        # compile our string into a regex 
        regex = re.compile(parameters[0])
        # once turned into regex, print the substitution of all matches in pipedInput
        # and replace() double empty lines at the end
        print(regex.sub(parameters[1], pipedInput).replace('\n\n','\n'))
    else:
        # print the substitution of all instances of the first parameter with {parameter} in pipedInput
        # and replace() double empty lines
        print(re.sub(parameters[0], f'{{{parameters[0]}}}', pipedInput).replace('\n\n','\n'))

# define your functions above

# add your commands to the dictionary below
__commands = {
    #
    # 'commandName' : functionName
    # Command names MUST be (single or double) quoted
    # Function names must [NOT] be quoted or else it'll be a string and not a function reference
    #

    # 'example' : exampleFunction,
    'helloworld' : helloWorld,
    'clear'     : clearScreen,
    'cls'       : clearScreen,
    'wipe'      : clearScreen,
    'testme'    : testMe,
    'peck'      : peckRegex
}

def getCommands():
    # get the command names
    global __names
    # return them
    return __names

def init(ShellClass=None):
    # set names to global so we can access it
    global __names, shellName, shellVersion, shellLicense, shellPrompt
    # create a new shell instance
    ShellClass = Shell()
    if ShellClass is None:
        # error out if it doesn't exist
        print("We didn't get the shell information.")
        return -1
    else:
        # if we successfully created a shell, set our variables
        shellName = ShellClass.shellName
        shellVersion = ShellClass.shellVersion
        shellLicense = ShellClass.shellLicense
        shellPrompt = ShellClass.shellPrompt

    # get each dict element
    for k,v in __commands.items():
        # append it
        __names.append(k)

    # return 0 to signal we're okay
    return 0

if __name__ == '__main__':
    print("Hey there!!! you aren't supposed to be running this as a standalone. Exiting now.")
    sys.exit(-1)
