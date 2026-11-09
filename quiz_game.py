import json
import os
from quiz import Quiz


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.best_total = 0

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.state_path = os.path.join(base_dir, "state.json")

    def create_default_quizzes(self):
        return [
            Quiz(
                "파이썬에서 리스트를 만들 때 사용하는 기호는?",
                ["()", "[]", "{}", "<>"],
                2
            ),
            Quiz(
                "파이썬에서 조건문을 만들 때 사용하는 키워드는?",
                ["for", "if", "def", "class"],
                2
            ),
            Quiz(
                "파이썬에서 함수를 정의할 때 사용하는 키워드는?",
                ["function", "define", "def", "func"],
                3
            ),
            Quiz(
                "반복문 중 목록을 순서대로 순회할 때 주로 사용하는 키워드는?",
                ["if", "for", "try", "return"],
                2
            ),
            Quiz(
                "화면에 문자열을 출력할 때 사용하는 함수는?",
                ["input", "print", "open", "append"],
                2
            )
        ]

    def show_menu(self):
        print("\n===== 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 확인")
        print("5. 저장 후 종료")

    def input_number(self, message, min_value, max_value):
        while True:
            value = input(message).strip()

            if value == "":
                print("빈 입력은 사용할 수 없습니다.")
                continue

            try:
                number = int(value)
            except ValueError:
                print("숫자를 입력해야 합니다.")
                continue

            if number < min_value or number > max_value:
                print(f"{min_value}부터 {max_value} 사이의 숫자를 입력하세요.")
                continue

            return number

    def input_text(self, message):
        while True:
            value = input(message).strip()

            if value == "":
                print("빈 입력은 사용할 수 없습니다.")
                continue

            return value

    def play_quiz(self):
        if len(self.quizzes) == 0:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0

        print("\n===== 퀴즈 시작 =====")
        print("각 문제의 정답 번호를 1~4 중에서 입력하세요.")

        for index, quiz in enumerate(self.quizzes, start=1):
            quiz.display(index)
            user_answer = self.input_number("정답 번호를 입력하세요: ", 1, 4)

            if quiz.check_answer(user_answer):
                print("정답입니다!")
                score += 1
            else:
                correct_text = quiz.choices[quiz.answer - 1]
                print(f"오답입니다. 정답은 {quiz.answer}번 '{correct_text}'입니다.")

        total = len(self.quizzes)

        print("\n===== 결과 =====")
        print(f"점수: {score} / {total}")

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_total = total
            print("최고 점수가 갱신되었습니다!")

        self.save_data()

    def add_quiz(self):
        print("\n===== 퀴즈 추가 =====")

        question = self.input_text("문제를 입력하세요: ")

        choices = []
        for index in range(1, 5):
            choice = self.input_text(f"선택지 {index}번을 입력하세요: ")
            choices.append(choice)

        answer = self.input_number("정답 번호를 입력하세요(1~4): ", 1, 4)

        try:
            quiz = Quiz(question, choices, answer)
            self.quizzes.append(quiz)
            self.save_data()
            print("퀴즈가 추가되었습니다.")
        except ValueError as error:
            print("퀴즈 추가에 실패했습니다.")
            print(error)

    def show_quizzes(self):
        if len(self.quizzes) == 0:
            print("등록된 퀴즈가 없습니다.")
            return

        print("\n===== 퀴즈 목록 =====")

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n{index}. {quiz.question}")

            for choice_index, choice in enumerate(quiz.choices, start=1):
                print(f"   {choice_index}. {choice}")

            correct_text = quiz.choices[quiz.answer - 1]
            print(f"   정답: {quiz.answer}번 {correct_text}")

    def show_best_score(self):
        print("\n===== 최고 점수 =====")

        if self.best_score is None:
            print("아직 퀴즈를 푼 기록이 없습니다.")
        else:
            print(f"최고 점수: {self.best_score} / {self.best_total}")

    def save_data(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_total": self.best_total
        }

        try:
            with open(self.state_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError:
            print("데이터 저장 중 오류가 발생했습니다.")

    def load_data(self):
        if not os.path.exists(self.state_path):
            print("state.json 파일이 없어 기본 퀴즈를 불러옵니다.")
            self.quizzes = self.create_default_quizzes()
            self.best_score = None
            self.best_total = 0
            self.save_data()
            return

        try:
            with open(self.state_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            quiz_data_list = data.get("quizzes", [])

            if len(quiz_data_list) == 0:
                self.quizzes = self.create_default_quizzes()
            else:
                self.quizzes = [
                    Quiz.from_dict(quiz_data)
                    for quiz_data in quiz_data_list
                ]

            self.best_score = data.get("best_score")
            self.best_total = data.get("best_total", 0)

        except (json.JSONDecodeError, KeyError, TypeError, OSError, ValueError):
            print("state.json 파일에 문제가 있어 기본 데이터로 초기화합니다.")
            self.quizzes = self.create_default_quizzes()
            self.best_score = None
            self.best_total = 0
            self.save_data()

    def run(self):
        while True:
            try:
                self.show_menu()
                menu = self.input_number("메뉴 번호를 선택하세요: ", 1, 5)

                if menu == 1:
                    self.play_quiz()
                elif menu == 2:
                    self.add_quiz()
                elif menu == 3:
                    self.show_quizzes()
                elif menu == 4:
                    self.show_best_score()
                elif menu == 5:
                    self.save_data()
                    print("저장 후 종료합니다.")
                    break

            except KeyboardInterrupt:
                print("\nCtrl+C가 입력되었습니다. 저장 후 안전하게 종료합니다.")
                self.save_data()
                break

            except EOFError:
                print("\n입력 스트림이 종료되었습니다. 저장 후 안전하게 종료합니다.")
                self.save_data()
                break