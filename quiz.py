class Quiz:
    def __init__(self, question, choices, answer):
        if not isinstance(question, str) or question.strip() == "":
            raise ValueError("문제는 비어 있을 수 없습니다.")

        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")

        if not isinstance(answer, int) or answer < 1 or answer > 4:
            raise ValueError("정답 번호는 1~4 사이여야 합니다.")

        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number):
        print(f"\n문제 {number}. {self.question}")

        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["question"],
            data["choices"],
            data["answer"]
        )