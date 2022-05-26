#select a database which want to choose to work
-- USE sql_store;

#select all data from table customers
-- SELECT * FROM customers;

-- SELECT * FROM customers
-- where customer_id=1
-- order by first_name

-- make an alias using as 
-- select last_name,first_name,points, (points + 10)*100 as 'discount factor' 
-- from customers

-- select name, unit_price, (unit_price *1.1) as new_price 
-- from products

-- select * from customers where birth_date <'1990-01-01'
-- select * from orders where order_date >= '2019-01-01'
-- select * from customers 	
-- where birth_date>'1990-01-01' or points>1000 
-- select * from order_items where order_id=6 and unit_price*quantity > 30
-- select * from customers where state in ('va','fl','ga')
-- select * from customers where state not in ('va','fl','ga')

-- select * from products where quantity_in_stock in (49,38,72)
-- select * from customers where points between 1000 and 3000
-- select * from customers where birth_date between '1990-01-01' and '2000-01-01'
-- select * from customers where last_name like '%b%'
-- select * from customers where address like '%avenue%' or address like '%trail%';
-- select * from customers where phone like '%9'

select * from customers 
where first_name like 'ELKA' or first_name like 'ambur';

select * from customers 
where first_name regexp 'ELKA|ambur';


select * from customers 
where last_name regexp 'ey$|on$';

select * from customers 
where last_name regexp '^my|^se';

select * from customers 
where last_name regexp 'b[ru]'; 

-- Null operator
select * from customers where phone is Null;

select * from orders where shipper_id is Null;

select * from customers order by state,first_name desc;

select *,quantity * unit_price as 'total price' 
from order_items where order_id=2 order by 'total price'  desc;

-- Limit clause
select * from customers order by points desc limit 3;

-- Inner joins
select * from orders join customers on orders.customer_id = customers.customer_id ;

select order_id, p.product_id, quantity , oi.unit_price from order_items oi join products p on oi.product_id = p.product_id;

select * from order_items oi join sql_inventory.products p on oi.product_id =p.product_id;

-- Self Joins
use sql_hr;
select 
e.employee_id,
e.first_name,
m.first_name as manager
from employees e
join employees m on e.reports_to =m.employee_id;

-- joining Multiple Tables

Use sql_invoicing;

select p.client_id,p.payment_id, pm.name,c.name,c.address,c.city 
from payments p 
join clients c on p.client_id = c.client_id
join payment_methods pm on p.payment_method = pm.payment_method_id;


-- Compound join conditions
use sql_store;
select * from order_items oi
join order_item_notes oin
on oi.order_id=oin.order_id
and oi.product_id=oin.product_id;

-- INNER JOINS END --

-- Outer joins start

select p.product_id,p.name, oi.quantity from order_items oi
right join products p on p.product_id= oi.product_id;

-- multiple tables

select p.product_id,p.name, oi.quantity 
from order_items oi
right join products p on p.product_id= oi.product_id;

select 
c.customer_id,
c.first_name,
o.order_id,
sh.name as Shippers 
from customers c
left join orders o 
on c.customer_id=o.customer_id
left join shippers sh
on o.shipper_id=sh.shipper_id
order by c.customer_id;


select o.order_date,
o.order_id,
c.first_name as customer,
sh.name as shipper,
os.name as status
from orders o
left join customers c on c.customer_id=o.customer_id
left join shippers sh
on sh.shipper_id=sh.shipper_id
join order_statuses os
on o.status=os.order_status_id;


-- self outer joins

use sql_hr;
select 
e.employee_id,
e.first_name,
m.first_name as manager
from employees e
left join employees m
on e.reports_to=m.employee_id;



-- Using clause

select o.order_date,
o.order_id,
c.first_name as customer,
sh.name as shipper,
os.name as status
from orders o
left join customers c 
-- same thing but shorter
-- on c.customer_id=o.customer_id 
using(customer_id)
left join shippers sh
-- on sh.shipper_id=sh.shipper_id
using(shipper_id)
join order_statuses os
on o.status=os.order_status_id;


select p.date,
c.name,
p.amount,
pm.name
from payments p
join clients c 
using(client_id)
join payment_methods pm
on p.payment_method= pm.payment_method_id;


-- cross join is used to join every record of table 1 and table 2

-- cross join (every record 1st table to 2nd table) didnot work explicit
select 
c.first_name,
p.name
from customers c join products p 
order by c.first_name;

-- cross join (every record 1st table to 2nd table) didnot work implicit
select 
c.first_name,
p.name
from customers c, products p 
order by c.first_name;

-- implicit
select * from products s , shippers;

-- explicit
select * from products s cross join shippers;


-- Unions
-- combine column using join
-- combine row using union, combine columns in different tables
select customer_id,
first_name,
points,
'Bronze' as type
from customers
where points<2000
UNION
select customer_id,
first_name,
points,
'Silver'
from customers
where points between 2000 and 3000
UNION
select customer_id,
first_name,
points,
'Gold'
from customers
where points>=3000
order by first_name;


-- column attributes

Insert into customers(first_name,last_name,birth_date,phone,address,city,state,points)
values('Syed','Mehmaam','1998-01-20','0315656587','Malir','karachi','SI',7000);
-- multiple insert
Insert into customers(first_name,last_name,birth_date,phone,address,city,state,points)
values('Syed','Mehmaam','1998-01-20','0315656587','Malir','karachi','SI',7000),
('Syed','Mehmaam','1998-01-20','0315656587','Malir','karachi','SI',7000),
('Syed','Mehmaam','1998-01-20','0315656587','Malir','karachi','SI',7000);

-- copy table (abc copy the values o fproduct table) not copy primary key auto increment etc
create table abc as select * from products;



-- update
update invoices
set payment_total =10,payment_date='2020-01-01'
where invoice_id =1;
-- update multiple
update invoices
set payment_total =10,payment_date='2020-01-01'
where invoice_id in (1,2);

-- not update
select first_name, birth_date , points,points + 50 as bonus from customers
where birth_date < '1990-01-01'
Union
select first_name, birth_date , points,points as bonus from customers;

-- update
update customer set points = points + 50 where birth_date < '1990-01-01';


-- sub queries

update orders set comments='Gold Customer' where customer_id in (
select customer_id from customers where points> 3000);

-- delete 
delete from invoices; -- delete all data
delete from invoices where invoices_id =1;

-- restoring database
