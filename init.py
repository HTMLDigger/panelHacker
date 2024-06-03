import nuke
import os.path

nuke.pluginAddPath(currentDir := os.path.dirname(__file__))
nuke.tprint(f'Adding {currentDir} to nuke path')
