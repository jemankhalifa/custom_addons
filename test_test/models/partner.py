from odoo import models, fields, api

class CrmDeal(models.Model):
    _name = 'crm.deal'
    _description = 'CRM Deal'
    _order = 'sequence'

    description = fields.Char(string='Description', required=True)
    sequence = fields.Char(string='Sequence', required=True, copy=False, readonly=True, default=lambda self: self._generate_sequence())
    type = fields.Selection([
        ('deal', 'Deal'),
        ('third_party_deal', 'Third Party Deal'),
        ('cash', 'Cash')
    ], string='Type', required=True)

    @api.model
    def _generate_sequence(self):
        sequence = self.env['ir.sequence'].next_by_code('crm.deal')
        return sequence or ''