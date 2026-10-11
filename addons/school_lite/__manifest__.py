{
    'name': 'School Lite',
    'version': '18.0.1.0.0',
    'summary': 'Register students, organize them into classes and enroll them in subjects',
    'category': 'Education',
    'author': 'Muhammad Atique Qayum',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/school_security.xml',
        'security/ir.model.access.csv',
        'data/school_sequence.xml',
        'views/school_student_views.xml',
        'views/school_class_views.xml',
        'views/school_subject_views.xml',
        'views/school_enrollment_views.xml',
        'views/school_menus.xml',
    ],
    'demo': [
        'demo/school_demo.xml',
    ],
    'application': True,
}
