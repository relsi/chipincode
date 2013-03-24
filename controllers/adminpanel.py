# -*- coding: utf-8 -*-
@auth.requires_membership('admin')
def index():
    return locals()

@auth.requires_membership('admin')
def list_all_projects():
    query = db.project
    maxtextlength = {
                'project.project_name':50,
                'project.project_total_collected':10,
                'project.id_auth_user':50,
                'project.status_text':50
    }

    headers = {
                'project.project_name':T('Name'),
                'project.project_total_collected':T('Total Collected'),
                'project.id_auth_user':T('Owner'),
                'project.status_text':T('Project Status')
    }
    fields = [
                db.project.id,
                db.project.project_name,
                db.project.project_total_collected,
                db.project.id_auth_user,
                db.project.status_text
        ]

    ui = dict(
        widget='',
        header='',
        content='',
        default='',
        cornerall='',
        cornertop='',
        cornerbottom='',
        button='btn btn-warning',
        buttontext='buttontext button',
        buttonadd='plus',
        buttonback='leftarrow',
        buttonexport='downarrow',
        buttondelete='trash',
        buttonedit='pen',
        buttontable='rightarrow',
        buttonview='magnifier')

    grid = SQLFORM.grid(
        query=query, 
        headers=headers, 
        fields=fields,
        _class='table table-striped',
        deletable=False,
        editable=False,
        create=False,
        maxtextlength = maxtextlength,
        ui = ui
    )
    return locals()

@auth.requires_membership('admin')
def list_actives_projects():
    query = db.project.status == True
    maxtextlength = {
                'project.project_name':50,
                'project.project_total_collected':10,
                'project.id_auth_user':50,
                'project.status_text':50
    }

    headers = {
                'project.project_name':T('Name'),
                'project.project_total_collected':T('Total Collected'),
                'project.id_auth_user':T('Owner'),
                'project.status_text':T('Project Status')
    }
    fields = [
                db.project.id,
                db.project.project_name,
                db.project.project_value,
                db.project.project_total_collected,
                db.project.id_auth_user,
                db.project.status_text
        ]

    ui = dict(
        widget='',
        header='',
        content='',
        default='',
        cornerall='',
        cornertop='',
        cornerbottom='',
        button='btn btn-warning',
        buttontext='buttontext button',
        buttonadd='plus',
        buttonback='leftarrow',
        buttonexport='downarrow',
        buttondelete='trash',
        buttonedit='pen',
        buttontable='rightarrow',
        buttonview='magnifier')

    grid = SQLFORM.grid(
        query=query, 
        headers=headers, 
        fields=fields,
        _class='table table-striped',
        deletable=False,
        editable=False,
        create=False,
        maxtextlength = maxtextlength,
        ui = ui
    )
    return locals()

@auth.requires_membership('admin')
def config_website_links():
    query = db.social_network
    fields = [
                db.social_network.network_name

        ]
    ui = dict(
        widget='',
        header='',
        content='',
        default='',
        cornerall='',
        cornertop='',
        cornerbottom='',
        button='btn btn-warning',
        buttontext='buttontext button',
        buttonadd='plus',
        buttonback='leftarrow',
        buttonexport='downarrow',
        buttondelete='trash',
        buttonedit='pen',
        buttontable='rightarrow',
        buttonview='magnifier')
    grid = SQLFORM.grid(
        fields=fields,
        ui = ui,
        query=query, 
        _class='table table-striped',
        deletable=True,
        editable=True,
        create=True
    )
    return locals()

@auth.requires_membership('admin')
def config_website_faq():
    query = db.website_faq
    ui = dict(
        widget='',
        header='',
        content='',
        default='',
        cornerall='',
        cornertop='',
        cornerbottom='',
        button='btn btn-warning',
        buttontext='buttontext button',
        buttonadd='plus',
        buttonback='leftarrow',
        buttonexport='downarrow',
        buttondelete='trash',
        buttonedit='pen',
        buttontable='rightarrow',
        buttonview='magnifier')

    grid = SQLFORM.grid(
        ui = ui,
        query=query, 
        _class='table table-striped',
        deletable=True,
        editable=True,
        create=True
    )
    return locals()

