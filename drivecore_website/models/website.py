import base64

from odoo import api, models
from odoo.modules.module import get_resource_path


class Website(models.Model):
    _inherit = "website"

    @api.model
    def drivecore_activate_homepage(self):
        """Apply the DriveCore homepage and brand icon to every website."""
        values = {"homepage_url": "/"}
        favicon_path = get_resource_path(
            "drivecore_website", "static", "src", "img", "favicon.png"
        )
        if favicon_path:
            with open(favicon_path, "rb") as favicon_file:
                values["favicon"] = base64.b64encode(favicon_file.read())

        websites = self.sudo().search([])
        if websites:
            websites.write(values)

        homepage_view = self.env.ref("website.homepage", raise_if_not_found=False)
        if homepage_view:
            canonical_page = self.env["website.page"].sudo().search(
                [("view_id", "=", homepage_view.id)], limit=1
            )
            if canonical_page:
                canonical_page.write({"url": "/", "is_published": True})

        return True
