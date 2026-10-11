from odoo import fields, models


class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Subject'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    credit_hours = fields.Integer(required=True, default=1)

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'The subject code must be unique.'),
        ('credit_hours_positive', 'CHECK(credit_hours > 0)', 'Credit hours must be greater than 0.'),
    ]
