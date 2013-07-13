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

### User event handling

Local events triggered by the user are addressed separately from external (server) events.

## Styling & Formatting

Widgets can contain styling and formatting information inside the widget definition. Alternatively, styles can be specified at the app level and referenced in each widget. Currently, each widget can have only one style at a time.

Style or formatting information in a style reference will override the default information for a widget

### Style sample
    {
      "name": "sampleStyle",
      "fgColor": "blue",
      "bgColor": "black",
      "reverse": true
    }

## Internals

### Builders

When constructing a widget from the specified JSON, the engine will attempt to merge the relevant portions of the specification dictionary into a dictionary which specifies default values. This way, those values you specify will overwrite the defaults and become part of the widget instance's state, while the defaults will remain for any optional parameters you leave unspecified.

Once this merge is complete, the full specification is copied to the widget instance's current_state attribute. Every time we 'build' a widget, we will refer to this instead of the instance's spec attribute. The idea here is that we can resize or otherwise change a widget instance by modifying its current_state, then reset it using the spec attribute. Methods for querying the spec and current_state are the same, with an extra optional parameter being used to tell the methods which to query. The default is the current_state.

Whenever we modify the current_state of the widget, we should mark the widget as dirty, using the mark_dirty method. This will trigger the widget to be 'rebuilt' (the current_state to be reprocessed) upon next render cycle.

### Draw methods

Draw methods are what they sound like: they do all the manipulation of the wrapped caca canvas object for the widget.

## TODO

### key bindings/event loop/messaging & events
- Application-wide primitives
- Widget-specific events
  - Specify widget must be focused for event to trigger
    {
      "key" : "t",
      "func": "widgetSpecificHook",
      "requireFocus": true
    }

### formatting and styling
- App-wide config
    - Fullscreen (Useless later on but for now...)
- Widget resizing
- Implement 'mark_dirty' and rebuilding methods
- widget formatting
  - separate color schemes and formatting styles
  - align: left, right, center
  - margin - horizontal and vertical
- other styling
  - reverse video
  - emphasis?
- resizing?
- widget nesting
- Widget content types -
  - text/line buffers
  - widgets
  - collections (e.g. list boxes)
- menus - list boxes, form controls

## Textual markup language for line/text buffers
- colors
- emphasis
- printf-style interpolation (data binding from within buffers?)
- hyperlinks?

- Possible refactor: override_or_assign function for default json
