#! /usr/bin/env python3
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
           continue
        elif args[0] == 'exit':                         # exit command
            looping = False
        elif args[0] == 'cd':                       # change directory
            try:
                os.chdir('{0}/{1}'.format(os.getcwd(),args[1]))
                os.write(1,('changing directory to: %s\n' %
                            os.getcwd()).encode())
            except  FileNotFoundError:
                os.write(2,('directory %s not found.\n' %args[1]).encode())

        elif args[0] == 'PS1':
            print ('PS1 variable accessed!')    # change normal-prompt
            os.environ['PS1'] = args[1]         # to the 2nd  argument

#       take and input and read it and parse it. if you encounter
#       '<' , '>'  or '|'  you will send it to redirected  option
        elif symbol:
            os.close(1)                   #redirect child's stdout
            #format  'programs' 'arg' '>' 'file'
            if symbol.group(1) == '>':
                sys.stdout = open(args[3], "w")
                fd = sys.stdout.fileno() 
                os.set_inheritable(fd, True)
                for dir in re.split(":", os.environ['PATH']):
                    program = "%s/%s" % (dir,args[0])
                    try:
                        os.execve(program, args, os.environ)
                    except FileNotFoundError:                
                        pass                             
                os.write(2,("It was an error running %s\n" %
                           program).encode())   
                    
            elif symbol.group(1) == '<':             #'<' is found
                #format 'file' '<' 'programs' 'arg'
                sys.stdout = open(args[0], "w")
                fd = sys.stdout.fileno() 
                os.set_inheritable(fd, True)
                #try to execute
                for dir in re.split(":", os.environ['PATH']):
                    program = "%s/%s" % (dir,args[2]) #after symbol
                    try:
                        os.execve(program, args, os.environ)
                    except FileNotFoundError:                
                        pass                             
                os.write(2,("It was an error running %s\n" %
                           program).encode())   

            elif symbol.group(1) == '|':             #'|' is found
                #format  'program' 'file' '|' 'program' 
                print ('piping\n')
                pr,pw = os.pipe()
                for f in (pr, pw):
                    os.set_inheritable(f, True)
                rc2 = os.fork()                     # grandchild
                if rc2 < 0:
                    os.write(2, ("fork failed, returning %d\n" %
                                 rc).encode())
                    continue
                elif rc2 == 0:            # child - will talk  to pipe
                    os.close(1)              # redirect child's stdout
                    os.dup(pw)
                    for fd in (pr, pw):
                        os.close(fd)

                    for dir in re.split(":", os.environ['PATH']):
                        program = "%s/%s" % (dir,args[3])
                        try:
                            os.execve(program, args, os.environ)
                        except FileNotFoundError:                
                            pass                            
                    os.write(2,("It was an error running %s\n" %
                           program).encode())   # terminate with error
else:

                    

                else:                             # parent (forked ok)
                    os.close(0)
                    os.dup(pr)
                    for fd in (pw, pr):
                        os.close(fd)


                                                          #normal case
        else:                             # try each directory in path
          for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir,args[0])
                try:
                    os.execve(program, args, os.environ)# exec program
                except FileNotFoundError:                # ...expected
                    pass                             # ...fail quietly
          os.write(2,("It was an error running %s\n" %
                           program).encode())   # terminate with error
else:
    childPidCode = os.wait()
    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
             (pid, rc)).encode())
    os.write(1, ("Parent: Child %d terminated with exit code %d\n"
                 %  childPidCode).encode())

        
        
