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
from ucsc_apis.admin.locale import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_locale_create():
    locale_create(handle, name="test_locale")
    found = locale_exists(handle, name="test_locale")[0]
    assert_equal(found, True)


def test_002_locale_modify():
    mo = locale_modify(handle, name="test_locale", descr="testing locale")
    assert_equal(mo.descr, "testing locale")


def test_003_locale_org_assign():
    mo = locale_org_assign(handle, locale_name="test_locale",
                           name="test_org_assign", org_dn="org-root")
    assert_equal(mo.name, "test_org_assign")


def test_004_locale_domaingroup_assign():
    mo = locale_domaingroup_assign(handle, locale_name="test_locale",
                                   name="test_domgrp_asn")
    assert_equal(mo.name, "test_domgrp_asn")


def test_005_locale_delete():
    locale_delete(handle, name="test_locale")
    found = locale_exists(handle, name="test_locale")[0]
    assert_equal(found, False)
