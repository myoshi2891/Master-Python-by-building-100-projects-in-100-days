import tkinter as tk
from typing import Any, cast

window: tk.Tk = tk.Tk()
window.title("Widget Examples")
window.minsize(width=500, height=500)

label: tk.Label = tk.Label(text="This is old text")
label.config(text="This is new text")
label.pack()


def action() -> None:
    print("Do something")


button: tk.Button = tk.Button(text="Click Me", command=action)
button.pack()

entry: tk.Entry = tk.Entry(width=30)
entry.insert(tk.END, "Some text to begin with.")
print(entry.get())
entry.pack()

text: tk.Text = tk.Text(height=5, width=30)
text.focus()
text.insert(tk.END, "Example of multi-line text entry.")
print(text.get("1.0", tk.END))
text.pack()


def spinbox_used() -> None:
    print(spinbox.get())


spinbox: tk.Spinbox = tk.Spinbox(from_=0, to=10, width=5, command=spinbox_used)
spinbox.pack()


def scale_used(value: Any) -> None:
    print(value)


scale: tk.Scale = tk.Scale(from_=0, to=100, command=scale_used)
scale.pack()


def checkbutton_used() -> None:
    print(checked_state.get())


checked_state: tk.IntVar = tk.IntVar()
checkbutton: tk.Checkbutton = tk.Checkbutton(
    text="Is On?", variable=checked_state, command=checkbutton_used
)
checkbutton.pack()


def radio_used() -> None:
    print(radio_state.get())


radio_state: tk.IntVar = tk.IntVar()
radiobutton1: tk.Radiobutton = tk.Radiobutton(
    text="Option1", value=1, variable=radio_state, command=radio_used
)
radiobutton2: tk.Radiobutton = tk.Radiobutton(
    text="Option2", value=2, variable=radio_state, command=radio_used
)
radiobutton1.pack()
radiobutton2.pack()


def listbox_used(event: tk.Event[tk.Listbox]) -> None:
    selection = cast(tuple[int, ...], listbox.curselection())
    if selection:
        index: int = selection[0]
        selected_item: str = cast(str, listbox.get(index))
        print(selected_item)


listbox: tk.Listbox = tk.Listbox(height=4)
fruits: list[str] = ["Apple", "Pear", "Orange", "Banana"]
for item in fruits:
    listbox.insert(tk.END, item)
listbox.bind("<<ListboxSelect>>", listbox_used)
listbox.pack()

window.mainloop()
