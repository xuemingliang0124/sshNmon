#coding:utf-8
import paramiko
import os
import re
class downloadResult:
    def ssh_linux_to_win_result(self, host, username, password, nmonpath,winpath):
        '''从Linux服务器下载文件到本地

        Args:
            linuxpath: 文件在服务器上的路径及名字
            winpath: 文件下载到本地的路径及名字

        '''
        linuxpath = nmonpath
        try:
            tran = paramiko.Transport(host, 22)
            tran.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(tran)
            if os.path.isdir(winpath):  # 判断本地参数是目录还是文件
                a = sftp.listdir(linuxpath)
                if not re.search('\.nmon',str(a),flags=0):
                    return 'No such file or directory!'
                for f in a:  # 遍历远程目录
                    if f == 'nmon':
                        pass
                    else:
                        sftp.get(os.path.join(linuxpath + f), os.path.join(winpath + f))  # 下载目录中文件
            else:
                sftp.get(linuxpath, winpath)  # 下载文件
        except Exception as e:
            return e
        tran.close()
        return str(host)+' download suceessful!'