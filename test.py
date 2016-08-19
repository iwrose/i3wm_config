#!/usr/bin/env python3

import i3ipc
# Get the conection Object
i3 = i3ipc.Connection()
wspaces= i3.get_workspaces()




# Print the name of the focused window
focused = i3.get_tree().find_focused()
print('Focused window %s is on workspace %s' %
      (focused.name, focused.workspace().name))



