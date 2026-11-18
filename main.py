import json
import os
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent / "state.json"

DEFAULT_QUIZZES = [
    {"question": "파이썬에서 화면에 글자를 출력하는 함수는?", "choices": ["input()", "print()", "len()", "int()"], "answer": 2},
    {"question": "파이썬에서 정수 자료형의 이름은?", "choices": ["str", "bool", "int", "list"], "answer": 3},
    {"question": "조건을 판단할 때 사용하는 키워드는?", "choices": ["if", "for", "def", "class"], "answer": 1},
    {"question": "리스트의 첫 번째 위치 번호는?", "choices": ["1", "2", "-1", "0"], "answer": 4},
    {"question": "키와 값을 묶어서 저장하는 자료형은?", "choices": ["tuple", "dict", "str", "bool"], "answer": 2},
]


class Quiz:
    def __init__(self, question, choices, answer):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 빈 문자열일 수 없습니다.")
        if not isinstance(choices, list) or len(choices) != 4 or not all(
            isinstance(choice, str) and choice.strip() for choice in choices
        ):
            raise ValueError("선택지는 비어 있지 않은 문자열 4개여야 합니다.")
        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답은 1~4의 정수여야 합니다.")
        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer

    def show(self):
        print(self.question)
        for number, choice in enumerate(self.choices, start=1):
            print(f"  {number}. {choice}")

    def is_correct(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {"question": self.question, "choices": self.choices, "answer": self.answer}


class QuizGame:
    def __init__(self):
        self.quizzes = [Quiz(**data) for data in DEFAULT_QUIZZES]
        self.best_score = None
        self.best_result = None
        self.load()

    def load(self):
        if not STATE_FILE.exists():
            print("기본 퀴즈 5개로 시작합니다.")
            return
        try:
            with STATE_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict) or not isinstance(data.get("quizzes"), list):
                raise ValueError("퀴즈 목록 형식이 잘못되었습니다.")
            quizzes = [Quiz(**item) for item in data["quizzes"]]
            best = data.get("best_score")
            if best is not None and (type(best) is not int or not 0 <= best <= 100):
                raise ValueError("최고 점수 형식이 잘못되었습니다.")
            result = data.get("best_result")
            if result is not None:
                if (not isinstance(result, dict) or type(result.get("correct")) is not int
                    or type(result.get("total")) is not int or result["total"] <= 0
                    or not 0 <= result["correct"] <= result["total"]):
                    raise ValueError("최고 점수 상세 정보가 잘못되었습니다.")
            self.quizzes = quizzes
            self.best_score = best
            self.best_result = result
            print(f"저장 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개)")
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
            print(f"저장 파일에 문제가 있어 기본 퀴즈로 시작합니다: {error}")
            print("손상된 파일은 즉시 덮어쓰지 않습니다.")

    def save(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_result": self.best_result,
        }
        temporary = STATE_FILE.with_name("state.json.tmp")
        try:
            with temporary.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            os.replace(temporary, STATE_FILE)
            return True
        except OSError as error:
            print(f"저장 실패: {error}")
            return False

    @staticmethod
    def ask_number(message, minimum, maximum):
        while True:
            value = input(message).strip()
            if not value:
                print("빈칸은 입력할 수 없습니다.")
                continue
            try:
                number = int(value)
            except ValueError:
                print("숫자를 입력해 주세요.")
                continue
            if minimum <= number <= maximum:
                return number
            print(f"{minimum}~{maximum} 사이의 숫자를 입력해 주세요.")

    @staticmethod
    def ask_text(message):
        while True:
            value = input(message).strip()
            if value:
                return value
            print("빈칸은 입력할 수 없습니다.")

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        correct = 0
        total = len(self.quizzes)
        print(f"\n퀴즈를 시작합니다! 총 {total}문제")
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[문제 {index}/{total}]")
            quiz.show()
            answer = self.ask_number("정답 번호 (1~4): ", 1, 4)
            if quiz.is_correct(answer):
                correct += 1
                print("정답입니다!")
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")
        score = round(correct / total * 100)
        print(f"\n결과: {correct}/{total} 정답, {score}점")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_result = {"correct": correct, "total": total}
            print("새로운 최고 점수입니다!")
        self.save()

    def add_quiz(self):
        print("\n새 퀴즈 추가")
        question = self.ask_text("문제: ")
        choices = [self.ask_text(f"선택지 {number}: ") for number in range(1, 5)]
        answer = self.ask_number("정답 번호 (1~4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        if self.save():
            print("퀴즈를 추가하고 저장했습니다!")
        else:
            print("퀴즈가 현재 실행 중인 프로그램에만 추가되었습니다. 저장 문제를 해결하세요.")

    def show_list(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        print(f"\n등록된 퀴즈 목록 ({len(self.quizzes)}개)")
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")

    def show_score(self):
        if self.best_score is None:
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"최고 점수: {self.best_score}점")
            if self.best_result:
                print(f"기록: {self.best_result['total']}문제 중 {self.best_result['correct']}문제 정답")

    def run(self):
        try:
            while True:
                print("\n======== 나만의 파이썬 퀴즈 게임 ========")
                print("1. 퀴즈 풀기")
                print("2. 퀴즈 추가")
                print("3. 퀴즈 목록")
                print("4. 점수 확인")
                print("5. 종료")
                choice = self.ask_number("선택 (1~5): ", 1, 5)
                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_list()
                elif choice == 4:
                    self.show_score()
                else:
                    print("게임을 종료합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되었습니다. 안전하게 종료합니다.")
        finally:
            self.save()


if __name__ == "__main__":
    QuizGame().run()
