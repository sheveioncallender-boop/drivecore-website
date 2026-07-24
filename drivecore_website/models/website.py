from odoo import api, models


class Website(models.Model):
    _inherit = "website"

    @api.model
    def drivecore_activate_homepage(self):
        """Use the DriveCore static page as homepage on unconfigured/shop-first sites."""
        websites = self.search([
            "|",
            ("homepage_url", "=", False),
            ("homepage_url", "in", ["", "/", "/shop"]),
        ])
        if websites:
            websites.write({"homepage_url": "/drivecore-home"})
        self.env.registry.clear_cache("templates")
        return True
