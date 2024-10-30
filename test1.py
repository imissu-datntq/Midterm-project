import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Treeview Example")

# Create the Treeview widget
tree = ttk.Treeview(root)
tree.pack()

# Add columns to the treeview
tree['columns'] = ('Name', 'Age')
tree.column('#0', width=0, stretch=tk.NO)
tree.column('Name', anchor=tk.W, width=120)
tree.column('Age', anchor=tk.CENTER, width=80)

tree.heading('#0', text='', anchor=tk.W)
tree.heading('Name', text='Name', anchor=tk.W)
tree.heading('Age', text='Age', anchor=tk.CENTER)

# Insert some initial items
tree.insert('', 'end', values=('Alice', 25))
tree.insert('', 'end', values=('Bob', 30))

# Function to insert a new item at the end
def insert_item_at_end():
    tree.insert('', 'end', values=('Charlie', 22))

# Button to add a new item
button = tk.Button(root, text='Add Item', command=insert_item_at_end)
button.pack()

# Run the application
root.mainloop()
