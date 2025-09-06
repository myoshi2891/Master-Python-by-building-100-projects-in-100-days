import tkinter as tk
import math
from typing import Optional
import os


class PomodoroTimer:
    """Pomodoro Timer Application using Tkinter."""
    
    # Constants
    PINK = "#e2979c"
    RED = "#e7305b"
    GREEN = "#9bdeac"
    YELLOW = "#f7f5dd"
    FONT_NAME = "Courier"
    WORK_MIN = 25
    SHORT_BREAK_MIN = 5
    LONG_BREAK_MIN = 20
    
    def __init__(self) -> None:
        """Initialize the Pomodoro Timer application."""
        self.reps = 0
        self.timer: Optional[str] = None
        self.window = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.layout_widgets()
    
    def setup_window(self) -> None:
        """Configure the main window."""
        self.window.title("Pomodoro Clock")
        self.window.config(padx=100, pady=50, bg=self.YELLOW)
        self.window.resizable(False, False)
    
    def create_widgets(self) -> None:
        """Create all UI widgets."""
        # Title label
        self.title_label = tk.Label(
            text="Timer",
            fg=self.GREEN,
            bg=self.YELLOW,
            font=(self.FONT_NAME, 50)
        )
        
        # Canvas with tomato image
        self.canvas = tk.Canvas(
            width=200,
            height=224,
            bg=self.YELLOW,
            highlightthickness=0
        )
        
        # Load tomato image with error handling
        self._load_tomato_image()
        
        # Timer text on canvas
        self.timer_text = self.canvas.create_text(
            100, 130,
            text="00:00",
            font=(self.FONT_NAME, 35, "bold"),
            fill="white"
        )
        
        # Start button
        self.start_button = tk.Button(
            text="Start",
            command=self.start_timer,
            font=(self.FONT_NAME, 20),
            highlightthickness=0,
            bg="white",
            fg="black"
        )
        
        # Reset button
        self.reset_button = tk.Button(
            text="Reset",
            command=self.reset_timer,
            font=(self.FONT_NAME, 20),
            highlightthickness=0,
            bg="white",
            fg="black"
        )
        
        # Check marks label
        self.check_marks = tk.Label(
            fg=self.GREEN,
            bg=self.YELLOW,
            font=(self.FONT_NAME, 20)
        )
    
    def _load_tomato_image(self) -> None:
        """Load the tomato image with error handling."""
        try:
            # Try different possible paths
            possible_paths = [
                "tomato.png",
                "./tomato.png",
                os.path.join(os.path.dirname(__file__), "tomato.png")
            ]
            
            image_loaded = False
            for path in possible_paths:
                if os.path.exists(path):
                    self.tomato_img = tk.PhotoImage(file=path)
                    self.canvas.create_image(100, 112, image=self.tomato_img)
                    image_loaded = True
                    break
            
            if not image_loaded:
                # Create a simple tomato representation if image not found
                self._create_fallback_tomato()
                
        except tk.TclError as e:
            print(f"Error loading tomato image: {e}")
            self._create_fallback_tomato()
    
    def _create_fallback_tomato(self) -> None:
        """Create a simple tomato shape if image is not available."""
        # Draw a simple tomato shape
        self.canvas.create_oval(50, 80, 150, 180, fill=self.RED, outline="darkred", width=3)
        self.canvas.create_oval(80, 60, 120, 90, fill=self.GREEN, outline="darkgreen", width=2)
        self.canvas.create_text(100, 50, text="🍅", font=(self.FONT_NAME, 30))
    
    def layout_widgets(self) -> None:
        """Layout all widgets using grid."""
        self.title_label.grid(column=1, row=0, pady=(0, 20))
        self.canvas.grid(column=1, row=1, pady=(0, 20))
        self.start_button.grid(column=0, row=2, padx=(0, 20))
        self.reset_button.grid(column=2, row=2, padx=(20, 0))
        self.check_marks.grid(column=1, row=3, pady=(20, 0))
    
    def reset_timer(self) -> None:
        """Reset the timer to initial state."""
        if self.timer is not None:
            self.window.after_cancel(self.timer)
            self.timer = None
        
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.title_label.config(text="Timer", fg=self.GREEN)
        self.check_marks.config(text="")
        self.reps = 0
    
    def start_timer(self) -> None:
        """Start the timer based on current repetition."""
        self.reps += 1
        
        work_sec = self.WORK_MIN * 60
        short_break_sec = self.SHORT_BREAK_MIN * 60
        long_break_sec = self.LONG_BREAK_MIN * 60
        
        if self.reps % 8 == 0:
            # Long break after 4 work sessions
            self._start_countdown(long_break_sec, "Long Break", self.RED)
        elif self.reps % 2 == 0:
            # Short break after work session
            self._start_countdown(short_break_sec, "Short Break", self.PINK)
        else:
            # Work session
            self._start_countdown(work_sec, "Work", self.GREEN)
    
    def _start_countdown(self, duration: int, title: str, color: str) -> None:
        """Start countdown with given duration and update UI."""
        self.title_label.config(text=title, fg=color)
        self.count_down(duration)
    
    def count_down(self, count: int) -> None:
        """Countdown mechanism."""
        count_min = math.floor(count / 60)
        count_sec = count % 60
        
        # Format seconds with leading zero if needed
        count_sec_str = f"{count_sec:02d}"
        
        # Update timer display
        self.canvas.itemconfig(self.timer_text, text=f"{count_min}:{count_sec_str}")
        
        if count > 0:
            # Continue countdown
            self.timer = self.window.after(1000, self.count_down, count - 1)
        else:
            # Timer finished, start next session and update check marks
            self.start_timer()
            self._update_check_marks()
    
    def _update_check_marks(self) -> None:
        """Update check marks based on completed work sessions."""
        work_sessions = math.floor(self.reps / 2)
        marks = "✔" * work_sessions
        self.check_marks.config(text=marks)
    
    def run(self) -> None:
        """Start the application main loop."""
        self.window.mainloop()


def main() -> None:
    """Main function to run the Pomodoro Timer application."""
    app = PomodoroTimer()
    app.run()


if __name__ == "__main__":
    main()
# ```

# ## 主なリファクタリング内容

# ### 1. **クラスベース設計**
# - 全ての機能を `PomodoroTimer` クラスにカプセル化
# - グローバル変数を排除し、インスタンス変数として管理

# ### 2. **型ヒントの追加**
# - 全ての関数とメソッドに適切な型ヒントを追加
# - `Optional[str]` を使用してタイマーIDの型安全性を確保

# ### 3. **エラーハンドリングの改善**
# - 画像ファイルが見つからない場合のフォールバック機能
# - 複数のパスを試行する仕組み
# - 画像が読み込めない場合の代替表示

# ### 4. **コードの整理と分離**
# - 機能ごとにメソッドを分割
# - UI設定、ウィジェット作成、レイアウトを分離
# - プライベートメソッド（`_`プレフィックス）の使用

# ### 5. **可読性の向上**
# - 明確なメソッド名とドキュメント文字列
# - 定数の適切な使用
# - コメントの改善

# ### 6. **保守性の向上**
# - 設定値の変更が容易
# - 新機能の追加が簡単
# - テストしやすい構造

# この設計により、コードはより保守しやすく、拡張しやすく、理解しやすくなりました。