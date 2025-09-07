# Password Managerアプリケーションのクラスベース設計へのリファクタリング、型安全性とエラーハンドリングを改善

## 主なリファクタリング内容

### 1. **クラスベース設計**

- 全ての機能を `PasswordManager` クラスにカプセル化
- グローバル変数を排除し、インスタンス変数として管理
- メソッドの責任を明確に分離

### 2. **型ヒントの追加**

- 全ての関数とメソッドに適切な型ヒントを追加
- `Dict[str, Any]` でJSONデータの型を明示
- `Optional` 型を使用して null許容性を明確化

### 3. **エラーハンドリングの大幅改善**

- 画像ファイルが見つからない場合のフォールバック機能
- JSONファイルの破損に対する対応
- 各操作での例外処理とユーザーフレンドリーなエラーメッセージ

### 4. **バリデーション機能の追加**

- フォームデータの検証を専用メソッドで実装
- 空文字列や無効な入力のチェック
- 保存前の確認ダイアログ

### 5. **コードの構造化と分離**

- UI作成を複数のメソッドに分割（`_create_widgets`, `_setup_layout`など）
- データ操作を専用メソッドに分離（`_load_data`, `_save_data`）
- プライベートメソッド（`_`プレフィックス）の適切な使用

### 6. **定数の使用**

- マジックナンバーを定数として定義
- 設定値の変更が容易
- コードの可読性向上

### 7. **ユーザビリティの向上**

- パスワード生成時にクリップボードコピーの通知
- 検索時にパスワードを自動的にクリップボードにコピー
- より詳細な成功/エラーメッセージ

### 8. **レイアウトの改善**

- `sticky`オプションを使用したより良いウィジェット配置
- 適切なパディングとスペーシング
- ウィンドウサイズの固定

### 9. **保守性の向上**

- 機能ごとの明確な分離
- 新機能の追加が容易
- テストしやすい構造
- 設定の変更が簡単

### 10. **セキュリティの向上**

- `string`モジュールを使用したより安全な文字セット
- 入力データのサニタイゼーション（`strip()`）
- より強固なパスワード生成アルゴリズム

この設計により、コードはより保守しやすく、拡張しやすく、エラーに強く、ユーザーフレンドリーになりました。

