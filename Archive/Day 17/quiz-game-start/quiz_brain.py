from typing import List
from question_model import Question


class QuizBrain:

    def __init__(self, questions_list: List[Question]):
        self.questions_number: int = 0
        self.questions_list = questions_list
        self.score: int = 0

    def next_question(self) -> None:
        current_question = self.questions_list[self.questions_number]
        self.questions_number += 1
        user_answer = input(f"Q.{self.questions_number}: {current_question.text} (True/False): ")
        self.check_answer(user_answer, current_question.answer)

    def still_has_questions(self) -> bool:
        return self.questions_number < len(self.questions_list)
    
    def check_answer(self, user_answer: str, correct_answer: str) -> None:
        if user_answer.lower() == correct_answer.lower():
            print("You got it right!")
            self.score += 1
        else:
            print("Sorry, that's wrong.")
        print(f"The correct answer was {correct_answer}.")
        print(f"Your score: {self.score}/{self.questions_number}")
        print("\n")

