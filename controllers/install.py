# -*- coding: utf-8 -*-
def index():
    
    db.auth_user.username.readable = db.auth_user.username.writable=False
    
    verify_install = db(db.system_install.id>0).select().first()

    if verify_install.status == False:      
        form_register = SQLFORM(db.auth_user)
        form_register.element(_name="password")["_id"] = "password"
        form_register.element(_name="email")["_id"] = "user_email"
        form_register.element(_name="email")['_class'] = "span9"
        form_register.element(_name="password")['_class'] = "span9"
        form_register.element(_name="first_name")['_class'] = "span9"
        form_register.element(_name="last_name")['_class'] = "span9"
            
        if form_register.accepts(request.vars):
            auth.add_group('admin', 'Administrative Group')
            auth.add_membership('admin', form_register.vars.id)
            verify_install.update_record(status=True)
            redirect(URL(c='adminpanel', f='index'))
        else:
            response.flash = form_register.errors
        return dict(form_register=form_register)

    else:
        redirect(URL(c='adminpanel', f='index'))