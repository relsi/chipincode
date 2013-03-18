# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',check_reserved=['all'])
    #db = DAL('mysql://username:password@host/db',pool_size=10,check_reserved=['all'])
    #db = DAL('postgres://username:password@host/db',,pool_size=10,check_reserved=['all'])
    #db = DAL('mssql://username:password@host/db')
    #db = DAL('firebird://username:password')
    #db = DAL('oracle://username/password@db')
    #db = DAL('mongodb://username:password@host/db')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables

auth.settings.extra_fields['auth_user']= [
    Field("avatar", "upload", label=T('User avatar.')),
    Field("address", "string", label=T('Address.')),
    Field("u_city", "string", label=T('City.')),
    Field("u_state", "string", label=T('State.')),
    Field("zip", "string", label=T('Zip code.')),
    Field("phone", "string", label=T('Contact phone.')),
    Field("ein", "string", label=T('User EIN.')),
    Field("website", "string", label=T('Website.')),
    Field("facebook", "string", label=T('Facebook Profile.')),
    Field("twitter", "string", label=T('Twitter page.')),
    Field("about", "text", label=T('About user.')),
    Field('completed_registration','boolean',default=False)
]
auth.define_tables(username=True)
auth.settings.login_userfield = 'email'
auth.settings.on_failed_authorization = URL(c='default', f='not_autorized')

## configure email
mail = auth.settings.mailer

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# authentication with social media
if session.auth_with == 'facebook':
    import facebook_account
    auth.settings.login_form = facebook_account.FaceBookAccount(globals(), db)
        
#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

from datetime import *

#image for home
db.define_table("home_banner",
  Field("image", "upload", uploadfolder=request.folder+'uploads/website_images', autodelete=True, label=T('Home Banner.'))
)

#image for logo
db.define_table("logo_image",
  Field("image", "upload", uploadfolder=request.folder+'uploads/website_images', autodelete=True, label=T('Logo Image.'))
)

db.define_table("default_avatar",
  Field("image", "upload", uploadfolder=request.folder+'uploads/website_images', autodelete=True, label=T('Default Avatar.'))
)

db.define_table("anonymous_avatar",
  Field("image", "upload", uploadfolder=request.folder+'uploads/website_images', autodelete=True, label=T('Anonymous avatar.'))
)

db.define_table("default_image",
  Field("image", "upload", uploadfolder=request.folder+'uploads/website_images', autodelete=True, label=T('Default Image.'))
)

db.define_table("website_meta",
    Field('site_title', 'string', label=T('Website Title')),
    Field('meta_author', 'string', label=T('Website Author')),
    Field('meta_description', 'string', label=T('Website description')),
    Field('meta_keywords', 'string', label=T('Website keywords')),
    Field('google_analytics_id', 'string', label=T('Google Analytics id'))
 )

#project categories
db.define_table("project_categories",
    Field("category_name", "string", label=T('Category Name'))
)

#projects table
db.define_table("project",
    Field("project_name", "string", label=T('Name of the project.')),
    Field("project_slug", compute=lambda row: IS_SLUG()(row.project_name)[0]),
    Field("project_value", "double", label=T('Value of the project.')),
    Field("project_total_collected", "double", default=0.0, label=T('Value total collected.')),
    Field("project_total_donor", "integer", default=0, label=T('Total of donors.')),
    Field("id_category", db.project_categories, label=T('Project Category')),
    Field("description", "text", label=T('Description of the project.')),
    Field("short_description", "text", label=T('Short Description of the project.')),
    Field("website", "string", label=T('Website of the project.')),
    Field("facebook", "string", label=T('Facebook page of the project.')),
    Field("twitter", "string", label=T('Twitter account of the project.')),
    Field("short_url", "string", label=T('short_url.')),
    Field("video", "string", label=T('Video URL of the project.')),
    Field("image", "upload", uploadfolder=request.folder+'uploads/project_images', autodelete=True, label=T('Featured picture of the  project.')),
    Field("terms_of_use", "boolean", default=False, label=T('Terms of use of the Chip In Code Plataform')),
    Field("id_auth_user", db.auth_user, label=T('User owner of the project.')),
    Field("status", "boolean", default=False, label=T('Status of the project.')),
    Field("status_text", "string", default=T('Waiting for approval'), label=T('Status text.')),
    Field("goal", "boolean", default=False, label=T('Goal of the project.')),
    Field("finalized", "boolean", default=False, label=T('Project Finalized?')),
    Field("register_date", "date", default=date.today(), label=T('Register date of the project.')),
    Field("start_date", "date", default=date.today(), label=T('Start date of the project.')),
    Field("end_date", "date", default=date.today(), label=T('End date of the project.'))
)

db.project.project_value.requires = IS_NOT_EMPTY(error_message=T('Fill the project value.'))
db.project.project_name.requires = IS_LENGTH(maxsize=55, minsize=1, error_message=T('Please, enter a value from 1 to 55 characters'))
db.project.description.requires = IS_NOT_EMPTY(error_message=T('Fill the project description.'))
db.project.id_category.requires=IS_IN_DB(db, 'project_categories.id', ' %(category_name)s',  zero=T('--------------------- Select ---------------------'), error_message=T('Fill the project categories'))
db.project.website.requires =  IS_NULL_OR(IS_URL(error_message=T('It should be a url! eg. http://codeup.com.br')))
db.project.facebook.requires = IS_NULL_OR(IS_URL(error_message=T('It should be a url! eg. http://facebook.com/codeupstudio')))
db.project.video.requires =  IS_NULL_OR(IS_MATCH('[0-9]+', strict=True, error_message=T('It should be a number! eg. 33670166')))
db.project.short_description.requires = IS_LENGTH(maxsize=150, minsize=1, error_message=T('Please, enter a value from 1 to 140 characters'))
db.project.terms_of_use.requires = IS_NOT_EMPTY(error_message=T('Accept the terms to proceed.'))

db.define_table("system_texts",
    Field("terms", "text", default=None)
    )

#project donation
db.define_table("project_donation",
    Field("id_auth_user", "integer", label=T('User.')),
    Field("id_project", "integer", label=T('Project')),
    Field("id_project_rewards", "integer", label=T('Reward')),
    Field("donation_value", "double", label=T('Donation value.')),
    Field("status", "boolean", default=False, label=T('Donation status.')),
    Field("status_text", "string", label=T('Donation status text.')),
    Field("payment_gateway", "string", label=T('Donation gateway.')),
    Field("donation_date", "date", label=T('Donation date.')),
    Field("donation_visibility", "boolean", default=True, label=T('Donation visibility.'))
)

#project rewards
db.define_table("project_rewards",
    Field("id_auth_user", "integer", label=T('User.')),
    Field("id_project", "integer", label=T('Project')),
    Field("reward_value", "double", label=T('Reward value.')),
    Field("reward_description", "text", label=T('Reward description.'))
)

#user credits
db.define_table("user_credit",
    Field("id_auth_user", "integer", label=T('User.')),
    Field("credit_value", "double", label=T('Credit value.'))
)

#user messages
db.define_table("user_messages",
    Field("id_auth_user", "integer", label=T('User')),
    Field("message_title", "string", label=T('Title')),
    Field("message_content", "text", label=T('Message')),
    Field("message_read", "boolean", default=False),
)

#project updates
db.define_table("project_updates",
    Field("id_project", "integer", label=T('Project')),
    Field("id_auth_user", "integer", label=T('User.')),
    Field("title", "string", label=T('Title.')),
    Field("update_content", "text", label=T('Content.'))
)

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
