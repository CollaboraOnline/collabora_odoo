{
    'name': 'Collabora Online',
    'version': '18.0.0.1.0',
    'category': 'Productivity',
    'website': 'https://collaboraonline.com',
    'description': """
    The Collabora Online module allow to open and collaboratively edit office documents
    attached in Odoo in Collabora Online.

    This module can use your existing setup of Collabora Online.
    """,
    'depends': [
        "base",
        "mail"
    ],
    "external_dependencies": {
        "python": [
            "pyjwt"
        ]
    },
    'data': [
        'views/templates.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'collabora_odoo/static/src/components/*/*.xml',
            'collabora_odoo/static/src/models/*.js',
        ],
        'web.assets_frontend': [
            'collabora_odoo/static/src/cool/js/*',
            'collabora_odoo/static/src/cool/css/*',
        ]
    },
    'images': [
        'static/description/images/cool_edit_screenshot.png',
        'static/description/images/cool_attachment.png',
    ],

    'installable': True,
    'application': True,
    'author': 'Collabora Productivity',
    'license': 'Other OSI approved licence',
}
