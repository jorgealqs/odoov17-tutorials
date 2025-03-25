# 🏠 Real Estate Management System - Odoo Module

## Overview

A comprehensive real estate property management module for Odoo, designed to handle property listings, offers, and sales processes efficiently.

## 🌟 Features

### Property Management

- Complete property lifecycle management (New → Offer Received → Offer Accepted → Sold)
- Detailed property information tracking:
    -Basic details (name, description, postcode)
    -Physical characteristics (bedrooms, living area, facades)
    -Financial aspects (expected price, selling price)
    -Availability dates
- Property type categorization
- Tag-based property labeling with color coding
- Status tracking and visualization

### Offer Management

- Inline offer creation and management
- Offer acceptance/refusal workflow
- Automatic best offer tracking
- State-dependent offer handling

### User Interface

- Intuitive form views for property details
- List views with visual state indicators
- Advanced search and filtering capabilities
- Color-coded tags for easy visualization
- Dynamic button states based on property status

## 🛠️ Technical Stack

- **Platform**: Odoo
- **Language**: Python
- **Database**: PostgreSQL
- **Views**: XML
- **Business Logic**: Python models with Odoo ORM

## 📁 Project Structure

```plaintext
addons/estate/
├── models/
│   ├── estate_property.py
│   ├── estate_property_type.py
│   └── estate_property_tag.py
├── views/
│   ├── estate_property_views.xml
│   ├── estate_property_type_views.xml
│   └── estate_menus.xml
├── security/
│   └── ir.model.access.csv
├── __init__.py
└── __manifest__.py
```

## 🚀 Installation

1. Clone the repository into your Odoo addons directory:

    ```bash
    git clone [repository-url] /path/to/odoo/addons/estate
    ```

2. Update your Odoo configuration to include the new module:

    ```bash
    path/to/odoo/odoo-bin -d your_database -i estate
    ```

3. Restart your Odoo server and update the module list.

4. Install the module through the Odoo Apps interface.

## 💻 Usage

### Property Types

1. Access through Real Estate → Settings → Property Types
2. Create and manage property categories
3. View properties associated with each type

### Property Tags

1. Create and manage tags through the property form
2. Use tags to categorize and filter properties
3. Customize tag colors for better visualization

## 🔒 Security

- Access rights defined in `ir.model.access.csv`
- Role-based access control for different user types
- Data integrity constraints for critical fields

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the LGPL-3 - see the LICENSE file for details.

## 👥 Authors

- Jorge Alberto Quiroz Sierra - [LinkedIn](https://www.linkedin.com/in/jorgealqs/)

## 📞 Contact

- Email: [joralquisi@hotmail.com](mailto:joralquisi@hotmail.com)
- WhatsApp: [+57 319 366 2738](https://wa.me/573193662738?text=Hello%20Jorge,%20I'm%20interested%20in%20talking%20with%20you)

## 🙏 Acknowledgments

- Odoo Community
- Contributors and testers
- Documentation team

---
Made with ❤️ using Odoo
