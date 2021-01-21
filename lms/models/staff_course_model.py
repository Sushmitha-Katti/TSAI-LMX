
# Core Django imports.
from django.db import models

from .course_model import Course
from .users_model import Staff


class StaffCourse(models.Model):
    """
    Model to capture student-course enrollments.
    """
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    

    def __str__(self):
        return f'{self.staff.user.username} - {self.course.title}'

    # Constraints to ensure that a student cannot enroll into the same course more than once
    class Meta:
        unique_together = ('staff', 'course',)