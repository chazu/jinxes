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

## TODO

- key bindings/event loop/messaging & events
  - Application-wide primitives
    - Moving focus
  - establishing focus order at init
  - Widget-specific events

-formatting and styling
  - widget formatting
    - align: left, right, center
    - margin
  - widget coloring
    - bg/foreground
    - border bg/foreground
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

- Textual markup language for line/text buffers
  - colors
  - emphasis
  - printf-style interpolation (data binding from within buffers?)
  - hyperlinks?

- Possible refactor: override_or_assign function for default json
