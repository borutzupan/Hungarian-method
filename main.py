import tkinter as tk
from tkinter import DISABLED, messagebox
import numpy as np
from HM import hungarian_method
from statistics import analysis
import warnings

# we ignore some warnings about future disagreement between
# python and numpy
warnings.simplefilter(action='ignore', category=FutureWarning)


root = tk.Tk()
root.title("HUNGARIAN METHOD")

global lst_custom
global lst_random
global weights_custom_min
global weights_custom_max
global weights_random_min
global weights_random_max

lst_custom = None
lst_random = []
weights_custom_min = []
weights_custom_max = []
weights_random_min = []
weights_random_max = []


# FUNCTIONS FOR WIDGETS
def save(matrix, sort):
    # function that will save a matrix into a list
    global lst_custom
    global lst_random
    if sort == "custom":
        lst_custom = matrix
    elif sort == "random":
        lst_random.append(matrix)


def clear(sort):
    # function that will clear the list with matrices
    global lst_custom
    global lst_random
    global weights_custom_min
    global weights_custom_max
    global weights_random_min
    global weights_random_max
    global pairings
    if sort == "custom":
        lst_custom = None
    elif sort == "random":
        lst_random = []
    elif sort == "weights_custom_min":
        weights_custom_min = []
    elif sort == "weights_custom_max":
        weights_custom_max = []
    elif sort == "weights_random_min":
        weights_random_min = []
    elif sort == "weights_random_max":
        weights_random_max = []
    elif sort == "pairings":
        pairings = []


def show_matrix(matrix, window):
    # function that will show matrix on a window
    (n_rows, n_cols) = matrix.shape
    if (n_rows <= 10) and (n_cols <= 10):
        for widget in window.winfo_children():
            widget.destroy()
        for r in range(n_rows):
            for c in range(n_cols):
                mystr = tk.StringVar()
                mystr.set('{}'.format(matrix[r, c]))
                entry = tk.Entry(window, width=5, textvariable=mystr, state=DISABLED)
                entry.grid(row=r, column=c)
    else:
        for widget in window.winfo_children():
            widget.destroy()
        conformationLabel = tk.Label(window, text="Matrix created!", font=('Helvetica', 14, 'bold'))
        conformationLabel.grid(row=0, column=0)


def get_data():
    # function that will put data into a matrix in custom window
    global matrix
    global frame2
    for r, row in enumerate(all_entries):
        for c, entry in enumerate(row):
            text = entry.get()
            matrix[r, c] = int(text)
    save(matrix, "custom")
    # show the matrix
    show_matrix(matrix, frame2)


def get_data_random(num_rows, num_cols, how_many):
    # function that will put data into a matrix in random window
    global matrix_random
    global lower_number
    global higher_number
    global frameR2
    global lst_random
    # clear the list with matrices
    clear("random")
    for i in range(how_many):
        # create the matrix
        matrix_random = np.random.randint(int(lower_number.get()),
                                          high=int(higher_number.get()),
                                          size=(num_rows, num_cols))
        # save matrix in the list
        save(matrix_random, "random")
    # if there is only one matrix then display it
    if how_many == 1:
        show_matrix(matrix_random, frameR2)
    # if there are more then one matrix then tell that they were created
    else:
        # first delete the messages or a matrix on screen
        for widget in frameR2.winfo_children():
            widget.destroy()
        # show the message
        conformationLabel = tk.Label(frameR2, text="Matrices created!", font=('Helvetica', 14, 'bold'))
        conformationLabel.grid(row=0, column=0)


