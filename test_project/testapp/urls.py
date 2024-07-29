from django.urls import path
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.SearchView.as_view(), name='search'),
    path('qlkh', views.qlkh, name='qlkh'),
    path('suattkh/<int:id>', views.SuaTTKH.as_view(), name='suaTTKH'),
    path('qlsp', views.qlsp, name='qlsp'),
    path('xemttsp/<int:id>', views.xemttsp, name='xemTTSP'),
    path('suattsp/<int:id>', views.SuaTTSP.as_view(), name='suaTTSP'),
    path('qldh', views.qldh, name='qldh'),
    path('thaotacdh/<int:id>/<int:action>', views.thao_tac_dh, name='thaotacdh')
]