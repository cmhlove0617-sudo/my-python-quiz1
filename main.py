class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer
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
