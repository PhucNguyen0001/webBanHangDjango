from django.db import models, connection
from django.db.models import Sum, OuterRef, Subquery
from django.db.models.functions import TruncMonth
import datetime
import calendar
import json


# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.TextField()
    password = models.TextField(db_column='pass')
    username = models.TextField()
    mobile = models.TextField()
    uid = models.TextField()
    diachi = models.TextField()

    class Meta:
        db_table = 'user'

    @classmethod
    def get_user(cls):
        return cls.objects.all()

    @classmethod
    def get_by_userid(cls, id):
        return cls.objects.get(id=id)

    @classmethod
    def change_inf(cls, id, username, mobile, diachi):
        record = cls.objects.get(id=id)
        record.username = username
        record.mobile = mobile
        record.diachi = diachi
        record.save()


class SanPham(models.Model):
    id = models.IntegerField(primary_key=True)
    tensanpham = models.TextField()
    hinhanh = models.TextField()

    class Meta:
        db_table = 'sanpham'

    @classmethod
    def get_loai(cls):
        return cls.objects.all()


class DonHang(models.Model):
    id = models.IntegerField(primary_key=True)
    iduser = models.ForeignKey(User, to_field='id', on_delete=models.DO_NOTHING, db_column='iduser')
    diachi = models.TextField()
    sodienthoai = models.TextField()
    email = models.TextField()
    soluong = models.IntegerField()
    tongtien = models.IntegerField()
    trangthai = models.IntegerField()
    ngaydathang = models.DateField()

    class Meta:
        db_table = 'donhang'

    @classmethod
    def select_dh(cls):
        return cls.objects.select_related('iduser').all()

    @classmethod
    def tongTien(cls):
        return cls.objects.aggregate(Sum('tongtien'))['tongtien__sum']

    @classmethod
    def tongTienThangNay(cls):
        year, month = datetime.date.today().year, datetime.date.today().month
        total_amount = (cls.objects.filter(ngaydathang__year=year, ngaydathang__month=month)
        .aggregate(Sum('tongtien'))['tongtien__sum'])
        return total_amount if total_amount else 0

    @classmethod
    def demDonHT(cls):
        return cls.objects.filter(trangthai=3).count()

    @classmethod
    def demDonChuaHT(cls):
        return cls.objects.exclude(trangthai=3).count()

    @classmethod
    def tongTienTheoThang(cls):
        year = datetime.date.today().year
        year_filter = cls.objects.filter(ngaydathang__year=year)
        result = (year_filter.annotate(month=TruncMonth('ngaydathang')).values('month')
                  .annotate(total_amount=Sum('tongtien')))
        # return [record['month'] for record in result]
        months = []
        total_amounts = []

        # Duyệt qua kết quả và thêm vào các mảng
        for entry in result:
            month_name = calendar.month_name[entry['month'].month]
            months.append(month_name)
            total_amounts.append(entry['total_amount'])

        # In kết quả
        return {
            'month': months,
            'total_amounts': total_amounts
        }


class SanPhamMoi(models.Model):
    id = models.IntegerField(primary_key=True)
    tensp = models.TextField()
    giasp = models.IntegerField()
    hinhanh = models.TextField()
    mota = models.TextField()
    loai = models.ForeignKey(SanPham, to_field='id', db_column='loai', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'sanphammoi'

    @classmethod
    def sua_ttsp(cls, id, tensp, giasp, mota, loai, hinhanh):
        record = cls.objects.get(id=id)
        record.tensp = tensp
        record.giasp = giasp
        record.mota = mota
        record.loai = SanPham.objects.get(id=loai)
        if hinhanh:
            record.hinhanh = hinhanh
        record.save()


class ChiTietDonHang(models.Model):
    iddonhang = models.ForeignKey(DonHang, db_column='iddonhang', to_field='id', on_delete=models.DO_NOTHING)
    idsp = models.ForeignKey(SanPhamMoi, db_column='idsp', to_field='id', on_delete=models.DO_NOTHING)
    soluong = models.IntegerField()
    gia = models.IntegerField()

    class Meta:
        db_table = 'chitietdonhang'
        constraints = [
            models.UniqueConstraint(fields=['iddonhang', 'idsp'], name='unique_field1_field2')
        ]


def tongTienTheoLoai():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT tensanpham, sum(soluong * gia) 
                          from chitietdonhang join sanphammoi on chitietdonhang.idsp = sanphammoi.id 
                          join sanpham on sanphammoi.loai = sanpham.id 
                          group by tensanpham
                        """)
        rows = cursor.fetchall()
    type = []
    total_amounts = []
    for row in rows:
        type.append(row[0])
        total_amounts.append(row[1])
    return {
        'type': type,
        'total_amounts': total_amounts
    }


def get_sp():
    results = SanPhamMoi.objects.select_related('loai').all()
    return results


def get_sp_by_id(id):
    results = SanPhamMoi.objects.select_related('loai').get(id=id)
    return results


