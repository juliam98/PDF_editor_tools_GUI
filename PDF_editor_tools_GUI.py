import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import font as tkfont
from PIL import ImageTk,Image 
from tkinter import filedialog
from tkmacosx import Button
import os
from PyPDF2 import PdfReader, PdfWriter

# code based on:
# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028

class General_setup(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # configure the root window
        self.title('PDF tools')
        self.geometry('600x600')
        self.minsize(600, 600)
        self.defaultFont = tkfont.nametofont("TkDefaultFont")
        self.defaultFont.config(family='Arial', size=16)
        style = ttk.Style()
        
        self.bg_colour = '#6DAEDB'
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
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tk_setPalette(self.bg_colour)
            frame.config(bg=self.bg_colour)
    
        # Menu definition
        menubar = tk.Menu(self, bg='#b6d7a8')
        self.config(menu=menubar)
        menu_pdf_tools = tk.Menu(menubar, tearoff=False, type='normal')
        
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
        label = tk.Label(self, text="This is the start page")
        label.place(relx=.5, rely=.045, anchor='center')

        button1 = Button(self, text="Go to \'Rotate page\'", padx=20,
                            command=lambda: controller.show_frame("Rotate_PDF"), borderless=True)
        button2 = Button(self, text="Go to \'Merge PDF files\'", overrelief='sunken',
                            command=lambda: controller.show_frame("Merge_PDF"), borderless=True)
        button1.place(relx=0.5, rely=.15, anchor='center')
        button2.place(relx=0.5, rely=.25, anchor='center')


class Rotate_PDF(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Window title
        label = tk.Label(self, text="Rotate individual pages in a PDF file", font=('Arial', 20))
        label.place(relx=.5, rely=.045, anchor='center')

        # Select files: Label
        file_select_label = tk.Label(self, text="Select file:", padx=20)
        file_select_label.place(relx=.5, rely=.15, anchor='e')

        # Select files: Filebrowser button
        file_select_button = Button(self, text="Browse files", command=lambda: self.select_files(self.path_entry), padx=20, justify='right', borderless=True)
        file_select_button.place(relx=.5, rely=.15, anchor='w')

        # Select files: "Your file:" label 
        list_files_label = tk.Label(self, text="Your file:", padx=20)
        list_files_label.place(relx=.5, rely=.2,anchor='e')

        self.path_entry = StringVar(self, "no file selected yet") # Placeholder value to which selected path will be assigned

        # Select files: Display the selected file
        self.selected_file = tk.Label(self, textvariable=self.path_entry, padx=20) # selected file will replace this label text
        self.selected_file.place(relx=.5, rely=.2, anchor='w')

        # Rotation angle: Label
        rotate_by_label = tk.Label(self, text="Rotate by:", padx=20)
        rotate_by_label.place(relx=0.5, rely=0.25, anchor='e')

        self.angle_var = tk.IntVar(None, value=90) # Placeholder value to which angle of rotation will be assigned

        # Rotation angle: Choose angle of rotation
        R_90 = tk.Radiobutton(self, text="90\N{DEGREE SIGN}", variable=self.angle_var, value=90)
        R_90.place(relx=.55, rely=.25, anchor='center')
        R_180 = tk.Radiobutton(self, text="180\N{DEGREE SIGN}", variable=self.angle_var, value=180)
        R_180.place(relx=.65, rely=.25, anchor='center')
        R_270 = tk.Radiobutton(self, text="270\N{DEGREE SIGN}", variable=self.angle_var, value=270)
        R_270.place(relx=.75, rely=.25, anchor='center')

        # Name of the new file
        self.new_filename = tk.StringVar(None, "rotated_PDF") # Placeholder value to which angle of rotation will be assigned, default value is "rotated_PDF"
        # Name of the new file: Label
        new_filename_label = tk.Label(self, text='Name of the new file:', padx=20)
        new_filename_label.place(relx=0.5, rely=0.3, anchor='e')

        # Name of the new file: Entry box
        new_filename_entry = tk.Entry(self, justify='right', background='#ffffff', textvariable=self.new_filename)
        new_filename_entry.place(relx=0.5, rely=0.3, anchor='w', relwidth=.2)
        # Name of the new file: label with ".pdf" extension to let the user know that filename should be typed without the extensions
        ext_label = tk.Label(self, text='.pdf', padx=0)
        ext_label.place(relx=0.7, rely=0.3, anchor='w')

        # Pages to rotate
        self.pages_to_rotate = StringVar(self, "1") # Placeholder value which angle of rotation will be assigned
        # Pages to rotate: Label
        pages_to_rotate_label = tk.Label(self, text='Pages to rotate', padx=20)
        pages_to_rotate_label.place(relx=0.5, rely=0.35, anchor='e')
        # Pages to rotate: Entry
        self.pages_to_rotate_entry = tk.Entry(self, justify='left', background='#ffffff', textvariable=self.pages_to_rotate)
        self.pages_to_rotate_entry.place(relx=0.5, rely=0.35, anchor='w', relwidth=.2)

        # General page buttons: Return to main page
        file_select_button = Button(self, text="Return to main page", command=lambda: controller.show_frame("StartPage"), padx=0, justify='right', borderless=True, overrelief='groove')
        file_select_button.place(relx=.5, rely=.45, anchor='e')
        # General page buttons: OK (submits the entry)
        file_select_button = Button(self, text="OK", command=self.rotate_pdf_pages, padx=20, justify='right', borderless=True)
        file_select_button.place(relx=.5, rely=.45, anchor='w')

        self.output_text = StringVar(self, "") # Placeholder value to which new filename and path where file was saved will be assigned when "OK" button is clicked
        # Message (from output_text variable) that is displayed after "OK" is clicked to inform the user that their PDF was saved
        output_text_label = tk.Label(self, textvariable=self.output_text, wraplength=500, fg='#ffffff')
        output_text_label.place(relx=.5, rely=.55, anchor="center")

    def select_files(self, var):
        """
        This function definies filebrowser dialog assigned to a button widget.
        """
        filetypes = (
            ('PDFs', '*.pdf'),
            ('text files', '*.txt'))

        file_path = filedialog.askopenfilename(
            title='Open files',
            initialdir='',
            filetypes=filetypes)
        
        var.set(file_path)
        self.focus()

        return file_path

    def rotate_pdf_pages(self):
        # create output path (same directory as original file + filename)
        out_path = os.path.dirname(self.path_entry.get()) + "/" + self.new_filename.get() + ".pdf"

        # get page numbers to rotate
        self.pages_no = [int(num) for num in (self.pages_to_rotate_entry.get()).split(",")]

        try:
            with open(self.path_entry.get(), 'rb') as file:
                reader = PdfReader(file)
                writer = PdfWriter()

                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num] # all pages in the selected pdf is assigned to the variable "page"

                    if page_num + 1 in self.pages_no: # since python indexes from 0
                        page.rotate(self.angle_var.get()) 
                
                    writer.add_page(page)

                with open(out_path, "wb") as out_path:
                    writer.write(out_path)
        
            self.output_text.set("\"" + self.new_filename.get() + ".pdf" + "\"" + " was saved in " + os.path.dirname(self.path_entry.get()) + "/")
        
        except FileNotFoundError:
            self.selected_file.configure(background='#EE9D9D')
            self.selected_file.after(750, lambda: self.selected_file.configure(background='#6DAEDB'))

        
class Merge_PDF(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page for merging two PDF files. Under construction", background='#6DAEDB', wraplength=300)
        label.place(relx=0.5, rely=0.1, anchor='center')

        button = Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"), borderless=True)
        button.place(relx=0.5, rely=0.2, anchor='center')


if __name__ == "__main__":
    app = General_setup()
    app.mainloop()