import base64

from odoo import api, models, tools


class Website(models.Model):
    _inherit = "website"

    @api.model
    def drivecore_activate_homepage(self):
        """Apply the DriveCore homepage and brand icon to every website."""
        values = {"homepage_url": "/"}

        # Odoo 19 removed get_resource_path from odoo.modules.module.
        # file_open is the supported addons-path-aware API for module files.
        try:
            with tools.file_open(
                "drivecore_website/static/src/img/favicon.png", "rb"
            ) as favicon_file:
                values["favicon"] = base64.b64encode(favicon_file.read())
        except FileNotFoundError:
            # Do not prevent the database registry from loading if the optional
            # favicon asset is unavailable for any reason.
            pass

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
