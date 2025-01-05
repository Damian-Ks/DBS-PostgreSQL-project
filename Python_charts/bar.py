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
        database= DATABASE,
        user= USER,
        password= PASSWORD
    )

    cursor = connection.cursor()

    

except psycopg2.Error as e:
    print(f"Fehler beim Verbinden zur PostgreSQL-Datenbank: {e}")


#SQL-Abfrage wird an DB gesendet
#Aufteilung von Studierenden auf Städte
cursor.execute("SELECT b.\"Name\", COUNT(h.\"Hochschulname\") AS Anzahl_Unis FROM public.\"Hochschulen\" AS h JOIN public.\"Hochschultyp_und_Traegerschaft\" AS h_t ON h.\"ID_Typ\" = h_t.\"ID_Typ\" JOIN public.\"Bundeslaender\" AS b ON h.\"Bundesland\" = b.\"ID_Bundesland\" WHERE h_t.\"Traegerschaft\" = 'privat, staatlich anerkannt' GROUP BY b.\"Name\" ORDER BY Anzahl_Unis DESC;")
rows = cursor.fetchall() #In rows werden die Ergebnisse aus unserer SQL-Abfrage gespeichert
    
cursor.execute("SELECT b.\"Name\", COUNT(h.\"Hochschulname\") AS Anzahl_Unis FROM public.\"Hochschulen\" AS h JOIN public.\"Hochschultyp_und_Traegerschaft\" AS h_t ON h.\"ID_Typ\" = h_t.\"ID_Typ\" JOIN public.\"Bundeslaender\" AS b ON h.\"Bundesland\" = b.\"ID_Bundesland\" WHERE h_t.\"Traegerschaft\" = 'öffentlich-rechtlich' GROUP BY b.\"Name\" ORDER BY Anzahl_Unis DESC;")
rows2 = cursor.fetchall()

for row in rows2:
    print(row)
    
# Verbindung wird geschlossen
if connection:
    cursor.close()
    connection.close()
    print("Verbindung zur PostgreSQL-Datenbank geschlossen.")

bundeslaender1 = []
bundeslaender2 = []
Anzahl_privat = []
Anzahl_oeffentlich = []
for row in rows:
    bundeslaender1.append(row[0][:4])
    Anzahl_privat.append(row[1])
for row in rows2:
    Anzahl_oeffentlich.append(row[1])
    bundeslaender2.append(row[0][:4])

fig, axes = plt.subplots(1, 2, figsize=(30, 10)) #Zwei Graphen in eine Zeile

axes[0].bar(bundeslaender1, Anzahl_privat, width=0.4, label='privat', color='blue')
axes[1].bar(bundeslaender2, Anzahl_oeffentlich, width=0.4, label='öffentlich', color='grey')
axes[0].set_title("Anzahl der privaten Hochschulen pro Bundesland")
axes[1].set_title("Anzahl der öffentlichen Hochschulen pro Bundesland")
plt.xlabel('Bundesländer')
plt.ylabel('Anzahl der Hochschulen')

plt.show()