# import all the models here and them to the admin panel

from .subject import Subject
from .student import Student
from db.session import admin

admin.register(
    Subject,
    list_display=["id", "name", "code"],
)

admin.register(
    Student,
    list_display=["id", "name", "email", "phone", "college"]
)
