from django.shortcuts import render
from django.http import HttpResponse
from .data import *


def main(request):
    return HttpResponse("""
<h1>Barbershop</h1>
<p>We are the best barbershop in the world!</p>""")


def master_detail(request, master_id):
    try:
        master = [m for m in masters if m['id'] ==  master_id][0]
    except IndexError:
        return HttpResponse('Мастер не найден')
    return HttpResponse(f'<h1>{master["name"]}</h1>')

def thanks(request):
    masters_count = len(masters)
    context = {
        'masters_count': masters_count
    }
    return render(request, 'thanks.html', context)
