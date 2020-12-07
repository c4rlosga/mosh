# mosh
a very high level mo(dular) sh(ell) scripted in python

### How to write a function/command
  Open `commands.py` and create a function (**above** line 84, where `__comands = {` is) with your desired name and **two** (required) parameters (typically named `Parameters` and `pipedInput`).
  For this example, we'll use helloWorld:
  ```python
  def helloWorld(Parameters=None, pipedInput=None):
    print("Hello world!")
    pass
  ```
  Now, you need to edit `__commands` in the same file and add a line with the command (as in what will the user type) and the name of the function you've just written.
  In this case, we'd add this:
  ```python
  __commands = {
  [...]
  'hello'  : helloWorld
  [...]
  }
  ```
  After saving that, you can type `reload` if you have a running instance or open a new instance of `mosh` to use `hello`, your new command!
  Further information can be found in the [project Wiki](wiki/Home)

&nbsp;
##### Things that work
 - Piping (theoretical infinite)
 - Basic terminal commands (`cat`, `tee`, `ls`, `cd`...)
 - Reloading external commands (`commands.py`) without reloading the shell (using `reload`)
 - Customizable shell info
 - Running external code (for instance piping `cat [FILE] | run`) or using (`run -f [FILE]`)
 - Dynamic prompt (using a lambda function)
 - Command history (Up and down arrows and using `history`)
 - Exception handling when running external commands
 
##### TO-DO
 - Return codes/return status
 - Add colors
 - Check/fix compatibility with Win/NT based systems (remove dependencies on \*NIX carriage control, for instance)
 - 
