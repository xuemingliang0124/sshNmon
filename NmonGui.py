# coding:utf-8


from tkinter import *
import os
from openIpList import OpenFile
import xlrd
from xlutils.copy import copy
from parseResult import parseResult
from  CoverConfirm import CoverConfirm


class Gui:
    def __init__(self,master):
        pwd=os.getcwd()
        url=os.path.join(pwd+'\\temp.xls')
        excelfile = xlrd.open_workbook(url)
        sheet = excelfile.sheet_by_index(0)
        self.frm_top1=Frame(master)
        self.frm_top2=Frame(master)
        self.frm1=Frame(self.frm_top1)
        self.frm2=Frame(self.frm_top1)
        self.frm3=Frame(self.frm_top2)
        self.result = StringVar()
        self.nmon_path=StringVar()
        self.iplist_path=StringVar()
        self.result_path=StringVar()
        self.analysis_path=StringVar()
        self.nmon_path.set(sheet.cell_value(0,1))
        self.iplist_path.set(sheet.cell_value(0,0))
        self.result_path.set(sheet.cell_value(0,2))
        self.analysis_path.set(sheet.cell_value(0,3))
        Button(self.frm1, text='启动nmon', bg='green',command=self.upnmon).pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(self.frm1, text='结束nmon进程',bg='red',command=self.killnmon).pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(self.frm1, text='下载nmon结果',command=self.downloadRes).pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(self.frm1, text='删除nmon结果',command=self.deleteRes).pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(self.frm1, text='上传nmon',command=self.uploadNmon).pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(self.frm1, text='下载nmon').pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(self.frm1, text='分析结果文件',command=self.parseResult).pack(side=TOP, anchor=W, fill=X, expand=YES)
        Label(self.frm2, text='IPlist 位置').pack(side=TOP,anchor=W)
        self.iplist_path = Entry(self.frm2, textvariable=self.iplist_path)
        self.iplist_path.pack(side=TOP,fill=X, anchor=W)
        Label(self.frm2, text='下载结果保存位置').pack(side=TOP, anchor=W)
        self.result_path = Entry(self.frm2, textvariable=self.result_path)
        self.result_path.pack(side=TOP, fill=X, anchor=W)
        Label(self.frm2,text='本地nmon位置').pack(side=TOP,anchor=W)
        self.nmonpath=Entry(self.frm2,textvariable=self.nmon_path)
        self.nmonpath.pack(side=TOP, anchor=W, fill=X)
        Label(self.frm2, text='分析结果保存位置').pack(side=TOP, anchor=W)
        self.analysis_path = Entry(self.frm2, textvariable=self.analysis_path)
        self.analysis_path.pack(side=TOP, anchor=W, fill=X)
        self.res=Text(self.frm3)
        self.res.pack(side=LEFT,fill=X,expand=YES)
        self.frm1.pack(side=LEFT, fill=BOTH, expand=YES)
        self.frm2.pack(side=LEFT, fill=BOTH, expand=YES)
        self.frm3.pack(side=LEFT, fill=BOTH, expand=YES)
        self.frm_top1.pack(side=TOP,fill=BOTH,expand=YES)
        self.frm_top2.pack(side=TOP,fill=BOTH,expand=YES)
    def upnmon(self):
        self.savePath()
        self.res.delete(0.0,END)
        self.res.update()
        iplist=self.iplist_path.get()
        step='up'
        result=OpenFile().openfile(iplist,step)
        for i in result:
            self.res.insert(END,(str(i)+'\n'))
    def killnmon(self):
        self.savePath()
        self.res.delete(0.0, END)
        self.res.update()
        iplist=self.iplist_path.get()
        step='kill'
        result=OpenFile().openfile(iplist,step)
        for i in result:
            self.res.insert(END,(str(i)+'\n'))
    def downloadRes(self):
        self.savePath()
        self.res.delete(0.0, END)
        self.res.update()
        iplist=self.iplist_path.get()
        winpath=self.result_path.get()
        step='download_res'
        result=OpenFile().openfile(iplist,step,winpath)
        for i in result:
            self.res.insert(END,(str(i)+'\n'))
    def deleteRes(self):
        self.savePath()
        self.res.delete(0.0, END)
        self.res.update()
        iplist = self.iplist_path.get()
        step = 'delete_res'
        result = OpenFile().openfile(iplist, step)
        for i in result:
            self.res.insert(END,(str(i)+'\n'))
    def uploadNmon(self):
        self.savePath()
        self.res.delete(0.0, END)
        self.res.update()
        iplist = self.iplist_path.get()
        winpath=self.nmonpath.get()
        step = 'upload_nmon'
        result = OpenFile().openfile(iplist, step,winpath)
        for i in result:
            self.res.insert(END,(str(i)+'\n'))
    def parseResult(self):
        self.savePath()
        self.res.delete(0.0, END)
        self.res.update()
        res_path=self.result_path.get()
        ana_path=self.analysis_path.get()
        if os.path.exists(ana_path):
            self.result=CoverConfirm().confirmDialog(ana_path)
            if self.result!=1:
                self.res.insert(END, (self.result+ '\n'))
            else:
                parseResult(res_path, ana_path)
                self.result = '结果分析完成，文件路径：' + str(ana_path)
                self.res.insert(END, (self.result + '\n'))
        else:
            parseResult(res_path,ana_path)
            self.res='结果分析完成，文件路径：'+str(ana_path)
            self.result.set(self.res)
    def savePath(self):
        iplist_path=self.iplist_path.get()
        nmon_path=self.nmon_path.get()
        winpath=self.result_path.get()
        analysis_path=self.analysis_path.get()
        pwd = os.getcwd()
        url = os.path.join(pwd + '\\temp.xls')
        excelfile = xlrd.open_workbook(url)
        excelfilenew = copy(excelfile)
        sheet = excelfilenew.get_sheet(0)
        sheet.write(0, 0, iplist_path)
        sheet.write(0, 1, nmon_path)
        sheet.write(0, 2, winpath)
        sheet.write(0,3,analysis_path)
        excelfilenew.save(url)
    def setResultLabel(self,results):
        self.result.set(results)
root = Tk()
root.title('nmon')
root.geometry('500x300')
Gui(root)
root.mainloop()