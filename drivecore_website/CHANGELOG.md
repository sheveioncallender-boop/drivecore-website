
## 19.0.1.2.0
- Added a real published DriveCore homepage page at `/drivecore-home`.
- Configured Odoo root `/` to internally reroute to the DriveCore homepage instead of `/shop`.
- Added an upgrade-safe homepage activation method for existing databases.
- Increased dark-theme paragraph, helper, form, card and footer text contrast.
- Updated direct asset cache versions.

# 19.0.1.1.0

- Rebuilt the visual direction around a premium black automotive palette.
- Replaced generated people/workshop artwork with authentic licensed photography.
- Added real-photo service cards for all six primary service categories.
- Added real-photo internal page heroes, booking imagery and About imagery.
- Added stronger global dark-background enforcement and cache-busted assets.
- Added photography credits and optimized all new images to WebP.

# Changelog

## 19.0.1.0.2
- Force the default website homepage URL back to `/` during install and module upgrades.
- Prevent Odoo eCommerce configuration from opening `/shop` as the DriveCore homepage.


## 19.0.1.0.1 — 2026-07-24
- Fixed the Odoo 19 service-request search view by removing unsupported `expand` and `string` attributes from the search-view `<group>` container.
- Kept the Service and Status group-by filters available as valid root-level search filters.

## 19.0.1.0.0 — Initial release

- Complete DriveCore branded Odoo website
- Global header, footer and favicon
- Responsive desktop and mobile layouts
- Service and contact request backend models
- Direct-loaded CSS and JavaScript
