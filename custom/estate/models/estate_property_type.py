from odoo import models,fields



class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(required = True)
    
    _sql_constraints = [
        (
            'name_type_unique',
            'UNIQUE(name)',
            'O nome do tipo deve ser único'
        ),
    ]