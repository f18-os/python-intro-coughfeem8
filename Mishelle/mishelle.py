'''
the program is the version of shell. Will create a subprocess, include
an ability make user redirecitons, create and run different  programs
just like a normal shell
'''
import os, sys, re


pid = os.getpid()                                      #get current id


os.write(1,("welcome to Mishelle.\nms>>").encode())
while True:                                      #terminate with break
    rc = os.fork()
    if rc <  0:                                     #notifiy the error
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        continue
    elif rc == 0:                             #read input for commands
        '''
        take and input and read it and parse it. if you encounter 
        '<' , '>'  or '|'  you will send it to redired  option
        '''
        command = input()
        args = re.split(" ",command)                         #arg list
        if args[0] == "exit":                  #myshelle exit commands
            break
        # try each directory in the path
        
        for dir in re.split(":", os.environ['PATH']): 
            program = "%s/%s" % (dir, args[0])        
            try:
                                                 # try to exec program
                os.execve(program, args, os.environ)
            except FileNotFoundError:                       # expected
                pass                                     #fail quietly
            os.write(2,("It was an error running %s" %
                        program).encode())
            continue                                 # exit subprocess

    else:                                 #allow the parent todo stuff
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n"
                     %  childPidCode).encode())
        os.write(1,('ms>>').encode())
        
