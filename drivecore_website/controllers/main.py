from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import request


SERVICES = {
    "wheel-alignment": {
        "name": "Wheel Alignment",
        "icon": "fa-crosshairs",
        "image": "wheel_alignment.webp",
        "intro": "Precision alignment for steadier handling, improved tyre life and a safer drive.",
        "details": "Incorrect wheel alignment can cause uneven tyre wear, steering pull, vibration and reduced stability. DriveCore checks your vehicle's alignment angles and corrects them using precise workshop procedures.",
        "benefits": ["Improved steering control", "More even tyre wear", "Better road stability", "Reduced rolling resistance"],
    },
    "mechanical-repairs": {
        "name": "Mechanical Repairs",
        "icon": "fa-wrench",
        "image": "mechanical_repairs.webp",
        "intro": "Dependable repairs and practical solutions that keep your vehicle performing at its best.",
        "details": "From unusual noises and leaks to worn components and drivability problems, our team follows a careful inspection process before recommending the work your vehicle actually needs.",
        "benefits": ["Clear fault assessment", "Quality replacement parts", "Transparent recommendations", "Workmanship you can trust"],
    },
    "vehicle-diagnostics": {
        "name": "Vehicle Diagnostics",
        "icon": "fa-laptop",
        "image": "diagnostics.webp",
        "intro": "Modern diagnostics that identify faults quickly and help us fix the right problem first.",
        "details": "Warning lights and intermittent issues require more than guesswork. We combine scan-tool information, live data and physical inspection to trace faults accurately.",
        "benefits": ["Warning-light diagnosis", "Electronic system checks", "Live data analysis", "Clear repair guidance"],
    },
    "engine-services": {
        "name": "Engine Services",
        "icon": "fa-cogs",
        "image": "engine_services.webp",
        "intro": "Complete engine care, from routine tune-ups to investigation of major performance concerns.",
        "details": "Our engine service process is designed to protect reliability, restore performance and help prevent small issues from becoming expensive repairs.",
        "benefits": ["Tune-ups and inspections", "Cooling-system checks", "Leak and noise diagnosis", "Performance troubleshooting"],
    },
    "brake-service": {
        "name": "Brake Service",
        "icon": "fa-stop-circle-o",
        "image": "brake_service.webp",
        "intro": "Professional brake inspection, servicing and replacement for confident stopping power.",
        "details": "Your braking system is essential to vehicle safety. We inspect key components, explain their condition and recommend only the work needed to restore dependable braking.",
        "benefits": ["Pad and rotor inspection", "Brake-fluid checks", "Noise and vibration diagnosis", "Safer braking performance"],
    },
    "maintenance-more": {
        "name": "Maintenance & More",
        "icon": "fa-tint",
        "image": "maintenance.webp",
        "intro": "Routine maintenance and practical auto-care services that support long-term reliability.",
        "details": "Consistent maintenance helps your vehicle last longer and perform better. DriveCore can help you plan the essential services your vehicle needs based on condition and usage.",
        "benefits": ["Oil and filter service", "Fluid and belt checks", "General safety inspection", "Preventive maintenance planning"],
    },
}


class DriveCoreWebsite(http.Controller):

    @http.route("/drivecore/service/<string:slug>", type="http", auth="public", website=True, sitemap=True)
    def service_detail(self, slug, **kwargs):
        service = SERVICES.get(slug)
        if not service:
            raise NotFound()
        return request.render("drivecore_website.service_detail_page", {
            "service": service,
            "service_slug": slug,
        })

    @http.route("/drivecore/book/submit", type="http", auth="public", website=True, methods=["POST"], csrf=True)
    def submit_booking(self, **post):
        if not post.get("name") or not post.get("email") or not post.get("phone"):
            return request.redirect("/book-a-service?error=missing")
        valid_services = {"wheel_alignment", "mechanical_repairs", "diagnostics", "engine_services", "brake_service", "maintenance", "other"}
        service_type = post.get("service_type") if post.get("service_type") in valid_services else "other"
        request.env["drivecore.service.request"].sudo().create({
            "name": post.get("name"),
            "email": post.get("email"),
            "phone": post.get("phone"),
            "vehicle_make": post.get("vehicle_make"),
            "vehicle_model": post.get("vehicle_model"),
            "vehicle_year": post.get("vehicle_year"),
            "registration_number": post.get("registration_number"),
            "service_type": service_type,
            "preferred_date": post.get("preferred_date") or False,
            "preferred_time": post.get("preferred_time") or False,
            "issue_description": post.get("issue_description"),
        })
        return request.redirect("/request-received?type=booking")

    @http.route("/drivecore/contact/submit", type="http", auth="public", website=True, methods=["POST"], csrf=True)
    def submit_contact(self, **post):
        if not post.get("name") or not post.get("email") or not post.get("message"):
            return request.redirect("/contact-us?error=missing")
        request.env["drivecore.contact.request"].sudo().create({
            "name": post.get("name"),
            "email": post.get("email"),
            "phone": post.get("phone"),
            "subject": post.get("subject"),
            "message": post.get("message"),
        })
        return request.redirect("/request-received?type=contact")
