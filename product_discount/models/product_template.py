from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    discount_percentage = fields.Float(
        string="Discount (%)", 
        help="Set the discount percentage for this product.",
        default=0.0
    )

    discounted_price = fields.Float(
        string="Discounted Price", 
        compute="_compute_discounted_price", 
        store=True
    )

    @api.depends('list_price', 'discount_percentage')
    def _compute_discounted_price(self):
        for product in self:
            if product.discount_percentage > 0:
                product.discounted_price = product.list_price * (1 - product.discount_percentage / 100)
            else:
                product.discounted_price = product.list_price

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, vals):
        """
        Override create to ensure the discounted price is set.
        """
        if 'product_id' in vals:
            product = self.env['product.product'].browse(vals['product_id'])
            # Check for discount and apply the discounted price
            if product.discount_percentage > 0:
                vals['price_unit'] = product.list_price * (1 - product.discount_percentage / 100)
            else:
                vals['price_unit'] = product.list_price
        return super(SaleOrderLine, self).create(vals)

    def write(self, vals):
        """
        Override write to ensure the discounted price is not reset during updates.
        """
        for line in self:
            product = self.env['product.product'].browse(
                vals.get('product_id', line.product_id.id)
            )
            # Check if the product has a discount and update the price_unit
            if product.discount_percentage > 0:
                vals['price_unit'] = product.list_price * (1 - product.discount_percentage / 100)
            else:
                vals['price_unit'] = product.list_price

        return super(SaleOrderLine, self).write(vals)

