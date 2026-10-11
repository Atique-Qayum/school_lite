from odoo import fields, models


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student'
    _inherit = ['mail.thread']
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(string='Student Code', readonly=True, copy=False)
    birth_date = fields.Date()
    class_id = fields.Many2one('school.class', string='Class', tracking=True)
    guardian_name = fields.Char()
    guardian_phone = fields.Char()
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('enrolled', 'Enrolled'),
            ('graduated', 'Graduated'),
            ('withdrawn', 'Withdrawn'),
        ],
        default='draft',
        required=True,
        tracking=True,
    )
    active = fields.Boolean(default=True)
