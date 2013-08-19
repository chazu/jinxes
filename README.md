# TARTENGINE

TARTENGINE is a text-based application framework. Applications are specified using a declarative JSON structure, which is interpreted at runtime by the application engine. Application-level logic can be added to an application through the use of hooks.

## Syntax

## Events

There are currently three types of event in the system:

### Keypress events
### Local events
### Remote events

### Remote event dispatch

The remote event dispatch provides an interface between the app and any netcode which may be asynchronously sending and receiving messages which affecting app state.

Although the API was designed with AMQP in mind as the means of message brokering, we have tried to keep things generic.

The default dispatch establishes a connection with an AMQP server and creates an exclusive queue with which the broker can notify the client of events. Additional queues can be implemented at the application level.

## Styling & Formatting

Widgets can contain styling and formatting information inside the widget definition. Alternatively, styles can be specified at the app level and referenced in each widget. Currently, each widget can have only one style at a time.

Style or formatting information in a style reference will override the default information for a widget.

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
- widget formatting
  - separate color schemes and formatting styles
  - align: left, right, center
  - margin - horizontal and vertical
- other styling
  - reverse video
  - emphasis?
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
