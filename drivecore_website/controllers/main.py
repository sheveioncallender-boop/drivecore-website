from urllib.parse import urlsplit

from werkzeug.exceptions import NotFound

from odoo import http
from odoo.addons.website.controllers.main import Website as OdooWebsiteController
from odoo.http import request


SERVICES = {
    "wheel-alignment": {
        "name": "Wheel Alignment",
        "icon": "fa-crosshairs",
        "image": "service_wheel_alignment.webp",
        "intro": "Precision alignment for steadier handling, improved tyre life and a safer drive.",
        "details": "Incorrect wheel alignment can cause uneven tyre wear, steering pull, vibration and reduced stability. DriveCore checks your vehicle's alignment angles and corrects them using precise workshop procedures.",
        "benefits": ["Improved steering control", "More even tyre wear", "Better road stability", "Reduced rolling resistance"],
    },
    "mechanical-repairs": {
        "name": "Mechanical Repairs",
        "icon": "fa-wrench",
        "image": "service_mechanical.webp",
        "intro": "Dependable repairs and practical solutions that keep your vehicle performing at its best.",
        "details": "From unusual noises and leaks to worn components and drivability problems, our team follows a careful inspection process before recommending the work your vehicle actually needs.",
        "benefits": ["Clear fault assessment", "Quality replacement parts", "Transparent recommendations", "Workmanship you can trust"],
    },
    "vehicle-diagnostics": {
        "name": "Vehicle Diagnostics",
        "icon": "fa-laptop",
        "image": "service_diagnostics.webp",
        "intro": "Modern diagnostics that identify faults quickly and help us fix the right problem first.",
        "details": "Warning lights and intermittent issues require more than guesswork. We combine scan-tool information, live data and physical inspection to trace faults accurately.",
        "benefits": ["Warning-light diagnosis", "Electronic system checks", "Live data analysis", "Clear repair guidance"],
    },
    "engine-services": {
        "name": "Engine Services",
        "icon": "fa-cogs",
        "image": "service_engine.webp",
        "intro": "Complete engine care, from routine tune-ups to investigation of major performance concerns.",
        "details": "Our engine service process is designed to protect reliability, restore performance and help prevent small issues from becoming expensive repairs.",
        "benefits": ["Tune-ups and inspections", "Cooling-system checks", "Leak and noise diagnosis", "Performance troubleshooting"],
    },
    "brake-service": {
        "name": "Brake Service",
        "icon": "fa-stop-circle-o",
        "image": "service_brakes.webp",
        "intro": "Professional brake inspection, servicing and replacement for confident stopping power.",
        "details": "Your braking system is essential to vehicle safety. We inspect key components, explain their condition and recommend only the work needed to restore dependable braking.",
        "benefits": ["Pad and rotor inspection", "Brake-fluid checks", "Noise and vibration diagnosis", "Safer braking performance"],
    },
    "maintenance-more": {
        "name": "Maintenance & More",
        "icon": "fa-tint",
        "image": "service_maintenance.webp",
        "intro": "Routine maintenance and practical auto-care services that support long-term reliability.",
        "details": "Consistent maintenance helps your vehicle last longer and perform better. DriveCore can help you plan the essential services your vehicle needs based on condition and usage.",
        "benefits": ["Oil and filter service", "Fluid and belt checks", "General safety inspection", "Preventive maintenance planning"],
    },
}


class DriveCoreHomepageController(OdooWebsiteController):
    """Serve the DriveCore homepage deterministically at the root URL."""

    @http.route()
    def index(self, **kw):
        return request.render("drivecore_website.drivecore_homepage_page")


class DriveCoreWebsite(http.Controller):

    @staticmethod
    def _public_form_allowed(post):
        """Lightweight anti-spam / cross-site protection for public enquiry forms.

        These endpoints intentionally do not depend on Odoo's session-bound CSRF
        token because cached/mobile website sessions can otherwise invalidate the
        token between page render and submit.  We still reject obvious cross-site
        browser posts and bot-filled honeypots.
        """
        if post.get("website_url"):
            return False

        headers = request.httprequest.headers
        fetch_site = (headers.get("Sec-Fetch-Site") or "").lower()
        if fetch_site and fetch_site not in {"same-origin", "same-site", "none"}:
            return False

        current_host = (request.httprequest.host or "").split(":", 1)[0].lower()
        for header_name in ("Origin", "Referer"):
            value = headers.get(header_name)
            if not value:
                continue
            try:
                source_host = (urlsplit(value).hostname or "").lower()
            except ValueError:
                return False
            if source_host and source_host != current_host:
                return False
            break
        return True

    @staticmethod
    def _clean(value, limit=500):
        value = (value or "").strip()
        return value[:limit]

    @http.route("/drivecore/service/<string:slug>", type="http", auth="public", website=True, sitemap=True)
    def service_detail(self, slug, **kwargs):
        service = SERVICES.get(slug)
        if not service:
            raise NotFound()
        return request.render("drivecore_website.service_detail_page", {
            "service": service,
            "service_slug": slug,
        })

    @http.route("/drivecore/book/submit", type="http", auth="public", website=True, methods=["POST"], csrf=False)
    def submit_booking(self, **post):
        if not self._public_form_allowed(post):
            return request.redirect("/book-a-service?error=security")
        if not post.get("name") or not post.get("email") or not post.get("phone"):
            return request.redirect("/book-a-service?error=missing")
        valid_services = {"wheel_alignment", "mechanical_repairs", "diagnostics", "engine_services", "brake_service", "maintenance", "other"}
        service_type = post.get("service_type") if post.get("service_type") in valid_services else "other"
        request.env["drivecore.service.request"].sudo().create({
            "name": self._clean(post.get("name"), 120),
            "email": self._clean(post.get("email"), 254),
            "phone": self._clean(post.get("phone"), 80),
            "vehicle_make": self._clean(post.get("vehicle_make"), 80),
            "vehicle_model": self._clean(post.get("vehicle_model"), 80),
            "vehicle_year": self._clean(post.get("vehicle_year"), 12),
            "registration_number": self._clean(post.get("registration_number"), 40),
            "service_type": service_type,
            "preferred_date": post.get("preferred_date") or False,
            "preferred_time": self._clean(post.get("preferred_time"), 40) or False,
            "issue_description": self._clean(post.get("issue_description"), 4000),
        })
        return request.redirect("/request-received?type=booking")

    @http.route("/drivecore/contact/submit", type="http", auth="public", website=True, methods=["POST"], csrf=False)
    def submit_contact(self, **post):
        if not self._public_form_allowed(post):
            return request.redirect("/contact-us?error=security")
        if not post.get("name") or not post.get("email") or not post.get("message"):
            return request.redirect("/contact-us?error=missing")
        request.env["drivecore.contact.request"].sudo().create({
            "name": self._clean(post.get("name"), 120),
            "email": self._clean(post.get("email"), 254),
            "phone": self._clean(post.get("phone"), 80),
            "subject": self._clean(post.get("subject"), 200),
            "message": self._clean(post.get("message"), 4000),
        })
        return request.redirect("/request-received?type=contact")
