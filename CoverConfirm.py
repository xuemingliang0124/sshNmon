#coding:utf-8
from tkinter import messagebox

class CoverConfirm:
    def confirmDialog(self,ana_path):
        if messagebox.askyesno('覆盖文件', str(ana_path)+'文件已存在，是否覆盖？'):
            return 1
        else:
            return '分析取消,请修改保存路径后重试！'
