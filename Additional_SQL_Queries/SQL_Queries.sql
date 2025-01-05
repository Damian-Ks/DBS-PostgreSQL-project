--Aufteilung von Studierenden auf Städte

SELECT SUM(h."Anzahl_Studierende") AS Anzahl_Studierende, o."Ort_Name"
FROM public."Hochschulen" AS h
JOIN public."Orte" AS o ON h."Ort" = o."Ort_Name" 
GROUP BY o."Ort_Name"
ORDER BY Anzahl_Studierende DESC
LIMIT 30;


-- Vergleich der Anzahl von öffentlichen Hochschulen und privaten Hochschulen

SELECT b."Name", COUNT(h."Hochschulname") AS Anzahl_Unis
FROM public."Hochschulen" AS h
JOIN public."Hochschultyp_und_Traegerschaft" AS h_t ON h."ID_Typ" = h_t."ID_Typ"
JOIN public."Bundeslaender" AS b ON h."Bundesland" = b."ID_Bundesland"
WHERE h_t."Traegerschaft" = 'privat, staatlich anerkannt'
GROUP BY b."Name"
ORDER BY Anzahl_Unis DESC;


-- Wo sind in den letzten 20 Jahren am meisten Hochschulen entstanden

SELECT b."Name", COUNT(h."Hochschulname") AS Anzahl_Unis
FROM public."Hochschulen" AS h
JOIN public."Bundeslaender" AS b ON h."Bundesland" = b."ID_Bundesland"
WHERE h."Gruendungsjahr" >= 2004
GROUP BY b."Name"
ORDER BY Anzahl_Unis DESC;


-- Durchschnittliches Gründungsjahr von Hochschulen pro Bundesland

SELECT b."Name", AVG(h."Gruendungsjahr") 
FROM public."Hochschulen" AS h
JOIN public."Bundeslaender" AS b ON h."Bundesland" = b."ID_Bundesland"
GROUP BY b."Name";


-- entspannte Orte zum promovieren, in Landkreisen, Städten mit weniger als 100000 Einwohnern

SELECT o."Ort_Name", h."Hochschulname"
FROM public."Orte" AS o
JOIN public."Hochschulen" AS h ON h."Ort" = o."Ort_Name"
WHERE h."Promotionsrecht" = True AND o."Bevoelkerungsstand_insgesamt" < 100000;


-- Anzahl Studis an Fachhochschulen vs Anzahl an Studis an Universitäten

WITH FachHoch_studierende AS (
    SELECT h."Bundesland", SUM(h."Anzahl_Studierende") AS Anzahl
    FROM public."Hochschulen"AS h
    JOIN public."Hochschultyp_und_Traegerschaft" AS h_t ON h."ID_Typ" = h_t."ID_Typ"
    WHERE h_t."Hochschultyp" IN('Fachhochschulen / HAW', 'Künstlerische Hochschulen', 'Verwaltungshochschule')
    GROUP BY h."Bundesland"
),
UNI_studierende AS (
    SELECT h."Bundesland", SUM(h."Anzahl_Studierende") AS Anzahl
    FROM public."Hochschulen" AS h
    JOIN public."Hochschultyp_und_Traegerschaft" AS h_t ON h."ID_Typ" = h_t."ID_Typ"
    WHERE h_t."Hochschultyp" = 'Universitäten'
    GROUP BY h."Bundesland"

)
SELECT b."Name", FachHoch_studierende.Anzahl AS sum_FachHoch, UNI_studierende.Anzahl AS sum_UNI
FROM FachHoch_studierende
FULL OUTER JOIN UNI_studierende ON FachHoch_studierende."Bundesland" = UNI_studierende."Bundesland"
JOIN public."Bundeslaender" AS b ON FachHoch_studierende."Bundesland" = b."ID_Bundesland";
