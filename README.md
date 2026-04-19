# Interactive Node-Based Mind Mapper 

A dynamic, interactive digital whiteboard application built with Python and Flet. This tool allows you to visually organize your thoughts by creating draggable text nodes and linking them together with connecting lines on a dark-themed digital canvas.

## Features

* **Draggable Nodes:** Click and drag any idea across the screen in real-time. Connecting lines automatically update their geometry to follow the nodes.
* **Freeform Linking:** Click one node to select it, highlighted with a yellow border, then click another to instantly draw a connection between them.
* **Dynamic Renaming:** Double-click any node, including the default "Main Idea" to open a dialog and edit its text on the fly.
* **Modern Architecture:** Built using the latest Flet capabilities (0.83+/0.25+), including the decoupled `flet.canvas` module and updated Gesture event handling.

## Technologies Used
Python 3: Core programming language.
flet: Handles the UI layout, Dialogs, and Gesture detection.
flet.canvas: The specialized graphics module used to draw the dynamic intersecting lines between absolute coordinate points.

## Prerequisites

Before running this application, ensure you have **Python 3.8+** installed on your system. 
You will also need to install the Flet library:

```bash
pip install flet
