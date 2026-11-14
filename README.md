# Python Quiz Game

## 1. 프로젝트 소개

이 프로젝트는 Python으로 만든 콘솔 기반 퀴즈 게임입니다.

사용자는 터미널에서 퀴즈를 풀 수 있고, 직접 새로운 퀴즈를 추가할 수 있습니다.  
퀴즈 데이터와 최고 점수는 JSON 파일에 저장되어 프로그램을 종료한 후에도 유지됩니다.

또한 Git과 GitHub를 사용하여 프로젝트 버전 관리를 수행하고, 브랜치 생성, 커밋, 병합, 푸시 등의 Git 명령어를 실습하는 것을 목표로 합니다.

---

## 2. 프로젝트 목표

이 프로젝트의 주요 목표는 다음과 같습니다.

- Python 클래스와 객체 사용하기
- 여러 파일로 코드를 나누어 관리하기
- 콘솔 입력과 출력 처리하기
- JSON 파일을 이용해 데이터 저장 및 불러오기
- Git 명령어를 사용해 프로젝트 버전 관리하기
- GitHub 원격 저장소에 프로젝트 업로드하기

---

## 3. 주요 기능

### 퀴즈 게임 기능

- 퀴즈 문제 출력
- 객관식 선택지 출력
- 사용자 정답 입력
- 정답 여부 확인
- 점수 계산
- 최고 점수 저장
- 퀴즈 직접 추가
- 퀴즈 목록 확인
- JSON 파일을 이용한 데이터 저장 및 불러오기

### Git 미션 기능

프로젝트 진행 중 다음 Git 명령어를 사용했습니다.

- `git init`
- `git add`
- `git commit`
- `git push`
- `git pull`
- `git checkout`
- `git clone`

---

## 4. 파일 구조

```text
E1-2-Mission-1/
│
├── main.py
├── quiz.py
├── quiz_game.py
├── state.json
├── README.md
└── .gitignore
```

---

## 5. 파일별 역할

### `main.py`

프로그램의 시작점입니다.

작성 코드
```bash
from quiz_game import QuizGame


def main():
    game = QuizGame()
    game.load_data()
    game.run()


if __name__ == "__main__":
    main()
```

사용자가 터미널에서 아래 명령어를 입력하면 `main.py`가 실행됩니다.

<img width="681" height="239" alt="image" src="https://github.com/user-attachments/assets/0085fb17-693b-49ef-84ed-9ca40af752bb" />


`main.py`는 `QuizGame` 객체를 생성하고, 저장된 데이터를 불러온 뒤 게임을 실행합니다.

```bash
if __name__ == "__main__":
    main()
```
 이 파일이 직접 실행될 때만 main() 함수를 실행하라는 뜻
 "__main__" : 파이썬에서 프로그램의 시작점으로 실행된 파일에 붙는 특별한 이름
 

주요 역할:

- 프로그램 실행 시작
- `QuizGame` 객체 생성
- 데이터 불러오기
- 게임 메뉴 실행

---

### `quiz.py`

퀴즈 한 문제를 표현하는 파일입니다.

이 파일에는 `Quiz` 클래스가 들어 있으며, 하나의 퀴즈 문제가 가져야 할 정보를 관리합니다.

작성 코드
```text
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
```

주요 역할:

- 문제 내용 저장
- 선택지 저장
- 정답 번호 저장
<img width="507" height="237" alt="image" src="https://github.com/user-attachments/assets/943934ae-2183-4acd-a7c8-ec2695aba7ee" />

- 문제 출력
- 정답 확인
<img width="520" height="187" alt="image" src="https://github.com/user-attachments/assets/339cfa01-8174-4f0d-815d-27ce80fc5d8d" />
<img width="536" height="197" alt="image" src="https://github.com/user-attachments/assets/699791ce-8d3d-45d0-9ce1-9bd277a6b379" />

- JSON 저장을 위한 딕셔너리 변환

---

### `quiz_game.py`

퀴즈 게임 전체를 관리하는 파일입니다.

이 파일에는 `QuizGame` 클래스가 들어 있으며, 여러 개의 퀴즈를 관리하고 게임의 전체 흐름을 담당합니다.

작성 코드

- 초기 설정
```text
import json
import os
from quiz import Quiz
```

- 자동 초기화
```text
def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.best_total = 0

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.state_path = os.path.join(base_dir, "state.json")
```

