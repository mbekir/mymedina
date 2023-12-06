from odoo import fields, models, api
import uuid

from datetime import datetime, timedelta


class AssociationTemplate(models.Model):
    _name = 'association.template'
    _description = 'Association Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(compute='_compute_name', store=True)

    nom = fields.Char(required=True)
    prenom = fields.Char(string="prénom")

    fonction_id = fields.Many2one('fonction.ecole', string='Fonction dans l’école')
    email = fields.Char()
    tel = fields.Char()
    tel_international = fields.Char(string="numéro de téléphone",compute='_compute_tel', store=True)
    adresse_ecole = fields.Char(string="adresse de l’école")
    nom_ecole = fields.Char(string="adresse de l’école")
    type_ecole_id = fields.Many2one('type.ecole', string='Type d’école')

    niveau_id = fields.Many2one('niveau.ecole')
    effectif= fields.Integer()
    ief_id = fields.Many2one('ief.ecole',string="IEF")
    date_de_la_demande = fields.Date(default=lambda self: fields.Date.today())
    type_de_besoins_id = fields.Many2one('type.besoins')
    description_du_besoin = fields.Text()
    pourcentage_CFEE = fields.Float(string='Dernier pourcentage de réussite au CFEE de l’école')
    pourcentage_BAC = fields.Float(string='Dernier pourcentage de réussite BAC  de l’école')
    pourcentage_BFEM = fields.Float(string='Dernier pourcentage de réussite au BFEM de l’école')
    country = fields.Many2one('res.country', string="Country")
    country_code = fields.Integer(related="country.phone_code")


    def _default_token(self):
        return str(uuid.uuid4())


    token = fields.Char(string='Token', required=True, copy=False, default=lambda self: self._default_token())

    STATE_SELECTION = [
        ('confirmé', 'Confirmé'),
        ('non_confirmé', 'Non confirmé'),
    ]

    state = fields.Selection(STATE_SELECTION, string='État', default='non_confirmé')



    _sql_constraints = [
        ('tel_unique', 'UNIQUE(tel)', "Le numéro de téléphone saisi est déjà utilisé. Veuillez fournir un numéro de téléphone différent !")
    ]

    @api.depends('nom', 'prenom')
    def _compute_name(self):
        for record in self:
            record.name = (record.nom or '') + ' ' + (record.prenom or '')

    @api.depends('country_code', 'tel')
    def _compute_tel(self):
        for record in self:
            record.tel_international = '+' + (str(record.country_code) or '') + ' ' + (record.tel or '')

    def send_mailing(self, email_to, subject, body):
        mail_values = {
            'subject': subject,
            'body_html': body,
            'email_to': email_to,
        }
        mail = self.env['mail.mail'].create(mail_values)
        mail.send()







