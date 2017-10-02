# -*- coding: utf-8 -*-

from openerp import models, fields, api
import inspect
import pprint
import os
import tempfile
import shutil
import errno
import logging
_logger = logging.getLogger(__name__)
import subprocess

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
        def child_dependency(children):
            res = self.env['product.product']
            for child in children:
                if not child.dependent_product_ids:
                    continue
                res += child.dependent_product_ids
                res += child_dependency(child.dependent_product_ids)
            return res
        for product in self:
            ret_val[product.id] = product.dependent_product_ids
            if product.dependent_product_ids:
                ret_val[product.id] += child_dependency(product.dependent_product_ids)
        return ret_val

    @api.multi
    def generate_zip_file(self):
        for product in self:
            tmpdir = tempfile.mkdtemp()
            dependent_product_ids = product.create_dependency_list()[product.id]
            for dependent_product in dependent_product_ids:
                p1 = subprocess.Popen(['cp','-r', dependent_product.module_path, tmpdir], stdout=subprocess.PIPE)
            p1 = subprocess.Popen(['cp','-r', product.module_path, tmpdir], stdout=subprocess.PIPE)
            #createzip of folder
            tmpzipfile = os.path.join(tmpdir,self.name)
            shutil.make_archive(tmpzipfile, 'zip', tmpdir)
            with open(tmpzipfile, "rb") as fileobj:
                try:
                    data_encode = base64.encodestring(fileobj.read())
                    attachment_id = attachment_obj.create({'datas': data_encode,
                                                   'datas_fname': tmpzipfile,
                                                   'type': 'binary',
                                                   'name': tmpzipfile,
                                                   'res_model': self._name,
                                                   'product_downloadable': True,
                                                    })
                except:
                    _logger.info('Error reading tmp Zipfile %s' % tmpzipfile)
            try:
                shutil.rmtree(tmpdir)
            except Exception as exc:
                _logger.warning('Could not remove Tempdir %s, Errormsg %s' % (tmpdir, exc.message))

    def copyfolder(self, src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)



ProductProduct()



