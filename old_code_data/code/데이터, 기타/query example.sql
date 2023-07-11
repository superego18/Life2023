create database shop;
use shop;
create table goods
(
goods_id char(4) not null,
goods_name varchar(100) not null,
goods_classify varchar(32) not null,
sell_price integer,
buy_price integer,
register_date date,
primary key (goods_id)
);
alter table goods add column goods_name_eng varchar(100);
alter table goods drop column goods_name_eng
insert into goods value ('0001', '티셔츠', '의류', 1000, 500, '2020-09-20')
insert into goods value ('0002', '펀칭기', '사무용품', 500, 320, '2020-09-11')
select goods_id, goods_name, buy_price
from goods;
select * from goods;
select goods_id as id,
	goods_name as name,
    buy_price as price
from goods;
select '상품' as category,
	38 as num,
    '2022-01-01' as date,
    goods_id,
    goods_name,
    sell_price, buy_price, sell_price - buy_price as profit
from goods;

insert into goods value ('0003', '펀칭기2', '사무용품', 500, 320, '2020-09-11')
select distinct goods_classify from goods;
select goods_name, goods_classify from goods where goods_classify='사무용품';
select *, sell_price - buy_price as profit from goods where sell_price - buy_price >= 500;
select goods_classify, count(*) from goods group by goods_classify;
select goods_classify, avg(sell_price) from goods group by goods_classify  having avg(sell_price) >= 750;

create view GoodSum (goods_classify, cnt_goods) as select goods_classify, count(*) from g0oods group by goods_classify;
select * from GoodSum;

select goods_classify, cnt_goods
from (
	select goods_classify, count(*) as cnt_goods
    from goods
    group by goods_classify
) as GoodsSum2;

select * from GoodSum;

create table SampleLike
(strcol varchar(6) not null,
primary key (strcol));

insert into SampleLike (strcol) values ('abcddd');
insert into SampleLike (strcol) values ('dddabc');
insert into SampleLike (strcol) values ('abdddc');
insert into SampleLike (strcol) values ('abcdd');
insert into SampleLike (strcol) values ('ddabc');
insert into SampleLike (strcol) values ('abddc');

select * from SampleLike where strcol like 'ddd%';

select * from goods where sell_price between 100 and 1000;
select * from goods where 100 <= sell_price <= 1000;

select * from goods where buy_price in (320, 500);

select goods_name, sell_price,
case when sell_price >= 6000 then '고가'
when sell_price >= 3000 and sell_price < 6000 then '중가'
when sell_price < 3000 then '저가'
else null
end as price_classify from goods;

create table goods2
(
goods_id char(4) not null,
goods_name varchar(100) not null,
goods_classify varchar(32) not null,
sell_price integer,
buy_price integer,
register_date date,
primary key (goods_id)
);

insert into goods2 values ('0001', '티셔츠', '의류', 1000, 500, '2020-09-20');
insert into goods2 values ('0002', '펀칭기', '사무용품', 500, 320, '2020-09-11');
insert into goods2 values ('0003', '와이셔츠', '의류', 4000, 2800, Null);
insert into goods2 values ('0009', '장갑', '의류', 800, 500, Null);
insert into goods2 values ('0010', '주전자', '주방용품', 2000, 1700, '2020-09-20');

select * from goods2;
select * from goods;

select * from goods union all select * from goods2;

create table storegoods
(store_id char(4) not null,
store_name varchar(200) not null,
goods_id char(4) not null,
num integer not null,
primary key (store_id, goods_id));

select * from storegoods;

insert into storegoods values ('000A', '서울', '0001', 30);
insert into storegoods values ('000A', '서울', '0002', 50);
insert into storegoods values ('000A', '서울', '0003', 15);
insert into storegoods values ('000B', '대전', '0002', 30);
insert into storegoods values ('000B', '대전', '0003', 120);
insert into storegoods values ('000B', '대전', '0004', 20);
insert into storegoods values ('000B', '대전', '0006', 10);
insert into storegoods values ('000B', '대전', '0007', 40);
insert into storegoods values ('000C', '부산', '0003', 20);
insert into storegoods values ('000C', '부산', '0004', 50);

select store.store_id, store.store_name, store.goods_id, goods.goods_name, goods.sell_price
from storegoods as store
left outer join goods on store.goods_id = goods.goods_id;

select distinct(goods_id) from goods;

select goods_name, goods_classify, sell_price,
rank() over (partition by goods_classify order by sell_price) as ranking from goods2;

select * from goods;

select * from iris;

use exam;
select * from price;

create table price2(
날짜 varchar(10),
티커 varchar(6),
종가 int,
거래량 int,
primary key(날짜, 티커)
);

insert into price2 values ('2021-01-02', '000001', 1340, 1000), ('2021-01-03', '000001', 1315, 2000), ('2021-01-02', '000002', 500, 200);
select * from price2;sys_config

insert into price2 values
('2021-01-02', '000001', 1340, 1000),
('2021-01-03', '000001', 1315, 2000),
('2021-01-02', '000002', 500, 200),
('2021-01-03', '000002', 1380, 3000)
as new
on duplicate key update
종가 = new.종가, 거래량 = new.거래량;

insert into price2 values
('2021-01-02', '000001', 1300, 1100),
('2021-01-04', '000001', 1300, 2000)
as new
on duplicate key update
종가 = new.종가, 거래량 = new.거래량;

use world;
select * from city;
drop database world;