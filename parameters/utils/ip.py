# standard library
from ipaddress import IPv4Address
from ipaddress import IPv6Address


class BaseRange:
    def __repr__(self):
        return "{!s}({!r}, {!r})".format(
            self.__class__.__name__, str(self.start), str(self.end)
        )

    def __str__(self):
        return "{:s}-{:s}".format(self.start, self.end)

    def __contains__(self, other):
        if not isinstance(other, self._address_class):
            raise TypeError(
                "Only {:s} addresses can be checked".format((self._address_class,))
            )
        else:
            return self.start <= other <= self.end

    def __init__(self, start, end):
        if isinstance(start, str):
            start = self._address_class(start)
        if isinstance(end, str):
            end = self._address_class(end)
        if (
            type(start) is not self._address_class
            or type(end) is not self._address_class
        ):
            raise TypeError("Incompatible address classes")
        if start > end:
            raise ValueError("Start address must be lower than end")

        self.start = start
        self.end = end


class IPv4Range(BaseRange):
    """Represents a range of IPv4 addresses"""

    _address_class = IPv4Address


class IPv6Range(BaseRange):
    """Represents a range of IPv6 addresses"""

    _address_class = IPv6Address
