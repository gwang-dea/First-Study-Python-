import streamlit as st
from Utils.Calculator import calculate_expense
from Utils.Visualizer import plot_pie_chart

st.set_page_config(page_title="밴쿠버 생활비 계산기", layout="centered")

st.title("💸 나만의 밴쿠버 생활비 계산기")
st.write("당신의 월 지출을 입력하면 연간 지출과 비율을 계산해드립니다!")

# 사용자 입력
rent = st.number_input("🏠 주거비 (렌트)", min_value=0, step=10)
food = st.number_input("🍽 식비", min_value=0, step=10)
transport = st.number_input("🚌 교통비", min_value=0, step=10)
phone = st.number_input("📱 통신비", min_value=0, step=10)
leisure = st.number_input("🎮 여가/문화", min_value=0, step=10)
shopping = st.number_input("🛍 쇼핑/개인 소비", min_value=0, step=10)
etc = st.number_input("💼 기타", min_value=0, step=10)

if st.button("지출 계산하기"):
    categories = {
        "주거비": rent,
        "식비": food,
        "교통비": transport,
        "통신비": phone,
        "여가/문화": leisure,
        "쇼핑": shopping,
        "기타": etc
    }

    total_monthly, total_yearly = calculate_expense(categories)
    st.subheader("📊 결과")
    st.write(f"**월 지출 총합:** ${total_monthly:,.2f}")
    st.write(f"**연 지출 총합:** ${total_yearly:,.2f}")

    st.plotly_chart(plot_pie_chart(categories))
