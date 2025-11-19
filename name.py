import streamlit as st

# Baskin-Robbins 스타일 간단 키오스크 (Streamlit용)
# 외부 라이브러리 불필요. Streamlit만 사용.

st.set_page_config(page_title="🍨 BR Kiosk", page_icon="🍦", layout="centered")

st.title("🍨 Baskin-Robbins 키오스크")
st.write("안녕하세요! 친절한 키오스크가 주문을 도와드릴게요. 원하는 옵션을 골라주세요. 😊")

# --- 매장/포장 선택 ---
dine_choice = st.radio("1) 매장에서 드시나요, 포장(테이크아웃)하시나요?", ("매장식사 (Eat in)", "포장 (Takeout)"))

# --- 용기 선택 ---
containers = {
    "컵 (1스쿱)": {"type": "cup", "scoops": 1, "price_per_scoop": 3000, "surcharge": 0},
    "컵 (2스쿱)": {"type": "cup", "scoops": 2, "price_per_scoop": 3000, "surcharge": 0},
    "콘 (와플)": {"type": "cone", "scoops": 1, "price_per_scoop": 3500, "surcharge": 500},
    "콘 (설탕)": {"type": "cone", "scoops": 1, "price_per_scoop": 3200, "surcharge": 0},
    "파인트 (Take-home 473ml)": {"type": "pint", "scoops": 4, "price_fixed": 12000, "surcharge": 0},
    "파티 통 (1.5L)": {"type": "tub", "scoops": 12, "price_fixed": 35000, "surcharge": 0},
}

container_choice = st.selectbox("2) 용기를 골라주세요:", list(containers.keys()))
meta = containers[container_choice]

# --- 맛 목록 (용기에 따라 일부 제약) ---
# 실제 매장의 재고/가용성은 다를 수 있으니 예시로 구성했습니다.
classic_flavors = [
    "바닐라", "초콜릿", "딸기", "민트초코", "쿠키앤크림", "녹차", "로즈(장미)"
]
seasonal_flavors = [
    "아망드카라멜", "망고치즈케이크", "솔티카라멜", "레인보우샤베트"
]
premium_flavors = [
    "블랙소금카라멜", "피칸프랄린", "초코브라우니"
]

# 간단 규칙: 컵/콘 -> classic + seasonal, 파인트/통 -> 모든 맛 선택 가능
if meta["type"] in ("cup", "cone"):
    available_flavors = classic_flavors + seasonal_flavors
else:
    available_flavors = classic_flavors + seasonal_flavors + premium_flavors

# --- 스쿱 수와 맛 선택 UI ---
max_scoops = meta.get("scoops", 1)

if meta.get("price_fixed"):
    st.info(f"이 용기는 고정 가격입니다. 권장 최대 스쿱: {max_scoops} (혼합 가능)")
    chosen_flavors = st.multiselect(f"3) 맛을 골라주세요 (최대 {max_scoops}개):", available_flavors)
else:
    # 컵/콘: 스쿱은 고정이거나 유동적일 수 있으니 사용자에게 고르게 함
    scoops = max_scoops
    st.write(f"이 용기는 최대 {scoops}스쿱입니다.")
    # flavor 선택을 스쿱 수에 맞게 제한
    chosen_flavors = st.multiselect(f"3) 맛을 골라주세요 (최대 {scoops}개):", available_flavors)

# 강제 제한: 선택된 맛이 스쿱 수를 초과하면 경고
if len(chosen_flavors) > max_scoops:
    st.warning(f"⚠️ 선택하신 맛이 최대 스쿱 수({max_scoops})보다 많아요. 먼저 선택을 조정해주세요.")

# --- 가격 계산 ---
subtotal = 0
price_breakdown = []

if meta.get("price_fixed"):
    subtotal = meta["price_fixed"]
    price_breakdown.append(("용기(고정 가격)", meta["price_fixed"]))
else:
    # 스쿱 가격 계산
    price_per_scoop = meta.get("price_per_scoop", 0)
    used_scoops = min(len(chosen_flavors), max_scoops)
    scoop_cost = price_per_scoop * used_scoops
    subtotal += scoop_cost
    price_breakdown.append((f"스쿱 {used_scoops} x {price_per_scoop}원", scoop_cost))
    # 용기별 서차지
    surcharge = meta.get("surcharge", 0)
    if surcharge:
        subtotal += surcharge
        price_breakdown.append(("콘 추가 요금", surcharge))

# 매장 식사 시 간단한 부가세(예시) 적용
tax_rate = 0.0
if "매장식사" in dine_choice:
    tax_rate = 0.10  # 예시: 10%
    tax = int(subtotal * tax_rate)
else:
    tax = 0

total = subtotal + tax

# --- 주문 요약 ---
st.markdown("---")
st.header("🧾 주문 요약")
st.write(f"**용기:** {container_choice}")
st.write(f"**식사 형태:** {dine_choice}")
if chosen_flavors:
    st.write(f"**선택된 맛:** {', '.join(chosen_flavors)}")
else:
    st.write("**선택된 맛:** 아직 선택되지 않음")

st.write("**가격 상세**")
for label, amount in price_breakdown:
    st.write(f"- {label}: {amount:,}원")

if tax > 0:
    st.write(f"- 매장 세금 (예시 {int(tax_rate*100)}%): {tax:,}원")

st.subheader(f"총액: {total:,}원")

# --- 결제 방식 선택 ---
st.markdown("---")
st.header("💳 결제")
payment_method = st.radio("결제 수단을 선택해주세요:", ("카드 결제", "현금 결제"))

# 결제 버튼
if st.button("결제 진행하기 ✅"):
    if len(chosen_flavors) == 0:
        st.error("아직 맛을 선택하지 않았어요. 먼저 맛을 골라주세요! 🍨")
    elif len(chosen_flavors) > max_scoops:
        st.error(f"선택된 맛이 최대 스쿱 수({max_scoops})를 초과했습니다. 조정해주세요.")
    else:
        # 간단한 결제 성공 화면
        st.balloons()
        st.success(f"결제가 완료되었습니다! 총 {total:,}원 — ({payment_method})\n맛있게 드세요! 😋")
        st.info("주문 영수증은 매장 직원에게 보여주세요. 감사합니다! 🙏")

# 하단 도움말
st.markdown("---")
st.write("원하시면 이 앱을 수정해 드릴게요 — 예: 가격, 맛 목록, 세부 규칙을 바꿔드릴게요. 편하게 말해줘요! 💬")
