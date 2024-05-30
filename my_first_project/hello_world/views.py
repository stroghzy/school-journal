from .models import Teacher, Class, Subjects, CreditByStudent, Student, TeacherByClass
from custom_auth.models import Token, PseudoUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
from re import match

# Teacher, Student, Director, Parent

@api_view(["GET", "POST"])
def get_all_teachers(request):
    if request.method == 'POST':
        if "token" not in request.data:
            return Response({"status": "error", "message": "Передайте токен"})
        user = get_user(request.data["token"])
        if user["status"] == "error":                                             
            return Response(user)
        if user["user"]["role"] not in  ["Teacher", "Director"]: 
            return Response({"status": "error", "message": "У вас недостаточно прав для использования этой функции"})
        data = Teacher.objects.all()
        result = {"data": []}
        for teacher in data:
            result["data"].append([teacher.id, teacher.name, teacher.age])
        return Response(result)
    return Response({"message": "Здесь вы можете получить информацию о учителях"})


@api_view(["GET", "POST"])
def get_all_classes(request):
    data = Class.objects.all()
    result = {}
    for class1 in data:
        if class1.homeroom_id is None:
            result.append(f"{class1.id} {class1.name} Классного нет <br>")
        else:
            result.append(f"{class1.id} {class1.name} {class1.homeroom_id.name}<br>")
    return Response("".join(result))


@api_view(["GET", "POST"])
def get_class(request): # Sdelano
    if request.method == 'POST':
        if "token" not in request.data:
            return Response({"status": "error", "message": "Передайте токен"})
        user = get_user(request.data["token"])
        if user["status"] == "error":                                             
            return Response(user)
        if user["user"]["role"] not in  ["Teacher", "Student", "Parent"]: 
            return Response({"status": "error", "message": "У вас недостаточно прав для использования этой функции"})
        if user["user"]["role"] == "Teacher":
            result = {"classes": []}
            for triplet in TeacherByClass.objects.filter(teacher_id=Teacher.objects.get(id=user["user"]["role_id"])):
                result["classes"].append({"name": triplet.class_id.name, "homeroom": triplet.class_id.homeroom_id.name, "subject": triplet.subjects_id.name, "students": []})
                for student in Student.objects.filter(class_id=triplet.class_id):
                    student_credit = CreditByStudent.objects.filter(student_id=student, subject_id=triplet.subjects_id)
                    if student_credit.exists():
                        result["classes"][-1]["students"].append({"name": student.name, "credit": student_credit[0].credit})
                    else:
                        result["classes"][-1]["students"].append({"name": student.name, "credit": None})
            return Response(result)
        else:
            result = {'name': None, "homeroom": None, "students": []}
            class_obj = Student.objects.get(id=user["user"]["role_id"]).class_id
            result["name"] = class_obj.name
            result["homeroom"] = class_obj.homeroom_id.name
            for student in Student.objects.filter(class_id=class_obj):
                result["students"].append(student.name)
            return Response(result)
    return Response({"message": "Здесь вы можете получить информацию о заданном классе"})


@api_view(["GET", "POST"])
def get_all_TeacherByClass(request):
    data = TeacherByClass.objects.all()
    result = {}
    for TeacherByClass in data:
        result.append(f"{TeacherByClass.id} {TeacherByClass.name} {TeacherByClass.age}<br>")
    return Response("".join(result))

@api_view(["GET", "POST"])
def get_quarter_credits(request):
    if request.method == "POST":
        data = request.data
        if "token" not in data:
            return Response({"status": "error", "message": "Передайте токен"})
        user = get_user(data["token"])
        if user["status"] == "error":                                             
            return Response(user)
        if user["user"]["role"] not in ["Student", "Parent", "Teacher"]:
             return Response({"status": "error", "message": "Этот раздел для учеников"})
        if user["user"]["role"] == "Teacher":
            if "class_id" not in data or "subject_id" not in data:
                return Response({'status': 'error', 'message': 'Передайте class_id и subject_id'})
            subject_obj = Subjects.objects.filter(id=data['subject_id'])
            if not subject_obj.exists():
                return Response({'status': 'error', 'message': 'Нет такого предмета в базе'})
            class_obj = Class.objects.filter(id=data['class_id'])
            if not class_obj.exists():
                return Response({'status': 'error', 'message': 'Нет такого класса в базе'})
            result = {"class": class_obj[0].name, "subjects": subject_obj[0].name, "students": []}
            for student_obj in Student.objects.filter(class_id=class_obj[0]):
                triplet = CreditByStudent.objects.get(student_id=student_obj)
                credits = list(map(int, list(triplet.credit)))
                result["student"].append({"name": student_obj.name, "avg_credit": round(sum(credits)/len(credits), 2) })
            return Response(result)
        else:
            student_obj = Student.objects.get(id=user["user"]["role_id"])
            result = {"student": {"name": student_obj.name, "class": student_obj.class_id.name}, "credits": {}}
            for triplet in CreditByStudent.objects.filter(student_id=student_obj): 
                credits = list(map(int, list(triplet.credit)))
                result["credits"][triplet.subjects_id.name] = round(sum(credits)/len(credits), 2)
            return Response(result)
    return Response({"message": "Здесь можно посмотреть итоговую оценку за четверть"})


