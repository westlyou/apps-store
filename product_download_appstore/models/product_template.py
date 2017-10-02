# -*- coding: utf-8 -*-


from openerp import models, fields, api
import inspect
import pprint

class ProductTemplate(models.Model):
    _inherit = 'product.template'



ProductTemplate()


class ProductProduct(models.Model):
    _inherit = 'product.product'

    dependent_product_ids = fields.Many2many('product.product', 'prto_validateoduct_dependent_rel', 'src_id', 'dest_id', string='Dependent Products')
    module_path = fields.Char('Module Path')

    @api.multi
    def create_dependency_list(self):
        ret_val = {}
        def child_dependancy(children):
            res = self.env['product.product']
            for child in children:
                if not child.dependent_product_ids:
                    continue
                res += child.dependent_product_ids
                res += child_dependancy(child.dependent_product_ids)
            return res
        for product in self:
            ret_val[product.id] = product.dependent_product_ids
            if product.dependent_product_ids:
                ret_val[product.id] += child_dependancy(product.dependent_product_ids)
        return ret_val
    @api.multi
    def generate_zip_file(self):
        for product in self:
            dependent_product_ids = product.create_dependency_list()[product.id]

ProductProduct()

