from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from datetime import datetime, time
from pytz import timezone
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q

# Create your views here.

# --------------------------------- General ---------------------------------

def index(request):
    name = request.user
    leave = LeaveApplication.objects.all()
    attendance = Attendance.objects.all()
    visiting = VisitingReport.objects.all()
    users = User.objects.all()
    eight_hours = timedelta(hours=8)
    for i in attendance:
        if i.morning_time and i.evening_time:
            morning_datetime = datetime.combine(datetime.today(), i.morning_time)
            evening_datetime = datetime.combine(datetime.today(), i.evening_time)
            working_hour = evening_datetime - morning_datetime
            difference = working_hour - eight_hours
            print()
            i.working_hour = working_hour
            if working_hour <= eight_hours:
                i.difference = "0Hrs"
            else:
                i.difference = difference
            i.save()
    return render(request, "index.html", {"attendance": attendance, "users": users, "visiting":visiting, "name":name, "leave":leave})

def visiting_report(request):
    if request.method == "POST":
        ist = timezone('Asia/Kolkata')
        current_time = datetime.now(ist).time()
        current_date = datetime.now(ist).date()
        name = request.POST.get("name")
        address = request.POST.get("address")
        phonenumber = request.POST.get("phonenumber")
        approval_chance = request.POST.get("approval_chance")
        summery = request.POST.get("summery")
        visiting = VisitingReport(name=name, address=address, phonenumber=phonenumber, approval_chance=approval_chance, summery=summery, usr=request.user, visited_date=current_date, visited_time=current_time)
        visiting.save()
        messages.info(request, "Visiting report added successfuly...")
        return redirect("index")
    return redirect("index")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already Taken")
                return render(request, "register.html")
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                return redirect('login')
        else:
            messages.info(request, "Both passwords are not matching")
            return render(request, "register.html")
    return render(request, "register.html")

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password incorrect')
            return render(request, "login.html")
    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

# --------------------------------- Attandance ---------------------------------

def punch(request):
    return render(request, "punch.html")

def mark_attendance(request):
    user = request.user
    if request.method == 'POST':
        ist = timezone('Asia/Kolkata')
        current_time = datetime.now(ist).time()
        current_date = datetime.now(ist).date()

        # Define time ranges for attendance marking
        morning_start = time(8, 30)
        morning_end = time(9, 30)
        intermediate_time = time(13, 0)
        evening_start = time(18, 0)
        evening_end = time(18, 30)

        punch_stat = ''
        if current_time < morning_start:
            punch_stat = 'Overtime'
        if morning_start <= current_time <= morning_end:
            punch_stat = 'OnTimeMorning'
        elif morning_end < current_time < intermediate_time:
            punch_stat = 'LatePunchMorning'
            
        elif intermediate_time <= current_time < evening_start:
            punch_stat_evening = 'EarlyPunchEvening'
        elif evening_start <= current_time <= evening_end:
            punch_stat_evening  = 'OntimeEvening'
        elif current_time > evening_end:
            punch_stat_evening  = 'Overtime'
        
        if Attendance.objects.filter(usr=request.user, date=current_date).exists():
            attendance = Attendance.objects.filter(usr=request.user, date=current_date).first()
            if current_time > intermediate_time:
                if attendance.evening_time:
                    return JsonResponse({'status': 'already_marked'})
                attendance.evening_time = current_time
                attendance.punch_stat_evening = punch_stat_evening
                attendance.date = current_date
                attendance.save()
                return JsonResponse({'status':'success'})
            else:
                if attendance.morning_time:
                    return JsonResponse({'status': 'already_marked'})
                attendance.morning_time = current_time
                attendance.punch_stat = punch_stat
                attendance.date = current_date
                attendance.save()
                return JsonResponse({'status':'success'})
        else:
            if current_time < intermediate_time:
                new_punch = Attendance(usr=request.user, date=current_date, morning_time=current_time, punch_stat=punch_stat)
                new_punch.save()
                return JsonResponse({'status':'success'})
            else:
                new_punch = Attendance(usr=request.user, date=current_date, evening_time=current_time,punch_stat_evening=punch_stat_evening)
                new_punch.save()
                return JsonResponse({'status':'success'})
    return redirect("index")

def overtime(request):
    attendance = Attendance.objects.filter(Q(punch_stat="overtime") | Q(punch_stat_evening="overtime"))
    users = User.objects.all()
    return render(request, "General/overtime.html", {"attendance":attendance, "users":users})
    
from datetime import datetime, timedelta

def viewallatendancereport(request):
    attendance = Attendance.objects.all()
    users = User.objects.all()
    eight_hours = timedelta(hours=8)
    for i in attendance:
        if i.morning_time and i.evening_time:
            morning_datetime = datetime.combine(datetime.today(), i.morning_time)
            evening_datetime = datetime.combine(datetime.today(), i.evening_time)
            working_hour = evening_datetime - morning_datetime
            difference = working_hour - eight_hours
            print()
            i.working_hour = working_hour
            if working_hour <= eight_hours:
                i.difference = "0Hrs"
            else:
                i.difference = difference
            i.save()
    return render(request, "General/Attendance_Report.html", {"attendance": attendance, "users": users})


