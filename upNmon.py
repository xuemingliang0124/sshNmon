#coding=utf-8
import time
import paramiko
import re
class upNmon:
    def execute(self,host,username,password,nmonPath,command):
        try:
            tran = paramiko.Transport(host, 22)
            tran.connect(username=username, password=password)
            channel = tran.open_session()
            channel.get_pty()
            channel.invoke_shell()
        except Exception as e:
            return e
        date=time.strftime('%Y%m%d',time.localtime(time.time()))
        times=time.strftime('%H%M',time.localtime(time.time()))
        command=command[0].split('-F')
        upnmon=[command[0]+'-F '+host+'_'+date+'_'+times+'.nmon'+command[1]]
        firstCommand=['cd '+nmonPath]
        command=firstCommand+upnmon
        for i in range(len(command)):
            send_str=command[i]+'\n'
            channel.send(send_str)
            result=''
            while True:
                time.sleep(0.5)
                res = channel.recv(65535).decode('utf8')
                result += res
                if res.endswith('# ') or res.endswith('$ '):
                    result=re.sub('\n.+$','',result,flags=0)
                    break
        tran.close()
        return result