from odoo import fields, models, api


class TypeEcole(models.Model):
    _name = 'type.ecole'
    _description = 'Type Ecole'

    name = fields.Char()
