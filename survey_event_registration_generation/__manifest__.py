# Copyright 2016-2020 Akretion France (<https://www.akretion.com>)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Survey event registration generation",
    "version": "16.0.0.0.0",
    "license": "AGPL-3",
    "author": "Elabore",
    "website": "https://www.elabore.coop",
    "category": "",
    "depends": ["survey"],
    "data": [
        'views/survey_question_views.xml', 
        'views/survey_survey_views.xml',
        'views/survey_templates.xml', 
        #'security/ir.model.access.csv',
    ],
    'assets': {
        'survey.survey_assets': [
            '/survey_event_registration_generation/static/src/js/survey_form.js',
        ],
    },
    "installable": True,
}
