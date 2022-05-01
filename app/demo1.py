from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql import text
# echo=True will write sql statements to the console (like: verbose)
engine = create_engine('postgresql://dev:ax2@db:5432/app', echo=True) # the Engine is most efficient when created just once at the module level of an application, not per-object or per-function call.
conn = engine.connect()

meta = MetaData()

# Using sqlalchemy.Table rather than Class Student(Base):
students = Table(
    'students', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('lastname', String),
)

addresses = Table(
    'addresses', meta,
    Column('id', Integer, primary_key=True),
    Column('st_id', Integer),
    Column('postal_add', String),
    Column('email_add', String)
)


if __name__ == '__main__':
    # Clean up before we start: (and using text() to create basic sql statements)
    sql = text('DROP TABLE IF EXISTS students;')
    sql2 = text('DROP TABLE IF EXISTS addresses;')
    result = engine.execute(sql)
    result = engine.execute(sql2)
    # Create all tables
    meta.create_all(engine)
    
    # insert
    ins = students.insert().values(name='Ravi', lastname='Kapoor')
    result = conn.execute(ins)
    # in bulk:
    conn.execute(students.insert(), [
        {'name': 'Rajiv', 'lastname': 'Khanna'},
        {'name': 'Komal', 'lastname': 'Bhandari'},
        {'name': 'Abdul', 'lastname': 'Sattar'},
        {'name': 'Priya', 'lastname': 'Rajhans'},
    ])
    # select
    s = students.select()
    result = conn.execute(s)

    for row in result:
        print(row)

    # select with filter
    s = students.select().where(students.c.id > 6)
    result = conn.execute(s)
    for row in result:
        print(row)

    # select with parameters
    s = text("select students.name, students.lastname from students where students.name between :x and :y")
    # fetchall turns the iterator into a list of rows
    result = conn.execute(s, x='A', y='L').fetchall()
    print(result)

    # update
    stmt = students.update().where(students.c.lastname ==
                                   'Khanna').values(lastname='Kapoor')
    conn.execute(stmt)
    s = students.select()
    result = conn.execute(s).fetchall()
    print('Khanna changed to Kapoor', result)

    # delete
    stmt = students.delete().where(students.c.lastname == 'Kapoor')
    conn.execute(stmt)
    s = students.select()
    result = conn.execute(s).fetchall()
    print(result)

    # multiple tables
    print('MULTIPLE TABLES')
    from sqlalchemy.sql import select
    conn.execute(addresses.insert(), [
        {'st_id': 1, 'postal_add': 'Shivajinagar Pune',
            'email_add': 'ravi@gmail.com'},
        {'st_id': 1, 'postal_add': 'ChurchGate Mumbai',
            'email_add': 'kapoor@gmail.com'},
        {'st_id': 3, 'postal_add': 'Jubilee Hills Hyderabad',
            'email_add': 'komal@gmail.com'},
        {'st_id': 5, 'postal_add': 'MG Road Bangaluru', 'email_add': 'as@yahoo.com'},
        {'st_id': 2, 'postal_add': 'Cannought Place new Delhi',
            'email_add': 'admin@khanna.com'},
    ])
    print('SELECTING MULTI')
    s = select([students, addresses]).where(students.c.id == addresses.c.st_id)
    result = conn.execute(s)
    print('RESULT::::::', result)
    for row in result:
        print(row)

    # Create table sql: 
    engine.execute("""
CREATE TABLE IF NOT EXISTS my_new_table (
    m_id BIGSERIAL PRIMARY KEY,
    name text
    )
""")
    # cli: SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_name = 'my_new_table';
    
    # clean up (Not necessary now, that this main method starts by cleaning up tables)
    # conn.execute(students.delete())
    # conn.execute(addresses.delete())
