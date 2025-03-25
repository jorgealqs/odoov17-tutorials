{
    "name": "Real State Tutorial",
    "version": "1.0",
    "author": "Jorge Alberto Quiroz Sierra",
    "depends": [
        "base",
    ],
    "sequence": -10,
    'category': 'Tutorials/RealState',
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users_inherited_views.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "description": """
        Estate Management System is an
        application that allows users to manage properties,
        property types, property tags, property offers,
        and inherit data from the base module.

        Features:
        - Property Management
        - Property Listings
        - Price Tracking
        - Garden Information
        - Property Details
    """,
    "license": "LGPL-3"
}
