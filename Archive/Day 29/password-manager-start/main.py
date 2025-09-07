import tkinter as tk
from tkinter import messagebox
from random import choice, randint, shuffle

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    # password = ""
    # for char in password_list:
    #     password += char

    password = "".join(password_list)
    password_entry.delete(0, tk.END)  # 既存の内容をクリア
    password_entry.insert(0, password)
    # tkinterの内蔵クリップボード機能を使用
    window.clipboard_clear()
    window.clipboard_append(password)
    window.update()  # クリップボードの更新を確実にする

    print(f"Your password is: {password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if not website or not email or not password:
        messagebox.showwarning(
            title="Oops", message="Please make sure you've filled in all fields."
        )
        return
    else:
        is_ok = messagebox.askokcancel(
            title=website,
            message=f"There are the details you've entered:\nEmail: {email}\nPassword: {password}  \nDo you want to save this?",
        )

        if is_ok:
            with open("secret.txt", "a") as data_file:
                data_file.write(f"{website} | {email} | {password}\n")
                website_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)

            messagebox.showinfo(title="Success", message="Password saved!")


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = tk.Canvas(width=200, height=200)
logo_img = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = tk.Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = tk.Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = tk.Label(text="Password:")
password_label.grid(column=0, row=3)

# Entry
website_entry = tk.Entry(width=36)
website_entry.grid(column=1, row=1, columnspan=2)
website_entry.focus()
email_entry = tk.Entry(width=36)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "example@email.com")
password_entry = tk.Entry(width=21, show="*")
password_entry.grid(column=1, row=3)

# Buttons
generate_password_button = tk.Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)
add_button = tk.Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
