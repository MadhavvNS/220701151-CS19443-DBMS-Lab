1. Add a table-level PRIMARY KEY constraint to the EMP table on the ID column. The constraint
   should be named at creation. Name the constraint my_emp_id_pk

	ALTER TABLE emp
	ADD CONSTRAINT my_emp_id_pk PRIMARY KEY (id);

2. Create a PRIMARY KEY constraint to the DEPT table using the ID column. The constraint
   should be named at creation. Name the constraint my_dept_id_pk.

	ALTER TABLE dept
	ADD CONSTRAINT my_dept_id_pk PRIMARY KEY(id);

3. Add a column DEPT_ID to the EMP table. Add a foreign key reference on the EMP table that
   ensures that the employee is not assigned to a nonexistent department. Name the constraint
   my_emp_dept_id_fk.

	ALTER TABLE emp
	ADD (dept_id NUMBER(7));
	ALTER TABLE emp
	ADD CONSTRAINT my_emp_dept_id_fk
	FOREIGN KEY (dept_id) REFERENCES dept(id);

4. Modify the EMP table. Add a COMMISSION column of NUMBER data type, precision 2, scale 2.
   Add a constraint to the commission column that ensures that a commission value is greater than
   zero.

	ALTER TABLE EMP
	ADD commission NUMBER(2,2)
	CONSTRAINT my_emp_comm_ck CHECK (commission >= 0);