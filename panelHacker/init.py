import nuke
import os

# This just ensures that the current directory is in the nuke path and that we don't add it multiple times
if currentDir := os.path.dirname(__file__) not in nuke.pluginPath():
    nuke.tprint(f'Adding {currentDir} to nuke path')
    nuke.pluginAddPath(currentDir)
