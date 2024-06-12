import nuke
import traceback
import panelHacker
import panels.scriptEditor
import panels.preferencePanel

try:
    nuke.tprint('Importing and initializing Panel Hacker')
    panelHacker.start()
    nuke.tprint('Registering Panels')
    hacker = panelHacker.PanelHacker()
    hacker.registerPanel(panels.preferencePanel.Preferences)
    hacker.registerPanel(panels.scriptEditor.ScriptEditor)
    nuke.tprint('Panel Hacker initialized')

# Open-ended error as we don't know what the error might be, but we ensure to print it out
except:
    nuke.tprint('Failed to import and initialize Panel Hacker')
    error = traceback.format_exc()
    for line in error.split('\n'):
        nuke.tprint(f'[Panel Hacker Error] {line}')
