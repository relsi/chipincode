# -*- coding: utf-8 -*-
#########################################################################
## Customize your APP 
#########################################################################
## read more at http://dev.w3.org/html5/markup/meta.name.html
response.title = "Chip in Code - Plataforma de Crowdfunding Open Source"
response.meta.author = 'CodeUp - Apps Studio - http://codeup.com.br <contato@codeup.com.br>'
response.meta.description = 'Chip in Code - Plataforma de Crowdfunding Open Source'
response.meta.keywords = 'web2py, python, Crowdfunding, Chip in Code, CodeUp'
response.meta.generator = 'Web2py Web Framework'

#the defaults avatar image
default_avatar = URL('static', 'images/default_avatar.png')
anonymous_avatar = URL('static', 'images/anonymous_avatar.png')

## your http://google.com/analytics id
response.google_analytics_id = None

#email configuration
response.email_server = 'smtp.gmail.com:587'
response.email_sender = 'ussr_name@gmail.com'
response.email_login = 'user_name:password'

#the email that will receive notifications about registered projects
response.projects_email = "user_name@gmail.com"

#paypal configurations
paypal_enable = True
paypal_id = "YOUR-PAYPAL-ID"
ipn_handler = URL(c='project', f='ipn', host=True, scheme=True)
paypal_return_url =  URL(c='project', f='paypal_return', args='paypal', host=True, scheme=True)

#moip configurations
paypal_enable = True
moip_id = 'SEU-EMAIL-DO-MOIP'
nasp_url = URL(c='project', f='nasp', host=True, scheme=True)
moip_return_url =  URL(c='project', f='moip_return', host=True, scheme=True)
