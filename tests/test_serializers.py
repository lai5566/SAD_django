# import relevant modules
import unittest
from unittest.mock import patch

from django.test import TestCase
from rest_framework import serializers
from schedule_courses.serializers import CourseSelectionSerializer


class TestCourseSelectionSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.serializer = CourseSelectionSerializer()

    def setUp(self):
        self.data = {
            "course_ids": [1, 2, 3]
        }

    @patch("schedule_courses.serializers.Course.objects.filter")
    def test_validate_course_ids(self, mock_filter):
        mock_filter.return_value.count.return_value = len(set(self.data["course_ids"]))
        self.assertEqual(self.serializer.validate_course_ids(self.data["course_ids"]), self.data["course_ids"])
        mock_filter.return_value.count.assert_called_once()

        mock_filter.return_value.count.return_value = len(set(self.data["course_ids"])) - 1
        self.assertRaises(serializers.ValidationError, self.serializer.validate_course_ids, self.data["course_ids"])
        mock_filter.return_value.count.assert_called()

    def test_create(self):
        mock_context = {
            "request": unittest.mock.MagicMock()
        }
        self.serializer.context = mock_context
        with patch("schedule_courses.serializers.StudentCourse.objects.filter") as mock_filter, \
                patch("schedule_courses.serializers.StudentCourse.objects.bulk_create") as mock_bulk_create:
            mock_filter.return_value.delete.return_value = None
            mock_bulk_create.return_value = None
            result = self.serializer.create(self.data)

            self.assertEqual(result, {"message": "Courses selected successfully."})
            mock_filter.assert_called_once_with(user=self.serializer.context["request"].user)
            mock_filter.return_value.delete.assert_called_once()

            student_courses = [
                unittest.mock.MagicMock(user=self.serializer.context["request"].user, course_id=course_id) for course_id
                in self.data["course_ids"]
            ]
            mock_bulk_create.assert_called_once_with(student_courses)


if __name__ == "__main__":
    unittest.main()
