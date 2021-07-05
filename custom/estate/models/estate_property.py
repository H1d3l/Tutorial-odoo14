
from odoo import models,fields,api
from odoo.exceptions import UserError,ValidationError

from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = "id desc"

    name = fields.Char(required = True)
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
        
        )
    property_tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Property Tag',
        )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default= lambda self:date.today()+relativedelta(months=+3))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True,copy=False,default=0)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West')
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection =[
        ('new', 'New'),
        ('offer received', 'Offer Received'),
        ('offer accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')], required = True,copy = False,default='new')
    salesman_id = fields.Many2one(
        'res.users',
        string='Salesman',default = lambda self:self.env.user
        )
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',copy=False
        )
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')



    _sql_constraints = [
        (
            'expected_price_positive',
            'CHECK(expected_price > 0)',
            'O valor esperado deve ser maior que 0'
        ),

        (
            'selling_price_positive',
            'CHECK(selling_price > 0 WHERE state!=new)',
            'O valor de venda deve ser maior que 0'
        ),

    ]

    #calcula a area total da propriedade
    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    #calcula a melhor oferta 
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.mapped('offer_ids.price') == []:
                record.best_price = 0
            else:
                record.best_price = max(record.mapped('offer_ids.price'))

    @api.onchange('garden')
    def _onchange_garden_area(self):
        if self.garden == True:
            self.garden_area = 10
        else:
            self.garden_area = 0

    @api.onchange('garden')
    def _onchange_garden_orientation(self):
        if self.garden == True:
            self.garden_orientation = 'north'
        else:
            self.garden_orientation = ''


    def action_cancel_property(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
            else:
                raise UserError(" Sold properties cannot be canceled")
        return True


    def action_sold_property(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
            else:
                raise UserError("Canceled properties cannot be sold")
        return True






    @api.constrains('expected_price','selling_price','offer_ids')
    def _check_selling_price(self):
        for record in self:
            if 'accepted' in record.mapped('offer_ids.status'):
                if record.selling_price < record.expected_price * 0.9:
                    raise ValidationError("O valor de venda não pode ser inferior a 90% do preço esperado.")




        
