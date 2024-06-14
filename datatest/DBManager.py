import cx_Oracle

class DBManager:
    def __init__(self):
        self.conn = None
        self.get_connection()
    def get_connection(self):
        self.conn = cx_Oracle.connect("", ""
                                      , "")#"user", "password", "ip:port/xe"
        # 실행 시 "?" 안에 비밀번호 쓰기!
        print("DB 접속됨.")
        return self.conn
    def __del__(self):
        # 사용이 끝나면 호출 됨. (소멸자)
        try:
            print("소멸자")
            if self.conn:
                self.conn.close()
                print("접속을 종료 함.")
        except Exception as e:
            print("__del__", str(e))
    def insert(self, query, param):
        cursor = self.conn.cursor()
        cursor.execute(query, param)
        self.conn.commit()
        cursor.close()

if __name__ == '__main__' :
    db = DBManager()
