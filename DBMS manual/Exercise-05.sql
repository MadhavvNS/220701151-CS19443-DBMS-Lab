1.
    select last_name, salary
    from employees
    where salary > 12000;

2. 
    Select last_name, department_id from employees
    where employee_id = 176;

3.  Select last_name, salary
    from employees
    where salary>12000 or salary<5000;

4.
    Select lastname,jobid,startdate from employees 
    where startdate>='20-Feb-1998' and startdate<='01-May-1998'
    order by startdate ASC;

5.
    Select last_name, department_id from employees
    where department_id in (20,50)
    order by last_name;

6.
    Select last_name "Employee", salary "Monthly Salary" from employees
    where (salary between 5000 and 12000) and department_id in (20,50);

7.
    Select last_name, hire_date
    from employees
    where hire_date like '%94';

8.
    Select last_name, job_id from employees
    where manager_id is null;

9.
    Select last_name, salary, commission_pct from employees
    where commission_pct is not null
    order by salary, commission_pct;

10.
    Select last_name from employees
    where last_name like '__a%';

11.
    Select last_name from employees
    where last_name like '%a%' and last_name like '%e%';

12.
    Select last_name, job_id, salary
    from employees
    where (job_id='SA_REP' or job_id='ST_CLERK') and salary not in(2500,3500,7000);

13.
    Select last_name "Employee", salary "Monthly Salary", commission_pct from employees
    where commission_pct=.2;
