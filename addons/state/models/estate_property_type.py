"""
Estate Property Type Model
========================

This module defines property types for real estate management in Odoo.
It provides a way to categorize properties (e.g., apartments, houses, land)
and track offers associated with each property type.

Key Features:
- Property type categorization
- Offer tracking per property type
- Automatic offer counting
- Sequence management for custom ordering
- Unique name constraints

Technical Details:
- Model Name: estate.property.type
- Table Name: estate_property_type
- Order: By name
- Dependencies: estate.property, estate.property.offer
"""

from odoo import api, models, fields  # type: ignore


class EstatePropertyType(models.Model):
    """
    Estate Property Type Model

    Manages categories of real estate properties and their associated offers.
    Each property type can have multiple properties and offers linked to it.

    Key Fields:
    - name: Unique identifier for the property type
    - property_ids: Properties of this type
    - offer_ids: Offers made on properties of this type
    - sequence: Custom ordering number
    - offer_count: Computed number of offers
    """

    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"  # Orders types alphabetically by name

    # Basic Information
    name = fields.Char(
        required=True,
        help="Name of the property type (e.g., Apartment, House, Land)"
    )

    # Relationships
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        help="Properties categorized under this type"
    )

    # Ordering
    sequence = fields.Integer(
        help="Used to customize the order of property types"
    )

    # Offer Management
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_type_id',
        help="Offers made on properties of this type"
    )
    offer_count = fields.Integer(
        compute="_compute_offer_count",
        help="Total number of offers for this property type"
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        """
        Computes the total number of offers for each property type.
        This method is automatically triggered when offer_ids changes.
        """
        for record in self:
            record.offer_count = len(record.offer_ids)

    # Database Constraints
    _sql_constraints = [
        (
            'check_name',
            'UNIQUE(name)',
            'Property type names must be unique.'
        )
    ]