- 디폴트 퀴즈 생성
```text
def create_default_quizzes(self):
        return [
            Quiz(
                "다음 중 KS D 3867의 소재가 아닌 것은?",
                ["SCM440", "SM45C", "SNCM220", "SNCM420"],
                2
            ),
            Quiz(
                "다음 중 열처리 공정의 종류가 아닌 것은?",
                ["QT", "MT", "고주파", "침탄"],
                2
            ),
            Quiz(
                "다음 중 KS M 5550 No.17875의 색상인 것은?",
                ["검은색", "노란색", "흰색", "녹색"],
                3
            ),
            Quiz(
                "다음 중 인산염 피막의 처리 방벙에 대해 기술 된 규격은?",
                ["KS D 8352", "KS D 3607", "KS M 5550", "KDS 0115-0017"],
                1
            ),
            Quiz(
                "다음 중 KS D 3752 SM45C 소재에서 규정되지 않은 화학원소는?",
                ["C", "Si", "Mn", "Mo"],
                4
            )
        ]
```

- 메뉴 출력
```text
def show_menu(self):
        print("\n===== 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 확인")
        print("5. 저장 후 종료")
```

- 숫자 입력 검증
```text
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
```

- 문자 입력 검증
```text
def input_text(self, message):
        while True:
            value = input(message).strip()

            if value == "":
                print("빈 입력은 사용할 수 없습니다.")
                continue

            return value
```

- 퀴즈 플레이 기능
```text
def play_quiz(self):
        if len(self.quizzes) == 0:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0

        print("\n===== 퀴즈 시작 =====")
        print("각 문제의 정답 번호를 1~4번 중에서 입력하세요.")

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
```


- 퀴즈 추가 기능
```text
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
```

- 퀴즈 목록 보기
```text
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
```

- 최고 점수 관리
```text
def show_best_score(self):
        print("\n===== 최고 점수 =====")

        if self.best_score is None:
            print("아직 퀴즈를 푼 기록이 없습니다.")
        else:
            print(f"최고 점수: {self.best_score} / {self.best_total}")
```
- 데이터 저장 및 불러오기
```text
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
```
```text
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
```

- 메뉴 실행
```text
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
```

---

### `state.json`

퀴즈 데이터와 게임 상태를 저장하는 JSON 파일입니다.

프로그램에서 추가한 퀴즈나 최고 점수 등의 정보가 저장됩니다.

예시 구조:

```json
{
    "quizzes": [
        {
            "question": "다음 중 KS D 3867의 소재가 아닌 것은?",
            "choices": [
                "SCM440",
                "SM45C",
                "SNCM220",
                "SNCM420"
            ],
            "answer": 2
        },
        {
            "question": "다음 중 열처리 공정의 종류가 아닌 것은?",
            "choices": [
                "QT",
                "MT",
                "고주파",
                "침탄"
            ],
            "answer": 2
        },
        {
            "question": "다음 중 KS M 5550 No.17875의 색상인 것은?",
            "choices": [
                "검은색",
                "노란색",
                "흰색",
                "녹색"
            ],
            "answer": 3
        },
        {
            "question": "다음 중 인산염 피막의 처리 방벙에 대해 기술 된 규격은?",
            "choices": [
                "KS D 8352",
                "KS D 3607",
                "KS M 5550",
                "KDS 0115-0017"
            ],
            "answer": 1
        },
        {
            "question": "다음 중 KS D 3752 SM45C 소재에서 규정되지 않은 화학원소는?",
            "choices": [
                "C",
                "Si",
                "Mn",
                "Mo"
            ],
            "answer": 4
        },
        {
            "question": "테스트용 퀴즈 추가 입니다.",
            "choices": [
                "선택지 테스트1",
                "선택지 테스트2",
                "선택지 테스트3(정답)",
                "선택지 테스트4"
            ],
            "answer": 3
        }
    ],
    "best_score": 2,
    "best_total": 5
}
```

---

## 6. 실행 방법

### 1단계: 프로젝트 폴더로 이동

```bash
cd E1-2-Mission-1
```

### 2단계: 프로그램 실행

```bash
python main.py
```

또는 환경에 따라 다음 명령어를 사용할 수 있습니다.

```bash
python3 main.py
```

---

## 7. 사용 방법

프로그램을 실행하면 콘솔에 메뉴가 출력됩니다.

예시:

```text
===== 퀴즈 게임 =====
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록 보기
4. 최고 점수 확인
5. 저장 후 종료
```

사용자는 원하는 메뉴 번호를 입력하여 기능을 실행할 수 있습니다.

---

## 8. 프로그램 실행 흐름

전체 실행 흐름은 다음과 같습니다.

```text
사용자
↓
python main.py 실행
↓
main.py에서 QuizGame 객체 생성
↓
quiz_game.py에서 데이터 불러오기
↓
메뉴 출력
↓
사용자 선택에 따라 기능 실행
↓
quiz.py의 Quiz 객체를 이용해 문제 출력 및 정답 확인
↓
결과 저장
```

