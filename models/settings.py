# -*- coding: utf-8 -*-
#########################################################################
## Customize your APP 
#########################################################################
## read more at http://dev.w3.org/html5/markup/meta.name.html
website_info = db(db.website_info.id > 0).select()
if not website_info:
	title = 'Chip in Code - Plataforma de Crowdfunding Open Source'
	author = 'CodeUp - Apps Studio - http://codeup.com.br <contato@codeup.com.br>'
	description = 'Chip in Code - Plataforma de Crowdfunding Open Source'
	keywords = 'web2py, python, Crowdfunding, Chip in Code, CodeUp'
	google_analytics_id = None
	site_funding_time = 30
else:
	for info in website_info:
		title = info.site_title or ''
		author = info.meta_author or ''
		description = info.meta_description or ''
		keywords = info.meta_keywords or ''
		google_analytics_id = info.google_analytics_id or ''
		site_funding_time = info.funding_time or 30

response.title = title
response.meta.author = author
response.meta.description = description
response.meta.keywords = keywords
response.meta.generator = 'Chip in Code'
response.google_analytics_id = google_analytics_id

funding_time = site_funding_time

website_logo = db(db.logo_image.id > 0).select()
if not website_logo:
	logo = URL('static', 'images/logo.png')
else:
	for logo in website_logo:
		logo = URL('download', args=logo.image)

response.logo = logo

home_banner = db(db.home_banner.id > 0).select()
if not home_banner:
	banner = URL('static', '14.png')
else:
	for banner_img in home_banner:
		banner = URL('download', args=banner_img.image)

response.banner = banner

default_avatar = db(db.default_avatar.id > 0).select()
if not default_avatar:
	avatar = URL('static', 'images/default_avatar.png')
else:
	for avatar_img in default_avatar:
		avatar = URL('download', args=avatar_img.image)

default_avatar = avatar

anonymous_avatar = db(db.anonymous_avatar.id > 0).select()
if not anonymous_avatar:
	anonymous = URL('static', 'images/anonymous_avatar.png')
else:
	for anonymous_img in anonymous_avatar:
		anonymous = URL('download', args=anonymous_img.image)

anonymous_avatar = anonymous

default_img = db(db.default_image.id > 0).select()
if not default_img:
	image = URL('static', 'images/default_image.png')
else:
	for img in default_img:
		image = URL('download', args=img.image)

default_image = image

email_settings = db(db.email_settings.id > 0).select()
if not email_settings:
	email_sender = ""
	email_server = ""
	email_port = ""
	email_login = ""
	email_pass = ""
else:
	for s_email in email_settings:
		email_sender = s_email.email_sender
		email_server = s_email.email_server
		email_port = str(s_email.email_server_port)
		email_login = s_email.email_login
		email_pass = s_email.email_pass

response.projects_email = email_sender
mail.settings.server = email_server+':'+email_port
mail.settings.sender = email_sender
mail.settings.login = email_login+':'+email_pass



#paypal configurations
paypal_enable = True
paypal_send_url = "https://www.sandbox.paypal.com/cgi-bin/webscr"
paypal_id = "DKGSERZBL6RKS"
ipn_handler = URL(c='project', f='ipn', host=True, scheme=True)
paypal_return_url =  URL(c='project', f='paypal_return', args='paypal', host=True, scheme=True)

#moip configurations
moip_enable = True
moip_send_url = "https://desenvolvedor.moip.com.br/sandbox/PagamentoMoIP.do"
moip_id = 'relsi'
nasp_url = URL(c='project', f='nasp', host=True, scheme=True)
moip_return_url =  URL(c='project', f='moip_return', host=True, scheme=True)