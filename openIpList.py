#coding:utf-8
import xlrd
from upNmon import upNmon
from downloadResult import downloadResult as downres
from killNmon import killNmon
from uploadNmon import uploadNmon
from deleteResult import DeleteResult
class OpenFile:
    def openfile(self,ipListPath,step,winpath=None):
        self.winpath=winpath
        excelfile = xlrd.open_workbook(ipListPath)
        sheet = excelfile.sheet_by_index(0)
        ip = sheet.col_values(0)
        res=[]
        for i in range(1,len(ip)):
            host = sheet.cell_value(i, 0)
            username = sheet.cell_value(i, 1)
            password = sheet.cell_value(i, 2)
            nmonpath = sheet.cell_value(i, 3)
            command = [sheet.cell_value(i, 5)]
            if step == 'up':
                res.append(upNmon().execute(host,username,password,nmonpath,command))
            elif step=='kill':
                res.append(killNmon().execute(host,username,password))
            elif step=='download_res':
                res.append(downres().ssh_linux_to_win_result(host, username, password, nmonpath,winpath))
            elif step=='delete_res':
                res.append(DeleteResult().execute(host,username,password,nmonpath))
            elif step=='upload_nmon':
                res.append(uploadNmon().ssh_win_to_linux(host,username,password,nmonpath,self.winpath))
        return res
