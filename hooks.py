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

def maximizeFocusWidget(app):

    if not app.display.focused_widget. \
            specifies("maximized", True, ["custom"]):
        app.display.focused_widget.cache_state_at_path(["anchor"])
        app.display.focused_widget.cache_state_at_path(["height"])
        app.display.focused_widget.cache_state_at_path(["width"])

        app.display.focused_widget.move_anchor(0, 0)
        app.display.focused_widget.resize(
            app.spec["app"]["height"],
            app.spec["app"]["width"]
            )
        app.display.focused_widget.current_state["custom"] \
            ["maximized"] = True
        app.display.focused_widget.mark_dirty()

def restoreFocusWidget(app):

    app.display.focused_widget.restore_state_from_cache(["anchor"])
    app.display.focused_widget.restore_state_from_cache(["height"])
    app.display.focused_widget.restore_state_from_cache(["width"])

    app.display.focused_widget.resize(
        app.display.focused_widget.current_state["height"],
        app.display.focused_widget.current_state["width"]
        )
    app.display.focused_widget.current_state["custom"] \
        ["maximized"] = False

    app.display.focused_widget.mark_dirty()

#########################################################

def printWidgetSpec(widget):
    print(widget.spec)

def printFoo(widget):
    raise Exception
