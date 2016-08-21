#!/usr/bin/env python3
import layoutcontrol as lc
from argparse import ArgumentParser

parser = ArgumentParser(description="""Choose to init the Programming Workspace or Just refresh Programming Workspace.
""")
parser.add_argument('-t', type=str)

args=parser.parse_args()
type = args.t
if type=="init":
    lc.LayoutControl("8:").initWSLayoutByXML('/home/negatlov/.config/i3/smartI3config/music_layout.xml')
elif type=="refresh":
    lc.LayoutControl("8:").refreshWSLayoutByXML('/home/negatlov/.config/i3/smartI3config/music_layout.xml')
else:
    print("Arguments is error!")
        
