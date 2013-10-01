from handlers import *

def get_handlers_urls():
    return [
            (r"/", IndexHandler),
            (r'/ws', SocketHandler),
            (r'/api', ApiHandler),
        ]
