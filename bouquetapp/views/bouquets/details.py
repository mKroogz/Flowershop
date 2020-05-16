import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from bouquetapp.models import Bouquet
from ..connection import Connection

def get_bouquet(bouquet_id):
    with sqlite3.connect(Connection.db_path) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                b.id,
                b.name,
                b.occasion,
                f.name,
                bf.quantity,
                bf.id
            FROM bouquetapp_bouquetflower AS bf 
            JOIN bouquetapp_bouquet AS b ON bf.bouquet_id = b.id
            JOIN bouquetapp_flower AS f ON bf.flower_id = f.id
            WHERE bf.bouquet_id = ?
        """, (bouquet_id,))

        all_bouquets = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            bouquet = Bouquet()
            bouquet.id = row[0]
            bouquet.name = row[1]
            bouquet.occasion = row[2]
            bouquet.flower_name = row[3]
            bouquet.quantity = row[4]
            bouquet.flower = row[5]

            all_bouquets.append(bouquet)

        return all_bouquets

def remove_flower(flower):
    with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            DELETE FROM bouquetapp_bouquetflower
            WHERE id = ?
            """, (flower,))



def bouquet_details(request, bouquet_id):
    if request.method == 'GET':
        bouquets = get_bouquet(bouquet_id)
        info = ""
        if bouquets:
            info = bouquets[0]

        template = 'bouquets/detail.html'
        context = {
            'bouquets': bouquets,
            'info': info,
        }

        return render(request, template, context)
    
    elif request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
            and "flower" in form_data
        ):
            remove_flower(form_data["flower"])

        return redirect(reverse('bouquetapp:home'))