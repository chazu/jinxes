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

## Events

### Subscription Format

Since subscriptions are nested under local or remote, there is no need to specify this in the subscription data structure.


{
  "exchange"
}

## Internals

### Builders

When constructing a widget from the specified JSON, the engine will attempt to merge the relevant portions of the specification dictionary into a dictionary which specifies default values. This way, those values you specify will overwrite the defaults and become part of the widget instance's state, while the defaults will remain for any optional parameters you leave unspecified.

## TODO

 - Scrolling/buffers
 - key bindings/event loop
 - focus
 - widgets in widgets
 - content types: text, widgets, collections
 - Parse text for color
 - Possible refactor: override_or_assign function for default json
 - Implement basic callbacks for changing UI