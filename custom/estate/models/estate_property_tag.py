from odoo import models,fields



class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(required = True)

    _sql_constraints = [
        (
            'name_tag_unique',
            'UNIQUE(name)',
            'O nome da tag deve ser único'
        ),
    ]