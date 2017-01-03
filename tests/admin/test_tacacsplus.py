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
from ucsc_apis.admin.tacacsplus import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_tacacsplus_provider_create():
    tacacsplus_provider_create(
        handle, name="test_tacac_prov", port="320", timeout="10")
    found = tacacsplus_provider_exists(
        handle, name="test_tacac_prov", port="320")[0]
    assert_equal(found, True)


def test_002_tacacsplus_provider_modify():
    mo = tacacsplus_provider_modify(
        handle, name="test_tacac_prov", timeout="5")
    assert_equal(mo.timeout, "5")


def test_003_tacacsplus_provider_group_create():
    tacacsplus_provider_group_create(handle, name="test_prov_grp")
    found = tacacsplus_provider_group_exists(handle, name="test_prov_grp")[0]
    assert_equal(found, True)


def test_004_tacacsplus_provider_group_add_provider():
    tacacsplus_provider_group_add_provider(
        handle, group_name="test_prov_grp", name="test_tacac_prov")
    found = tacacsplus_provider_group_provider_exists(
            handle,
            group_name="test_prov_grp", name="test_tacac_prov")[0]
    assert_equal(found, True)


def test_005_tacacsplus_provider_group_modify_provider():
    mo = tacacsplus_provider_group_modify_provider(
        handle, group_name="test_prov_grp", name="test_tacac_prov",
        order="2")
    assert_equal(mo.order, "2")


def test_006_tacacsplus_provider_group_remove_provider():
    tacacsplus_provider_group_remove_provider(
        handle, group_name="test_prov_grp", name="test_tacac_prov")
    found = tacacsplus_provider_group_provider_exists(
            handle,
            group_name="test_prov_grp", name="test_tacac_prov")[0]
    assert_equal(found, False)


def test_007_tacacsplus_provider_group_delete():
    tacacsplus_provider_group_delete(handle, name="test_prov_grp")
    found = tacacsplus_provider_group_exists(handle, name="test_prov_grp")[0]
    assert_equal(found, False)


def test_008_tacacsplus_provider_delete():
    tacacsplus_provider_delete(handle, name="test_tacac_prov")
    found = tacacsplus_provider_exists(handle, name="test_tacac_prov")[0]
    assert_equal(found, False)
