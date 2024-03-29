# Copyright 2009 the Melange authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module containing the GHOP Callback.
"""

__authors__ = [
  '"Madhusudan C.S." <madhusudancs@gmail.com>',
  '"Lennard de Rijk" <ljvderijk@gmail.com>',
  ]


from soc.modules.ghop.tasks import org_app_survey as org_app_survey_tasks
from soc.modules.ghop.tasks import task_update
from soc.modules.ghop.views.models import mentor
from soc.modules.ghop.views.models import organization
from soc.modules.ghop.views.models import org_admin
from soc.modules.ghop.views.models import org_app_survey
from soc.modules.ghop.views.models import program
from soc.modules.ghop.views.models import student
from soc.modules.ghop.views.models import task
from soc.modules.ghop.views.models import task_subscription
from soc.modules.ghop.views.models import timeline


class Callback(object):
  """Callback object that handles interaction between the core.
  """

  API_VERSION = 1

  def __init__(self, core):
    """Initializes a new Callback object for the specified core.
    """

    self.core = core

  def registerWithSitemap(self):
    """Called by the server when sitemap entries should be registered.
    """

    self.core.requireUniqueService('registerWithSitemap')

    # register the GHOP Views
    self.core.registerSitemapEntry(mentor.view.getDjangoURLPatterns())
    self.core.registerSitemapEntry(organization.view.getDjangoURLPatterns())
    self.core.registerSitemapEntry(org_admin.view.getDjangoURLPatterns())
    self.core.registerSitemapEntry(org_app_survey.view.getDjangoURLPatterns())
    self.core.registerSitemapEntry(program.view.getDjangoURLPatterns())
    self.core.registerSitemapEntry(student.view.getDjangoURLPatterns())
    self.core.registerSitemapEntry(task.view.getDjangoURLPatterns())
    self.core.registerSitemapEntry(
        task_subscription.view.getDjangoURLPatterns())
    self.core.registerSitemapEntry(timeline.view.getDjangoURLPatterns())

    # register GHOP GAE Tasks URL's
    self.core.registerSitemapEntry(org_app_survey_tasks.getDjangoURLPatterns())
    self.core.registerSitemapEntry(task_update.getDjangoURLPatterns())

  def registerWithSidebar(self):
    """Called by the server when sidebar entries should be registered.
    """

    # Require that we had the chance to register the urls we need with the
    # sitemap.
    self.core.requireUniqueService('registerWithSidebar')

    # register the GHOP menu entries
    self.core.registerSidebarEntry(mentor.view.getSidebarMenus)
    self.core.registerSidebarEntry(organization.view.getExtraMenus)
    self.core.registerSidebarEntry(organization.view.getSidebarMenus)
    self.core.registerSidebarEntry(org_admin.view.getSidebarMenus)
    self.core.registerSidebarEntry(program.view.getExtraMenus)
    self.core.registerSidebarEntry(program.view.getSidebarMenus)
    self.core.registerSidebarEntry(student.view.getSidebarMenus)
    self.core.registerSidebarEntry(task.view.getSidebarMenus)
    self.core.registerSidebarEntry(task_subscription.view.getSidebarMenus)

  def registerRights(self):
    """Called by the server when the document rights should be registered.
    """

    ghop_program_membership  = {
        'admin': ['host'],
        'restricted': ['host', 'ghop_org_admin'],
        'member': ['host', 'ghop_org_admin', 'ghop_org_mentor',
                   'ghop_org_student'],
        'list': ['host', 'ghop_org_admin', 'ghop_org_mentor'],
        }

    ghop_organization_membership = {
        'admin': ['host', 'ghop_org_admin'],
        'restricted': ['host', 'ghop_org_admin', 'ghop_org_mentor'],
        'member': ['host', 'ghop_org_admin', 'ghop_org_mentor',
                   'ghop_org_student'],
        'list': ['host', 'ghop_org_admin', 'ghop_org_mentor'],
        }

    self.core.registerRight('ghop_program', ghop_program_membership)
    self.core.registerRight('ghop_org', ghop_organization_membership)