def hung_method(lst, problem, sort):
    global weights_custom_min
    global weights_custom_max
    global weights_random_min
    global weights_random_max
    global frameR4
    global frame4
    global frameR5
    global pairings

    clear(lst)
    pairings = []

    if (sort == "custom") and (problem == "min"):
        clear("weights_custom_min")
        clear("pairings")
        for widget in frame4.winfo_children():
            widget.destroy()
        (w, p) = hungarian_method(lst, "min")
        weights_custom_min.append(w)
        pairings = p

        lb = tk.Label(frame4, text="Minimum weights of matrices:", font=('Helvetica', 12, 'bold'))
        lb.grid(row=0, column=0)
        lb = tk.Label(frame4, text="{}".format(weights_custom_min[0]))
        lb.grid(row=1, column=0)
        lb.grid_columnconfigure(0, weight=1)

        lb = tk.Label(frame4, text="Pairing:", font=('Helvetica', 12, 'bold'))
        lb.grid(row=2, column=0)
        lb = tk.Label(frame4, text="{}".format(pairings))
        lb.grid(row=3, column=0)
        lb.grid_columnconfigure(0, weight=1)

    if (sort == "custom") and (problem == "max"):
        clear("weights_custom_max")
        clear("pairings")
        for widget in frame4.winfo_children():
            widget.destroy()
        (w, p) = hungarian_method(lst, "max")
        weights_custom_max.append(w)
        pairings = p

        lb = tk.Label(frame4, text="Maximum weights of matrices:", font=('Helvetica', 12, 'bold'))
        lb.grid(row=0, column=0)
        lb = tk.Label(frame4, text="{}".format(weights_custom_max[0]))
        lb.grid(row=1, column=0)
        lb.grid_columnconfigure(0, weight=1)
        
        lb = tk.Label(frame4, text="Pairing:" ,font=('Helvetica', 12, 'bold'))
        lb.grid(row=2, column=0)
        lb = tk.Label(frame4, text="{}".format(pairings))
        lb.grid(row=3, column=0)
        lb.grid_columnconfigure(0, weight=1)

    if (sort == "random") and (problem == "min"):
        clear("weights_random_min")
        clear("pairings")
        for widget in frameR4.winfo_children():
            widget.destroy()
        for widget in frameR5.winfo_children():
            widget.destroy()
        for matrix in lst:
            (w, p) = hungarian_method(matrix, "min")
            weights_random_min.append(w)
            # pairings.append(p)

        if len(lst) <= 20:
            lb = tk.Label(frameR4, text="Minimum weights of matrices:", font=('Helvetica', 10, 'bold'))
            lb.grid(row=0, column=0)
            if len(lst) == 1:
                lb = tk.Label(frameR4, text="{}".format(weights_random_min[0]))
                lb.grid(row=1, column=0)
                lb.grid_columnconfigure(0, weight=1)
            else:
                lb = tk.Label(frameR4, text="{}".format(weights_random_min))
                lb.grid(row=1, column=0)
                lb.grid_columnconfigure(0, weight=1)

        (wd, td, _, _) = analysis(lst, problem)

        lb = tk.Label(frameR5, text="Weights:", font=('Helvetica', 12, 'bold'))
        lb.grid(row=0, column=0)
        i = 1
        for key, value in wd.items():
            lb = tk.Label(frameR5, text="{}: {}".format(key, value))
            lb.grid(row=i, column=0)
            lb.grid_columnconfigure(0, weight=1)
            i += 1

        i += 1
        lb = tk.Label(frameR5, text="Time:", font=('Helvetica', 12, 'bold'))
        lb.grid(row=i, column=0)
        i += 1
        for key, value in td.items():
            lb = tk.Label(frameR5, text="{}: {}".format(key, value))
            lb.grid(row=i, column=0)
            lb.grid_columnconfigure(0, weight=1)
            i += 1

    if (sort == "random") and (problem == "max"):
        # clear every list and widget of the screen
        # to make space for new ones
        clear("weights_random_max")
        clear("pairings")
        for widget in frameR4.winfo_children():
            widget.destroy()
        for widget in frameR5.winfo_children():
            widget.destroy()
        # hungarian method on matrices
        for matrix in lst:
            (w, p) = hungarian_method(matrix, "max")
            weights_random_max.append(w)
            # pairings.append(p)
        
        if len(lst) <= 20:
            lb = tk.Label(frameR4, text="Maximum weights of matrices:", font=('Helvetica', 10, 'bold'))
            lb.grid(row=0, column=0)
            if len(lst) == 1:
                lb = tk.Label(frameR4, text="{}".format(weights_random_max[0]))
                lb.grid(row=1, column=0)
                lb.grid_columnconfigure(0, weight=1)
            else:
                lb = tk.Label(frameR4, text="{}".format(weights_random_max))
                lb.grid(row=1, column=0)
                lb.grid_columnconfigure(0, weight=1)
        
        # do an analysis on list of matrices
        (wd, td, _, _) = analysis(lst, problem)

        # put the analysis results on screen
        lb = tk.Label(frameR5, text="Weights:", font=('Helvetica', 12, 'bold'))
        lb.grid(row=0, column=0)
        i = 1
        for key, value in wd.items():
            lb = tk.Label(frameR5, text="{}: {}".format(key, value))
            lb.grid(row=i, column=0)
            lb.grid_columnconfigure(0, weight=1)
            i += 1

        i += 1
        lb = tk.Label(frameR5, text="Time:", font=('Helvetica', 12, 'bold'))
        lb.grid(row=i, column=0)
        i += 1
        for key, value in td.items():
            lb = tk.Label(frameR5, text="{}: {}".format(key, value))
            lb.grid(row=i, column=0)
            lb.grid_columnconfigure(0, weight=1)
            i += 1


