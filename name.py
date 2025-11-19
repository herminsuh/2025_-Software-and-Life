import streamlit as st

# 🍨 Baskin-Robbins 스타일 키오스크 (Streamlit)
# ➜ 외부 라이브러리 X, streamlit 기본만 사용

st.set_page_config(page_title="🍨 BR Kiosk", page_icon="🍦", layout="centered")

# --- 전체 테마용 CSS (베스킨라빈스 느낌 색감) ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #ffe6f2 0%, #fff7fb 40%, #e6f3ff 100%);
        font-family: "Noto Sans KR", sans-serif;
    }
    .br-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ff66a3;
        text-shadow: 1px 1px 2px rgba(255, 102, 163, 0.2);
    }
    .br-subtitle {
        color: #555555;
        font-size: 1.05rem;
    }
    .br-box {
        padding: 1rem 1.2rem;
        border-radius: 1rem;
        background: rgba(255,255,255,0.85);
        border: 1px solid #ffd6ea;
        box-shadow: 0 4px 10px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }
    .br-highlight {
        color: #ff4b9b;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- 타이틀 영역 ---
st.markdown('<div class="br-title">🍨 Baskin-Robbins 키오스크</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="br-subtitle">안녕하세요! 달콤한 아이스크림 주문을 도와드릴게요. '
    '천천히 원하시는 옵션을 골라주세요. 😊</p>',
    unsafe_allow_html=True,
)

# ======================
# 1) 매장 / 포장 선택
# ======================
with st.container():
    st.markdown('<div class="br-box">', unsafe_allow_html=True)
    dine_choice = st.radio(
        "1) 매장에서 드시나요, 포장(테이크아웃)하시나요? 🏠👜",
        ("매장식사 (Eat in)", "포장 (Takeout)"),
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ======================
# 2) 용기 선택
# ======================
containers = {
    "싱글컵 (1스쿱)": {"type": "cup", "scoops": 1, "price_per_scoop": 3300, "surcharge": 0},
    "더블컵 (2스쿱)": {"type": "cup", "scoops": 2, "price_per_scoop": 3100, "surcharge": 0},  # 예시 단가
    "싱글콘 (슈가콘, 1스쿱)": {"type": "cone", "scoops": 1, "price_per_scoop": 3500, "surcharge": 0},
    "싱글콘 (와플콘, 1스쿱)": {"type": "cone", "scoops": 1, "price_per_scoop": 3500, "surcharge": 500},
    "파인트 (약 3~4스쿱)": {"type": "pint", "scoops": 4, "price_fixed": 9900, "surcharge": 0},
    "쿼터 (약 4가지 맛)": {"type": "quart", "scoops": 4, "price_fixed": 15500, "surcharge": 0},
    "패밀리 (약 5가지 맛)": {"type": "family", "scoops": 5, "price_fixed": 22000, "surcharge": 0},
    "하프갤런 (약 6가지 맛)": {"type": "half_gallon", "scoops": 6, "price_fixed": 27000, "surcharge": 0},
}

with st.container():
    st.markdown('<div class="br-box">', unsafe_allow_html=True)
    container_choice = st.selectbox("2) 용기를 골라주세요 🥄", list(containers.keys()))
    st.markdown('</div>', unsafe_allow_html=True)

meta = containers[container_choice]

# ======================
# 3) 아이스크림 맛 선택
#   (실제 베스킨라빈스에서 자주 볼 수 있는 인기 메뉴들 중심)
# ======================

# 대표적인 베라 맛들 (예시 - 수업/프로젝트용)
classic_flavors = [
    "엄마는외계인",
    "슈팅스타",
    "민트초코봉봉",
    "아몬드봉봉",
    "베리베리스트로베리",
    "뉴욕치즈케이크",
    "피스타치오아몬드",
    "초코나무숲",
    "바람과함께사라지다",
    "초콜릿무스",
    "레인보우샤베트",
    "사랑에빠진딸기",
    "체리쥬빌레",
    "이상한나라의솜사탕",
    "쿨민트",
    "요거트",
]

# 시즌/스페셜 맛 예시
seasonal_flavors = [
    "아이스허니버터아몬드",
    "치즈고구마",
    "망고탱고",
    "쿠앤크봉봉",
]

# 프리미엄/리치한 느낌의 맛 예시
premium_flavors = [
    "피칸프랄린",
    "초콜릿브라우니",
    "블랙소금카라멜",
]

# 용기 타입에 따라 선택 가능한 맛 범위 설정
if meta["type"] in ("cup", "cone"):
    available_flavors = classic_flavors + seasonal_flavors
else:
    available_flavors = classic_flavors + seasonal_flavors + premium_flavors

max_scoops = meta.get("scoops", 1)

with st.container():
    st.markdown('<div class="br-box">', unsafe_allow_html=True)
    if meta.get("price_fixed"):
        st.info(
            f"이 용기는 **고정 가격**이에요. 🧊\n\n"
            f"권장 최대 맛 개수: **{max_scoops}가지** (골라먹는 재미 up! ✨)"
        )
        chosen_flavors = st.multiselect(
            f"3) 아이스크림 맛을 골라주세요 (최대 {max_scoops}가지) 🍦",
            available_flavors,
        )
    else:
        scoops = max_scoops
        st.write(f"이 용기는 최대 **{scoops}스쿱**까지 담을 수 있어요.")
        chosen_flavors = st.multiselect(
            f"3) 아이스크림 맛을 골라주세요 (최대 {scoops}가지) 🍦",
            available_flavors,
        )

    if len(chosen_flavors) > max_scoops:
        st.warning(f"⚠️ 선택하신 맛이 최대 스쿱 수(**{max_scoops}개**)를 넘었어요. 조금만 줄여볼까요? 😊")

    st.markdown('</div>', unsafe_allow_html=True)

# ======================
# 4) 가격 계산
# ======================
subtotal = 0
price_breakdown = []

if meta.get("price_fixed"):
    subtotal = meta["price_fixed"]
    price_breakdown.append(("용기(고정 가격)", meta["price_fixed"]))
else:
    price_per_scoop = meta.get("price_per_scoop", 0)
    used_scoops = min(len(chosen_flavors), max_scoops)
    scoop_cost = price_per_scoop * used_scoops
    subtotal += scoop_cost
    price_breakdown.append((f"스쿱 {used_scoops} x {price_per_scoop}원", scoop_cost))

    surcharge = meta.get("surcharge", 0)
    if surcharge:
        subtotal += surcharge
        price_breakdown.append(("와플콘 추가 요금", surcharge))

# 간단 예시로 매장식사 시 세금 10% 적용
tax_rate = 0.0
if "매장식사" in dine_choice:
    tax_rate = 0.10
    tax = int(subtotal * tax_rate)
else:
    tax = 0

total = subtotal + tax

# ======================
# 5) 주문 요약
# ======================
with st.container():
    st.markdown('<div class="br-box">', unsafe_allow_html=True)
    st.markdown("### 🧾 주문 요약")
    st.write(f"**용기:** {container_choice}")
    st.write(f"**식사 형태:** {dine_choice}")
    if chosen_flavors:
        st.write(f"**선택된 맛:** {', '.join(chosen_flavors)}")
    else:
        st.write("**선택된 맛:** 아직 선택되지 않았어요 🍧")

    st.write("**가격 상세**")
    for label, amount in price_breakdown:
        st.write(f"- {label}: {amount:,}원")

    if tax > 0:
        st.write(f"- 매장 세금 (예시 {int(tax_rate * 100)}%): {tax:,}원")

    st.subheader(f"💰 총액: {total:,}원")
    st.markdown('</div>', unsafe_allow_html=True)

# ======================
# 6) 결제 수단 선택 (기프티콘 추가)
# ======================
with st.container():
    st.markdown('<div class="br-box">', unsafe_allow_html=True)
    st.markdown("### 💳 결제")
    payment_method = st.radio(
        "결제 수단을 선택해주세요:",
        ("카드 결제", "현금 결제", "기프티콘 결제"),
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ======================
# 7) 결제 버튼 & 완료 화면 (핑크 하트 폭발 💗)
# ======================
if st.button("결제 진행하기 ✅"):
    if len(chosen_flavors) == 0:
        st.error("아직 아이스크림 맛을 선택하지 않았어요. 먼저 맛부터 골라볼까요? 🍨")
    elif len(chosen_flavors) > max_scoops:
        st.error(f"선택된 맛이 최대 스쿱 수({max_scoops})를 초과했어요. 다시 조정해 주세요. 🙏")
    else:
        # 풍선 이펙트
        st.balloons()

        # 결제 성공 메시지
        st.success(
            f"결제가 완료되었습니다! 🎉\n\n"
            f"총 **{total:,}원** — (**{payment_method}**)로 결제되었어요.\n"
            "달콤한 아이스크림, 맛있게 드세요! 😋"
        )

        # 다양한 톤의 핑크 하트 연출
        heart_line_1 = "💗 💖 💕 💓 💞 💗 💖 💕"
        heart_line_2 = "💞 💓 💕 💖 💗 💞 💓 💕"
        heart_line_3 = "💖 💗 💞 💕 💓 💖 💗 💞"

        st.markdown(
            f"""
            <div style="text-align:center; font-size: 2rem; margin-top: 1rem;">
                {heart_line_1}<br>
                {heart_line_2}<br>
                {heart_line_3}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.info("주문 영수증 화면을 직원에게 보여주시면, 바로 준비해 드릴게요. 감사합니다! 🙏")

# ======================
# 8) 하단 안내
# ======================
st.markdown("---")
st.write(
    "💡 *가격이나 맛 구성, 세금 규칙 등을 실제 매장 상황에 맞게 바꾸고 싶다면,*\n"
    "원하는 조건을 알려주시면 코드도 같이 수정해 드릴게요! 🍦"
)
