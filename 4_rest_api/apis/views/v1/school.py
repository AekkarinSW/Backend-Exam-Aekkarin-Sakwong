from django.db.models import Count
from rest_framework import viewsets

from ...filters import SchoolFilter
from ...models import School
from ...serializers import SchoolDetailSerializer, SchoolSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all().order_by("id")
    serializer_class = SchoolSerializer
    filterset_class = SchoolFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "retrieve":
            queryset = queryset.annotate(
                classroom_count=Count("classrooms", distinct=True),
                teacher_count=Count(
                    "classrooms__teachers",
                    distinct=True,
                ),
                student_count=Count(
                    "classrooms__students",
                    distinct=True,
                ),
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SchoolDetailSerializer
        return SchoolSerializer
