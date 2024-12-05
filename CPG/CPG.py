import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os

# Directory for images
IMAGES_DIRECTORY = r"D:\Developer\Python\projects\CPG\images"

# Chess piece data with descriptions
chess_pieces = [
    ("King", "king", 
     "Chessboard Representation\n"
     "• The chessboard is a 5x5 grid.\n"
     "• Each cell is represented as a tuple (r,c), where:\n"
     "  - r is the row index (0 ≤ r < 5)\n"
     "  - c is the column index (0 ≤ c < 5)\n"
     "• The board contains 25 nodes, and edges between nodes depend on the movement rules of the chess pieces.\n\n"
     "King Movement\n"
     "• The King moves one square in any direction. In discrete mathematics, this can be represented as moving to any adjacent vertex in a graph.\n\n"
     "Movement Rules:\n"
     "  - {(dr, dc) = (±1, 0), (0, ±1), (±1, ±1)}\n"
     "Example: A King at (2,2) can move to any of its 8 neighbors."
    ),
    ("Queen", "queen", 
     "Chessboard Representation\n"
     "• The chessboard is a 5x5 grid.\n"
     "• Each cell is represented as a tuple (r,c), where:\n"
     "  - r is the row index (0 ≤ r < 5)\n"
     "  - c is the column index (0 ≤ c < 5)\n"
     "• The board contains 25 nodes, and edges between nodes depend on the movement rules of the chess pieces.\n\n"
     "Queen Movement\n"
     "• The Queen moves any number of squares in any direction. In discrete mathematics, this can be represented as moving along any path in a graph without changing direction.\n\n"
     "Movement Rules:\n"
     "  - {(dr, dc) = (i, i), (i, −i), (i, 0), (0, i) | −4 ≤ i ≤ 4}"
    ),
    ("Bishop", "bishop", 
     "Chessboard Representation\n"
     "• The chessboard is a 5x5 grid.\n"
     "• Each cell is represented as a tuple (r,c), where:\n"
     "  - r is the row index (0 ≤ r < 5)\n"
     "  - c is the column index (0 ≤ c < 5)\n"
     "• The board contains 25 nodes, and edges between nodes depend on the movement rules of the chess pieces.\n\n"
     "Bishop Movement\n"
     "• The Bishop moves diagonally any number of squares. In discrete mathematics, this can be represented as moving along a diagonal path in a graph.\n\n"
     "Movement Rules:\n"
     "  - {(dr, dc) = (i, i), (i, −i) | −4 ≤ i ≤ 4}\n"
     "Example: A Bishop at (2,2) can move to nodes along diagonal paths, e.g., (1,1), (3,3), etc."
    ),
    ("Knight", "knight", 
     "Chessboard Representation\n"
     "• The chessboard is a 5x5 grid.\n"
     "• Each cell is represented as a tuple (r,c), where:\n"
     "  - r is the row index (0 ≤ r < 5)\n"
     "  - c is the column index (0 ≤ c < 5)\n"
     "• The board contains 25 nodes, and edges between nodes depend on the movement rules of the chess pieces.\n\n"
     "Knight Movement\n"
     "• The Knight moves in an L-shape: two squares in one direction and then one square perpendicular. In discrete mathematics, this can be represented as moving to a vertex that is two edges away in one direction and one edge away in a perpendicular direction.\n\n"
     "Movement Rules:\n"
     "  - {(dr, dc) = ±(2, 1), ±(1, 2)}\n"
     "Example: A Knight at (2,2) can move to (4,3), (4,1), (3,4), (3,0), (0,3), (0,1), (1,4), (1,0), subject to boundary constraints."
    ),
    ("Rook", "rook", 
     "Chessboard Representation\n"
     "• The chessboard is a 5x5 grid.\n"
     "• Each cell is represented as a tuple (r,c), where:\n"
     "  - r is the row index (0 ≤ r < 5)\n"
     "  - c is the column index (0 ≤ c < 5)\n"
     "• The board contains 25 nodes, and edges between nodes depend on the movement rules of the chess pieces.\n\n"
     "Rook Movement\n"
     "• The Rook moves any number of squares vertically or horizontally. In discrete mathematics, this can be represented as moving along a straight path in a graph.\n\n"
     "Movement Rules:\n"
     "  - {(dr, dc) = (i, 0), (0, i) | −4 ≤ i ≤ 4}\n"
     "Example: A Rook at (2,2) can move to (2,0), (2,4), (0,2), (4,2), etc."
    ),
    ("Pawn", "pawn", 
     "Chessboard Representation\n"
     "• The chessboard is a 5x5 grid.\n"
     "• Each cell is represented as a tuple (r,c), where:\n"
     "  - r is the row index (0 ≤ r < 5)\n"
     "  - c is the column index (0 ≤ c < 5)\n"
     "• The board contains 25 nodes, and edges between nodes depend on the movement rules of the chess pieces.\n\n"
     "Pawn Movement\n"
     "• The Pawn moves one square forward. On its first move, it can move two squares forward. In discrete mathematics, this can be represented as moving to the next vertex in a directed path, with an option to move two vertices on the first move.\n\n"
     "Movement Rules:\n"
     "  - {(dr, dc) = (1, 0)}\n"
     "Example: A Pawn at (2,2) can move to (3,2)."
    )
]

