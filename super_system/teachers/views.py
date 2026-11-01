from django.db.models import Q
from django.shortcuts import render,redirect
from .models import Teacher,Student,Code


def welcome(request):
    if request.method=='POST':
        role=request.POST.get('role')
        if role=='teacher':
            return redirect('teacher_register')
        elif role=='student':
            return redirect('student_login')
    return render(request,'welcome.html')


def teacher_register(request):
    error = None
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        subject = request.POST.get('subject')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        code_text = request.POST.get('code_input','').strip().lower()
        code_obj = Code.objects.filter(codes__iexact=code_text, is_used=False).first()
        if code_obj: 
            Teacher.objects.create(
                first_name=first_name,
                last_name=last_name,
                subject=subject,
                phone=phone,
                password=password,
                activation_code=code_obj)
             
            code_obj.is_used = True
            code_obj.save()
            return redirect('teacher_login')

        else:
            error = "الرجاء التأكد من صحة كود التفعيل "
            return render(request, 'teacher_register.html', {'error': error})

    return render(request, 'teacher_register.html',{'error':error})


def teacher_login(request):
    error=None
    if request.method=='POST':
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        teacher=Teacher.objects.filter(phone=phone,password=password).first()
        if teacher:
            request.session['teacher_id']=teacher.id
            return redirect('dashboard')
        else:
            error="الرجاء التأكد من صحة كلا من رقم الهاتف و كلمة المرور"
    return render(request,'teacher_login.html',{'error':error})

def dashboard(request):
    teacher_id=request.session.get('teacher_id')
    if not teacher_id:
        return redirect('teacher_login')
    teacher=Teacher.objects.get(id=teacher_id)
    if request.method=='POST':
        name=request.POST.get('name')
        grade=request.POST.get('grade')
        phone=request.POST.get('phone')
        if name and grade:
            Student.objects.create(
                teacher=teacher,
                name=name,
                grade=grade,
                phone=phone,
            )
        return redirect('dashboard')
    all_student=Student.objects.filter(teacher=teacher)
    return render(request,'dashboard.html',{'students':all_student,"teacher":teacher})

def student_login(request):
    error=None
    if request.method=='POST':
        name=request.POST.get('name')
        grade=request.POST.get('grade')
        teacher_name=request.POST.get('teacher_name')
        parts=teacher_name.split()
        if len(parts)>=2:
            teacher = Teacher.objects.filter(first_name__icontains=parts[0], last_name__icontains=parts[1]).first()
            if teacher:
                student=Student.objects.filter(name__icontains=name.strip(),teacher=teacher).first()
                if student:
                    return redirect('student_detail',student_id=student.id)
            else:
                student=Student.objects.filter(name__icontains=name.strip()).first()
                print(f"FOUND STUDENT={student}")
        
        error="حضرتك ممكن تتأكد من البيانات المكتوبة و تحاول كتابتها تاني"
    return render(request,'student_login.html',{'error':error})

def student_detail(request,student_id):
    student=Student.objects.get(id=student_id)
    return render(request,'student_detail.html',{'student':student})


def edit_student(request,student_id):
    student=Student.objects.get(id=student_id)
    if request.method=='POST':
        student.name=request.POST.get('name')
        student.grade=request.POST.get('grade')
        student.phone=request.POST.get('phone')
        student.attend=request.POST.get('attend')=='on'
        student.homework=request.POST.get('homework')=='on'
        student.paid=request.POST.get('paid')=='on'
        student.save()
        return redirect('dashboard')
    return render(request,'edit_student.html',{'student':student})


def delete_student(request,student_id):
    student=Student.objects.get(id=student_id)
    if request.method=='POST':
        student.delete()
        return redirect('dashboard')
    return render(request,'confirm_delete.html',{'student':student})