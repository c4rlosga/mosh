#!/usr/bin/python3
import sys, re, os
from io import StringIO
from importlib import reload
import commands as cmd

class Shell:
    def __init__(self):
        self.shellName = 'mosh'
        self.shellVersion = '0.3-pipes'
        self.shellLicense = 'mo(dular)sh(ell) pit v0 license'
        # this is set as a lambda to test dynamic prompts, got the idea
        # and used https://stackoverflow.com/a/42499891 as reference for
        # a "dynamic" f-string without making it too complicated.
        # That means you can call functions or modules to make them the
        # prompt as long as they return a string.
        self.shellPrompt = lambda: f'mosh - {os.getcwd().split("/")[-1]}$ '
        #self.shellPrompt = lambda: f"Your!Prompt!Here!> "


isDone = False
nextCmd = []
lastCmd = [None]
ourShell = Shell()
up_index = 0
lastUp = True

def reloadCommands(parameters=None, pipedInput=None):
    global cmd, ourShell
    try:
        reload(cmd)
        cmd.init(ourShell)
    except Exception as e:
        print(f"\nUhh... something went wrong reloading :(\nmosh will stay the same\n{e}")
    else:
        print("Finished reload!")
    pass

def exitShell(parameters=None, pipedInput=None):
    global isDone
    isDone = True
    pass

def showHelp(parameters=None, pipedInput=None):
    global ourShell
    import platform
    helpString = f"""    {ourShell.shellName}, version {ourShell.shellVersion} (x86_64-{platform.system()})
    These shell commands are defined internally. Type "help" to see this list.
    """
    print(helpString)

    t_funcs = []
    # iterate key and value in dict
    for k,v in localCommands.items():
        # if it's an internal command (starts with "__") ignore it
        # if it's not, add it to the table of functions
        if not k[:2] == "__":
            t_funcs.append(k)
    for v in cmd.getCommands():
        # repeat process with external commands
        if not v[:2] == "__":
            t_funcs.append(v)
    #for each sorted command name, print it
    for i in sorted(t_funcs):
        print(i)
    pass

def showHistory(parameters=None, pipedInput=None):
    global lastCmd
    for entry in lastCmd:
        # only print the entry if it's valid (not empty, not null) and 
        # don't show the latest entry (which we know 100% will be "history")
        if (entry != '') and (entry != "\r") and (entry != lastCmd[0]):
            print(entry)

def cat(parameters=None, pipedInput=None):
    import os
    #if len(parameters) <= 0:
    #    print("no file given.")
    #    return -1
    for i in parameters:
        try:
            file = open(i, 'r')
            print(file.read(),end='')
            file.close()
        except Exception as e:
            print(f"Whoops, we couldn't open the file \"{i}\"\n{e}")
    return 0

def tee(parameters=None, pipedInput=None):
    import os
    append = False
    if "-h" in parameters or "--help" in parameters:
        print("tee [OPTIONS] [FILENAME]...")
        print("\t-a, --append\n\t\tAppend to the file/s given")
        print("\t-h, --help\n\t\tShow this help message")
    if len(parameters) <= 0:
        print("No parameters. Can't continue.")
        return -1
    if "-a" in parameters or "--append" in parameters:
        append = True
        parameters.remove("-a") if "-a" in parameters else parameters.remove("--append")
    for filename in parameters:
        try:
            if not append:
                # if we aren't appending, open as write (replace) and read mode "w+"
                f = open(filename, "w+")
                # go to the beginning
                f.seek(0)
                f.write(pipedInput)
                f.truncate()
                print(pipedInput)
            else:
                # if we're appending, open in append and read mode "a+"
                f = open(filename, "a+")
                # append content
                f.write(pipedInput)
                print(pipedInput)
        except Exception as e:
            print(f"Whoops, we couldn't open the file \"{filename}\"\n{e}")

    return 0

def echo(parameters=None, pipedInput=None):
    for item in parameters:
        print(item, end=' ') 
    print("", flush=True, end='')

def printMOTD(parameters=None, pipedInput=None):
    global ourShell

    MOTD = f"""    {ourShell.shellName} v{ourShell.shellVersion}
    Distributed under the {ourShell.shellLicense} license.
    Type 'help' to see available commands."""
    print(MOTD)
    pass

