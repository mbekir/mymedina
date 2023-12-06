from odoo import fields, models, api


class FonctionEcole(models.Model):
    _name = 'fonction.ecole'
    _description = 'Fonction Ecole'

    name = fields.Char()
