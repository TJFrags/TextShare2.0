import customtkinter as ctk
import pystray
import threading
import socket
import os
import PIL.Image
import pyautogui as pg
from appServer import Server

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
   def __init__(self):
      super().__init__()
      self.cwd = os.getcwd()
      
      self.server = Server(4444)

      #COnfigure Window
      self.title("TextShare")
      self.iconbitmap( self.cwd + r"\server\bin\textshare.ico")

      #Configure Grid
   
      self.frame = ctk.CTkFrame(master=self, corner_radius=26)
      self.frame.pack(fill=ctk.BOTH, expand=True)

      self.frame.grid_columnconfigure(0)
      self.frame.grid_columnconfigure(1)
      self.frame.grid_columnconfigure(2)

      self.frame.grid_rowconfigure(0)
      self.frame.grid_rowconfigure(1)
      self.frame.grid_rowconfigure(2)

      self.master_screen = ctk.CTkToplevel(self)
      self.master_screen.withdraw()
      self.master_screen.attributes("-transparent", "maroon3")
      self.picture_frame = ctk.CTkFrame(self.master_screen, bg_color="maroon3")
      self.picture_frame.pack(fill="both", expand="YES")

      self.snip_surface = ctk.CTkCanvas(self.picture_frame, cursor="cross", bg="grey11")
      self.snip_surface.pack(fill="both", expand="YES")

      self.lb_IP = ctk.CTkLabel(master=self.frame, text= "IP Adreas: 000.000.000.000")
      self.lb_IP.grid(row = 0, column = 0, pady = 10, padx = 10)

      self.txt_Port = ctk.CTkEntry(master=self.frame, width= 50, placeholder_text="Port",)
      self.txt_Port.grid(row = 0, column = 1, pady = 10, padx = 10)
      self.txt_Port.insert(0, "4444")

      self.btn_startServer = ctk.CTkButton(master=self.frame, text="Start Server", command= self.Start_server)
      self.btn_startServer.grid(row = 2, column = 0, sticky = "S", pady = 10, padx = 10)

      self.btn_changeRegeon = ctk.CTkButton(master=self.frame, text="Change regeon", command= self.Change_regeon)
      self.btn_changeRegeon.grid(row = 2, column = 1, sticky = "S", pady = 10, padx = 10)

      #self.btn_stopServer = ctk.CTkButton(master=self.frame, text="Stop Server", command= self.server.stop)
      #self.btn_stopServer.grid(row = 2, column = 2, sticky = "S", pady = 10, padx = 10)

   def display_rectangle_position(self):
      print(self.start_x)
      print(self.start_y)
      print(self.current_x)
      print(self.current_y)

   def on_button_release(self, event):
      self.display_rectangle_position()

      if self.start_x <= self.current_x and self.start_y <= self.current_y:
         print("right down")
         self.regeon = (self.start_x, self.start_y, self.current_x - self.start_x, self.current_y - self.start_y)

      elif self.start_x >= self.current_x and self.start_y <= self.current_y:
         print("left down")
         self.regeon = (self.current_x, self.start_y, self.start_x - self.current_x, self.current_y - self.start_y)

      elif self.start_x <= self.current_x and self.start_y >= self.current_y:
         print("right up")
         self.regeon = (self.start_x, self.current_y, self.current_x - self.start_x, self.start_y - self.current_y)

      elif self.start_x >= self.current_x and self.start_y >= self.current_y:
         print("left up")
         self.regeon = (self.current_x, self.current_y, self.start_x - self.current_x, self.start_y - self.current_y)
      
      self.server.update_regeon(self.regeon)
      self.master_screen.withdraw()
      self.deiconify()

   def on_snip_drag(self, event):
      self.current_x, self.current_y = (event.x, event.y)
      # expand rectangle as you drag the mouse
      self.snip_surface.coords(1, self.start_x, self.start_y, self.current_x, self.current_y)

   def on_button_press(self, event):
      # save mouse drag start position
      self.start_x = self.snip_surface.canvasx(event.x)
      self.start_y = self.snip_surface.canvasy(event.y)
      self.snip_surface.create_rectangle(0, 0, 1, 1, outline='red', width=3, fill="maroon3")
   
   def Change_regeon(self):
      print("Change Regeon: btn pressed")
      self.master_screen.deiconify()
      self.withdraw()

      self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
      self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
      self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

      self.master_screen.attributes('-fullscreen', True)
      self.master_screen.attributes('-alpha', .3)
      self.master_screen.lift()
      self.master_screen.attributes("-topmost", True)

   def Start_server(self):
      print(" Start: btn pressed")
      ip = socket.gethostbyname(socket.gethostname())
      self.lb_IP.configure(text = f"IP Adreas: {ip}")
      svr_thread = threading.Thread(target=self.server.Main, args=(int(self.txt_Port.get()),))
      svr_thread.start()

if __name__ == "__main__":
   app = App()

   # Define a function for quit the window
   def quit_window(icon, item):
      icon.stop()
      app.destroy()
      exit()

   # Define a function to show the window again
   def show_window(icon, item):
      icon.stop()
      app.after(0,app.deiconify())

   # Hide the window and show on the system taskbar
   def hide_window():
      app.withdraw()
      image=PIL.Image.open(app.cwd + r"\server\bin\textshare.ico")
      menu=(pystray.MenuItem('Quit', quit_window), pystray.MenuItem('Open', show_window))
      icon=pystray.Icon("name", image, "My System Tray Icon", menu)
      icon.run()

   app.protocol('WM_DELETE_WINDOW', hide_window)

   app.mainloop()



#reset button: clears everything