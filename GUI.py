import customtkinter
from nodes import MNode, MSearchTree

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

m_tree = None

# Creation of the Tree calls nodes.py
def create_tree():
    global m_tree
    m_value = int(entry_m.get())
    keys = [int(x.strip()) for x in entry_keys.get().split(',')]

    m_tree = MSearchTree(m_value)
    for key in keys:
        res = m_tree.root.insert(key)
        if res:
            mid_value, left_child, right_child = res
            new_root = MNode(m_value)
            new_root.keys = [mid_value]
            new_root.children = [left_child, right_child]
            m_tree.root = new_root

    # Control of the printing of tree in the GUI
    if getattr(root, 'printed', False):
        text_box.delete(1.0, "end")
    else:
        setattr(root, 'printed', True)

    tree_str = m_tree.root.print_tree()
    text_box.insert("end", tree_str)

# Search the M-way Search Tree
def search_tree():
    value = int(entry_search_num.get())
    result = m_tree.search(value)
    if result:
        text_box.insert("end", result + "\n")
        button_left_subtree.grid(row=4, column=2, pady=5, padx=5)
        button_right_subtree.grid(row=4, column=3, pady=5, padx=5)
        # Set the value for the left and right subtree buttons
        button_left_subtree.configure(command=lambda: get_left_subtree(value))
        button_right_subtree.configure(command=lambda: get_right_subtree(value))
    else:
        text_box.insert("end", f"Value {value} not found in the tree\n")

# Get left subtree
def get_left_subtree(value):
    left_subtree = m_tree.root.get_left_subtree(value)
    if left_subtree:
        text_box.insert("end", f"Left Subtree: {left_subtree.keys}\n")
    else:
        text_box.insert("end", "No Left Subtree\n")

# Get right subtree
def get_right_subtree(value):
    right_subtree = m_tree.root.get_right_subtree(value)
    if right_subtree:
        text_box.insert("end", f"Right Subtree: {right_subtree.keys}\n")
    else:
        text_box.insert("end", "No Right Subtree\n")

# Insert a value into the M-way Search Tree
def insert_tree():
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

# Delete a value from the M-way Search Tree
def delete_value():
    values = entry_delete_num.get().split(',')
    for value in values:
        try:
            value = int(value.strip())
            m_tree.root.delete(value)
        except ValueError:
            print(f"Invalid input value: {value}")

    # Refresh the tree view
    text_box.delete(1.0, "end")
    tree_str = m_tree.root.print_tree()
    text_box.insert("end", tree_str)

# creation the main window
root = customtkinter.CTk()
root.geometry("700x500")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label1 = customtkinter.CTkLabel(master=frame, text="MSearchTree Visualized - project by Ognjen Obradovic", font=("Helvetica", 14, "bold"))
label1.grid(row=0, column=0, columnspan=3, pady=10)

entry_m = customtkinter.CTkEntry(master=frame, placeholder_text="Enter m value")
entry_m.grid(row=1, column=0, pady=5, padx=5)

entry_keys = customtkinter.CTkEntry(master=frame, placeholder_text="Enter keys (comma-separated)")
entry_keys.grid(row=2, column=0, pady=5, padx=5)

# Button for creating the tree calls the create_tree function
button_create_tree = customtkinter.CTkButton(master=frame, text="Generate the tree", command=create_tree)
button_create_tree.grid(row=3, column=0, columnspan=2, pady=5, padx=5, sticky="ew")

entry_search_num = customtkinter.CTkEntry(master=frame, placeholder_text="Input the value you want to search for")
entry_search_num.grid(row=4, column=0, pady=5, padx=5)

# Button for searching the tree
button_search_num = customtkinter.CTkButton(master=frame, text="Search", command=search_tree)
button_search_num.grid(row=4, column=1, pady=5, padx=5, sticky="ew")

# Button for getting the left subtree
button_left_subtree = customtkinter.CTkButton(master=frame, text="Get Left Subtree")
# Initially, hide this button
button_left_subtree.grid(row=4, column=2, pady=5, padx=5)
button_left_subtree.grid_remove()

# Button for getting the right subtree
button_right_subtree = customtkinter.CTkButton(master=frame, text="Get Right Subtree")
# Initially, hide this button
button_right_subtree.grid(row=4, column=3, pady=5, padx=5)
button_right_subtree.grid_remove()

entry_insert_num = customtkinter.CTkEntry(master=frame, placeholder_text="Input the value you want to insert")
entry_insert_num.grid(row=5, column=0, pady=5, padx=5)

# Button for inserting a value into the tree
button_insert_num = customtkinter.CTkButton(master=frame, text="Insert", command=insert_tree)
button_insert_num.grid(row=5, column=1, pady=5, padx=5, sticky="ew")

entry_delete_num = customtkinter.CTkEntry(master=frame, placeholder_text="Input the value you want to delete")
entry_delete_num.grid(row=6, column=0, pady=5, padx=5)

# Button for deleting a value from the tree
button_delete_num = customtkinter.CTkButton(master=frame, text="Delete", command=delete_value)
button_delete_num.grid(row=6, column=1, pady=5, padx=5, sticky="ew")

text_box = customtkinter.CTkTextbox(master=frame)
text_box.grid(row=7, column=0, columnspan=2, pady=10, padx=5, sticky="nsew")

root.mainloop()
