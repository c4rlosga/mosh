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
    reload(cmd)
    cmd.init(ourShell)
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
        # if it's an internal command don't append
        if not k[:2] == "__":
            t_funcs.append(k)
    for v in cmd.getCommands():
        if not v[:2] == "__":
            t_funcs.append(v)
    #for i in a sorted list do
    for i in sorted(t_funcs):
        print(i)
    #cmd.runCommand("__help","__help")
    pass

def showHistory():
    global lastCmd
    for entry in lastCmd:
        if (entry != '') and (entry != "\r") and (entry != lastCmd[0]):
            print(entry)

#def printup():
#    global up_index
#    print(f"up_index {up_index} , {lastCmd}")
#    pass

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
    #print("readCmd()")
    print(ourShell.shellPrompt,end='')
    sys.stdout.flush()

    userString = ""
    isReturn = False

    userChar = getchar()
    print("\r",end="")
    while not userChar == "\r":
        t_in = ""
        #print("got '{0}', {1}".format(userChar,len(userChar)),end='')
        #sys.stdout.flush()
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
            # a down arrow?
            elif t_in == "\x1b[B":
                # if we've pressed up at least once
                if up_index != 0:
                    # clear input buffer
                    t_in = ""
                    #print(up_index)
                    if up_index == 1 and len(lastCmd) == 2:
                        userString = ""
                    if lastUp and len(lastCmd) >= 3:
                        up_index += 2
                        lastUp = False
                    else:
                        up_index += 1
                    userString = lastCmd[up_index-1]

                    print("\r{0}{1}".format(ourShell.shellPrompt,userString),end=' '*24)
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
            #print("backspacin")
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
        return userString

def main(Arguments=None):
    global ourShell, lastCmd, up_index
    printMOTD()
    cmd.init(ourShell)
    while not isDone:
        global nextCmd
        nextCmd = readCmd()
        if len(lastCmd) > 10:
            del(lastCmd[9:])
        lastCmd.append(nextCmd)
        nextCmdName = nextCmd.split(' ')[0]
        if nextCmd.lstrip() == "" or nextCmd == "\r":
            print("\r{0}{1} ".format(ourShell.shellPrompt,""),end=''*24)
            print("\r{0}{1}".format(ourShell.shellPrompt,""),end='')
            print("\33[1C",end='')
            pass
        elif cmd.commandExists(nextCmdName) or nextCmdName in localCommands:
            print()
            #commands[nextCmdName]()
            doCommand(nextCmdName,nextCmd)
            up_index = 0
        else:
            #print(bytes(nextCmd,'UTF-8'))
            print("\n{0}: {1}: command not found".format(ourShell.shellName, nextCmd))
            #print("{0}, {1}".format(len(nextCmd), nextCmd[:-1]))
    else:
        print("Goodbye!")
        return 0
    return 0

if __name__ == '__main__':
    main(sys.argv)

