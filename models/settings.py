# -*- coding: utf-8 -*-
#########################################################################
## Customize your APP 
#########################################################################
## read more at http://dev.w3.org/html5/markup/meta.name.html
website_meta = db(db.website_meta.id > 0).select()
if not website_meta:
	title = 'Chip in Code - Plataforma de Crowdfunding Open Source'
	author = 'CodeUp - Apps Studio - http://codeup.com.br <contato@codeup.com.br>'
	description = 'Chip in Code - Plataforma de Crowdfunding Open Source'
	keywords = 'web2py, python, Crowdfunding, Chip in Code, CodeUp'
else:
	for meta in website_meta:
		title = meta.site_title or ''
		author = meta.meta_author or ''
		description = meta.meta_description or ''
		keywords = meta.meta_keywords or ''

response.title = title
response.meta.author = author
response.meta.description = description
response.meta.keywords = keywords
response.meta.generator = 'Chip in Code'

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

#funding time of the projects
funding_time = 30

## your http://google.com/analytics id
response.google_analytics_id = None

#the email that will receive notifications about registered projects
response.projects_email = "chipincode@gmail.com"

#email configuration
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'chipincode@gmail.com'
mail.settings.login = 'chipincode:B612cseth'

#paypal configurations
paypal_enable = True
paypal_id = "DKGSERZBL6RKS"
ipn_handler = URL(c='project', f='ipn', host=True, scheme=True)
paypal_return_url =  URL(c='project', f='paypal_return', args='paypal', host=True, scheme=True)

#moip configurations
moip_enable = True
moip_id = 'relsi'
nasp_url = URL(c='project', f='nasp', host=True, scheme=True)
moip_return_url =  URL(c='project', f='moip_return', host=True, scheme=True)