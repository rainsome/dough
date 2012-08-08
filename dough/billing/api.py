# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Sina Corporation
# All Rights Reserved.
# Author: Zhongyue Luo <lzyeval@gmail.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from dateutil.relativedelta import relativedelta
from nova import utils

from dough import db
from dough.billing import driver


def creating(context, subscription_id, tenant_id, item_name, resource_uuid,
             created_at, updated_at, expires_at,
             order_unit, order_size, price, currency, region_name,
             interval_unit, interval_size, is_prepaid):
    app = context.app
    conn = driver.get_connection(item_name)
    if not conn.is_running(resource_uuid):
        app.info("wait:%s creating, but %s not running." % (str(subscription_id), item_name))
        if created_at + relativedelta(minutes=10) < utils.utcnow():
            app.info("%s(%s) status creating-->error" % (str(subscription_id), item_name))
            db.subscription_error(context, subscription_id)
            # TODO(lzyeval): report
    else:
        interval_info = {
            interval_unit: interval_size,
            }
        app.info("%s(%s) status creating-->verify" % (str(subscription_id), item_name))
        db.subscription_verify(context, subscription_id)
        if is_prepaid:
            quantity = conn.get_usage(resource_uuid,
                    expires_at - relativedelta(**interval_info),
                    expires_at, order_size)
            print "creating and is running", tenant_id, subscription_id, \
                    quantity, order_size, "\033[1;33m", price, "\033[0m"
            app.info("creating %s:subid=%s,tid=%s,price=%s" % (item_name, subscription_id, tenant_id, str(price)))
            charge(context, tenant_id, subscription_id, quantity,
                   order_size, price)
        else:
            app.info("%s/%s/%s is_prepaid" % (tenant_id, str(subscription_id), item_name))
        db.subscription_extend(context, subscription_id,
                               expires_at + relativedelta(**interval_info))


def deleting(context, subscription_id, tenant_id, item_name, resource_uuid,
             created_at, updated_at, expires_at,
             order_unit, order_size, price, currency, region_name,
             interval_unit, interval_size, is_prepaid):
    app = context.app
    conn = driver.get_connection(item_name)
    if not conn.is_terminated(resource_uuid):
        app.info("wait:%s deleting, but %s not terminated." % (str(subscription_id), item_name))
        if updated_at + relativedelta(minutes=10) < utils.utcnow():
            app.info("%s(%s) status deleting-->error" % (str(subscription_id), item_name))
            db.subscription_error(context, subscription_id)
            # TODO(lzyeval): report
    else:
        # TODO(lzyeval): implement
        app.info("%s(%s) status deleting-->terminated" % (str(subscription_id), item_name))
        db.subscription_terminate(context, subscription_id)
        if not is_prepaid:
            interval_info = {
                interval_unit: interval_size,
                }
            quantity = conn.get_usage(resource_uuid,
                    expires_at - relativedelta(**interval_info),
                    expires_at, order_size)
            print "deleting", tenant_id, subscription_id, \
                    quantity, order_size, "\033[1;33m", price, "\033[0m"
            app.info("deleting %s(%s),tid=%s,price=%s" % (subscription_id, item_name, tenant_id, str(price)))
            charge(context, tenant_id, subscription_id, quantity,
                   order_size, price)
        else:
            app.info("%s/%s/%s is_prepaid" % (tenant_id, str(subscription_id), item_name))


def verified(context, subscription_id, tenant_id, item_name, resource_uuid,
             created_at, updated_at, expires_at,
             order_unit, order_size, price, currency, region_name,
             interval_unit, interval_size, is_prepaid):
    app = context.app
    conn = driver.get_connection(item_name)
    if not conn.is_running(resource_uuid, tenant_id=tenant_id):
        # FIXME(lzyeval): raise Exception()
        app.info("%s verified, but %s not running." % (str(subscription_id), item_name))
        return
    interval_info = {
        interval_unit: interval_size,
        }
    quantity = conn.get_usage(resource_uuid,
                              expires_at - relativedelta(**interval_info),
                              expires_at, order_size)
    print "verified", tenant_id, subscription_id, \
                    quantity, order_size, "\033[1;33m", price, "\033[0m"
    app.info("verified %s(%s/%s/%s)" \
             % (subscription_id, item_name, str(price), str(expires_at)))
    charge(context, tenant_id, subscription_id, quantity, order_size, price)
    db.subscription_extend(context, subscription_id,
                           expires_at + relativedelta(**interval_info))


def error(context, subscription_id, tenant_id, item_name, *args, **kwargs):
    # TODO(lzyeval): report
#    print "[BillingAPI]error", args, kwargs
#    context.app.info("error:%s(%s)" % (subscription_id, item_name))
    return


def charge(context, tenant_id, subscription_id, quantity, order_size, price):
    if not quantity:
        return
    line_total = price * quantity / order_size
    values = {
        'subscription_id': subscription_id,
        'quantity': quantity,
        'line_total': line_total,
    }
    print "purchase_create, tenant_id=%s, subid=%s" % (tenant_id, subscription_id)
    print values
    context.app.info("purchase_create:tenant_id=%s, subid=%s, line_total=%s" % (tenant_id, subscription_id, str(line_total)))
    db.purchase_create(context, values)
