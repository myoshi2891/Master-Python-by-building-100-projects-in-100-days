import tkinter

window = tkinter.Tk()
window.title("My First GUI App")
window.minsize(width=500, height=300)
window.config(padx=20, pady=20)


def button_clicked():
    print("Button clicked!")
    new_text = input.get()
    label.config(text=new_text)


# Label
label = tkinter.Label(text="Hello, World!", font=("Arial", 24, "bold"))
label["text"] = "Welcome to my GUI App!"
label.config(text="Welcome to my GUI App!")
label.grid(column=0, row=0)
label.config(padx=50, pady=50)

# Button
button = tkinter.Button(text="Click Me", command=button_clicked)
button.grid(column=1, row=1)
new_button = tkinter.Button(text="Click Me", command=button_clicked)
new_button.grid(column=0, row=2)

# Entry
input = tkinter.Entry(width=10)
print(input.get())
input.grid(column=3, row=2)

window.mainloop()
