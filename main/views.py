import os

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Childern
from .models import Course
from .models import Admin
from django.http import HttpResponse
import csv
import pandas as pd
from .models import Notices
import openpyxl

# Create your views here.



def index(request):
    return render(request, 'Admin-home.html')

def studentlist(request):
    stu_list= Childern.objects.all()
    return render(request, 'studentlist.html', {'stu_list':stu_list})

def courselist(request):
    course_list= Course.objects.all()
    return render(request, 'courselist.html',{'course_list':course_list} )

def modifycourse(request):
    return render(request, 'modifyCourse.html')

def modifystudent(request):
    course_list = Course.objects.all()
    return render(request, 'modifyStudent.html', {'course_list': course_list})

def addstudent(request):
    course_list = Course.objects.all()
    return render(request, 'addstu.html' , {'course_list': course_list})

def newstu(request):
    if request.method == "POST":
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        name4 = name[0:4]
        yob = dob[0:4]
        pas = name4+str(yob)
        email = request.POST.get('email')
        mob = request.POST.get('mob')
        ad = request.POST.get('addr')
        course = request.POST.get('course')
        c = Course.objects.get(course_id = course)
        data = Childern(course = c, name=name, dob=dob, email=email, pas = pas, mobile = mob, add = ad)
        data.save()
    return render(request, 'Admin-home.html')


from .forms import UploadFileForm
def upload1(request, id):
    cvar = Course.objects.get(id=id)
    return render(request, 'uploadfile.html', {'cvar':cvar})

def uploadfile(request, id):
    df = request.FILES['uploadedfile']
    wb = openpyxl.load_workbook(df)
    worksheet = wb["Sheet1"]
    excel_data = list()
    for row in worksheet.iter_rows():
        row_data = list()
        for cell in row:
            row_data.append(str(cell.value))
        excel_data.append(row_data)
    df = pd.DataFrame(excel_data,columns=['Name', 'DOB', 'mail', 'mobile', 'address'])
    rows = df.shape[0]
    for i in range(rows):
        name = df.at[i, 'Name']
        dob = df.at[i, 'DOB']
        email = df.at[i, 'mail']
        mobile = df.at[i, 'mobile']
        addr = df.at[i,'address']
        c = Course.objects.get(id=id)
        name4 = name[0:4]
        yob = dob[0:4]
        pas = name4 + str(yob)
        data = Childern(course=c, name=name, dob=dob, email=email, pas=pas, mobile=mobile, add=addr)
        data.save()
    stu_list = Childern.objects.all()
    return render(request, 'studentlist.html', {'stu_list': stu_list})

def changestd(request):
    if request.method == "POST":
        csid = request.POST.get('sid')
        cnum = request.POST.get('newnum')
        cadd = request.POST.get('newadd')
        ccourse = request.POST.get('newcourse')
        c = Course.objects.get(course_id = ccourse)
        if (Childern.objects.filter(id=csid).exists()):
            t = Childern.objects.get(id=csid)
            t.mobile = cnum
            t.add = cadd
            t.course = c
            t.save()
            messages.success(request, 'Student Mofified Successfully!')
            return render(request, 'Admin-home.html')
        return render(request, 'Admin-home.html')
    return render(request, 'Admin-home.html')

def addcourse(request):
    return render(request, 'addcourse.html')

def newcourse(request):
    if request.method == "POST":
        cname = request.POST.get('cname')
        cid = request.POST.get('cid')
        clink = request.POST.get('clink')
        sdate = request.POST.get('startdate')
        edate = request.POST.get('enddate')
        if (Course.objects.filter(course_id = cid).exists()):
            return render(request, 'Admin-home.html')
        else:
            data = Course(course_name = cname, course_id=cid, link = clink, start_date = sdate, end_date=edate)
            data.save()
    return render(request, 'Admin-home.html')

def changecourse(request):
    if request.method == "POST":
        cname = request.POST.get('Cname')
        cid = request.POST.get('Ccode')
        nname = request.POST.get('Nname')
        nid = request.POST.get('Ncode')
        nsdate = request.POST.get('nsdate')
        nedate = request.POST.get('nedate')
        nlink = request.POST.get('Nlink')
        if (Course.objects.filter(course_name=cname, course_id=cid).exists()):
            t = Course.objects.get(course_id = cid)
            t.course_name = nname
            t.course_id = nid
            t.link = nlink
            t.start_date = nsdate
            t.end_date = nedate
            t.save()
            messages.success(request, 'Course Mofified Successfully!')
            return render(request, 'Admin-home.html')
        return render(request, 'Admin-home.html')
    return render(request, 'Admin-home.html')

def validiate(request):
    if request.method == "POST":
        id = request.POST.get('sid')
        if (Childern.objects.filter(id = id).exists()):
            child = Childern.objects.get(id = id)
            mob = child.mobile
            print(mob)
            if (request.POST.get('option1')):
                newmob = mob
            else:
                newmob = request.POST.get('newnum')
                child.mobile = newmob
            add = child.add
            if (request.POST.get('option2')):
                newadd = add
            else:
                newadd = request.POST.get('newadd')
                child.add = newadd
    return render(request, 'Admin-home.html')


