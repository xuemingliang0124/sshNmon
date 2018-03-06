#coding=utf-8

import time
import re
import paramiko

class killNmon:
    def execute(self,host,username,password):
        try:
            tran = paramiko.Transport(host, 22)
            tran.connect(username=username, password=password)
            channel = tran.open_session()
            channel.get_pty()
            channel.invoke_shell()
        except Exception as e:
            return str(host)+' '+str(e)
        send_str='ps -ef | grep nmon\n'
        channel.send(send_str)
        result=''
        while True:
            time.sleep(0.5)
            res = channel.recv(65535).decode('utf8')
            result += res
            if res.endswith('# ') or res.endswith('$ '):
                break
        start=re.search('.+\n.+\n+.+\n',result).group()
        end=re.search('\[.+$',result).group()
        all_nmon_ps=result.split(start)[1].split(end)[0]
        nmon_ps=all_nmon_ps.split('\n')[0]
        if re.search('grep nmon',nmon_ps):
            return str(host)+" nmon is not running!"
        pid=re.search('\d+',nmon_ps).group()
        print(pid)
        try:
            killCommand='kill -9 '+pid+'\n'
            channel.send(killCommand)
        except Exception as e:
            return str(host)+str(e)
        time.sleep(0.5)
        result = channel.recv(65535).decode('utf8')
        result=re.search('.+\n',result,flags=0).group()
        return all_nmon_ps+result+str(host)+' nmon进程kill成功!'



