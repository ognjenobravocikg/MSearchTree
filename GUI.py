import customtkinter
from nodes import MNode, MSearchTree
from exceptions import NodeNotFoundException, InvalidKeyException, SubtreeNotFoundException, DuplicateKeyException

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

m_tree = None

# Creation of the Tree calls nodes.py
def create_tree():
    global m_tree
    try:
        m_value = int(entry_m.get())
        keys = [int(x.strip()) for x in entry_keys.get().split(',')]

        m_tree = MSearchTree(m_value)
        for key in keys:
            try:
                res = m_tree.root.insert(key)
                if res:
                    mid_value, left_child, right_child = res
                    new_root = MNode(m_value)
                    new_root.keys = [mid_value]
                    new_root.children = [left_child, right_child]
                    m_tree.root = new_root
            except DuplicateKeyException as e:
                text_box.insert("end", f"{e}\n")
        
        # Control of the printing of tree in the GUI
        if getattr(root, 'printed', False):
            text_box.delete(1.0, "end")
        else:
            setattr(root, 'printed', True)

        tree_str = m_tree.root.print_tree()
        text_box.insert("end", tree_str)
    except ValueError:
        text_box.insert("end", "Invalid input. Please enter a valid integer.\n")

# Search the M-way Search Tree
def search_tree():
    try:
        value = int(entry_search_num.get())
        result = m_tree.search(value)
        if result:
            text_box.insert("end", f"Found {value} at level {m_tree.root.search(value)}\n")
            
            # Show the buttons for additional operations
            button_left_subtree.grid()
            button_right_subtree.grid()
            button_max_value.grid()
            button_min_value.grid()
            button_is_full.grid()
            button_is_empty.grid()
            
            # Set the value for the left and right subtree buttons
            button_left_subtree.configure(command=lambda: get_left_subtree(value))
            button_right_subtree.configure(command=lambda: get_right_subtree(value))
            button_max_value.configure(command=lambda: get_max_value(value))
            button_min_value.configure(command=lambda: get_min_value(value))
            button_is_full.configure(command=lambda: check_is_full(value))
            button_is_empty.configure(command=lambda: check_is_empty(value))
        else:
            text_box.insert("end", f"Value {value} not found in the tree\n")
    except ValueError:
        text_box.insert("end", "Invalid input. Please enter a valid integer.\n")
    except NodeNotFoundException as e:
        text_box.insert("end", f"{e}\n")


# Function to check whether the node is fulll
def check_is_full(value):
    try:
        node = m_tree.root.search(value)
        if node.isFull():
            text_box.insert("end", f"Node containing {value} is full.\n")
        else:
            text_box.insert("end", f"Node containing {value} is not full.\n")
    except NodeNotFoundException as e:
        text_box.insert("end", f"{e}\n")

# Function to check whether the node is empty
def check_is_empty(value):
    try:
        node = m_tree.root.search(value)
        if node.isEmpty():
            text_box.insert("end", f"Node containing {value} is empty.\n")
        else:
            text_box.insert("end", f"Node containing {value} is not empty.\n")
    except NodeNotFoundException as e:
        text_box.insert("end", f"{e}\n")

def get_left_subtree(value):
    try:
        left_subtree_root = m_tree.root.get_left_subtree(value)
        if left_subtree_root:
            text_box.insert("end", f"Left Subtree:\n{left_subtree_root.print_tree()}\n")
        else:
            text_box.insert("end", "No Left Subtree\n")
    except SubtreeNotFoundException as e:
        text_box.insert("end", f"{e}\n")
    except NodeNotFoundException as e:
        text_box.insert("end", f"{e}\n")

# Function to display the right subtree
def get_right_subtree(value):
    try:
        right_subtree_root = m_tree.root.get_right_subtree(value)
        if right_subtree_root:
            text_box.insert("end", f"Right Subtree:\n{right_subtree_root.print_tree()}\n")
        else:
            text_box.insert("end", "No Right Subtree\n")
    except SubtreeNotFoundException as e:
        text_box.insert("end", f"{e}\n")
    except NodeNotFoundException as e:
        text_box.insert("end", f"{e}\n")

# Gets the maximal value in the node we searched for by value
def get_max_value(value):
    try:
        max_value = m_tree.root.getMaxNum(value)
        if max_value:
            text_box.insert("end", f"Maximal value in the node is: {max_value}\n")
        else:
            text_box.insert("end", "No Max Value Found\n")
    except NodeNotFoundException as e:
        text_box.insert("end", f"{e}\n")

# Gets the minimal value in the node we searched for by value
def get_min_value(value):
    try:
        min_value = m_tree.root.getMinNum(value)
        if min_value:
            text_box.insert("end", f"Minimal value in the node is: {min_value}\n")
        else:
            text_box.insert("end", "No Min Value Found\n")
    except NodeNotFoundException as e:
        text_box.insert("end", f"{e}\n")

