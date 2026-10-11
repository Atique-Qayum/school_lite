from odoo import _, api, fields, models


class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'School Class'
    _order = 'name'

    name = fields.Char(required=True)
    academic_year = fields.Char(required=True)
    teacher_id = fields.Many2one('res.users', string='Homeroom Teacher')
    student_ids = fields.One2many('school.student', 'class_id')
    student_count = fields.Integer(compute='_compute_student_count', store=True)

    @api.depends('student_ids.active')
    def _compute_student_count(self):
        for school_class in self:
            school_class.student_count = len(school_class.student_ids)

    def action_view_students(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Students'),
            'res_model': 'school.student',
            'view_mode': 'list,kanban,form',
            'domain': [('class_id', '=', self.id)],
            'context': {'default_class_id': self.id},
        }
