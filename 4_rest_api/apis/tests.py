from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Classroom, School, Student, Teacher


def response_ids(response):
    return {item["id"] for item in response.data}


class AuthenticatedApiTestCase(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="tester",
            password="password123",
        )
        self.client.force_authenticate(user=user)

        self.school = School.objects.create(
            name="Alpha School",
            abbreviation="AS",
            address="Bangkok",
        )
        self.other_school = School.objects.create(
            name="Beta School",
            abbreviation="BS",
            address="Chiang Mai",
        )

        self.classroom_1 = Classroom.objects.create(
            school=self.school,
            grade=1,
            room=1,
        )
        self.classroom_2 = Classroom.objects.create(
            school=self.school,
            grade=1,
            room=2,
        )
        self.other_classroom = Classroom.objects.create(
            school=self.other_school,
            grade=2,
            room=1,
        )

        self.teacher = Teacher.objects.create(
            first_name="John",
            last_name="Smith",
            gender="male",
        )
        self.teacher.classrooms.set([self.classroom_1, self.classroom_2])

        self.other_teacher = Teacher.objects.create(
            first_name="Jane",
            last_name="Brown",
            gender="female",
        )
        self.other_teacher.classrooms.add(self.other_classroom)

        self.student_1 = Student.objects.create(
            first_name="Alice",
            last_name="Green",
            gender="female",
            classroom=self.classroom_1,
        )
        self.student_2 = Student.objects.create(
            first_name="Bob",
            last_name="White",
            gender="male",
            classroom=self.classroom_2,
        )


