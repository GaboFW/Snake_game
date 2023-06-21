import sqlite3


conexion=sqlite3.connect("Puntajes.db")
try:
    conexion.execute("""create table Ranking (
                            jugador text,
                            inicio datetime,
                            final datetime,
                            puntos integer
                        )""")
    print("se creo la tabla Ranking")                        
except sqlite3.OperationalError:
    print("La tabla Ranking ya existe")                    
conexion.close()