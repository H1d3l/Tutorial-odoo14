from odoo import models

class EstateProperty(models.model):

    _inherit = 'estate.property'

    def inherited_action_sold_property(self):
        return super().inherited_action_sold_property()