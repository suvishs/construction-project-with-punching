from django.urls import path
from constructionapp import views

urlpatterns = [
    path('', views.login, name="login"),
    path('login', views.login, name="login"),
    path('index',views.index, name="index"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"),
    
    path('sortvisiting', views.sortvisiting, name="sortvisiting"),
    path('delete_visiting/<int:id>', views.delete_visiting, name="delete_visiting"),
    path('update_visiting/<int:id>', views.update_visiting, name="update_visiting"),
    path('visiting_report', views.visiting_report, name="visiting_report"),
    path('punch', views.punch, name="punch"),
    path('mark_attendance', views.mark_attendance, name="mark_attendance"),
    path('overtime', views.overtime, name="overtime"),
    path('viewallatendancereport', views.viewallatendancereport, name="viewallatendancereport"),
    path('sortattandance', views.sortattandance, name="sortattandance"),
    path('sortattandanceovertime', views.sortattandanceovertime, name="sortattandanceovertime"),
    path('Applicationforleave', views.Applicationforleave, name="Applicationforleave"),
    path('Viewleaveaplications', views.Viewleaveaplications, name="Viewleaveaplications"),
    path('ApproveViewleaveaplications', views.ApproveViewleaveaplications, name="ApproveViewleaveaplications"),
    path('ApproveViewleaveaplication/<int:id>', views.ApproveViewleaveaplication, name="ApproveViewleaveaplication"),
]
