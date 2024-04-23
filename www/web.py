import asyncio
import tornado

from setting import settings
from setting import conn

from controller import auth
from controller import findmaster_order
from controller import findmaster_demouser

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/api/demouser/create",findmaster_demouser.CreateUserAPIHandler),
        (r"/api/order/del",findmaster_order.DelOrderAPIHandler),
        (r"/api/order/update",findmaster_order.UpdateOrderAPIHandler),
        (r"/api/order/create",findmaster_order.CreateOrderAPIHandler),
        (r"/api/order/list",findmaster_order.ListOrderAPIHandler),
        (r"/api/data/json",findmaster_order.JsonDataAPIHandler),
        (r"/", MainHandler),
    ],**settings)

async def main():
    app = make_app()
    app.listen(8100)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())