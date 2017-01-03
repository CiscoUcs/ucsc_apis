# Copyright 2015 Cisco Systems, Inc.
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
from ucsc_apis.admin.keyring import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_keyring_create():
    key_ring_create(handle, "test_kr")
    found = key_ring_exists(handle, name="test_kr")[0]
    assert_equal(found, True)


def test_002_keyring_modify():
    mo = key_ring_modify(handle, name="test_kr", regen="true")
    assert_equal(mo.regen, "yes")


def test_003_certificate_add():
    certificate_request_add(handle, name="test_kr", dns="10.10.10.100",
                            country="IN")
    found, mo = certificate_request_exists(handle, name="test_kr",
                                           dns="10.10.10.100")
    assert_equal(found, True)
    assert_equal(mo.dns, "10.10.10.100")


def test_004_trusted_point_create():
    trusted_point_create(handle, "test_tp")
    found = trusted_point_exists(handle, name="test_tp")[0]
    assert_equal(found, True)


def test_005_trusted_point_modify():
    mo = trusted_point_modify(handle, name="test_tp", descr="testing tp")
    assert_equal(mo.descr, "testing tp")


def test_006_trusted_point_delete():
    trusted_point_delete(handle, "test_tp")
    found = trusted_point_exists(handle, name="test_tp")[0]
    assert_equal(found, False)


def test_007_certificate_remove():
    certificate_request_remove(handle, name="test_kr")
    found = certificate_request_exists(handle, name="test_kr")[0]
    assert_equal(found, False)


def test_008_keyring_delete():
    key_ring_delete(handle, "test_kr")
    found = key_ring_exists(handle, name="test_kr")[0]
    assert_equal(found, False)
