from odoo import models,fields



class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = "name"


    name = fields.Char(required = True)
    color = fields.Integer()

    _sql_constraints = [
        (
            'name_tag_unique',
            'UNIQUE(name)',
            'O nome da tag deve ser único'
        ),
    ]