def sortattandance(request):
    users = User.objects.all()
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        print(start_date)
        end_date = request.POST.get("end_date")
        print(end_date)
        by_user = request.POST.get("by_user")
        print(by_user)
        name = request.user
        leave = LeaveApplication.objects.all()
        attendance = Attendance.objects.all()
        visiting = VisitingReport.objects.all()
        users = User.objects.all()
        eight_hours = timedelta(hours=8)
        for i in attendance:
            if i.morning_time and i.evening_time:
                morning_datetime = datetime.combine(datetime.today(), i.morning_time)
                evening_datetime = datetime.combine(datetime.today(), i.evening_time)
                working_hour = evening_datetime - morning_datetime
                difference = working_hour - eight_hours
                print()
                i.working_hour = working_hour
                if working_hour <= eight_hours:
                    i.difference = "0Hrs"
                else:
                    i.difference = difference
                i.save()
        if by_user == "all":
            attendance = Attendance.objects.filter(date__gte=start_date, date__lte=end_date)
            return render(request, "index.html", {"attendance":attendance, "users":users, "visiting":visiting, "name":name, "leave":leave})
        else:
            usr = User.objects.get(username=by_user)
            attendance = Attendance.objects.filter(date__gte=start_date, date__lte=end_date, usr=usr)
            return render(request, "index.html", {"attendance":attendance, "users":users, "visiting":visiting, "name":name, "leave":leave})

def update_visiting(request, id):
    visited = VisitingReport.objects.get(id=id)
    leave = LeaveApplication.objects.all()
    attendance = Attendance.objects.all()
    visiting = VisitingReport.objects.all()
    name = request.user
    users = User.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        phonenumber = request.POST.get("phonenumber")
        summery = request.POST.get("summery")
        approval_chance = request.POST.get("approval_chance")
        visited.name = name
        visited.address = address
        visited.phonenumber = phonenumber
        visited.summery = summery
        visited.approval_chance = approval_chance
        visited.save()
        messages.info(request, "{} Updated succesfuly...".format(name)) 
        eight_hours = timedelta(hours=8)
        for i in attendance:
            if i.morning_time and i.evening_time:
                morning_datetime = datetime.combine(datetime.today(), i.morning_time)
                evening_datetime = datetime.combine(datetime.today(), i.evening_time)
                working_hour = evening_datetime - morning_datetime
                difference = working_hour - eight_hours
                print()
                i.working_hour = working_hour
                if working_hour <= eight_hours:
                    i.difference = "0Hrs"
                else:
                    i.difference = difference
                i.save()
        return render(request, "update_visiting.html", {"attendance": attendance, "users": users, "visiting":visiting, "name":name, "leave":leave,"visited":visited})
    return render(request, "update_visiting.html", {"attendance": attendance, "users": users, "visiting":visiting, "name":name, "leave":leave,"visited":visited})

def delete_visiting(request, id):
    visited = VisitingReport.objects.get(id=id)
    visited.delete()
    messages.info(request, "Visited data deleted...")
    return redirect("index")
        
def sortattandanceovertime(request):
    users = User.objects.all()
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        print(start_date)
        end_date = request.POST.get("end_date")
        print(end_date)
        by_user = request.POST.get("by_user")
        print(by_user)
        if by_user == "all":
            attendance = Attendance.objects.filter(date__gte=start_date, date__lte=end_date)
            return render(request, "General/overtime.html", {"attendance":attendance, "users":users})
        else:
            usr = User.objects.get(username=by_user)
            attendance = Attendance.objects.filter(date__gte=start_date, date__lte=end_date, usr=usr)
            return render(request, "General/overtime.html", {"attendance":attendance, "users":users})

def Applicationforleave(request):
    if request.method == "POST":
        empname = request.POST.get('empname')
        reason = request.POST.get('reason')
        leave = LeaveApplication(empname=empname, reason=reason, usr=request.user)
        leave.save()
        messages.info(request, "Leave application submited successfuly...")
        return redirect('index')
    return redirect('index')

def Viewleaveaplications(request):
    applications = LeaveApplication.objects.all()
    return render(request, "General/Viewleaveaplications.html",{"applications":applications})

def ApproveViewleaveaplications(request):
    applications = LeaveApplication.objects.all()
    return render(request, "General/ApproveViewleaveaplications.html",{"applications":applications})

def ApproveViewleaveaplication(request, id):
    application = LeaveApplication.objects.get(id=id)
    application.approval = True
    application.save()
    messages.info(request, f"{application.empname}'s Leave application approved...")
    return redirect('index')