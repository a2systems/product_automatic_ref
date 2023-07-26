from odoo import tools, models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class ProductCategory(models.Model):
    _inherit = 'product.category'

    def _compute_product_sequence_id(self):
        for rec in self:
            res = None
            categ = rec
            while categ:
                if categ.sequence_id:
                    res = categ.sequence_id.id
                    break
                else:
                    categ = categ.parent_id
            rec.product_sequence_id = res

    sequence_id = fields.Many2one('ir.sequence','Product Ref Sequence')
    product_sequence_id = fields.Many2one('ir.sequence','Computed Product Ref Sequence',compute=_compute_product_sequence_id)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        if vals.get('purchase_ok') and vals.get('categ_id'):
            categ_id = vals.get('categ_id')
            categ = self.env['product.category'].browse(categ_id)
            seq = categ.product_sequence_id
            if not seq:
                raise ValidationError('Please configure sequence in category')
            default_code = seq._next()
            vals['default_code'] = default_code
        return super(ProductTemplate, self).create(vals)
