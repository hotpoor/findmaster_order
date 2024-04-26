import asyncio
import tornado

from setting import settings
from setting import conn

from controller import auth
from controller import findmaster_order
from controller import findmaster_demouser
from controller import findmaster_product
from controller import findmaster_supplier
from controller import findmaster_search
from controller import findmaster_file

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([

        (r"/api/demouser/create",findmaster_demouser.CreateUserAPIHandler),
        (r"/api/demouser/login",findmaster_demouser.LoginAPIHandler),
        (r"/api/demouser/logout",findmaster_demouser.LogoutAPIHandler),
        (r"/api/demouser/data",findmaster_demouser.DataAPIHandler),

        (r"/home/demouser/orders",findmaster_demouser.OrdersHomeHandler),


        (r"/api/file/demouser/check",findmaster_file.CheckDemouserFileAPIHandler),
        (r"/api/file/demouser/add",findmaster_file.AddDemouserFileAPIHandler),

        (r"/api/search/add_free", findmaster_search.SearchAddFreeAPIHandler),
        (r"/api/search/add", findmaster_search.SearchAddAPIHandler),
        (r"/api/search/list_more", findmaster_search.SearchListMoreAPIHandler),
        (r"/api/search/list_force", findmaster_search.SearchListForceAPIHandler),
        (r"/api/search/list", findmaster_search.SearchListAPIHandler),

        (r"/api/product/create", findmaster_product.CreateProductAPIHandler),
        (r"/api/supplier/create", findmaster_supplier.CreateSupplierAPIHandler),

        (r"/api/supplier/list_test2", findmaster_supplier.ListTest2SupplierAPIHandler),
        (r"/api/supplier/list_test", findmaster_supplier.ListTestSupplierAPIHandler),
        (r"/api/supplier/list", findmaster_supplier.ListSupplierAPIHandler),

        (r"/api/supplier/update", findmaster_supplier.UpdateSupplierAPIHandler),
        (r"/api/supplier/del", findmaster_supplier.DelSupplierAPIHandler),
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