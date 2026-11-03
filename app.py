import streamlit as st
import pandas as pd
import psycopg2

st.title("📚 Madang 도서 주문 조회 시스템")

# 1. Neon DB 연결 함수 (캐시 적용)
@st.cache_resource
def init_connection():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"],
        sslmode=st.secrets["postgres"]["sslmode"]
    )

try:
    conn = init_connection()
    st.success("Neon DB 연결 성공!")
except Exception as e:
    st.error(f"데이터베이스 연결 실패: {e}")

# 2. 사용자 입력 및 조회 기능
name = st.text_input("조회할 고객 이름을 입력하세요 (예: 박지성)")

if st.button("주문 내역 조회"):
    if name:
        # PostgreSQL(Neon) 쿼리 실행
        query = """
            SELECT o.orderid, c.name, b.bookname, o.saleprice, o.orderdate 
            FROM Customer c, Orders o, Book b 
            WHERE c.name = %s AND c.custid = o.custid AND b.bookid = o.bookid;
        """
        
        try:
            # pandas를 이용해 쿼리 결과를 데이터프레임으로 가져오기
            df = pd.read_sql(query, conn, params=(name,))
            
            if not df.empty:
                st.dataframe(df)
            else:
                st.info("검색된 주문 내역이 없습니다.")
        except Exception as e:
            st.error(f"쿼리 실행 중 오류가 발생했습니다: {e}")
    else:
        st.warning("고객 이름을 입력해주세요.")