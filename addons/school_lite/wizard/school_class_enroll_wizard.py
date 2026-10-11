from odoo import fields, models


class SchoolClassEnrollWizard(models.TransientModel):
    _name = 'school.class.enroll.wizard'
    _description = 'Enroll Class in Subject'

    class_id = fields.Many2one('school.class', required=True, readonly=True)
    subject_id = fields.Many2one('school.subject', required=True)

    def action_enroll_class(self):
        self.ensure_one()
        students = self.class_id.student_ids
        already_enrolled = self.env['school.enrollment'].search([
            ('student_id', 'in', students.ids),
            ('subject_id', '=', self.subject_id.id),
        ]).student_id
        self.env['school.enrollment'].create([
            {'student_id': student.id, 'subject_id': self.subject_id.id}
            for student in students - already_enrolled
        ])
        return {'type': 'ir.actions.act_window_close'}