def dropstu(request):
    return render(request, 'dropstu.html')

def dropcourse(request):
    return render(request, 'dropcourse.html')

def delete(request, id):
  member = Childern.objects.get(id=id)
  member.delete()
  stu_list = Childern.objects.all()
  return render(request, 'studentlist.html' , {'stu_list': stu_list})

def delete1(request, id):
  member = Course.objects.get(id=id)
  member.delete()
  course_list = Course.objects.all()
  return render(request, 'courselist.html', {'course_list': course_list})




def getdata(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="Students.csv"'},
    )
    students = Childern.objects.all()
    writer = csv.writer(response)
    writer.writerow(['ID','Name','Date of birth', 'Email', 'Mobile','Address', 'Course', 'Attendance', 'Progress'])
    for student in students:
        writer.writerow([student.id,student.name,student.dob, student.email, student.mobile, student.add,student.course, student.attendance, student.progress])
    return response

def downloadcoursecsv(request, id):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="CourseStudents.csv"'},
    )
    students = Childern.objects.filter(course = id)
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Date of birth', 'Email', 'Mobile', 'Address', 'Attendance', 'Progress'])
    for student in students:
        writer.writerow([student.id, student.name, student.dob, student.email, student.mobile, student.add, student.attendance, student.progress])
    return response


def back(request):
    return render(request, 'Admin-home.html')

def home(request):
    return render(request, 'index.html')
def upload(request, id):
    cvar = Course.objects.get(id = id)
    return render(request, 'fileupload.html', {'cvar': cvar})
# def uploadmedia(request, id):
#     cvar = Course.objects.get(id=id)
#     return render(request, 'fileupload.html', {'cvar': cvar})
#
# def formsubmission(request, id):
#     form = upload()
#     if request.method == "POST":
#         form = upload(request.POST,request.FILES)
#         if form.is_valid():
#             f = request.FILES['file']
#             cvar = Course.objects.get(id=id)
#             cname = cvar.course_id
#             with open('media/' + cname + '/' + f.name, 'wb+') as destination:
#                 for chunk in f.chunks():
#                     destination.write(chunk)
#             return HttpResponse("FILE UPLOADED SUCCESSFULLY")
#         else:
#             form = upload()
#             return render(request, 'Admin-home.html', {'form': form})

def notification(request):
    course_list = Course.objects.all()
    return render(request, 'notice.html', {'course_list': course_list})

def pushnotice(request):
    cid = request.POST.get('course')
    msg = request.POST.get('notice')
    c = Course.objects.get(course_id = cid)
    data = Notices(course_id=c, notice = msg)
    data.save()
    return render(request, 'Admin-home.html')

def newstu(request):
    if request.method == "POST":
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        name4 = name[0:4]
        yob = dob[0:4]
        pas = name4 + str(yob)
        email = request.POST.get('email')
        mob = request.POST.get('mob')
        ad = request.POST.get('addr')
        course = request.POST.get('course')
        c = Course.objects.get(course_id=course)
        data = Childern(course=c, name=name, dob=dob, email=email, pas=pas, mobile=mob, add=ad)
        data.save()
    return render(request, 'Admin-home.html')


def pushednotices(request, id):
    notices = Notices.objects.filter(course_id = id)
    c = Course.objects.get(id = id)
    cid = c.course_id
    context = {}
    context.update({'notices':notices})
    context.update({'cid': cid})
    return render(request, 'pushednotices.html', context)

def deletenotice(request, id):
  member = Notices.objects.get(id=id)
  member.delete()
  return render(request, 'Admin-home.html')

def changeadminpassword(request):
    return render(request, 'changeadminpass.html')

def updateadminpass(request):
    if request.method == "POST":
        mail = request.POST.get('email')
        newpass = request.POST.get('newpass')
        if (Admin.objects.filter(email = mail).exists()):
            t = Admin.objects.get(email = mail)
            oldpass = t.pas

            if (request.POST.get('oldpass') == oldpass):
                t.pas = newpass
                t.save()
    return render(request, 'Admin-home.html')

def attendance(request, id):
    cvar = Childern.objects.filter(course = id)
    return render(request, 'attend.html', {'cvar':cvar})

def markattend(request, id):
    stu = Childern.objects.get(id = id)
    attend = request.POST.get('attend')
    stu.attendance = attend
    stu.save()
    return render(request, 'Admin-home.html')

def grades(request, id):
    cvar = Childern.objects.filter(course = id)
    return render(request, 'grades.html', {'cvar':cvar})

def markgrades(request, id):
    stu = Childern.objects.get(id=id)
    grade = request.POST.get('grade')
    stu.progress = grade
    stu.save()
    return render(request, 'Admin-home.html')
