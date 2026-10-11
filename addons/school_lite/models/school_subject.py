from odoo import fields, models


class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Subject'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    credit_hours = fields.Integer(required=True, default=1)
