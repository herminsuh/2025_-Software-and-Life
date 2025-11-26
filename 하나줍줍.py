import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import uuid  # 고유 ID
# -----------------------------------------------------------
# 초기 설정
# -----------------------------------------------------------
st.set_page_config(
    page_title="하나고 온라인 분실물함 - 하나줍줍 (완전판)",
    page_icon="🎒",
    layout="wide"
)

# -----------------------------------------------------------
# LostItem 테이블 초기화
# -----------------------------------------------------------
if 'lost_items' not in st.session_state:
    st.session_state.lost_items = [
        {
            'item_id': str(uuid.uuid4()),
            'name': '하나카드',
            'location': '매점 입구',
            'floor': 1,
            'found_date': '2025-11-26',
            'uploaded_at': datetime(2025, 11, 26, 9, 30),
            'photo_url': 'https://via.placeholder.com/300?text=ID+Card',
            'uploader_id': 'webdev_01',
            'is_resolved': False
        },
        # 테스트용 오래된 데이터
        {
            'item_id': str(uuid.uuid4()),
            'name': 'c타입 충전기',
            'location': 'A동 움파',
            'floor': 3,
            'found_date': '2025-10-25',
            'uploaded_at': datetime(2025, 10, 25, 10, 0),
            'photo_url': 'https://via.placeholder.com/300?text=Old+Charger',
            'uploader_id': 'helper_02',
            'is_resolved': False
        },
        {
            'item_id': str(uuid.uuid4()),
            'name': '갤럭시 버즈',
            'location': 'B305',
            'floor': 3,
            'found_date': '2025-11-25',
            'uploaded_at': datetime(2025, 11, 26, 8, 0),
            'photo_url': 'https://via.placeholder.com/300?text=Earbuds',
            'uploader_id': 'helper_02',
            'is_resolved': False
        },
        {
            'item_id': str(uuid.uuid4()),
            'name': '영어 교과서',
            'location': '급식실',
            'floor': 4,
            'found_date': '2025-11-20',
            'uploaded_at': datetime(2025, 11, 25, 15, 0),
            'photo_url': 'https://via.placeholder.com/300?text=Book',
            'uploader_id': 'helper_02',
            'is_resolved': False
        },
    ]

# -----------------------------------------------------------
# User 테이블 초기화
# -----------------------------------------------------------
if 'users' not in st.session_state:
    st.session_state.users = {
        'webdev_01': {'name': '25199 허민서', 'upload_count': 1, 'notification_on': True},
        'helper_02': {'name': '25116 이래나', 'upload_count': 3, 'notification_on': True},
        'newbie_03': {'name': '25196 표단', 'upload_count': 0, 'notification_on': False},
    }

# -----------------------------------------------------------
# 알림 테이블 초기화
# -----------------------------------------------------------
if 'notifications' not in st.session_state:
    st.session_state.notifications = [
        {'time': datetime(2025, 11, 26, 9, 30), 'message': '새로운 분실물: 학생증이 등록되었습니다.'},
    ]

# -----------------------------------------------------------
# UI 시작
# -----------------------------------------------------------
st.title("🎒 하나고등학교 온라인 분실물함 – '하나줍줍'")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 홈",
    "📝 업로드",
    "🔍 전체/검색 목록",
    "⏳ 오래된 분실물",
    "🏆 랭킹",
    "🔔 알림/설정"
])

# ===========================================================
# TAB 1 — 홈 (최근 분실물 게시판)
# ===========================================================
with tab1:
    st.header("✨ 최근 분실물 게시판 (사진 크게 보임!)")
    items_df = pd.DataFrame(st.session_state.lost_items)

    if items_df.empty:
        st.info("등록된 분실물이 없습니다.")
    else:
        recent_items_df = items_df.sort_values(by='uploaded_at', ascending=False).head(12)
        cols = st.columns(3)

        for i, row in recent_items_df.iterrows():
            col = cols[i % 3]
            with col:
                st.markdown(f"#### 📦 {row['name']}")
                st.image(row['photo_url'], use_column_width=True)   # ⭐ 사진 크게!
                st.caption(f"📍 {row['location']} | 🏢 {row['floor']}층")
                st.caption(f"📅 발견: {row['found_date']}")
                st.caption(f"⬆️ 업로드: {row['uploaded_at'].strftime('%m-%d %H:%M')}")

