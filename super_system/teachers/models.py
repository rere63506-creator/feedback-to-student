from django.db import models
import secrets
def generate_code():
    return secrets.token_hex(4)

class Code(models.Model):
    codes=models.CharField(max_length=20,unique=True,default=generate_code)
    is_used=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.codes}-{'used'if self.is_used else'free'}"


class Teacher(models.Model):
    first_name=models.CharField(max_length=30,default="")
    last_name=models.CharField(max_length=30,null=True,default="")
    subject=models.CharField(max_length=50,null=True,default="")
    activation_code=models.OneToOneField(Code,null=True,on_delete=models.CASCADE,blank=True,unique=True)
    phone=models.CharField(max_length=20,null=True,default="",unique=True)
    password=models.CharField(max_length=200,null=True,default="")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.full_name} {self.subject}"

class Student(models.Model):
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=True,default="")
    phone=models.CharField(max_length=20,null=True,default="")
    grade=models.CharField(max_length=50,null=True,blank=True)
    attend=models.BooleanField(default=True)
    homework=models.BooleanField(default=False,null=True)
    paid=models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    done=models.BooleanField(default=False)


class Homework(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='homework_list')
    date=models.DateField(auto_now_add=True)
    done=models.BooleanField(default=False)
    note=models.CharField(max_length=20,blank=True)


class Payment(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    paid=models.BooleanField(default=False)
    date=models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.student.name}-{self.date}"