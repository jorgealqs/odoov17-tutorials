from odoo import models, exceptions, Command  # type: ignore
import logging

logger = logging.getLogger(__name__)


class InheritedEstatePropertyModel(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        """
            Create an invoice for the sold property before marking it as sold.
        """
        for record in self:
            # Validate required fields
            if not record.selling_price or not record.buyer:
                raise exceptions.UserError(
                    "Cannot create invoice: Selling price and buyer are "
                    "required."
                )

            # Create invoice
            invoice = self.env["account.move"].create({
                "partner_id": record.buyer.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    # Line 1: 6% of the selling price
                    Command.create({
                        "name": f"Commission (6%) for property {record.name}",
                        "quantity": 1.0,
                        "price_unit": record.selling_price * 0.06,
                    }),
                    # Line 2: Fixed administrative fee
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1.0,
                        "price_unit": 100.00,
                    }),
                ],
            })

            logger.info(
                "Invoice created for property %s (ID: %s) - Invoice ID: %s",
                record.name, record.id, invoice.id
            )

        # Call the original action_sold method from the parent class
        return super().action_sold()
