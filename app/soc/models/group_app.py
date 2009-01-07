#!/usr/bin/python2.5
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

"""This module contains the Group Application Model."""

__authors__ = [
  '"Todd Larsen" <tlarsen@google.com>',
]


from google.appengine.ext import db

from django.utils.translation import ugettext_lazy

import soc.models.document
import soc.models.linkable
import soc.models.user


class GroupApplication(soc.models.linkable.Linkable):
  """Common application questions for all groups.

  Eventually, this will be replaced with a Question/Answer/Quiz/Response
  approach.  At that time, existing OrgApplication entities will be migrated
  (converted) to their new representations in the Datastore.
  """

  #: Required field that will become the name of the Group in the profile,
  #: if the Group Application is accepted.
  #: See also:  soc.models.group.Group.name
  name = db.StringProperty(required=True,
      verbose_name=ugettext_lazy('Group Name'))
  name.help_text = ugettext_lazy('Complete, formal name of the group.')  
  
  #: Required many:1 relationship indicating the User who is applying on
  #: behalf of the Group.  If the Group Application is accepted, this User
  #: will become the founding User of the Group.
  #: See also:  soc.models.group.Group.founder
  applicant = db.ReferenceProperty(reference_class=soc.models.user.User,
    required=True, collection_name='group_apps',
    verbose_name=ugettext_lazy('Applicant'))

  #: Required field indicating the home page URL of the applying Group.
  #: See also:  soc.models.group.Group.home_page
  home_page = db.LinkProperty(required=True,
      verbose_name=ugettext_lazy('Home Page URL'))
  
  #: Required email address used as the "public" contact mechanism for
  #: the Group (as opposed to the applicant.account email address which is
  #: kept secret, revealed only to Developers).
  #: See also:  soc.models.group.Group.email
  email = db.EmailProperty(required=True,
    verbose_name=ugettext_lazy('Public Email'))
  
  #: Required description of the Group.
  description = db.TextProperty(required=True,
      verbose_name=ugettext_lazy('Description'))

  why_applying = db.TextProperty(required=True,
    verbose_name=ugettext_lazy(
      'Why is your group applying to participate?'
      ' What do you hope to gain by participating?'))

  prior_participation = db.TextProperty(required=False,
    verbose_name=ugettext_lazy(
      'Has your group participated previously?'
      ' If so, please summarize your involvement and any past successes'
      ' and failures. (optional)'))

  prior_application = db.TextProperty(required=False,
    verbose_name=ugettext_lazy(
      'If your group has not previously participated, have you applied in'
      ' the past?  If so, for what sort of participation? (optional)'))

  pub_mailing_list = db.StringProperty(required=False,
    verbose_name=ugettext_lazy(
      'What is the main public mailing list for your group? (optional)'))
  pub_mailing_list.help_text = ugettext_lazy(
    'Mailing list email address, URL to sign-up page, etc.')

  irc_channel = db.StringProperty(required=False,
    verbose_name=ugettext_lazy(
      'Where is the main IRC channel for your group?'
      ' (optional)'))
  irc_channel.help_text = ugettext_lazy('IRC network and channel.')

  backup_admin = db.ReferenceProperty(reference_class=soc.models.user.User,
    required=True,  collection_name='group_app_backup_admin',
    verbose_name=ugettext_lazy(
      'Please select your backup group administrator.'))

  member_criteria = db.TextProperty(required=True,
    verbose_text=ugettext_lazy(
      'What criteria do you use to select the members of your group?'
      ' Please be as specific as possible.'))
  member_disappears = ugettext_lazy(
    'Members include mentors, admininstrators, and the like.')

  member_template = db.ReferenceProperty(
    reference_class=soc.models.document.Document, required=False,
    collection_name='group_app_member_template',
    verbose_name=ugettext_lazy(
      'Please select the application template you would like potential'
      ' members of your group to use.  (optional).'))
  contrib_template.help_text = ugettext_lazy(
    'This template will be presented to potential members when they'
    ' apply to the group.')
