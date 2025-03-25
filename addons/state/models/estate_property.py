"""
Estate Property Model
===================

This module defines the EstateProperty model for managing real estate
properties in Odoo. It provides comprehensive property management
functionality including basic details, pricing, amenities, and state
management.

Key Features:
- Property details management (name, description, specifications)
- Price tracking (expected and selling prices)
- Property status workflow (new → offer received → offer accepted →
sold/canceled)
- Relationship management (buyers, salespeople, property types)
- Automated calculations (total area, best price)
- Garden and amenities tracking

Technical Details:
- Model Name: estate.property
- Table Name: estate_property
- Dependencies: res.users, res.partner, estate.property.type
"""

from odoo import api, fields, models, exceptions  # type: ignore
from datetime import timedelta


class EstateProperty(models.Model):
    """
    Estate Property Model

    Manages real estate property listings with comprehensive property
    information, sales workflow, and relationship tracking.

    Key Fields:
    - Basic Info: name, description, postcode
    - Specifications: bedrooms, living_area, facades
    - Pricing: expected_price, selling_price
    - Amenities: garage, garden, garden_area, garden_orientation
    - Status: active, state
    - Relationships: property_type_id, salesperson, buyer, tag_ids, offer_ids

    Important Relationships:
    - salesperson (res.users): Links to the Odoo user responsible for the
        property
    - buyer (res.partner): Tracks the eventual purchaser
    - property_type_id (estate.property.type): Categorizes the property
    - offer_ids (estate.property.offer): Manages received offers
    """

    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    # Basic Information Fields
    name = fields.Char(
        string='Name',
        required=True,
        help="Property title or identifier"
    )
    description = fields.Text(
        string='Description',
        help="Detailed description of the property"
    )
    postcode = fields.Char(
        string='Postcode',
        help="Postal code where the property is located"
    )

    # Dates and Availability
    date_availability = fields.Date(
        string='Available From',
        copy=False,
        default=lambda self: fields.Date.today() + timedelta(days=90),
        help="Date from which the property becomes available"
    )

    # Pricing Information
    expected_price = fields.Float(
        string='Expected Price',
        required=True,
        help="Expected selling price for the property"
    )
    selling_price = fields.Float(
        string='Selling Price',
        readonly=True,
        copy=False,
        help="Final selling price of the property"
    )

    # Property Specifications
    bedrooms = fields.Integer(
        string='Bedrooms',
        default=2,
        help="Number of bedrooms in the property"
    )
    living_area = fields.Integer(
        string='Living Area (sqm)',
        help="Total living area in square meters"
    )
    facades = fields.Integer(
        string='Facades',
        help="Number of facades the property has"
    )

    # Amenities
    garage = fields.Boolean(
        string='Garage',
        help="Indicates if the property has a garage"
    )
    garden = fields.Boolean(
        string='Garden',
        help="Indicates if the property has a garden"
    )
    garden_area = fields.Integer(
        string='Garden Area (sqm)',
        help="Garden area in square meters"
    )
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        help="Cardinal direction of the garden's orientation"
    )

    # Status and Classification
    active = fields.Boolean(
        string='Active',
        default=True,
        help="If unchecked, the property will be archived"
    )
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        required=True,
        default='new',
        copy=False,
        help="Current state of the property in the sales pipeline"
    )

    # Relationships
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
        help="Category or type of the property"
    )
    salesperson = fields.Many2one(
        'res.users',  # Links to Odoo's built-in user model
        string='Salesperson',
        default=lambda self: self.env.user,
        # Automatically set to current user
        help="User responsible for selling the property"
    )
    buyer = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False,
        help="Partner who has purchased the property"
    )
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Tags',
        help="Tags associated with the property"
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers',
        help="Offers made for this property"
    )
    total_area = fields.Integer(
        string='Total Area (sqm)',
        compute='_compute_total_area',
        help="Total area of the property including living and garden areas"
    )
    best_price = fields.Float(
        string='Best Offer',
        compute='_compute_best_price',
        help="Highest offer received for the property"
    )

    _sql_constraints = [
        (
            'check_expected_price_positive',
            'CHECK(expected_price > 0)',
            'The expected price must be strictly positive.'
        ),
        (
            'check_selling_price_positive',
            'CHECK(selling_price >= 0)',
            'The selling price must be positive.'
        )
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        """Calculates the total area by summing living and garden areas."""
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError(
                    "A sold property cannot be canceled."
                )
            record.state = "canceled"

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise exceptions.UserError(
                    "A canceled property cannot be set as sold."
                )
            record.state = "sold"

    def unlink(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise exceptions.UserError(
                    "You cannot delete a property that is not in 'New' or "
                    "'Canceled' state."
                )
        return super().unlink()
