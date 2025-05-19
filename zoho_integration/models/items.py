from odoo import models,fields, api
import logging
_logger = logging.getLogger(__name__)

class Items(models.Model):
	_inherit = 'product.template'

	zoho_id = fields.Char("Zoho ID")
	is_zoho = fields.Boolean("Zoho ?")

	@api.model
	def create(self, vals):
		_logger.info(f'{vals}')
		z_uom = vals.pop('z_uom')
		_logger.info(f'{z_uom}')

		if z_uom:
			uom_id = self.uom_id.search([('name', '=', z_uom)])
			uom_id = uom_id.id if uom_id else False
			vals['uom_id'] = uom_id
		return super().create(vals)