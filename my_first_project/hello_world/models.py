from django.db import models

# Create your models here.
class Teacher(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    

class Class(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    homeroom_id = models.ForeignKey("hello_world.Teacher", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

class Subjects(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    
class TeacherByClass(models.Model):
    teacher_id = models.ForeignKey("hello_world.Teacher", on_delete=models.DO_NOTHING )
    class_id = models.ForeignKey("hello_world.Class", on_delete=models.DO_NOTHING )
    subjects_id = models.ForeignKey("hello_world.Subjects", on_delete=models.DO_NOTHING)

    def str(self):
        return f"{self.teacher_id.name} {self.class_id.name} {self.subjects_id.name}"
    

class CreditByStudent(models.Model):
        student_id = models.ForeignKey("hello_world.Student", on_delete=models.DO_NOTHING )
        subject_id = models.ForeignKey("hello_world.Subjects", on_delete=models.DO_NOTHING )
        credit = models.CharField(max_length=100)




class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    class_id = models.ForeignKey("hello_world.Class", on_delete=models.DO_NOTHING )

    def __str__(self):
        return self.name
    





    

    # class StudentToClass(models.Model):
    #     class_id = models.ForeignKey("hello_world.Class", on_delete=models.DO_NOTHING )
    #     id = models.BigAutoField(primary_key=True)
    

    

    

