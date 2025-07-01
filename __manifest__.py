{
    'name': 'Collabora Online',
    'version': '0.1.0',
    'category': 'Productivity',
    'website': 'https://collaboraonline.com',
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
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'collabora_odoo/static/src/components/*/*.xml',
            'collabora_odoo/static/src/models/*.js',
        ],
    },
    'images': [
        'static/description/icon.svg'
    ],

    'installable': True,
    'application': True,
    'author': 'Collabora Productivity',
    'license': 'Other OSI approved licence',
}
