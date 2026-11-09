import streamlit as st
import pandas as pd
import psycopg2

st.title("📚 마당책 주문 조회 시스템")

# DB 연결을 생성하는 함수 (캐시 없이 매번 안전하게 새로 연결)
def get_connection():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"],
        sslmode=st.secrets["postgres"]["sslmode"]
    )

# 1. 초기 연결 테스트
try:
    test_conn = get_connection()
    test_conn.close()
    st.success("Neon DB 연결 성공!")
except Exception as e:
    st.error(f"데이터베이스 연결 실패: {e}")

# 2. 사용자 입력 및 조회 기능
name = st.text_input("귀하의 이름을 입력하세요 (예: 박지성)")

if st.button("주문 내역 조회"):
    if name:
        query = """
            SELECT o.orderid, c.name, b.bookname, o.saleprice, o.orderdate 
            FROM Customer c, Orders o, Book b 
            WHERE c.name = %s AND c.custid = o.custid AND b.bookid = o.bookid;
        """
        
        try:
            # 조회할 때마다 새로운 연결을 맺어 SSL 끊김 에러 원천 차단
            conn = get_connection()
            df = pd.read_sql(query, conn, params=(name,))
            conn.close()
            
            if not df.empty:
                st.dataframe(df)
            else:
                st.info("검색된 주문 내역이 없습니다.")
        except Exception as e:
            st.error(f"쿼리 실행 중 오류가 발생했습니다: {e}")
    else:
        st.warning("고객 이름을 입력해주세요.")름을 입력해주세요.")
