from odoo import models

class EstateProperty(models.Model):

    _inherit = 'estate.property'

    def inherited_action_sold_property(self):
        print("vendido")
        return super().action_sold_property()