from odoo import fields, models, api


class NiveauEcole(models.Model):
    _name = 'niveau.ecole'
    _description = 'Niveau Ecole'

    name = fields.Char()
