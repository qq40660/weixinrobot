import os
import web
import message
urls = (
    '/get_message', 'message.get_message'
)

app = web.application(urls, globals())
app.run()
