import html
from typing import Optional

from question_model import Question


class QuizBrain:
    """クイズの進行管理を担うクラス"""

    def __init__(self, q_list: list[Question]) -> None:
        self.question_number: int = 0
        self.score: int = 0
        self.question_list: list[Question] = q_list
        self.current_question: Optional[Question] = None

    def still_has_questions(self) -> bool:
        """まだ出題すべき問題が残っているか判定"""
        return self.question_number < len(self.question_list)

    def next_question(self) -> str:
        """次の問題を取り出し、テキストとして返す"""
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text: str = html.unescape(self.current_question.text)
        return f"Q.{self.question_number}: {q_text}"

    def check_answer(self, user_answer: str) -> bool:
        """ユーザーの解答が正しいか判定し、スコアを更新"""
        if self.current_question is None:
            raise ValueError("No current question set")

        correct_answer: str = self.current_question.answer
        is_correct: bool = user_answer.strip().lower() == correct_answer.strip().lower()

        if is_correct:
            self.score += 1

        return is_correct