@auth.requires_membership('admin')
def show_project():
    project_id = request.args(0) or redirect(URL('project', 'index'))
    project_slug = request.args(1)

    project_details = db(db.project.id == project_id).select(
        db.project.ALL,
        db.auth_user.ALL,
        db.project_categories.ALL,
        left = [
            db.auth_user.on(db.auth_user.id == db.project.id_auth_user),
            db.project_categories.on(db.project_categories.id == db.project.id_category),
        ]
    )
    updates = db(db.project_updates.id_project == project_id).select(orderby=~db.project_updates.id)
    #donation_sum = db.project_donation.donation_value.sum()
    #donors = db.project_donation.id.count()
    for item in project_details:
        #donations=db(db.project_donation.id_project == item.project.id).select(donation_sum).first()[donation_sum] or 0
        remaining_days = item.project.end_date - date.today()
        #amount_donors = db(db.project_donation.id_project == item.project.id).select(donors).first()[donors] or 0

    show_donors = db((db.project_donation.id_project == project_id)&(db.project_donation.status == True)).select(
        db.project_donation.ALL,
        db.auth_user.ALL,
        left=[
            db.auth_user.on(db.auth_user.id == db.project_donation.id_auth_user)
        ]
    )
    show_rewards = db(db.project_rewards.id_project == project_id).select()

    return dict(project_details=project_details, show_donors=show_donors, show_rewards=show_rewards, updates=updates, remaining_days = remaining_days)

@auth.requires_membership('admin')
def list_pending_projects():
    query = ((db.project.status == False)&(db.project.finalized == False))
    extra_links = [
        lambda row:A(T('Authorize'),_class="btn btn-success",_href=URL("adminpanel","authorize_project",user_signature=True,args=[row.id]))
    ] 
    maxtextlength = {
                'project.project_name':50,
                'project.status_text':50
    }

    headers = {
                'project.project_name':T('Name'),
                'project.id_auth_user':T('Owner'),
                'project.status_text':T('Project Status'),
                'project.project_value':T('Value Required')
    }
    fields = [
                db.project.id,
                db.project.project_name,
                db.project.id_auth_user,
                db.project.status_text,
                db.project.project_value
        ]

    ui = dict(
        widget='',
        header='',
        content='',
        default='',
        cornerall='',
        cornertop='',
        cornerbottom='',
        button='btn btn-warning',
        buttontext='buttontext button',
        buttonadd='plus',
        buttonback='leftarrow',
        buttonexport='downarrow',
        buttondelete='trash',
        buttonedit='pen',
        buttontable='rightarrow',
        buttonview='magnifier')

    grid = SQLFORM.grid(
        searchable=True,
        links=extra_links,
        query=query, 
        headers=headers, 
        fields=fields,
        _class='table table-striped',
        deletable=False,
        editable=False,
        create=False,
        maxtextlength = maxtextlength,
        ui = ui
    )
    return locals()

@auth.requires_membership('admin')
def authorize_project():
    id_project = request.args(0) or redirect(URL('adminpanel', 'index'))

    project_data = db(db.project.id == id_project).select()
    for item in project_data:
        project_name = item.project_name
    start_date = date.today()
    end_date = date.today() + timedelta(days=int(funding_time))
    db(db.project.id == id_project).update(
            start_date = start_date,
            end_date = end_date,
            status = True,
            status_text = T("Raising Funding")
            )
    session.flash="Project Authorized With Successful."
    redirect(URL('adminpanel', 'list_pending_projects'))

    pass

@auth.requires_membership('admin')
def config_website_categories():
    query = (db.project_categories)
    fields = [
        db.project_categories.category_name
    ]
    ui = dict(
        widget='',
        header='',
        content='',
        default='',
        cornerall='',
        cornertop='',
        cornerbottom='',
        buttonadd='plus',
        button='btn btn-warning',

)

    grid = SQLFORM.grid(
        query = query,
        ui = ui,
        fields = fields,
        deletable=False,
        details=False,
        )
    return locals()

