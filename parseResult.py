import os
import xlwt
from xlutils.copy import copy
import xlrd
import re
class parseResult:
    cpu=[]
    cpuwait=[]
    diskwrite=[]
    diskread = []
    mem=[]
    def __init__(self,result_path,analysis_path):
        if os.path.isdir(result_path):
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet('sheet1')
            sheet.write(0, 0, 'IP')
            sheet.write(0, 1, 'CPU(%)')
            sheet.write(0, 4, 'CPUWait(%)')
            sheet.write(0, 3, 'IORead+Write(KB/秒)')
            sheet.write(0, 2, 'MEM(%)')
            now_dir=os.getcwd()
            filename=re.search('\w+\.\w+$',analysis_path,flags=0).group()
            ana_dir=re.sub('\w+\.\w+$','',analysis_path)
            os.chdir(ana_dir)
            workbook.save(filename)
            j=0
            for i in os.listdir(result_path):
                j+=1
                ip=re.search('\d+\.\d+\.\d+\.\d+',i,flags=0).group()
                file=open(result_path+i,'r',encoding='gb18030',errors='ignore')
                self.lines=file.readlines()
                res_cpu=self.getCpu()
                res_disk=self.getDisk()
                res_mem=self.getMem()
                workbook=xlrd.open_workbook(analysis_path)
                workbooknew=copy(workbook)
                sheet=workbooknew.get_sheet(0)
                sheet.write(j, 0, ip)
                sheet.write(j,1,res_cpu[0])
                sheet.write(j, 4, res_cpu[1])
                sheet.write(j, 3, res_disk)
                sheet.write(j, 2, res_mem)
                workbooknew.save(analysis_path)
            os.chdir(now_dir)
    def getCpu(self):
        for i in self.lines:
            i=i.split(',')
            if 'CPU_ALL' in i[0] and 'CPU Total' not in i[1]:
                self.cpu.append(float(i[2])+float(i[3]))
                self.cpuwait.append(float(i[4]))
        cpu_avg=round(sum(self.cpu)/len(self.cpu),2)
        cpuwait=round(sum(self.cpuwait)/len(self.cpuwait),2)
        return cpu_avg,cpuwait
    def getDisk(self):
        for i in self.lines:
            i=i.split(',')
            if 'DISKREAD' in i[0] and 'Disk Read' not in i[1]:
                self.diskread.append(sum(map(float,i[2:9])))
        for i in self.lines:
            i=i.split(',')
            if 'DISKWRITE' in i[0] and 'Disk Write' not in i[1]:
                self.diskwrite.append(sum(map(float,i[2:9])))
        disk=round(sum(self.diskread)/len(self.diskread)+sum(self.diskwrite)/len(self.diskwrite),2)
        return disk
    def getMem(self):
        for i in self.lines:
            i=i.split(',')
            if 'MEM' in i[0] and 'Memory MB' not in i[1]:
                self.mem.append((float(i[2])-float(i[6])-float(i[11])-float(i[14]))/float(i[2]))
        mem=round(sum(self.mem)/len(self.mem),4)*100
        return mem