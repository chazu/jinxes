## Keypress Functions ###################################

def quitApp(app):
    app.quit = True

def scrollFocusDown(app):
    if (app.focused_widget.scroll["currentLine"] <
        app.focused_widget.scroll["maxCurrentLine"]):
        app.focused_widget.scroll["currentLine"] += 1

def scrollFocusUp(app):
    if (app.focused_widget.scroll["currentLine"] > 0):
        app.focused_widget.scroll["currentLine"] -= 1

#########################################################