```python
import tkinter as tk
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip  # type: ignore
import json
from typing import Dict, Any, Optional
import string
import os


class PasswordManager:
    """Password Manager Application with GUI interface."""

    # Class constants
    DEFAULT_EMAIL = "test@example.com"
    DATA_FILE = "data.json"
    LOGO_FILE = "logo.png"

    # Password generation settings
    PASSWORD_LETTERS_RANGE = (8, 10)
    PASSWORD_SYMBOLS_RANGE = (2, 4)
    PASSWORD_NUMBERS_RANGE = (2, 4)

    def __init__(self) -> None:
        """Initialize the Password Manager application."""
        self.window = tk.Tk()
        self._setup_window()
        self._create_widgets()
        self._setup_layout()

    def _setup_window(self) -> None:
        """Configure the main window properties."""
        self.window.title("Password Manager")
        self.window.config(padx=50, pady=50)
        self.window.resizable(False, False)

    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        self._create_canvas()
        self._create_labels()
        self._create_entries()
        self._create_buttons()

    def _create_canvas(self) -> None:
        """Create and configure the canvas with logo."""
        self.canvas = tk.Canvas(height=200, width=200)

        # Try to load logo with error handling
        try:
            if os.path.exists(self.LOGO_FILE):
                self.logo_img = tk.PhotoImage(file=self.LOGO_FILE)
                self.canvas.create_image(100, 100, image=self.logo_img)
            else:
                # Fallback: create a simple text logo
                self.canvas.create_text(100, 100, text="🔐", font=("Arial", 48))
        except tk.TclError:
            # If image loading fails, show text fallback
            self.canvas.create_text(100, 100, text="Password\nManager",
                                  font=("Arial", 14), justify="center")

    def _create_labels(self) -> None:
        """Create all label widgets."""
        self.website_label = tk.Label(text="Website:")
        self.email_label = tk.Label(text="Email/Username:")
        self.password_label = tk.Label(text="Password:")

    def _create_entries(self) -> None:
        """Create all entry widgets."""
        self.website_entry = tk.Entry(width=21)
        self.email_entry = tk.Entry(width=35)
        self.password_entry = tk.Entry(width=21)

        # Set default values
        self.email_entry.insert(0, self.DEFAULT_EMAIL)
        self.website_entry.focus()

    def _create_buttons(self) -> None:
        """Create all button widgets."""
        self.search_button = tk.Button(
            text="Search",
            command=self.search_password,
            width=13
        )
        self.generate_password_button = tk.Button(
            text="Generate Password",
            command=self.generate_password
        )
        self.add_button = tk.Button(
            text="Add",
            width=36,
            command=self.save_password
        )

    def _setup_layout(self) -> None:
        """Arrange all widgets using grid layout."""
        # Canvas
        self.canvas.grid(row=0, column=1)

        # Labels
        self.website_label.grid(row=1, column=0, sticky="e", padx=(0, 5))
        self.email_label.grid(row=2, column=0, sticky="e", padx=(0, 5))
        self.password_label.grid(row=3, column=0, sticky="e", padx=(0, 5))

        # Entries
        self.website_entry.grid(row=1, column=1, sticky="ew")
        self.email_entry.grid(row=2, column=1, columnspan=2, sticky="ew")
        self.password_entry.grid(row=3, column=1, sticky="ew")

        # Buttons
        self.search_button.grid(row=1, column=2, sticky="ew", padx=(5, 0))
        self.generate_password_button.grid(row=3, column=2, sticky="ew", padx=(5, 0))
        self.add_button.grid(row=4, column=1, columnspan=2, sticky="ew", pady=(10, 0))

    def generate_password(self) -> None:
        """Generate a secure random password and copy to clipboard."""
        try:
            # Use string constants for better maintainability
            letters = string.ascii_letters
            numbers = string.digits
            symbols = "!#$%&()*+"

            # Generate password components
            password_letters = [
                choice(letters)
                for _ in range(randint(*self.PASSWORD_LETTERS_RANGE))
            ]
            password_symbols = [
                choice(symbols)
                for _ in range(randint(*self.PASSWORD_SYMBOLS_RANGE))
            ]
            password_numbers = [
                choice(numbers)
                for _ in range(randint(*self.PASSWORD_NUMBERS_RANGE))
            ]

            # Combine and shuffle
            password_list = password_letters + password_symbols + password_numbers
            shuffle(password_list)
            password = "".join(password_list)

            # Clear existing password and insert new one
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)

            # Copy to clipboard
            pyperclip.copy(password)

            # Show success message
            messagebox.showinfo(
                title="Success",
                message="Password generated and copied to clipboard!"
            )

        except Exception as e:
            messagebox.showerror(
                title="Error",
                message=f"Failed to generate password: {str(e)}"
            )

    def _get_form_data(self) -> Dict[str, str]:
        """Get data from form entries."""
        return {
            "website": self.website_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "password": self.password_entry.get().strip()
        }

    def _validate_form_data(self, data: Dict[str, str]) -> bool:
        """Validate form data before saving."""
        if not data["website"]:
            messagebox.showwarning(
                title="Invalid Input",
                message="Please enter a website name."
            )
            return False

        if not data["password"]:
            messagebox.showwarning(
                title="Invalid Input",
                message="Please enter a password."
            )
            return False

        if not data["email"]:
            messagebox.showwarning(
                title="Invalid Input",
                message="Please enter an email address."
            )
            return False

        return True

    def _load_data(self) -> Dict[str, Any]:
        """Load existing data from JSON file."""
        try:
            with open(self.DATA_FILE, "r") as data_file:
                return json.load(data_file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            messagebox.showerror(
                title="Error",
                message="Data file is corrupted. Creating a new one."
            )
            return {}

    def _save_data(self, data: Dict[str, Any]) -> bool:
        """Save data to JSON file."""
        try:
            with open(self.DATA_FILE, "w") as data_file:
                json.dump(data, data_file, indent=4)
            return True
        except Exception as e:
            messagebox.showerror(
                title="Error",
                message=f"Failed to save data: {str(e)}"
            )
            return False

    def save_password(self) -> None:
        """Save password data to file."""
        form_data = self._get_form_data()

        if not self._validate_form_data(form_data):
            return

        # Confirm before saving
        is_ok = messagebox.askokcancel(
            title=form_data["website"],
            message=f"These are the details entered:\n"
                   f"Email: {form_data['email']}\n"
                   f"Password: {form_data['password']}\n"
                   f"Is it ok to save?"
        )

        if not is_ok:
            return

        # Prepare new data
        new_data = {
            form_data["website"]: {
                "email": form_data["email"],
                "password": form_data["password"],
            }
        }

        # Load existing data and update
        data = self._load_data()
        data.update(new_data)

        # Save updated data
        if self._save_data(data):
            messagebox.showinfo(
                title="Success",
                message="Password saved successfully!"
            )
            self._clear_form()
        else:
            messagebox.showerror(
                title="Error",
                message="Failed to save password."
            )

    def _clear_form(self) -> None:
        """Clear form entries after successful save."""
        self.website_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.website_entry.focus()

    def search_password(self) -> None:
        """Search for saved password data."""
        website = self.website_entry.get().strip()

        if not website:
            messagebox.showwarning(
                title="Invalid Input",
                message="Please enter a website name to search."
            )
            return

        data = self._load_data()

        if not data:
            messagebox.showinfo(
                title="No Data",
                message="No password data found. Please save some passwords first."
            )
            return

        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]

            # Copy password to clipboard
            pyperclip.copy(password)

            messagebox.showinfo(
                title=f"Password for {website}",
                message=f"Email: {email}\n"
                       f"Password: {password}\n\n"
                       f"Password copied to clipboard!"
            )
        else:
            messagebox.showinfo(
                title="Not Found",
                message=f"No details for '{website}' found."
            )

    def run(self) -> None:
        """Start the application main loop."""
        self.window.mainloop()


def main() -> None:
    """Main function to run the Password Manager application."""
    app = PasswordManager()
    app.run()


if __name__ == "__main__":
    main()
```
