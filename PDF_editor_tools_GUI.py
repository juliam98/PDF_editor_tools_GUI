import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font as tkfont
from PIL import ImageTk,Image 
from tkinter import filedialog
from tkmacosx import Button
import os

# code based on:
# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028

class General_setup(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # configure the root window
        self.title('PDF tools')
        self.geometry('550x500')
        self.title_font = tkfont.Font(family='Arial', size=25)
        self.text_font = tkfont.Font(family='Arial', size=18)
        self.bg_colour = '#BCB4F6'
        self.red = '#F6B6CF'

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, background=self.bg_colour)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create the stripe background image for decoration 
        self.canvas_4_stripes = Canvas(self, width = 550, height = 200, bg=self.bg_colour, highlightbackground=self.bg_colour)
        self.canvas_4_stripes.place(rely=1.012, relx=-0.01, anchor='sw')
        self.img_stripes = Image.open("stripes.png")
        self.img_stripes = self.img_stripes.resize((550, 200))
        self.img_stripes = ImageTk.PhotoImage(self.img_stripes)
        self.canvas_4_stripes.create_image(0,0, anchor=NW, image=self.img_stripes)

        self.frames = {}
        for F in (StartPage, Rotate_PDF, Merge_PDF):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
            frame.config(bg=self.bg_colour, highlightbackground=self.bg_colour)
        
        # Menu definition
        menubar = tk.Menu(self, bg='#b6d7a8')
        self.config(menu=menubar)
        menu_pdf_tools = tk.Menu(menubar, tearoff=False, bg='#b6d7a8', activebackground='#93c47d', type='normal')
        
        # add menu items to the File menu
        menu_pdf_tools.add_command(label='Rotate page', command=lambda: self.show_frame("Rotate_PDF"))
        menu_pdf_tools.add_command(label='Merge PDF files', command=lambda: self.show_frame("Merge_PDF"))
        menu_pdf_tools.add_separator()
        menu_pdf_tools.add_command(label='Main window', command=lambda: self.show_frame("StartPage"))
        menu_pdf_tools.add_separator()
        menu_pdf_tools.add_command(label='Exit', command=self.destroy)

        # add the File menu to the menubar
        menubar.add_cascade(label="PDF tools", menu=menu_pdf_tools)

        # create the Help menu
        help_menu = tk.Menu(menubar, tearoff=1)
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About...')
        menubar.add_cascade(label="Help", menu=help_menu)    

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", background='#BCB4F6')
        label.pack(side="top", fill="x", pady=10)

        button1 = Button(self, text="Go to \'Rotate page\'",
                            command=lambda: controller.show_frame("Rotate_PDF"), borderless=True)
        button2 = Button(self, text="Go to \'Merge PDF files\'", overrelief='sunken',
                            command=lambda: controller.show_frame("Merge_PDF"), borderless=True)
        button1.place(relx=0.5, rely=.15, anchor='center')
        button2.place(relx=0.5, rely=.25, anchor='center')


class Rotate_PDF(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the page for rotating page(s) in your PDF files", background='#BCB4F6')
        label.place(relx=.5, rely=.05, anchor='center')

        file_select_label = Label(self, text="Select file:", padx=20, background='#BCB4F6')
        file_select_label.place(relx=.5, rely=.15, anchor='e')

        file_select_button = Button(self, text="Browse files", command=lambda: self.select_files(self.text_entry), padx=20, justify='right', borderless=True)
        file_select_button.place(relx=.5, rely=.15, anchor='w')

        # Display the selected file
        list_files_label = Label(self, text="Your file:", padx=20, background='#BCB4F6')
        list_files_label.place(relx=.5, rely=.25,anchor='e')

        self.text_entry = StringVar(self, "nothng selected yet") # Empty string variablet which will be updated with user's entry 
        selected_file = Label(self, textvariable=self.text_entry, padx=0, wraplength=250, background='#BCB4F6')
        selected_file.place(relx=.5, rely=.25, anchor='w')

        # Choose angle of rotation
        rotate_by_label = Label(self, text="Rotate by:", background='#BCB4F6', padx=20)
        rotate_by_label.place(relx=0.5, rely=0.35, anchor='e')

        self.angle_var = tk.IntVar(None, value=90)
        R_90 = Radiobutton(self, text="90\N{DEGREE SIGN}", variable=self.angle_var, value=90, background='#BCB4F6', command=self.printResults)
        R_90.place(relx=.55, rely=.35, anchor='center')
        R_180 = Radiobutton(self, text="180\N{DEGREE SIGN}", variable=self.angle_var, value=180, background='#BCB4F6', command=self.printResults)
        R_180.place(relx=.65, rely=.35, anchor='center')
        R_270 = Radiobutton(self, text="270\N{DEGREE SIGN}", variable=self.angle_var, value=270, background='#BCB4F6', command=self.printResults)
        R_270.place(relx=.75, rely=.35, anchor='center')

        # Name of the new file
        new_filename = StringVar(None, "rotated_PDF")
        new_filename_label = Label(self, text='Name of the new file:', padx=20, background='#BCB4F6')
        new_filename_label.place(relx=0.5, rely=0.45, anchor='e')

        new_filename_entry = Entry(self, textvariable=new_filename, justify='right', background='#ddd9fc', highlightbackground='#BCB4F6')
        new_filename_entry.place(relx=0.5, rely=0.45, anchor='w', relwidth=.2)
        ext_label = Label(self, text='.pdf', padx=0, background='#BCB4F6')
        ext_label.place(relx=0.7, rely=0.45, anchor='w')

        file_select_button = Button(self, text="Return to main page", command=lambda: controller.show_frame("StartPage"), padx=0, justify='right', borderless=True, bg='#F6B6CF', overrelief='groove')
        file_select_button.place(relx=.5, rely=.55, anchor='e')

        file_select_button = Button(self, text="OK", command=None, padx=20, justify='right', borderless=True)
        file_select_button.place(relx=.5, rely=.55, anchor='w')

    def select_files(self, var):
        """
        This function definies filebrowser dialog assigned to a button widget.

        In the "main_window" the listbox widget "list_files_output" is updated to show the "file_path" variable(s) (i.e. path to the file(s))
        """
        filetypes = (
            ('excel', '*.xlsx'),
            ('photo', '*.png'),
            ('text files', '*.txt'))

        file_path = filedialog.askopenfilename(
            title='Open files',
            initialdir='/Users/juliamarcinkowska/Desktop/',
            filetypes=filetypes)
        
        filename = os.path.basename(file_path)

        var.set(filename)
        self.focus()
        return filename
    
    def printResults(self):
        print(self.angle_var.get())


class Merge_PDF(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page for merging two PDF files. Under construction", background='#BCB4F6', wraplength=300)
        label.place(relx=0.5, rely=0.1, anchor='center')

        button = Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"), borderless=True)
        button.place(relx=0.5, rely=0.2, anchor='center')


if __name__ == "__main__":
    app = General_setup()
    app.mainloop()