import psycopg2 #psycopg2 für die Verbindung zu unsere PostgreSQL Datenbank
import matplotlib.pyplot as plt #matplotLib für das ploten von Graphen
import geopandas as gpd  #geopandas für das ploten von Karten
import pandas as pd #Für das erstellen von Dataframes
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
cursor.execute("SELECT b.\"Name\", COUNT(h.\"Hochschulname\") AS Anzahl_Unis FROM public.\"Hochschulen\" AS h JOIN public.\"Bundeslaender\" AS b ON h.\"Bundesland\" = b.\"ID_Bundesland\" WHERE h.\"Gruendungsjahr\" >= 2004 GROUP BY b.\"Name\" ORDER BY Anzahl_Unis DESC;")
rows = cursor.fetchall() #In rows werden die Ergebnisse aus unserer SQL-Abfrage gespeichert
    
bundeslaender = [] #Ergebnisse der Queries in Listen
Anzahl_Unis = []
for row in rows:
    bundeslaender.append(row[0])
    Anzahl_Unis.append(row[1])

bundes_l = gpd.read_file("germany-states.geojson")  #Laden der Datei mit den GeoDaten

daten = {
    'Bundeslandname': bundeslaender,
    'Anzahl_Unis': Anzahl_Unis
}
frame = pd.DataFrame(daten)  #umwandeln in Pandas frame

bundes_l = bundes_l.rename(columns={"NAME_1": "Bundeslandname"}) # Die Spalte in bundes_l bennenen wir um damit es die selbe ist wie die aus unserem Dataframe

bundes_l = bundes_l.set_index("Bundeslandname")
frame = frame.set_index("Bundeslandname")

# Verbinde die beiden DataFrames
gdf = bundes_l.join(frame, how="left")

fig, ax = plt.subplots(1, 1, figsize=(10, 15))
gdf.plot(column='Anzahl_Unis', ax=ax, legend=True,
    legend_kwds={'label': "Anzahl neuer Hochschulen in den letzten 20 Jahren", #Legende
                    'orientation': "vertical"},
    cmap='OrRd', missing_kwds={"color": "lightgrey"})  

plt.title("Anzahl neuer Hochschulen in den letzten 20 Jahren (pro Bundesland)")
ax.set_axis_off() #Achsen entfernen

plt.show()

