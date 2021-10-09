# ### Task 4.7
# Implement a class Money to represent value and currency.
# You need to implement methods to use all basic arithmetics expressions
# (comparison, division, multiplication, addition and subtraction).
# Tip: use class attribute exchange rate which is dictionary and stores
# information about exchange rates to your default currency:


class Money:
    exchange_rate_to_usd = {
        'EUR': 0.86,
        'BYN': 2.51,
        'RUB': 72.50,
        'JPY': 110.94
    }

    def __init__(self, value, currency="USD"):
        self.value = value
        self.currency = currency.upper()
        if self.currency != "USD":
            self.exchange_rate_to_usd = {**Money.exchange_rate_to_usd}
            for key, value in Money.exchange_rate_to_usd.items():
                self.exchange_rate_to_usd[key] = self.exchange_rate_to_usd[key] / Money.exchange_rate_to_usd[self.currency]
            self.exchange_rate_to_usd["USD"] = 1 / Money.exchange_rate_to_usd[self.currency]

    def __repr__(self):
        return f"Money({self.value:0.2f}, {self.currency})"

    def __str__(self):
        return f"{self.value:0.2f} {self.currency}"

    def __add__(self, other):
        if isinstance(other, Money):
            return Money((self.value + other.value) if other.currency == self.currency
                         else (self.value + other.value / self.exchange_rate_to_usd[other.currency]), self.currency)
        else:
            return self

    def __radd__(self, other):
        return self

    def __sub__(self, other):
        if isinstance(other, Money):
            return Money((self.value - other.value) if other.currency == self.currency
                         else (self.value - other.value / self.exchange_rate_to_usd[other.currency]), self.currency)
        else:
            return self

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Money(self.value / other, self.currency)
        elif isinstance(other, Money):
            return self.value / other.value if other.currency == self.currency else (self.value / (other.value / self.exchange_rate_to_usd[other.currency]))
        else:
            return self

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Money(self.value * other, self.currency)
        else:
            return self

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Money(other * self.value, self.currency)
        else:
            return self


u = Money(10)
b = Money(2.51, 'byn')
e = Money(1, 'eur')
print(u, b, e)
print(u + b)
print(b + u)
print(e + b)
print(e + 'b')
print(e * 2, 2 * b + e, e / 2, sep=', ', end='\n')
print(u / b)

x = Money(10, "BYN")
y = Money(11)
z = Money(12.34, "EUR")
print(z + 3.11 * x + y * 0.8)

lst = [Money(10, "BYN"), Money(11), Money(12.01, "JPY")]
s = sum(lst)
print(s)
