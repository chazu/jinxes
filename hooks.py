## Keypress Functions ###################################

def quitApp(app, **kwargs):
    app.quit = True

def scrollFocusDown(app, **kwargs):
    if (app.display.focused_widget.buffer.scroll["currentLine"] <
        app.display.focused_widget.buffer.scroll["maxCurrentLine"]):
        app.display.focused_widget.buffer.scroll["currentLine"] += 1

def scrollFocusUp(app, **kwargs):
    if (app.display.focused_widget.buffer.scroll["currentLine"] > 0):
        app.display.focused_widget.buffer.scroll["currentLine"] -= 1

def incrementAppFocus(app, **kwargs):
    app.display.focused_widget = app.display.focus_order[ \
        (app.display.focus_order.index(
                app.display.focused_widget
                ) + 1) % len(app.display.focus_order)
        ]

def decrementAppFocus(app, **kwargs):
    app.display.focused_widget = app.display.focus_order[ \
        (app.display.focus_order.index(
                app.display.focused_widget
                ) + 2) % len(app.display.focus_order)
        ]

def maximizeFocusWidget(app, **kwargs):

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

def restoreFocusWidget(app, **kwargs):

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
# WIDGET HOOKS

def appendKeyToTextBuffer(widget, **kwargs):
    widget.buffer.add_text(kwargs["key"])
    widget.mark_dirty()

def sendLocalCommand(widget, **kwargs):
    send = widget.buffer.get_text()
    widget.app.local_event_dispatch.emit_message({
            "channel": "command",
            "body": send
            })
    widget.buffer.clear()
    widget.mark_dirty()
#########################################################
# MESSAGE HOOKS

def printLocalCommand(widget, **kwargs):
    widget.buffer.add_text(kwargs["message"]["body"])
    widget.mark_dirty()

def appendBodyToTextBuffer(widget, **kwargs):
    widget.buffer.add_text(kwargs["message"]["body"])
    widget.mark_dirty()
