import customtkinter 
from nodes import MNode, MSearchTree

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

def create_tree():
    m_value = int(entry1.get())
    keys = [int(x.strip()) for x in entry2.get().split(',')]
    
    m_tree = MSearchTree(m_value)
    for key in keys:
        m_tree.root.insertKey(key)

    if getattr(root, 'printed', False):
        text_box.delete(1.0, "end")
    else:
        setattr(root, 'printed', True)

    tree_str = m_tree.root.print_tree()
    text_box.insert("end", tree_str) 

root = customtkinter.CTk()
root.geometry("500x350")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label1 = customtkinter.CTkLabel(master=frame, text="MSearchTree Visualized - project by Ognjen Obradovic")
label1.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Enter m value")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Enter keys (comma-separated)")
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Generate the tree", command=create_tree)
button.pack(pady=12, padx=10)

text_box = customtkinter.CTkTextbox(master=frame)
text_box.pack(pady=12, padx=10, fill="both", expand=True)

root.mainloop()
