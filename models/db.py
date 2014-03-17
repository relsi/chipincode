# -*- coding: utf-8 -*-


## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:

# request.requires_https()

# Set the database conection:


if request.is_local:
    db = DAL('sqlite://sto.sqlti',check_reserved=['all'])
else:
    db = DAL('sqlite://storage.sqlite',check_reserved=['all'])




#db = DAL('mysql://username:password@host/db',check_reserved=['all'])
#db = DAL('postgres://username:password@host/db',check_reserved=['all'])
#db = DAL('mssql://username:password@host/db')
#db = DAL('firebird://username:password')
#db = DAL('oracle://username/password@db')
#db = DAL('mongodb://username:password@host/db')

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
    Field("ssc", "string", label=T('User SSC (social security card).')),
    Field("website", "string", label=T('Website.')),
    Field("facebook", "string", label=T('Facebook Profile.')),
    Field("twitter", "string", label=T('Twitter page.')),
    Field("about", "text", label=T('About user.')),
    Field('completed_registration','boolean',default=False)
]
auth.define_tables(username=True)
auth.settings.login_userfield = 'email'
auth.settings.on_failed_authorization = URL(c='default', f='not_autorized')
auth.settings.logged_url = URL(c='user', f='profile')

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
## App tables
#########################################################################

from datetime import *

db.define_table("system_install",
  Field("status", "boolean", default=False)
)

db.define_table("website_images",
  Field("home_banner", "upload", uploadfolder=request.folder+'uploads/website_images', autodelete=True, label=T('Home Banner.')),
  Field("logo_image", "upload", uploadfolder=request.folder+'uploads/website_images', autodelete=True, label=T('Logo Image.')),
  Field("default_avatar", "upload", uploadfolder=request.folder+'uploads/website_images', autodelete=True, label=T('Default Avatar.')),
  Field("anonymous_avatar", "upload", uploadfolder=request.folder+'uploads/website_images', autodelete=True, label=T('Anonymous avatar.')),
  Field("default_image", "upload", uploadfolder=request.folder+'uploads/website_images', autodelete=True, label=T('Default Image.'))
)

db.define_table("website_info",
    Field('site_title', 'string', label=T('Website Title')),
    Field('meta_author', 'string', label=T('Website Author')),
    Field('meta_description', 'string', label=T('Website description')),
    Field('meta_keywords', 'string', label=T('Website keywords')),
    Field('google_analytics_id', 'string', label=T('Google Analytics id')),
    Field('funding_time', 'integer', label=T('Funding Time'))
 )

db.define_table("website_faq",
    Field('faq_question', 'string', label=T('F.A.Q Question')),
    Field('faq_answer', 'text', label=T('Website Answer'))
 )

db.define_table("email_settings",
    Field('email_sender', 'string', label=T('Website email')),
    Field('email_server', 'string', label=T('Email Server')),
    Field('email_server_port', 'integer', label=T('Email Server Port')),
    Field('email_login', 'string', label=T('Email Login')),
    Field('email_pass', 'string', label=T('Email Password'))
 )

db.define_table("social_network",
    Field('network_name', 'string', label=T('Network'), requires = IS_IN_SET([
        ('facebook',T('Facebook')),
        ('google',T('G+')),
        ('twitter',T('Twitter')),
        ('youtube',T('Youtube')),
        ('feed',T('Blog')),
        ('vimeo',T('Vimeo')),
            ])),
    Field('link_text', 'string', label=T('Link Description')),
    Field('link_url', 'string', label=T('Link URL')),
 )

db.define_table("payment_settings",
    Field('paypal_enable', 'integer', label=T('Enable Paypal'), requires = IS_IN_SET([('1',T('Enable')),('0',T('Disable'))])),
    Field('paypal_id', 'string', label=T('Paypal ID')),
    Field('paypal_send_url', 'string', label=T('Paypal URL')),
    Field('moip_enable', 'integer', label=T('Enable MoIP'), requires = IS_IN_SET([('1',T('Enable')),('0',T('Disable'))])),
    Field('moip_id', 'string', label=T('MoIP id')),
    Field('moip_send_url', 'string', label=T('MoIP URL'))
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
    Field("update_content", "text", label=T('Content.')),
    auth.signature
)

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
