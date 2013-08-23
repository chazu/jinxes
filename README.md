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

### Remote event dispatches

The remote event dispatch provides an abstraction layer between the app and any netcode which may be asynchronously sending and receiving messages which affecting app state.

Although the API was designed with AMQP in mind as the means of message brokering, we have tried to keep things generic.

The remote event dispatch exposes a number of queues to the application. Once during each app cycle, queues with registered event handlers are checked for new messages. Upon receipt of a new message, the relevant handler is called with either the app object or widget as well as the message. The hook does the rest.

The default implementation included allows for queues to be declared by the app at runtime. This means the burden of setting up the AMQP entities is on the APP implementor. In future we hope to implement a trust feature such that it will be possible to restrict applications from creating or modifying AMQP entities, instead allowing only the use of those entities established by the host application.

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

### Custom state

Since application builders may want to add state to widgets in order to aid them in creating new types of UI behavior, by convention all such state should be namespaced under 'custom'. For example, a widget may have a boolean indicating whether it has been maximized. This would be kept at widget.current_state["custom"]["maximized"].

Custom app-level state should be similarly namespaced.

### Draw methods

Draw methods are what they sound like: they do all the manipulation of the wrapped caca canvas object for the widget.

## TODO

### key bindings/event loop/messaging & events
 - Local event dispatching (non-network, non-keypress-oriented hooks)

### formatting and styling
- App-wide config
    - Fullscreen (Useless later on but for now...)
- widget formatting
  - integrate boldness etc into styles
  - alignment
  - margin - horizontal and vertical
- widget nesting
- Widget content types -
  - text vs line buffers vs widget buffers vs formatted text buffers...
  - collections (e.g. list boxes)

## Textual markup language for line/text buffers
- colors
- emphasis
- printf-style interpolation (data binding from within buffers?)
- hyperlinks?

- Possible refactor: override_or_assign function for default json