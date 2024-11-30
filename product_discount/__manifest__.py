{
    'name': 'Product Discount',
    'version': '1.0',
    'author': 'BKC',
    'category': 'Sales',
    'summary': 'Adds discount to products',
    'depends': ['product', 'sale','website','sale','account'],
    'data': [
        'views/product_template_view.xml',
        'views/website_product_template.xml',
        'views/website_cart_template.xml',
        'views/website_checkout_template.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'assets': {
                    'web.assets_frontend': [
                        'product_discount/static/src/css/product_discount.css',
                    ],
                },
}
