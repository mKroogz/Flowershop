import sqlite3
from django.shortcuts import render
from bouquetapp.models import Bouquet
from .connection import Connection

def home(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                b.id,
                b.name,
                b.occasion
            FROM bouquetapp_bouquet AS b
            ORDER BY b.name
            """)

            all_bouquets = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                bouquet = Bouquet()
                bouquet.id = row['id']
                bouquet.name = row['name']
                bouquet.budget = row['occasion']

                all_bouquets.append(bouquet)

    template = 'home.html'
    context = {
        'bouquets': all_bouquets
    }

    return render(request, template, context)
