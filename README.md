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

## Configure it
In order to configure it properly it we recommend to configure some environment variables and the setup files.

Available environment variables are

    WOO_HOST=https://www.mywoocommerce.com/wp-json/wc/v3
    LANGUAGES=it,en
    WOO_CONSUMER_KEY=ck_f4k3889898tgddfrr709eaade5e39a361c782
    WOO_CONSUMER_SECRET=cs_4g41nf4ke69797adsas23458af18253aad51a
    XML_SITE_NAME=My Woo Commerce
    XML_SITE_HOST=www.mywoocommerce.com
    XML_GOOGLE_PRODUCT_CATEGORY=11211

The setup files are `config.json` and `mapping.json`.

The config file contains all the variations to the product objects to let the algorithm generate the XML feed easily.
Example of config file is

    {
        "products" : {
            "attributes" : {
                "sku" : {
                    "attribute" : {
                        "field" : "id"
                    }
                },
                "name" : {
                    "attribute" : {
                        "path" : "meta_data(key=title)",
                        "field" : "value"
                    }
                }
            }
        },
        "variations" : {
            "attributes" : {
                "variation_parent_id" : {
                    "attribute" : {
                        "from" : "parent",
                        "field" : "id"
                    }
                },
                "categories" : {
                    "attribute" : {
                        "from" : "parent",
                        "field" : "categories"                
                    }
                }
            }
        }
    }

It contains all the rules to the `Product` and `ProductVariation` objects. Each object of these two types will contain the attributes specified in the JSON file.
In order to copy some attributes sometimes it's required to pass by attribute paths: the `path` statement indicates to the interpreter the path to the `field` statement. It's possible to select a path from a list of objects by array conditions (example `categories[0]`) or key value conditions (example `meta_data(key=title)`)
Product variations objects can inherit parent product attributes by specifying the `"from" : "parent"` statement. The only one mandatory statement is `field`, the rest of abovementioned statements is optional.


The mapping file it too is a JSON file and it contains all the references between products objects and the XML feed attributes.
Example of mapping file is

    {
        "switcher_google" : {
            "True" : "in stock",
            "False" : "out of stock"
    },
        "switcher_item" : {
            "g:brand" : {
                "static" : {
                    "variable" : "settings.XML_SITE_NAME"
                }
            },
            "g:id" : {
                "attribute" : "id"
            },
            "g:title" : {
                "attribute" : "name"
            },
            "g:description" : {
                "static" : "Example description"
            }
            "g:availability" : {
                "attribute" : "stock_status",
                "replace" : {
                    "variable" : "utils.switcher_google"
                }
            }
        }
    }
The mapping file contains two switchers: `switcher_google` and `switcher_item`.
The google switcher contains all the replacements of certain strings with Google-like statements.
It's possible to call the google switcher by calling it with the `replace` statement.
The item switcher contains all the references between XML feed attributes and products attributes.
XML file attributes can be referenced by three types of statements: `attribute` which references to the specified object field, `static` which contains a static string, `list` which repeats feed attributes for every dict contained.
It's possibile to reference feed attributes to algorithm variables with the `variable` statement specifying the variable path.

The setup of these two files let users to generate customized feeds for Google Merchant and Facebook Catalogs.

## Test it

    cd tests/
    pytest .