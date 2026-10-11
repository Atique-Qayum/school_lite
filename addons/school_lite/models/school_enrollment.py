from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolEnrollment(models.Model):
    _name = 'school.enrollment'
    _description = 'Enrollment'

    student_id = fields.Many2one('school.student', required=True, ondelete='cascade')
    subject_id = fields.Many2one('school.subject', required=True, ondelete='restrict')
    enrollment_date = fields.Date(default=fields.Date.context_today)
    grade = fields.Float()
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
        ],
        default='draft',
        required=True,
    )

    _sql_constraints = [
        (
            'student_subject_unique',
            'UNIQUE(student_id, subject_id)',
            'A student can only be enrolled once in the same subject.',
        ),
    ]

    @api.constrains('grade')
    def _check_grade(self):
        for enrollment in self:
            if not 0 <= enrollment.grade <= 100:
                raise ValidationError(_("The grade must be between 0 and 100."))
