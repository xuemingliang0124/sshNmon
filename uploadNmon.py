import os
import paramiko
import time
class uploadNmon:
    def ssh_win_to_linux(self, host, username, password, nmonpath, winpath):
        '''从windows向linux服务器上传文件
    
        Args:
            winpath: 要上传的文件在本地的路径及位置
            linuxpath: 文件要上传至服务器的路径及名字
        '''
        nmon = nmonpath+'nmon'
        try:
            ssh_tran = paramiko.Transport(host, 22)
            ssh_tran.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(ssh_tran)
            sftp.put(winpath, nmon)
            ssh_tran.close()
            tran = paramiko.Transport(host, 22)
            tran.connect(username=username, password=password)
            channel = tran.open_session()
            channel.get_pty()
            channel.invoke_shell()
            channel.send('cd '+nmonpath+'\n')
            channel.send('chmod 777 nmon\n')
            channel.send('ll')
            res=channel.recv(65535).decode('utf8')
            print(res)
            # time.sleep(0.5)
            # tran.close()
            return str(host)+' ' + ' upload successful!'
        except Exception as e:
            return str(host)+' '+str(e)