# Inventory Management System (IMS)

A small Flask REST API for tracking products, suppliers, and stock transactions.
Data is stored **in memory** (plain Python objects, no database) and is reset
every time the app restarts — this project is meant to run before you've
covered databases.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

The API runs at `http://127.0.0.1:5000`.

## Web UI

Open `http://127.0.0.1:5000/` in a browser for a basic HTML front end (plain
forms and tables, no JavaScript) to add/delete products and suppliers, and
record stock transactions:

| Page | Path |
|---|---|
| Home | `/` |
| Products | `/ui/products` |
| Suppliers | `/ui/suppliers` |
| Transactions | `/ui/transactions` |

This UI is separate from the JSON API below — it's there so you can see the
app working without a REST client, and calls the same in-memory store.

## Entities

- **Product**: `id, name, sku, unit_price, quantity_on_hand`
- **Supplier**: `id, name, contact_email`
- **Transaction**: `id, product_id, supplier_id, type (IN/OUT), quantity, transaction_date`

## JSON API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/products` | List all products |
| POST | `/products` | Create a product |
| GET | `/products/<id>` | Get one product |
| PUT | `/products/<id>` | Update a product |
| DELETE | `/products/<id>` | Delete a product |
| GET | `/products/<id>/stock-level` | Current quantity on hand |
| GET | `/suppliers` | List all suppliers |
| POST | `/suppliers` | Create a supplier |
| GET | `/suppliers/<id>` | Get one supplier |
| PUT | `/suppliers/<id>` | Update a supplier |
| DELETE | `/suppliers/<id>` | Delete a supplier |
| POST | `/transactions` | Record a stock movement (`product_id`, `type`: IN/OUT, `quantity`, optional `supplier_id`) |
| GET | `/transactions?product_id=&supplier_id=` | Look up transactions |

## Tests

This project uses pytest for automated testing and Playwright for end-to-end (E2E) browser testing.

Install the Playwright Chromium browser:

```bash
python -m playwright install chromium
```

Run all tests:

```bash
python -m pytest
```

Run the E2E tests with the browser visible:
```bash
python -m pytest tests/e2e -v --headed
```

The E2E tests use Playwright to simulate user interactions with the web interface, such as filling out forms, clicking buttons, and verifying the results. Each test creates the data it needs so tests can run independently.

## Docker

Build the Docker image from the project folder:

```bash
docker build -t cisc327-group91 .
```

Run the Docker container:

```bash
docker run --rm -p 5000:5000 cisc327-group91
```

The application runs at http://localhost:5000 and uses port 5000. Flask listens on 0.0.0.0 so it can be accessed from outside the container.

To stop the container, press Ctrl+C in the terminal where it is running. The --rm option automatically removes the container after it stops.

##E2E Tests with Docker
The same E2E tests should be run against the Docker container to verify that the application behaves consistently in both environments.

First, stop the locally running Flask application and start the Docker container:

```bash
docker run --rm -p 5000:5000 cisc327-group91
```

Open another terminal, activate the virtual environment, and run:

```bash
python -m pytest tests/e2e -v --headed
```

The tests access the application at http://127.0.0.1:5000, which is mapped to the Docker container.

## Docker Hub
The Docker image is available through the following public Docker Hub repository:

```bash
https://hub.docker.com/r/bhealy103/cisc327-group91/tags
```

Download the image:

```bash
docker pull bhealy103/cisc327-group91:latest
```

Run the downloaded image:

```bash
docker run --rm -p 5000:5000 bhealy103/cisc327-group91:latest
```

## Data Persistence
The application stores data in memory using Python objects. Products, suppliers, and transactions are reset whenever the application restarts or the Docker container stops. No database or Docker volumes are used.

## Technologies Used
- Pyhon
- Flask
- pytest
- Playwright
- Chromium
- Docker