class GeneralApiTests(AuthenticatedApiTestCase):
    def test_versioned_route_names_can_be_reversed(self):
        expected_routes = {
            "v1:school-list": "/api/v1/schools/",
            "v1:classroom-list": "/api/v1/classrooms/",
            "v1:teacher-list": "/api/v1/teachers/",
            "v1:student-list": "/api/v1/students/",
        }

        for route_name, expected_url in expected_routes.items():
            with self.subTest(route_name=route_name):
                self.assertEqual(reverse(route_name), expected_url)

    def test_authentication_is_required_for_all_resources(self):
        self.client.force_authenticate(user=None)

        for url in (
            "/api/v1/schools/",
            "/api/v1/classrooms/",
            "/api/v1/teachers/",
            "/api/v1/students/",
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unknown_detail_returns_404(self):
        for url in (
            "/api/v1/schools/999999/",
            "/api/v1/classrooms/999999/",
            "/api/v1/teachers/999999/",
            "/api/v1/students/999999/",
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SchoolApiTests(AuthenticatedApiTestCase):
    def test_school_create_filter_update_and_delete(self):
        create_response = self.client.post(
            "/api/v1/schools/",
            {
                "name": "Gamma School",
                "abbreviation": "GS",
                "address": "Lampang",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        school_id = create_response.data["id"]

        filter_response = self.client.get("/api/v1/schools/?name=GAMMA")
        self.assertEqual(response_ids(filter_response), {school_id})

        update_response = self.client.patch(
            f"/api/v1/schools/{school_id}/",
            {"address": "Lamphun"},
            format="json",
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["address"], "Lamphun")

        delete_response = self.client.delete(
            f"/api/v1/schools/{school_id}/",
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_school_detail_returns_distinct_counts(self):
        response = self.client.get(f"/api/v1/schools/{self.school.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["classroom_count"], 2)
        self.assertEqual(response.data["teacher_count"], 1)
        self.assertEqual(response.data["student_count"], 2)

    def test_empty_school_returns_zero_counts(self):
        school = School.objects.create(
            name="Empty School",
            abbreviation="ES",
            address="Lampang",
        )
        response = self.client.get(f"/api/v1/schools/{school.id}/")

        self.assertEqual(response.data["classroom_count"], 0)
        self.assertEqual(response.data["teacher_count"], 0)
        self.assertEqual(response.data["student_count"], 0)

    def test_school_requires_name_abbreviation_and_address(self):
        invalid_payloads = (
            {"abbreviation": "NS", "address": "Bangkok"},
            {"name": "No Abbreviation", "address": "Bangkok"},
            {"name": "No Address", "abbreviation": "NA"},
        )

        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                response = self.client.post(
                    "/api/v1/schools/",
                    payload,
                    format="json",
                )
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ClassroomApiTests(AuthenticatedApiTestCase):
    def test_classroom_create_filter_update_and_delete(self):
        create_response = self.client.post(
            "/api/v1/classrooms/",
            {"school": self.school.id, "grade": 3, "room": 1},
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        classroom_id = create_response.data["id"]

        filter_response = self.client.get(
            f"/api/v1/classrooms/?school={self.school.id}"
        )
        self.assertIn(classroom_id, response_ids(filter_response))
        self.assertNotIn(self.other_classroom.id, response_ids(filter_response))

        update_response = self.client.patch(
            f"/api/v1/classrooms/{classroom_id}/",
            {"room": 2},
            format="json",
        )
        self.assertEqual(update_response.data["room"], 2)

        delete_response = self.client.delete(
            f"/api/v1/classrooms/{classroom_id}/",
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_classroom_detail_lists_teachers_and_students(self):
        response = self.client.get(f"/api/v1/classrooms/{self.classroom_1.id}/")

        teacher_ids = {item["id"] for item in response.data["teachers"]}
        student_ids = {item["id"] for item in response.data["students"]}

        self.assertEqual(teacher_ids, {self.teacher.id})
        self.assertEqual(student_ids, {self.student_1.id})

    def test_classroom_rejects_unknown_school(self):
        response = self.client.post(
            "/api/v1/classrooms/",
            {"school": 999999, "grade": 1, "room": 1},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TeacherApiTests(AuthenticatedApiTestCase):
    def test_teacher_create_with_multiple_classrooms_and_detail(self):
        response = self.client.post(
            "/api/v1/teachers/",
            {
                "first_name": "Peter",
                "last_name": "Parker",
                "gender": "male",
                "classrooms": [self.classroom_1.id, self.classroom_2.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        teacher_id = response.data["id"]
        self.assertEqual(
            set(response.data["classrooms"]),
            {self.classroom_1.id, self.classroom_2.id},
        )

        detail_response = self.client.get(f"/api/v1/teachers/{teacher_id}/")
        classroom_ids = {
            item["id"] for item in detail_response.data["classrooms"]
        }
        self.assertEqual(
            classroom_ids,
            {self.classroom_1.id, self.classroom_2.id},
        )

    def test_teacher_filters_and_school_filter_has_no_duplicates(self):
        filters_to_test = (
            f"school={self.school.id}",
            f"classroom={self.classroom_1.id}",
            "firstname=joh",
            "first_name=JOHN",
            "last_name=smi",
            "lastname=SMITH",
            "gender=MALE",
        )

        for query in filters_to_test:
            with self.subTest(query=query):
                response = self.client.get(f"/api/v1/teachers/?{query}")
                self.assertIn(self.teacher.id, response_ids(response))

        school_response = self.client.get(
            f"/api/v1/teachers/?school={self.school.id}"
        )
        school_ids = [item["id"] for item in school_response.data]

        self.assertEqual(school_ids.count(self.teacher.id), 1)
        self.assertNotIn(self.other_teacher.id, school_ids)

    def test_teacher_can_clear_classrooms_and_be_deleted(self):
        update_response = self.client.patch(
            f"/api/v1/teachers/{self.teacher.id}/",
            {"classrooms": []},
            format="json",
        )
        self.assertEqual(update_response.data["classrooms"], [])

        delete_response = self.client.delete(
            f"/api/v1/teachers/{self.teacher.id}/",
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_teacher_rejects_unknown_classroom(self):
        response = self.client.post(
            "/api/v1/teachers/",
            {
                "first_name": "Invalid",
                "last_name": "Teacher",
                "gender": "male",
                "classrooms": [999999],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StudentApiTests(AuthenticatedApiTestCase):
    def test_student_create_filter_and_detail(self):
        create_response = self.client.post(
            "/api/v1/students/",
            {
                "first_name": "Charlie",
                "last_name": "Black",
                "gender": "male",
                "classroom": self.classroom_1.id,
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        student_id = create_response.data["id"]

        filters_to_test = (
            f"school={self.school.id}",
            f"classroom={self.classroom_1.id}",
            "firstname=char",
            "first_name=CHARLIE",
            "last_name=bla",
            "lastname=BLACK",
            "gender=MALE",
        )

        for query in filters_to_test:
            with self.subTest(query=query):
                response = self.client.get(f"/api/v1/students/?{query}")
                self.assertIn(student_id, response_ids(response))

        detail_response = self.client.get(f"/api/v1/students/{student_id}/")
        self.assertEqual(
            detail_response.data["classroom"]["id"],
            self.classroom_1.id,
        )

    def test_student_can_move_to_one_classroom_and_be_deleted(self):
        update_response = self.client.patch(
            f"/api/v1/students/{self.student_1.id}/",
            {"classroom": self.classroom_2.id},
            format="json",
        )
        self.assertEqual(update_response.data["classroom"], self.classroom_2.id)

        self.student_1.refresh_from_db()
        self.assertEqual(self.student_1.classroom_id, self.classroom_2.id)

        delete_response = self.client.delete(
            f"/api/v1/students/{self.student_1.id}/",
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_student_requires_a_classroom(self):
        response = self.client.post(
            "/api/v1/students/",
            {
                "first_name": "No",
                "last_name": "Classroom",
                "gender": "female",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_student_rejects_unknown_classroom(self):
        response = self.client.post(
            "/api/v1/students/",
            {
                "first_name": "Invalid",
                "last_name": "Student",
                "gender": "female",
                "classroom": 999999,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
