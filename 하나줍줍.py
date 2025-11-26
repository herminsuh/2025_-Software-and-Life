import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import uuid # 고유 ID 생성을 위해 사용

# --- 1. 초기 설정 및 데이터 초기화 (DB 역할) ---

st.set_page_config(
    page_title="하나고 온라인 분실물함 - 하나줍줍 (완전판)",
    page_icon="🎒",
    layout="wide"
)

# 데이터베이스 역할: LostItem 테이블 초기화
if 'lost_items' not in st.session_state:
    st.session_state.lost_items = [
        {
            'item_id': str(uuid.uuid4()),
            'name': '학생증 (김하나)',
            'location': '급식실 입구',
            'floor': 1,
            'found_date': '2025-11-26',
            'uploaded_at': datetime(2025, 11, 26, 9, 30),
            'photo_url': 'https://via.placeholder.com/150?text=ID+Card',
            'uploader_id': 'webdev_01',
            'is_resolved': False
        },
        # 오래된 분실물 테스트용 데이터 (30일 전)
        {
            'item_id': str(uuid.uuid4()),
            'name': '오래된 우산',
            'location': '과학동 복도',
            'floor': 2,
            'found_date': '2025-10-25',
            'uploaded_at': datetime(2025, 10, 25, 10, 0),
            'photo_url': 'https://via.placeholder.com/150?text=Old+Umbrella',
            'uploader_id': 'helper_02',
            'is_resolved': False
        },
        {
            'item_id': str(uuid.uuid4()),
            'name': '갤럭시 버즈',
            'location': '3층 305호 교실',
            'floor': 3,
            'found_date': '2025-11-25',
            'uploaded_at': datetime(2025, 11, 26, 8, 0),
            'photo_url': 'https://via.placeholder.com/150?text=Earbuds',
            'uploader_id': 'helper_02',
            'is_resolved': False
        },
        {
            'item_id': str(uuid.uuid4()),
            'name': '영어 교과서',
            'location': '도서관 4층',
            'floor': 4,
            'found_date': '2025-11-20',
            'uploaded_at': datetime(2025, 11, 25, 15, 0),
            'photo_url': 'https://via.placeholder.com/150?text=Book',
            'uploader_id': 'helper_02',
            'is_resolved': False
        },
    ]

# 데이터베이스 역할: User 테이블 초기화
if 'users' not in st.session_state:
    st.session_state.users = {
        'webdev_01': {'name': '웹 개발자', 'upload_count': 1, 'notification_on': True},
        'helper_02': {'name': '친절한 학생', 'upload_count': 3, 'notification_on': True},
        'newbie_03': {'name': '신입생', 'upload_count': 0, 'notification_on': False}, # 알림 OFF 테스트용
    }

# 알림 리스트 초기화
if 'notifications' not in st.session_state:
    st.session_state.notifications = [
        {'time': datetime(2025, 11, 26, 9, 30), 'message': '새로운 분실물: 학생증 (김하나)이 등록되었습니다.'},
    ]

# --- 2. 메인 페이지 UI 및 탭 구성 ---

st.title("🎒 하나고등학교 온라인 분실물함 – '하나줍줍'")

# 탭 구성 (총 6개의 탭)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 홈", 
    "📝 업로드", 
    "🔍 전체/검색 목록", 
    "⏳ 오래된 분실물", # 요청 5번 기능
    "🏆 랭킹", 
    "🔔 알림/설정" # 요청 7번 기능
])

# ==============================================================================
# 탭 1: 홈 (Home) - 최근 분실물 게시판
# ==============================================================================
with tab1:
    st.header("✨ 최근 분실물 게시판")
    st.markdown("가장 최근에 등록된 분실물 12개를 보여줍니다.")

    items_df = pd.DataFrame(st.session_state.lost_items)
    
    if items_df.empty:
        st.info("등록된 분실물이 아직 없습니다.")
    else:
        recent_items_df = items_df.sort_values(by='uploaded_at', ascending=False).head(12).reset_index(drop=True)
        
        cols = st.columns(3)
        for i, row in recent_items_df.iterrows():
            col = cols[i % 3]
            with col:
                st.info(f"📌 {row['name']}", icon="📦")
                st.image(row['photo_url'], caption=f"발견 장소: {row['location']}", width=200)
                st.caption(f"📅 발견: {row['found_date']}")
                st.caption(f"⬆️ 업로드: {row['uploaded_at'].strftime('%m-%d %H:%M')}")
                st.caption(f"해결: {'✅' if row['is_resolved'] else '❌'}")
    
