import customtkinter as ctk
import threading
import socket
import os
import PIL.Image
import pyautogui as pg
from Client import Client

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
   def __init__(self):
      super().__init__()
      self.cwd = os.getcwd()
      
      self.client = Client()

      #COnfigure Window
      self.title("TextShare")
      #self.iconbitmap( self.cwd + r"\bin\textshare.ico")

      #Configure Grid
   
      self.frame = ctk.CTkFrame(master=self, corner_radius=26)
      self.frame.pack(fill=ctk.BOTH, expand=True)

      self.frame.grid_columnconfigure(0)
      self.frame.grid_columnconfigure(1)
      self.frame.grid_columnconfigure(2)

      self.frame.grid_rowconfigure(0)
      self.frame.grid_rowconfigure(1)
      self.frame.grid_rowconfigure(2)

      self.btn_getText = ctk.CTkButton(master=self.frame, text="Get Text", command= self.getText)
      self.btn_getText.grid(row = 2, column = 0, sticky = "S", pady = 10, padx = 10)

      self.btn_getClipboard = ctk.CTkButton(master=self.frame, text="Get Clip", command= self.getClipboard)
      self.btn_getClipboard.grid(row = 2, column = 1, sticky = "S", pady = 10, padx = 10)

   def getText(self):
      self.client.Main("getText")
      
   def getClipboard(self):
      self.client.Main("getClipboard")

      #self.btn_stopServer = ctk.CTkButton(master=self.frame, text="Stop Server", command= self.server.stop)
      #self.btn_stopServer.grid(row = 2, column = 2, sticky = "S", pady = 10, padx = 10)

if __name__ == "__main__":
   app = App()

   app.mainloop()



#reset button: clears everything