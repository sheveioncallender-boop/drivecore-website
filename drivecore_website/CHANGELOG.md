# 19.0.2.5.0

- Fixed public Book a Service and Contact form submissions on mobile/Safari when an Odoo session-bound CSRF token expires between page load and submit.
- Replaced session-bound CSRF on the two create-only public enquiry endpoints with same-origin/fetch-metadata validation plus a hidden honeypot.
- Added input trimming/length limits and friendly security retry messages.

# Changelog

## 19.0.2.4.0
- Forced all public-page headings and their nested spans to render white.
- Preserved lime-green emphasis inside heading `em` elements.
- Added an inline critical contrast safeguard after the Odoo frontend assets.
- Added inline title colours in QWeb templates to resist editor/theme overrides.
- Switched to a new stylesheet filename to bypass stale browser and proxy caches.
- Refreshed favicon and asset cache keys.

## 19.0.2.3.0
- Fixed Odoo 19 startup failure caused by the removed `get_resource_path` import.
- Switched favicon loading to the supported `odoo.tools.file_open` API.
- Added a safe fallback so a missing favicon can never prevent registry startup.

## 19.0.2.2.0 — White title system and branded favicon

- Updated the homepage headline to “Complete Auto Care. Expert Service. Every Time.”
- Locked every public website heading to high-contrast white, while preserving lime-green emphasis text.
- Added stronger Odoo-specific title overrides, including text-fill and opacity protection.
- Rebuilt the favicon as a compact DriveCore DC emblem for clear browser-tab visibility.
- Added ICO, 16 px, 32 px, 180 px and 512 px favicon assets with cache-busting URLs.
- Applied the favicon to every Odoo website record during module install or upgrade.

## 19.0.2.1.0 — Homepage guarantee and full visual audit

- Added an Odoo 19 controller extension that serves the DriveCore homepage directly at `/`.
- Reused one canonical homepage content template in both the root controller and `website.homepage` inheritance.
- Reset every website entry point to `/` during install or upgrade.
- Set the DriveCore logo icon as the Odoo website favicon.
- Retired the temporary `/drivecore-home` page from earlier builds.
- Rebuilt and audited Home, About, Services, Book a Service, FAQ, Contact, legal, thank-you, and all service-detail pages.
- Removed inherited white surfaces and enforced dark backgrounds throughout the public website.
- Increased paragraph, label, helper, card, footer, and form text contrast.
- Retained authentic mechanic and workshop photography throughout the design.
- Improved responsive navigation, forms, service cards, calls to action, and footer layouts.

## 19.0.2.0.0 — Full website rebuild

- Replaced the original homepage body with the new dark DriveCore design.
- Added a consistent dark surface system and high-contrast typography.

## 19.0.1.2.0

- Earlier homepage and contrast correction.
