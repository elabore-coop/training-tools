# -*- coding: utf-8 -*-

{
    "name": "Learning Event Partner",
    "version": "16.0.0.0.0",
    "depends": [
        #'__export__',
        "base",
        "event",
        "hr",
    ],
    "author": "Nicolas JEUDY",
    "installable": True,
    "data": [
        "views/event_menu_view.xml",
        "views/event_speakers_view.xml",
        "views/event_event_view.xml",
        "views/hr_employee_views.xml",
        "security/ir.model.access.csv",
    ],
}
