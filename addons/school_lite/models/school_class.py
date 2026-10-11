from odoo import fields, models


class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'School Class'
    _order = 'name'

    name = fields.Char(required=True)
    academic_year = fields.Char(required=True)
    teacher_id = fields.Many2one('res.users', string='Homeroom Teacher')
    student_ids = fields.One2many('school.student', 'class_id')
