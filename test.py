import tkinter as tk
from PIL import Image, ImageTk
import io
from datetime import datetime

from .wraplink_api import Wraplink, TransLinkAPIError
from .models import *

busapi = None

class WrapApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Next 33 Buses')
        self.geometry('480x360')
        self.resizable(False, False)

class WrapFrame(tk.Frame):
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        self.bus_schedule = None

        # Frame geometry setup
        self.grid(row=0, column=0, sticky='news')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Top row buttons and label
        self.get_buses_button = tk.Button(self, text='Update Now!')
        self.get_buses_button['command'] = self.get_buses_button_clicked
        self.get_buses_button.grid(row=0, column=0, padx=10, pady=10, sticky='NW')

        self.url_label = tk.Label(self, text="Click to start")
        self.url_label.grid(row=0, column=2, padx=10, pady=10, sticky='NSE')
        self.update()

        # Next row of another frame
        width = root.winfo_width()
        height = root.winfo_height()
        borderwidth = 5
        self.picture_frame = tk.Frame(self, borderwidth=borderwidth, relief='ridge', width=width, height=height)
        self.picture_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.picture_frame.update()
        self.picture_frame.rowconfigure(0, weight=1)
        self.picture_frame.columnconfigure(0, weight=1)

    def get_buses_button_clicked(self):
        self.bus_schedule = busapi.get_next_bus_arrivals(stop_num= 61127, get_count= 3, bus_num= 33)
        self.url_label.config(text="Last Updated: " + datetime.now().strftime('%I:%M %p'))
        
        # bus label stuff
        self.bus_label.delete(0,tk.END)
        self.bus_label.pack()
        self.bus_label = tk.Listbox(self.picture_frame, 
                height=3, 
                font=("Times New Roman", 48))
        self.bus_label.pack()               

        for i in range(len(self.bus_schedule)):
            bus_instance_formatted = datetime.strptime(self.bus_schedule[i], '%I:%M%p %Y-%m-%d').strftime('%I:%M %p')
            self.bus_label.insert(i+1, bus_instance_formatted)
        self.bus_label.pack()
                

if __name__ == '__main__':
    busapi = Wraplink()
    app = WrapApp()
    frame = WrapFrame(app)
    app.mainloop()