About
-----
This simple program will switch to the given i3 workspace.

If you have (exactly) two active outputs, the activated workspace will be moved to the focused output and the workspace that occupied that output will be moved to the second output.

In any other setup (one, three or more outputs) it will behave exactly the same as the default i3 behavior.

Usage
-----
```bash
pi3-switch WORKSPACE_NAME
```

Installation
------------
Install using [pipsi](https://github.com/mitsuhiko/pipsi) (recommended) or pip

```bash
pipsi install pi3-switch
```

Add keybindings to ~/.config/i3/config and reload i3

```bash
bindsym $mod+1 exec pi3-switch 1
bindsym $mod+2 exec pi3-switch 2
bindsym $mod+3 exec pi3-switch 3
bindsym $mod+4 exec pi3-switch 4
bindsym $mod+5 exec pi3-switch 5
bindsym $mod+6 exec pi3-switch 6
bindsym $mod+7 exec pi3-switch 7
bindsym $mod+8 exec pi3-switch 8
bindsym $mod+9 exec pi3-switch 9
bindsym $mod+0 exec pi3-switch 10
```

Credits
-------
Thanks to Travis Finkenauer for an inspiration ([i3-wk-switch](https://github.com/tmfink/i3-wk-switch)) and Tony Crisci for an easy-to-use i3 python library ([i3ipc-python](https://github.com/acrisci/i3ipc-python)).
