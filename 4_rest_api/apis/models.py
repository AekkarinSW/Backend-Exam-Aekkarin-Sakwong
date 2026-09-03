from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=50)
    address = models.TextField()

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.name


class Classroom(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="classrooms",
    )
    grade = models.PositiveSmallIntegerField()
    room = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["school_id", "grade", "room", "id"]

    def __str__(self) -> str:
        return f"{self.school.abbreviation} - Grade {self.grade}/{self.room}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    classrooms = models.ManyToManyField(
        Classroom,
        related_name="teachers",
        blank=True,
    )

    class Meta:
        ordering = ["first_name", "last_name", "id"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name="students",
    )

    class Meta:
        ordering = ["first_name", "last_name", "id"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
