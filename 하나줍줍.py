import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import uuid
import base64
from io import BytesIO

# -----------------------------------------------------------
# 기본 설정 (하나은행 느낌: 흰색 + 짙은 초록)
# -----------------------------------------------------------
st.set_page_config(
    page_title="하나고 온라인 분실물함 - 하나줍줍",
    page_icon="🎒",
    layout="wide"
)

# CSS로 색깔/글꼴 살짝 꾸미기
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
    .css-1cpxqw2 a {{
        color: {HANA_GREEN} !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-weight: 600;
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

# -----------------------------------------------------------
# 초기 데이터 (세션에 한 번만 세팅)
# -----------------------------------------------------------
def init_data():
    if "lost_items" not in st.session_state:
        st.session_state.lost_items = [
            {
                "id": str(uuid.uuid4()),
                "name": "하나카드",
                "location": "매점 입구",
                "floor": 1,
                "found_date": datetime(2025, 11, 26).date(),
                "uploaded_at": datetime(2025, 11, 26, 9, 30),
                "image_url": "https://placehold.co/400x250?text=Hana+Card",
                "image_data": None,
                "uploader": "25199 허민서",
                "resolved": False,
            },
            {
                "id": str(uuid.uuid4()),
                "name": "C타입 충전기",
                "location": "A동 움파",
                "floor": 3,
                "found_date": datetime(2025, 10, 25).date(),
                "uploaded_at": datetime(2025, 10, 25, 10, 0),
                "image_url": "https://placehold.co/400x250?text=Charger",
                "image_data": None,
                "uploader": "25116 이래나",
                "resolved": False,
            },
            {
                "id": str(uuid.uuid4()),
                "name": "갤럭시 버즈",
                "location": "B305",
                "floor": 3,
                "found_date": datetime(2025, 11, 25).date(),
                "uploaded_at": datetime(2025, 11, 26, 8, 0),
                "image_url": "https://placehold.co/400x250?text=Galaxy+Buds",
                "image_data": None,
                "uploader": "25116 이래나",
                "resolved": False,
            },
            {
                "id": str(uuid.uuid4()),
                "name": "영어 교과서",
                "location": "급식실",
                "floor": 4,
                "found_date": datetime(2025, 11, 20).date(),
                "uploaded_at": datetime(2025, 11, 25, 15, 0),
                "image_url": "https://placehold.co/400x250?text=English+Book",
                "image_data": None,
                "uploader": "25116 이래나",
                "resolved": False,
            },
        ]

    if "user_stats" not in st.session_state:
        # 업로더 이름 기준으로 업로드 횟수/알림 여부 관리
        st.session_state.user_stats = {
            "25199 허민서": {"upload_count": 1, "notification_on": True},
            "25116 이래나": {"upload_count": 3, "notification_on": True},
        }

    if "notifications" not in st.session_state:
        st.session_state.notifications = [
            {
                "time": datetime(2025, 11, 26, 9, 30),
                "message": "새로운 분실물 '하나카드'가 등록되었습니다.",
            }
        ]


init_data()

# -----------------------------------------------------------
# 공통: 이미지 출력 함수
# -----------------------------------------------------------
def show_item_image(item, width=None, use_col_width=False):
    """
    image_data(업로드된 실제 사진)가 있으면 그걸 쓰고,
    없으면 image_url(placeholder) 사용
    """
    if item.get("image_data"):
        img_bytes = base64.b64decode(item["image_data"])
        st.image(img_bytes, width=width, use_column_width=use_col_width)
    elif item.get("image_url"):
        st.image(item["image_url"], width=width, use_column_width=use_col_width)
    else:
        st.image("https://placehold.co/400x250?text=No+Image", width=width, use_column_width=use_col_width)


# -----------------------------------------------------------
# 타이틀 / 탭 구성
# -----------------------------------------------------------
st.title("🎒 하나고등학교 온라인 분실물함 - 하나줍줍")

tabs = st.tabs(
    ["🏠 홈", "📝 업로드", "🔍 전체/검색 목록", "⏳ 오래된 분실물", "🏆 랭킹", "🔔 알림/설정"]
)

# ===========================================================
# TAB 1 — 홈 (최근 분실물)
# ===========================================================
with tabs[0]:
    st.subheader("✨ 최근 분실물 게시판")

    if len(st.session_state.lost_items) == 0:
        st.info("등록된 분실물이 아직 없습니다.")
    else:
        # 최신순으로 12개까지
        items = sorted(
            st.session_state.lost_items,
            key=lambda x: x["uploaded_at"],
            reverse=True,
        )[:12]

        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                st.markdown(f"<div class='item-card'>", unsafe_allow_html=True)
                st.markdown(f"**📦 {item['name']}**")
                show_item_image(item, use_col_width=True)
                st.caption(f"📍 {item['location']} | 🏢 {item['floor']}층")
                st.caption(
                    f"📅 발견: {item['found_date'].strftime('%Y-%m-%d')}  ·  "
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
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("📦 물건 이름", placeholder="예: 아이폰 14, 체육복 상의")
            location = st.text_input("📍 발견 장소", placeholder="예: 3층 305호 앞 복도")
        with col_b:
            floor = st.selectbox("🏢 층수 (0: 야외/기타)", [0, 1, 2, 3, 4, 5, 6, 7], index=3)
            found_date = st.date_input("📅 발견 날짜", datetime.now().date())

        uploader = st.text_input("🙋 업로더 이름", value="25116 이래나")

        uploaded_file = st.file_uploader("📸 분실물 사진 (선택)", type=["png", "jpg", "jpeg"])

        submitted = st.form_submit_button("✅ 분실물 등록")

    if submitted:
        if not name or not location or not uploader:
            st.error("물건 이름, 발견 장소, 업로더 이름은 반드시 입력해야 합니다.")
        else:
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
                "uploaded_at": datetime.now(),
                "image_url": None
                if image_b64
                else "https://placehold.co/400x250?text=Lost+Item",
                "image_data": image_b64,
                "uploader": uploader,
                "resolved": False,
            }

            st.session_state.lost_items.append(new_item)

            # 업로더 랭킹 업데이트
            stats = st.session_state.user_stats.get(uploader, {"upload_count": 0, "notification_on": True})
            stats["upload_count"] += 1
            st.session_state.user_stats[uploader] = stats

            # 알림 추가
            st.session_state.notifications.insert(
                0,
                {
                    "time": datetime.now(),
                    "message": f"새로운 분실물 '{name}'이(가) 등록되었습니다. (업로더: {uploader})",
                },
            )

            st.success("🎉 분실물이 성공적으로 등록되었습니다!")
            st.balloons()

# ===========================================================
# TAB 3 — 전체/검색 목록
# ===========================================================
with tabs[2]:
    st.subheader("🔍 분실물 검색 및 전체 목록")

    if len(st.session_state.lost_items) == 0:
        st.info("등록된 분실물이 아직 없습니다.")
    else:
        df = pd.DataFrame(st.session_state.lost_items)

        col1, col2, col3 = st.columns([3, 1, 2])
        with col1:
            query = st.text_input("🔎 물건 이름 / 장소 검색", placeholder="예: 이어폰, 급식실")
        with col2:
            floor_filter = st.selectbox(
                "🏢 층수 필터",
                ["전체", 0, 1, 2, 3, 4, 5, 6, 7],
                index=0,
            )
        with col3:
            sort_order = st.radio("⏳ 정렬 기준", ["최신순", "오래된순"], horizontal=True)

        # 필터링
        filtered = df.copy()
        if query:
            mask = filtered["name"].str.contains(query, case=False) | filtered["location"].str.contains(
                query, case=False
            )
            filtered = filtered[mask]

        if floor_filter != "전체":
            filtered = filtered[filtered["floor"] == floor_filter]

        filtered = filtered.sort_values(
            by="uploaded_at", ascending=(sort_order == "오래된순")
        )

        # 표 형태
        tmp = filtered.copy()
        tmp["발견 날짜"] = tmp["found_date"].apply(lambda d: d.strftime("%Y-%m-%d"))
        tmp["업로드 시각"] = tmp["uploaded_at"].dt.strftime("%Y-%m-%d %H:%M")
        tmp = tmp.rename(
            columns={
                "name": "물건 이름",
                "location": "발견 장소",
                "floor": "층수",
                "uploader": "업로더",
                "resolved": "해결 여부",
            }
        )

        st.dataframe(
            tmp[["물건 이름", "발견 장소", "층수", "발견 날짜", "업로드 시각", "업로더", "해결 여부"]],
            use_container_width=True,
            hide_index=True,
        )
        st.caption(f"총 {len(filtered)}개의 분실물이 검색되었습니다.")

        st.markdown("---")
        st.markdown("### 🖼 카드 형태로 보기")

        for _, row in filtered.iterrows():
            item = st.session_state.lost_items[
                next(i for i, it in enumerate(st.session_state.lost_items) if it["id"] == row["id"])
            ]
            st.markdown("<div class='item-card'>", unsafe_allow_html=True)
            cols = st.columns([1, 2])
            with cols[0]:
                show_item_image(item, width=220)
            with cols[1]:
                st.markdown(f"**📦 {item['name']}**")
                st.write(f"📍 {item['location']} · 🏢 {item['floor']}층")
                st.write(f"📅 발견: {item['found_date'].strftime('%Y-%m-%d')}")
                st.write(f"⬆️ 업로드: {item['uploaded_at'].strftime('%Y-%m-%d %H:%M')}")
                st.write(f"🙋 업로더: {item['uploader']}")
            st.markdown("</div>", unsafe_allow_html=True)

# ===========================================================
# TAB 4 — 오래된 분실물
# ===========================================================
with tabs[3]:
    st.subheader("⏳ 오래된 분실물 게시판 (30일 이상 지난 분실물)")

    if len(st.session_state.lost_items) == 0:
        st.info("등록된 분실물이 아직 없습니다.")
    else:
        today = datetime.now()
        old_items = [
            item
            for item in st.session_state.lost_items
            if item["uploaded_at"] < today - timedelta(days=30)
        ]

        if len(old_items) == 0:
            st.info("아직 30일 이상 지난 분실물이 없습니다. 👍")
        else:
            df_old = pd.DataFrame(old_items)
            df_old["발견 날짜"] = df_old["found_date"].apply(lambda d: d.strftime("%Y-%m-%d"))
            df_old["업로드 시각"] = df_old["uploaded_at"].dt.strftime("%Y-%m-%d %H:%M")

            df_old = df_old.rename(
                columns={
                    "name": "물건 이름",
                    "location": "발견 장소",
                    "floor": "층수",
                    "uploader": "업로더",
                    "resolved": "해결 여부",
                }
            )

            st.dataframe(
                df_old[["물건 이름", "발견 장소", "층수", "발견 날짜", "업로드 시각", "업로더", "해결 여부"]],
                use_container_width=True,
                hide_index=True,
            )

# ===========================================================
# TAB 5 — 랭킹
# ===========================================================
with tabs[4]:
    st.subheader("🏆 분실물 업로드 랭킹")

    if len(st.session_state.user_stats) == 0:
        st.info("아직 업로드한 사용자가 없습니다.")
    else:
        rank_data = []
        for name, info in st.session_state.user_stats.items():
            rank_data.append(
                {"이름": name, "업로드 횟수": info["upload_count"]}
            )

        rank_df = pd.DataFrame(rank_data).sort_values(
            by="업로드 횟수", ascending=False
        ).reset_index(drop=True)
        rank_df["순위"] = rank_df.index + 1
        rank_df = rank_df[["순위", "이름", "업로드 횟수"]]

        st.dataframe(rank_df, use_container_width=True, hide_index=True)

# ===========================================================
# TAB 6 — 알림 / 설정
# ===========================================================
with tabs[5]:
    st.subheader("🔔 알림 설정 및 내역")

    # 간단히 "내 이름" 입력해서 그 사람 기준으로 알림 설정
    current_user = st.text_input("⚙️ 알림 설정할 사용자 이름", value="25116 이래나")
    stats = st.session_state.user_stats.get(
        current_user, {"upload_count": 0, "notification_on": True}
    )

    notif_on = st.checkbox(
        f"새 분실물 등록 시 알림 받기 (현재: {'ON' if stats['notification_on'] else 'OFF'})",
        value=stats["notification_on"],
    )

    if notif_on != stats["notification_on"]:
        stats["notification_on"] = notif_on
        st.session_state.user_stats[current_user] = stats
        st.success("알림 설정이 저장되었습니다.")

    st.markdown("---")
    st.markdown("### 📋 전체 알림 내역")

    if len(st.session_state.notifications) == 0:
        st.info("현재 알림이 없습니다.")
    else:
        for n in st.session_state.notifications:
            st.write(f"[{n['time'].strftime('%Y-%m-%d %H:%M:%S')}] {n['message']}")

        if st.button("🗑️ 알림 모두 지우기"):
            st.session_state.notifications = []
            st.success("알림을 모두 삭제했습니다.")