def lsDir(parameters=None, pipedInput=None):
    result = []
    dirs_only = False
    if "-h" in parameters or "--help" in parameters:
        print("ls [OPTIONS] [PATHS]...")
        print("\tIf no directory is given, the current directory is listed")
        print("\t-d, --directories\n\t\tOnly show directories")
        print("\t-h, --help\n\t\tShow this help message")
    if "-d" in parameters or "--directories" in parameters:
        dirs_only = True
        parameters.remove("-d") if "-d" in parameters else parameters.remove("--directories")
    # if we have no parameters
    if parameters == None or not parameters:
        # assume we're listing the current directory
        parameters.append(os.curdir)
    # iterate index and item in parameters
    for i, wd in enumerate(parameters):
        result.clear()
        # if there's more than one directory
        if not (len(parameters) == 1):
            # print its name
            print(f"{wd}:")
        # with each directory, get its contents
        for item in os.listdir(wd):
            # if it's a directory, format it as D
            if os.path.isdir(os.path.join(wd, item)):
                result.append(f"D    {item}")
            # if it's a L(ink), hard or soft, an L
            elif os.path.islink(os.path.join(wd, item)):
                result.append(f"L    {item}")
            # if not, it's a file, put an F
            else:
                result.append(f"F    {item}")
        for item in sorted(result):
            # if we're in directory-only mode and it's a directory
            if dirs_only and item[0] == 'D':
                # print it
                print(item)
            # if we're not in directory-only mode
            elif not dirs_only:
                # print everything
                print(item)
        # if there's more than 1 directory, add a newline in between
        if (i != len(parameters)-1):
            print()

    return 0

def getPwd(parameters=None, pipedInput=None):
    print(os.getcwd())
    return 0

def doCd(parameters=None, pipedInput=None):
    if parameters == None or len(parameters) == 0:
        getPwd()
    else:
        os.chdir(parameters[0])

def runPy(parameters=None, pipedInput=None):
    if (len(pipedInput) > 0) or (pipedInput != None):
        try:
            exec(pipedInput)
        except Exception as e:
            print(f"There was an exception whilst running your code\n{e}")
    if "-f" in parameters or "--file" in parameters:
        parameters.remove("-f") if "-f" in parameters else parameters.remove("--file")
        try:
            exec(open(parameters[0]).read())
        except Exception as e:
            print(f"There was an exception whilst running your code\n{e}")
    return 0

localCommands = {
    #debug
    #'__p_up' : printup,
    #end debug
    'reload'    : reloadCommands,
    'cat'       : cat,
    'tee'       : tee,
    #'reboot'    : reloadCommands,
    'exit'      : exitShell,
    'echo'      : echo,
    'quit'      : exitShell,
    '?'         : showHelp,
    'run'       : runPy,
    'ls'        : lsDir,
    'dir'       : lsDir,
    'cd'        : doCd,
    'pwd'       : getPwd,
    'help'      : showHelp,
    'history'   : showHistory,
    'motd'      : printMOTD
}

def doCommand(passedInput=None, pipedInput=None):
    commandName = passedInput.split(' ')[0]
    if commandName is None or passedInput is None:
        print("we somehow processed a None parameter?")
    if not commandName in cmd.getCommands():
        #print("we attempted to run a non-existing command. how.")
        passedInput = passedInput.split(' ')[1:]
        localCommands[commandName](passedInput, pipedInput)
    else:
        # if the command isn't mosh's then it's probably an external command
        # so, let commands.py handle that
        cmd.runCommand(commandName,passedInput, pipedInput)

def getchar():
    # Returns a single character from standard input
    import os
    ch = ''
    if os.name == 'nt': # how it works on windows
        import msvcrt
        ch = msvcrt.getch()
    else:
        import tty, termios, sys
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ord(ch) == 3: quit() # handle ctrl+C
    if type(ch) == bytes:
        ch = bytes.decode(ch)
    return ch

