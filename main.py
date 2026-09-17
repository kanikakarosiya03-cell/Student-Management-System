import json
from pathlib import Path
from abc import ABC , abstractmethod




Dataset = "School_data.json"
data = {"students" : [] ,"teachers" : []}

if Path(Dataset).exists():
     with open(Dataset,"r") as f:
          content = f.read()
          if content:
               data = json.loads(content)

def save():
     with open(Dataset,"w") as f:
          json.dump(data,f,indent=4)
          

class perpose(ABC):

     @abstractmethod
     def person(self):
          pass

     @abstractmethod
     def register(self):
          pass

     @abstractmethod
     def details(self):
          pass

     @staticmethod
     def validate_email(email):
          if "@" in email and "." in email:
               return True
          else:
               return False
     

class Student(perpose):
     def person(self):                                 # method to take who is accessing
          return "student"

     def register(self):                                 #take input for regiateration
          name = input("Enter student name :- ")
          age = int(input("Enter student age :- "))
          email = input("Enter student email :- ")
          roll_no = input("Enter student roll number :- ")

          if not perpose.validate_email(email):            #return invalid if email is wrong
               print("Invalid Email")
               return

          for i in data['students']:                        #check for roll no is not same for every student
               if i['roll_no'] == roll_no:
                    print("Student already Exsist")
                    return
               
          data["students"].append({
                "name" : name,
                "age" : age,
                "email" : email,
                "roll_no" : roll_no,
                "grades" :{},
            })


          save()
          print(f"{name} successfully registered")

     def details(self):
          roll_no = input("Enter your roll number :- ")
          for s in data["students"]:
               if s['roll_no'] == roll_no:
                    grade = s['grades']
                    avg = sum(grade.values())/len(grade) if grade else 0
                    print(f"Ditails of roll no {roll_no}")
                    print(f"\nName : {s['name']}")
                    print(f"Roll no : {s['roll_no']}")
                    print(f"Average marks : {avg:.1f}")
                    print(f"Grades : {grade}")

     def add_grades(self):
          roll_no = input("Enter your roll number :- ")
          subject = input("Enter subject :- ")
          marks = float(input("Enter your marks :- "))
          for s in data['students']:
               if s['roll_no'] == roll_no:
                    s['grades'] [subject] = marks
                    save()
                    print("Grades are successfully added ")
                    return
               print("Student not found ")

class Teacher(perpose):
     def person(self):
          return "teachers"

     def register(self):
          name = input("Enter Your name :- ")
          age = int(input("Enter Your age :- "))
          email = input("Enter Your email :- ")
          emp_id = input("Enter Your employee Id :- ")
          subject = input("Enter subject :- ")

          if not perpose.validate_email(email):            #return invalid if email is wrong
             print("Invalid Email")
             return


          for i in data['teachers']:                        #check for roll no is not same for every student
               if i['emp_id'] == emp_id:
                print("Teacher already Exsist")
                return

          data["teachers"].append({
                "name" : name,
                "age" : age,
                "email" : email,
                "emp_id" : emp_id,
                "subject" : subject
        })

          save()
          print(f"{name} successfully registered")


     def details(self):
          emp_id = input("Enter your employee ID :- ")
          for s in data['teachers']:
               if s['emp_id'] == emp_id:
                    print(f"Ditails of Employee ID : {emp_id}")
                    print(f"\nName : {s['name']}")
                    print(f"Employee ID: {s['emp_id']}")
                    print(f"Subject : {s['subject']}")
                    
                    


Stu = Student() 
Teach = Teacher()                     #object 
     
#operations that you can perform
print("Enter 1 for register students :- ")
print("Enter 2 for register Teachers :- ")
print("Enter 3 for check student details :- ")
print("Enter 4 for check teachers details :- ")
print("Enter 5 for add grades :- ")

choice = int(input("Enter your choice :- "))

if choice == 1:
     Stu.register()

elif choice == 2:
     Teach.register()

elif choice == 3:
     Stu.details()

elif choice == 4:
     Teach.details()

elif choice == 5:
     Stu.add_grades()