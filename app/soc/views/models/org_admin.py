#!/usr/bin/python2.5
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
from soc.logic.models import org_app as org_app_logic
from soc.views.helper import access
from soc.views.helper import dynaform
from soc.views.helper import widgets
from soc.views.models import organization as org_view
from soc.views.models import role

import soc.logic.models.org_admin


class View(role.View):
  """View methods for the Organization Admin model.
  """

  DEF_ALREADY_AGREED_MSG = ugettext(
      "You already agreed to the Agreement when applying")

  def __init__(self, params=None):
    """Defines the fields and methods required for the base View class
    to provide the user with list, public, create, edit and delete views.

    Params:
      params: a dict with params for this View
    """

    rights = access.Checker(params)
    rights['create'] = ['checkIsDeveloper']
    rights['edit'] = [('checkHasActiveRoleForScope', org_admin_logic.logic)]
    rights['delete'] = ['checkIsDeveloper']
    # TODO accessCheck checkIsAdministratorForOrg
    rights['invite'] = ['checkIsDeveloper']
    rights['accept_invite'] = [('checkCanCreateFromRequest', 'org_admin')]
    # TODO accessCheck checkIsAdministratorForOrg
    rights['process_request'] = ['checkIsDeveloper',
        ('checkCanProcessRequest', 'org_admin')]
    rights['manage'] = [
        ('checkIsAllowedToManageRole', [soc.logic.models.org_admin.logic,
             soc.logic.models.org_admin.logic])]

    new_params = {}
    new_params['logic'] = soc.logic.models.org_admin.logic
    new_params['group_logic'] = org_logic.logic
    new_params['group_view'] = org_view.view
    new_params['rights'] = rights

    new_params['scope_view'] = org_view

    new_params['name'] = "Organization Admin"
    new_params['module_name'] = "org_admin"
    new_params['sidebar_grouping'] = 'Organizations'

    new_params['extra_dynaexclude'] = ['agreed_to_tos']

    new_params['create_extra_dynafields'] = {
        'scope_path': forms.fields.CharField(widget=forms.HiddenInput,
                                             required=True),
        'admin_agreement': forms.fields.CharField(required=False,
            widget=widgets.AgreementField),
        'agreed_to_admin_agreement': forms.fields.BooleanField(
            initial=False, required=True,
            label=ugettext('I agree to the Admin Agreement')),
        }

    new_params['allow_invites'] = True

    params = dicts.merge(params, new_params)

    super(View, self).__init__(params=params)

    # register the role with the group_view
    params['group_view'].registerRole(params['module_name'], self)

    # create and store the special form for invited users
    updated_fields = {
        'link_id': forms.CharField(widget=widgets.ReadOnlyInput(),
            required=False),
        'admin_agreement': forms.fields.Field(required=False,
            widget=widgets.AgreementField),
        }

    invited_create_form = dynaform.extendDynaForm(
        dynaform = self._params['create_form'],
        dynafields = updated_fields)

    params['invited_create_form'] = invited_create_form

  def _editPost(self, request, entity, fields):
    """See base.View._editPost().
    """

    if not entity:
      fields['user'] = fields['link_id']
      fields['link_id'] = fields['user'].link_id

    fields['agreed_to_tos'] = fields['agreed_to_admin_agreement']

    super(View, self)._editPost(request, entity, fields)

  def _acceptInvitePost(self, fields, request, context, params, **kwargs):
    """Fills in the fields that were missing in the invited_created_form.

    For params see base.View._acceptInvitePost()
    """

    # fill in the appropriate fields that were missing in the form
    fields['user'] = fields['link_id']
    fields['link_id'] = fields['user'].link_id
    fields['agreed_to_tos'] = fields['agreed_to_admin_agreement']

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

    entity = context['entity']
    form = context['form']

    if 'scope_path' in form.initial:
      scope_path = form.initial['scope_path']
    elif 'scope_path' in request.POST:
      # TODO: do this nicely
      scope_path = request.POST['scope_path']
    else:
      # TODO: is this always sufficient?
      form.fields['admin_agreement'] = None
      return

    org_app = org_app_logic.logic.getFromKeyName(scope_path)

    if not entity and org_app:
      if org_app.applicant.key() == context['user'].key():
        form.fields['agreed_to_admin_agreement'] = forms.fields.BooleanField(
            widget=widgets.ReadOnlyInput, initial=True, required=True,
            help_text=self.DEF_ALREADY_AGREED_MSG)

    entity = org_logic.logic.getFromKeyName(scope_path)

    if not (entity and entity.scope and entity.scope.org_admin_agreement):
      return

    content = entity.scope.org_admin_agreement.content

    form.fields['admin_agreement'].widget.text = content


view = View()

accept_invite = view.acceptInvite
admin = view.admin
create = view.create
delete = view.delete
edit = view.edit
invite = view.invite
list = view.list
manage = view.manage
process_request = view.processRequest
public = view.public
export = view.export
