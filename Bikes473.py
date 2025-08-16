import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from bson.objectid import ObjectId

# ----------------- MongoDB Connection -----------------
client = MongoClient("mongodb://localhost:27017/")
db = client["bikeDB"]
collection = db["bikes"]

# ----------------- GUI Functions -----------------
def insert_data():
    bike = {
        "bike_no": entry_bike_no.get(),
        "owner": entry_owner.get(),
        "model": entry_model.get(),
        "color": entry_color.get()
    }
    if not all(bike.values()):
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    collection.insert_one(bike)
    messagebox.showinfo("Success", "Bike Registered ✅")
    show_data()
    clear_entries()


def show_data():
    for row in tree.get_children():
        tree.delete(row)

    for data in collection.find():
        tree.insert("", "end", values=(
            str(data["_id"]),
            data["bike_no"],
            data["owner"],
            data["model"],
            data["color"]
        ))


def update_data():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Error", "Please select a record to update!")
        return

    values = tree.item(selected, "values")
    bike_id = values[0]

    collection.update_one({"_id": ObjectId(bike_id)},
                          {"$set": {
                              "bike_no": entry_bike_no.get(),
                              "owner": entry_owner.get(),
                              "model": entry_model.get(),
                              "color": entry_color.get()
                          }})
    messagebox.showinfo("Updated", "Bike Data Updated ✅")
    show_data()
    clear_entries()


def delete_data():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Error", "Please select a record to delete!")
        return

    values = tree.item(selected, "values")
    bike_id = values[0]

    collection.delete_one({"_id": ObjectId(bike_id)})
    messagebox.showinfo("Deleted", "Bike Deleted ❌")
    show_data()


def clear_entries():
    entry_bike_no.delete(0, tk.END)
    entry_owner.delete(0, tk.END)
    entry_model.delete(0, tk.END)
    entry_color.delete(0, tk.END)


# ----------------- GUI Layout -----------------
root = tk.Tk()
root.title("🏍 Bike Management System (MongoDB)")
root.geometry("850x500")
root.configure(bg="#eaf4fc")

# Labels and Entries
tk.Label(root, text="Bike No:", bg="#eaf4fc").grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.Label(root, text="Owner:", bg="#eaf4fc").grid(row=1, column=0, padx=10, pady=5, sticky="w")
tk.Label(root, text="Model:", bg="#eaf4fc").grid(row=2, column=0, padx=10, pady=5, sticky="w")
tk.Label(root, text="Color:", bg="#eaf4fc").grid(row=3, column=0, padx=10, pady=5, sticky="w")

entry_bike_no = tk.Entry(root, width=30)
entry_owner = tk.Entry(root, width=30)
entry_model = tk.Entry(root, width=30)
entry_color = tk.Entry(root, width=30)

entry_bike_no.grid(row=0, column=1, padx=10, pady=5)
entry_owner.grid(row=1, column=1, padx=10, pady=5)
entry_model.grid(row=2, column=1, padx=10, pady=5)
entry_color.grid(row=3, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Add Bike", command=insert_data, bg="green", fg="white", width=15).grid(row=0, column=2, padx=10)
tk.Button(root, text="Update Bike", command=update_data, bg="blue", fg="white", width=15).grid(row=1, column=2, padx=10)
tk.Button(root, text="Delete Bike", command=delete_data, bg="red", fg="white", width=15).grid(row=2, column=2, padx=10)
tk.Button(root, text="Clear", command=clear_entries, bg="orange", fg="white", width=15).grid(row=3, column=2, padx=10)

# Table
columns = ("ID", "Bike No", "Owner", "Model", "Color")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=140)
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=20)

# Load data
show_data()

root.mainloop()