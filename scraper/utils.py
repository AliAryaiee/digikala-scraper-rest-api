from typing import List

import requests


DIGIKALA = "https://www.digikala.com"


def find_product_id_url(url: str) -> int:
    """
        Extract Product ID From URL
    """
    try:
        return list(
            filter(lambda part: part.startswith("dkp-"), url.split("/"))
        )[0].split("-")[-1]
    except:
        return None


def single_product(url: str) -> dict:
    """
        Product Details
            id
            product_id
            title
            title_en
            price
            rating
            link
            category
    """
    product_id = find_product_id_url(url)
    url = f"https://api.digikala.com/v1/product/{product_id}/"
    product = {}

    try:
        with requests.get(url) as response:
            # Getting Important Data
            response_object: dict = response.json()
            if response_object["status"] // 100 == 4:
                return product

            data: dict = response_object["data"]
            details = data["product"]
            category = data["intrack"]["eventData"]["leafCategory"]
            rating = details["rating"]

            product.update(product_id=details["id"])
            product.update(title=details["title_fa"])
            product.update(title_en=details["title_en"])
            product.update(
                price=data["intrack"]["eventData"]["unitPrice"]
            )
            product.update(rating=rating["rate"])
            product.update(link=DIGIKALA + f"/product/dkp-{product_id}")
            product.update(category=category)

    except Exception as error:
        print(error)

    return product


def related_products(data: List[dict]) -> List[dict]:
    """
        Related products
            id
            product_id
            title
            title_en
            price
            rating
            link
            category
    """
    products = []

    for product in data["products"]:
        item = {}

        category = product["data_layer"]["category"][1:-1].split(",")[-1]

        item.update(product_id=product["id"])
        item.update(title=product["title_fa"])
        item.update(title_en=product["title_en"])
        item.update(
            price=product["default_variant"]["price"]["selling_price"]
        )
        # item.update(rating=product["default_variant"]["rate"])
        item.update(rating=0)
        item.update(link=DIGIKALA + f"/product/dkp-{product['id']}")
        item.update(category=category)
        products.append(item)

    return products


def products_list(url: str) -> dict:
    """
        Product Details
            id
            product_id
            title
            title_en
            price
            rating
            link
            category
    """
    product_id = find_product_id_url(url)
    url = f"https://api.digikala.com/v1/product/{product_id}/"
    products = []

    try:
        with requests.get(url) as response:
            # Getting Important Props
            response_object: dict = response.json()
            if response_object["status"] // 100 == 4:
                return products

            data: dict = response_object["data"]
            details = data["product"]
            category = data["intrack"]["eventData"]["leafCategory"]
            rating = details["rating"]

            # Get Product Details
            product = {}
            product.update(product_id=details["id"])
            product.update(title=details["title_fa"])
            product.update(title_en=details["title_en"])
            product.update(
                price=data["intrack"]["eventData"]["unitPrice"]
            )
            product.update(rating=rating["rate"])
            product.update(link=DIGIKALA + f"/product/dkp-{product_id}")
            product.update(category=category)
            products.append(product)

            # Recommended Items
            recommendations = data["recommendations"]
            default_products = {"products": []}
            relateds = recommendations.get(
                "related_products",
                default_products
            )
            new_related_products = recommendations.get(
                "new_related_products",
                default_products
            )
            also_bought_products = recommendations.get(
                "also_bought_products",
                default_products
            )

            products.extend(related_products(relateds))
            products.extend(related_products(new_related_products))
            products.extend(related_products(also_bought_products))

    except Exception as error:
        print(error)

    return products


if __name__ == "__main__":
    pass