# ==============================================================================
# 탭 2: 분실물 업로드 (Upload)
# ==============================================================================
with tab2:
    st.header("📝 새로운 분실물 등록")
    
    with st.form("lost_item_upload_form"):
        item_name = st.text_input("📦 물건 이름", placeholder="예: 아이폰 14, 체육복 상의")
        
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("📍 발견 장소 (상세)", placeholder="예: 3층 305호 앞 복도")
        with col2:
            floor_options = [1, 2, 3, 4, 5, 0]
            floor = st.selectbox("🏢 층수", floor_options, index=2)
        
        found_date = st.date_input("📅 발견 날짜", datetime.now().date())
        current_uploader_id = st.selectbox("🔑 업로더 ID (테스트용)", list(st.session_state.users.keys()))
        uploaded_file = st.file_uploader("📸 분실물 사진 (선택)", type=['png', 'jpg', 'jpeg'])
        
        submitted = st.form_submit_button("✅ 분실물 등록")

    if submitted:
        if not item_name or not location:
            st.error("물건 이름과 발견 장소는 필수 입력 사항입니다.")
        else:
            new_id = str(uuid.uuid4())
            photo_url = "https://via.placeholder.com/150?text=Uploaded+Image" if uploaded_file else 'https://via.placeholder.com/150?text=No+Image'

            new_item = {
                'item_id': new_id,
                'name': item_name,
                'location': location,
                'floor': floor,
                'found_date': found_date.strftime('%Y-%m-%d'),
                'uploaded_at': datetime.now(),
                'photo_url': photo_url,
                'uploader_id': current_uploader_id,
                'is_resolved': False
            }
            
            # 1. LostItem 테이블에 추가
            st.session_state.lost_items.append(new_item)
            
            # 2. User 테이블: 업로드 횟수 증가
            st.session_state.users[current_uploader_id]['upload_count'] += 1
            
            # 3. 알림 생성 (요청 7번 기능)
            for user_id, user_data in st.session_state.users.items():
                if user_data['notification_on']:
                    st.session_state.notifications.insert(0, { # 최신 알림을 맨 앞에 추가
                        'time': datetime.now(), 
                        'message': f"🔔 **{user_data['name']}**님! 새로운 분실물: {item_name}이 등록되었습니다. (업로더: {st.session_state.users[current_uploader_id]['name']})"
                    })

            st.success(f"🎉 **{item_name}** 분실물 정보가 성공적으로 등록되었습니다!")
            st.balloons()
            
# ==============================================================================
# 탭 3: 전체/검색 목록 (List and Search/Filter)
# ==============================================================================
with tab3:
    st.header("🔍 분실물 검색 및 전체 목록")

    df = pd.DataFrame(st.session_state.lost_items)
    
    if df.empty:
        st.info("현재 등록된 분실물이 없습니다.")
    else:
        col_search, col_floor, col_date = st.columns([3, 1, 2])
        
        with col_search:
            search_query = st.text_input("📝 물건 이름/장소 검색", placeholder="예: 이어폰, 305호")
        
        with col_floor:
            floor_filter = st.selectbox("🏢 층수 필터", ["전체", 0, 1, 2, 3, 4, 5], index=0)
            
        with col_date:
            sort_order = st.radio("⏳ 정렬 기준", ["최신순", "오래된순"], index=0, horizontal=True)

        filtered_df = df.copy()

        if search_query:
            filtered_df = filtered_df[
                filtered_df['name'].str.contains(search_query, case=False) |
                filtered_df['location'].str.contains(search_query, case=False)
            ]
            
        if floor_filter != "전체":
            filtered_df = filtered_df[filtered_df['floor'] == floor_filter]

        ascending_sort = True if sort_order == "오래된순" else False
        filtered_df = filtered_df.sort_values(by='uploaded_at', ascending=ascending_sort)

        # 표시 형식 정리
        filtered_df['업로드 시각'] = filtered_df['uploaded_at'].dt.strftime('%Y-%m-%d %H:%M')

        display_df = filtered_df[[
            'name', 'location', 'floor', 'found_date', '업로드 시각', 'uploader_id', 'is_resolved'
        ]].rename(columns={
            'name': '물건 이름',
            'location': '발견 장소',
            'floor': '층수',
            'found_date': '발견 날짜',
            'uploader_id': '업로더 ID',
            'is_resolved': '해결 여부'
        })
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        st.caption(f"총 {len(filtered_df)}개의 분실물이 검색되었습니다.")

