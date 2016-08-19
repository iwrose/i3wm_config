#!/usr/bin/env python3

# This py is using for parsing layout.xml file,
import xml.dom.minidom as DOM
from xml.dom.minidom import Node
import sys

def remove_blanks(node):
    for x in node.childNodes:
        if x.nodeType == Node.TEXT_NODE:
            if x.nodeValue:
                x.nodeValue = x.nodeValue.strip()
        elif x.nodeType == Node.ELEMENT_NODE:
            remove_blanks(x)

def getWorkspace(filepath):
    root = DOM.parse(filepath);
    remove_blanks(root)
    root.normalize()
    return root.documentElement;

#screen is a also a bigger container
def getScreen(workspace):
    return workspace.childNodes;

def isNodeContainer(element):
    if element.nodeName == "container":
        return True;
    else:
        return False;
    
def isNodeWindow(element):
    if element.nodeName == "window":
        return True;
    else:
        return False;


def isNodeScreen(node):
    if node.nodeName == "screen":
        return True;
    else:
        return False;
    
rightNode = None;
def getContainerTrueWindow(win):
    pNode=win.parentNode;
    #print("this Pnode:",pNode.firstChild)
    #print("this Win:",win)
    if isNodeScreen(pNode) or not(pNode.firstChild.isSameNode(win)):
        global rightNode;
        rightNode = win;
    else:
        getContainerTrueWindow(pNode)

def getRightOrientation(win):
    getContainerTrueWindow(win);
    global rightNode;
    parent = rightNode.parentNode;
    orientation = parent.getAttribute("orient")
    return orientation;


def getAppName(win):
    return win.getAttribute("exename");

def getAppID(win):
    return win.getAttribute("name");

