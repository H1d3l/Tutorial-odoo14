
from odoo import models,fields,api
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

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
    selling_price = fields.Float(readonly = True,copy=False)
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
    active = fields.Boolean(active=True)
    status = fields.Selection(
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