def readCmd():
    global lastCmd, up_index
    print(ourShell.shellPrompt(),end='')
    sys.stdout.flush()

    userString = ""
    isReturn = False

    # get a keypress
    userChar = getchar()

    # as long as the keypress isn't Return
    while not userChar == "\r":
        t_in = ""
        #if we get an ANSI escape sequence
        if userChar == "\x1b":
            #print(f"\ngot esc, {up_index}")
            t_in = ""
            # store it
            t_in += userChar
            # check the next two characters
            t_in += getchar()
            t_in += getchar()
            # an up arrow?
            if t_in == "\x1b[A":
                # okay, do we have any commands in history?
                if lastCmd[up_index-1] != None:
                    # clean the keypress
                    t_in = ""
                    # put the command as if we've just typed it in
                    userString = lastCmd[up_index-1]
                    # advance pointer to the next position
                    up_index -= 1
                    # dirty hack with carriage return to clear line
                    print("\r{0}{1}".format(ourShell.shellPrompt(),userString),end=' '*24)
                    print("\r{0}{1}".format(ourShell.shellPrompt(),userString),end='')
                    # ANSI sequence to move cursor
                    print("\33[1C",end='')
                    lastUp = True
            # we got a down arrow
            elif t_in == "\x1b[B":
                # if we've pressed up at least once
                if up_index != 0:
                    # clear the input buffer
                    t_in = ""
                    # if we're are the last entry already or we have no entries
                    if up_index == 1 and len(lastCmd) == 2:
                        # clear what was written
                        userString = ""
                    # if our last keypress was an up arrow, up_index += 2
                    # don't know why, but it works perfectly
                    if lastUp and len(lastCmd) >= 3:
                        up_index += 2
                        lastUp = False
                    # if not, then just +1
                    else:
                        up_index += 1
                    # update what the user has "written" to the command in the history
                    # and reprint prompt + userString
                    userString = lastCmd[up_index-1]

                    print("\r{0}{1}".format(ourShell.shellPrompt(),userString),end=' '*(len(ourShell.shellPrompt())+24))
                    print("\r{0}{1}".format(ourShell.shellPrompt(),userString),end='')
                    print("\33[1C",end='')
                # so.. we're at the end of command history, pressing down AGAIN?
                #elif len(userString) > 0:
                #    # then I guess you just want to clean your input??
                #    userString = ""
                #    up_index = 0
                #    print("\r{0}{1}".format(ourShell.shellPrompt()),userString),end=' '*24)
                #    print("\r{0}{1}".format(ourShell.shellPrompt()),userString),end='')
                #    print("\33[1C",end='')

        elif userChar == "\x7f":
            # backspace handling, drop a character, carriage return and reprint
            userString = userString[:-1]
            print("\r{0}{1} ".format(ourShell.shellPrompt(),userString),end='')
            print("\r{0}{1}".format(ourShell.shellPrompt(),userString),end='')
            print("\33[1C",end='')
        else:
            userString += userChar
            print("\r{0}{1}".format(ourShell.shellPrompt(),userString),end='')
            print("\33[1C",end='')
        userChar = ""
        userChar = getchar()
    else:
        # if the user input is NOT essentially blank
        if userString.lstrip() != "" and userString != "\r":
            # return it
            return userString
        # if it is, pass a null/None
        else:
            return None

def main(Arguments=None):
    global ourShell, lastCmd, up_index
    printMOTD()
    # create a new instance so we can set up the class for later reference
    cmd.init(ourShell)
    while not isDone:
        # get the global nextCmd
        global nextCmd
        # read user input
        nextCmd = readCmd()
        # if we have too much in history, keep it 10 items long
        if len(lastCmd) > 10:
            del(lastCmd[-1])
        # append the command we just read from user input
        lastCmd.append(nextCmd)

        # stupid workaround to print a newline without changing readCmd()
        print()
        # if we didn't get a None/null input
        regExp = r'(?!\B"[^"]*)\|(?![^"]*"\B)(?<!\\\|)'
        # this absolute behemoth of a regex is a mix of https://stackoverflow.com/questions/21105360/regex-find-comma-not-inside-quotes/21106122
        # and my own workings to detect pipes that aren't escaped or in quotes
        try:
            splitCmd = list(re.split(regExp, nextCmd))
        except:
            continue
        pipedInput = ""
        for i, item in enumerate(splitCmd):
            nextCmd = item.strip()
            if nextCmd != None:
                # get the command name (without parameters)
                nextCmdName = nextCmd.split(' ')[0]
                # check if the current cmd instance knows the command or if it's a shell command
                if nextCmdName in cmd.getCommands() or nextCmdName in localCommands:
                    # if it exists, and is the only/last command
                    #print(len(splitCmd), i)
                    #print(i == (len(splitCmd)-1))
                    if (len(splitCmd) <= 1) or (i == (len(splitCmd)-1)):
                        #doCommand(nextCmdName, nextCmd, pipedInput)
                        doCommand(nextCmd, pipedInput)
                        #print(lastCmd)
                        # reset up_index after executing so our up arrow works properly
                        up_index = 0
                        # if the command doesn't exist, error out
                    else:
                        #print("piped")
                        # source: https://www.kite.com/python/answers/how-to-redirect-print-output-to-a-variable-in-python
                        # store the reference to stdout
                        old_stdout = sys.stdout
                        # create a new stdout as a StringIO
                        new_stdout = StringIO()
                        # assign stdout to the StringIO instance
                        sys.stdout = new_stdout
                        # run command
                        #doCommand(nextCmdName, nextCmd, pipedInput)
                        doCommand(nextCmd, pipedInput)
                        # store output in pipedInput
                        pipedInput = new_stdout.getvalue()
                        # restore stdout so we're back to normal
                        sys.stdout = old_stdout
                else:
                    print("{0}: {1}: command not found".format(ourShell.shellName, nextCmd))
    else:
        print("Goodbye!")
        return 0
    return 0

if __name__ == '__main__':
    main(sys.argv)

