r"""
>>> from decimal import Decimal
>>> from django import db
>>> from satchmo.product.models import *

# Create option groups and their options
>>> sizes = OptionGroup.objects.create(name="sizes", sort_order=1)
>>> option_small = Option.objects.create(optionGroup=sizes, name="Small", value="small", displayOrder=1)
>>> option_large = Option.objects.create(optionGroup=sizes, name="Large", value="large", displayOrder=2, price_change=1)
>>> colors = OptionGroup.objects.create(name="colors", sort_order=2)
>>> option_black = Option.objects.create(optionGroup=colors, name="Black", value="black", displayOrder=1)
>>> option_white = Option.objects.create(optionGroup=colors, name="White", value="white", displayOrder=2, price_change=3)

# Change an option
>>> option_white.price_change = 5
>>> option_white.displayOrder = 2
>>> option_white.save()

# You can't have two options with the same value in an option group
>>> option_white.value = "black"
>>> try:
...     option_white.save()
...     assert False
... except db.IntegrityError: pass
>>> db.transaction.rollback()

# Check the values that were saved to the database
>>> option_white = Option.objects.get(id=option_white.id)
>>> ((option_white.value, option_white.price_change, option_white.displayOrder)
... == (u'white', 5, 2))
True

# Create a configurable product
>>> django_shirt = Product.objects.create(slug="django-shirt", name="Django shirt")
>>> shirt_price = Price.objects.create(product=django_shirt, price="10.5")
>>> django_config = ConfigurableProduct.objects.create(product=django_shirt)
>>> django_config.option_group.add(sizes, colors)
>>> django_config.option_group.order_by('name')
[<OptionGroup: colors>, <OptionGroup: sizes>]
>>> django_config.save()

# Create a product variation
>>> white_shirt = Product.objects.create(slug="django-shirt_small_white", name="Django Shirt (White/Small)")
>>> pv_white = ProductVariation.objects.create(product=white_shirt, parent=django_config)
>>> pv_white.options.add(option_white, option_small)
>>> pv_white.unit_price == Decimal("15.50")
True

# Create a product with a slug that could conflict with an automatically
# generated product's slug.
>>> clash_shirt = Product.objects.create(slug="django-shirt_small_black", name="Django Shirt (Black/Small)")

# Automatically create the rest of the product variations
>>> django_config.create_subs = True
>>> django_config.save()
>>> ProductVariation.objects.filter(parent=django_config).count()
4
"""

if __name__ == "__main__":
    import doctest
    doctest.testmod()

