# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db.models import Count, Sum
from django.test import TestCase

from tabulate_django import queryset_table
from test_app.models import Account, Country, Order


class BasicTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        uk = Country.objects.create(name="United Kingdom", code="GB")
        france = Country.objects.create(name="France", code="FR")
        germany = Country.objects.create(name="Germany", code="DE")
        alice = Account.objects.create(
            name="Alice Smith", email="alice@smith.example", country=uk
        )
        bob = Account.objects.create(
            name="Bob Jones", email="bob.jones@example.com", country=uk
        )
        charlotte = Account.objects.create(
            name="Charlotte Muller", email="charlie@example.com", country=germany
        )
        dietrich = Account.objects.create(
            name="Dietrich Schmidt", email="dschmidt@example.de", country=germany
        )
        eva = Account.objects.create(
            name="Eva Dupont", email="eva@dupont.example", country=france
        )
        francoise = Account.objects.create(
            name="Francois Michel", email="francois.michel@example.fr", country=france
        )
        Order.objects.create(account=alice, order_date="2021-01-01", order_total=10.00)
        Order.objects.create(account=alice, order_date="2021-02-01", order_total=15.00)
        Order.objects.create(account=alice, order_date="2021-03-01", order_total=20.00)
        Order.objects.create(account=bob, order_date="2021-01-10", order_total=250.00)
        Order.objects.create(
            account=charlotte, order_date="2021-02-10", order_total=10.00
        )
        Order.objects.create(
            account=dietrich, order_date="2021-02-02", order_total=200.00
        )
        Order.objects.create(
            account=dietrich, order_date="2021-02-02", order_total=100.00
        )
        Order.objects.create(account=eva, order_date="2021-03-10", order_total=220.00)
        Order.objects.create(
            account=francoise, order_date="2021-01-15", order_total=220.00
        )

    def test_output_account_fields(self):
        all_accounts = Account.objects.order_by("name")
        table = queryset_table(all_accounts, ["name", "email"], print_result=False)
        expected = """
╒══════════════════╤════════════════════════════╕
│ Name             │ Email                      │
╞══════════════════╪════════════════════════════╡
│ Alice Smith      │ alice@smith.example        │
├──────────────────┼────────────────────────────┤
│ Bob Jones        │ bob.jones@example.com      │
├──────────────────┼────────────────────────────┤
│ Charlotte Muller │ charlie@example.com        │
├──────────────────┼────────────────────────────┤
│ Dietrich Schmidt │ dschmidt@example.de        │
├──────────────────┼────────────────────────────┤
│ Eva Dupont       │ eva@dupont.example         │
├──────────────────┼────────────────────────────┤
│ Francois Michel  │ francois.michel@example.fr │
╘══════════════════╧════════════════════════════╛
""".strip()
        self.assertEqual(expected, table)

    def test_output_foreign_keys(self):
        all_accounts = Account.objects.order_by("name")
        table = queryset_table(
            all_accounts, ["name", "email", "country__name"], print_result=False
        )
        expected = """
╒══════════════════╤════════════════════════════╤════════════════╕
│ Name             │ Email                      │ Country Name   │
╞══════════════════╪════════════════════════════╪════════════════╡
│ Alice Smith      │ alice@smith.example        │ United Kingdom │
├──────────────────┼────────────────────────────┼────────────────┤
│ Bob Jones        │ bob.jones@example.com      │ United Kingdom │
├──────────────────┼────────────────────────────┼────────────────┤
│ Charlotte Muller │ charlie@example.com        │ Germany        │
├──────────────────┼────────────────────────────┼────────────────┤
│ Dietrich Schmidt │ dschmidt@example.de        │ Germany        │
├──────────────────┼────────────────────────────┼────────────────┤
│ Eva Dupont       │ eva@dupont.example         │ France         │
├──────────────────┼────────────────────────────┼────────────────┤
│ Francois Michel  │ francois.michel@example.fr │ France         │
╘══════════════════╧════════════════════════════╧════════════════╛
""".strip()
        self.assertEqual(expected, table)

    def test_alias_headings(self):
        all_accounts = Account.objects.order_by("name")
        table = queryset_table(
            all_accounts,
            ["name", "email", ("country__name", "Residence")],
            print_result=False,
        )
        expected = """
╒══════════════════╤════════════════════════════╤════════════════╕
│ Name             │ Email                      │ Residence      │
╞══════════════════╪════════════════════════════╪════════════════╡
│ Alice Smith      │ alice@smith.example        │ United Kingdom │
├──────────────────┼────────────────────────────┼────────────────┤
│ Bob Jones        │ bob.jones@example.com      │ United Kingdom │
├──────────────────┼────────────────────────────┼────────────────┤
│ Charlotte Muller │ charlie@example.com        │ Germany        │
├──────────────────┼────────────────────────────┼────────────────┤
│ Dietrich Schmidt │ dschmidt@example.de        │ Germany        │
├──────────────────┼────────────────────────────┼────────────────┤
│ Eva Dupont       │ eva@dupont.example         │ France         │
├──────────────────┼────────────────────────────┼────────────────┤
│ Francois Michel  │ francois.michel@example.fr │ France         │
╘══════════════════╧════════════════════════════╧════════════════╛
""".strip()
        self.assertEqual(expected, table)

    def test_aggregate_functions(self):
        all_accounts = Account.objects.order_by("name")
        table = queryset_table(
            all_accounts,
            ["name", "email", "#order", "+order__order_total"],
            print_result=False,
        )
        expected = """
╒══════════════════╤════════════════════════════╤══════════╤══════════════════════╕
│ Name             │ Email                      │   #Order │   +Order Order Total │
╞══════════════════╪════════════════════════════╪══════════╪══════════════════════╡
│ Alice Smith      │ alice@smith.example        │        3 │                   45 │
├──────────────────┼────────────────────────────┼──────────┼──────────────────────┤
│ Bob Jones        │ bob.jones@example.com      │        1 │                  250 │
├──────────────────┼────────────────────────────┼──────────┼──────────────────────┤
│ Charlotte Muller │ charlie@example.com        │        1 │                   10 │
├──────────────────┼────────────────────────────┼──────────┼──────────────────────┤
│ Dietrich Schmidt │ dschmidt@example.de        │        2 │                  300 │
├──────────────────┼────────────────────────────┼──────────┼──────────────────────┤
│ Eva Dupont       │ eva@dupont.example         │        1 │                  220 │
├──────────────────┼────────────────────────────┼──────────┼──────────────────────┤
│ Francois Michel  │ francois.michel@example.fr │        1 │                  220 │
╘══════════════════╧════════════════════════════╧══════════╧══════════════════════╛
""".strip()
        self.assertEqual(expected, table)

    def test_alias_aggregate_functions(self):
        all_accounts = Account.objects.order_by("name")
        table = queryset_table(
            all_accounts,
            [
                "name",
                "email",
                ("#order", "Orders"),
                ("+order__order_total", "Order Value"),
            ],
            print_result=False,
        )
        expected = """
╒══════════════════╤════════════════════════════╤══════════╤═══════════════╕
│ Name             │ Email                      │   Orders │   Order Value │
╞══════════════════╪════════════════════════════╪══════════╪═══════════════╡
│ Alice Smith      │ alice@smith.example        │        3 │            45 │
├──────────────────┼────────────────────────────┼──────────┼───────────────┤
│ Bob Jones        │ bob.jones@example.com      │        1 │           250 │
├──────────────────┼────────────────────────────┼──────────┼───────────────┤
│ Charlotte Muller │ charlie@example.com        │        1 │            10 │
├──────────────────┼────────────────────────────┼──────────┼───────────────┤
│ Dietrich Schmidt │ dschmidt@example.de        │        2 │           300 │
├──────────────────┼────────────────────────────┼──────────┼───────────────┤
│ Eva Dupont       │ eva@dupont.example         │        1 │           220 │
├──────────────────┼────────────────────────────┼──────────┼───────────────┤
│ Francois Michel  │ francois.michel@example.fr │        1 │           220 │
╘══════════════════╧════════════════════════════╧══════════╧═══════════════╛
""".strip()
        self.assertEqual(expected, table)

    def test_alias_aggregate_functions_as_expressions(self):
        all_accounts = Account.objects.order_by("name")
        table = queryset_table(
            all_accounts,
            [
                "name",
                "email",
                (Count("order"), "Orders"),
                (Sum("order__order_total"), "Order Value"),
            ],
            print_result=False,
        )
        expected = """
╒══════════════════╤════════════════════════════╤══════════╤═══════════════╕
│ Name             │ Email                      │   Orders │   Order Value │
╞══════════════════╪════════════════════════════╪══════════╪═══════════════╡
│ Alice Smith      │ alice@smith.example        │        3 │            45 │
├──────────────────┼────────────────────────────┼──────────┼───────────────┤
│ Bob Jones        │ bob.jones@example.com      │        1 │           250 │
├──────────────────┼────────────────────────────┼──────────┼───────────────┤
│ Charlotte Muller │ charlie@example.com        │        1 │            10 │
├──────────────────┼────────────────────────────┼──────────┼───────────────┤
│ Dietrich Schmidt │ dschmidt@example.de        │        2 │           300 │
├──────────────────┼────────────────────────────┼──────────┼───────────────┤
│ Eva Dupont       │ eva@dupont.example         │        1 │           220 │
├──────────────────┼────────────────────────────┼──────────┼───────────────┤
│ Francois Michel  │ francois.michel@example.fr │        1 │           220 │
╘══════════════════╧════════════════════════════╧══════════╧═══════════════╛
""".strip()
        self.assertEqual(expected, table)

    def test_show_keys(self):
        all_accounts = Account.objects.order_by("name")
        table = queryset_table(
            all_accounts,
            [
                "name",
                "email",
                ("#order", "Orders"),
                ("+order__order_total", "Order Value"),
            ],
            show_keys=True,
            print_result=False,
        )
        expected = """
╒══════════════════╤════════════════════════════╤═════════════════════════╤═════════════════════════════════════════╕
│ Name (name)      │ Email (email)              │   Orders (_count_order) │   Order Value (_sum_order__order_total) │
╞══════════════════╪════════════════════════════╪═════════════════════════╪═════════════════════════════════════════╡
│ Alice Smith      │ alice@smith.example        │                       3 │                                      45 │
├──────────────────┼────────────────────────────┼─────────────────────────┼─────────────────────────────────────────┤
│ Bob Jones        │ bob.jones@example.com      │                       1 │                                     250 │
├──────────────────┼────────────────────────────┼─────────────────────────┼─────────────────────────────────────────┤
│ Charlotte Muller │ charlie@example.com        │                       1 │                                      10 │
├──────────────────┼────────────────────────────┼─────────────────────────┼─────────────────────────────────────────┤
│ Dietrich Schmidt │ dschmidt@example.de        │                       2 │                                     300 │
├──────────────────┼────────────────────────────┼─────────────────────────┼─────────────────────────────────────────┤
│ Eva Dupont       │ eva@dupont.example         │                       1 │                                     220 │
├──────────────────┼────────────────────────────┼─────────────────────────┼─────────────────────────────────────────┤
│ Francois Michel  │ francois.michel@example.fr │                       1 │                                     220 │
╘══════════════════╧════════════════════════════╧═════════════════════════╧═════════════════════════════════════════╛
""".strip()
        self.assertEqual(expected, table)

    def test_filter(self):
        all_accounts = Account.objects.order_by("name")
        table = queryset_table(
            all_accounts,
            [
                "name",
                "email",
                ("#order", "Orders"),
                ("+order__order_total", "Order Value"),
            ],
            filter={"_count_order__gt": 1},
            print_result=False,
        )
        expected = """
╒══════════════════╤═════════════════════╤══════════╤═══════════════╕
│ Name             │ Email               │   Orders │   Order Value │
╞══════════════════╪═════════════════════╪══════════╪═══════════════╡
│ Alice Smith      │ alice@smith.example │        3 │            45 │
├──────────────────┼─────────────────────┼──────────┼───────────────┤
│ Dietrich Schmidt │ dschmidt@example.de │        2 │           300 │
╘══════════════════╧═════════════════════╧══════════╧═══════════════╛
""".strip()
        self.assertEqual(expected, table)

    def test_format_string(self):
        all_accounts = Account.objects.order_by("name")
        table = queryset_table(
            all_accounts,
            [
                "name",
                ("f|https://example.com/admin/orders/account/{id}/change", "Edit link"),
            ],
            print_result=False,
        )
        expected = """
╒══════════════════╤═══════════════════════════════════════════════════╕
│ Name             │ Edit link                                         │
╞══════════════════╪═══════════════════════════════════════════════════╡
│ Alice Smith      │ https://example.com/admin/orders/account/1/change │
├──────────────────┼───────────────────────────────────────────────────┤
│ Bob Jones        │ https://example.com/admin/orders/account/2/change │
├──────────────────┼───────────────────────────────────────────────────┤
│ Charlotte Muller │ https://example.com/admin/orders/account/3/change │
├──────────────────┼───────────────────────────────────────────────────┤
│ Dietrich Schmidt │ https://example.com/admin/orders/account/4/change │
├──────────────────┼───────────────────────────────────────────────────┤
│ Eva Dupont       │ https://example.com/admin/orders/account/5/change │
├──────────────────┼───────────────────────────────────────────────────┤
│ Francois Michel  │ https://example.com/admin/orders/account/6/change │
╘══════════════════╧═══════════════════════════════════════════════════╛
""".strip()
        self.assertEqual(expected, table)

    def test_slice(self):
        all_accounts = Account.objects.order_by("name")
        table = queryset_table(
            all_accounts, ["name", "email"], print_result=False, slice=(2, 4)
        )
        expected = """
╒══════════════════╤═════════════════════╕
│ Name             │ Email               │
╞══════════════════╪═════════════════════╡
│ Charlotte Muller │ charlie@example.com │
├──────────────────┼─────────────────────┤
│ Dietrich Schmidt │ dschmidt@example.de │
╘══════════════════╧═════════════════════╛
""".strip()
        self.assertEqual(expected, table)

    def test_tsv(self):
        all_accounts = Account.objects.order_by("name")
        table = queryset_table(
            all_accounts, ["name", "email"], print_result=False, table_format="tsv"
        )
        expected = """
Alice Smith	alice@smith.example
Bob Jones	bob.jones@example.com
Charlotte Muller	charlie@example.com
Dietrich Schmidt	dschmidt@example.de
Eva Dupont	eva@dupont.example
Francois Michel	francois.michel@example.fr
""".strip()
        self.assertEqual(expected, table)
