from Utils.Calculator import calculate_expense
from Utils.Visualizer import plot_pie_chart
import argparse


def main():
    print("======= 생활비 계산기 =======")
    categories = {}

    # 항목 입력
    categories['월세'] = float(input("월세 지출 (CAD): "))
    categories['식비'] = float(input("식비 지출 (CAD): "))
    categories['교통비'] = float(input("교통비 지출 (CAD): "))
    categories['기타'] = float(input("기타 지출 (CAD): "))

    # 계산
    total_monthly, total_yearly = calculate_expense(categories)
    print(f"\n총 월 지출: ${total_monthly}")
    print(f"총 연 지출: ${total_yearly}")



    # 시각화 저장 시 저장 유무 출력 체크 
    parser = argparse.ArgumentParser()
    parser.add_argument('--save', action = 'store_true', help='이미지 저장 여부')
    args = parser.parse_args()


    if args.save:
        # 시각화
        fig = plot_pie_chart(categories)
        print("차트 이미지 저장 중......(잠시만 기다려 주세요!)")
        fig.write_image("pie_chart.png")  # 이미지로 저장
        print("\n[차트] pie_chart.png 로 저장 완료!")
    else:
        print("\n(이미지 저장 없이 종료됩니다.)")

if __name__ == "__main__":
    main()
