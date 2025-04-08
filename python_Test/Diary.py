# 일기장 프로그램램

def write_diary():
    date = input("날짜를 입력하세요 (YYYY-MM-DD): ")
    content = input("일기 내용을 작성하세요:\n")
    with open(f"{date}.txt", 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"{date} 일기가 저장되었습니다.")

def read_diary():
    date = input("조회할 날짜를 입력하세요 (YYYY-MM-DD): ")
    try:
        with open(f"{date}.txt", 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"\n{date} 일기 내용:\n{content}")
    except FileNotFoundError:
        print(f"{date}에 작성된 일기가 없습니다.")

while True:
    choice = input("\n1: 일기 작성, 2: 일기 조회, 3: 종료 \n선택하세요: ")
    if choice == "1":
        write_diary()
    elif choice == "2":
        read_diary()
    elif choice == "3":
        break
    else:
        print("올바른 선택이 아닙니다.")