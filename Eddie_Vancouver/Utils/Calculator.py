def calculate_expense(categories: dict):
    """
    총 지출 계산 함수

    Args:
        categories (dict): 항목별 지출 딕셔너리

    Returns:
        tuple: 월 지출 총합, 연 지출 총합
    """
    total_monthly = sum(categories.values())
    total_yearly = total_monthly * 12
    return total_monthly, total_yearly
