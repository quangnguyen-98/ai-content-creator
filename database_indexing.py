import sqlite3
from sqlite3 import Error
import time

class Database:
    def __init__(self, db_file):
        """ create a database connection to a SQLite database """
        self.conn = self.create_connection(db_file)

    def create_connection(self, db_file):
        """ Create a database connection """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    def execute_query(self, query):
        """ Execute a single query """
        try:
            c = self.conn.cursor()
            c.execute(query)
            self.conn.commit()
        except Error as e:
            print(e)

    def execute_read_query(self, query):
        """ Execute a single read query """
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()

class Index:
    def __init__(self, table_name, index_name):
        self.table_name = table_name
        self.index_name = index_name

    def create_index(self, db):
        """ Create an index on the specified table """
        query = f"CREATE INDEX {self.index_name} ON {self.table_name} (id)"
        db.execute_query(query)

    def drop_index(self, db):
        """ Drop the specified index """
        query = f"DROP INDEX {self.index_name}"
        db.execute_query(query)

class Employee:
    def __init__(self, db):
        self.db = db
        self.create_employee_table()

    def create_employee_table(self):
        """ Create employee table """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            salary REAL NOT NULL
        );
        """
        self.db.execute_query(create_table_query)

    def add_employee(self, name, salary):
        """ Add a new employee to the table """
        query = f"INSERT INTO employees (name, salary) VALUES ('{name}', {salary})"
        self.db.execute_query(query)

    def fetch_all_employees(self):
        """ Fetch all employees """
        query = "SELECT * FROM employees"
        return self.db.execute_read_query(query)

def measure_execution_time(func):
    """ Measure the execution time of a function """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'Execution time: {end_time - start_time} seconds')
        return result
    return wrapper

@measure_execution_time
def create_and_index_database():
    """ Create database, add employees and create index """
    database = Database("employee_database.db")
    employee_table = Employee(database)

    # Adding employees
    for i in range(1, 1001):
        employee_table.add_employee(f'Employee-{i}', 50000 + i)

    # Creating an index
    index = Index("employees", "salary_index")
    index.create_index(database)
    print("Index created")

@measure_execution_time
def fetch_employees(database):
    """ Fetch all employees from the database """
    employee_table = Employee(database)
    employees = employee_table.fetch_all_employees()
    for emp in employees:
        print(emp)

def main():
    """ Main function to execute the script """
    database = Database("employee_database.db")
    create_and_index_database()
    fetch_employees(database)

if __name__ == "__main__":
    main()