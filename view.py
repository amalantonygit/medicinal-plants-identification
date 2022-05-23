import sys
import sqlite3
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
from PIL import Image
from PIL import ImageTk

all_images=[]
def start_gui():
    '''Starting point when module is the main routine.'''
    global root
    view_root = tk.Tk()
    top = Toplevel (view_root)
    view_root.mainloop()

class Toplevel:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        self.style.theme_use('vista')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("600x450+346+134")
        top.minsize(1, 1)
        top.maxsize(1351, 738)
        top.resizable(1, 1)
        top.configure(highlightcolor="black")

        self.Label1 = tk.Label(top,relief="raised")
        self.Label1.place(relx=0.075, rely=0.044, height=150, width=150)
        self.Label1.configure(activebackground="#f9f9f9")

        self.Label4 = tk.Label(top,justify=tk.LEFT,anchor="w",font=(None,11,"italic"))
        self.Label4.place(relx=0.33, rely=0.100, height=25)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(text='''Common Name''')

        self.Label5 = tk.Label(top,justify=tk.LEFT,anchor="w",font=(None,12,"bold"))
        self.Label5.place(relx=0.53, rely=0.100, height=25)
        self.Label5.configure(activebackground="#f9f9f9")

        self.Label6 = tk.Label(top,justify=tk.LEFT,anchor="w",font=(None,11,"italic"))
        self.Label6.place(relx=0.33, rely=0.175, height=25)
        self.Label6.configure(activebackground="#f9f9f9")
        self.Label6.configure(text='''Species Name''')

        self.Label7 = tk.Label(top,justify=tk.LEFT,anchor="w",font=(None,12,"bold"))
        self.Label7.place(relx=0.53, rely=0.175, height=25)
        self.Label7.configure(activebackground="#f9f9f9")

        self.Label8 = tk.Label(top,justify=tk.LEFT,anchor="w",font=(None,11,"italic"))
        self.Label8.place(relx=0.33, rely=0.250, height=25)
        self.Label8.configure(activebackground="#f9f9f9")
        self.Label8.configure(text='''Family''')

        self.Label9 = tk.Label(top,justify=tk.LEFT,anchor="w",font=(None,12,"bold"))
        self.Label9.place(relx=0.53, rely=0.250, height=25)
        self.Label9.configure(activebackground="#f9f9f9")

        self.Label10 = tk.Label(top,justify=tk.LEFT,anchor="w",font=(None,11,"italic"))
        self.Label10.place(relx=0.075, rely=0.400, height=25)
        self.Label10.configure(activebackground="#f9f9f9")
        self.Label10.configure(text='''Description''')

        self.Scrolledtext1 = ScrolledText(top,font = ("Times New Roman",13))
        self.Scrolledtext1.place(relx=0.075, rely=0.465, relheight=0.45
                , relwidth=0.837)
        self.Scrolledtext1.configure(background="white")
        self.Scrolledtext1.configure(insertborderwidth="3")
        self.Scrolledtext1.configure(selectbackground="#c4c4c4")
        self.Scrolledtext1.configure(wrap="word")



        #fetch plant details
        parameters=(sys.argv[1],)
        conn = sqlite3.connect('database/plant_database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM plants WHERE id=? LIMIT 1",parameters)
        for row in c:
            self.Label5.configure(text=row[1])
            self.Label7.configure(text=row[2])
            self.Label9.configure(text=row[3])
            img=Image.open("images/"+row[5])
            img=img.resize((150,150),Image.ANTIALIAS)
            preview=ImageTk.PhotoImage(img)
            global all_images
            all_images+=(img,preview)
            self.Label1.configure(image=preview)
            self.Scrolledtext1.config(tabs=(40,))
            plant_description=row[4].split("\n")
            plant_data="\t"
            for _ in plant_description:
                plant_data+=(_+"\n\t")
            self.Scrolledtext1.insert(tk.INSERT,plant_data)
            self.Scrolledtext1.configure(state ='disabled')
            top.title(row[2])

class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass

        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        else:
            methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
                  + tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledText(AutoScroll, tk.Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')

if __name__ == '__main__':
    parameters=(sys.argv[1],)
    connection = sqlite3.connect('database/plant_database.db', timeout=10)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM history WHERE id=? ",parameters)
        rows = cursor.fetchall()
        rowcount=len(rows)
        if rowcount>0:
            cursor.execute("UPDATE history SET access_time =datetime('now','localtime') WHERE id=?",parameters)
        else:
            cursor.execute("INSERT INTO history VALUES(?,datetime('now','localtime')) ",parameters)
        connection.commit()
    except sqlite3.OperationalError:
        print("database locked")
    start_gui()





