import tkinter as tk
from tkinter import Canvas, Label, Button, PhotoImage
# from typing import Optional

from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
TRUE_IMAGE_PATH = "images/true.png"
FALSE_IMAGE_PATH = "images/false.png"


class QuizInterface:
    """クイズアプリの GUI を管理するクラス"""

    def __init__(self, quiz_brain: QuizBrain) -> None:
        self.quiz: QuizBrain = quiz_brain

        # メインウィンドウ
        self.window: tk.Tk = tk.Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # スコア表示
        self.score_label: Label = Label(
            text="Score: 0", fg="white", bg=THEME_COLOR
        )
        self.score_label.grid(row=0, column=1)

        # 問題表示用キャンバス
        self.canvas: Canvas = Canvas(width=300, height=250, bg="white")
        self.question_text: int = self.canvas.create_text(
            150,
            125,
            width=280,
            text="Some Question Text",
            fill=THEME_COLOR,
            font=("Arial", 20, "italic"),
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        # ボタン画像（参照を保持する必要がある）
        self.true_image: PhotoImage = PhotoImage(file=TRUE_IMAGE_PATH)
        self.false_image: PhotoImage = PhotoImage(file=FALSE_IMAGE_PATH)

        # True / False ボタン
        self.true_button: Button = Button(
            image=self.true_image, highlightthickness=0, command=self.true_pressed
        )
        self.true_button.grid(row=2, column=0)

        self.false_button: Button = Button(
            image=self.false_image, highlightthickness=0, command=self.false_pressed
        )
        self.false_button.grid(row=2, column=1)

        # 初回の問題を表示
        self.get_next_question()

        # イベントループ開始
        self.window.mainloop()

    def get_next_question(self) -> None:
        """次の問題を取得して表示"""
        self.canvas.config(bg="white")
        if not self.quiz.still_has_questions():
            self.canvas.itemconfig(
                self.question_text, text="You've completed the quiz"
            )
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
        else:
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text: str = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)

    def true_pressed(self) -> None:
        """True ボタンが押された時の処理"""
        is_right: bool = self.quiz.check_answer("True")
        self.give_feedback(is_right)

    def false_pressed(self) -> None:
        """False ボタンが押された時の処理"""
        is_right: bool = self.quiz.check_answer("False")
        self.give_feedback(is_right)

    def give_feedback(self, is_right: bool) -> None:
        """回答の正誤に応じたフィードバックを表示"""
        self.canvas.config(bg="green" if is_right else "red")
        self.window.after(1000, self.get_next_question)
