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

from ..connection.info import custom_setup, custom_teardown
from nose.tools import *
from ucsc_apis.network.lan_conn_policy import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_lan_conn_policy_create():
    lan_conn_policy_create(
        handle, name="test_lan_con_pol", descr="testing lan")
    found = lan_conn_policy_exists(handle, name="test_lan_con_pol")[0]
    assert_equal(found, True)


def test_002_lcp_vnic_add():
    lcp_vnic_add(handle, name="test_vnic",
                 parent_dn="org-root/lan-conn-pol-test_lan_con_pol",
                 switch_id="A",
                 mtu="2240",
                 adaptor_profile_name="global-SRIOV")
    found = lcp_vnic_exists(handle, name="test_vnic",
                            parent_dn="org-root/lan-conn-pol-test_lan_con_pol",
                            mtu="2240")[0]
    assert_equal(found, True)


def test_004_lcp_iscsi_vnic_add():
    lcp_iscsi_vnic_add(handle, name="test_iscsiv",
                       parent_dn="org-root/lan-conn-pol-test_lan_con_pol",
                       switch_id="A",
                       vnic_name="test_vnic")
    found = lcp_iscsi_vnic_exists(
            handle, name="test_iscsiv",
            parent_dn="org-root/lan-conn-pol-test_lan_con_pol",
            vnic_name="test_vnic")[0]
    assert_equal(found, True)


def test_002_lcp_iscsi_vnic_delete():
    lcp_iscsi_vnic_delete(
            handle, name="test_iscsiv",
            parent_dn="org-root/lan-conn-pol-test_lan_con_pol")
    found = lcp_iscsi_vnic_exists(
            handle, name="test_iscsiv",
            parent_dn="org-root/lan-conn-pol-test_lan_con_pol")[0]
    assert_equal(found, False)


def test_003_lcp_vnic_delete():
    lcp_vnic_delete(
            handle, name="test_vnic",
            parent_dn="org-root/lan-conn-pol-test_lan_con_pol")
    found = lcp_vnic_exists(
            handle, name="test_vnic",
            parent_dn="org-root/lan-conn-pol-test_lan_con_pol")[0]
    assert_equal(found, False)


def test_003_lan_conn_policy_delete():
    lan_conn_policy_delete(handle, name="test_lan_con_pol")
    found = lan_conn_policy_exists(handle, name="test_lan_con_pol")[0]
    assert_equal(found, False)
