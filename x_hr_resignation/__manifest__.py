
{
    'name': 'Open HRMS Resignation',
    'version': '13.0.2.0.0',
    'summary': 'Handle the resignation process of the employee',
    'author': 'Cybrosys Techno solutions,Open HRMS',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.openhrms.com',
    'depends': ['base','hr'],
    'category': 'Generic Modules/Human Resources',
    'maintainer': 'Cybrosys Techno Solutions',
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
    'license': 'AGPL-3',
}

