import sqlite3
import predict
import subprocess
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True
from tkinter import filedialog as fd
from PIL import Image
from PIL import ImageTk

all_images=[]
def new_search():
        top.Entry1.delete(0,"end")
        top.Entry1.focus_set()
        top.Label1.place_forget()
        home_root.geometry('813x215')

def keyword_search():
    global all_images
    search_term=top.Entry1.get()
    top.Label1.place_forget()
    search_term=" ".join(search_term.split())
    search_terms=search_term.split(" ")
    valid_search=False
    for value in search_terms:
        if len(value)>=3:
            valid_search=True;
            break
        else:
            continue
    search_terms=[x for x in search_terms if len(x)>=3]
    if valid_search:
        top.tree.delete(*top.tree.get_children())
        top.Label2.place_forget()
        conn = sqlite3.connect('database/plant_database.db')
        c = conn.cursor()
        parameters=[]
        where_clauses=[]
        for word in search_terms:
            parameters.append("%"+word+"%")
            parameters.append("%"+word+"%")
            parameters.append("%"+word+"%")
            where_clauses.append(" keyword LIKE ?")
            where_clauses.append(" description LIKE ?")
            where_clauses.append(" family LIKE ?")
        parameters=tuple(parameters)
        query_string="SELECT DISTINCT plants_index.id,plants.common_name,\
                            plants.scientific_name,plants.image \
                                FROM plants_index INNER JOIN plants ON plants.id=plants_index.id WHERE"
        query_string+=(" OR".join(where_clauses))
        c.execute(query_string, parameters)
        rows = c.fetchall()
        rowcount=len(rows)
        if rowcount==0:
            home_root.geometry('813x215')
            top.Label2.place(x=145, y=110)
        else:
            for row in rows:
                img=Image.open("images/"+row[3])
                img=img.resize((60,60),Image.ANTIALIAS)
                preview=ImageTk.PhotoImage(img)
                all_images = all_images + [img, preview]
                top.tree.insert('', 'end', text=row[2],value=(row[1], row[0]),
                                             image=preview)
            home_root.geometry('813x400')
        conn.close()
    else:
        home_root.geometry('813x215')
        top.Label2.place(x=145, y=110)

def open_file():
    global all_images
    select_file=name= fd.askopenfilename(filetypes=[('Image files','.jpg'),('Image files','.jpeg')])
    img_file=Image.open(name)
    img_file=img_file.resize((150,150),Image.ANTIALIAS)
    thumbnail=ImageTk.PhotoImage(img_file)
    all_images = all_images + [img_file, thumbnail]
    top.Label1.configure(image=thumbnail)
    top.Label1.image=thumbnail
    top.Label1.place(x=540, y=55, height=150, width=150)
    return select_file

def image_search():
    global all_images
    top.Entry1.delete(0,"end")
    file_name=open_file()
    if file_name:
        predicted_class,confidence_score=predict.predict_class(file_name)
        if confidence_score>0.8:
            top.tree.delete(*top.tree.get_children())
            top.Label2.place_forget()
            conn = sqlite3.connect('database/plant_database.db')
            c = conn.cursor()
            parameters=(str(predicted_class),)
            c.execute("SELECT id,common_name,scientific_name,\
                      image FROM plants WHERE id=? LIMIT 1",parameters)
            rows = c.fetchall()
            rowcount=len(rows)
            if rowcount==0:
                home_root.geometry('813x215')
                top.Label2.place(x=550, y=110)
                top.Label1.place_forget()
            else:
                for row in rows:
                    img=Image.open("images/"+row[3])
                    img=img.resize((60,60),Image.ANTIALIAS)
                    preview=ImageTk.PhotoImage(img)
                    all_images = all_images + [img, preview]
                    top.tree.insert('', 'end', text=row[2],value=(row[1], row[0]),
                                    image=preview)
                conn.close()
                home_root.geometry('813x400')
        else:
            home_root.geometry('813x215')
            top.Label2.place(x=550, y=110)
            top.Label1.place_forget()
            
