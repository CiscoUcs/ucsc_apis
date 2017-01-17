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
This module performs the operation related to callhome.
"""
from ucscsdk.ucscexception import UcscOperationError
from ..common.utils import get_device_profile_dn
ucsc_base_dn = get_device_profile_dn(name="default")


def call_home_enable(handle, alert_throttling_admin_state=None, name=None,
                     descr=None, **kwargs):
    """
    Enables call home alert.

    Args:
        handle (UcscHandle)
        alert_throttling_admin_state (string): "on" or "off"
        name (string): name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CallhomeEp : ManagedObject

    Raises:
        UcscOperationError: If CallhomeEp is not present

    Example:
        call_home_enable(handle, alert_throttling_admin_state="on")
    """

    mo = handle.query_dn(ucsc_base_dn + "/call-home")
    if not mo:
        raise UcscOperationError("call_home_state_enable",
                                 "Call home not available.")

    mo.admin_state = "on"
    if alert_throttling_admin_state:
        mo.alert_throttling_admin_state = alert_throttling_admin_state
    mo.name = name
    mo.descr = descr

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_config(handle, contact=None, phone=None, email=None,
                     addr=None, customer=None, contract=None, site=None,
                     r_from=None, reply_to=None, urgency=None, **kwargs):
    """
    Configures call home

    Args:
        handle (UcscHandle)
        contact (string): Contact Name
        phone (string): phone number e.g. +91-1234567890
        email (string): contact email address
        addr (string): contact address
        customer (number): customer id
        contract (number): contract id
        site (number): site id
        r_from (string): from email address
        reply_to (string): to email address
        urgency (string): alert priority
         valid values are "alert", "critical", "debug", "emergency",
         "error", "info", "notice", "warning"
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        SmartcallhomeSource: ManagedObject

    Raises:
        UcscOperationError: If SmartcallhomeSource is not present

    Example:
        from ucscsdk.mometa.callhome.SmartcallhomeSource import \
            SmartcallhomeSourceConsts

        call_home_config(handle,
                         contact="user name",
                         phone="+91-1234567890",
                         email="user@cisco.com",
                         addr="user address",
                         customer="1111",
                         contract="2222",
                         site="3333",
                         r_from="from@cisco.com",
                         reply_to="to@cisco.com",
                         urgency=CallhomeSourceConsts.URGENCY_ALERT,
                         )
    """

    # configure call home
    dn = ucsc_base_dn + "/call-home/sch-source"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcscOperationError("call_home_config",
                                 "Call home source '%s' not available." % dn)

    args = {'contact': contact,
            'phone': phone,
            'email': email,
            'addr': addr,
            'customer': customer,
            'contract': contract,
            'site': site,
            'r_from': r_from,
            'reply_to': reply_to,
            'urgency': urgency}

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_disable(handle):
    """
    Disables call home alert.

    Args:
        handle (UcscHandle)

    Returns:
        CallhomeEp : ManagedObject

    Raises:
        UcscOperationError: If CallhomeEp is not present

    Example:
        call_home_state_disable(handle)
    """

    mo = handle.query_dn(ucsc_base_dn + "/call-home")
    if not mo:
        raise UcscOperationError("call_home_disable",
                                 "Call home not available.")

    mo.admin_state = "off"

    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_proxy_config(handle, url, port="80", **kwargs):
    """
    Configures HTTP proxy for callhome

    Args:
        handle (UcscHandle)
        url (String) : URL for the call home proxy
        port (String) : port number for the call home proxy
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        SmartcallhomeHttpProxy : ManagedObject

    Raises:
        UcscOperationError: If SmartcallhomeHttpProxy is not present

    Example:
        call_home_proxy_config(handle, url="www.testproxy.com", port=80)
    """

    mo = handle.query_dn(ucsc_base_dn + "/call-home/proxy")
    if not mo:
        raise UcscOperationError("call_home_proxy_config",
                                 "call home proxy is not available.")

    mo.url = url
    mo.port = port

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def call_home_transport_gw_config(handle, enabled, url, cert_chain=None,
                                  **kwargs):
    """
    Configures HTTP transport gateway for callhome

    Args:
        handle (UcscHandle)
        enabled (Boolean) : Transport gw is enabled or not, True or False
        url (String) : URL for the transport gw
        cert_chain (String): Certificate for the transport gw
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        SmartcallhomeTransportGateway : ManagedObject

    Raises:
        UcscOperationError: If SmartcallhomeTransportGateway is not present

    Example:
        call_home_transport_gw_config(handle, enabled="true",
                                      url="sch.gw.com")
    """

    mo = handle.query_dn(
        ucsc_base_dn + "/call-home/transport-gateway")
    if not mo:
        raise UcscOperationError("call_home_transport_gw_config",
                                 "call home transport gw is not available.")

    mo.enabled = enabled
    mo.url = url
    if cert_chain:
        mo.cert_chain = cert_chain

    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo
