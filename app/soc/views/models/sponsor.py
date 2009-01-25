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

"""Views for Sponsor profiles.
"""

__authors__ = [
    '"Sverre Rabbelier" <sverre@rabbelier.nl>',
    '"Lennard de Rijk" <ljvderijk@gmail.com>',
    '"Pawel Solyga" <pawel.solyga@gmail.com>',
  ]


from soc.logic import dicts
from soc.views.helper import access
from soc.views.models import group

import soc.models.sponsor
import soc.logic.dicts
import soc.logic.models.host
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

    rights = {}
    rights['create'] = [access.checkIsDeveloper]
    rights['edit'] = [access.checkIsHostForSponsor]
    rights['delete'] = [access.checkIsDeveloper]
    rights['list'] = [access.checkIsDeveloper]
    rights['list_requests'] = [access.checkIsHostForSponsor]

    new_params = {}
    new_params['logic'] = soc.logic.models.sponsor.logic
    new_params['rights'] = rights

    new_params['name'] = "Program Owner"
    new_params['module_name'] = "sponsor"

    # set the roles logic
    new_params['roles_logic'] =  {'host': soc.logic.models.host.logic}

    params = dicts.merge(params, new_params)

    super(View, self).__init__(params=params)


view = View()

create = view.create
delete = view.delete
edit = view.edit
list = view.list
list_requests = view.listRequests
public = view.public
export = view.export
pick = view.pick
