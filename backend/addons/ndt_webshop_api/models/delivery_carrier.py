from odoo import models, fields, api
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError, ValidationError
class ProviderGrid(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(selection_add=[('base_on_rule', 'Based on Rules')])
    price_rule_ids = fields.One2many('delivery.price.rule', 'carrier_id', 'Pricing Rules', copy=True)

    def base_on_rule_rate_shipment2(self, order):
        # carrier = self._match_address(order.partner_shipping_id)
        # if not carrier:
        #     return {'success': False,
        #             'price': 0.0,
        #             'error_message': _('Error: this delivery method is not available for this address.'),
        #             'warning_message': False}

        # try:
        price_unit = self._get_price_available2(order)
        # except UserError as e:
        #     return {'success': False,
        #             'price': 0.0,
        #             'error_message': e.name,
        #             'warning_message': False}
        # if order.company_id.currency_id.id != order.pricelist_id.currency_id.id:
        #     price_unit = order.company_id.currency_id.with_context(date=order.date_order).compute(price_unit, order.pricelist_id.currency_id)

        return {'success': True,
                'price': price_unit,
                'error_message': False,
                'warning_message': False}

    def _get_price_available2(self, order):
        # self.ensure_one()
        total = weight = volume = quantity = 0
        total_delivery = 0.0
        for line in order.order_line:
            # if line.state == 'cancel':
            #     continue
            # if line.is_delivery:
            #     total_delivery += line.price_total
            # if not line.product_id or line.is_delivery:
            #     continue
            # qty = line.product_uom._compute_quantity(line.product_uom_qty, line.product_id.uom_id)
            qty = line.qty
            weight += (line.product_id.weight or 0.0) * qty
            volume += (line.product_id.volume or 0.0) * qty
            quantity += qty
        # total = (order.amount_total or 0.0) - total_delivery

        # total = order.currency_id.with_context(date=order.date_order).compute(total, order.company_id.currency_id)
        total = order.amount_total
        return self._get_price_from_picking2(total, weight, volume, quantity)

    def _get_price_from_picking2(self, total, weight, volume, quantity):
        price = 0.0
        criteria_found = False
        price_dict = {'price': total, 'volume': volume, 'weight': weight, 'wv': volume * weight, 'quantity': quantity}
        for line in self.price_rule_ids:
            test = safe_eval(line.variable + line.operator + str(line.max_value), price_dict)
            if test:
                price = line.list_base_price + line.list_price * price_dict[line.variable_factor]
                criteria_found = True
                break
        if not criteria_found:
            raise UserError(_("No price rule matching this order; delivery cost cannot be computed."))

        return price

    def base_on_rule_send_shipping(self, pickings):
        res = []
        for p in pickings:
            carrier = self._match_address(p.partner_id)
            if not carrier:
                raise ValidationError(_('Error: no matching grid.'))
            res = res + [{'exact_price': p.carrier_id._get_price_available2(p.sale_id) if p.sale_id else 0.0,  # TODO cleanme
                          'tracking_number': False}]
        return res

    # def base_on_rule_get_tracking_link(self, picking):
    #     return False

    # def base_on_rule_cancel_shipment(self, pickings):
    #     raise NotImplementedError()

