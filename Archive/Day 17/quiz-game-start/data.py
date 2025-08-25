from typing import List, TypedDict

class QuestionDict(TypedDict):
    type: str
    difficulty: str
    category: str
    question: str
    correct_answer: str
    incorrect_answers: List[str]

question_data: List[QuestionDict] = [
    {
        "type": "boolean",
        "difficulty": "hard",
        "category": "Entertainment: Books",
        "question": "Harry Potter was born on July 31st, 1980.",
        "correct_answer": "True",
        "incorrect_answers": ["False"],
    },
    {
        "type": "boolean",
        "difficulty": "easy",
        "category": "Entertainment: Books",
        "question": "The book 1984 was published in 1949.",
        "correct_answer": "True",
        "incorrect_answers": ["False"],
    },
    {
        "type": "boolean",
        "difficulty": "easy",
        "category": "Entertainment: Books",
        "question": "The Harry Potter series of books, combined, are over 1,000,000 words in length.",
        "correct_answer": "True",
        "incorrect_answers": ["False"],
    },
    {
        "type": "boolean",
        "difficulty": "medium",
        "category": "Entertainment: Books",
        "question": "Originally, the character Charlie from Charlie and the Chocolate Factory was going to be black.",
        "correct_answer": "True",
        "incorrect_answers": ["False"],
    },
    {
        "type": "boolean",
        "difficulty": "easy",
        "category": "Entertainment: Books",
        "question": "&quot;Green Eggs and Ham&quot; consists of only 50 different words.",
        "correct_answer": "True",
        "incorrect_answers": ["False"],
    },
    {
        "type": "boolean",
        "difficulty": "easy",
        "category": "Entertainment: Books",
        "question": "Stephen Chbosky wrote the book &#039;The Perks of Being A Wallflower&#039;.",
        "correct_answer": "True",
        "incorrect_answers": ["False"],
    },
    {
        "type": "boolean",
        "difficulty": "easy",
        "category": "Entertainment: Books",
        "question": "&quot;Elementary, my dear Watson&quot; is a phrase that is never truly said within the Conan Doyle books of Sherlock Holmes.",
        "correct_answer": "True",
        "incorrect_answers": ["False"],
    },
    {
        "type": "boolean",
        "difficulty": "easy",
        "category": "Entertainment: Books",
        "question": "Dracula is destroyed by contact with sunlight",
        "correct_answer": "False",
        "incorrect_answers": ["True"],
    },
    {
        "type": "boolean",
        "difficulty": "easy",
        "category": "Entertainment: Books",
        "question": "Shub-Niggurath is a creature that was created by J. R. R. Tolkien in his novel &quot;The Lord of The Rings&quot;.",
        "correct_answer": "False",
        "incorrect_answers": ["True"],
    },
    {
        "type": "boolean",
        "difficulty": "hard",
        "category": "Entertainment: Books",
        "question": "In Harry Potter and the Deathly Hallows, Hermione destroyed the fourth Horcrux by stabbing it with the Sword of Gryffindor.",
        "correct_answer": "False",
        "incorrect_answers": ["True"],
    },
]
