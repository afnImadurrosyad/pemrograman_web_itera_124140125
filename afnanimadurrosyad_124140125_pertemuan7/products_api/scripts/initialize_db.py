import transaction
from pyramid.paster import get_appsettings, setup_logging
from sqlalchemy import engine_from_config
from sqlalchemy import select

from ..models import get_database_url, get_session_factory, get_tm_session
from ..models.category import Category
from ..models.product import Product


def main():
    config_uri = 'development.ini'
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    settings['sqlalchemy.url'] = get_database_url()
    engine = engine_from_config(settings, 'sqlalchemy.')
    session_factory = get_session_factory(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        seed_categories = [
            Category(
                name='Elektronik',
                description='Perangkat elektronik seperti laptop dan smartphone',
                is_active=True,
            ),
            Category(
                name='Pakaian',
                description='Pakaian dan aksesori fesyen',
                is_active=True,
            ),
        ]
        categories = {}
        for item in seed_categories:
            existing = dbsession.execute(
                select(Category).where(Category.name == item.name)
            ).scalar_one_or_none()
            if existing is None:
                dbsession.add(item)
                dbsession.flush()
                categories[item.name] = item
            else:
                categories[item.name] = existing

        seed_products = [
            Product(
                name='Laptop Premium',
                description='High performance laptop',
                price=1299.99,
                sku='LP1001',
                category_id=categories['Elektronik'].id,
                is_active=True,
            ),
            Product(
                name='Smartphone Pro',
                description='Latest model smartphone',
                price=899.99,
                sku='SP2002',
                category_id=categories['Elektronik'].id,
                is_active=True,
            ),
            Product(
                name='Kemeja Formal',
                description='Kemeja lengan panjang bahan katun',
                price=249.99,
                sku='KM3003',
                category_id=categories['Pakaian'].id,
                is_active=True,
            ),
        ]
        for item in seed_products:
            existing = dbsession.execute(
                select(Product).where(Product.sku == item.sku)
            ).scalar_one_or_none()
            if existing is None:
                dbsession.add(item)
        print("Berhasil memasukkan data seeding awal kategori dan produk!")


if __name__ == '__main__':
    main()
