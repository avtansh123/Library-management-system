from django.contrib import admin
from  myapp.models import Author,Book,Student,Course,Topic
import  re
# Register your models here.
admin.site.register(Author)

#admin.site.register(Student)
admin.site.register(Course)
#admin.site.register(Book)
admin.site.register(Topic)


class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'author', 'numpages','in_stock')]
    list_display = ('title', 'author', 'numpages','in_stock')
class StudentAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','show_course']
    def show_course(self,obj):
        a=obj.course_set.all().values_list('title')
        s=str(a)
        return re.findall("'(.*?)'",s)


admin.site.register(Book,BookAdmin)
admin.site.register(Student,StudentAdmin)