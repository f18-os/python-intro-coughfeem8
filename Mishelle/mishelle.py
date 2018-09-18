#!/usr/bin/env/python3
'''
the program is the version of shell. Will create a subprocess, include
an ability make user redirecitons, create and run different  programs
just like a normal shell
'''
import os, sys, re


pid = os.getpid()                                      #get current id

looping = True
os.write(1,("welcome to Mishelle.\nms>>").encode())

rc = os.fork()
while looping:    
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        break
    elif rc == 0:
        command = input()
        args = re.split(' ',command)                    #argument list
        symbol = re.search(r'([<>]){1}',command)

        if command == 'exit':                           # exit command
            looping = False
        elif command == 'cd':                       # change directory
            print('changing directory')
        elif command == 'PS1':
            print ('PS1 variable accessed!')    # change normal-prompt

#       take and input and read it and parse it. if you encounter 
#       '<' , '>'  or '|'  you will send it to redirected  option
        elif symbol:
            os.close(1)                   #redirect child's stdout
            if symbol.group(1) == '>':
                sys.stdout = open(args[3], "w")
                fd = sys.stdout.fileno() 
                os.set_inheritable(fd, True)
            elif symbol.group(1) == '<':                 #'<' is found
                sys.stdout = open(args[1], "w")
                fd = sys.stdout.fileno() 
                os.set_inheritable(fd, True)
            elif symbol.group(1) == '|':                 #'|' is found
                rc2= os.fork()
                sys.stdout = open(args[0], "w")
                fd = sys.stdout.fileno()
        else:                             # try each directory in path
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir,args[0])
                try:
                    os.execve(program, args, os.environ)# exec program
                except FileNotFoundError:                # ...expected
                    pass                             # ...fail quietly
                os.write(2,("It was an error running %s" %
                            program).encode())  # terminate with error
                continue                              
    
    else:
        childPidCode = os.wait()
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                 (pid, rc)).encode())
        os.write(1, ("Parent: Child %d terminated with exit code %d\n"
                     %  childPidCode).encode())
        os.write(1,('ms>>').encode())
        continue

        
        
