import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    def test_standard_rates(self):
        for zone, expected in (("local", 8.0), ("regional", 11.0)):
            with self.subTest(zone=zone):
                self.assertEqual(shipping_quote(2, zone), expected)
                self.assertEqual(shipping_quote(2, zone, "standard"), expected)

    def test_express_rates(self):
        for zone, expected in (("local", 15.0), ("regional", 18.0)):
            with self.subTest(zone=zone):
                self.assertEqual(shipping_quote(2, zone, "express"), expected)

    def test_rounding_and_surcharge(self):
        for zone, base in (("local", 5.0), ("regional", 8.0)):
            for weight in (0.1, 1.234, 10):
                with self.subTest(zone=zone, weight=weight):
                    standard = shipping_quote(weight, zone)
                    express = shipping_quote(weight, zone, service="express")
                    self.assertEqual(standard, round(base + 1.5 * weight, 2))
                    self.assertEqual(express, round(standard + 7, 2))

    def test_invalid_weight(self):
        for service in ("standard", "express"):
            for weight in (0, -1):
                with self.subTest(service=service, weight=weight):
                    with self.assertRaisesRegex(ValueError, "weight must be positive"):
                        shipping_quote(weight, "local", service=service)

    def test_invalid_zone(self):
        for service in ("standard", "express"):
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown zone"):
                    shipping_quote(2, "international", service=service)

    def test_unknown_service(self):
        for service in ("overnight", "", "EXPRESS"):
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown service"):
                    shipping_quote(2, "local", service=service)