# ===========================================================
# TAB 2 — 업로드
# ===========================================================
with tab2:
    st.header("📝 새로운 분실물 등록")
    with st.form("lost_item_upload_form"):
        item_name = st.text_input("📦 물건 이름")
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("📍 발견 장소")
        with col2:
            floor = st.selectbox("🏢 층수", [0,1,2,3,4,5,6,7], index=1)

        found_date = st.date_input("📅 발견 날짜", datetime.now().date())
        current_uploader_id = st.selectbox("🔑 업로더 ID", list(st.session_state.users.keys()))
        uploaded_file = st.file_uploader("📸 사진 업로드", type=['png','jpg','jpeg'])

        submit = st.form_submit_button("등록하기")

    if submit:
        new_item = {
            'item_id': str(uuid.uuid4()),
            'name': item_name,
            'location': location,
            'floor': floor,
            'found_date': found_date.strftime("%Y-%m-%d"),
            'uploaded_at': datetime.now(),
            'photo_url': 'https://via.placeholder.com/300?text=Uploaded',
            'uploader_id': current_uploader_id,
            'is_resolved': False
        }

        st.session_state.lost_items.append(new_item)
        st.session_state.users[current_uploader_id]['upload_count'] += 1
        st.success("🎉 등록 완료!")
        st.balloons()

# ===========================================================
# TAB 3 — 전체/검색 목록 (이미지 카드 추가됨)
# ===========================================================
with tab3:
    st.header("🔍 전체/검색 목록")

    df = pd.DataFrame(st.session_state.lost_items)

    # 검색 UI
    col_search, col_floor, col_sort = st.columns([3,1,2])
    search_query = col_search.text_input("검색어 입력(이름/장소)")
    floor_filter = col_floor.selectbox("층수", ["전체",0,1,2,3,4,5,6,7])
    sort_order = col_sort.radio("정렬 기준", ["최신순", "오래된순"], horizontal=True)

    filtered = df.copy()
    if search_query:
        filtered = filtered[
            filtered['name'].str.contains(search_query, case=False) |
            filtered['location'].str.contains(search_query, case=False)
        ]
    if floor_filter != "전체":
        filtered = filtered[filtered['floor'] == floor_filter]

    filtered = filtered.sort_values(by='uploaded_at', ascending=(sort_order=="오래된순"))

    # 표 출력
    display_df = filtered.copy()
    display_df['업로드 시각'] = display_df['uploaded_at'].dt.strftime("%Y-%m-%d %H:%M")
    st.dataframe(display_df[['name','location','floor','found_date','업로드 시각','uploader_id','is_resolved']],
                 use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("🖼 사진으로 보기")

    # ⭐⭐ 이미지 카드 리스트 (사진 크게 보임)
    for _, row in filtered.iterrows():
        st.markdown("---")
        colA, colB = st.columns([1,2])
        with colA:
            st.image(row['photo_url'], width=250)  # ⭐ 사진 크게!
        with colB:
            st.markdown(f"### {row['name']}")
            st.write(f"📍 {row['location']}")
            st.write(f"🏢 {row['floor']}층")
            st.write(f"📅 발견: {row['found_date']}")
            st.write(f"⏳ 업로드: {row['uploaded_at'].strftime('%Y-%m-%d %H:%M')}")

# ===========================================================
# TAB 4 — 오래된 분실물
# ===========================================================
with tab4:
    st.header("⏳ 오래된 분실물")
    df = pd.DataFrame(st.session_state.lost_items)
    threshold_date = datetime.now() - timedelta(days=30)
    old_df = df[df['uploaded_at'] < threshold_date]

    if len(old_df)==0:
        st.info("30일 이상 지난 분실물이 없습니다.")
    else:
        old_df['업로드 시각'] = old_df['uploaded_at'].dt.strftime("%Y-%m-%d %H:%M")
        st.dataframe(old_df[['name','location','floor','found_date','업로드 시각','is_resolved']],
                     use_container_width=True, hide_index=True)

# ===========================================================
# TAB 5 — 랭킹
# ===========================================================
with tab5:
    st.header("🏆 업로드 랭킹")
    user_list = [{
        'name': data['name'],
        'upload_count': data['upload_count']
    } for _, data in st.session_state.users.items()]

    rank_df = pd.DataFrame(user_list).sort_values(by='upload_count', ascending=False)
    rank_df['순위'] = range(1, len(rank_df)+1)
    st.dataframe(rank_df[['순위','name','upload_count']], use_container_width=True, hide_index=True)

# ===========================================================
# TAB 6 — 알림
# ===========================================================
with tab6:
    st.header("🔔 알림 내역")
    for item in st.session_state.notifications:
        st.write(f"[{item['time'].strftime('%Y-%m-%d %H:%M:%S')}] {item['message']}")
