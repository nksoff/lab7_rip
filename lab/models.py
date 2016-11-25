from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Tutor(models.Model):
    lastname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50)
    birthday = models.DateField(null=True, blank=True)
    sex = models.BooleanField(default=True)

    def __str__(self):
        return 'Tutor: {} {} {}'.format(self.lastname, self.firstname, self.middlename)


class SexListFilter(admin.SimpleListFilter):
    title = 'Sex'
    parameter_name = 'sex'

    def lookups(self, request, model_admin):
        return [
            (True, 'Male'),
            (False, 'Female')
        ]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(sex=self.value())
        return queryset


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'firstname', 'middlename', 'birthday', 'sex_str', )
    search_fields = ('lastname',)
    list_filter = (SexListFilter,)

    def get_ordering(self, request):
        return ['birthday']


    def sex_str(self, obj):
        return 'Male' if obj.sex else 'Female'

    sex_str.short_description = 'Sex'


class Course(models.Model):
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)
    tutor = models.ForeignKey(Tutor)

    def __str__(self):
        return 'Course: {}'.format(self.name)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'tutor', 'my_field',)
    readonly_fields = ('my_field',)
    search_fields = ('name', 'full_name',)

    def my_field(self, obj):
        return "Some custom value for course {}".format(obj.name)

    def get_ordering(self, request):
        return ['-name']

    def get_list_filter(self, request):
        return ['tutor']
