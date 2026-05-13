import sqlite3

conn = sqlite3.connect('rods.db')

cursor = conn.cursor()

# Create Table
cursor.execute('''
CREATE TABLE rods (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    part_number TEXT,
    drawing_number TEXT,
    model_name TEXT,
    total_length TEXT,
    ref_length TEXT,
    plating_thickness TEXT,
    thread_type TEXT,
    plant TEXT,
    supplier TEXT,
    remarks TEXT
)
''')

# Insert Data
cursor.executemany('''

INSERT INTO rods (

part_number,
drawing_number,
model_name,
total_length,
ref_length,
plating_thickness,
thread_type,
plant,
supplier,
remarks

)

VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

''', [

('34040205', '12-8-2019-00', 'KOLA', '154.9 REF Ø', '117.3 ± 0.40', '15 ±04', '7 mm Plain', 'GIL HSR + NSK', 'KALIKA ENGG.', 'Nil'),

('34040315-19', '02.08.2013-00', 'N100', '172.00 REF', '130.5 ± 0.40', '15 ±04', 'M7 x1.0 -6g', 'GIL HSR', 'KALIKA ENGG.', 'Nil'),

('34040395-5', '1-7-16-03', 'KWPJ Honda', '154 REF', '115.9 ± 0.40', '15 ±04', '7 mm Plain', 'GIL NSK', 'ESPEE ENGG', 'Ring Mark M10 Face')

])

conn.commit()

conn.close()

print("Database Created Successfully")