from odoo import api, models


class Website(models.Model):
    _inherit = "website"

    @api.model
    def drivecore_activate_homepage(self):
        """Reset every website entry point to the canonical root URL."""
        websites = self.sudo().search([])
        if websites:
            websites.write({"homepage_url": "/"})

        homepage_view = self.env.ref("website.homepage", raise_if_not_found=False)
        if homepage_view:
            canonical_page = self.env["website.page"].sudo().search(
                [("view_id", "=", homepage_view.id)], limit=1
            )
            if canonical_page:
                canonical_page.write({"url": "/", "is_published": True})

        return True
