#!/usr/bin/env python2.5
#
# Copyright 2009 the Melange authors.
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

"""Views for Organization Admins.
"""

__authors__ = [
    '"Lennard de Rijk" <ljvderijk@gmail.com>'
    '"Sverre Rabbelier" <sverre@rabbelier.nl>',
  ]


from django import forms
from django.utils.translation import ugettext

from soc.logic import dicts
from soc.logic.models import organization as org_logic
from soc.logic.models import org_admin as org_admin_logic
from soc.logic.models import student as student_logic
from soc.views.helper import access
from soc.views.helper import dynaform
from soc.views.helper import redirects
from soc.views.helper import responses
from soc.views.helper import params as params_helper
from soc.views.helper import widgets
from soc.views.models import organization as org_view
from soc.views.models import role

import soc.logic.models.org_admin


class View(role.View):
  """View methods for the Organization Admin model.
  """

  DEF_ALREADY_AGREED_MSG = ugettext(
      "You have already accepted this agreement when submitting "
      "the organization application.")

  def __init__(self, params=None):
    """Defines the fields and methods required for the base View class
    to provide the user with list, public, create, edit and delete views.

    Params:
      params: a dict with params for this View
    """

    rights = access.Checker(params)
    rights['create'] = ['checkIsDeveloper']
    rights['edit'] = [('checkIsMyActiveRole', org_admin_logic.logic)]
    rights['delete'] = ['checkIsDeveloper']
    rights['invite'] = [('checkHasRoleForScope',
                         org_admin_logic.logic)]
    rights['accept_invite'] = [
        ('checkIsMyRequestWithStatus', [['group_accepted']]),
        ('checkIsNotStudentForProgramOfOrgInRequest', [org_logic.logic,
                                              student_logic.logic])]
    rights['process_request'] = [
        ('checkCanProcessRequest', [[org_admin_logic.logic]])]
    rights['manage'] = [
        ('checkIsAllowedToManageRole', [org_admin_logic.logic,
             org_admin_logic.logic])]

    new_params = {}
    new_params['logic'] = soc.logic.models.org_admin.logic
    new_params['group_logic'] = org_logic.logic
    new_params['group_view'] = org_view.view
    new_params['rights'] = rights

    new_params['scope_view'] = org_view

    new_params['name'] = "Organization Admin"
    new_params['module_name'] = "org_admin"
    new_params['sidebar_grouping'] = 'Organizations'

    new_params['extra_dynaexclude'] = ['agreed_to_tos', 'program']

    new_params['create_dynafields'] = [
        {'name': 'scope_path',
         'base': forms.fields.CharField,
         'widget': forms.HiddenInput,
         'required': True,
         },
        {'name': 'admin_agreement',
         'base': forms.fields.CharField,
         'required': False,
         'widget': widgets.AgreementField,
         'group': ugettext("5. Terms of Service"),
         },
        {'name': 'agreed_to_admin_agreement',
         'base': forms.fields.BooleanField,
         'initial': False,
         'required':True,
         'label': ugettext('I agree to the Admin Agreement'),
         'group': ugettext("5. Terms of Service"),
         },
        ]

    new_params['allow_invites'] = True
    # only if subclassed, so params is not empty
    new_params['show_in_roles_overview'] = bool(params)

    new_params['public_field_keys'] = ['name', 'link_id', 'scope_path']
    new_params['public_field_names'] = ["Admin Name", "Admin ID", "Organization ID"]

    params = dicts.merge(params, new_params)

    super(View, self).__init__(params=params)

    # register the role with the group_view
    self._params['group_view'].registerRole(self._logic.role_name, self)

    # create and store the special form for invited users
    dynafields = [
        {'name': 'link_id',
         'base': forms.CharField,
         'widget': widgets.ReadOnlyInput(),
         'required': False,
         },
        {'name': 'admin_agreement',
         'base': forms.fields.Field,
         'required': False,
         'widget': widgets.AgreementField,
         'group': ugettext("5. Terms of Service"),
        },
        ]

    dynaproperties = params_helper.getDynaFields(dynafields)

    invited_create_form = dynaform.extendDynaForm(
        dynaform = self._params['create_form'],
        dynaproperties = dynaproperties)

    self._params['invited_create_form'] = invited_create_form

  def _editPost(self, request, entity, fields):
    """See base.View._editPost().
    """

    if not entity:
      fields['user'] = fields['link_id']
      fields['link_id'] = fields['user'].link_id
      group_logic = self._params['group_logic']
      group_entity = group_logic.getFromKeyName(fields['scope_path'])
      fields['program'] = group_entity.scope

    fields['agreed_to_tos'] = fields['agreed_to_admin_agreement']

    super(View, self)._editPost(request, entity, fields)

  def _acceptInvitePost(self, fields, request, context, params, **kwargs):
    """Fills in the fields that were missing in the invited_created_form.

    For params see base.View._acceptInvitePost()
    """

    # fill in the appropriate fields that were missing in the form
    fields['agreed_to_tos'] = fields['agreed_to_admin_agreement']

    group_logic = params['group_logic']
    group_entity = group_logic.getFromKeyName(fields['scope_path'])
    fields['program'] = group_entity.scope

  def _editGet(self, request, entity, form):
    """Sets the content of the agreed_to_tos_on field and replaces.

    Also replaces the agreed_to_tos field with a hidden field when the ToS has been signed.
    For params see base.View._editGet().
    """

    if entity.agreed_to_tos:
      form.fields['agreed_to_admin_agreement'] = forms.fields.BooleanField(
          widget=forms.HiddenInput, initial=entity.agreed_to_tos,
          required=True)

    super(View, self)._editGet(request, entity, form)

  def _editContext(self, request, context):
    """See base.View._editContext.
    """

    from soc.logic.models.org_app_survey import logic as org_app_logic

    entity = context['entity']
    form = context['form']

    if 'scope_path' in form.initial:
      scope_path = form.initial['scope_path']
    elif 'scope_path' in request.POST:
      scope_path = request.POST['scope_path']
    else:
      form.fields['admin_agreement'] = None
      return

    org_entity = self._params['group_logic'].getFromKeyName(scope_path)
    org_app = org_app_logic.getForProgram(org_entity.scope)

    if org_app:
      user_entity = context['user']
      fields = {'main_admin': user_entity,
                'survey': org_app}
      record_logic = org_app_logic.getRecordLogic()
      org_app_record = record_logic.getForFields(fields, unique=True)

      if not entity and org_app_record:
        form.fields['agreed_to_admin_agreement'].initial = True

    if not (org_entity and org_entity.scope and 
            org_entity.scope.org_admin_agreement):
      return

    agreement = org_entity.scope.org_admin_agreement

    content = agreement.content
    params = {'url_name': 'document'}

    widget = form.fields['admin_agreement'].widget
    widget.text = content
    widget.url = redirects.getPublicRedirect(agreement, params)


view = View()

accept_invite = responses.redirectLegacyRequest
admin = responses.redirectLegacyRequest
create = responses.redirectLegacyRequest
delete = responses.redirectLegacyRequest
edit = responses.redirectLegacyRequest
invite = responses.redirectLegacyRequest
list = responses.redirectLegacyRequest
manage = responses.redirectLegacyRequest
process_request = responses.redirectLegacyRequest
public = responses.redirectLegacyRequest
export = responses.redirectLegacyRequest
