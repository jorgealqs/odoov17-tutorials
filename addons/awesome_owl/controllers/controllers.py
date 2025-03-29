from odoo import http  # type: ignore
from odoo.http import request  # type: ignore


class OwlPlayground(http.Controller):
    """
    Controller class that handles HTTP routes for the Awesome OWL Playground.
    Inherits from Odoo's base Controller class to provide web routing
    capabilities.
    """

    @http.route(['/awesome_owl'], type='http', auth='public')
    def show_playground(self):
        """
        Renders the OWL playground page.

        Route: /awesome_owl
        Type: HTTP GET request
        Authentication: Public (no login required)

        Returns:
            http.Response: Rendered HTML template for the OWL playground
            Template used: 'awesome_owl.playground'
        """
        return request.render('awesome_owl.playground')
