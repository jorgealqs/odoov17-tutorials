"""
Estate Property Tag Model
========================

This module defines property tags for real estate management in Odoo.
Tags are used to categorize and label properties with specific attributes
or characteristics (e.g., "Renovated", "Sea View", "Near School").

Key Features:
- Unique tag names
- Color coding support for visual distinction
- Alphabetical ordering by name

Technical Details:
- Model Name: estate.property.tag
- Table Name: estate_property_tag
- Order: Alphabetically by name
"""

from odoo import models, fields  # type: ignore


class EstatePropertyTag(models.Model):
    """
    Estate Property Tag Model

    A simple model for managing property tags with color support.
    Each tag must have a unique name and can be assigned a color
    for UI display purposes.

    Attributes:
        name (fields.Char): The tag name (required, unique)
        color (fields.Integer): Color index for the tag in the UI

    SQL Constraints:
        - check_name: Ensures tag names are unique across the system
    """

    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        (
            'check_name',
            'UNIQUE(name)',
            'The name must be unique.'
        )
    ]
