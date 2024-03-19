CREATE TABLE news_url_tbl (
id mediumint NOT NULL AUTO_INCREMENT,
text varchar(1024) NOT NULL,
url varchar(1024) NOT NULL,
user_check_flg char(1) default 0,
del_flg char(1) default 0,
create_datetime DATETIME(2),
PRIMARY KEY (id)
  );