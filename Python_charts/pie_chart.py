import psycopg2 #psycopg2 für die Verbindung zu unsere PostgreSQL Datenbank
import matplotlib.pyplot as plt #matplotLib für das ploten von Graphen
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

try:
    connection = psycopg2.connect(  #Verbinden uns zu unserer Datenbank
        host="localhost",
        port="5432",
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )

    cursor = connection.cursor()

    

except psycopg2.Error as e:
    print(f"Fehler beim Verbinden zur PostgreSQL-Datenbank: {e}")


#SQL-Abfrage wird durchgeführt
#Aufteilung von Studierenden auf Städte
cursor.execute("SELECT SUM(h.\"Anzahl_Studierende\") AS Anzahl_Studierende, o.\"Ort_Name\"FROM public.\"Hochschulen\" AS h JOIN public.\"Orte\" AS o ON h.\"Ort\" = o.\"Ort_Name\" GROUP BY o.\"Ort_Name\" ORDER BY Anzahl_Studierende DESC LIMIT 20;")
rows1 = cursor.fetchall() #In rows werden die Ergebnisse aus unserer SQL-Abfrage gespeichert
    
# Verbindung wird geschlossen
if connection:
    cursor.close()
    connection.close()
    print("Verbindung zur PostgreSQL-Datenbank geschlossen.")

values1 = []
labels1 = []
for row in rows1:
    values1.append(row[0])  #Wir schreiben uns die Values von jedem Studi in Liste
    labels1.append(row[1]) #Wir schreiben uns Namen der Städte in Liste

# Pie-Chart erstellen
plt.figure(figsize=(30, 10))
plt.pie(values1, labels=labels1, autopct='%1.1f%%', startangle=140)
plt.title("Aufteilung von Studierenden auf Städte (TOP 20)")

# Diagramm anzeigen
plt.show()