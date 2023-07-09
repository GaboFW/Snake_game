import sqlite3

conexion = sqlite3.connect("Puntacion.db")

try:
    conexion.execute("""create table Ranking (
                            jugador text,
                            puntos integer
                        )""")
    print("Se creo la tabla Ranking")          
except sqlite3.OperationalError:
    print("La tabla Ranking ya existe")
