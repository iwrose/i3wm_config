#!/usr/bin/env python3
import layoutparse as lp
import i3IPCmsg as im
import time

class LayoutControl:
    def __init__(self,workspaceName):
        self.i3xx = im.I3Msg();
        self.workspaceid = None;
        self.workspaceName = workspaceName;

    def initWorkspaceid(self):
        self.workspaceid = self.i3xx.getCurrentWSID(self.workspaceName);
    
        #Init Workspace Layout
    def initWSLayoutByXML(self,layout):
        self.i3xx.sendCmd("workspace "+str(self.workspaceName))
        self.initWorkspaceid()
        workspace = lp.getWorkspace(layout);
        screens = lp.getScreen(workspace);
        for screen in screens:
            #若该screen存在,且信息准确,则继续下一步
            if self.isScreenValid(screen):
                self.initLayoutAndApps(screen);

    def isScreenValid(self,screen):
        #利用i3ipc查询信息,对比screen参数准确,且不为空
        return True;

    def initLayoutAndApps(self,screen):
        for node in screen.childNodes:
            if lp.isNodeContainer(node):
                print("N: is about container",node)
                self.initLayoutAndApps(node);
                self.i3xx.focusParent();
                #time.sleep(3)
            elif lp.isNodeWindow(node):
                #focus()
                print("N: is about window",node)
                #1. 确定分割方向,横向还是纵向
                orientation = lp.getRightOrientation(node);
                self.i3xx.setSplitOrientation(orientation);
                #time.sleep(2)
                #2. 打开对应的APP
                appname = lp.getAppName(node);
                appid = lp.getAppID(node);
                self.i3xx.openAppAndMark(appname,appid,self.workspaceid);
            

    def refreshWSLayoutByXML(self,layout):
        self.i3xx.sendCmd("workspace "+str(self.workspaceName))
        self.initWorkspaceid()
        self.i3xx.moveAllApps(self.workspaceid)
        workspace = lp.getWorkspace(layout);
        screens = lp.getScreen(workspace);
        for screen in screens:
            #若该screen存在,且信息准确,则继续下一步
            if self.isScreenValid(screen):
                self.refreshLayoutAndApps(screen);

    def refreshLayoutAndApps(self,screen):
        for node in screen.childNodes:
            if lp.isNodeContainer(node):
                print("N: is about container",node)
                self.refreshLayoutAndApps(node);
                self.i3xx.focusParent();
                #time.sleep(3)
            elif lp.isNodeWindow(node):
                #focus()
                print("N: is about window",node)
                #1. 确定分割方向,横向还是纵向
                orientation = lp.getRightOrientation(node);
                self.i3xx.setSplitOrientation(orientation);
                #time.sleep(2)
                #2. 打开对应的APP
                appname = lp.getAppName(node);
                appid = lp.getAppID(node);
                print(":::::::",appid,"  ",appname)
                self.i3xx.moveAppAndMark(appname,appid,self.workspaceid);
    


#time.sleep(2)




