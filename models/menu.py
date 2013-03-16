# -*- coding: utf-8 -*-

#categories menu
get_categories = db(db.project_categories.id > 0).select()
response.menu_categories = get_categories