@api_view(["GET", "POST"]) #Сделано
def add_credit(request):
    if request.method == 'POST':
        data = request.data
        if not ("student_id" in data and "subject_id" in data and "credit" in data and "token" in data):
            return Response({'status': 'error', 'message': 'Проверьте что вы передали 4 ключа(student_id, subject_id, credit, token)'})
        user = get_user(data["token"])
        if user["status"] == "error":                                             
            return Response(user)
        if user["user"]["role"] not in ["Teacher"]: 
            return Response({"status": "error", "message": "У вас недостаточно прав для использования этой функции"})
        if not (isinstance(data['student_id'], int)  and isinstance(data['subject_id'], int)):
            return Response({'status': 'error', 'message': 'Ключи должны быть в формате целого числа' })
        if match(r'^\d$', data["credit"]) is None:
            return Response({'status': 'error', 'message': 'Проверьте правильность написания оценки'})
        if not Student.objects.filter(id=data['student_id']).exists():
            return Response({'status': 'error', 'message': 'Нет такого студента в базе'})
        if not Subjects.objects.filter(id=data['student_id']).exists():
            return Response({'status': 'error', 'message': 'Нет такого предмета в базе'})
        student_obj = Student.objects.get(id=data['student_id'])
        is_allowed_student = False
        for class_id_temp in TeacherByClass.objects.filter(teacher_id=user["user"]["role_id"]):
            if student_obj.class_id == class_id_temp.class_id:
                is_allowed_student = True
        if not is_allowed_student:
            return Response({'status': 'error', 'message': 'Вам нельзя ставить оценку этому ученику'})

        subjects_obj = Subjects.objects.get(id=data['subject_id'])
        creditby_obj =CreditByStudent.objects.filter(student_id=student_obj, subject_id=subjects_obj)
        if creditby_obj.exists():
            creditby_obj.update(credit=creditby_obj[0].credit+data['credit'])
        else:
            CreditByStudent.objects.create(student_id=student_obj, subject_id=subjects_obj,credit=data['credit'])

        return Response({'status': 'success'})
    return Response({'message': 'Добавьте оценку'})

@api_view(["GET", "POST"]) #Сделано
def remove_credit(request):
    if request.method == "POST":
        data = request.data
        if not ("student_id" in data and "subject_id" in data and "token" in data):
            return Response({'status': 'error', 'message': 'Проверьте что вы передали 2 ключа'})
        user = get_user(data["token"])
        if user["status"] == "error":                                             
            return Response(user)
        if user["user"]["role"] not in ["Teacher"]: 
            return Response({"status": "error", "message": "У вас недостаточно прав для использования этой функции"})
        if not (isinstance(data['student_id'], int)  and isinstance(data['subject_id'], int)):
            return Response({'status': 'error', 'message': 'Ключи должны быть в формате целого числа' })
        if not Student.objects.filter(id=data['student_id']).exists():
            return Response({'status': 'error', 'message': 'Нет такого студента в базе'})
        if not Subjects.objects.filter(id=data['student_id']).exists():
            return Response({'status': 'error', 'message': 'Нет такого предмета в базе'})
        student_obj = Student.objects.get(id=data['student_id'])
        is_allowed_student = False
        for class_id_temp in TeacherByClass.objects.filter(teacher_id=user["user"]["role_id"]):
            if student_obj.class_id == class_id_temp.class_id:
                is_allowed_student = True
        if not is_allowed_student:
            return Response({'status': 'error', 'message': 'Вам нельзя ставить оценку этому ученику'})
        subjects_obj = Subjects.objects.get(id=data['subject_id'])
        creditby_obj =CreditByStudent.objects.filter(student_id=student_obj, subject_id=subjects_obj)
        if not creditby_obj.exists() or len(creditby_obj[0].credit) == 0:
            return Response({'status': 'error', 'message': 'У ученика нет такой оценки'})
        creditby_obj.update(credit=creditby_obj[0].credit[0:-1])
        return Response({'status': 'success'})
    return Response({'message': 'здесь вы можете удалить оценку'})

def get_user(token):
    token_obj = Token.objects.filter(token=token)
    if not token_obj.exists():
        return {"status": "error", "message": "Токена не существует"}
    if token_obj[0].date_expired < datetime.datetime.now(datetime.timezone.utc):
        return {"status": "error", "message": "Токен просрочен"}
    user_obj = PseudoUser.objects.filter(email=token_obj[0].email)[0]
    return {"status": "success", "user": {"email": user_obj, "role": user_obj.role, "role_id": user_obj.role_id}}
    