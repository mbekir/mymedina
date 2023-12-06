from odoo import fields, models, api


class iefEcole(models.Model):
    _name = 'ief.ecole'
    _description = 'Ief Ecole'

    name = fields.Char()
