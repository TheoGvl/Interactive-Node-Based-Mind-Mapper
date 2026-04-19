import flet as ft
import flet.canvas as cv

class MindMapNode(ft.GestureDetector):
    """
    A custom Flet control representing a single idea/node on the mind map.
    Inherits from GestureDetector to allow dragging and clicking interactions.
    """
    def __init__(self, text, x, y, on_move, on_tap, on_double_tap):
        super().__init__()
        # Change the mouse cursor to indicate the item is draggable
        self.mouse_cursor = ft.MouseCursor.MOVE
        self.drag_interval = 10 # How often the drag event fires
        
        # Bind the internal pan handler to the drag event
        self.on_pan_update = self.handle_pan_update
        
        # Bind external functions passed during initialization to tap events
        self.on_tap = lambda e: on_tap(self)
        self.on_double_tap = lambda e: on_double_tap(self)
        self.on_move = on_move
        
        # Store current logical coordinates
        self.x = x
        self.y = y
        
        # We store the Text control in a variable so its value can be updated later
        self.text_control = ft.Text(text, weight=ft.FontWeight.BOLD, color="white")
        
        # The visual container for the node
        self.content = ft.Container(
            content=self.text_control,
            bgcolor="blue700",
            padding=15,
            border_radius=20,
            alignment=ft.Alignment(0, 0), # Safely centers the text
            border=None # Starts with no border; a yellow border is applied when selected
        )
        
        # Initial absolute positioning on the Stack
        self.left = x
        self.top = y

    def handle_pan_update(self, e: ft.DragUpdateEvent):
        """Handles the real-time dragging of the node across the workspace."""
        # Ensure local_delta exists before trying to access x and y
        if e.local_delta:
            # Update logical coordinates based on mouse movement
            self.x += e.local_delta.x
            self.y += e.local_delta.y
            
            # Update visual Stack coordinates
            self.left = self.x
            self.top = self.y
            
            # Refresh this specific node's UI
            self.update()
            
            # Trigger the callback to redraw all connecting lines on the canvas
            self.on_move()

def main(page: ft.Page):
    # --- Window Configuration ---
    page.title = "Interactive Mind Mapper"
    page.bgcolor = "black"
    page.window.width = 1000
    page.window.height = 700

    # --- State Management ---
    nodes = [] # Holds all created MindMapNode objects
    selected_node = [None] # Tracks the currently selected node
    connections = [] # Stores tuples of connected nodes
    node_to_rename = [None] # Tracks which node is currently being renamed

    # --- The Drawing Canvas ---
    canvas = cv.Canvas(
        expand=True,
        shapes=[],
    )

    def update_connections():
        """Clears and redraws all lines between connected nodes."""
        canvas.shapes.clear()
        for n1, n2 in connections:
            canvas.shapes.append(
                cv.Line(
                    # Add 50 and 25 to roughly target the visual center of the UI Container
                    n1.x + 50, n1.y + 25,
                    n2.x + 50, n2.y + 25,
                    paint=ft.Paint(color="white24", stroke_width=2)
                )
            )
        canvas.update()

    # --- Feature 1, Selection and Connecting ---
    def handle_node_tap(node):
        """Handles single clicks for selecting and connecting nodes."""
        if selected_node[0] == node:
            # If clicking the already selected node, deselect it
            node.content.border = None
            selected_node[0] = None
            node.update()
        elif selected_node[0] is not None:
            # If another node is selected, create a connection between them and check to avoid duplicate lines in either direction
            if (selected_node[0], node) not in connections and (node, selected_node[0]) not in connections:
                connections.append((selected_node[0], node))
            
            # Reset the selection state after connecting
            selected_node[0].content.border = None
            selected_node[0].update()
            selected_node[0] = None
            
            # Redraw lines to show the new connection
            update_connections()
        else:
            # If nothing is selected, highlight this node as the active selection
            node.content.border = ft.border.all(3, "yellowAccent")
            selected_node[0] = node
            node.update()

    # --- Feature 2, Renaming Nodes ---
    rename_input = ft.TextField(label="New Name", width=300)

    def close_dialog(e):
        """Closes the rename dialog without saving."""
        rename_dialog.open = False
        page.update()

    def save_name(e):
        """Saves the new name to the node and closes the dialog."""
        if node_to_rename[0] and rename_input.value:
            # Update the text of the targeted node
            node_to_rename[0].text_control.value = rename_input.value
            node_to_rename[0].update()
        
        rename_dialog.open = False
        page.update()

    # The popup dialog for renaming
    rename_dialog = ft.AlertDialog(
        title=ft.Text("Rename Idea"),
        content=rename_input,
        actions=[
            ft.TextButton("Cancel", on_click=close_dialog),
            ft.TextButton("Save", on_click=save_name),
        ]
    )

    def handle_node_double_tap(node):
        """Triggers the rename dialog when a node is double-clicked."""
        node_to_rename[0] = node
        rename_input.value = node.text_control.value # Pre-fill with current name
        
        # Ensure the dialog is in the page overlay before opening
        if rename_dialog not in page.overlay:
            page.overlay.append(rename_dialog)
            
        rename_dialog.open = True
        page.update()

    # --- Main Workspace ---
    workspace = ft.Stack(controls=[canvas], expand=True)

    def add_node(e):
        """Creates a new node based on the text input and adds it to the workspace."""
        if node_input.value:
            new_node = MindMapNode(
                node_input.value, 
                400 + (len(nodes) * 20), # Slight visual offset for each new node
                300 + (len(nodes) * 20), 
                update_connections,
                handle_node_tap,
                handle_node_double_tap
            )
            nodes.append(new_node)
            workspace.controls.append(new_node)
            
            # Clear the input field
            node_input.value = ""
            page.update()

    # --- Top UI Bar ---
    node_input = ft.TextField(label="Idea Name", width=200, color="white")
    add_btn = ft.Button(content="Add Node", on_click=add_node) # Modern Flet Button

    page.add(
        ft.Row([node_input, add_btn], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(color="white10"),
        workspace
    )

    # Initialize the app with a default center node
    initial_node = MindMapNode("Main Idea", 450, 300, update_connections, handle_node_tap, handle_node_double_tap)
    nodes.append(initial_node)
    workspace.controls.append(initial_node)
    page.update()

# --- Application Entry Point ---
if hasattr(ft, 'run'):
    ft.run(main)
else:
    ft.app(target=main)