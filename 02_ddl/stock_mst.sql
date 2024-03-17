CREATE TABLE stock_mst (
     id MEDIUMINT NOT NULL AUTO_INCREMENT,
     stock_number CHAR(4) NOT NULL,
     jpn_stock_flg CHAR(1) NOT NULL,
     stock_kbn CHAR(2) NOT NULL,
     stock_market CHAR(1) NOT NULL,
     company_name VARCHAR(1024) NOT NULL,
     company_url VARCHAR(256) ,
     note VARCHAR(2048),
     PRIMARY KEY (id)
);
