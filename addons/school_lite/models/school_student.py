from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student'
    _inherit = ['mail.thread']
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(string='Student Code', readonly=True, copy=False)
    birth_date = fields.Date()
    age = fields.Integer(compute='_compute_age')
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

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'The student code must be unique.'),
    ]

    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.context_today(self)
        for student in self:
            if student.birth_date:
                student.age = relativedelta(today, student.birth_date).years
            else:
                student.age = 0

    @api.constrains('birth_date')
    def _check_birth_date(self):
        today = fields.Date.context_today(self)
        for student in self:
            if student.birth_date and student.birth_date > today:
                raise ValidationError(_("The birth date cannot be in the future."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('school.student')
        return super().create(vals_list)
