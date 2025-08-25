from typing import List
from question_model import Question
from data import question_data
from quiz_brain import QuizBrain


question_bank: List[Question] = []
for question in question_data:
    question_text: str = question["question"]
    question_answer: str = question["correct_answer"]
    new_question: Question = Question(question_text, question_answer)
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)

while quiz.still_has_questions():
    quiz.next_question()

print(f"Quiz over! Your final score is: {quiz.score}/{len(question_bank)}")
