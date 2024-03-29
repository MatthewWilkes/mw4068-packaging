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

"""Views for Sponsor profiles.
"""

__authors__ = [
    '"Sverre Rabbelier" <sverre@rabbelier.nl>',
    '"Lennard de Rijk" <ljvderijk@gmail.com>',
    '"Pawel Solyga" <pawel.solyga@gmail.com>',
  ]


from django import forms

from soc.logic import dicts
from soc.logic.models.host import logic as host_logic
from soc.logic.models.sponsor import logic as sponsor_logic
from soc.views.helper import access
from soc.views.helper import decorators
from soc.views.helper import redirects
from soc.views.models import group

import soc.models.sponsor
import soc.logic.dicts
import soc.logic.models.sponsor


class View(group.View):
  """View methods for the Sponsor model.
  """

  def __init__(self, params=None):
    """Defines the fields and methods required for the base View class
    to provide the user with list, public, create, edit and delete views.

    Params:
      params: a dict with params for this View
    """    

    rights = access.Checker(params)
    rights['create'] = ['checkIsDeveloper']
    rights['edit'] = [('checkHasRoleForLinkIdAsScope', host_logic),
                      ('checkGroupIsActiveForLinkId', sponsor_logic)]
    rights['delete'] = ['checkIsDeveloper']
    rights['home'] = [('checkHasRoleForScope', host_logic)]
    rights['list'] = ['checkIsDeveloper']
    rights['list_requests'] = [('checkHasRoleForLinkIdAsScope', 
                                host_logic)]
    rights['list_roles'] = [('checkHasRoleForLinkIdAsScope', host_logic)]

    new_params = {}
    new_params['logic'] = soc.logic.models.sponsor.logic
    new_params['rights'] = rights

    new_params['name'] = "Program Owner"
    new_params['module_name'] = "sponsor"
    new_params['document_prefix'] = "sponsor"
    new_params['sidebar_grouping'] = 'Programs'

    new_params['create_dynafields'] = [
        {'name': 'link_id',
         'base': forms.fields.CharField,
         'label': 'Sponsor Link ID',
         },
        ]

    params = dicts.merge(params, new_params)

    super(View, self).__init__(params=params)

  def _getExtraMenuItems(self, role_description, params=None):
    """Used to create the specific Sponsor menu entries.

    For args see group.View._getExtraMenuItems().
    """

    submenus = []

    group_entity = role_description['group']
    roles = role_description['roles']
  
    if roles.get('host'):
      # add a link to create a new program
      submenu = (redirects.getCreateRedirect(group_entity,
          {'url_name': 'program'}),"Create a New Program", 'any_access')
      submenus.append(submenu)

      # add a link to the management page
      submenu = (redirects.getListRolesRedirect(group_entity, params), 
          "Manage Program Administrators", 'any_access')
      submenus.append(submenu)

      # add a link to invite an a host
      submenu = (redirects.getInviteRedirectForRole(group_entity, 'host'), 
          "Invite a Program Administrator", 'any_access')
      submenus.append(submenu)

      # add a link to the request page
      submenu = (redirects.getListRequestsRedirect(group_entity, params), 
          "List Program Administrator Invites", 'any_access')
      submenus.append(submenu)

      # add a link to the edit page
      submenu = (redirects.getEditRedirect(group_entity, params), 
          "Edit Program Owner Profile", 'any_access')
      submenus.append(submenu)

      # add a link to resign as a host
      submenu = (redirects.getManageRedirect(roles['host'], 
          {'url_name': 'host'}), 
          "Resign as Program Administrator", 'any_access')
      submenus.append(submenu)

      # add a link to create a new document
      submenu = (redirects.getCreateDocumentRedirect(group_entity, 'sponsor'),
          "Create a New Document", 'any_access')
      submenus.append(submenu)

      # add a link to list all documents
      submenu = (redirects.getListDocumentsRedirect(group_entity, 'sponsor'),
          "List Documents", 'any_access')
      submenus.append(submenu)

    return submenus


view = View()

admin = decorators.view(view.admin)
create = decorators.view(view.create)
delete = decorators.view(view.delete)
edit = decorators.view(view.edit)
home = decorators.view(view.home)
list = decorators.view(view.list)
list_requests = decorators.view(view.listRequests)
list_roles = decorators.view(view.listRoles)
public = decorators.view(view.public)
export = decorators.view(view.export)
pick = decorators.view(view.pick)
