## Keypress Functions ###################################

def quitApp(app):
    app.quit = True

def scrollFocusDown(app):
    if (app.display.focused_widget.scroll["currentLine"] <
        app.display.focused_widget.scroll["maxCurrentLine"]):
        app.display.focused_widget.scroll["currentLine"] += 1

def scrollFocusUp(app):
    if (app.display.focused_widget.scroll["currentLine"] > 0):
        app.display.focused_widget.scroll["currentLine"] -= 1

#########################################################
