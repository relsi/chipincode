# -*- coding: utf-8 -*-

def index():
    redirect(URL(c='default', f='index'))
    pass

@auth.requires_login()
def profile():
    suported_projects = db(db.project_donation.id_auth_user == auth.user.id).select(
        db.project.ALL,
        db.project_donation.ALL,
        left=[db.project.on(db.project.id == db.project_donation.id_project)]
    )
    created_projects = db(db.project.id_auth_user == auth.user.id).select()
    
    #reverse donation
    if request.post_vars:
        user_credit = db(db.user_credit.id_auth_user == request.post_vars.id_auth_user).select()
        if not user_credit:
            credit_insert =  db.user_credit.insert(
                id_auth_user = request.post_vars.id_auth_user, 
                credit_value = request.post_vars.donation_value
                )
            donation_delete = db((db.project_donation.id_auth_user == request.post_vars.id_auth_user)&(db.project_donation.id_project == request.post_vars.id_project)).delete()
            response.flash = T("Donation reversed!")
        else:
            user_credit = db(db.user_credit.id_auth_user == request.post_vars.id_auth_user).select()
            for item in user_credit:
                credit_value = item.credit_value
                new_value = credit_value + float(request.post_vars.donation_value)
                new_credit = db(db.user_credit.id_auth_user == request.post_vars.id_auth_user).update(credit_value = new_value)
                donation_delete = db((db.project_donation.id_auth_user == request.post_vars.id_auth_user)&(db.project_donation.id_project == request.post_vars.id_project)).delete()
                response.flash = T("Donation reversed!")

    total_user_credit = db(db.user_credit.id_auth_user == auth.user.id).select()
    for credit in total_user_credit:
        total_credit = credit.credit_value
    if not total_user_credit: 
        total_credit = 0.0

    return dict(suported_projects=suported_projects, created_projects=created_projects, total_credit=total_credit)

@auth.requires_login()
def profile_edit():
    db.auth_user.username.readable = db.auth_user.username.writable = False 
    db.auth_user.completed_registration.readable = db.auth_user.completed_registration.writable = False 
    form_profile_edit=auth.profile(next=URL(c='user', f='profile'))
    form_profile_edit.element(_name='first_name')['_class'] = "span2"
    form_profile_edit.element(_name='about')['_class'] = "span5"
    form_profile_edit.element(_name='about')['_rows'] = "3"
    form_profile_edit.element(_name='address')['_class'] = "span6"
    form_profile_edit.element(_name='u_state')['_class'] = "span1"
    form_profile_edit.element(_name='zip')['_class'] = "span2"
    return dict(form_profile_edit=form_profile_edit)

@auth.requires_login()
def profile_complete():
    db.auth_user.username.readable = db.auth_user.username.writable = False 
    form_profile_complete=auth.profile(next=URL(c='project', f='project_send'))
    form_profile_complete.element(_name='first_name')['_class'] = "span2"
    form_profile_complete.element(_name='ein')['_required'] = "required"
    form_profile_complete.element(_name='zip')['_required'] = "required"
    form_profile_complete.element(_name='address')['_required'] = "required"
    form_profile_complete.element(_name='u_city')['_required'] = "required"
    form_profile_complete.element(_name='u_state')['_required'] = "required"
    form_profile_complete.element(_name='phone')['_required'] = "required"
    form_profile_complete.element(_name='about')['_class'] = "span5"
    form_profile_complete.element(_name='about')['_rows'] = "3"
    form_profile_complete.element(_name='address')['_class'] = "span6"
    form_profile_complete.element(_name='u_state')['_class'] = "span1"
    form_profile_complete.element(_name='zip')['_class'] = "span2"
    return dict(form_profile_complete=form_profile_complete)

def request_password():
    """
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """ 
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
