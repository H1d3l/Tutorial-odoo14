from odoo import models,fields,api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')],copy=False)
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',required = True)
    property_id = fields.Many2one(
        'estate.property',
        string='Property',required = True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline',inverse='_inverse_date_deadline',default= lambda self:date.today()+relativedelta(days=+7))


#Corrigir bug no campo date deadline
    @api.depends('date_deadline')
    def _compute_date_deadline(self):
        for record in self:
            print(record.create_date+relativedelta(days=record.validity))
            record.date_deadline = record.create_date+relativedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
      
            dfs= record.date_deadline.strftime('%Y-%m-%d')
            dis= record.create_date.strftime('%Y-%m-%d')
            print(dfs,dis)
          
            df=  datetime.strptime(dfs,'%Y-%m-%d')       
            di=  datetime.strptime(dis,'%Y-%m-%d')  
            record.validity = abs((df-di).days)
            