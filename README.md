
# Digikala Scraper REST API

This application retrieve all related products on a product page of Digikala and then save the all products in the database.

## Installation

Extract digikala-scraper-rest-api files and then run these command:
* You need Python v3.8 minimum
```bash
  virtualenv env
  env\scripts\activate
  pip install -r requirements.txt
  python manage.py runserver
```

API will run on port 8000

```
  localhost:8000
```
## API Reference

### Save and retrive a single product

```http
  POST /digikala/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `url` | `string` | **Required** (Digikala Product Page URL) |

This endpoint save a single product (just the product itself)

### Save and retrive a list of products

```http
  POST /digikala/list/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `url`      | `string` | **Required** (Digikala Product Page URL) |

This endpoint save the product itself and all related products.


## Description

When a product in Digikala is called, a request will be sent to the server of Digikala that contains *productID*.
The response contains information about the product itself and related products.
We can use Digikala's API for retrieving related products.
