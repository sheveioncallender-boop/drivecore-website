from odoo import fields, models


class DriveCoreServiceRequest(models.Model):
    _name = "drivecore.service.request"
    _description = "DriveCore Service Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(required=True, tracking=True)
    email = fields.Char(required=True, tracking=True)
    phone = fields.Char(required=True, tracking=True)
    vehicle_make = fields.Char(tracking=True)
    vehicle_model = fields.Char(tracking=True)
    vehicle_year = fields.Char(tracking=True)
    registration_number = fields.Char(tracking=True)
    service_type = fields.Selection([
        ("wheel_alignment", "Wheel Alignment"),
        ("mechanical_repairs", "Mechanical Repairs"),
        ("diagnostics", "Vehicle Diagnostics"),
        ("engine_services", "Engine Services"),
        ("brake_service", "Brake Service"),
        ("maintenance", "Maintenance & More"),
        ("other", "Other / Not Sure"),
    ], required=True, default="other", tracking=True)
    preferred_date = fields.Date(tracking=True)
    preferred_time = fields.Selection([
        ("morning", "Morning"),
        ("midday", "Midday"),
        ("afternoon", "Afternoon"),
    ], tracking=True)
    issue_description = fields.Text(tracking=True)
    state = fields.Selection([
        ("new", "New"),
        ("contacted", "Contacted"),
        ("booked", "Booked"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ], default="new", required=True, tracking=True)


class DriveCoreContactRequest(models.Model):
    _name = "drivecore.contact.request"
    _description = "DriveCore Contact Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(required=True, tracking=True)
    email = fields.Char(required=True, tracking=True)
    phone = fields.Char(tracking=True)
    subject = fields.Char(tracking=True)
    message = fields.Text(required=True, tracking=True)
    state = fields.Selection([
        ("new", "New"),
        ("replied", "Replied"),
        ("closed", "Closed"),
    ], default="new", required=True, tracking=True)
