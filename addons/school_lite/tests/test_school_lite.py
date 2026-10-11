from datetime import timedelta

from dateutil.relativedelta import relativedelta
from psycopg2 import IntegrityError

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, new_test_user
from odoo.tools import mute_logger


class TestSchoolLite(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.teacher = new_test_user(
            cls.env, login='teacher_a', groups='school_lite.group_school_teacher')
        cls.other_teacher = new_test_user(
            cls.env, login='teacher_b', groups='school_lite.group_school_teacher')
        cls.class_a = cls.env['school.class'].create({
            'name': 'Class A', 'academic_year': '2026-2027', 'teacher_id': cls.teacher.id,
        })
        cls.class_b = cls.env['school.class'].create({
            'name': 'Class B', 'academic_year': '2026-2027', 'teacher_id': cls.other_teacher.id,
        })
        cls.subject = cls.env['school.subject'].create({'name': 'History', 'code': 'HIST'})
        cls.student = cls.env['school.student'].create({
            'name': 'Test Student', 'class_id': cls.class_a.id,
        })

    def _enroll_in_subject(self, student):
        return self.env['school.enrollment'].create({
            'student_id': student.id, 'subject_id': self.subject.id,
        })

    def test_batch_create_gives_each_student_a_code(self):
        students = self.env['school.student'].create([{'name': 'A'}, {'name': 'B'}, {'name': 'C'}])
        codes = students.mapped('code')
        self.assertTrue(all(codes))
        self.assertEqual(len(set(codes)), 3)

    def test_age_is_zero_without_birth_date(self):
        self.assertEqual(self.student.age, 0)
        today = fields.Date.context_today(self.student)
        self.student.birth_date = today - relativedelta(years=10)
        self.assertEqual(self.student.age, 10)

    def test_birth_date_cannot_be_in_the_future(self):
        tomorrow = fields.Date.context_today(self.student) + timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.student.birth_date = tomorrow

    def test_student_count_follows_move_and_archive(self):
        self.assertEqual(self.class_a.student_count, 1)
        self.student.class_id = self.class_b
        self.assertEqual(self.class_a.student_count, 0)
        self.assertEqual(self.class_b.student_count, 1)
        self.student.active = False
        self.assertEqual(self.class_b.student_count, 0)

    def test_grade_must_be_between_0_and_100(self):
        enrollment = self._enroll_in_subject(self.student)
        for grade in (-1, 101):
            with self.assertRaises(ValidationError):
                enrollment.grade = grade

    @mute_logger('odoo.sql_db')
    def test_sql_constraints(self):
        with self.assertRaises(IntegrityError):
            self.env['school.subject'].create({'name': 'Duplicate', 'code': 'HIST'})
        with self.assertRaises(IntegrityError):
            self.env['school.subject'].create({'name': 'Zero', 'code': 'ZERO', 'credit_hours': 0})
        self._enroll_in_subject(self.student)
        with self.assertRaises(IntegrityError):
            self._enroll_in_subject(self.student)

    def test_enroll_requires_a_class(self):
        student_without_class = self.env['school.student'].create({'name': 'No Class'})
        with self.assertRaises(UserError):
            student_without_class.action_enroll()
        self.student.action_enroll()
        self.assertEqual(self.student.state, 'enrolled')

    def test_confirm_requires_an_enrolled_student(self):
        enrollment = self._enroll_in_subject(self.student)
        with self.assertRaises(UserError):
            enrollment.action_confirm()
        self.student.action_enroll()
        enrollment.action_confirm()
        self.assertEqual(enrollment.state, 'confirmed')

    def test_teacher_sees_only_own_class_data(self):
        self.env['school.student'].create({'name': 'Other Student', 'class_id': self.class_b.id})
        as_teacher = self.env(user=self.teacher)
        self.assertEqual(as_teacher['school.class'].search([]), self.class_a)
        self.assertEqual(as_teacher['school.student'].search([]), self.student)

    def test_wizard_skips_existing_enrollments(self):
        second_student = self.env['school.student'].create({
            'name': 'Second Student', 'class_id': self.class_a.id,
        })
        self._enroll_in_subject(self.student)
        wizard = self.env['school.class.enroll.wizard'].create({
            'class_id': self.class_a.id, 'subject_id': self.subject.id,
        })
        wizard.action_enroll_class()
        enrolled_students = self.env['school.enrollment'].search(
            [('subject_id', '=', self.subject.id)]).student_id
        self.assertEqual(enrolled_students, self.student | second_student)
