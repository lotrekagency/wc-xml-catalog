# WC XML Catalog

Microservice for generating xml catalogs from WooCommerce.

Xml files will be stored in `/app/feeds`

## Use it in Compose

    xmlcatalog:
        image: lotrekagency/wc_xml_catalog
        volumes:
            - ./xmlfeeds:/app/feeds
        depends_on:
            - redis
        env_file: ./envs/prod/myxmlcatalog.env

## Configure it using env variables

Available variables are

    WOO_HOST=https://www.mywoocommerce.com/wp-json/wc/v3
    LANGUAGES=it,en
    WOO_CONSUMER_KEY=ck_f4k3889898tgddfrr709eaade5e39a361c782
    WOO_CONSUMER_SECRET=cs_4g41nf4ke69797adsas23458af18253aad51a
    XML_SITE_NAME=My Woo Commerce
    XML_SITE_HOST=www.mywoocommerce.com
    XML_GOOGLE_PRODUCT_CATEGORY=11211