# ==============================================================================
# 탭 4: 오래된 분실물 게시판 (Old Lost Items) - 요청 5번 기능
# ==============================================================================
with tab4:
    st.header("⏳ 오래된 분실물")
    
    # 30일(예시)이 지난 분실물을 찾습니다.
    threshold_date = datetime.now() - timedelta(days=30)
    
    if df.empty:
        st.info("등록된 분실물이 없습니다.")
    else:
        old_items_df = df[df['uploaded_at'] < threshold_date].sort_values(by='uploaded_at', ascending=True)
        
        st.warning(f"⚠️ **{threshold_date.strftime('%Y년 %m월 %d일')}** 이전에 등록된 분실물 **{len(old_items_df)}개**입니다.")
        st.caption("장기간 주인을 찾지 못한 물건들은 일정 기간 후 학교 행정실로 인계될 수 있습니다.")

        # 표시 형식 정리
        old_items_df['업로드 시각'] = old_items_df['uploaded_at'].dt.strftime('%Y-%m-%d %H:%M')

        display_old_df = old_items_df[[
            'name', 'location', 'floor', 'found_date', '업로드 시각', 'is_resolved'
        ]].rename(columns={
            'name': '물건 이름',
            'location': '발견 장소',
            'floor': '층수',
            'found_date': '발견 날짜',
            'is_resolved': '해결 여부'
        })
        
        if display_old_df.empty:
            st.info("아직 30일 이상 지난 오래된 분실물은 없습니다. (현재: 2025-11-26)")
        else:
            st.dataframe(display_old_df, use_container_width=True, hide_index=True)


# ==============================================================================
# 탭 5: 랭킹 (Ranking)
# ==============================================================================
with tab5:
    st.header("🏆 선행 랭킹 게시판")
    
    user_list = [
        {'user_id': uid, 'name': data['name'], 'upload_count': data['upload_count']} 
        for uid, data in st.session_state.users.items()
    ]
    rank_df = pd.DataFrame(user_list)
    
    rank_df = rank_df.sort_values(by='upload_count', ascending=False).reset_index(drop=True)
    rank_df['순위'] = rank_df.index + 1
    
    display_rank_df = rank_df[[
        '순위', 'name', 'upload_count'
    ]].rename(columns={
        'name': '이름',
        'upload_count': '업로드 횟수'
    })
    
    st.dataframe(display_rank_df, use_container_width=True, hide_index=True)
    st.caption("업로드 횟수는 분실물을 발견하여 등록한 횟수를 의미합니다.")

# ==============================================================================
# 탭 6: 알림/설정 (Notifications) - 요청 7번 기능
# ==============================================================================
with tab6:
    st.header("🔔 알림 리스트 및 설정")
    
    # 임시 로그인 사용자 (알림 ON/OFF 설정은 이 사용자를 대상으로 합니다)
    st.subheader("⚙️ 알림 수신 설정 (현재 사용자: 웹 개발자)")
    target_user_id = 'webdev_01'
    
    # 현재 설정 상태 가져오기
    current_setting = st.session_state.users.get(target_user_id, {}).get('notification_on', True)
    
    # 알림 ON/OFF 토글
    new_setting = st.checkbox(
        f"새 분실물 등록 시 알림 받기 (현재: {'ON' if current_setting else 'OFF'})", 
        value=current_setting
    )
    
    # 설정 변경 시 session_state 업데이트
    if new_setting != current_setting:
        st.session_state.users[target_user_id]['notification_on'] = new_setting
        st.toast("알림 설정이 저장되었습니다!", icon='✅')
        st.rerun() # 설정 변경을 즉시 반영

    st.markdown("---")
    
    st.subheader("📋 전체 알림 내역")
    
    if st.session_state.notifications:
        
        # 알림 DataFrame으로 변환
        notif_df = pd.DataFrame(st.session_state.notifications)
        notif_df['시간'] = notif_df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        for index, row in notif_df.iterrows():
            st.text(f"[{row['시간']}] {row['message']}")
            
        st.caption(f"총 {len(st.session_state.notifications)}개의 알림이 있습니다.")
        
        if st.button("🗑️ 알림 모두 지우기"):
            st.session_state.notifications = []
            st.rerun()
            
    else:
        st.info("새로운 알림이 없습니다.")

# --- 코드 종료 ---
