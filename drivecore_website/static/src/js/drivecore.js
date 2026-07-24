(function () {
    "use strict";

    function ready(callback) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", callback, { once: true });
        } else {
            callback();
        }
    }

    ready(function () {
        var toggle = document.querySelector(".dc-menu-toggle");
        var menu = document.getElementById("dcMobileMenu");
        var serviceToggle = document.querySelector(".dc-mobile-services-toggle");
        var submenu = document.querySelector(".dc-mobile-submenu");

        function closeMenu() {
            if (!toggle || !menu) return;
            toggle.setAttribute("aria-expanded", "false");
            menu.setAttribute("aria-hidden", "true");
            menu.classList.remove("is-open");
            document.documentElement.classList.remove("dc-menu-open");
        }

        if (toggle && menu) {
            toggle.addEventListener("click", function () {
                var opening = toggle.getAttribute("aria-expanded") !== "true";
                toggle.setAttribute("aria-expanded", opening ? "true" : "false");
                menu.setAttribute("aria-hidden", opening ? "false" : "true");
                menu.classList.toggle("is-open", opening);
                document.documentElement.classList.toggle("dc-menu-open", opening);
            });

            menu.querySelectorAll("a").forEach(function (link) {
                link.addEventListener("click", closeMenu);
            });
        }

        if (serviceToggle && submenu) {
            serviceToggle.addEventListener("click", function () {
                var opening = !submenu.classList.contains("is-open");
                submenu.classList.toggle("is-open", opening);
                serviceToggle.classList.toggle("is-open", opening);
            });
        }

        document.querySelectorAll(".dc-faq-item > button").forEach(function (button) {
            button.addEventListener("click", function () {
                var item = button.closest(".dc-faq-item");
                var opening = !item.classList.contains("is-open");
                document.querySelectorAll(".dc-faq-item.is-open").forEach(function (openItem) {
                    if (openItem !== item) openItem.classList.remove("is-open");
                });
                item.classList.toggle("is-open", opening);
            });
        });

        var currentPath = window.location.pathname.replace(/\/$/, "") || "/";
        document.querySelectorAll("[data-dc-nav]").forEach(function (link) {
            var target = link.getAttribute("data-dc-nav").replace(/\/$/, "") || "/";
            var active = target === "/" ? currentPath === "/" : currentPath === target || currentPath.indexOf(target + "/") === 0;
            link.classList.toggle("is-active", active);
        });

        var serviceSelect = document.querySelector('select[name="service_type"]');
        if (serviceSelect) {
            var params = new URLSearchParams(window.location.search);
            var slug = params.get("service");
            var serviceMap = {
                "wheel-alignment": "wheel_alignment",
                "mechanical-repairs": "mechanical_repairs",
                "vehicle-diagnostics": "diagnostics",
                "engine-services": "engine_services",
                "brake-service": "brake_service",
                "maintenance-more": "maintenance"
            };
            if (slug && serviceMap[slug]) serviceSelect.value = serviceMap[slug];
        }

        var dateInput = document.querySelector('input[name="preferred_date"]');
        if (dateInput) {
            var today = new Date();
            var yyyy = today.getFullYear();
            var mm = String(today.getMonth() + 1).padStart(2, "0");
            var dd = String(today.getDate()).padStart(2, "0");
            dateInput.min = yyyy + "-" + mm + "-" + dd;
        }
    });
})();