@auth.requires_membership('admin')
def list_expired_projects():
    query = ((db.project.end_date < date.today())&(db.project.finalized == False))
    extra_links = [
        lambda row:A(T('Approve'),_class="btn btn-success",_href=URL("adminpanel","finish_successfully",user_signature=True,args=[row.id])),
        lambda row:A(T('Disapprove'),_class="btn btn-danger",_href=URL("adminpanel","finish_unsuccessfully",user_signature=True,args=[row.id]))
    ] 
    maxtextlength = {
                'project.project_name':50,
                'project.project_total_collected':10,
    }

    headers = {
                'project.project_name':T('Name'),
                'project.project_total_collected':T('Total Collected'),
    }
    fields = [
                db.project.project_name,
                db.project.project_value,
                db.project.project_total_collected,
                db.project.end_date
        ]

    ui = dict(
        widget='',
        header='',
        content='',
        default='',
        cornerall='',
        cornertop='',
        cornerbottom='',
        button='btn btn-warning',
        buttontext='buttontext button',
        buttonadd='plus',
        buttonback='leftarrow',
        buttonexport='downarrow',
        buttondelete='trash',
        buttonedit='pen',
        buttontable='rightarrow',
        buttonview='magnifier')

    grid = SQLFORM.grid(
        links = extra_links,
        searchable=True,
        query=query, 
        headers=headers, 
        fields=fields,
        _class='table table-striped',
        deletable=False,
        editable=False,
        create=False,
        maxtextlength = maxtextlength,
        ui = ui
    )
    return locals()

@auth.requires_membership('admin')
def finish_successfully():
    if request.post_vars:
        project_data = db(db.project.id == request.post_vars.project_id).select()
        for item in project_data:
            total_project = item.project_value or 0.0
            total_collected = item.project_total_collected or 0.0
            user_data = db['auth_user'][item.id_auth_user]
            body_email = """<html>Seu projeto <b>"""+item.project_name+"""</b>, alcançou a meta desejada. <br>
            <b>Total Pretendido</b>:"""+str(('%.2f' % total_project))+"""<br> 
            <b>Total Arrecadado</b>:"""+str(('%.2f' % total_collected))+"""<br>
            Logo nossa equipe entrará em contato com você.</html>"""
            mail.send(user_data.email, 'Seu Projeto foi finalizado.', body_email)

        db(db.project.id == request.post_vars.project_id).update(
            status = False,
            status_text = T("Finalized"),
            finalized = True,
            goal = True
            )
        session.flash="Project Finalized With Successful."
        redirect(URL('adminpanel', 'list_expired_projects'))
    return locals()

@auth.requires_membership('admin')
def finish_unsuccessfully():
    if request.post_vars:
        project_data = db(db.project.id == request.post_vars.project_id).select()
        for item in project_data:
            total_project = item.project_value or 0.0
            total_collected = item.project_total_collected or 0.0
            user_data = db['auth_user'][item.id_auth_user]
            body_email = """<html>Seu projeto <b>"""+item.project_name+"""</b>, não alcançou a meta. <br>
            Ele foi finalizado e o valor arrecadado foi devolvido para os doadores.<br>
            <b>Total Pretendido</b>:"""+str(('%.2f' % total_project))+"""<br> 
            <b>Total Arrecadado</b>:"""+str(('%.2f' % total_collected))+"""<br></html>"""
            mail.send(user_data.email, 'Seu Projeto foi finalizado.', body_email)

        db(db.project.id == request.post_vars.project_id).update(
            status = False,
            status_text = T("Finalized"),
            finalized = True
            )

        donation_data = db((db.project_donation.id_project == request.post_vars.project_id)&(db.project_donation.status == True)).select()
        for donation in donation_data:
            project_name = db['project'][donation.id_project]
            user_data = db['auth_user'][donation.id_auth_user]
            
            body_message = """O projeto <b>"""+project_name.project_name+"""</b>, para o qual você fez uma doação
            não alcançou a meta. <br>
            Ele foi finalizado, e o valor de """+str(('%.2f' % donation.donation_value))+""" 
            foi creditado em sua conta.<br>"""
            title = "Você recebeu um crédito"
            db.user_messages.insert(message_title=title, message_content=body_message, id_auth_user=user_data.id, message_read=False)     

            status = "Estornada"
            db(db.project_donation.id == donation.id).update(status_text = status)

            get_user_credit = db(db.user_credit.id_auth_user == donation.id_auth_user).select()
            for credit in get_user_credit:
                user_credit = credit.credit_value             
            if not  get_user_credit:
                db.user_credit.insert(id_auth_user= user_data.id, credit_value=donation.donation_value)
            else:
                total_user_credit = user_credit
                new_credit = total_user_credit + donation.donation_value
                db(db.user_credit.id_auth_user == user_data.id).update(credit_value=new_credit)
        session.flash="Project Finalized With Successful."
        redirect(URL('adminpanel', 'list_expired_projects'))
       
    return locals()

