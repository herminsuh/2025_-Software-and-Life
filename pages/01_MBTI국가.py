import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np

# -------------------
#  데이터 불러오기
# -------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# MBTI 컬럼(16개 유형)
mbti_cols = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ENFP", "ESTP",
    "ISTJ", "ESTJ", "ENFJ", "ESFJ"
]

# -------------------
#  사이드바 / 제목
# -------------------
st.set_page_config(
    page_title="Countries MBTI Explorer",
    layout="wide"
)

st.title("🌎 Countries MBTI Explorer")
st.markdown(
    """
    국가를 선택하면, 해당 국가의 **MBTI 16유형 비율**을  
    인터랙티브한 Plotly 막대그래프로 확인할 수 있어요.
    """
)

# 국가 선택
countries = df["Country"].sort_values().unique()
default_country = "South Korea" if "South Korea" in countries else countries[0]
selected_country = st.sidebar.selectbox("국가를 선택하세요", countries, index=list(countries).index(default_country))

st.sidebar.markdown("---")
st.sidebar.markdown("**그래프 설명**")
st.sidebar.markdown("- 1등 유형은 **빨간색** 🔴")
st.sidebar.markdown("- 나머지는 **밝기만 다른 그라데이션** 색상")

# 선택된 국가의 데이터 추출
country_row = df[df["Country"] == selected_country].iloc[0]

# x, y 데이터 준비
x = mbti_cols
y = [country_row[c] for c in mbti_cols]

# -------------------
#  색상 설정 (1등 = 빨간색, 나머지 그라데이션)
# -------------------
# 1등 인덱스
max_idx = int(np.argmax(y))

# 기본 색상: 빨간색 계열 (hex)
base_color = np.array([255, 0, 0])  # 빨간색

colors = []
max_value = max(y)
min_value = min(y) if min(y) < max_value else 0.0

for i, val in enumerate(y):
    if i == max_idx:
        # 1등: 완전 빨강
        colors.append("rgb(255,0,0)")
    else:
        # 값에 따라 밝기 조절 (그라데이션 느낌)
        # val이 작을수록 밝고, 클수록 진한 붉은색
        if max_value - min_value == 0:
            intensity = 0.4
        else:
            norm = (val - min_value) / (max_value - min_value)
            # 0.2 ~ 0.8 사이에서 변화 (너무 밝거나 너무 어두운 것 방지)
            intensity = 0.2 + 0.6 * norm

        # base_color * intensity + 흰색 섞기
        rgb = base_color * intensity + np.array([255, 255, 255]) * (1 - intensity)
        r, g, b = rgb.astype(int)
        colors.append(f"rgb({r},{g},{b})")

# -------------------
#  Plotly 막대그래프 생성
# -------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=x,
        y=y,
        marker=dict(color=colors),
        text=[f"{val*100:.1f}%" for val in y],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>%{y:.3f} (비율)<extra></extra>",
    )
)

fig.update_layout(
    title=f"{selected_country} MBTI 비율 (16유형)",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (0~1)",
    yaxis=dict(range=[0, max_value * 1.2]),
    template="simple_white",
    margin=dict(l=40, r=40, t=80, b=40),
)

# -------------------
#  페이지에 그래프 표시
# -------------------
st.plotly_chart(fig, use_container_width=True)

# 데이터 테이블 옵션
with st.expander("🔎 이 국가의 MBTI 원본 데이터 보기"):
    st.dataframe(
        pd.DataFrame(
            {
                "MBTI": x,
                "비율": y,
                "퍼센트(%)": [round(val * 100, 2) for val in y],
            }
        ).set_index("MBTI")
    )
