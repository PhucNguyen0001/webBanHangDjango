from django.shortcuts import render
from django.http import HttpResponse
from .models import Bearings
from django.views import View
# Create your views here.


def index(request):
    return render(request, 'find_bearing.html')


class MyFormView(View):
    def get(self, request):
        d_bore = request.GET.get('d bore', None)
        d_outside = request.GET.get('D outside', None)
        b = request.GET.get('B', None)

        filtered_records = Bearings.filter_by_my_field(d_bore, d_outside, b)

        return render(request, 'test_testdb_dir/result.html', {'result': filtered_records})
