import mysql.connector

#testing
db = mysql.connector.connect(host="localhost",
                     user="root",
                     password="root",
                     db = "bookstore_POS",
                     consume_results=True)


cur = db.cursor()




cur.execute("CREATE DATABASE IF NOT EXISTS bookstore_POS")

cur.execute(" CREATE  TABLE IF NOT EXISTS `customers` (`id` INT  AUTO_INCREMENT ,`name` VARCHAR(150) NOT NULL ,`email` VARCHAR(150) ,`tel` VARCHAR(20) ,`created_at` DATETIME ,`updated_at` DATETIME ,PRIMARY KEY (`ID`)) ;")

cur.execute("CREATE  TABLE IF NOT EXISTS `invoices` (`id` INT  AUTO_INCREMENT ,`number` VARCHAR(150) NOT NULL ,`sub_total` FLOAT(10,2) ,`tax_total` FLOAT(10,2) ,`total` FLOAT(10,2)  ,`customer_id` INT ,`created_at` DATETIME ,`updated_at` DATETIME ,PRIMARY KEY (`ID`),FOREIGN KEY (customer_id) REFERENCES customers(id) );")

cur.execute("CREATE  TABLE IF NOT EXISTS `invoice_lines` (`id` INT  AUTO_INCREMENT ,`description` VARCHAR(150) NOT NULL ,`unit_price` INT ,`sub_total` FLOAT(10,2) ,`quantity` INT , `tax_total` FLOAT(10,2) ,`tax_id` INT ,`sku_id` INT ,`invoice_id` INT ,`created_at` DATETIME ,`updated_at` DATETIME ,PRIMARY KEY (`ID`), FOREIGN KEY (invoice_id) REFERENCES invoices(id) );")

cur.execute("SELECT count(*) `Number of customers purchase more than 5 books` from (SELECT  customers.id `Customer ID` , count(distinct invoices.number) `Number of orders` , sum(invoice_lines.quantity) `Number of books bought` from customers join invoices on invoices.customer_id = customers.id join invoice_lines on invoice_lines.invoice_id = invoices.id group by customers.id having `Number of books bought` > 5)a")


cur.execute("""SELECT 
    COUNT(DISTINCT customers.id) `Customer ID`,
    COUNT(invoices.number) `Number of orders`
FROM
    customers
        JOIN
    invoices ON invoices.customer_id = customers.id
GROUP BY customer_id
HAVING `Number of orders` = 0""")

cur.execute("""SELECT 
    customers.id `Customer ID`,
    GROUP_CONCAT(invoice_lines.description) `List of books bought`
FROM
    customers
        JOIN
    invoices ON invoices.customer_id = customers.id
        JOIN
    invoice_lines ON invoice_lines.invoice_id = invoices.id
GROUP BY customers.id""")

db.close()