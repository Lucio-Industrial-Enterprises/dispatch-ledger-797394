# Warehouse tools

Small Python utilities for warehouse order and shipping workflows.

Run the tests with `python3 -m unittest discover -s tests -v`.

## Shipping

`shipping_quote(weight_kg, zone, service="standard")` returns a shipping quote
in dollars, rounded to two decimal places. Zones are `local` and `regional`;
weights must be positive. Standard shipping costs $5 for local or $8 for regional,
plus $1.50 per kilogram. Express adds $7 to standard shipping in either zone.
Omitting `service` preserves standard pricing. Invalid weights, unknown zones,
and unknown services raise `ValueError`.

```python
from warehouse.rates import shipping_quote

shipping_quote(2, "local")                     # 8.0 (standard)
shipping_quote(2, "regional", "standard")      # 11.0
shipping_quote(2, "local", service="express")  # 15.0
shipping_quote(2, "regional", "express")       # 18.0
```

The command-line entry point prints a dollar-formatted quote. `--service` accepts
`standard` (the default) or `express`; other services are rejected.

```sh
python3 -m warehouse.cli 2 local                    # $8.00
python3 -m warehouse.cli 2 regional --service standard  # $11.00
python3 -m warehouse.cli 2 local --service express   # $15.00
python3 -m warehouse.cli 2 regional --service express  # $18.00
```
