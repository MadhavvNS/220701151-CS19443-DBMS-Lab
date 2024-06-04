1. 
	ALTER TABLE emp
	ADD CONSTRAINT my_emp_id_pk PRIMARY KEY (id);

2. 
	ALTER TABLE dept
	ADD CONSTRAINT my_dept_id_pk PRIMARY KEY(id);

3.
	ALTER TABLE emp
	ADD (dept_id NUMBER(7));
	ALTER TABLE emp
	ADD CONSTRAINT my_emp_dept_id_fk
	FOREIGN KEY (dept_id) REFERENCES dept(id);

4. 
	ALTER TABLE EMP
	ADD commission NUMBER(2,2)
	CONSTRAINT my_emp_comm_ck CHECK (commission >= 0);
