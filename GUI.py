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
    else:
        text_box.insert("end", f"Value {value} not found in the tree\n")

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
    values = entry_delete_num.get().split(',')  # Split input values by comma
    for value in values:
        try:
            value = int(value.strip())  # Convert each value to integer
            m_tree.root.delete(value)  # Delete the value from the tree
        except ValueError:
            print(f"Invalid input value: {value}")
    
    # Refresh the tree view
    text_box.delete(1.0, "end")
    tree_str = m_tree.root.print_tree()
    text_box.insert("end", tree_str)

# creation the main window 
root = customtkinter.CTk()
root.geometry("700x700")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label1 = customtkinter.CTkLabel(master=frame, text="MSearchTree Visualized - project by Ognjen Obradovic")
label1.pack(pady=12, padx=10)

entry_m = customtkinter.CTkEntry(master=frame, placeholder_text="Enter m value")
entry_m.pack(pady=12, padx=10)

entry_keys = customtkinter.CTkEntry(master=frame, placeholder_text="Enter keys (comma-separated)")
entry_keys.pack(pady=12, padx=10)

# Button for creating the tree calls the create_tree function
button_create_tree = customtkinter.CTkButton(master=frame, text="Generate the tree", command=create_tree)
button_create_tree.pack(pady=12, padx=10)

entry_search_num = customtkinter.CTkEntry(master=frame, placeholder_text="Input the value you want to search for")
entry_search_num.pack(pady=12, padx=10)

# Button for searching the tree 
button_search_num = customtkinter.CTkButton(master=frame, text="Search", command=search_tree)
button_search_num.pack(pady=12, padx=10)

entry_insert_num = customtkinter.CTkEntry(master=frame, placeholder_text="Input the value you want to insert")
entry_insert_num.pack(pady=12, padx=10)

# Button for inserting a value into the tree 
button_insert_num = customtkinter.CTkButton(master=frame, text="Insert", command=insert_tree)
button_insert_num.pack(pady=12, padx=10)

entry_delete_num = customtkinter.CTkEntry(master=frame, placeholder_text="Input the value you want to delete")
entry_delete_num.pack(pady=12, padx=10)

# Button for deleting a value from the tree 
button_delete_num = customtkinter.CTkButton(master=frame, text="Delete", command=delete_value)
button_delete_num.pack(pady=12, padx=10)

text_box = customtkinter.CTkTextbox(master=frame)
text_box.pack(pady=12, padx=10, fill="both", expand=True)

root.mainloop()
