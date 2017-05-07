import os
import sys
import time
import easygui
from subprocess import call

action = sys.argv[1]

if os.getuid() == 0:
    time.sleep(0.5)
    print ("Starting...")
    sys.stdout.flush()
    time.sleep(0.5)
    print ("Elevating my privleges!")
else:
    print ("Elevate my privileges!")
    sys.exit(1)

directory_env = '/etc'
directory_acq  = '/etc/apt/apt.conf.d' 
environment = os.environ
env = environment['http_proxy'] or environment['https_proxy'] or environment['ftp_proxy'] or environment['HTTP_PROXY'] or environment['HTTPS_PROXY'] or environment['FTP_PROXY']

if (action == "set"):
    if env is not '':
        if easygui.ccbox("Previous proxies configuartion already exists. Override?", title="Warning"):
            env = ''
        else:
            pass
    if env is '':
        proxy = 'http://myproxy.mydomain:8080/'
        
        #If you need to authenticate on your proxy, you need to stick a <username:password> in front of the proxy server address
        #For instance
        #http://myusername:mypassword@myproxy.mydomain.com:8080/

        noproxy = '"my, no, proxy, list"'
        protocols = ['http_proxy=','https_proxy=','ftp_proxy=','no_proxy=','HTTP_PROXY=','HTTPS_PROXY=','FTP_PROXY=','NO_PROXY=']
        acquire = ['http','ftp','https']

        target_env = open(os.path.join(directory_env, "environment"), "w")
        target_acq = open(os.path.join(directory_acq, "95proxies"),"w") 
        
        target_env.write('PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"')
        target_env.write('\n')
        for i in protocols:
            target_env.write(i)
            if i is 'no_proxy=' or i is 'NO_PROXY=':
                target_env.write(noproxy)
            else:
                target_env.write(proxy)
            target_env.write('\n')
        
        for i in acquire:
            acq = 'Acquire::' + i + '::proxy' + ' ' + '"' + i + proxy[4:] + '"' + ';' + '\n'
            target_acq.write(acq)
        
        target_env.close()
        target_acq.close()

        time.sleep(1)
        easygui.msgbox("Congratulations!", title="Success")
        print ("Done!") 

elif (action == 'unset'):
    if env is '':
        easygui.msgbox("No proxy configured on the system. Please check your internet connection.", title="Error")
        print ("Error!")
    else:
        protocols = ['http_proxy=','https_proxy=','ftp_proxy=','no_proxy=','HTTP_PROXY=','HTTPS_PROXY=','FTP_PROXY=','NO_PROXY=']
        
        target_env = open(os.path.join(directory_env, "environment"), "w")
        target_acq = os.path.join(directory_acq, "95proxies")

        target_env.write('PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"')
        target_env.write('\n')
        for i in protocols:
            target_env.write(i)
            target_env.write('\n')
        target_env.close()

        command = 'rm -rf ' + str(target_acq)
        call(command, shell = True)
        time.sleep(1)
        print ("Done!")
else:
    easygui.msgbox("This script supports only two options! Set & Unset.", title="Error")
    sys.exit(1)