current_piece_index = 0  # Start with the first piece

def generate_piece_graph(piece):
    """Generate the logic graph for the selected chess piece on a 5x5 board."""
    graph = nx.Graph()
    positions = {}

    # Represent the chessboard as a 5x5 grid of nodes
    for row in range(5):  # Limit to 5 rows
        for col in range(5):  # Limit to 5 columns
            node = (row, col)
            graph.add_node(node)
            positions[node] = (col, -row)  # Reverse y-axis for display

    # Add edges based on the piece's movement rules
    directions = get_move_directions(piece)
    for node in graph.nodes:
        for dr, dc in directions:
            neighbor = (node[0] + dr, node[1] + dc)
            if 0 <= neighbor[0] < 5 and 0 <= neighbor[1] < 5:  # Adjust boundaries to 5x5
                graph.add_edge(node, neighbor)

    return graph, positions

def get_move_directions(piece):
    """Return movement directions for the given piece on a smaller board."""
    directions = {
        "Pawn": [(1, 0)],
        "Knight": [(2, 1), (1, 2), (-2, 1), (-1, 2), (-2, -1), (-1, -2), (2, -1), (1, -2)],
        "Bishop": [(i, i) for i in range(-4, 5)] + [(i, -i) for i in range(-4, 5)],
        "Rook": [(i, 0) for i in range(-4, 5)] + [(0, i) for i in range(-4, 5)],
        "Queen": [(i, i) for i in range(-4, 5)] + [(i, -i) for i in range(-4, 5)] + [(i, 0) for i in range(-4, 5)] + [(0, i) for i in range(-4, 5)],
        "King": [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    }
    return directions.get(piece, [])

def display_moves():
    """Display text and image in the left box, and graph in the right box."""
    piece = chess_pieces[current_piece_index][0]
    update_left_box(piece)  # Update the left box
    update_right_box(piece)  # Update the right box

def update_left_box(piece):
    """Update the left box with the image and description of the piece."""
    image_path = os.path.join(IMAGES_DIRECTORY, f"{piece.lower()}.png")
    try:
        img = Image.open(image_path)
        img = img.resize((200, 200))
        piece_img = ImageTk.PhotoImage(img)
        piece_image_label.config(image=piece_img)
        piece_image_label.image = piece_img  # Keep a reference to avoid garbage collection
    except FileNotFoundError:
        piece_image_label.config(image='', text=f"Image for {piece} not found.", font=("Helvetica", 12), fg="red")

def update_right_box(piece):
    global right_box
    """Update the right box with the graph of the piece's moves."""
    graph, positions = generate_piece_graph(piece)
    figure = plt.Figure(figsize=(4, 4))
    ax = figure.add_subplot(111)
    nx.draw(graph, positions, with_labels=True, ax=ax, node_size=500, node_color="lightblue", font_size=8)
    for widget in right_box.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(figure, right_box)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

def open_guide(piece_name, piece_key):
    """Open the guide window for the selected chess piece and close the selection window."""
    global selection_window
    selection_window.destroy()  # Close the selection window

    guide = tk.Toplevel()  # Use Toplevel to open a new window instead of a blank Tk instance
    guide.title(f"{piece_name} Guide")
    guide.geometry("842x1000")

    # Explanation Boxes
    frame = tk.Frame(guide)
    frame.pack(pady=20, fill="x")

    # Left Box (Image)
    left_box = tk.Frame(frame, relief="solid", width=400, height=470)
    left_box.pack(side="left", padx=10)
    left_box.pack_propagate(False)

    # Right Box (Graph)
    right_box = tk.Frame(frame, relief="solid", width=400, height=440)
    right_box.pack(side="right", padx=10)
    right_box.pack_propagate(False)

    def update_guide_content():
        """Update the guide window with content for the selected piece."""
        # Left side: Image
        image_path = os.path.join(IMAGES_DIRECTORY, f"{piece_key}_moves.png")
        try:
            img = Image.open(image_path)
            img = img.resize((400, 400))
            piece_img = ImageTk.PhotoImage(img)

            for widget in left_box.winfo_children():
                widget.destroy()
            img_label = tk.Label(left_box, image=piece_img)
            img_label.image = piece_img  # Keep a reference to avoid garbage collection
            img_label.pack(pady=10)
        except FileNotFoundError:
            for widget in left_box.winfo_children():
                widget.destroy()
            error_label = tk.Label(left_box, text=f"Image for {piece_name} not found.", font=("Helvetica", 12), fg="red")
            error_label.pack()

        # Right side: Graph of moves
        graph, positions = generate_piece_graph(piece_name)
        figure = plt.Figure(figsize=(4, 4))
        ax = figure.add_subplot(111)

        nx.draw(graph, positions, with_labels=True, ax=ax, node_size=500, node_color="lightblue", font_size=8)

        for widget in right_box.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(figure, right_box)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

        # Add description text below both boxes
        piece_description = next((desc for name, key, desc in chess_pieces if key == piece_key), "No description available.")
        description_text = tk.Text(guide, wrap="word", font=("Helvetica", 14), height=17)
        description_text.insert(tk.END, piece_description)
        description_text.config(state=tk.DISABLED)
        description_text.pack(pady=10)

    def back_to_selection():
        """Close the guide window and reopen the selection window."""
        guide.destroy()
        reopen_selection_window()

    # Initialize the guide content
    update_guide_content()

    # Back Button
    back_button = tk.Button(guide, text="Back", command=back_to_selection)
    back_button.pack(pady=10)

    guide.mainloop()

def previous_piece():
    """Navigate to the previous chess piece."""
    global current_piece_index
    current_piece_index = (current_piece_index - 1) % len(chess_pieces)
    update_selection_display()

def next_piece():
    """Navigate to the next chess piece."""
    global current_piece_index
    current_piece_index = (current_piece_index + 1) % len(chess_pieces)
    update_selection_display()

def update_selection_display():
    """Update the selection window display with the current piece."""
    piece_name, piece_key = chess_pieces[current_piece_index][:2]
    piece_description_label.config(text=piece_name)
    image_path = os.path.join(IMAGES_DIRECTORY, f"{piece_key}.png")
    try:
        img = Image.open(image_path)
        img = img.resize((200, 200))
        piece_img = ImageTk.PhotoImage(img)
        piece_image_label.config(image=piece_img)
        piece_image_label.image = piece_img  # Keep a reference to avoid garbage collection
    except FileNotFoundError:
        piece_image_label.config(image='', text=f"Image for {piece_name} not found.", font=("Helvetica", 12), fg="red")

def reopen_selection_window():
    """Reopen the selection window."""
    global selection_window
    selection_window = tk.Toplevel()
    selection_window.title("Select Chess Piece")
    selection_window.geometry("400x400")

    # Image display
    global piece_image_label
    piece_image_label = tk.Label(selection_window)
    piece_image_label.pack(pady=10)

    # Description label
    global piece_description_label
    piece_description_label = tk.Label(selection_window, text="", font=("Helvetica", 14))
    piece_description_label.pack(pady=5)

    # Navigation Buttons
    nav_frame = tk.Frame(selection_window)
    nav_frame.pack(pady=20)

    previous_button = tk.Button(nav_frame, text="Previous", command=previous_piece)
    previous_button.pack(side="left", padx=10)

    next_button = tk.Button(nav_frame, text="Next", command=next_piece)
    next_button.pack(side="left", padx=10)

    # Open Guide Button
    select_button = tk.Button(
        selection_window, text="Open Guide",
        command=lambda: open_guide(chess_pieces[current_piece_index][0], chess_pieces[current_piece_index][1])
    )
    select_button.pack(pady=10)

    # Initialize the display
    update_selection_display()

# Selection Window
selection_window = tk.Tk()
selection_window.title("Select Chess Piece")
selection_window.geometry("400x400")

# Image display
piece_image_label = tk.Label(selection_window)
piece_image_label.pack(pady=10)

# Description label
piece_description_label = tk.Label(selection_window, text="", font=("Helvetica", 14))
piece_description_label.pack(pady=5)

# Navigation Buttons
nav_frame = tk.Frame(selection_window)
nav_frame.pack(pady=20)

previous_button = tk.Button(nav_frame, text="Previous", command=previous_piece)
previous_button.pack(side="left", padx=10)

next_button = tk.Button(nav_frame, text="Next", command=next_piece)
next_button.pack(side="left", padx=10)

# Open Guide Button
select_button = tk.Button(
    selection_window, text="Open Guide",
    command=lambda: open_guide(chess_pieces[current_piece_index][0], chess_pieces[current_piece_index][1])
)
select_button.pack(pady=10)

# Initialize the display
update_selection_display()

selection_window.mainloop()
