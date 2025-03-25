"""
Estate Property Offer Model
=========================

This module defines the EstatePropertyOffer model for managing offers on real
estate properties in Odoo. It handles offer creation, validation,
acceptance/refusal, and deadline calculations.

Key Features:
- Offer price management with validation rules
- Automatic deadline calculation based on validity period
- Offer status tracking (accepted/refused)
- Property state management on offer actions
- Price constraints and validation rules

Technical Details:
- Model Name: estate.property.offer
- Table Name: estate_property_offer
- Dependencies: estate.property, res.partner
- Order: Descending by price
"""

from odoo import api, fields, models, exceptions  # type: ignore
from odoo.tools import float_utils  # type: ignore
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    """
    Estate Property Offer Model

    Manages offers made on real estate properties with price validation,
    deadline tracking, and offer status management.

    Key Fields:
    - price: Offer amount with validation rules
    - status: Offer state (accepted/refused)
    - partner_id: Potential buyer
    - property_id: Related property
    - validity: Offer valid period in days
    - date_deadline: Computed deadline date
    """

    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"  # Orders offers by price, highest first

    # Basic Fields
    price = fields.Float(
        help="Offer amount - must be positive and above 90% of expected price"
    )
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False,
        help="Current status of the offer"
    )

    # Relationships
    partner_id = fields.Many2one(
        'res.partner',
        required=True,
        help="Partner making the offer"
    )
    property_id = fields.Many2one(
        'estate.property',
        required=True,
        help="Property for which offer is made"
    )

    # Deadline Management
    validity = fields.Integer(
        default=7,
        help="Number of days the offer remains valid"
    )
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
        help="Automatically computed deadline based on validity days"
    )

    # Related Fields
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
        help="Property type from related property"
    )

    # SQL Constraints
    _sql_constraints = [
        (
            'check_price_positive',
            'CHECK(price > 0)',
            'The price offer must be strictly positive.'
        )
    ]

    @api.depends("validity", "date_deadline")
    def _compute_date_deadline(self):
        """
            Computes deadline date based on creation date and validity period.
        """
        for record in self:
            if not record.create_date:
                record.date_deadline = (
                    fields.Date.today() + timedelta(days=record.validity)
                )
            else:
                create_date = fields.Datetime.from_string(record.create_date)
                deadline_date = create_date + timedelta(days=record.validity)
                record.date_deadline = deadline_date.date()

    def _inverse_date_deadline(self):
        """Updates validity days when deadline date is manually changed."""
        for record in self:
            if record.date_deadline and record.create_date:
                deadline_date = fields.Date.from_string(record.date_deadline)
                create_date = fields.Datetime.from_string(record.create_date)
                record.validity = (deadline_date - create_date.date()).days

    def action_accepted(self):
        """
        Accepts the offer and updates related property information.
        Raises error if another offer is already accepted.
        """
        for record in self:
            if record.property_id.offer_ids.filtered(
                lambda o: o.status == 'accepted' and o.id != record.id
            ):
                raise exceptions.UserError(
                    "This property already has an accepted offer."
                )
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
            record.property_id.state = "offer_accepted"

    def action_refused(self):
        """Marks the offer as refused."""
        for record in self:
            record.status = "refused"

    @api.constrains('price')
    def check_price(self):
        """
        Validates that offer price is at least 90% of expected price.
        Raises UserError if validation fails.
        """
        for record in self:
            if (
                not float_utils.float_is_zero(
                    record.property_id.expected_price, precision_digits=2
                )
                and float_utils.float_compare(
                    record.price,
                    0.9 * record.property_id.expected_price,
                    precision_digits=2
                ) < 0
            ):
                raise exceptions.UserError(
                    "The offer price cannot be lower than 90% of the expected"
                    "price! The expected price is "
                    f"{record.property_id.expected_price:,.2f}"
                )

    @api.model
    def create(self, vals):
        """
        Override create method to add additional validations:
        - Prevents creation of offers lower than existing ones
        - Updates property state to 'offer_received'
        """
        if 'property_id' in vals:
            property_id = vals['property_id']
            property_obj = self.env['estate.property'].browse(property_id)
            if 'price' in vals:
                new_offer_price = vals['price']
                existing_offers = property_obj.offer_ids.filtered(
                    lambda offer: offer.price > new_offer_price
                )
                if existing_offers:
                    raise exceptions.UserError(
                        "You cannot create an offer "
                        "with a lower amount than an existing offer."
                    )
            property_obj.write({'state': 'offer_received'})
        return super().create(vals)
