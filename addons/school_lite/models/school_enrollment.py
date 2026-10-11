from odoo import fields, models


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
