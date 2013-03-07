import os

import sae
import web
import message
urls = (
    '/get_message', 'message.get_message'
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

app = web.application(urls, globals()).wsgifunc()

application = sae.create_wsgi_app(app)