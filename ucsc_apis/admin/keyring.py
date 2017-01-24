# Copyright 2017 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module performs the operation related to key management.
"""
from ucscsdk.ucscexception import UcscOperationError
from ..common.utils import get_device_profile_dn
ucsc_base_dn = get_device_profile_dn(name="default")


def key_ring_create(handle, name, descr=None, tp=None,
                    cert=None, regen="no", modulus="mod2048", **kwargs):
    """
    Creates a key ring

    Args:
        handle (ucschandle)
        name (string): name
        descr (string): description
        tp (string): tp
        cert (string): certificate
        regen (string): regen, "false", "no", "true", "yes"
        modulus (string): modulus, valid values are
            "mod2048", "mod2560", "mod3072", "mod3584", "mod4096", "modinvalid"
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        PkiKeyRing: managed object

    Example:
        key_ring = key_ring_create(handle, name="mykeyring", regen="yes")
    """

    from ucscsdk.mometa.pki.PkiKeyRing import PkiKeyRing

    mo = PkiKeyRing(parent_mo_or_dn=ucsc_base_dn + "/pki-ext",
                    name=name,
                    descr=descr, tp=tp, cert=cert,
                    regen=regen, modulus=modulus)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def key_ring_get(handle, name):
    """
    Gets the key ring

    Args:
        handle (UcscHandle)
        name (string): name

    Returns:
        PkiKeyRing: managed object OR None

    Example:
        key_ring = key_ring_get(handle, name="mykeyring")
    """

    dn = ucsc_base_dn + "/pki-ext/keyring-" + name
    return handle.query_dn(dn)


def key_ring_exists(handle, name, **kwargs):
    """
    Checks if a key ring exists

    Args:
        handle (UcscHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        key_ring = key_ring_exists(handle, name="mykeyring")
    """

    mo = key_ring_get(handle, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def key_ring_modify(handle, name, **kwargs):
    """
    Modifies a key ring

    Args:
        handle (UcscHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        PkiKeyRing : Managed object

    Raises:
        UcscOperationError: if PkiKeyRing is not present

    Example:
        key_ring = key_ring_modify(handle, name="test_kr", regen="no")
    """

    mo = key_ring_get(handle, name)
    if not mo:
        raise UcscOperationError("key_ring_modify",
                                 "keyring '%s' does not exist" % name)

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def key_ring_delete(handle, name):
    """
    Deletes a key ring

    Args:
        handle (UcscHandle)
        name (string): name

    Returns:
        none

    Raises:
        UcscOperationError: if pkikeyring mo is not present

    Example:
        key_ring_delete(handle, name="mykeyring")
    """

    mo = key_ring_get(handle, name)
    if not mo:
        raise UcscOperationError("key_ring_delete",
                                 "keyring '%s' does not exist" % name)

    handle.remove_mo(mo)
    handle.commit()


def certificate_request_add(handle, name, dns=None, locality=None, state=None,
                            country=None, org_name=None, org_unit_name=None,
                            email=None, pwd=None, subj_name=None, ip="0.0.0.0",
                            ip_a="0.0.0.0", ip_b="0.0.0.0", ipv6="::",
                            ipv6_a="::", ipv6_b="::", **kwargs):
    """
    Adds a certificate request to keyring

    Args:
        handle (UcscHandle)
        name (string): KeyRing name
        dns (string): dns
        locality (string): locality owner
        state (string): state
        country (string): country
        org_name (string): org_name
        org_unit_name (string): org_unit_name
        email (string): email
        pwd (string): pwd
        subj_name (string): subj_name
        ip (string): ipv4
        ip_a (string):
        ip_b (string):
        ipv6 (string):
        ipv6_a (string):
        ipv6_b (string):
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        PkiCertReq: Managed object

    Raises:
        UcscOperationError: If PkiKeyRing is not present

    Example:
        certificate_request_add(handle, name="test_kr", dns="10.10.10.100",
                                country="IN")
    """

    from ucscsdk.mometa.pki.PkiCertReq import PkiCertReq

    dn = ucsc_base_dn + "/pki-ext/keyring-" + name
    obj = handle.query_dn(dn)
    if not obj:
        raise UcscOperationError("certificate_request_add",
                                 "keyring '%s' does not exist" % dn)

    mo = PkiCertReq(parent_mo_or_dn=obj,
                    dns=dns,
                    locality=locality,
                    state=state,
                    country=country,
                    org_name=org_name,
                    org_unit_name=org_unit_name,
                    email=email,
                    pwd=pwd,
                    subj_name=subj_name,
                    ip=ip,
                    ip_a=ip_a,
                    ip_b=ip_b,
                    ipv6=ipv6,
                    ipv6_a=ipv6_a,
                    ipv6_b=ipv6_b)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def certificate_request_get(handle, name):
    """
    Checks if a certificate request exists

    Args:
        handle (UcscHandle)
        name (string): KeyRing name

    Returns:
        PkiCertReq: Managed object OR None

    Example:
        key_ring = key_ring_create(handle, name="mykeyring")

        certificate_request_get(handle, key_ring="keyring")
    """

    dn = ucsc_base_dn + "/pki-ext/keyring-" + name + "/certreq"
    return handle.query_dn(dn)


def certificate_request_exists(handle, name, **kwargs):
    """
    Checks if a certificate request exists

    Args:
        handle (UcscHandle)
        name (string): KeyRing name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        key_ring = key_ring_create(handle, name="mykeyring")

        certificate_request_exists(handle, key_ring="keyring")
    """

    mo = certificate_request_get(handle, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


'''
Note: certificate_request_modify is not possible
'''


def certificate_request_remove(handle, name):
    """
    Removes a certificate request from keyring

    Args:
        handle (UcscHandle)
        name (string): KeyRing name

    Returns:
        None

    Raises:
        UcscOperationError: If PkiCertReq is not present

    Example:
        key_ring = key_ring_create(handle, name="mykeyring")

        certificate_request_remove(handle, key_ring=key_ring)

    """

    mo = certificate_request_get(handle, name)
    if not mo:
        raise UcscOperationError(
                "certificate_request_remove",
                "keyring certificate '%s' does not exist" % name)

    handle.remove_mo(mo)
    handle.commit()


def trusted_point_create(handle, name, descr=None, cert_chain=None, **kwargs):
    """
    Creates a trusted point

    Args:
        handle (ucschandle)
        name (string): name
        descr (string): description
        cert_chain (string): chain of certificate
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        PkiTP: managed object

    Example:
        trusted_point = trusted_point_create(handle, name="mytrustedpoint")
    """

    from ucscsdk.mometa.pki.PkiTP import PkiTP

    mo = PkiTP(parent_mo_or_dn=ucsc_base_dn + "/pki-ext",
               name=name,
               descr=descr,
               cert_chain=cert_chain)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def trusted_point_get(handle, name):
    """
    Checks if a trusted point exists

    Args:
        handle (ucschandle)
        name (string): name

    Returns:
        PkiTP: managed object OR None

    Example:
        key_ring = trusted_point_get(handle, name="mytrustedpoint")
    """

    dn = ucsc_base_dn + "/pki-ext/tp-" + name
    return handle.query_dn(dn)


def trusted_point_exists(handle, name, **kwargs):
    """
    Checks if a trusted point exists

    Args:
        handle (ucschandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        key_ring = trusted_point_exists(handle, name="mytrustedpoint")
    """

    mo = trusted_point_get(handle, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def trusted_point_modify(handle, name, **kwargs):
    """
    Modifies a trusted point

    Args:
        handle (ucschandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        PkiTP object

    Raises:
        UcscOperationError: if PkiTP not present

    Example:
        trusted_point = trusted_point_modify(handle, name="test_tp",
                                             descr="testing tp")
    """

    mo = trusted_point_get(handle, name)
    if not mo:
        raise UcscOperationError("trusted_point_modify",
                                 "trusted point '%s' does not exist" % name)

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def trusted_point_delete(handle, name):
    """
    Deletes a truted point

    Args:
        handle (ucschandle)
        name (string): name

    Returns:
        None

    Raises:
        UcscOperationError: if PkiTP mo is not present

    Example:
        trusted_point_delete(handle, name="mytrustedpoint")
    """

    mo = trusted_point_get(handle, name)
    if not mo:
        raise UcscOperationError("trusted_point_delete",
                                 "trust point '%s' does not exist" % name)

    handle.remove_mo(mo)
    handle.commit()
