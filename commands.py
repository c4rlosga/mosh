#!/bin/env/python3
# functionName
from shell_modular import Shell

# pls no touch
__names = []
shellName = ""
shellVersion = ""
shellLicense = ""
shellPrompt = ""
# end of pls no touch

def runCommand(commandName=None,parameters=None):
    parameters = parameters.split(' ')[1:]
    __commands[commandName](parameters)

# in order to define a function to interact with mosh properly, you MUST use a
# new line terminator and you MUST define only ONE function parameter in which
# you'll receive the user's parameters.
# What that means is that if the user types "ip link dev eth0" you'll receive
# the following array: ['link','dev','eth0'].

# def exampleFunction(parameters=None):
#     print("Hi!")
#     print(f"We got the following parameters: {parameters}")
#     pass

# define your functions below
def helloWorld(parameters=None):
    print("Hello, world!")
    pass

def testMe(parameters=None):
    print("Thanks for using mosh!")
    print(f"Got parameters: {parameters}")
    pass
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
    'testme' : testMe
}

# Do not edit these functions below if you don't plan on changing mosh's inner workings
# as these commands are crucial in order to run commands
def commandExists(commandName=None):
    # define it as global so we can interact with it
    global __names
    # if we're passed a null command
    if commandName == None:
        return 0
    # if not, just return a bool
    return (commandName in __names)

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
