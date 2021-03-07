-- CONSTRAINT TO DO NOT PERMIT MORE THAN 10 DIFFERENTS PRODUCTS IN THE SAME TRANSACTION.
CREATE OR REPLACE FUNCTION check_max_products_on_sales()
  RETURNS trigger AS
$func$
BEGIN
   IF EXISTS (SELECT count(1) FROM tb_order_details WHERE id_order = NEW.id_order GROUP BY id_order HAVING (count(1)=10)) THEN
      RAISE EXCEPTION 'The maximum number of products per sale is 10.';
   END IF;
   RETURN NEW;
END
$func$ LANGUAGE plpgsql;


-- TRIGGER FOR check_max_products_on_sales()
CREATE TRIGGER trigger_max_products_on_sales
BEFORE INSERT ON "tb_order_details"
FOR EACH ROW EXECUTE FUNCTION check_max_products_on_sales();


-- FUNCTION TO CALCULATE A DISCOUNT TO CUSTOMER
CREATE OR REPLACE FUNCTION order_discount(id_param INTEGER) 
  RETURNS INTEGER AS
$func$
  DECLARE 
    discount INTEGER;
	amount DECIMAL;
BEGIN
	SELECT SUM(total) INTO amount from (
      SELECT id_order, SUM(unit_price * quantity) total
      FROM tb_orders tor, tb_order_details tod
      WHERE tor.id=tod.id_order AND id_costumer = id_param GROUP BY id_order) tb_total;
	
	discount := 0;
	
    IF amount >= 1000 AND amount <= 5000 THEN
      discount := 10;
    ELSIF amount >= 5001 AND amount <= 15000 THEN
      discount := 15;
	ELSIF amount > 15000 THEN
      discount := 20;
    END IF;
    RETURN discount;
END
$func$ LANGUAGE plpgsql;
  

-- FUNCTION TO INSERT THE DISCOUNT IN A SALE
CREATE OR REPLACE FUNCTION insert_order_discount()
  RETURNS trigger AS
$func$
BEGIN
   NEW.discount := order_discount(NEW.id_costumer);
   RETURN NEW;
END
$func$  LANGUAGE plpgsql;
  
-- TRIGGER FOR insert_order_discount()
CREATE TRIGGER trigger_insert_order_discount
BEFORE INSERT ON "tb_orders" 
FOR EACH ROW EXECUTE PROCEDURE insert_order_discount(); 