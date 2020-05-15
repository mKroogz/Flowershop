import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from bouquetapp.models import Bouquet
from ..connection import Connection


# @login_required
def bouquet_form(request):
    if request.method == 'GET':
        template = 'bouquets/form.html'

        return render(request, template)
    
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO bouquetapp_bouquet
            (
                name, occasion
            )
            VALUES (?, ?)
            """,
            (form_data['name'], form_data['occasion']))

        return redirect(reverse('bouquetapp:home'))