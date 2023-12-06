from odoo import fields, models, api


class TypeBesoins(models.Model):
    _name = 'type.besoins'
    _description = 'Type Besoins'

    name = fields.Char()
