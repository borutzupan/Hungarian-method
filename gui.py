import tkinter as tk
from tkinter import DISABLED, messagebox
import numpy as np
import sqlite3
import main


root = tk.Tk()
root.title("HUNGARIAN METHOD")
root.geometry("250x250")


# FUNCTIONS FOR WIDGETS
def show_matrix(matrix, window):
    (n_rows, n_cols) = matrix.shape
    for r in range(n_rows):
        for c in range(n_cols):
            mystr = tk.StringVar()
            mystr.set('{}'.format(matrix[r, c]))
            entry = tk.Entry(window, width=5, textvariable=mystr, state=DISABLED)
            entry.grid(row=r+3, column=c)
    window.after(1, lambda: window.focus_force())


def get_data():
    global matrix
    for r, row in enumerate(all_entries):
        for c, entry in enumerate(row):
            text = entry.get()
            matrix[r, c] = int(text)

    show_matrix(matrix, root)


def get_data_random(num_rows, num_cols):
    global matrix_random
    global lower_number
    global higher_number
    matrix_random = np.random.randint(int(lower_number.get()), high=int(higher_number.get()), size=(num_rows, num_cols))
    show_matrix(matrix_random, root)


def openwindow(sort):
    global num_rows
    global num_cols
    global matrix
    global matrix_random

    num_rows = int(rows.get())
    num_cols = int(cols.get())

    if sort == "custom":
        if (num_rows == 0) or (num_cols == 0):
            messagebox.showerror("Error", "Number of rows and columns have to be greater than 0")
            return
        
        topC = tk.Toplevel()
        topC.title("Custom Matrix")
        topC.geometry("250x250")

        matrix = np.zeros((num_rows, num_cols))

        global all_entries
        all_entries = []
        for r in range(num_rows):
            entries_row = []
            for c in range(num_cols):
                e = tk.Entry(topC, width=5)
                e.insert('end', 0)
                e.grid(row=r, column=c)
                entries_row.append(e)
            all_entries.append(entries_row)
        
        b = tk.Button(topC, text='CREATE', command=get_data)
        b.grid(row=num_rows+1, column=0, columnspan=num_cols)
        b.grid_columnconfigure(0, weight=1)

        exit_button = tk.Button(topC, text="Exit", command=topC.destroy)
        exit_button.grid(row=num_rows+2, column=0, columnspan=num_cols)
        exit_button.grid_columnconfigure(0, weight=1)

    if sort == "random":
        if (num_rows == 0) or (num_cols == 0):
            messagebox.showerror("Error", "Number of rows and columns have to be greater than 0")
            return
 
        topR = tk.Toplevel()
        topR.title("Random Matrix")
        topR.geometry("350x250")

        descriptionR = tk.Label(topR, text=("Specify intiger lower and higher bound for intigers in matrix:"))

        global lower_number
        global higher_number

        lowerLabel = tk.Label(topR, text=("lower bound: "))
        higherLabel = tk.Label(topR, text=("higher bound: "))
        lower_number = tk.Entry(topR, width=10)
        lower_number.insert('end', 0)
        higher_number = tk.Entry(topR, width=10)
        higher_number.insert('end', 10)

        descriptionR.grid(row=0, column=0, columnspan=2)
        lowerLabel.grid(row=1, column=0)
        lower_number.grid(row=1, column=1)
        higherLabel.grid(row=2, column=0)
        higher_number.grid(row=2, column=1)

        matrix_random = np.zeros((num_rows, num_cols))
        
        b = tk.Button(topR, text='CREATE', command=lambda: get_data_random(num_rows, num_cols))
        b.grid(row=3, column=0, columnspan=2)
        b.grid_columnconfigure(0, weight=1)

        exit_button = tk.Button(topR, text="Exit", command=topR.destroy)
        exit_button.grid(row=4, column=0, columnspan=2)


# CREATING WIDGETS
# ----------------------------------------------

# ----------------------------------------------
rowsLabel = tk.Label(root, text=("rows: "))
colsLabel = tk.Label(root, text=("cols: "))
rows = tk.Entry(root, width=10)
rows.insert('end', 3)
cols = tk.Entry(root, width=10)
cols.insert('end', 3)


custom_matrix_btn = tk.Button(root, text="Create Custom Matrix", command=lambda: openwindow("custom"))
random_matrix_btn = tk.Button(root, text="Create Random Matrix", command=lambda: openwindow("random"))


# WIDGET ON SCREEN
rowsLabel.grid(row=0, column=0)
rows.grid(row=0, column=1)
colsLabel.grid(row=0, column=2)
cols.grid(row=0, column=3)
custom_matrix_btn.grid(row=1, column=0, columnspan=2)
random_matrix_btn.grid(row=2, column=0, columnspan=2)



# main loop
root.mainloop()
