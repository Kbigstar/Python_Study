CREATE TABLE stock (
        code VARCHAR2(10) PRIMARY KEY
       ,name VARCHAR2(100)
       ,market VARCHAR2(10)
       ,marcap NUMBER
       ,stocks NUMBER
       ,use_yn VARCHAR2(1) DEFAULT 'N'
 );
CREATE TABLE stock_price (
       code VARCHAR2(10) 
      ,seq  NUMBER
      ,price NUMBER
      ,create_dt DATE DEFAULT SYSDATE
);
CREATE SEQUENCE stock_seq 
START WITH 1
INCREMENT BY 1
MINVALUE 1
MAXVALUE 9999999999;
select *
from stock;

    INSERT INTO stock (code, name, market, marcap, stocks)
    VALUES ('1234', '', '', '','');

UPDATE stock
SET use_yn ='Y'
WHERE name LIKE '%»ï¼º%';
SELECT *
FROM stock
WHERE USE_YN ='Y';
    
INSERT INTO stock_price (code, seq, price)
VALUES (:1, stock_seq.NEXTVAL, :2);
;
SELECT stock_seq.NEXTVAL
FROm dual;

SELECT *
FROM stock_price;

delete stock_price;
drop sequence stock_seq;