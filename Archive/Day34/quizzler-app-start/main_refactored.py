from question_model import Question
from data_refactored import get_question_data
from quiz_brain import QuizBrain

from ui import QuizInterface


def build_question_bank() -> list[Question]:
    """question_data から Question オブジェクトのリストを構築する"""
    question_bank: list[Question] = []
    for question in get_question_data(amount=10, q_type="boolean"):
        question_text: str = question["question"]
        question_answer: str = question["correct_answer"]
        new_question = Question(question_text, question_answer)
        question_bank.append(new_question)
    return question_bank

def main() -> None:
    """クイズアプリのエントリーポイント"""
    question_bank: list[Question] = build_question_bank()
    quiz: QuizBrain = QuizBrain(question_bank)

    # 参照しないが必要なインスタンスなので _quiz_ui にして警告回避
    _quiz_ui: QuizInterface = QuizInterface(quiz)

    while quiz.still_has_questions():
        quiz.next_question()

    print("You've completed the quiz")
    print(f"Your final score was: {quiz.score}/{quiz.question_number}")

if __name__ == "__main__":
    main()
