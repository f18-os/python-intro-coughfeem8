#!/usr/bin/env/python3
'''
the program is the version of shell. Will create a subprocess, include
the ability make  redirecitons, create and run different  programs
just like a normal shell
'''
import os, sys, re


pid = os.getpid()                                      #get current id
os.environ['PS1'] = '$ ' #os.getcwd()
looping = True

rc = os.fork()

if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())

elif rc == 0:
    while looping:
        command = input(os.environ['PS1'])
        args = re.split(' ',command)                    #argument list
        symbol = re.search(r'([<>\|]){1}',command)

        if command == '':
            os.write(2,('not a command at all' %args[1]).encode())
        elif args[0] == 'exit':                         # exit command
            looping = False
        elif args[0] == 'cd':                       # change directory
            print('changing directory')
            try:
                os.chdir('{0}/{1}'.format(os.getcwd(),args[1]))
            except  NotADirectoryError:
                os.write(2,('directory %s not found.' %args[1]).encode())

        elif args[0] == 'PS1':
            print ('PS1 variable accessed!')    # change normal-prompt
            os.environ['PS1'] = args[1]         # to the 2nd  argument

#       take and input and read it and parse it. if you encounter
#       '<' , '>'  or '|'  you will send it to redirected  option
        elif symbol:
            os.close(1)                   #redirect child's stdout
            if symbol.group(1) == '>':
                sys.stdout = open(args[2], "w")
                fd = sys.stdout.fileno() 
                os.set_inheritable(fd, True)
            elif symbol.group(1) == '<':             #'<' is found
                sys.stdout = open(args[0], "w")
                fd = sys.stdout.fileno() 
                os.set_inheritable(fd, True)
            elif symbol.group(1) == '|':             #'|' is found
                print ('piping')
        else:                             # try each directory in path
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir,args[0])
                try:
                    os.execve(program, args, os.environ)# exec program
                except FileNotFoundError:                # ...expected
                    pass                             # ...fail quietly
                os.write(2,("It was an error running %s\n cat" %
                           program).encode())  # terminate with error 

else:
    childPidCode = os.wait()
    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
             (pid, rc)).encode())
    os.write(1, ("Parent: Child %d terminated with exit code %d\n"
                 %  childPidCode).encode())

        
        
