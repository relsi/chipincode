# -*- coding: utf-8 -*-
def index():
    #donation_sum = db.project_donation.donation_value.sum()
    random_projects = db((db.project.status == True)&(db.project.end_date > date.today())).select(
        db.auth_user.ALL,
        db.project.ALL,
        left=[
            db.auth_user.on(db.auth_user.id == db.project.id_auth_user)
        ],
        limitby=(0,4), 
        orderby='<random>'
    )

    projects = []
    for item in random_projects:
        #donations=db(db.project_donation.id_project == item.project.id).select(donation_sum).first()[donation_sum] or 0
        donations = item.project.project_total_collected or 0
        percent = int((donations*100)/item.project.project_value)      
        remaining_days = item.project.end_date - date.today()
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
                              <p class="details-author">"""+T('by ')+"""  """+item.auth_user.first_name+""" """+item.auth_user.last_name+"""</p>
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
                                    """+T('R$')+""" """+str(('%.2f' %donations))+"""<br /><span>"""+T('Collected')+"""</span>
                                    </p>
                                </li>
                                <li>
                                    <p>"""+str(percent)+"""%<br /> <span>"""+T('Achieved')+"""</span></p>
                                </li>
                                <li>
                                    <p>"""+str(remaining_days.days)+""" """+T('days')+"""<br /> <span>"""+T('Left')+"""</span></p>
                                </li>
                              </ul>
                          </div>                  
                      </div>""")

    finishing_projects = db((db.project.status == True)&(db.project.end_date > date.today())).select(
        db.auth_user.ALL,
        db.project.ALL,
        left=[
            db.auth_user.on(db.auth_user.id == db.project.id_auth_user)
        ],
        limitby=(0,4), 
        orderby='<random>'
    )

    final_projects = []
    for f_item in finishing_projects:
        f_donations = f_item.project.project_total_collected or 0
        f_percent = int((f_donations*100)/f_item.project.project_value)      
        f_remaining_days = f_item.project.end_date - date.today()
        if f_remaining_days.days <= 5:
          final_projects, final_projects.append("""
                   <div class="span3 well">
                        <div class="details">
                            <a href='"""+URL(c='project', f='show', args=[f_item.project.id, f_item.project.project_slug])+"""' title='"""+f_item.project.project_name+"""'>
                                <img src='"""+URL('download',args=f_item.project.image)+"""' alt='"""+f_item.project.project_name+"""'>  
                            </a>
                            <h4>
                              <a href='"""+URL(c='project', f='show', args=[f_item.project.id, f_item.project.project_slug])+"""' title='"""+f_item.project.project_name+"""'>
                                """+f_item.project.project_name+"""
                              </a>
                            </h4>
                            <p class="details-author">"""+T('by ')+""" """+f_item.auth_user.first_name+""" """+f_item.auth_user.last_name+"""</p>
                            <p>
                              """+f_item.project.short_description+"""
                            </p>
                            <p class="details-author">"""+f_item.auth_user.u_city+"""/"""+f_item.auth_user.u_state+"""</p>
                            <div class="progress">
                              <div class="bar bar-warning" style="width: """+str(f_percent)+"""%;"></div>     
                            </div>
                            <ul>
                              <li>
                                  <p> 
                                  """+T('R$')+""" """+str(('%.2f' %f_donations))+"""<br /><span>"""+T('Collected')+"""</span>
                                  </p>
                              </li>
                              <li>
                                  <p>"""+str(f_percent)+"""%<br /> <span>"""+T('Achieved')+"""</span></p>
                              </li>
                              <li>
                                  <p>"""+str(f_remaining_days.days)+""" """+T('days')+"""<br /> <span>"""+T('left')+"""</span></p>
                              </li>
                            </ul>
                        </div>                  
                    </div>""")

    return dict(projects=projects, final_projects=final_projects)

def contact():
    if request.vars:
        name = request.vars.name
        email = request.vars.email
        message = request.vars.message
        subject = request.vars.subject
        body = '<html>'+T("Data Sender")+'<br><strong>'+T("Name")+'</strong>: '+name+'<br /><strong>'+T("Email")+'</strong>: '+email+'<br /><strong>'+T("Message")+'</strong>: '+message+'</html>'
        mail.send(response.projects_email, subject, body)
        response.flash = T("Email sent successfully")
    return locals()

def user():
    """
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """

    form_login = auth()
    form_login.element(_name="password")["_class"] = "span9"
    form_login.element(_name="email")["_class"] = "span9"
    
    form_register = auth.register()
    form_register.element(_name="password")["_id"] = "password"
    form_register.element(_name="email")["_id"] = "user_email"
    form_register.element(_name="email")['_class'] = "span9"
    form_register.element(_name="password")['_class'] = "span9"
    form_register.element(_name="first_name")['_class'] = "span9"
    form_register.element(_name="last_name")['_class'] = "span9"
    form_register.element(_name="password_two")['_class'] = "span9"

    return dict(form_login=form_login, form_register=form_register)


def not_autorized():
    return locals()

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

def login_fb():
    if request.vars['social_media'] == 'facebook':
        session.auth_with = 'facebook'
    redirect(URL(c='user', f='profile'))
