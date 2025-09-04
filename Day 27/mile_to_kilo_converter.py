# import tkinter

# window = tkinter.Tk()
# window.title("Miles to kilometers converter")
# # window.minsize(width=500, height=300)
# window.config(padx=20, pady=20)


# def miles_to_km():
#     miles = miles_input.get()
#     km = round(float(miles) * 1.609)
#     kilometer_result_label.config(text=f"{km}")

# # Entry
# miles_input = tkinter.Entry(width=7)
# miles_input.get()
# miles_input.grid(column=1, row=0)

# # Label
# miles_label = tkinter.Label(text="Miles", font=("Arial", 24))
# miles_label.grid(column=2, row=0)

# is_equal_label = tkinter.Label(text="is equal to", font=("Arial", 24))
# is_equal_label.grid(column=0, row=1)

# kilometer_result_label = tkinter.Label(text="0", font=("Arial", 24))
# kilometer_result_label.grid(column=1, row=1)

# kilometer_label = tkinter.Label(text="Km", font=("Arial", 24))
# kilometer_label.grid(column=2, row=1)


# # Button
# calculate_button = tkinter.Button(text="Calculate", command=miles_to_km)
# calculate_button.grid(column=1, row=2)


# window.mainloop()

import tkinter as tk
# from tkinter import ttk


class MileToKmConverter:
    """A GUI application to convert miles to kilometers."""

    MILES_TO_KM_RATIO = 1.609344

    def __init__(self):
        self.window = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.layout_widgets()

    def setup_window(self):
        """Configure the main window properties."""
        self.window.title("Miles to Kilometers Converter")
        self.window.config(padx=20, pady=20)
        self.window.resizable(False, False)

    def create_widgets(self):
        """Create all GUI widgets."""
        # Entry widget for miles input
        self.miles_input = tk.Entry(width=10, font=("Arial", 14), justify="center")

        # Labels
        self.miles_label = tk.Label(text="Miles", font=("Arial", 16))
        self.is_equal_label = tk.Label(text="is equal to", font=("Arial", 16))
        self.kilometer_result_label = tk.Label(text="0", font=("Arial", 16, "bold"))
        self.kilometer_label = tk.Label(text="Km", font=("Arial", 16))

        # Button
        self.calculate_button = tk.Button(
            text="Calculate",
            command=self.miles_to_km,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5,
        )

        # Bind Enter key to calculation
        self.miles_input.bind("<Return>", lambda event: self.miles_to_km())

    def layout_widgets(self):
        """Arrange widgets using grid layout."""
        # Row 0: Miles input and label
        self.miles_input.grid(column=1, row=0, padx=5, pady=5)
        self.miles_label.grid(column=2, row=0, padx=5, pady=5)

        # Row 1: Result display
        self.is_equal_label.grid(column=0, row=1, padx=5, pady=5)
        self.kilometer_result_label.grid(column=1, row=1, padx=5, pady=5)
        self.kilometer_label.grid(column=2, row=1, padx=5, pady=5)

        # Row 2: Calculate button
        self.calculate_button.grid(column=1, row=2, padx=5, pady=10)

    def miles_to_km(self):
        """Convert miles to kilometers and update the result label."""
        try:
            miles = float(self.miles_input.get())
            km = round(miles * self.MILES_TO_KM_RATIO, 2)
            self.kilometer_result_label.config(text=str(km))
        except ValueError:
            self.kilometer_result_label.config(text="Invalid input")

    def run(self):
        """Start the GUI application."""
        # Focus on input field and start the main loop
        self.miles_input.focus()
        self.window.mainloop()


if __name__ == "__main__":
    app = MileToKmConverter()
    app.run()

# ## Key Improvements Made:

# 1. **Object-Oriented Design**: Converted to a class-based structure for better organization and reusability.

# 2. **Error Handling**: Added try-except block to handle invalid input gracefully.

# 3. **Constants**: Used a more precise conversion ratio as a class constant.

# 4. **Better Styling**: 
#    - Improved fonts and sizing
#    - Added button styling with colors
#    - Better spacing with padding

# 5. **Enhanced User Experience**:
#    - Enter key binding for quick calculation
#    - Input field gets focus on startup
#    - Centered text in input field
#    - More precise decimal results

# 6. **Code Organization**:
#    - Separated concerns into different methods
#    - Clear method names and documentation
#    - Proper imports with aliases

# 7. **Maintainability**:
#    - Easy to modify styling and layout
#    - Clear separation of widget creation and layout
#    - Documented methods

# 8. **Robustness**:
#    - Window is not resizable to maintain layout
#    - Better error handling for edge cases

# The refactored code is more professional, maintainable, and user-friendly while preserving all the original functionality.