@auth.requires_membership('admin')
def config_website_info():
    crud.settings.formstyle = 'divs'
    crud.messages.submit_button = T('Insert')
    meta_data = db(db.website_info.id > 0).select()
    for item in meta_data:
        data_id = item.id
    if not meta_data:
        form = crud.create(db.website_info, next=URL('adminpanel', 'config_website_info'))
    else:
        form = crud.update(db.website_info, data_id)
    form.element(_name='site_title')['_class'] = "span5"
    form.element(_name='meta_author')['_class'] = "span5"
    form.element(_name='meta_description')['_class'] = "span5"
    form.element(_name='meta_keywords')['_class'] = "span5"
    form.element(_name='google_analytics_id')['_class'] = "span5"
    form.element(_name='funding_time')['_class'] = "span2"
    form.element(_value='Inserir')['_class'] = "btn-warning"    
    return dict(form=form)

@auth.requires_membership('admin')
def config_website_terms():
    crud.settings.formstyle = 'divs'
    crud.messages.submit_button = T('Insert')
    meta_data = db(db.system_texts.id > 0).select()
    for item in meta_data:
        data_id = item.id
    if not meta_data:
        form = crud.create(db.system_texts, next=URL('adminpanel', 'config_website_terms'))
    else:
        form = crud.update(db.system_texts, data_id)
    form.element(_name='terms')['_class'] = "span11"

    return dict(form=form)

@auth.requires_membership('admin')
def config_website_email():
    crud.settings.formstyle = 'divs'
    crud.messages.submit_button = T('Insert')
    meta_data = db(db.email_settings.id > 0).select()
    for item in meta_data:
        data_id = item.id
    if not meta_data:
        form = crud.create(db.email_settings, next=URL('adminpanel', 'config_website_email'))
    else:
        form = crud.update(db.email_settings, data_id)
    form.element(_name='email_sender')['_class'] = "span5"
    form.element(_name='email_server')['_class'] = "span5"
    form.element(_name='email_server_port')['_class'] = "span5"
    form.element(_name='email_login')['_class'] = "span5"
    form.element(_name='email_pass')['_class'] = "span5"
    form.element(_name='email_pass')['_type'] = "password"
    form.element(_value='Inserir')['_class'] = "btn-warning"   
    return dict(form=form)

@auth.requires_membership('admin')
def config_website_payment():
    crud.settings.formstyle = 'divs'
    crud.messages.submit_button = T('Insert')
    meta_data = db(db.payment_settings.id > 1).select()
    for item in meta_data:
        data_id = item.id
    if not meta_data:
        form = crud.create(db.payment_settings, next=URL('adminpanel', 'config_website_payment'))
    else:
        form = crud.update(db.payment_settings, data_id)
    form.element(_name='paypal_enable')['_class'] = "span3"
    form.element(_name='paypal_id')['_class'] = "span5"
    form.element(_name='paypal_send_url')['_class'] = "span5"
    form.element(_name='moip_enable')['_class'] = "span3"
    form.element(_name='moip_id')['_class'] = "span5"
    form.element(_name='moip_send_url')['_class'] = "span5"
    form.element(_value='Inserir')['_class'] = "btn-warning"   
    return dict(form=form)

@auth.requires_membership('admin')
def config_website_images():
    crud.settings.formstyle = 'divs'
    crud.settings.update_deletable = False
    img_data = db(db.website_images.id > 0).select()
    for item in img_data:
        img_id = item.id
    if not img_data:
        form_images = crud.create(db.website_images, next=URL('adminpanel', 'config_website_images'))
    else:
        form_images = crud.update(db.website_images, img_id)
    form_images.element(_value='Enviar')['_class'] = "btn-warning"
    return dict(form_images=form_images)
 
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

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())