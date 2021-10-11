"""Скрипт для заполнения пустой таблицы в базе SQLlite исходными данными формата json.
   
   В исходных данных количество столбцов должно соответствовать количеству в таблице БД.
   Скрипт не является универсальным. Записываемые столбцы перечисляются в переменной ingredient
"""


import json
import sqlite3


DB_FILE = 'db.sqlite3'
FIXTURES = 'ingredients.json'

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
with open(FIXTURES, 'r', encoding='utf-8') as ingredients:
    obj = json.load(ingredients)

for i in range(len(obj)):
    ingredient = [(i, obj[i]['name'], obj[i]['measurement_unit'])]
    try:
        cursor.executemany("""INSERT INTO recipes_ingredients
                  VALUES (?,?,?)""", ingredient)
    except Exception:
        print(ingredient)
        continue
conn.commit()

