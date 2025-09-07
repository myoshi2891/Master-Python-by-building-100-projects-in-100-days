import tkinter as tk
from tkinter import messagebox
from random import choice, randint, shuffle
from typing import Optional
import os
import string


class PasswordManager:
    """A GUI-based password manager application."""

    # Constants
    WINDOW_TITLE = "Password Manager"
    WINDOW_PADDING = 50
    CANVAS_SIZE = (200, 200)
    ENTRY_WIDTH = 36
    PASSWORD_ENTRY_WIDTH = 21
    DATA_FILE = "secret.txt"
    LOGO_FILE = "logo.png"

    def __init__(self) -> None:
        """Initialize the Password Manager application."""
        self.window = tk.Tk()

        # Initialize widgets as None first, then create them
        self.canvas: tk.Canvas
        self.logo_img: Optional[tk.PhotoImage] = None

        # Entry widgets
        self.website_entry: tk.Entry
        self.email_entry: tk.Entry
        self.password_entry: tk.Entry

        # Label widgets
        self.website_label: tk.Label
        self.email_label: tk.Label
        self.password_label: tk.Label

        # Button widgets
        self.generate_password_button: tk.Button
        self.add_button: tk.Button

        self._setup_window()
        self._create_widgets()
        self._setup_layout()

    def _setup_window(self) -> None:
        """Configure the main window."""
        self.window.title(self.WINDOW_TITLE)
        self.window.config(padx=self.WINDOW_PADDING, pady=self.WINDOW_PADDING)

    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        self._create_canvas()
        self._create_labels()
        self._create_entries()
        self._create_buttons()

    def _create_canvas(self) -> None:
        """Create and configure the canvas with logo."""
        self.canvas = tk.Canvas(width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self._load_logo_image()

    def _load_logo_image(self) -> None:
        """Load the logo image with error handling."""
        try:
            possible_paths = [
                self.LOGO_FILE,
                f"./{self.LOGO_FILE}",
                os.path.join(os.path.dirname(__file__), self.LOGO_FILE),
            ]

            image_loaded = False
            for path in possible_paths:
                if os.path.exists(path):
                    self.logo_img = tk.PhotoImage(file=path)
                    self.canvas.create_image(100, 100, image=self.logo_img)
                    image_loaded = True
                    break

            if not image_loaded:
                self._create_fallback_logo()

        except tk.TclError as e:
            print(f"Error loading logo image: {e}")
            self._create_fallback_logo()

    def _create_fallback_logo(self) -> None:
        """Create a simple fallback logo if image loading fails."""
        self.canvas.create_rectangle(50, 50, 150, 150, fill="lightblue", outline="blue")
        self.canvas.create_text(100, 100, text="🔐", font=("Arial", 24))

    def _create_labels(self) -> None:
        """Create all label widgets."""
        self.website_label = tk.Label(text="Website:")
        self.email_label = tk.Label(text="Email/Username:")
        self.password_label = tk.Label(text="Password:")

    def _create_entries(self) -> None:
        """Create all entry widgets."""
        self.website_entry = tk.Entry(width=self.ENTRY_WIDTH)
        self.email_entry = tk.Entry(width=self.ENTRY_WIDTH)
        self.password_entry = tk.Entry(width=self.PASSWORD_ENTRY_WIDTH, show="*")

        # Set default email
        self.email_entry.insert(0, "example@email.com")

    def _create_buttons(self) -> None:
        """Create all button widgets."""
        self.generate_password_button = tk.Button(
            text="Generate Password", command=self.generate_password
        )
        self.add_button = tk.Button(
            text="Add", width=self.ENTRY_WIDTH, command=self.save_password
        )

    def _setup_layout(self) -> None:
        """Configure the grid layout for all widgets."""
        # Canvas
        self.canvas.grid(column=1, row=0)

        # Labels
        self.website_label.grid(column=0, row=1)
        self.email_label.grid(column=0, row=2)
        self.password_label.grid(column=0, row=3)

        # Entries
        self.website_entry.grid(column=1, row=1, columnspan=2)
        self.website_entry.focus()
        self.email_entry.grid(column=1, row=2, columnspan=2)
        self.password_entry.grid(column=1, row=3)

        # Buttons
        self.generate_password_button.grid(column=2, row=3)
        self.add_button.grid(column=1, row=4, columnspan=2)

    def generate_password(self) -> None:
        """Generate a secure random password and insert it into the password entry."""
        try:
            # Use string module for cleaner character sets
            letters = string.ascii_letters
            numbers = string.digits
            symbols = "!#$%&()*+"

            # Generate password components
            password_letters = [choice(letters) for _ in range(randint(8, 10))]
            password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
            password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

            # Combine and shuffle
            password_list = password_letters + password_symbols + password_numbers
            shuffle(password_list)

            password = "".join(password_list)

            # Update password entry
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)

            # Copy to clipboard
            self._copy_to_clipboard(password)

            print(f"Generated password: {password}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {e}")

    def _copy_to_clipboard(self, text: str) -> None:
        """Copy text to clipboard with error handling."""
        try:
            self.window.clipboard_clear()
            self.window.clipboard_append(text)
            self.window.update()
        except Exception as e:
            print(f"Failed to copy to clipboard: {e}")

    def save_password(self) -> None:
        """Save the password data to file after validation."""
        website = self.website_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        # Validate input
        if not self._validate_input(website, email, password):
            return

        # Confirm save
        if not self._confirm_save(website, email, password):
            return

        # Save to file
        if self._save_to_file(website, email, password):
            self._clear_entries()
            messagebox.showinfo("Success", "Password saved successfully!")

    def _validate_input(self, website: str, email: str, password: str) -> bool:
        """Validate that all required fields are filled."""
        if not website or not email or not password:
            messagebox.showwarning(
                "Missing Information", "Please make sure you've filled in all fields."
            )
            return False
        return True

    def _confirm_save(self, website: str, email: str, password: str) -> bool:
        """Show confirmation dialog before saving."""
        return messagebox.askokcancel(
            title=website,
            message=f"These are the details you've entered:\n"
            f"Website: {website}\n"
            f"Email: {email}\n"
            f"Password: {password}\n\n"
            f"Do you want to save this?",
        )

    def _save_to_file(self, website: str, email: str, password: str) -> bool:
        """Save password data to file with error handling."""
        try:
            with open(self.DATA_FILE, "a", encoding="utf-8") as data_file:
                data_file.write(f"{website} | {email} | {password}\n")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save password: {e}")
            return False

    def _clear_entries(self) -> None:
        """Clear website and password entries after successful save."""
        self.website_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.website_entry.focus()

    def run(self) -> None:
        """Start the application main loop."""
        self.window.mainloop()


def main() -> None:
    """Main function to run the Password Manager application."""
    app = PasswordManager()
    app.run()


if __name__ == "__main__":
    main()
