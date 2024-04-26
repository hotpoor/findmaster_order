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
from controller import findmaster_category
from controller import findmaster_specification
from controller import findmaster_raw_materials
from controller import findmaster_packing
from controller import findmaster_tasting

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/api/demouser/create",findmaster_demouser.CreateUserAPIHandler),
        (r"/api/demouser/login",findmaster_demouser.LoginAPIHandler),
        (r"/api/demouser/logout",findmaster_demouser.LogoutAPIHandler),
        (r"/api/demouser/data",findmaster_demouser.DataAPIHandler),

        (r"/api/search/add_free", findmaster_search.SearchAddFreeAPIHandler),
        (r"/api/search/add", findmaster_search.SearchAddAPIHandler),
        (r"/api/search/list_more", findmaster_search.SearchListMoreAPIHandler),
        (r"/api/search/list_force", findmaster_search.SearchListForceAPIHandler),
        (r"/api/search/list", findmaster_search.SearchListAPIHandler),

        # product
        (r"/api/product/create", findmaster_product.CreateProductAPIHandler),
        (r"/api/product/list", findmaster_product.ListProductAPIHandler),
        (r"/api/product/update", findmaster_product.UpdateProductAPIHandler),
        (r"/api/product/del", findmaster_product.DelProductAPIHandler),
        # supplier
        (r"/api/supplier/create", findmaster_supplier.CreateSupplierAPIHandler),
        (r"/api/supplier/list", findmaster_supplier.ListSupplierAPIHandler),
        (r"/api/supplier/update", findmaster_supplier.UpdateSupplierAPIHandler),
        (r"/api/supplier/del", findmaster_supplier.DelSupplierAPIHandler),
        # category
        (r"/api/category/create", findmaster_category.CreateCategoryAPIHandler),
        (r"/api/category/list", findmaster_category.ListCategoryAPIHandler),
        (r"/api/category/update", findmaster_category.UpdateCategoryAPIHandler),
        (r"/api/category/del", findmaster_category.DelCategoryAPIHandler),
        # specification
        (r"/api/specification/create", findmaster_specification.CreateSpecificationAPIHandler),
        (r"/api/specification/list", findmaster_specification.ListSpecificationAPIHandler),
        (r"/api/specification/update", findmaster_specification.UpdateSpecificationAPIHandler),
        (r"/api/specification/del", findmaster_specification.DelSpecificationAPIHandler),
        # raw materials
        (r"/api/raw_materials/create", findmaster_raw_materials.CreateRawMaterialsAPIHandler),
        (r"/api/raw_materials/list", findmaster_raw_materials.ListRawMaterialsAPIHandler),
        (r"/api/raw_materials/update", findmaster_raw_materials.UpdateRawMaterialsAPIHandler),
        (r"/api/raw_materials/del", findmaster_raw_materials.DelRawMaterialsAPIHandler),
        # packing
        (r"/api/packing/create", findmaster_packing.CreatePackingAPIHandler),
        (r"/api/packing/list", findmaster_packing.ListPackingAPIHandler),
        (r"/api/packing/update", findmaster_packing.UpdatePackingAPIHandler),
        (r"/api/packing/del", findmaster_packing.DelPackingAPIHandler),
        # tasting
        (r"/api/tasting/create", findmaster_tasting.CreateTastingAPIHandler),
        (r"/api/tasting/list", findmaster_tasting.ListTastingAPIHandler),
        (r"/api/tasting/update", findmaster_tasting.UpdateTastingAPIHandler),
        (r"/api/tasting/del", findmaster_tasting.DelTastingAPIHandler),

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