def openwindow(sort):
    # function that will open a window of sort = sort
    global num_rows
    global num_cols
    global matrix
    global matrix_random
    global lst_custom
    global lst_random
    global weights_custom_min
    global weights_custom_max
    global weights_random_min
    global weights_random_max

    # number of rows and columns of a matrix
    num_rows = int(rows.get())
    num_cols = int(cols.get())

    if sort == "custom":
        # if there are no dimensions than dont open the window
        if (num_rows == 0) or (num_cols == 0):
            messagebox.showerror("Error", "Number of rows and columns have to be greater than 0")
            return
        
        topC = tk.Toplevel()
        topC.title("Custom Matrix")
        
        # define frames on the window
        global frame2
        global frame4
        frame1 = tk.Frame(topC)
        frame1.grid(row=0, column=0)
        frame2 = tk.Frame(topC)
        frame2.grid(row=0, column=1, padx=20)
        frame3 = tk.Frame(topC)
        frame3.grid(row=1, column=0, pady=20)
        frame4 = tk.Frame(topC)
        frame4.grid(row=1, column=1, padx=20,  pady=20)

        matrix = np.zeros((num_rows, num_cols))

        # build a matrix out of entries
        global all_entries
        all_entries = []
        for r in range(num_rows):
            entries_row = []
            for c in range(num_cols):
                e = tk.Entry(frame1, width=5)
                e.insert('end', 0)
                e.grid(row=r, column=c)
                entries_row.append(e)
            all_entries.append(entries_row)
        
        # button that will create the matrix
        b = tk.Button(frame3, text='CREATE', command=get_data)
        b.grid(row=0, column=0, columnspan=num_cols)
        b.grid_columnconfigure(0, weight=1)

        # button which will launch hungarian method for minimal cost
        hungMin_button = tk.Button(frame3, text="Hungarian Min",
                                   command=lambda: hung_method(lst_custom, "min", "custom"))
        hungMin_button.grid(row=1, column=0)
        hungMin_button.grid_columnconfigure(0, weight=1)

        # button which will launch hungarian method for maximum cost
        hungMax_button = tk.Button(frame3, text="Hungarian max",
                                   command=lambda: hung_method(lst_custom, "max", "custom"))
        hungMax_button.grid(row=2, column=0)
        hungMax_button.grid_columnconfigure(0, weight=1)

        # button that will close the window
        exit_button = tk.Button(frame3, text="Exit", command=topC.destroy)
        exit_button.grid(row=4, column=0, pady=10)
        exit_button.grid_columnconfigure(0, weight=1)

    if sort == "random":
        # if there are no dimensions than dont open the window
        if (num_rows == 0) or (num_cols == 0):
            messagebox.showerror("Error", "Number of rows and columns have to be greater than 0")
            return

        topR = tk.Toplevel()
        topR.title("Random Matrix")

        # define frames on the window
        global frameR2
        global frameR4
        global frameR5
        frameR1 = tk.Frame(topR)
        frameR1.grid(row=0, column=0)
        frameR2 = tk.Frame(topR)
        frameR2.grid(row=0, column=1, padx=20)
        frameR3 = tk.Frame(topR)
        frameR3.grid(row=1, column=0, pady=20)
        frameR4 = tk.Frame(topR)
        frameR4.grid(row=1, column=1, padx=20, pady=20)
        frameR5 = tk.Frame(topR)
        frameR5.grid(row=0, column=2, padx=20, rowspan=2)

        # description label
        descriptionR = tk.Label(frameR1, text=("Specify intiger lower and higher bound for intigers in matrix:"))

        global lower_number
        global higher_number

        # entries
        lowerLabel = tk.Label(frameR1, text=("lower bound: "))
        higherLabel = tk.Label(frameR1, text=("higher bound: "))
        lower_number = tk.Entry(frameR1, width=10)
        lower_number.insert('end', 1)
        higher_number = tk.Entry(frameR1, width=10)
        higher_number.insert('end', 10)

        # put widgets on window
        descriptionR.grid(row=0, column=0, columnspan=2)
        lowerLabel.grid(row=1, column=0)
        lower_number.grid(row=1, column=1)
        higherLabel.grid(row=2, column=0)
        higher_number.grid(row=2, column=1)

        # matrix
        matrix_random = np.zeros((num_rows, num_cols))

        many_label = tk.Label(frameR3, text="How many: ")
        many_label.grid(row=0, column=0)

        # entry that will specify how many matrices do you want to create
        how_many = tk.Entry(frameR3, width=10)
        how_many.insert('end', 1)
        how_many.grid(row=0, column=1, pady=10)

        # button that will create a matrix
        b = tk.Button(frameR3, text='CREATE',
                      command=lambda: get_data_random(num_rows, num_cols, int(how_many.get())))
        b.grid(row=0, column=2, padx=20, pady=10)
        b.grid_columnconfigure(0, weight=1)

        # button which will launch hungarian method for minimal cost
        hungMin_button = tk.Button(frameR3, text="Hungarian Min",
                                   command=lambda: hung_method(lst_random, "min", "random"))
        hungMin_button.grid(row=1, column=0, columnspan=3, pady=5)
        hungMin_button.grid_columnconfigure(0, weight=1)

        # button which will launch hungarian method for maximum cost
        hungMax_button = tk.Button(frameR3, text="Hungarian max",
                                   command=lambda: hung_method(lst_random, "max", "random"))
        hungMax_button.grid(row=2, column=0, columnspan=3)
        hungMax_button.grid_columnconfigure(0, weight=1)

        # button that will close the window
        exit_button = tk.Button(frameR3, text="Exit", command=topR.destroy)
        exit_button.grid(row=4, column=0, columnspan=3, pady=10)


# CREATING WIDGETS ON ROOT WINDOW 
rowsLabel = tk.Label(root, text=("rows: "))
colsLabel = tk.Label(root, text=("cols: "))
rows = tk.Entry(root, width=10)
rows.insert('end', 3)
cols = tk.Entry(root, width=10)
cols.insert('end', 3)


custom_matrix_btn = tk.Button(root, text="Create Custom Matrix",
                              command=lambda: openwindow("custom"))
random_matrix_btn = tk.Button(root, text="Create Random Matrix",
                              command=lambda: openwindow("random"))


# WIDGET ON ROOT WINDOW
rowsLabel.grid(row=0, column=0)
rows.grid(row=0, column=1)
colsLabel.grid(row=0, column=2)
cols.grid(row=0, column=3)
custom_matrix_btn.grid(row=1, column=0, columnspan=4, pady=10)
random_matrix_btn.grid(row=2, column=0, columnspan=4)

# main loop
root.mainloop()
