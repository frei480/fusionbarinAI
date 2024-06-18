import tkinter as tk
from tkinter import ttk
from base64 import b64decode
from threading import Thread, Event
from fusionbrainai import Text2ImageAPI

from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        
        self.root = tk.Tk()
        
        self.frame = tk.Frame(self.root)
        self.frame.grid()
        
        self.root.title('Some title')
               
        self.btn_load = ttk.Button(self.frame, text="load", command=self.my_event_handler)
        self.btn_load.grid(row=1, column=0)
        self.btn_exit = ttk.Button(self.frame, text="Exit")
        self.btn_exit.grid(row=1, column=1)
        
        self.text_prompt = tk.Text(self.frame, height=1, width=40, font='Arial')
        self.text_prompt.grid(row=1, column=2)
        
        self.l = tk.Label(text = " ", width=30)
        self.l.grid(row=1, column=3)
        self.canvas = tk.Canvas(self.root, height=700, width=700)
        
        self.canvas.grid(row=2, column=0)
        self.root.mainloop()
        
    def my_event_handler(self):
        prompt = 'нарисуй для игры что "нарисовано": ' + self.text_prompt.get('1.0', "end-1c")
        self.btn_load.config(state=tk.DISABLED)
        done = Event()
        load_thread = Thread(target=self.get_images, args=[prompt, done])
        load_thread.start()
        print('sssstart!')

    def get_images(self, prompt:str, done: Event):
    #region Api
        api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'AF82BFE424490361D2DF67D858452645', '')
    #endregion
        model_id = api.get_model()
        uuid = api.generate(prompt, model_id)
        images = api.check_generation(uuid)
        done.set()
        self.images = images
        self.btn_load.config(state=tk.NORMAL)        
        self.photo = ImageTk.PhotoImage(data=b64decode(self.images[0]))
        self.c_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)


app = App()



