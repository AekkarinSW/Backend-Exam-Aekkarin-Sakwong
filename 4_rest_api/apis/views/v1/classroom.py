from rest_framework import viewsets

from ...filters import ClassroomFilter
from ...models import Classroom
from ...serializers import ClassroomDetailSerializer, ClassroomSerializer


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all().order_by("id")
    serializer_class = ClassroomSerializer
    filterset_class = ClassroomFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                "teachers",
                "students",
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ClassroomDetailSerializer
        return ClassroomSerializer
