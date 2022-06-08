import re


# Copied from Django:
# https://github.com/django/django/blob/main/django/core/validators.py#L68
_ul = "\u00a1-\uffff"  # Unicode letters range (must not be a raw string).
# IP patterns
_ipv4_re = (
    r"(?:0|25[0-5]|2[0-4][0-9]|1[0-9]?[0-9]?|[1-9][0-9]?)"
    r"(?:\.(?:0|25[0-5]|2[0-4][0-9]|1[0-9]?[0-9]?|[1-9][0-9]?)){3}"
)
_ipv6_re = r"\[[0-9a-f:.]+\]"  # (simple regex, validated later)
# Host patterns
_hostname_re = r"[a-z" + _ul + r"0-9_](?:[a-z" + _ul + r"0-9-_]{0,61}[a-z" + _ul + r"0-9_])?"
# Max length for domain name labels is 63 characters per RFC 1034 sec. 3.1
_domain_re = r"(?:\.(?!-)[a-z" + _ul + r"0-9-_]{1,63}(?<!-))*"
_tld_re = (
    r"\."  # dot
    r"(?!-)"  # can't start with a dash
    r"(?:[a-z" + _ul + "-_]{2,63}"  # domain label
    r"|xn--[a-z0-9]{1,59})"  # or punycode label
    r"(?<!-)"  # can't end with a dash
    r"\.?"  # may have a trailing dot
)
_host_re = "(" + _hostname_re + _domain_re + _tld_re + "|localhost)"
VALID_URL = re.compile(
    r"^(?P<scheme>https?://)?"  # scheme is validated separately
    r"(?P<user>[^\s:@/]+(?P<pass>:[^\s:@/]*)?@)?"  # user:pass authentication
    r"(?P<domain>" + _ipv4_re + "|" + _ipv6_re + "|" + _host_re + ")"  # domain
    r"(?P<port>:[0-9]{1,5})?"  # port
    r"(?P<rest>/?|[/?]\S+)?$",
    re.IGNORECASE,
)

WHITESPACE = re.compile(r"\s+", re.IGNORECASE)
