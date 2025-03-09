from django import forms
from django.utils.translation import gettext_lazy as _

from ..base import Kind, KindField


IPAddressKind = Kind(
    identifier="ip-address",
    name=_("IPv4 or IPv6 address"),
    field=KindField(klass=forms.GenericIPAddressField)
)


IP4AddressKind = Kind(
    identifier="ip4-address",
    name=_("IPv4 address"),
    field=KindField(
        klass=forms.GenericIPAddressField,
        initials={"protocol": "IPv4"},
    )
)


IP6AddressKind = Kind(
    identifier="ip6-address",
    name=_("IPv6 address"),
    field=KindField(
        klass=forms.GenericIPAddressField,
        initials={"protocol": "IPv6"},
    )
)
