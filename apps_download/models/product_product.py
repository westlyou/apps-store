# -*- coding: utf-8 -*-

import os
import tempfile
import shutil
import logging
import base64
import subprocess
import time
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    dependent_product_ids = fields.Many2many(
        'product.product', 'prto_validateoduct_dependent_rel',
        'src_id', 'dest_id', string='Dependent Products'
    )
    module_path = fields.Char('Module Path')

    @api.constrains('dependent_product_ids')
    def check_dependent_recursion(self):
        for product in self:
            def child_dependency_check(product_dependent_ids, children):
                res = self.env['product.product']
                for child in children:
                    if not child.dependent_product_ids:
                        continue
                    if child in product_dependent_ids:
                        raise ValidationError(
                            _('Error: You cannot create recursive dependency.')
                        )
                    product_dependent_ids += child
                    child_dependency_check(product_dependent_ids,
                                           child.dependent_product_ids)
                return res

            child_dependency_check(product, product.dependent_product_ids)

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
                ret_val[product.id] += child_dependency(
                    product.dependent_product_ids)
        return ret_val

    @api.multi
    def generate_zip_file(self):
        for product in self:
            if not product.module_path:
                continue
            tmpdir = tempfile.mkdtemp()
            tmpdir_2 = tempfile.mkdtemp()
            dependent_products = product.create_dependency_list()
            dependent_products = dependent_products[product.id]
            for dependent_product in dependent_products:
                if not dependent_product.module_path:
                    continue
                subprocess.Popen(['cp', '-r', dependent_product.module_path,
                                  tmpdir], stdout=subprocess.PIPE)
            subprocess.Popen(['cp', '-r', product.module_path, tmpdir],
                             stdout=subprocess.PIPE)
            time_value = time.strftime(
                '_%y%m%d_%H%M%S')

            tmp_zip_file = os.path.join(tmpdir_2, product.name) + time_value
            shutil.make_archive(tmp_zip_file, 'zip', tmpdir)
            tmp_zip_file = '%s.zip' % tmp_zip_file
            with open(tmp_zip_file, "rb") as file_obj:
                try:
                    data_encode = base64.encodestring(file_obj.read())
                    self.env['ir.attachment'].create({
                        'datas': data_encode,
                        'datas_fname': tmp_zip_file,
                        'type': 'binary',
                        'name': product.name + time_value + '.zip',
                        'res_model': product._name,
                        'res_id': product.id,
                        'product_downloadable': True,
                    })
                except:
                    _logger.error('Error creating attachment %s' %
                                  tmp_zip_file)
            try:
                shutil.rmtree(tmpdir)
            except OSError as exc:
                _logger.warning('Could not remove Tempdir %s, Errormsg %s' % (
                    tmpdir, exc.message))
            try:
                shutil.rmtree(tmpdir_2)
            except OSError as exc:
                _logger.warning('Could not remove Tempdir 2 %s, Errormsg %s' % (
                    tmpdir, exc.message))

    @api.model
    def generate_zip_file_batch(self):
        self.search([]).generate_zip_file()
