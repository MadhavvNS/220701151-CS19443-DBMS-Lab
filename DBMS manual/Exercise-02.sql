
1.
	CREATE TABLE my_employee
	(id NUMBER(4) CONSTRAINT my_employee_id_nn NOT NULL,
	last_name VARCHAR2(25),
	first_name VARCHAR2(25),
	userid VARCHAR2(8),
	salary NUMBER(9,2));


2. 
	INSERT INTO my_employee
	VALUES (1, ’Patel’, ’Ralph’, ’rpatel’, 895);

3.
                Select * from my_employee


4.
	INSERT INTO my_employee
	VALUES (&p_id, ’&p_last_name’, ’&p_first_name’,
	lower(substr(’&p_first_name’, 1, 1) ||
	substr(’&p_last_name’, 1, 7)), &p_salary);


5.
	COMMIT;


6. 
	SET last_name = ’Drexler’
	WHERE id = 3;

7. 
	UPDATE my_employee
	SET salary = 1000
	WHERE salary < 900;


8. 
	DELETE
	FROM my_employee
	WHERE last_name = ’Dancs’;

9.
   Delete from my_employee where id=4;
