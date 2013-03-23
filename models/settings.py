# -*- coding: utf-8 -*-
#########################################################################
## APP Settings
#########################################################################

verify_install = db(db.system_install.id > 0).select()
if not verify_install:
	db.system_install.insert(status= False)
	redirect(URL('install', 'index'))

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

website_images = db(db.website_images.id > 0).select()

if not website_images:
		logo = URL('static', 'images/logo.png')
		banner = URL('static', '14.png')
		avatar = URL('static', 'images/default_avatar.png')
		anonymous = URL('static', 'images/anonymous_avatar.png')
		image = URL('static', 'images/default_image.png')
else:
	
	for img in website_images:
		if not img.logo_image:
			logo = URL('static', 'images/logo.png')
		else:
			logo = URL('download', args=img.logo_image or 'images/logo.png')
		if not img.home_banner:
			banner = URL('static', '14.png')
		else:
			banner = URL('download', args=img.home_banner)
		if  not img.default_avatar:
			avatar = URL('static', 'images/default_avatar.png')
		else:
			avatar = URL('download', args=img.default_avatar)
		if not img.anonymous_avatar:
			anonymous = URL('static', 'images/anonymous_avatar.png')
		else:
			anonymous = URL('download', args=img.anonymous_avatar)
		if not img.default_image:
			image = URL('static', 'images/default_image.png')
		else:
			image = URL('download', args=img.default_image)

response.logo = logo
response.banner = banner
default_avatar = avatar
anonymous_avatar = anonymous
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

payment_settings = db(db.payment_settings.id > 1).select()
if not payment_settings:
	p_enable = 0
	p_send_url = ''
	p_id = ''
	m_enable = 0
	m_send_url = ''
	m_id = ''
else:
	for p_settings in payment_settings:
		p_enable = p_settings.paypal_enable
		p_send_url = p_settings.paypal_send_url
		p_id = p_settings.paypal_id
		m_enable = p_settings.moip_enable
		m_send_url = p_settings.moip_send_url
		m_id = p_settings.moip_id

paypal_enable = p_enable
paypal_send_url = p_send_url
paypal_id = p_id
ipn_handler = URL(c='project', f='ipn', host=True, scheme=True)
paypal_return_url =  URL(c='project', f='paypal_return', args='paypal', host=True, scheme=True)

moip_enable = m_enable
moip_send_url = m_send_url
moip_id = m_id
nasp_url = URL(c='project', f='nasp', host=True, scheme=True)
moip_return_url =  URL(c='project', f='moip_return', host=True, scheme=True)

social_network = db(db.social_network.id >0).select()
