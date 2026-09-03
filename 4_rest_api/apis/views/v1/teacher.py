from rest_framework import viewsets

from ...filters import TeacherFilter
from ...models import Teacher
from ...serializers import TeacherDetailSerializer, TeacherSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.prefetch_related("classrooms").order_by("id")
    serializer_class = TeacherSerializer
    filterset_class = TeacherFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TeacherDetailSerializer
        return TeacherSerializer
