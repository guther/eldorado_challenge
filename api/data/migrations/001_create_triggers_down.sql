DROP TRIGGER IF EXISTS trigger_max_products_on_sales ON tb_order_details;
DROP TRIGGER IF EXISTS trigger_insert_order_discount ON tb_orders;
DROP FUNCTION IF EXISTS check_max_products_on_sales();
DROP FUNCTION IF EXISTS insert_order_discount();
DROP FUNCTION IF EXISTS order_discount(integer);