import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import uuid
import base64

# ============================================
# 기본 설정 (하나은행 스타일)
# ============================================
st.set_page_config(
    page_title="하나고 온라인 분실물함 - 하나줍줍",
    page_icon="🎒",
    layout="wide"
)

HANA_GREEN = "#008485"

st.markdown(
    f"""
    <style>
    body {{
        background-color: #ffffff;
    }}
    .stApp {{
        background-color: #ffffff;
    }}
    h1, h2, h3, h4, h5 {{
        color: {HANA_GREEN};
    }}
    .stButton>button {{
        background-color: {HANA_GREEN};
        color: white;
        border-radius: 8px;
        border: none;
    }}
    .stButton>button:hover {{
        background-color: #006a66;
        color: white;
    }}
    .item-card {{
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 0.75rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        background-color: #ffffff;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================
# 초기 데이터 생성 (수정된 부분: 현재 날짜 기준으로 과거 시간 설정)
# ============================================
def init_data():
    if "lost_items" not in st.session_state:
        # 현재 시간을 기준으로 과거 시간을 계산하여 초기 데이터 설정
        now = datetime.now()
        st.session_state.lost_items = [
            {
                "id": str(uuid.uuid4()),
                "name": "하나카드",
                "location": "매점 입구",
                "floor": 1,
                "found_date": (now - timedelta(days=5)).date(),
                "uploaded_at": now - timedelta(days=5, hours=3),
                "image_url": "https://community-api-cdn.kr.karrotmarket.com/v1/resource/images/load?id=kr-community%231987053135104090112",
                "image_data": None,
                "uploader": "25199 허민서",
                "resolved": False,
            },
            {
                "id": str(uuid.uuid4()),
                "name": "C타입 충전기",
                "location": "A동 움파",
                "floor": 3,
                "found_date": (now - timedelta(days=35)).date(), # 35일 전 발견
                "uploaded_at": now - timedelta(days=35, hours=10), # 35일 전 업로드 (-> 오래된 분실물 탭에서 확인 가능)
                "image_url": "https://my.snu.ac.kr/dext5editor/handler/image_handler.jsp?fn=%2F2025%2F10%2F20251023_170208372_05296.jpg",
                "image_data": None,
                "uploader": "25116 이래나",
                "resolved": False,
            },
            {
                "id": str(uuid.uuid4()),
                "name": "갤럭시 버즈",
                "location": "B305",
                "floor": 3,
                "found_date": (now - timedelta(days=1)).date(),
                "uploaded_at": now - timedelta(days=1, hours=8),
                "image_url": "https://community-api-cdn.kr.karrotmarket.com/v1/resource/images/load?id=kr-community%231750767056434888704",
                "image_data": None,
                "uploader": "25116 이래나",
                "resolved": False,
            },
            {
                "id": str(uuid.uuid4()),
                "name": "영어 교과서",
                "location": "급식실",
                "floor": 4,
                "found_date": (now - timedelta(days=10)).date(),
                "uploaded_at": now - timedelta(days=10, hours=15),
                "image_url": "https://static.mercdn.net/item/detail/orig/photos/m16043469936_1.jpg?1736746405",
                "image_data": None,
                "uploader": "25116 이래나",
                "resolved": False,
            },
        ]

    if "user_stats" not in st.session_state:
        st.session_state.user_stats = {
            "25199 허민서": {"upload_count": 1, "notification_on": True},
            "25116 이래나": {"upload_count": 3, "notification_on": True},
        }

    if "notifications" not in st.session_state:
        # 알림 시간도 현재 시간 기준으로 수정
        now = datetime.now()
        st.session_state.notifications = [
            {
                "time": now - timedelta(days=5, hours=3),
                "message": "새로운 분실물 '하나카드'가 등록되었습니다.",
            }
        ]


init_data()

# ============================================
# 이미지 출력 함수
# ============================================
def show_item_image(item, width=None, use_column_width=False):
    if item.get("image_data"):
        img_bytes = base64.b64decode(item["image_data"])
        st.image(img_bytes, width=width, use_column_width=use_column_width)
    elif item.get("image_url"):
        st.image(item["image_url"], width=width, use_column_width=use_column_width)
    else:
        st.image("https://placehold.co/400x250?text=No+Image", width=width, use_column_width=use_column_width)


# ============================================
# UI 구성
# ============================================
st.title("🎒 하나고 온라인 분실물함 - 하나줍줍")

tabs = st.tabs([
    "🏠 홈",
    "📝 업로드",
    "🔍 전체/검색 목록",
    "⏳ 오래된 분실물",
    "🏆 랭킹",
    "🔔 알림/설정",
])

# ===========================================================
# TAB 1 — 홈 (최근 12개 항목 표시)
# ===========================================================
with tabs[0]:
    st.subheader("✨ 최근 분실물 게시판")

    # uploaded_at을 기준으로 정렬하여 최신순으로 12개 항목을 가져옴
    items = sorted(
        st.session_state.lost_items,
        key=lambda x: x["uploaded_at"],
        reverse=True,
    )[:12]

    cols = st.columns(3)
    for i, item in enumerate(items):
        # Resolved 항목 필터링 로직은 없지만, 일단 모든 항목 표시
        with cols[i % 3]:
            st.markdown("<div class='item-card'>", unsafe_allow_html=True)
            st.markdown(f"**📦 {item['name']}**")
            show_item_image(item, use_column_width=True)
            st.caption(f"📍 {item['location']} | 🏢 {item['floor']}층")
            st.caption(
                f"📅 발견: {item['found_date']}  ·  "
                f"⬆️ 업로드: {item['uploaded_at'].strftime('%m-%d %H:%M')}"
            )
            st.caption(f"🙋 업로더: {item['uploader']}")
            st.markdown("</div>", unsafe_allow_html=True)


# ===========================================================
# TAB 2 — 업로드
# ===========================================================
with tabs[1]:
    st.subheader("📝 새로운 분실물 등록")

    with st.form("upload_form", clear_on_submit=True):
        colA, colB = st.columns(2)
        with colA:
            name = st.text_input("📦 물건 이름")
            location = st.text_input("📍 발견 장소")
        with colB:
            floor = st.selectbox("🏢 층수 (0: 기타)", [0,1,2,3,4,5,6,7], index=3)
            found_date = st.date_input("📅 발견 날짜", datetime.now().date())

        uploader = st.text_input("🙋 업로더 이름", value="25116 이래나")

        uploaded_file = st.file_uploader("📸 분실물 사진 (선택)", type=["png","jpg","jpeg"])

        submitted = st.form_submit_button("등록하기")

    if submitted:
        image_b64 = None
        if uploaded_file is not None:
            img_bytes = uploaded_file.read()
            image_b64 = base64.b64encode(img_bytes).decode("utf-8")

        new_item = {
            "id": str(uuid.uuid4()),
            "name": name,
            "location": location,
            "floor": floor,
            "found_date": found_date,
            "uploaded_at": datetime.now(), # 현재 시각으로 설정
            "image_url": None if image_b64 else "https://placehold.co/400x250?text=Lost+Item",
            "image_data": image_b64,
            "uploader": uploader,
            "resolved": False,
        }

        st.session_state.lost_items.append(new_item)

        stats = st.session_state.user_stats.get(
            uploader, {"upload_count": 0, "notification_on": True}
        )
        stats["upload_count"] += 1
        st.session_state.user_stats[uploader] = stats

        st.session_state.notifications.insert(
            0,
            {
                "time": datetime.now(),
                "message": f"새로운 분실물 '{name}'이(가) 등록되었습니다. (업로더: {uploader})",
            },
        )

        st.success("🎉 분실물이 성공적으로 등록되었습니다! 홈 탭에서 확인해 보세요.")
        st.balloons()


# ===========================================================
# TAB 3 — 전체/검색
# ===========================================================
with tabs[2]:
    st.subheader("🔍 분실물 검색 및 전체 목록")

    df = pd.DataFrame(st.session_state.lost_items)

    col1, col2, col3 = st.columns([3,1,2])
    query = col1.text_input("검색어 입력 (물건/장소)")
    floor_filter = col2.selectbox("층수", ["전체",0,1,2,3,4,5,6,7], index=0)
    sort_order = col3.radio("정렬 기준", ["최신순","오래된순"], horizontal=True)

    filtered = df.copy()

    if query:
        filtered = filtered[
            filtered["name"].str.contains(query, case=False) |
            filtered["location"].str.contains(query, case=False)
        ]

    if floor_filter != "전체":
        filtered = filtered[filtered["floor"] == floor_filter]

    filtered = filtered.sort_values(
        by="uploaded_at", ascending=(sort_order=="오래된순")
    )

    # 표 출력
    tmp = filtered.copy()
    tmp["발견 날짜"] = tmp["found_date"].astype(str)
    tmp["업로드 시각"] = tmp["uploaded_at"].dt.strftime("%Y-%m-%d %H:%M")

    tmp = tmp.rename(columns={
        "name": "물건 이름",
        "location": "발견 장소",
        "floor": "층수",
        "uploader": "업로더",
        "resolved": "해결 여부"
    })

    st.dataframe(
        tmp[["물건 이름","발견 장소","층수","발견 날짜","업로드 시각","업로더","해결 여부"]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    st.markdown("### 🖼 사진 카드로 보기")

    for _, row in filtered.iterrows():
        item = next(x for x in st.session_state.lost_items if x["id"] == row["id"])
        st.markdown("<div class='item-card'>", unsafe_allow_html=True)
        cols = st.columns([1,2])
        with cols[0]:
            show_item_image(item, width=220)
        with cols[1]:
            st.markdown(f"**📦 {item['name']}**")
            st.write(f"📍 {item['location']} · 🏢 {item['floor']}층")
            st.write(f"📅 발견: {item['found_date']}")
            st.write(f"⬆️ 업로드: {item['uploaded_at'].strftime('%Y-%m-%d %H:%M')}")
            st.write(f"🙋 업로더: {item['uploader']}")
        st.markdown("</div>", unsafe_allow_html=True)


# ===========================================================
# TAB 4 — 오래된 분실물
# ===========================================================
with tabs[3]:
    st.subheader("⏳ 오래된 분실물 (30일 이상 지난 분실물)")

    today = datetime.now()
    # uploaded_at이 30일 이상 지난 항목만 필터링
    old_items = [
        item for item in st.session_state.lost_items
        if item["uploaded_at"] < today - timedelta(days=30)
    ]

    if len(old_items) == 0:
        st.info("30일 이상 지난 분실물이 없습니다.")
    else:
        df_old = pd.DataFrame(old_items)
        df_old["발견 날짜"] = df_old["found_date"].astype(str)
        df_old["업로드 시각"] = df_old["uploaded_at"].dt.strftime("%Y-%m-%d %H:%M")

        df_old = df_old.rename(columns={
            "name": "물건 이름",
            "location": "발견 장소",
            "floor": "층수",
            "uploader": "업로더",
            "resolved": "해결 여부"
        })

        st.dataframe(
            df_old[["물건 이름","발견 장소","층수","발견 날짜","업로드 시각","업로더","해결 여부"]],
            use_container_width=True,
            hide_index=True
        )

# ===========================================================
# TAB 5 — 랭킹
# ===========================================================
with tabs[4]:
    st.subheader("🏆 업로드 랭킹")

    rank = [
        {"이름": name, "업로드 횟수": info["upload_count"]}
        for name, info in st.session_state.user_stats.items()
    ]

    df_rank = pd.DataFrame(rank).sort_values(
        by="업로드 횟수", ascending=False
    ).reset_index(drop=True)
    df_rank["순위"] = df_rank.index + 1

    st.dataframe(
        df_rank[["순위","이름","업로드 횟수"]],
        use_container_width=True,
        hide_index=True
    )

# ===========================================================
# TAB 6 — 알림
# ===========================================================
with tabs[5]:
    st.subheader("🔔 알림 내역 및 설정")

    current_user = st.text_input("🔧 알림 설정할 사용자 이름", value="25116 이래나")

    stats = st.session_state.user_stats.get(
        current_user, {"upload_count": 0, "notification_on": True}
    )

    notif_on = st.checkbox(
        f"새 분실물 등록 시 알림 받기 (현재 {'ON' if stats['notification_on'] else 'OFF'})",
        value=stats["notification_on"]
    )

    # 알림 설정 변경 로직
    if notif_on != stats["notification_on"]:
        stats["notification_on"] = notif_on
        st.session_state.user_stats[current_user] = stats
        st.rerun() # 설정을 반영하기 위해 재실행

    st.markdown("---")
    st.markdown("### 📋 전체 알림 내역")

    if len(st.session_state.notifications) == 0:
        st.info("알림이 없습니다.")
    else:
        for n in st.session_state.notifications:
            st.write(f"[{n['time'].strftime('%Y-%m-%d %H:%M:%S')}] {n['message']}")

        if st.button("🗑️ 알림 모두 지우기"):
            st.session_state.notifications = []
            st.success("알림이 삭제되었습니다.")
            st.rerun() # 삭제 후 상태를 반영하기 위해 재실행
