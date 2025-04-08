import plotly.express as px

def plot_pie_chart(categories: dict):
    """
    항목별 지출 비율 파이차트 시각화

    Args:
        categories (dict): 항목별 지출 딕셔너리

    Returns:
        plotly figure
    """
    labels = list(categories.keys())
    values = list(categories.values())

    fig = px.pie(
        names=labels,
        values=values,
        title="카테고리별 지출 비율",
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig
