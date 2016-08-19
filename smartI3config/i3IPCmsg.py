#!/usr/bin/env python3

import i3ipc
import time
import threading
import os
import subprocess
# 
class I3Msg:
    def __init__(self):
        self.i3 = i3ipc.Connection()
        self.focusedID = None;


    def getCurrentWSID(self,name):
        wss = self.i3.get_tree().workspaces()
        cws = None;
        for ws in wss:
            print("workspace", ws.id)
            if str(ws.name) == str(name):
                cws = ws;
                break;
        return cws.id

        
    def focus(self,app_name):
        app_class = getAppClass(app_name)
        self.i3.command('[con_mark="^focuscon$"] focus')

    def setSplitOrientation(self,orientation):
        if orientation == 'h':
            self.i3.command('split horizontal')
            print("self.i3.command('split horizontal')")
        elif orientation == 'v':
            self.i3.command('split vertical')
            print("self.i3.command('split vertical')")
        else:
            print("参数错误")

    def sendCmd(self,cmd):
        self.i3.command(cmd)

    def focusParent(self):
        print("33333333333333333", self.focusedID);        
        app = self.i3.get_tree().find_by_id(self.focusedID)
        parentid = app.parent.id
        cmd = '[con_id='+ str(parentid)+'] focus'
        print("开发focusParent")
        print("当前的focused变量是",self.focusedID)
        print("当前正focuse在",app.name)
        print("正在focus",app.name,"的父节点",parentid)
        self.focusedID = parentid
        self.i3.command(cmd)
        while(not (self.isFocusRight(parentid))):
            self.i3.command(cmd)
        print("完成focusparen",cmd)
        
    def isFocusRight(self,focusid):
        fapp = self.i3.get_tree().find_focused()
        if fapp.id == focusid:
            return True;
        else:
            return False;
        
        
    def openingNewApp(self,appname,workspaceid):
        print("初始:")
        a = self.getAppsIDInCWS(workspaceid);
        #print(list(a))
        #subprocess.run(appname+"&",shell=True, check=True)
        self.i3.command("exec "+str(appname))
        newapps = None;
        print("正在准备打开",appname)
        time.sleep(0.1)
        while(True):

            b = self.getAppsIDInCWS(workspaceid);
            #print(list(b))
            newapps = set(b).difference(set(a))
            #print("哈哈哈",list(newapps))
            if len(newapps) != 0:
                break;
        if len(newapps) >1:
            print("严重错误.....fucking")
        self.focusedID = list(newapps)[0]

    def getAppsIDInCWS(self,workspaceid):
        leaves = self.i3.get_tree().leaves()
        cons = [];
        for app in leaves:
            if app.workspace().id == workspaceid:
                #print(app.id," ", app.name, " ", app.workspace().id)
                cons.append(app.id);
        return cons
        

            
    def getAppsInCWS(self,workspaceid):
        leaves = self.i3.get_tree().leaves()
        cons = [];
        for app in leaves:
            if app.workspace().id == workspaceid:
                #print(app.id," ", app.name, " ", app.workspace().id)
                cons.append(app);
        return cons
            

    def openAppAndMark(self,app,id,workspaceid):
        #cmd1 = '[con_mark="^focuscon$"] focus; exec '+app;
        #cmd1 = 'exec '+str(app)
        print("开始openAppAndMark")

        pcmd = '[con_id='+ str(self.focusedID) +'] focus'
        
        #print("opening ",app,"id is ", id)
        print("focuse",pcmd)
        self.i3.command(pcmd)

        self.openingNewApp(app,workspaceid)
        #self.i3.command(cmd1)
        #time.sleep(2)

        cmd = "[con_id=" + str(self.focusedID) + "] mark --add "+str(id);
        print("-----------------",cmd)
        self.i3.command(cmd)
        #time.sleep(4)
        #self.i3.command(cmd2)
        print("opened win is added focuscon mark")
        #time.sleep(10)

    def moveAllApps(self,workspaceid):
        ws = self.i3.get_tree().find_by_id(workspaceid)
        cmd = '[class=".*" workspace='+ws.name+'] move to workspace 9'
        self.i3.command(cmd)

    def moveAppAndMark(self,app,mark,workspaceid):
        #找到id对应的app,如果存在,则移动,不存在,则重新打开一个程序,并mark
        ws = self.i3.get_tree().find_by_id(workspaceid)
        a = self.getAppsIDInCWS(workspaceid);
        cmd = "[con_mark="+str(mark)+" workspace=9] move to workspace "+ws.name
        rst = self.i3.command(cmd)
        print("11111111111111111111111",rst)
        if not rst[0]['success']:
            self.openAppAndMark(app,mark,workspaceid)
        else:
            print("2222222222222")
            while(True):            
                b = self.getAppsIDInCWS(workspaceid);
                newapps = set(b).difference(set(a))
                if len(newapps) != 0:
                    break;
            if len(newapps) >1:
                print("严重错误.....fucking")
            self.focusedID = list(newapps)[0]



    #def isMarkAppExist(self,mark,workspaceid):
     #   apps = self.getAppsInCWS(workspaceid);
      #  for app in apps:
            
        
        

    def isNewAppFocused(self):
        self.i3.command('[con_mark="^focuscon$"] focus');
        focused = self.i3.get_tree().find_focused();
        for mark in focused.marks:
            if mark == "focuscon":
                return False;
        return True;
        

    def test(self):
        #os.system("firefox &")
        #subprocess.run("firefox&",shell=True, check=True)
        #time.sleep(5)
        #self.i3.command("workspace 7");
        #time.sleep(1)
        #self.i3.command("append_layout /home/negatlov/.config/i3/smartI3config/placeholder.json")
        
        
        #self.i3.command("append_layout /home/negatlov/.config/i3/Programming-Workspace.json")
        
        cons = []
        classed = self.i3.get_tree().leaves()
        for app in classed:
            if app.workspace().id == w.id:
                #print(app.id," ", app.name, " ", app.workspace().id)
                cons.append(app);
    
    '''
    def openAppAndMark(self,app,id):
        self.id = id;
        self.i3.on("window::new", self.on_window_new)
        t1 = threading.Thread(target=lambda:self.startMain,args=())
        t1.setDaemon(True);
        t1.start();
        time.sleep(1)
        cmd1 = 'unmark focuscon; exec '+app
        self.i3.command(cmd1)
        print(cmd1)
        #self.i3.command(cmd2)
        
    def startMain(self):
        print("进入到多线程了")
        self.i3.main()
    
        
    # Dynamically name your workspaces after the current window class
    def on_window_new(self,x,y):
        #focused = self.i3.get_tree().find_focused()
        cmd2 = 'mark --add focuscon; mark --add '+self.id;
        print(cmd2)
        self.i3.command(cmd2)
        #ws_name = "%s:%s" % (focused.workspace().num, focused.window_class)
        #self.i3.command('rename workspace to "%s"' % ws_name)
        self.i3.main_quit()
    '''



# Start the main loop and wait for events to come in.

#x = I3Msg()
#x.getCurrentWSID()
#print(x.getCurrentWSID(2))
#x.test()
#x.openAppAndMark("xterm",3)
