from typing import Counter, Sequence
from odoo import models,fields,api



class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = "sequence,name"


    name = fields.Char(required = True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_count = fields.Integer(compute='_compute_offer_count')


    _sql_constraints = [
        (
            'name_type_unique',
            'UNIQUE(name)',
            'O nome do tipo deve ser único'
        ),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        count=0
        for record in self:
            for r in record.offer_ids:
                #if r.property_type_id.id == record.offer_ids.property_type_id.id:
                count+=1

                print(r.property_type_id.id)
            record.offer_count = count
        return True


         

    
    


