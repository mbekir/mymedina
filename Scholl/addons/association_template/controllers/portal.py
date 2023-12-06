from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class WebsiteForm(http.Controller):
   @http.route(['/association'], type='http', auth="public", website=True)
   def appointment(self):
       fonctions = request.env['fonction.ecole'].sudo().search([])
       type_ecole_ids = request.env['type.ecole'].sudo().search([])
       niveau_ids = request.env['niveau.ecole'].sudo().search([])
       type_besoins_ids = request.env['type.besoins'].sudo().search([])
       ief_ids = request.env['ief.ecole'].sudo().search([])
       country = request.env['res.country'].sudo().search([], order='name')
       values = {}
       values.update({
           'fonctions': fonctions,
           'type_ecole_ids': type_ecole_ids,
           'niveau_ids': niveau_ids,
           'type_besoins_ids': type_besoins_ids,
           'ief_ids': ief_ids,
           'country': country
       })
       return request.render("association_template.online_appointment_form", values)

   @http.route('/set', auth='public', type="http", website=True)
   def create(self, **post):
       association = request.env["association.template"].sudo().create(post)
       email = post.get('email')
       name = post.get('nom') + ' ' + post.get('prenom')

       token = association.token
       body_template = """
       <!DOCTYPE html>
       <html>
       <head>
           <style>
               body {{
                   font-family: Arial, sans-serif;
                   background-color: #f4f4f4;
                   padding: 20px;
               }}
               .container {{
                   max-width: 600px;
                   margin: 0 auto;
                   background-color: #fff;
                   padding: 20px;
                   border: 1px solid #ddd;
                   border-radius: 5px;
                   box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
               }}
               .header {{
                   text-align: center;
                   background-color: #007BFF;
                   color: #fff;
                   padding: 10px 0;
                   border-radius: 5px 5px 0 0;
               }}
               .content {{
                   padding: 20px;
               }}
               .button {{
                   display: inline-block;
                   padding: 10px 20px;
                   background-color: #007BFF;
                   color: #fff;
                   text-decoration: none;
                   border-radius: 5px;
                   margin-top: 20px;
               }}
               .social-links {{
                   margin-top: 20px;
               }}
               .social-links a {{
                   display: inline-block;
                   margin-right: 10px;
                   text-decoration: none;
               }}
           </style>
       </head>
       <body>
           <div class="container">
               <div class="header">
                   <h2>Bonjour {name},</h2>
               </div>
               <div class="content">
                   <p>Votre demande a bien été prise en compte. Merci de cliquer sur le lien ci-dessous pour confirmer votre e-mail :</p>
                   <a class="button" href="http://localhost:2020/confirmation?token={token}">Lien de confirmation</a>
                   <p>N’hésitez pas à nous suivre sur les réseaux sociaux :</p>
                   <div class="social-links">
                       <a href="https://www.facebook.com/mymedinaschools">Facebook</a>
                       <a href="https://www.instagram.com/mymedinaschools/">Instagram</a>
                       <a href="https://www.tiktok.com/@mymedinaschools?_t=8huSv4jeYwz&_r=1">TikTok</a>
                   </div>
                   <p>L’équipe MMS Arica Kids</p>
                   <p><a href="www.mymedinaschools.com">www.mymedinaschools.com</a></p>
                   <p>
       00221775687995
       </p>
               </div>
           </div>
       </body>
       </html>
       """
       body = body_template.format(name=name, token=token)
       partner_id = request.env['res.partner'].sudo().browse(3)

       mail_values = {
           'email_from': partner_id.email,
           'email_to': email,
           'subject': 'Veuillez confirmer votre adresse e-mail',
           'body_html': body,
       }
       request.env['mail.mail'].sudo().create(mail_values).send()

       # association.send_mailing(
       #      email,
       #      'Veuillez confirmer votre adresse e-mail',
       #      body)
       return http.request.render('association_template.thank', {})



   @http.route('/confirmation', auth='public', methods=['GET'], website=True)
   def confirm_email(self, token, **kwargs):
       record = request.env['association.template'].sudo().search([('token', '=', token)], limit=1)
       if record:
           record.state = 'confirmé'
           return http.request.render('association_template.confirmation', {})
       else:
           return http.request.render('association_template.invalide_confirmation', {})
