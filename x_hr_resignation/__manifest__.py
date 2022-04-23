
{
    'name': 'HR Resignation',
    'version': '13.',
    'summary': 'Resignation process of the employee',
    'author': 'Asop Source',
    'company': 'Asop',
    'website': 'https://www.asop-source.com',
    'depends': ['base','hr'],
    'category': 'Human Resources',
    'maintainer': 'Techno Solutions',
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/resignation_mail.xml',
        'views/resignation_view.xml',
        'views/config_resignation.xml',
        'views/employee_view.xml',
        'wizard/approve_state.xml',
        'report/hr_resignation.xml'
    ],
    'images': ['static/description/banner.png'],
    'license': 'AGP-SX-2',
}

