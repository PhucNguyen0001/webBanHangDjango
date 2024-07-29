from django.shortcuts import render, redirect, get_object_or_404
from testdb.models import Bearings
from django.views import View
from . import models
import base64
from pathlib import Path

# Create your views here.
def custom_404(request, exception):
    return render(request, '404.html', status=404)


def index(request):
    return render(request, 'index.html',
                  {
                      'tongtien': models.DonHang.tongTien(),
                      'tongtienthangnay': models.DonHang.tongTienThangNay(),
                      'demdonHT': models.DonHang.demDonHT(),
                      'demdonChuaHT': models.DonHang.demDonChuaHT(),
                      'tongTienTheoThang': models.DonHang.tongTienTheoThang(),
                      'tongTienTheoLoai': models.tongTienTheoLoai()
                  })

class SearchView(View):
    def get(self, request):
        d_bore = request.GET.get('d bore', None)
        d_outside = request.GET.get('D outside', None)
        b = request.GET.get('B', None)

        result = Bearings.filter_by_my_field(d_bore, d_outside, b)

        return render(request, "search.html", {'result': result})


def qlkh(request):
    return render(request, "qlkh.html", {'users': models.User.get_user()})


class SuaTTKH(View):
    def get(self, request, id):
        return render(request, "suattkh.html", {'kh': models.User.get_by_userid(id)})

    def post(self, request, id):
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        diachi = request.POST.get('diachi')
        models.User.change_inf(id, username, mobile, diachi)
        return qlkh(request)
        # except Exception as e:
        #     return render(request, '404.html')


def qlsp(request):
    return render(request, "qlsp.html", {'products': models.get_sp()})


def xemttsp(request, id):
    return render(request, "xemttsp.html", {'product': models.get_sp_by_id(id)})


class SuaTTSP(View):
    def get(self, request, id):
        return render(request, "suattsp.html",
                      {
                            'list_loai': models.SanPham.get_loai(),
                            'product': models.get_sp_by_id(id)
                            }
                      )

    def post(self, request, id):
        tensp = request.POST.get('tensp')
        giasp = int(request.POST.get('giasp'))
        mota = request.POST.get('mota')
        loai = int(request.POST.get('loai'))
        hinhanh_file = request.FILES.get('hinhanh')
        if hinhanh_file:
            hinhanh_data = hinhanh_file.read()
            hinhanh_type = Path(hinhanh_file.name).suffix
            base64_encoded_data = base64.b64encode(hinhanh_data)
            hinhanh_base64 = f"data:image/{hinhanh_type[1:]};base64," + base64_encoded_data.decode('utf-8')
        else:
            hinhanh_base64 = None
        models.SanPhamMoi.sua_ttsp(id, tensp, giasp, mota, loai, hinhanh_base64)
        return qlsp(request)


def qldh(request):
    return render(request, "qldh.html", {'list_dh': models.DonHang.select_dh()})


def thao_tac_dh(request, id, action):
    if request.method == 'POST':
        record = models.DonHang.objects.get(id=id)
        if action == 1:
            record.trangthai = record.trangthai + 1
        else:
            record.trangthai = 4
        record.save()
    return qldh(request)