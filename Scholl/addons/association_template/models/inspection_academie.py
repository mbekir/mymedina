from odoo import fields, models, api


class inspectionAcademie(models.Model):
    _name = 'inspection.academie'
    _description = 'Inscpection Academie'

    name = fields.Char()