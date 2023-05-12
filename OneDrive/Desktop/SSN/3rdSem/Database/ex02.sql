REM ----------
REM Q1. Display first name, job id and salary of all the employees.

SELECT first_name, job_id, salary 
FROM EMPLOYEES

REM Q2.  Display the id, name(first & last), salary and annual salary of all the employees.
REM Sort the employees by first name. Label the columns as shown below:
REM (EMPLOYEE_ID, FULL NAME, MONTHLY SAL, ANNUAL SALARY)

SELECT employee_id AS EMPLOYEE_ID, first_name AS FULL NAME, last_name, salary AS MONTHLY SAL, salary*12 AS ANNUAL SAL
FROM employees
ORDER BY first_name

REM ------------
REM Q3.  List the different jobs in which the employees are working for.

SELECT DISTINCT job_id FROM employees;

REM -------------
REM Q4. Display the id, first name, job id, salary and commission of employees who are earning commissions.

SELECT employee_id, first_name, job_id, commission_pct
FROM employees 
WHERE commission_pct IS NOT NULL;

REM -------------
REM Q5.  Display the details (id, first name, job id, salary and dept id) of employees who are MANAGERS.

SELECT employee_id, first_name, job_id, salary, department_id
FROM EMPLOYEES 
WHERE

REM -----------
REM Q6. Display the details of employees other than sales representatives (id, first name,
REM hire date, job id, salary and dept id) who are hired after ‘01-May-1999’ or whose
REM salary is at least 10000

SELECT employee_id, first_name, hire_date, job_id, salary, department_id
FROM EMPLOYEES
WHERE hire_date > '01-May-1999' OR salary>= 10000;

REM ------------
REM Q7. Display the employee details (first name, salary, hire date and dept id) whose
REM salary falls in the range of 5000 to 15000 and his/her name begins with any of
REM characters (A,J,K,S). Sort the output by first name.

SELECT first_name, salary, hire_date, department_id
FROM EMPLOYEES
WHERE SALARY BETWEEN 5000