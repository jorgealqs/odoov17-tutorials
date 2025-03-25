"""
Inherited User Model
==================

This module extends Odoo's built-in user model (res.users) to add real estate
property management capabilities. It creates a relationship between users and
properties, specifically for tracking properties managed by salespeople.

Technical Details:
- Inherits: res.users (base user model)
- New Fields: property_ids (One2many to estate.property)
- Domain Filter: Only shows properties in 'new' or 'offer_received' states
"""

from odoo import fields, models  # type: ignore


class InheritedResUser(models.Model):
    """
    Extended User Model for Real Estate Management

    Inherits the base res.users model to add property management capabilities.
    This inheritance allows tracking which properties are being managed by
    which salesperson.

    Key Extensions:
    - Links properties to users (salespeople)
    - Filters properties by state
    - Provides quick access to assigned properties
    """

    _inherit = "res.users"  # Inherits the base user model

    property_ids = fields.One2many(
        "estate.property",          # Related model
        "salesperson",
        # Field in estate.property that references res.users
        string="Properties",       # Field label
        domain=[                   # Filter criteria
            ("state", "in", ["new", "offer_received"])
            # Only show active properties
        ],
    )
