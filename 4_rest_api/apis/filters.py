from django_filters import rest_framework as filters

from .models import Classroom, School, Student, Teacher


class SchoolFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
    )

    class Meta:
        model = School
        fields = ["name"]


class ClassroomFilter(filters.FilterSet):
    school = filters.NumberFilter(field_name="school_id")

    class Meta:
        model = Classroom
        fields = ["school"]


class TeacherFilter(filters.FilterSet):
    school = filters.NumberFilter(method="filter_school")
    classroom = filters.NumberFilter(field_name="classrooms__id")
    firstname = filters.CharFilter(
        field_name="first_name",
        lookup_expr="icontains",
    )
    first_name = filters.CharFilter(
        field_name="first_name",
        lookup_expr="icontains",
    )
    last_name = filters.CharFilter(
        field_name="last_name",
        lookup_expr="icontains",
    )
    lastname = filters.CharFilter(
        field_name="last_name",
        lookup_expr="icontains",
    )
    gender = filters.CharFilter(
        field_name="gender",
        lookup_expr="iexact",
    )

    class Meta:
        model = Teacher
        fields = []

    def filter_school(self, queryset, name, value):
        return queryset.filter(
            classrooms__school_id=value,
        ).distinct()


class StudentFilter(filters.FilterSet):
    school = filters.NumberFilter(field_name="classroom__school_id")
    classroom = filters.NumberFilter(field_name="classroom_id")
    firstname = filters.CharFilter(
        field_name="first_name",
        lookup_expr="icontains",
    )
    first_name = filters.CharFilter(
        field_name="first_name",
        lookup_expr="icontains",
    )
    last_name = filters.CharFilter(
        field_name="last_name",
        lookup_expr="icontains",
    )
    lastname = filters.CharFilter(
        field_name="last_name",
        lookup_expr="icontains",
    )
    gender = filters.CharFilter(
        field_name="gender",
        lookup_expr="iexact",
    )

    class Meta:
        model = Student
        fields = []
