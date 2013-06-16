# TARTENGINE

## Syntax

The TARTENGINE uses json documents to define user interfaces, including widget appearance, layout and data sources.
JSON files can contain one or more widgets, i.e. the document root can be an object describing a single widget, or a list of widgets.

### Nesting Widgets

Widgets can be nested within other widgets. Child widgets should be contained within the "children" key of their parent widget.

### Required Widget Fields

All widgets must have the following fields:
    - NONE SO FAR

### Optional widget fields

    - Border  - Boolean
    - Height - Integer
    - Width - Integer
    - Text - Text to be shown in the widget
    - Name - A name for the widget (unused currently)
    - widget - The type of widget

#### Border Options

     NOTE: This is currently unimplemented.

     { character : "X",
       bgColor: "RED",
       fgColor: "BLUE",
     }