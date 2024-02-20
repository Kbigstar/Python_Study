sql = { 'select_data': '''
                        SELECT *
                        FROM stock
                        WHERE USE_YN ='Y'
                        '''
       , 'insert_data': '''
                  INSERT INTO stock_price (code, seq, price)
                  VALUES (:1, NEXTVAL.stock_seq, :2)
                  '''
       }
# 정해진 시간 마다
# 조회 종목의 현재가를 수집하여 stock_price 테이블에 저장