import psycopg2
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# Laden der Umgebungsvariablen
load_dotenv()

# Datenbank-Konfiguration
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

# Verbindung zur Datenbank herstellen
try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )
    cursor = connection.cursor()
except psycopg2.Error as e:
    print(f"Fehler beim Verbinden zur PostgreSQL-Datenbank: {e}")

# SQL-Abfrage
query = """
SELECT 
    b."Name",
    SUM(CASE 
        WHEN h_t."Hochschultyp" IN ('Fachhochschulen / HAW', 'Künstlerische Hochschulen', 'Verwaltungshochschule') 
        THEN h."Anzahl_Studierende" 
        ELSE 0 
    END) AS sum_FachHoch,
    SUM(CASE 
        WHEN h_t."Hochschultyp" = 'Universitäten' 
        THEN h."Anzahl_Studierende" 
        ELSE 0 
    END) AS sum_UNI
FROM public."Hochschulen" AS h
JOIN public."Hochschultyp_und_Traegerschaft" AS h_t ON h."ID_Typ" = h_t."ID_Typ"
JOIN public."Bundeslaender" AS b ON h."Bundesland" = b."ID_Bundesland"
GROUP BY b."Name"
ORDER BY b."Name";
"""

cursor.execute(query)
rows = cursor.fetchall()

# Verbindung schließen
if connection:
    cursor.close()
    connection.close()
    print("Verbindung zur PostgreSQL-Datenbank geschlossen.")

# Daten in Listen konvertieren
bundeslaender = [row[0] for row in rows]
fachhochschulen_studierende = [row[1] if row[1] is not None else 0 for row in rows]
universitaeten_studierende = [row[2] if row[2] is not None else 0 for row in rows]

# Plot erstellen
fig, ax = plt.subplots(figsize=(15, 10))
bar_width = 0.35  # Breite der Balken

# Positionen für die Balken
index = range(len(bundeslaender))

# Balken für Fachhochschulen und Universitäten
rects1 = ax.bar(index, fachhochschulen_studierende, bar_width, label='Fachhochschulen/HAWs')
rects2 = ax.bar([i + bar_width for i in index], universitaeten_studierende, bar_width, label='Universitäten')

# Titel und Achsenbeschriftungen
ax.set_xlabel('Bundesland')
ax.set_ylabel('Anzahl Studierende')
ax.set_title('Anzahl Studierende an Fachhochschulen vs Universitäten pro Bundesland')
ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(bundeslaender, rotation=45, ha='right')

# Legende und Layout
ax.legend()
fig.tight_layout()

# Diagramm anzeigen
plt.show()

