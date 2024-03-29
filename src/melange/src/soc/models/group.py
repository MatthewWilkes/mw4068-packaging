#!/usr/bin/env python2.5
#
# Copyright 2008 the Melange authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module contains the Group Model."""

__authors__ = [
  '"Todd Larsen" <tlarsen@google.com>',
  '"Lennard de Rijk" <ljvderijk@gmail.com>',
  '"Pawel Solyga" <pawel.solyga@gmail.com>',
]


from google.appengine.ext import db

from django.utils.translation import ugettext

from soc.models import countries

import soc.models.presence
import soc.models.user


class Group(soc.models.presence.Presence):
  """Common data fields for all groups.
  """

  #: Required field storing name of the group.
  name = db.StringProperty(required=True,
      verbose_name=ugettext('Name'))
  name.help_text = ugettext('Complete, formal name of the group.')  
  
  #: Required field storing short name of the group.
  #: It can be used for displaying group as sidebar menu item.
  short_name = db.StringProperty(required=True,
      verbose_name=ugettext('Short name'))
  short_name.help_text = ugettext('Short name used for sidebar menu')

  #: Required many:1 relationship indicating the founding User of the
  #: Group (this relationship is needed to keep track of lifetime group
  #: creation limits, used to prevent spamming, etc.).
  founder = db.ReferenceProperty(reference_class=soc.models.user.User,
                                 required=True, collection_name="groups",
                                 verbose_name=ugettext('Registered by'))

  #: Required field storing a home page URL of the group.
  home_page = db.LinkProperty(required=True,
      verbose_name=ugettext('Home Page URL'))

  #: Required email address used as the "public" contact mechanism for
  #: the Group (as opposed to the founder.account email address which is
  #: kept secret, revealed only to Developers).
  email = db.EmailProperty(required=True,
      verbose_name=ugettext('Email'))
  email.help_text = ugettext(
      "Enter an email address to be used by would-be members seeking "
      "additional information. This can be an individual's email address or a "
      "mailing list address; use whichever will work best for you.")

  #: Required field storing description of the group.
  description = db.TextProperty(required=True,
      verbose_name=ugettext('Description'))

  #: Optional public mailing list.     
  pub_mailing_list = db.StringProperty(required=False,
    verbose_name=ugettext('Public Mailing List'))
  pub_mailing_list.help_text = ugettext(
    'Mailing list email address, URL to sign-up page, etc.')

  #: Optional public IRC channel.
  irc_channel = db.StringProperty(required=False,
    verbose_name=ugettext('Public IRC Channel (and Network)'))

  #====================================================================
  # (private) contact information
  #====================================================================

  #: Required field containing a group street address.
  #: Group street address can only be ASCII, not UTF-8 text,
  #: because, if supplied, it might be used as a shipping address.
  contact_street = db.StringProperty(required=True,
      verbose_name=ugettext('Street Address 1'))
  contact_street.help_text = ugettext(
      'street number and name, '
      '<a href="http://en.wikipedia.org/wiki/ASCII">ASCII</a> characters only')

  #: Optional field containing the 2nd group street address.
  #: Group street address can only be ASCII, not UTF-8 text,
  #: because, if supplied, it might be used as a shipping address.
  contact_street_extra = db.StringProperty(required=False,
      verbose_name=ugettext('Street Address 2'))
  contact_street_extra.help_text = ugettext(
      '2nd address line usually used for apartment numbers, '
      '<a href="http://en.wikipedia.org/wiki/ASCII">ASCII</a> characters only')

  #: Required field containing group address city.
  #: City can only be ASCII, not UTF-8 text, because, if
  #: supplied, it might be used as a shipping address.
  contact_city = db.StringProperty(required=True,
      verbose_name=ugettext('City'))
  contact_city.help_text = ugettext(
      '<a href="http://en.wikipedia.org/wiki/ASCII">ASCII</a> characters only')

  #: Required field containing group address state or province.
  #: Group state/province can only be ASCII, not UTF-8
  #: text, because, if supplied, it might be used as a shipping address.
  contact_state = db.StringProperty(
      verbose_name=ugettext('State/Province'))
  contact_state.help_text = ugettext(
      'optional if country/territory does not have states or provinces, '
      '<a href="http://en.wikipedia.org/wiki/ASCII">ASCII</a> characters only')

  #: Required field containing address country or territory of the group.
  contact_country = db.StringProperty(required=True,
      verbose_name=ugettext('Country/Territory'),
      choices=countries.COUNTRIES_AND_TERRITORIES)

  #: Required field containing address postal code of the group (ZIP code in
  #: the United States).Postal code can only be ASCII, not UTF-8
  #: text, because, if supplied, it might be used as a shipping address.
  contact_postalcode = db.StringProperty(required=True,
      verbose_name=ugettext('ZIP/Postal Code'))
  contact_postalcode.help_text = ugettext(
      '<a href="http://en.wikipedia.org/wiki/ASCII">ASCII</a> characters only')

  #: Required contact phone number that will be, amongst other uses,
  #: supplied to shippers along with the shipping address; kept private.
  phone = db.PhoneNumberProperty(required=True,
      verbose_name=ugettext('Phone Number'))
  phone.help_text = ugettext(
      'include complete international calling number with country code, '
      'use numbers only.')
  phone.example_text = ugettext(
      "e.g. 1650253000 for Google's Corp HQ number in the United States")

  #====================================================================
  # (private) shipping information
  #====================================================================

  #: Optional field containing a group street address.
  #: Group street address can only be ASCII, not UTF-8 text,
  #: because, if supplied, it is used as a shipping address.
  shipping_street = db.StringProperty(required=False,
      verbose_name=ugettext('Shipping Street Address 1'))
  shipping_street.help_text = ugettext(
      'street number and name, '
      '<a href="http://en.wikipedia.org/wiki/ASCII">ASCII</a> characters only '
      'Fill in only if you want the shipping address to differ from the '
      'contact address.')

  #: Optional field containing a 2nd line for the shipping street address; kept
  #: private. If shipping address is not present in its entirety, the
  #: group contact address will be used instead. Shipping street address can
  #: only be ASCII, not UTF-8 text, because, if supplied, it is used as a
  #: shipping address.
  shipping_street_extra = db.StringProperty(
      verbose_name=ugettext('Shipping Street Address 2'))
  shipping_street_extra.help_text = ugettext(
      '2nd address line usually used for apartment numbers, '
      '<a href="http://en.wikipedia.org/wiki/ASCII">ASCII</a> characters only. '
      'Fill in only if you want the shipping address to differ from the '
      'contact address.')

  #: Optional field containing group address city.
  #: City can only be ASCII, not UTF-8 text, because, if
  #: supplied, it is used as a shipping address.
  shipping_city = db.StringProperty(required=False,
      verbose_name=ugettext('Shipping City'))
  shipping_city.help_text = ugettext(
      '<a href="http://en.wikipedia.org/wiki/ASCII">ASCII</a> characters only '
      'Fill in only if you want the shipping address to differ from the '
      'contact address.')

  #: Optional field containing group address state or province.
  #: Group state/province can only be ASCII, not UTF-8
  #: text, because, if supplied, it is used as a shipping address.
  shipping_state = db.StringProperty(
      verbose_name=ugettext('Shipping State/Province'))
  shipping_state.help_text = ugettext(
      'optional if country/territory does not have states or provinces, '
      '<a href="http://en.wikipedia.org/wiki/ASCII">ASCII</a> characters only '
      'Fill in only if you want the shipping address to differ from the '
      'contact address.')

  #: Optional field containing address postal code of the group (ZIP code in
  #: the United States). Postal code can only be ASCII, not UTF-8
  #: text, because, if supplied, it is used as a shipping address.
  shipping_postalcode = db.StringProperty(required=False,
      verbose_name=ugettext('Shipping ZIP/Postal Code'))
  shipping_postalcode.help_text = ugettext(
      '<a href="http://en.wikipedia.org/wiki/ASCII">ASCII</a> characters only '
      'Fill in only if you want the shipping address to differ from the '
      'contact address.')

  #: Optional field containing address country or territory of the group.
  shipping_country = db.StringProperty(required=False,
      verbose_name=ugettext('Shipping Country/Territory'),
      choices=countries.COUNTRIES_AND_TERRITORIES)
  shipping_country.help_text = ugettext(
      'Choose one only if you want the shipping address to differ from the '
      'contact address.')

  #: Required property showing the current status of the group
  #: new: the group has not been active yet
  #: active: the group is active
  #: inactive: used to mark a group as read-only
  #: invalid: the group has been marked as removed
  status = db.StringProperty(required=True, default='new',
      choices=['new', 'active', 'inactive', 'invalid'])
