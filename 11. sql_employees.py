import sqlite3


class Employee:
    def __init__(self, id, name, salary):
        self.id = id
        self.name = name
        self.salary = salary


class EmployeeDB:
    def __init__(self, db_name, table_name="EMPLOYEES"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.table_name = table_name

    def create(self, employee):
        self.cursor.execute(
            f"INSERT INTO {self.table_name} (ID,NAME,SALARY) VALUES (?, ?, ?)",
            (employee.id, employee.name, employee.salary)
        )
        self.conn.commit()

    def read(self, id):
        self.cursor.execute(f"SELECT * from {self.table_name} where ID=?", (id,))
        row = self.cursor.fetchone()
        if row is not None:
            return Employee(row[0], row[1], row[2])
        else:
            return None

    def read_all(self):
        return db.cursor.execute(f"SELECT * from {self.table_name}").fetchall()

    def update(self, employee):
        self.cursor.execute(
            f"UPDATE {self.table_name} set NAME = ?, SALARY = ? where ID = ?",
            (employee.name, employee.salary, employee.id)
        )
        self.conn.commit()

    def delete(self, id):
        self.cursor.execute(f"DELETE from {self.table_name} where ID = ?", (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    # создание таблицы
    conn = sqlite3.connect('company.db')
    # Создание таблицы "Сотрудники"
    conn.execute('''
    CREATE TABLE EMPLOYEES
    (ID INT PRIMARY KEY NOT NULL,
    NAME TEXT NOT NULL,
    SALARY REAL);
    ''')
    conn.close()

    # Пример использования
    db = EmployeeDB('company.db')
    db.create(Employee(1, 'Fillip Zsk', 500330))
    db.create(Employee(2, 'Evgeniy Abc', 50))
    db.create(Employee(3, 'Bob Qwer', 4330))

    employee = db.read(1)
    print(employee.name)

    employee.salary = 6000
    db.update(employee)

    print(db.read_all())

    db.close()
