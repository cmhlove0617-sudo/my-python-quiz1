class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def check_answer(self, user_answer):
        return str(self.answer) == str(user_answer)



quiz1 = Quiz(
    "대한민국의 수도는 어디일까요?",
    ["서울", "부산", "대전", "광주"],
    1
)

quiz2 = Quiz(
    "파이썬에서 글자를 출력하는 명령어는?",
    ["input()", "print()", "int()", "str()"],
    2
)

quizzes = [quiz1, quiz2]

while True:
    print("================================")
    print("       🎯 나만의 퀴즈 게임")
    print("================================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 최고 점수 확인")
    print("5. 종료")
    print("================================")

    choice = input("메뉴 번호를 선택하세요 (1~5): ").strip()

    if choice == "1":
        print("📝 퀴즈를 시작합니다!")

        score = 0

        for number, quiz in enumerate(quizzes, start=1):
            print(f"\n[문제 {number}]")
            print(quiz.question)

            for i, option in enumerate(quiz.choices, start=1):
                print(f"{i}. {option}")

            while True:
                user_answer = input("정답 번호를 입력하세요 (1~4): ").strip()

                if user_answer in ["1", "2", "3", "4"]:
                    break
                else:
                    print("⚠️ 1~4 사이의 숫자를 입력하세요.")

            if quiz.check_answer(user_answer):
                print("✅ 정답입니다!")
                score += 1
            else:
                print("❌ 오답입니다!")

        total_score = int(score / len(quizzes) * 100)
        print(f"🏆 결과: {len(quizzes)}문제 중 {score}문제 정답! ({total_score}점)")
        

    elif choice == "2":
        print("📌 새로운 퀴즈를 추가합니다!")
    elif choice == "3":
        print("📋 퀴즈 목록을 보여줍니다!")
    elif choice == "4":
        print("🏆 최고 점수를 확인합니다!")
    elif choice == "5":
        print("👋 게임을 종료합니다!")
        break
    else:
        print("⚠️ 잘못된 입력입니다. 1~5 사이의 번호를 입력하세요.")

    print()
