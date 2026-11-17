# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.exceptions import AccessError
from odoo.http import request, route

from odoo.addons.website_sale.controllers.combo_configurator import (
    WebsiteSaleComboConfiguratorController,
)
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.product_configurator import (
    WebsiteSaleProductConfiguratorController,
)


def _check_configurator_allowed(product_template_id):
    """The configurators are part of the add to cart flow and return prices."""
    if not product_template_id:
        return
    template = request.env["product.template"].browse(int(product_template_id)).exists()
    if template and template._website_hide_price_blocks_cart():
        raise AccessError(request.env._("This product cannot be added to the cart."))


class WebsiteSaleHidePrice(WebsiteSale):
    @route()
    def shop(
        self,
        page=0,
        category=None,
        search="",
        min_price=0.0,
        max_price=0.0,
        tags="",
        **post,
    ):
        # Filtering or sorting by price would reveal the hidden prices
        if not request.website.website_show_price:
            min_price = max_price = 0.0
            if (post.get("order") or "").startswith("list_price"):
                post.pop("order")
        return super().shop(
            page=page,
            category=category,
            search=search,
            min_price=min_price,
            max_price=max_price,
            tags=tags,
            **post,
        )


class WebsiteSaleHidePriceProductConfigurator(WebsiteSaleProductConfiguratorController):
    @route()
    def website_sale_product_configurator_get_values(self, *args, **kwargs):
        _check_configurator_allowed(kwargs.get("product_template_id"))
        return super().website_sale_product_configurator_get_values(*args, **kwargs)

    @route()
    def website_sale_product_configurator_update_combination(self, *args, **kwargs):
        _check_configurator_allowed(kwargs.get("product_template_id"))
        return super().website_sale_product_configurator_update_combination(
            *args, **kwargs
        )

    @route()
    def website_sale_product_configurator_get_optional_products(self, *args, **kwargs):
        _check_configurator_allowed(kwargs.get("product_template_id"))
        return super().website_sale_product_configurator_get_optional_products(
            *args, **kwargs
        )


class WebsiteSaleHidePriceComboConfigurator(WebsiteSaleComboConfiguratorController):
    @route()
    def website_sale_combo_configurator_get_data(self, *args, **kwargs):
        _check_configurator_allowed(kwargs.get("product_tmpl_id"))
        return super().website_sale_combo_configurator_get_data(*args, **kwargs)

    @route()
    def website_sale_combo_configurator_get_price(self, *args, **kwargs):
        _check_configurator_allowed(kwargs.get("product_tmpl_id"))
        return super().website_sale_combo_configurator_get_price(*args, **kwargs)
