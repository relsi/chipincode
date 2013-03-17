# -*- coding: utf-8 -*-
def index():
    redirect(URL(c='default', f='index'))
    pass

def show():
    project_id = request.args(0) or redirect(URL('project', 'index'))
    project_slug = request.args(1)

    project_details = db((db.project.id == project_id)&(db.project.project_slug == project_slug)).select(
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
    
@auth.requires_login()
def project_send():
    if auth.user and not auth.user.completed_registration:
        redirect(URL(c='user', f='profile_complete'))
    else:
        terms = db(db.system_texts.id > 0).select()
        for item in terms:
            terms_of_use = item.terms
        db.project.start_date.readable = db.project.start_date.writable=False
        db.project.end_date.readable = db.project.end_date.writable=False
        form_project = SQLFORM(db.project)
        form_project.element(_name='id_category')['_class'] = "span7"
        form_project.element(_name='project_value')['_class'] = "span7 format_value"
        form_project.element(_name='project_value')['_placeholder'] = T("eg. 4000 (only numbers)")
        form_project.element(_name='description')['_class'] = "span9 textarea-send"
        form_project.element(_name='description')['_placeholder'] = T("Insert here the description of your project for us, what will you do with the money raised, etc.. Don't worry, you can improve it later")
        form_project.element(_name='short_description')['_class'] = "span7 short_description"
        form_project.element(_name='short_description')['_rows'] = "3"
        form_project.element(_name='short_description')['_placeholder'] = T("(max 140 characters)")
        form_project.element(_name='website')['_class'] = "span7"
        form_project.element(_name='website')['_placeholder'] = T("eg. http://codeup.com.br")
        form_project.element(_name='facebook')['_class'] = "span7"
        form_project.element(_name='facebook')['_placeholder'] = T("eg. http://facebook.com/codeupstudio")
        form_project.element(_name='twitter')['_class'] = "span7"
        form_project.element(_name='twitter')['_placeholder'] = T("eg. @codeupstudio")
        form_project.element(_name='video')['_class'] = "span7"
        form_project.element(_name='video')['_placeholder'] = T("eg. 33670166")
        form_project.element(_name='image')['_class'] = "span7"
        form_project.element(_name='project_name')['_class'] = "span7"
        form_project.element(_name='project_name')['_placeholder'] = T("A cool name here! (max 55 characters)")
        form_project.element(_name='status_text')['_type'] = "hidden"
        form_project.element(_name='register_date')['_type'] = "hidden"

        #goo.gl short url 
        #tks to http://axiacore.com/blog/2012/06/usar-toggl-desde-python-para-acortar-urls/
        import urllib2
        from gluon.contrib import simplejson   
        def shorturl(urltoshorten):
            try:
                apiurl = "https://www.googleapis.com/urlshortener/v1/url"
                req = urllib2.Request(apiurl,
                headers={'Content-Type': 'application/json'},
                data='{{"longUrl": "{0}"}}'.format(urltoshorten))
                shorturl = simplejson.loads(urllib2.urlopen(req).read())['id']
            except:
                shorturl = urltoshorten
            return shorturl

        if form_project.process(session=None, formname='None').accepted:
            update_url = db(db.project.id == form_project.vars.id).select()
            for item in update_url:
                project_slug = item.project_slug
            db(db.project.id == form_project.vars.id).update(
                short_url = shorturl(URL(c='project', f='show', args=[form_project.vars.id, project_slug], host=True, scheme=True))
                ) 
            session.flash = T("Project Registered Successfully!")
            #send confirmation email to user, after send project
            body_user ="""<html>
                """+T('His project was registered and is awaiting approval.')+"""<br>
               """+T('You can track the status of your project, and register rewards, accessing your user profile')+""": """+URL(c='user', f='profile',scheme=True,host=True)+"""</html>"""
            mail.send(auth.user.email, T('His project was registered.'), body_user)
            #send email to Chip In Code admin, after user send project
            body_admin ="""<html>
                """+T('A new project was registered.')+""":<br>
                <strong>"""+T('Project')+""": </strong>"""+request.post_vars.project_name+"""<br>
                <strong>"""+T('User')+""": </strong>"""+auth.user.first_name+""" """+auth.user.last_name+"""<br>
                <strong>"""+T('View')+""": </strong> """+URL(c='adminpanel',f='show_project',args=form_project.vars.id,scheme=True,host=True)+"""</html>"""
            mail.send(response.projects_email, T('A new project was registered.'), body_admin)
            redirect(URL(c='user', f='profile'))
        
        elif form_project.errors:
            response.flash = T("Please, check the form errors!")

        return dict(form_project = form_project, terms_of_use=terms_of_use)

def show_category():
    donation_sum = db.project_donation.donation_value.sum()

    random_projects = db((db.project.id_category == request.args(0))& (db.project.status == True)).select(
        db.auth_user.ALL,
        db.project.ALL,
        db.project_categories.ALL,
        left=[
            db.auth_user.on(db.auth_user.id == db.project.id_auth_user),
            db.project_categories.on(db.project_categories.id == db.project.id_category)
        ]
    )

    projects = []
    for item in random_projects:
        donations=db(db.project_donation.id_project == item.project.id).select(donation_sum).first()[donation_sum] or 0
        percent = int((donations*100)/item.project.project_value)      
        remaining_days = item.project.end_date - date.today()
        category_name = item.project_categories.category_name or ''
        projects, projects.append("""
                 <div class="span3 well">
                      <div class="details">
                          <a href='"""+URL(c='project', f='show', args=[item.project.id, item.project.project_slug])+"""' title='"""+item.project.project_name+"""'>
                              <img src='"""+URL('download',args=item.project.image)+"""' alt='"""+item.project.project_name+"""'>  
                          </a>
                          <h4>
                            <a href='"""+URL(c='project', f='show', args=[item.project.id, item.project.project_slug])+"""' title='"""+item.project.project_name+"""'>
                              """+item.project.project_name+"""
                            </a>
                          </h4>
                          <p class="details-author">"""+T('by ')+""" """+item.auth_user.first_name+""" """+item.auth_user.last_name+"""</p>
                          <p>
                            """+item.project.short_description+"""
                          </p>
                          <p class="details-author">"""+item.auth_user.u_city+"""/"""+item.auth_user.u_state+"""</p>
                          <div class="progress">
                            <div class="bar bar-warning" style="width: """+str(percent)+"""%;"></div>     
                          </div>
                          <ul>
                            <li>
                                <p> 
                                """+T('R$')+""" """+str(('%.2f' % donations) or 0)+"""<br /><span>"""+T('Collected')+"""</span>
                                </p>
                            </li>
                            <li>
                                <p>"""+str(percent)+"""%<br /><span>"""+T('Achieved')+"""</span></p>
                            </li>
                            <li>
                                <p>"""+str(remaining_days.days)+""" """+T('days')+"""<br /><span>"""+T('Left')+"""</span></p>
                            </li>
                          </ul>
                      </div>                  
                  </div>""")
    
    if not projects: category_name = ''
    return dict(projects=projects, category_name=category_name)

@auth.requires_login()
def donate():
    id_project = request.args(0) or redirect(URL(c='default', f='index'))
    project_rewards = db(db.project_rewards.id_project == id_project).select()
    project_info = db(db.project.id == id_project).select(
        db.project.ALL,
        db.auth_user.ALL,
        left=[
            db.auth_user.on(db.auth_user.id == db.project.id_auth_user),
        ]
    )
    if request.vars:
        session.payment_data = request.vars
        redirect(URL(c='project', f='payment'))

    return dict(project_rewards=project_rewards, project_info=project_info)

@auth.requires_login()
def payment():
    if not session.payment_data:
        redirect(URL(c='default', f='index'))
    else:
        user_credits = db(db.user_credit.id_auth_user == session.payment_data.id_auth_user).select()
        if not user_credits:
            total_credits = 0.0
        else:
            for item in user_credits:
                total_credits = item.credit_value or 0.0

    if request.vars:
        session.payment_data = request.vars
        if request.vars.payment_gateway == 'credits':
            credit_balance = total_credits - float(request.vars.value)
            db(db.user_credit.id_auth_user == session.payment_data.id_auth_user).update(
                credit_value = credit_balance
            )
            get_project_data = db(db.project.id == request.vars.id_project).select()
            for data in get_project_data:
                total_collected = data.project_total_collected or 0.00
                total_donor = data.project_total_donor or 0.00
                db(db.project.id == data.id).update(
                    project_total_collected = float(request.vars.value) + total_collected,
                    project_total_donor = total_donor + 1
                )           
            status_text = "Credited"
            status = True
            db.project_donation.insert(
                id_auth_user=request.vars.id_auth_user,
                id_project=request.vars.id_project,
                id_project_rewards=request.vars.id_project_rewards,
                donation_value=request.vars.value,
                status_text=status_text,
                status=status,
                payment_gateway=request.vars.payment_gateway,
                donation_date=date.today(),
                donation_visibility=request.vars.donation_visibility
            )
            session.flash = T("Donation registered successfully")
            redirect(URL(c='user', f='profile'))
        elif request.vars.payment_gateway == 'paypal':
            status_text = "Waiting gateway confirmation"
            status = False
            donate_id = db.project_donation.insert(
                id_auth_user=request.vars.id_auth_user,
                id_project=request.vars.id_project,
                id_project_rewards=request.vars.id_project_rewards,
                donation_value=request.vars.value,
                status_text=status_text,
                status=status,
                payment_gateway=request.vars.payment_gateway,
                donation_date=date.today(),
                donation_visibility=request.vars.donation_visibility
            )
            session.donate_id = donate_id
            response.flash = T("Donation registered successfully")
            redirect(URL(c='project', f='redirect_paypal'))
        elif request.vars.payment_gateway == 'moip':
            status_text = "Waiting gateway confirmation"
            status = False
            donate_id = db.project_donation.insert(
                id_auth_user=request.vars.id_auth_user,
                id_project=request.vars.id_project,
                id_project_rewards=request.vars.id_project_rewards,
                donation_value=request.vars.value,
                status_text=status_text,
                status=status,
                payment_gateway=request.vars.payment_gateway,
                donation_date=date.today(),
                donation_visibility=request.vars.donation_visibility
            )
            session.donate_id = donate_id
            response.flash = T("Donation registered successfully")
            redirect(URL(c='project', f='redirect_moip'))
    return locals()
    
def redirect_moip():
    return locals()
    
def moip_return():
    return locals()
    
@auth.requires_login()
def redirect_paypal():
    return locals()

def nasp():
    if not request.vars:
        redirect(URL(c='default', f='index'))
    else:
        #TODO: Verificar a necessidade de implementar os outros retornos
        if request.vars.status_pagamento == '4':
            db(db.project_donation.id == request.vars.id_transacao).update(
                status = True,
                status_text = "Creditado"
                )
            get_project_data = db(db.project_donation.id == request.vars.id_transacao).select()
            for data in get_project_data:
                update_project_data = db(db.project.id == data.id_project).select()
                for item in update_project_data:
                    donation_amount = item.project_total_collected or 0.00
                    total_backers = item.project_total_donor or 0
                    db(db.project.id == item.id).update(
                        project_total_collected = float(request.vars.valor[:-2]) + donation_amount,
                        project_total_donor = total_backers + 1
                 )
   
            return 'OK'
        else:
            raise HTTP(404)

def paypal_return():
    if request.args(0) == 'paypal':
        if request.vars.payment_status == 'Completed':
            message = "<p class='alert alert-success'>"+T('Thank you, for your donation.')+"</p>"
        else:
            db(db.project_donation.id == request.vars.invoice).update(
                status_text = request.vars.payment_status 
                )
            message = "<p class='alert alert-error'>Ooooops! The paypal sent the following warning "+request.vars.payment_status+".</p>"            
    else:
        redirect(URL(c='default', f='index'))

    return locals()

def ipn():
    import json
    if request.vars.payment_status == 'Completed':
        db(db.project_donation.id == request.vars.item_number).update(
            status = True,
            status_text = "Credited" 
            )
        get_project_data = db(db.project.id == request.vars.invoice).select()
        for data in get_project_data:
            db(db.project.id == data.id).update(
                                                project_total_collected = float(request.vars.payment_gross) + data.project_total_collected,
                                                project_total_donor = data.project_total_donor + 1
                                                ) 
    else:
        db(db.project_donation.id == request.vars.invoice).update(
            status_text = request.vars.payment_status 
            )
    return json.dumps(request.vars)

@auth.requires_login()
def project_edit():
    db.project.id_auth_user.readable = db.project.id_auth_user.writable = False 
    db.project.status_text.readable = db.project.status_text.writable=False
    db.project.project_value.readable = db.project.project_value.writable=False
    db.project.terms_of_use.readable = db.project.terms_of_use.writable=False
    db.project.status.readable = db.project.status.writable=False
    db.project.register_date.readable = db.project.register_date.writable=False
    db.project.start_date.readable = db.project.start_date.writable=False
    db.project.end_date.readable = db.project.end_date.writable=False

    check_owner = db((db.project.id == request.args(0))&(db.project.id_auth_user == auth.user.id)).select()
    if not check_owner:
        redirect(URL(c='project', f='inform', args=request.args(0)))
    else:
        crud.messages.record_updated = T('Project Updated')
        form_edit = crud.update(db.project, request.args(0), next=URL(c='user', f='profile'))
        form_edit.element(_name='description')['_class'] = "span8"
        form_edit.element(_name='description')['_rows'] = "30"
        form_edit.element(_name='project_name')['_class'] = "span6"
        form_edit.element(_name='short_description')['_class'] = "span6"
        form_edit.element(_name='short_description')['_rows'] = "2"

        return dict(form_edit=form_edit)

@auth.requires_login()
def project_updates():
    check_owner = db((db.project.id == request.args(0))&(db.project.id_auth_user == auth.user.id)).select()
    if not check_owner:
        redirect(URL(c='project', f='inform', args=request.args(0)))
    else:
        crud.messages.record_created = T('Update Project Created')
        form_project_updates = crud.create(db.project_updates)
        form_project_updates.element(_name='update_content')['_class'] = "span12"
        form_project_updates.element(_name='title')['_class'] = "span6"
        form_project_updates.element(_name='update_content')['_rows'] = "30"
        project_updates = db(db.project_updates.id_project == request.args(0)).select(orderby=~db.project_updates.id)
        return dict(form_project_updates=form_project_updates, project_updates=project_updates)

@auth.requires_login()
def project_update_edit():
    check_owner = db((db.project.id == request.args(0))&(db.project.id_auth_user == auth.user.id)).select()
    if not check_owner:
        redirect(URL(c='project', f='inform', args=request.args(0)))
    else:
        crud.messages.record_updated = T('Content Updated')
        form_update_edit = crud.update(db.project_updates,request.args(1), next=URL(c='project', f='project_updates', args=request.args(0)))
        form_update_edit.element(_name='update_content')['_class'] = "span8"
        form_update_edit.element(_name='title')['_class'] = "span6"
        form_update_edit.element(_name='update_content')['_rows'] = "30"
        return dict(form_update_edit=form_update_edit)

@auth.requires_login()
def project_update_delete():
    check_owner = db((db.project.id == request.args(0))&(db.project.id_auth_user == auth.user.id)).select()
    if not check_owner:
        redirect(URL(c='project', f='inform', args=request.args(0)))
    else:
        crud.messages.record_deleted = T('Content Deleted')
        crud.delete(db.project_updates,request.args(1))

@auth.requires_login()
def project_rewards():
    check_owner = db((db.project.id == request.args(0))&(db.project.id_auth_user == auth.user.id)).select()
    if not check_owner:
        redirect(URL(c='project', f='inform', args=request.args(0)))
    else:
        crud.messages.record_created = T('Project reward Created')
        form_project_reward = crud.create(db.project_rewards)
        form_project_reward.element(_name='reward_value')['_class'] = "span2 format_value"
        form_project_reward.element(_name='reward_description')['_rows'] = "4"
        form_project_reward.element(_name='reward_description')['_class'] = "span4"
        project_rewards = db(db.project_rewards.id_project == request.args(0)).select(orderby=db.project_rewards.reward_value)
        return dict(form_project_reward=form_project_reward, project_rewards=project_rewards)

@auth.requires_login()
def project_reward_edit():
    check_owner = db((db.project.id == request.args(0))&(db.project.id_auth_user == auth.user.id)).select()
    if not check_owner:
        redirect(URL(c='project', f='inform', args=request.args(0)))
    else:
        crud.messages.record_updated = T('Project reward Updated')
        form_project_reward_edit = crud.update(db.project_rewards, request.args(1), next=URL(c='project', f='project_rewards', args=request.args(0)))
        form_project_reward_edit.element(_name='reward_value')['_class'] = "span2 format_value"
        form_project_reward_edit.element(_name='reward_description')['_rows'] = "4"
        form_project_reward_edit.element(_name='reward_description')['_class'] = "span4"
        return dict(form_project_reward_edit=form_project_reward_edit)

@auth.requires_login()
def project_reward_delete():
    check_owner = db((db.project.id == request.args(0))&(db.project.id_auth_user == auth.user.id)).select()
    if not check_owner:
        redirect(URL(c='project', f='inform', args=request.args(0)))
    else:
        crud.messages.record_deleted = T('Content Deleted')
        crud.delete(db.project_rewards,request.args(1), next=URL(c='project', f='project_rewards', args=request.args(0)))

def inform():
    #send inform email to Chip In Code admin
    body ="""<html>
        """+T('A user tried to change a project that does not belong to him')+""":<br>
        <strong>"""+T('Project')+""": </strong>"""+request.args(0)+"""<br>
        <strong>"""+T('User')+""": </strong>"""+auth.user.first_name+""" """+auth.user.last_name+"""<br>
        <strong>"""+T('View')+""": </strong> """+URL(c='adminpanel',f='show_project',args=request.args,scheme=True,host=True)+"""</html>"""
    mail.send(response.projects_email, T("Suspect Operation!"), body)

    return locals()

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

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