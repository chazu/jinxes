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

def incrementAppFocus(app):
    app.display.focused_widget = app.display.focus_order[ \
        (app.display.focus_order.index(
                app.display.focused_widget
                ) + 1) % len(app.display.focus_order)
        ]

def decrementAppFocus(app):
    app.display.focused_widget = app.display.focus_order[ \
        (app.display.focus_order.index(
                app.display.focused_widget
                ) + 2) % len(app.display.focus_order)
        ]

#########################################################
