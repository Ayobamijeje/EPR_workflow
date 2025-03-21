from sqlalchemy import create_engine, text

def database_enginee():
	db_url = 'sqlite:///EPR_proj.db'
	engine = create_engine(db_url)
	return engine 

engine = database_enginee()

def get_tables()  -> list[str]:
    """Retrieve the names of all tables in the database."""
    # Include print logging statements so you can see when functions are being called.
    print(' - DB CALL: list_tables')

    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        return [row[0] for row in result]



def table_discription(table_name: str) -> list[tuple[str, str]]:
    """Look up the table schema.

    Returns:
        List of columns, where each entry is a tuple of (column, type).
    """

    print('- DB CALL: table schema')
    
    with engine.connect() as conn:
        schema = conn.execute(text(f"PRAGMA table_info({table_name});"))
        
    return [(col[1], col[2]) for col in schema]





def execute_query(sql_statement: str) -> list[list[str]]:
    """Execute a SELECT statement, returning the results."""
    print(' - DB CALL: execute_query')

    with engine.connect() as conn:
        query = conn.execute(text(sql_statement))
        return query.fetchall()





