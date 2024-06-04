1.	CREATE TABLE dept
	(id NUMBER(7),
	name VARCHAR2(25));
	
	DESCRIBE dept


2. 

	CREATE TABLE emp
	(id NUMBER(7),
	last_name VARCHAR2(25),
	first_name VARCHAR2(25),
	dept_id NUMBER(7));
	
	DESCRIBE emp

3. 
	ALTER TABLE emp
	MODIFY (last_name VARCHAR2(50));

	DESCRIBE emp

4. 

	CREATE TABLE employees2 AS
	SELECT employee_id id, first_name, last_name, salary,
	department_id dept_id
	FROM employees;

5. 

	DROP TABLE emp;

6. 

	RENAME employees2 TO emp;

7.
   COMMENT ON TABLE emp IS ’Employee Information’;
   COMMENT ON TABLE dept IS ’Department Information’;

	   SELECT *
	   FROM user_tab_comments
	   WHERE table_name = ’DEPT’
  	 OR table_name = ’EMP’;

8. 
	
	ALTER TABLE emp
	DROP COLUMN FIRST_NAME;
	
	DESCRIBE emp;
