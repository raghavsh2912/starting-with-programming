import tkinter as tk

root=tk.Tk()
root.title("my fist app")
root.geometry("400x400")
root.config(bg="blue")
root.resizable(True,True)

tilte= tk.Label(root,text="my first app",font=("Arial",20),bg="black",fg="white")
btn=tk.Button(root,text="click me",font=("Arial",20),bg="red",fg="white")


root.mainloop()