# Insert a value into the M-way Search Tree
def insert_tree():
    try:
        value = int(entry_insert_num.get())
        res = m_tree.root.insert(value)
        if res:
            mid_value, left_child, right_child = res
            new_root = MNode(m_tree.root.m)
            new_root.keys = [mid_value]
            new_root.children = [left_child, right_child]
            m_tree.root = new_root

        # Refresh the tree view
        text_box.delete(1.0, "end")
        tree_str = m_tree.root.print_tree()
        text_box.insert("end", tree_str)
    except DuplicateKeyException as e:
        text_box.insert("end", f"{e}\n")
    except ValueError:
        text_box.insert("end", "Invalid input. Please enter a valid integer.\n")

# Delete a value from the M-way Search Tree
def delete_value():
    try:
        values = [int(x.strip()) for x in entry_delete_num.get().split(',')]
        for value in values:
            m_tree.root.delete(value)

        # Refresh the tree view
        text_box.delete(1.0, "end")
        tree_str = m_tree.root.print_tree()
        text_box.insert("end", tree_str)
    except ValueError:
        text_box.insert("end", "Invalid input. Please enter a valid integer.\n")
    except NodeNotFoundException as e:
        text_box.insert("end", f"{e}\n")

# creation the main window
root = customtkinter.CTk()
root.geometry("700x500")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label1 = customtkinter.CTkLabel(master=frame, text="MSearchTree Visualized - project by Ognjen Obradovic", font=("Helvetica", 14, "bold"))
label1.grid(row=0, column=0, columnspan=3, pady=10)

entry_m = customtkinter.CTkEntry(master=frame, placeholder_text="Enter m value")
entry_m.grid(row=1, column=0, pady=5, padx=10)

entry_keys = customtkinter.CTkEntry(master=frame, placeholder_text="Enter keys (comma-separated)")
entry_keys.grid(row=2, column=0, pady=5, padx=10)

# Button for creating the tree calls the create_tree function
button_create_tree = customtkinter.CTkButton(master=frame, text="Generate the tree", command=create_tree)
button_create_tree.grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky="ew")

entry_search_num = customtkinter.CTkEntry(master=frame, placeholder_text="Input the value you want to search for")
entry_search_num.grid(row=4, column=0, pady=5, padx=10)

# Button for searching the tree
button_search_num = customtkinter.CTkButton(master=frame, text="Search", command=search_tree)
button_search_num.grid(row=4, column=1, pady=5, padx=10, sticky="ew")

# Button for getting the left subtree
button_left_subtree = customtkinter.CTkButton(master=frame, text="Get Left Subtree")
# Initially, hide this button
button_left_subtree.grid(row=7, column=0, pady=5, padx=10)
button_left_subtree.grid_remove()

# Button for getting the right subtree
button_right_subtree = customtkinter.CTkButton(master=frame, text="Get Right Subtree")
# Initially, hide this button
button_right_subtree.grid(row=7, column=1, pady=5, padx=10)
button_right_subtree.grid_remove()

# Button for getting the biggest value in a node
button_max_value = customtkinter.CTkButton(master=frame, text="Get Maximal Value")
# Initially, hide this button
button_max_value.grid(row=7, column=2, pady=5, padx=10)
button_max_value.grid_remove()

# Button for getting the smallest value in a node 
button_min_value = customtkinter.CTkButton(master=frame, text="Get Minimal Value")
# Initially, hide this button
button_min_value.grid(row=7, column=3, pady=5, padx=10)
button_min_value.grid_remove()

button_is_full = customtkinter.CTkButton(master=frame, text="Check if Full")
button_is_full.grid(row=7, column=4, pady=5, padx=10)
button_is_full.grid_remove()

button_is_empty = customtkinter.CTkButton(master=frame, text="Check if Empty")
button_is_empty.grid(row=7, column=5, pady=5, padx=10)
button_is_empty.grid_remove()

entry_insert_num = customtkinter.CTkEntry(master=frame, placeholder_text="Input the value you want to insert")
entry_insert_num.grid(row=8, column=0, pady=5, padx=10)

# Button for inserting the value
button_insert_num = customtkinter.CTkButton(master=frame, text="Insert", command=insert_tree)
button_insert_num.grid(row=8, column=1, pady=5, padx=10, sticky="ew")

entry_delete_num = customtkinter.CTkEntry(master=frame, placeholder_text="Input the value you want to delete")
entry_delete_num.grid(row=9, column=0, pady=5, padx=10)

# Button for deleting the value
button_delete_num = customtkinter.CTkButton(master=frame, text="Delete", command=delete_value)
button_delete_num.grid(row=9, column=1, pady=5, padx=10, sticky="ew")

text_box = customtkinter.CTkTextbox(master=frame, wrap="word")
text_box.grid(row=10, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

root.mainloop()