def launch_history():
    home_root.withdraw()
    history=subprocess.Popen(["pythonw","history.py"])
    history.wait()
    home_root.deiconify()

def start_gui():
    '''Starting point when module is the main routine.'''
    global home_root,top
    home_root = tk.Tk()
    top = Toplevel (home_root)
    home_root.mainloop()

class Toplevel:
    def OnDoubleClick(self, event):
        item = self.tree.selection()[0]
        item=self.tree.item(item)
        home_root.withdraw()
        view=subprocess.Popen(["pythonw","view.py",str(item['values'][1])])
        view.wait()
        home_root.deiconify()
        
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        self.style.theme_use('vista')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.bind('<Return>',lambda event:keyword_search())
        top.geometry("813x215+253+131")
        top.resizable(0, 0)
        top.title("Home")
        top.configure(highlightcolor="black")

        self.Entry1 = tk.Entry(top)
        self.Entry1.place(x=20, y=10,height=33, relwidth=0.45)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(relief="ridge")
        self.Entry1.configure(selectbackground="#c4c4c4")

        self.TButton1 = ttk.Button(top,command=keyword_search)
        self.TButton1.place(x=145, y=55, height=38, width=133)
        self.TButton1.configure(takefocus="")
        self.TButton1.configure(text='''Search''')

        self.TButton2 = ttk.Button(top,command=image_search)
        self.TButton2.place(x=550, y=10, height=38, width=133)
        self.TButton2.configure(takefocus="")
        self.TButton2.configure(text='Image Search')


        self.TSeparator1 = ttk.Separator(top)
        self.TSeparator1.place(relx=0.5, rely=-0.031, height=220)
        self.TSeparator1.configure(orient="vertical")


        self.Label1 = tk.Label(top)
        self.Label1.place(x=540, y=55, height=150, width=150)
        self.Label1.configure(activebackground="#f9f9f9")

        self.Label2 = tk.Label(top)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(text='''No results found.''')
        self.Label2.configure(fg="gray26")
        self.Label2.configure(font=("Book Antiqua",13,"italic","bold"))


        self.tree = ttk.Treeview(home_root, column=('#1','#2'), selectmode='browse',height=2)

        self.tree.place(relx=0.04,y=215,relwidth=0.9)

        verscrlbar = ttk.Scrollbar(home_root,
                                   orient ="vertical",
                                   command = self.tree.yview)
        verscrlbar.place(x=765, y=215, height=165)

        self.tree.configure(xscrollcommand = verscrlbar.set)

        self.style.configure('Treeview', rowheight=70)

        self.tree.heading('#0', text=' Scientific Name', anchor='center')
        self.tree.heading('#1', text=' Common Name', anchor='center')
        self.tree.heading('#2', text=' ID', anchor='center')


        self.tree.column('#0', anchor='center', minwidth=330,width=330,stretch=False)
        self.tree.column('#1', anchor='center', minwidth=330,width=330,stretch=False)
        self.tree.column('#2', anchor='center', minwidth=65,width=65,stretch=False)
        self.tree.bind("<Double-1>", self.OnDoubleClick)

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)

        self.searchmenu = tk.Menu(self.menubar, tearoff=0)
        self.searchmenu.add_command(label="New Text Search",command=new_search)
        self.searchmenu.add_command(label="New Image Search",command=image_search)
        self.menubar.add_cascade(label="Search", menu=self.searchmenu)

        self.extrasmenu = tk.Menu(self.menubar, tearoff=0)
        self.extrasmenu.add_command(label="View History",command=launch_history)
        self.menubar.add_cascade(label="Extras", menu=self.extrasmenu)
        self.extrasmenu.add_separator()
        top.configure(menu = self.menubar)

if __name__ == '__main__':
    start_gui()






