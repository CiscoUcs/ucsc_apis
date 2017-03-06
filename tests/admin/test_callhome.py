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
from ucsc_apis.admin.dns import *
from ucsc_apis.admin.callhome import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_dns_server_add():
    dns_server_add(handle, name="2.2.2.2")
    found = dns_server_exists(handle, name="2.2.2.2")[0]
    assert_equal(found, True)


def test_002_callhome_transport_gw_config():
    mo = call_home_transport_gw_config(handle, enabled="true",
                                       url="sch.gw.com")
    assert_equal(mo.url, "sch.gw.com")


def test_003_callhome_enable():
    mo = call_home_enable(handle, alert_throttling_admin_state="on")
    assert_equal(mo.alert_throttling_admin_state, "on")


def test_004_callhome_config():
    mo = call_home_config(handle, phone="+1-123456", urgency="warning")
    assert_equal(mo.urgency, "warning")


def test_005_callhome_proxy_config():
    mo = call_home_proxy_config(handle, url="http://sch.proxycisco.com", port="80")
    assert_equal(mo.url, "http://sch.proxycisco.com")
    mo = call_home_proxy_config(handle, url="", port="80")
    assert_equal(mo, None)


def test_006_callhome_disable():
    mo = call_home_disable(handle)
    assert_equal(mo.admin_state, "off")


def test_007_dns_server_remove():
    dns_server_remove(handle, name="2.2.2.2")
    found = dns_server_exists(handle, name="2.2.2.2")[0]
    assert_equal(found, False)
