#coding:utf-8

import paramiko
import time
class DeleteResult:
    def execute(self,host,username,password,nmonpath):
        try:
            tran=paramiko.Transport(host,22)
            tran.connect(username=username,password=password)
            channel=tran.open_session()
            channel.get_pty()
            channel.invoke_shell()
            command=[]
            command.append('cd '+nmonpath)
            command.append('rm -rf *.nmon')
            for i in range(len(command)):
                send_str=command[i]+'\n'
                channel.send(send_str)
            return host+' '+'Result delete successful!'
        except Exception as e:
            return e
