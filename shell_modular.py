#!/usr/bin/python3
import sys
from importlib import reload
import commands as cmd
import gc
gc.disable()

class Shell:
    def __init__(self):
        self.shellName = 'mosh'
        self.shellVersion = '0.2-history'
        self.shellLicense = 'mo(dular)sh(ell) pit v0 license'
        #self.shellPrompt = "Your!Prompt!Here!> "
        self.shellPrompt = '> '

isDone = False
nextCmd = []
lastCmd = [None]
ourShell = Shell()
up_index = 0
lastUp = True

def reloadCommands():
    global cmd, ourShell
    try:
        reload(cmd)
        cmd.init(ourShell)
    except Exception as e:
        print(f"\nUhh... something went wrong reloading :(\nmosh will stay the same\n{e}")
    else:
        print("Finished reload!")
    pass

def exitShell():
    global isDone
    isDone = True
    pass

def showHelp():
    global ourShell
    helpString = f"""    {ourShell.shellName}, version {ourShell.shellVersion} (x86_64-unknown-linux-gnu)
    These shell commands are defined internally. Type "help" to see this list.
    """
    print(helpString)

    t_funcs = []
    # iterate key and value in dict
    for k,v in localCommands.items():
        # if it's an internal command (prepend "__") ignore it
        if not k[:2] == "__":
            t_funcs.append(k)
    for v in cmd.getCommands():
        if not v[:2] == "__":
            t_funcs.append(v)
    #for each sorted command name, print it
    for i in sorted(t_funcs):
        print(i)
    pass

def showHistory():
    global lastCmd
    for entry in lastCmd:
        # only print the entry if it's valid (not empty, not null)
        if (entry != '') and (entry != "\r") and (entry != lastCmd[0]):
            print(entry)

localCommands = {
    #debug
    #'__p_up' : printup,
    #end debug
    'reload'    : reloadCommands,
    'reboot'    : reloadCommands,
    'exit'      : exitShell,
    'quit'      : exitShell,
    '?'         : showHelp,
    'help'      : showHelp,
    'history'   : showHistory
}

def printMOTD():
    global ourShell

    MOTD = f"""    {ourShell.shellName} v{ourShell.shellVersion}
    Distributed under the {ourShell.shellLicense} license.
    Type 'help' to see available commands."""
    print(MOTD)
    pass

def doCommand(commandName=None,passedInput=None):
    if commandName is None or passedInput is None:
        print("we somehow processed a None parameter?")
    if not cmd.commandExists(commandName):
        #print("we attempted to run a non-existing command. how.")
        localCommands[commandName]()
    else:
        # if the command isn't mosh's then it's probably an external command
        # so, let commands.py handle that
        cmd.runCommand(commandName,passedInput)

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
    return ch

def readCmd():
    global lastCmd, up_index
    print(ourShell.shellPrompt,end='')
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
                    print("\r{0}{1}".format(ourShell.shellPrompt,userString),end=' '*24)
                    print("\r{0}{1}".format(ourShell.shellPrompt,userString),end='')
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

                    print("\r{0}{1}".format(ourShell.shellPrompt,userString),end=' '*(len(ourShell.shellPrompt)+24))
                    print("\r{0}{1}".format(ourShell.shellPrompt,userString),end='')
                    print("\33[1C",end='')
                # so.. we're at the end of command history, pressing down AGAIN?
                #elif len(userString) > 0:
                #    # then I guess you just want to clean your input??
                #    userString = ""
                #    up_index = 0
                #    print("\r{0}{1}".format(ourShell.shellPrompt,userString),end=' '*24)
                #    print("\r{0}{1}".format(ourShell.shellPrompt,userString),end='')
                #    print("\33[1C",end='')

        elif userChar == "\x7f":
            # backspace handling, drop a character, carriage return and reprint
            userString = userString[:-1]
            print("\r{0}{1} ".format(ourShell.shellPrompt,userString),end='')
            print("\r{0}{1}".format(ourShell.shellPrompt,userString),end='')
            print("\33[1C",end='')
        else:
            userString += userChar
            print("\r{0}{1}".format(ourShell.shellPrompt,userString),end='')
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
            del(lastCmd[9:])
        # append the command we just ead
        lastCmd.append(nextCmd)

        # if we didn't get an empty inputº
        if nextCmd != None:
            # get ONLY the command name (no parameters)
            nextCmdName = nextCmd.split(' ')[0]

        # 'hack' to print a newline without changing readCmd()
        print()
        if cmd.commandExists(nextCmdName) or nextCmdName in localCommands:
            doCommand(nextCmdName,nextCmd)
            # reset up_index so our up arrow works properly
            up_index = 0
        # if the command doesn't exist, error out
        elif nextCmdName != None:
            print("{0}: {1}: command not found".format(ourShell.shellName, nextCmd))
        else:
            pass
    else:
        print("Goodbye!")
        return 0
    return 0

if __name__ == '__main__':
    main(sys.argv)

