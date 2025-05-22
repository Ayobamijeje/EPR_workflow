from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



from sqlalchemy import create_engine, text

# Create engine and connect
engine = create_engine('sqlite:///EPR_proj.db', echo=True) 
#conn = engine.connect()

with engine.connect() as conn:
	conn.execute(text('''
	    CREATE TABLE IF NOT EXISTS history (
	        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
	        name VARCHAR(80),
	        history VARCHAR(300)
	    );
	'''))

	conn.commit()



with engine.connect() as conn:

	conn.execute(text('''
	    CREATE TABLE IF NOT EXISTS vitals (
	        vitals_id INTEGER PRIMARY KEY AUTOINCREMENT,
	        Blood_pressure VARCHAR,
	        Heart_rate INTEGER,
	        Respiratory_rate INTEGER,
	        Oxygen_saturation INTEGER,
	        Temperature INTEGER,
	        patient_id INTEGER NOT NULL,

	        FOREIGN KEY (patient_id) REFERENCES history (patient_id)

	    );
	'''))


	conn.commit()
	print("Table created successfully!")


#with engine.connect() as conn:
#    conn.execute(text('''
#        INSERT INTO history (name, history) VALUES
#        ('John Jones', 'presented with cough, chest pain and fever'),
#        ('Harry Smith', 'Known COPD, presented with fever, breathless'),
#        ('Mary Colins', 'Known Asthma, presented with cough and breathless'),
#        ('Angel Apple', 'in ED, with sudden chest pain and difficulty breathing');
#    '''))
#    conn.commit()  # Save changes

# Insert data into vitals table
#with engine.connect() as conn:
#	conn.execute(text('''
#		INSERT INTO vitals (patient_id, Blood_pressure, Heart_rate, Respiratory_rate, Oxygen_saturation, Temperature) VALUES
#        (1, '120/80', 75, 16, 98, 37),
#        (2, '100/50', 100, 22, 85, 38),
#        (3, '90/50', 105, 24, 90, 38),
#        (4, '100/60', 90, 22, 93, 36);

 #   '''))
#	conn.commit()  

#print("Data inserted successfully!")


