from ctypes import util
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions

from . import utils, models, serializers


# Products
class SingleProductView(APIView):
    """
        docstring
    """

    def get_category(self, title: str):
        """
            Return Category Object
        """
        try:
            return models.Category.objects.get(title=title)
        except models.Category.DoesNotExist:
            return None

    def get_product(self, product_id: int):
        """
            Return Product Object
        """
        try:
            return models.Product.objects.get(product_id=product_id)
        except models.Product.DoesNotExist:
            return None

    def post(self, request):
        """
            docstring
        """
        request_body = request.data

        try:
            # Check Product in Database
            url = request_body["url"]
            product_id = utils.find_product_id_url(url)

            if not product_id:
                response = {
                    "msg": "Invalid URL!"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            if self.get_product(product_id):
                response = {
                    "msg": f"Product dkp-{product_id} is already exists!"
                }
                return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

            # Check Product's Category
            product = utils.single_product(url)
            category = product["category"]
            category_object = self.get_category(category)
            if category_object:
                serialized_category = serializers.CategorySerializer(
                    instance=category_object
                )
                category_id = serialized_category.data["id"]
            else:

                serialized_category = serializers.CategorySerializer(
                    data={"title": category}
                )
                serialized_category.is_valid(raise_exception=True)
                serialized_category.save()
                category_id = serialized_category.data["id"]

            # Save Product in Database
            print(f"CATEGORY = {category_id}")
            product.update(category=category_id)
            serialized_product = serializers.ProductSerializer(data=product)
            serialized_product.is_valid(raise_exception=True)
            serialized_product.save()

        except Exception as error:
            print(error)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serialized_product.data, status=status.HTTP_201_CREATED)


class ListProductsView(SingleProductView):
    """
        docstring
    """

    def post(self, request):
        """
            docstring
        """
        request_body = request.data
        response_products = []

        try:
            url = request_body["url"]
            product_id = utils.find_product_id_url(url)

            if not product_id:
                response = {
                    "msg": "Invalid URL!"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            if self.get_product(product_id):
                response = {
                    "msg": f"Product dkp-{product_id} is already exists!"
                }
                return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

            products = utils.products_list(url)

            for product in products:
                # print(product)
                if self.get_product(product["product_id"]):
                    print(f"Product dkp-{product_id} is already exists!")
                    continue
                category = product["category"]
                category_object = self.get_category(category)
                if category_object:
                    serialized_category = serializers.CategorySerializer(
                        instance=category_object
                    )
                    category_id = serialized_category.data["id"]
                else:

                    serialized_category = serializers.CategorySerializer(
                        data={"title": category}
                    )
                    serialized_category.is_valid(raise_exception=True)
                    serialized_category.save()
                    category_id = serialized_category.data["id"]

                # print(f"PRODUCT #{product['product_id']} | CATEGORY = {category_id}")
                product.update(category=category_id)
                serialized_product = serializers.ProductSerializer(
                    data=product
                )
                serialized_product.is_valid(raise_exception=True)
                serialized_product.save()
                response_products.append(serialized_product.data)

        except Exception as error:
            print(error)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        print(f"{len(response_products)} Products Added to the Database.")
        return Response(response_products, status=status.HTTP_201_CREATED)