---

## 9. 개발 순서

일반적인 개발 순서는 다음과 같습니다.

```text
1. 프로젝트 폴더 생성
2. README.md, .gitignore 파일 생성
3. quiz.py 파일 작성
4. Quiz 클래스 구현
5. quiz_game.py 파일 작성
6. QuizGame 클래스 구현
7. main.py 파일 작성
8. 프로그램 실행 테스트
9. JSON 저장 및 불러오기 기능 구현
10. Git으로 버전 관리
11. GitHub 원격 저장소 연결
12. 브랜치 생성 및 기능 개발
13. main 브랜치에 병합
14. GitHub에 push
```

---

## 10. Git 사용 기록

이 프로젝트에서는 Git을 사용하여 버전 관리를 진행했습니다.

### Git 저장소 초기화

```bash
git init
```

### 변경 파일 추가

```bash
git add .
```

### 커밋 생성

```bash
git commit -m "Init: 프로젝트 기본 파일 생성"
```

### 브랜치 생성 및 이동

```bash
git checkout -b feature/play-quiz
```

### main 브랜치로 이동

```bash
git checkout main
```

### 브랜치 병합

```bash
git merge feature/play-quiz
```

### 원격 저장소 연결

```bash
git remote add origin 본인_GitHub_저장소_URL
```

### GitHub에 업로드

```bash
git push
```

### 원격 저장소에서 최신 내용 가져오기

```bash
git pull
```

### 원격 저장소 복제

```bash
git clone 본인_GitHub_저장소_URL
```

---

## 11. 커밋 예시

프로젝트를 진행하면서 기능 단위로 커밋을 작성했습니다.

예시:

```text
Init: 프로젝트 기본 파일 생성
Docs: README 기본 내용 작성
Feat: Quiz 클래스 구현
Feat: QuizGame 클래스 기본 구조 구현
Feat: 퀴즈 추가 기능 구현
Feat: 퀴즈 출제 기능 구현
Feat: 점수 계산 기능 구현
Feat: JSON 저장 기능 구현
Feat: JSON 불러오기 기능 구현
Fix: 입력값 예외 처리 추가
Docs: README 실행 방법 추가
```

---

## 12. 브랜치 전략

기본 브랜치는 `main`을 사용했습니다.

새로운 기능은 별도의 기능 브랜치에서 작업한 뒤, 작업이 완료되면 `main` 브랜치에 병합했습니다.

예시:

```bash
git checkout -b feature/play-quiz
```

기능 구현 후:

```bash
git checkout main
git merge feature/play-quiz
```

---

## 13. 사용한 기술

- Python
- JSON
- Git
- GitHub
- VSCode

---

## 14. 배운 점

이 프로젝트를 통해 다음 내용을 학습했습니다.

- Python 클래스와 객체를 이용한 구조화된 프로그램 작성
- 파일을 여러 개로 나누어 역할별로 관리하는 방법
- 사용자 입력을 받아 콘솔 프로그램을 만드는 방법
- JSON 파일을 이용해 데이터를 저장하고 불러오는 방법
- Git을 이용한 버전 관리 방법
- GitHub 원격 저장소에 프로젝트를 업로드하는 방법
- 브랜치를 이용해 기능을 분리하여 개발하는 방법

---

## 15. 실행 예시

```text
===== 퀴즈 게임 =====
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록 보기
4. 최고 점수 확인
5. 저장 후 종료

메뉴를 선택하세요: 1

===== 퀴즈 시작 =====
각 문제의 정답 번호를 1~4 중에서 입력하세요.

문제 1. 파이썬에서 리스트를 만들 때 사용하는 기호는?
1. ()
2. []
3. {}
4. <>

정답 번호 입력: 2
정답입니다!

최종 점수: 1/1
```

---

## 16. 프로젝트 요약

이 프로젝트는 Python을 이용해 콘솔 기반 퀴즈 게임을 구현한 과제입니다.

`main.py`, `quiz.py`, `quiz_game.py`로 파일을 나누어 각각 실행, 퀴즈 문제, 게임 진행 역할을 담당하게 했습니다.

또한 JSON 파일을 사용하여 퀴즈 데이터와 점수를 저장하고, Git과 GitHub를 사용하여 프로젝트를 관리했습니다.

---

## 17. 한 줄 설명

Python 클래스, JSON 저장 기능, Git 버전 관리를 활용한 콘솔 퀴즈 게임 프로젝트입니다.
````

README 내용 아주 잘 구성됐어요.  
특히 과제 제출용이라면 **프로젝트 소개, 실행 방법, 파일별 역할, Git 사용 기록**이 들어가야 평가자가 보기 좋습니다.
