from question_model import Question
from quiz_brain import QuizBrain
# from data import question_data
from ui import QuizInterface
from data_refactored import get_question_data

question_bank = []
for question in get_question_data(amount=10, q_type="boolean"):
    question_text: str = question["question"]
    question_answer: str = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)


quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface(quiz)

while quiz.still_has_questions():
    quiz.next_question()

print("You've completed the quiz")
print(f"Your final score was: {quiz.score}/{quiz.question_number}")


# def main() -> None:
#     question_data = get_question_data(amount=10, q_type="boolean")
#     print(f"取得件数: {len(question_data)}")
#     print(question_data[0])  # サンプル出力

# if __name__ == "__main__":
#     main()
