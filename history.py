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
import subprocess

all_images=[]
def load_history():
    global all_images,top
    top.tree.delete(*top.tree.get_children())
    conn = sqlite3.connect('database/plant_database.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT plants.id,plants.image,plants.scientific_name,plants.common_name,history.access_time FROM history INNER JOIN plants ON history.id=plants.id ORDER BY history.access_time DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    rowcount=len(rows)
    if rowcount>0:
        for row in rows:
            img=Image.open("images/"+row[1])
            img=img.resize((60,60),Image.ANTIALIAS)
            preview=ImageTk.PhotoImage(img)
            all_images = all_images + [img, preview]
            top.tree.insert('', 'end', text=row[2],value=(row[3], row[0],row[4]),
                                             image=preview)
def start_gui():
    '''Starting point when module is the main routine.'''
    global history_root,top
    history_root = tk.Tk()
    top = Toplevel (history_root)
    load_history()
    history_root.mainloop()

class Toplevel:
    def OnDoubleClick(self, event):
        item = self.tree.selection()[0]
        item=self.tree.item(item)
        history_root.withdraw()
        view=subprocess.Popen(["pythonw","view.py",str(item['values'][1])])
        view.wait()
        history_root.deiconify()
        load_history()
        
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

        top.geometry("813x400+253+131")
        top.resizable(0, 0)
        top.title("History")
        top.configure(highlightcolor="black")

        self.tree = ttk.Treeview(history_root, column=('#1','#2','#3'), selectmode='browse',height=2)

        self.tree.place(relx=0.04,y=40,relwidth=0.9,relheight=0.8)

        verscrlbar = ttk.Scrollbar(history_root,
                                   orient ="vertical",
                                   command = self.tree.yview)
        verscrlbar.place(x=765, y=40, relheight=0.8)

        self.tree.configure(xscrollcommand = verscrlbar.set)
        self.style.configure('Treeview', rowheight=70)

        self.tree.heading('#0', text='Scientific Name', anchor='center')
        self.tree.heading('#1', text='Common Name', anchor='center')
        self.tree.heading('#2', text='ID', anchor='center')
        self.tree.heading('#3', text='Last Viewed', anchor='center')

        self.tree.column('#0', anchor='center', minwidth=260,width=260,stretch=False)
        self.tree.column('#1', anchor='center', minwidth=260,width=260,stretch=False)
        self.tree.column('#2', anchor='center', minwidth=65,width=65,stretch=False)
        self.tree.column('#3', anchor='center', minwidth=140,width=140,stretch=False)
        self.tree.bind("<Double-1>", self.OnDoubleClick)

if __name__ == '__main__':
    start_gui()






