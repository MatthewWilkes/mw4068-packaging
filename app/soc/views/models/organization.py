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

"""Views for Organizations.
"""

__authors__ = [
    '"Sverre Rabbelier" <sverre@rabbelier.nl>',
    '"Lennard de Rijk" <ljvderijk@gmail.com>',
  ]


from django import forms

from soc.logic import cleaning
from soc.logic import dicts
from soc.logic import accounts
from soc.logic.models import organization as org_logic
from soc.logic.models import org_admin as org_admin_logic
from soc.logic.models import org_app as org_app_logic
from soc.views.helper import access
from soc.views.helper import decorators
from soc.views.helper import dynaform
from soc.views.helper import lists
from soc.views.helper import redirects
from soc.views.helper import widgets
from soc.views.models import group
from soc.views.models import program as program_view

import soc.models.organization
import soc.logic.models.organization

class View(group.View):
  """View methods for the Organization model.
  """

  def __init__(self, params=None):
    """Defines the fields and methods required for the base View class
    to provide the user with list, public, create, edit and delete views.

    Params:
      original_params: a dict with params for this View
    """

    rights = access.Checker(params)
    rights['any_access'] = ['allow']
    rights['show'] = ['allow']
    rights['create'] = ['checkIsDeveloper']
    rights['edit'] = [('checkHasActiveRoleForScope', 
                           [org_admin_logic.logic, 'link_id']),
                      ('checkIsActive', [org_logic.logic, None])]
    rights['delete'] = ['checkIsDeveloper']
    rights['home'] = ['allow']
    rights['public_list'] = ['allow']
    rights['apply_mentor'] = ['checkIsUser']
    rights['list_requests'] = [('checkHasActiveRoleForScope', 
                                [org_admin_logic.logic, 'link_id'])]
    rights['list_roles'] = [('checkHasActiveRoleForScope', 
                             [org_admin_logic.logic, 'link_id'])]
    rights['applicant'] = [('checkIsApplicationAccepted',
                            org_app_logic.logic)]

    new_params = {}
    new_params['logic'] = soc.logic.models.organization.logic
    new_params['rights'] = rights

    new_params['scope_view'] = program_view
    new_params['scope_redirect'] = redirects.getCreateRedirect

    new_params['name'] = "Organization"
    new_params['url_name'] = "org"
    new_params['document_prefix'] = "org"
    new_params['sidebar_grouping'] = 'Organizations'

    new_params['public_template'] = 'soc/organization/public.html'
    new_params['list_row'] = 'soc/organization/list/row.html'
    new_params['list_heading'] = 'soc/organization/list/heading.html'

    new_params['application_logic'] = org_app_logic
    new_params['group_applicant_url'] = True
    new_params['sans_link_id_public_list'] = True

    patterns = []

    patterns += [(r'^%(url_name)s/(?P<access_type>apply_mentor)/%(scope)s$',
        'soc.views.models.%(module_name)s.apply_mentor', 
        "List of all %(name_plural)s you can apply to"),]

    new_params['extra_django_patterns'] = patterns

    new_params['create_extra_dynaproperties'] = {
        'scope_path': forms.CharField(widget=forms.HiddenInput,
                                   required=True),
        'clean_ideas': cleaning.clean_url('ideas'),
        'clean': cleaning.validate_new_group('link_id', 'scope_path',
            soc.logic.models.organization, org_app_logic)
        }

    # get rid of the clean method
    new_params['edit_extra_dynaproperties'] = {
        'clean': (lambda x: x.cleaned_data)}

    params = dicts.merge(params, new_params)

    super(View, self).__init__(params=params)

    # create and store the special form for applicants
    updated_fields = {
        'link_id': forms.CharField(widget=widgets.ReadOnlyInput(),
            required=False),
        'clean_link_id': cleaning.clean_link_id('link_id')
        }

    applicant_create_form = dynaform.extendDynaForm(
        dynaform = self._params['create_form'],
        dynaproperties = updated_fields)

    params['applicant_create_form'] = applicant_create_form

  @decorators.merge_params
  @decorators.check_access
  def applyMentor(self, request, access_type,
                  page_name=None, params=None, **kwargs):
    """Shows a list of all organizations and you can choose one to 
       apply to become a mentor.

    Args:
      request: the standard Django HTTP request object
      access_type : the name of the access type which should be checked
      page_name: the page name displayed in templates as page and header title
      params: a dict with params for this View
      kwargs: the Key Fields for the specified entity
    """

    list_params = params.copy()
    list_params['list_action'] = (redirects.getRequestRedirectForRole, 'mentor')
    list_params['list_description'] = ('Choose an Organization which '
        'you want to become a Mentor for.')

    filter = {'scope_path': kwargs['scope_path'],
              'status' : 'active'}

    return self.list(request, access_type, 
        page_name, params=list_params, filter=filter)

  @decorators.merge_params
  @decorators.check_access
  def listPublic(self, request, access_type, page_name=None,
           params=None, filter=None, **kwargs):
    """See base.View.list.
    """

    new_params = {}
    if accounts.isDeveloper():
      new_params['list_action'] = (redirects.getAdminRedirect, params)
    else:
      new_params['list_action'] = (redirects.getPublicRedirect, params)
    # safe to merge them the wrong way around because of @merge_params
    params = dicts.merge(new_params, params)

    new_filter = {}

    new_filter['scope_path'] = kwargs['scope_path']
    new_filter['status'] = 'active'
    filter = dicts.merge(filter, new_filter)

    content = lists.getListContent(request, params, filter)
    contents = [content]

    return self._list(request, params, contents, page_name)

  def _getExtraMenuItems(self, role_description, params=None):
    """Used to create the specific Organization menu entries.

    For args see group.View._getExtraMenuItems().
    """
    submenus = []

    group_entity = role_description['group']
    roles = role_description['roles']

    if roles.get('org_admin'):
      # add a link to the management page
      submenu = (redirects.getListRolesRedirect(group_entity, params),
          "Manage Admins and Mentors", 'any_access')
      submenus.append(submenu)

      # add a link to invite an org admin
      submenu = (redirects.getInviteRedirectForRole(group_entity, 'org_admin'),
          "Invite an Org Admin", 'any_access')
      submenus.append(submenu)

      # add a link to invite a member
      submenu = (redirects.getInviteRedirectForRole(group_entity, 'mentor'),
          "Invite a Mentor", 'any_access')
      submenus.append(submenu)

      # add a link to the request page
      submenu = (redirects.getListRequestsRedirect(group_entity, params), 
          "List Requests and Invites", 'any_access')
      submenus.append(submenu)

      # add a link to the edit page
      submenu = (redirects.getEditRedirect(group_entity, params), 
          "Edit Organization Profile", 'any_access')
      submenus.append(submenu)

    if roles.get('org_admin') or roles.get('mentor'):
      submenu = (redirects.getCreateDocumentRedirect(group_entity, 'org'),
          "Create a New Document", 'any_access')
      submenus.append(submenu)

      submenu = (redirects.getListDocumentsRedirect(group_entity, 'org'),
          "List Documents", 'any_access')
      submenus.append(submenu)

    if roles.get('org_admin'):
      # add a link to the resign page
      submenu = (redirects.getManageRedirect(roles['org_admin'], 
          {'url_name': 'org_admin'}), 
          "Resign as Org Admin", 'any_access')
      submenus.append(submenu)

      # add a link to the edit page
      submenu = (redirects.getEditRedirect(roles['org_admin'],
          {'url_name': 'org_admin'}),
          "Edit My Org Admin Profile", 'any_access')
      submenus.append(submenu)

    if roles.get('mentor'):
      # add a link to the resign page
      submenu = (redirects.getManageRedirect(roles['mentor'], 
          {'url_name' : 'mentor'}), 
          "Resign as Mentor", 'any_access')
      submenus.append(submenu)

      # add a link to the edit page
      submenu = (redirects.getEditRedirect(roles['mentor'],
          {'url_name': 'mentor'}),
          "Edit My Org Mentor Profile", 'any_access')
      submenus.append(submenu)

    return submenus


view = View()

admin = view.admin
applicant = view.applicant
apply_mentor = view.applyMentor
create = view.create
delete = view.delete
edit = view.edit
home = view.home
list = view.list
list_public = view.listPublic
list_requests = view.listRequests
list_roles = view.listRoles
public = view.public
export = view.export
pick = view.pick
