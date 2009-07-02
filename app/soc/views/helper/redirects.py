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

"""Redirect related methods.
"""

__authors__ = [
  '"Sverre Rabbelier" <sverre@rabbelier.nl>',
  '"Lennard de Rijk" <ljvderijk@gmail.com>',
  ]


from google.appengine.ext import db


def getApplyRedirect(entity, params):
  """Returns the apply redirect for the specified entity.
  """

  result ='/%s/apply/%s' % (
      params['url_name'], entity.key().id_or_name())

  return result

def getInviteRedirect(entity, params):
  """Returns the invitation redirect for the specified entity.
  """

  result ='/%s/invite/%s' % (
      params['url_name'], entity.key().id_or_name())

  return result


def getCreateRedirect(entity, params):
  """Returns the create redirect for the specified entity.
  """

  result ='/%s/create/%s' % (
      params['url_name'], entity.key().id_or_name())

  return result


def getEditRedirect(entity, params):
  """Returns the edit redirect for the specified entity.
  """

  return '/%s/edit/%s' % (
      params['url_name'], entity.key().id_or_name())


def getPublicRedirect(entity, params):
  """Returns the public redirect for the specified entity.
  """

  return '/%s/show/%s' % (
      params['url_name'], entity.key().id_or_name())


def getAdminRedirect(entity, params):
  """Returns the public redirect for the specified entity.
  """

  return '/%s/admin/%s' % (
      params['url_name'], entity.key().id_or_name())


def getListRedirect(entity, params):
  """Returns the public redirect for the specified entity.
  """

  return '/%s/list/%s' % (
      params['url_name'], entity.key().id_or_name())


def getPublicListRedirect(entity, params):
  """Returns the public redirect for the specified entity.
  """

  return '/%s/list_public/%s' % (
      params['url_name'], entity.key().id_or_name())


def getExportRedirect(entity, params):
  """Returns the export redirect for the specified entity.
  """

  return '/%s/export/%s' % (
      params['url_name'], entity.key().id_or_name())


def getHomeRedirect(entity, params):
  """Returns the home redirect for the specified entity.
  """

  return '/%s/home/%s' % (
      params['url_name'], entity.key().id_or_name())


def getReviewRedirect(entity, params):
  """Returns the redirect to review the specified entity.
  """

  return '/%s/review/%s' % (
      params['url_name'], entity.key().id_or_name())


def getReviewOverviewRedirect(entity, params):
  """Returns the redirect to the review_overview using the
     keyname of the specified entity.
  """

  return '/%s/review_overview/%s' % (
      params['url_name'], entity.key().id_or_name())

def getCreateRequestRedirect(entity, params):
  """Returns the create request redirect for the specified entity.
  """

  result ='/request/create/%s/%s/%s' % (
      params['group_scope'], params['url_name'], entity.key().id_or_name())

  return result


def getRequestRedirectForRole(entity, role_name):
  """Returns the redirect to create a request for a specific role.
  """

  result ='/%s/request/%s' % (
      role_name, entity.key().id_or_name())

  return result


def getInviteRedirectForRole(entity, role_name):
  """Returns the redirect to create an invite for a specific role.
  """

  result ='/%s/invite/%s' % (
      role_name, entity.key().id_or_name())

  return result


def getListProposalsRedirect(entity, params):
  """Returns the redirect for the List page for the given
  Org entity and Org View params.
  """

  result = '/%s/list_proposals/%s' % (
      params['url_name'], entity.key().id_or_name())

  return result


def getAcceptedOrgsRedirect(entity, params):
  """Returns the redirect for the List of accepted orgs.
  """

  result = '/%s/accepted_orgs/%s' % (
      params['url_name'], entity.key().id_or_name())

  return result


def getListProjectsRedirect(entity, params):
  """Returns the redirect for the List Projects page for the given entity.
  """

  result = '/%s/list_projects/%s' % (
      params['url_name'], entity.key().id_or_name())

  return result


def getListRequestsRedirect(entity, params):
  """Returns the redirect for the List Requests paged for the given
  Group entity and Group View params.
  """

  result = '/%s/list_requests/%s' % (
      params['url_name'], entity.key().id_or_name())

  return result


def getListSelfRedirect(entity, params):
  """Returns the redirect for list_self access type.
  """

  result = '/%s/list_self/%s' % (
      params['url_name'], entity.key().id_or_name())

  return result


def getListRolesRedirect(entity, params):
  """Returns the redirect for the List Roles paged for the given
  Group entity and Group View params.
  """

  result = '/%s/list_roles/%s' % (
      params['url_name'], entity.key().id_or_name())

  return result


def getUserRolesRedirect(_, __):
  """Returns the redirect to the users Roles page.
  """

  return '/user/roles'


def getProcessRequestRedirect(entity, _):
  """Returns the redirect for processing the specified request entity.
  """

  result = '/%s/process_request/%s/%s' % (
      entity.role, entity.scope_path, entity.link_id)

  return result


def getManageRedirect(entity, params):
  """Returns the redirect for managing the given entity.
  """

  result = '/%s/manage/%s' % (
      params['url_name'], entity.key().id_or_name())

  return result


def getManageOverviewRedirect(entity, params):
  """Returns the redirect for the manage overview view of the given entity.
  """

  result = '/%s/manage_overview/%s' % (
      params['url_name'], entity.key().id_or_name())

  return result


def getSelectRedirect(params):
  """Returns the pick redirect for the specified entity.
  """

  if params.get('args'):
    return '/%(url_name)s/pick?%(args)s' % params
  else:
    return '/%(url_name)s/pick' % params


def getInviteAcceptedRedirect(entity, _):
  """Returns the redirect for accepting an invite.
  """

  return '/%s/accept_invite/%s/%s' % (
      entity.role, entity.scope_path, entity.link_id)


def getInviteProcessRedirect(entity, _):
  """Returns the redirect for processing an invite.
  """

  return '/request/process_invite/%s/%s/%s' % (
      entity.scope_path, entity.role, entity.link_id)


def getApplicantRedirect(entity, params):
  """Returns the redirect for processing accepted Applications.
  """

  return '/%s/applicant/%s' % (
      params['url_name'], entity.key().id_or_name())


def getStudentEditRedirect(entity, params):
  """Returns the redirect for Students to edit their Projects.
  """

  return '/%s/st_edit/%s' % (
      params['url_name'], entity.key().id_or_name())


def getStudentProposalRedirect(entity, params):
  """Returns the student proposal redirect for the given org and student.
  """

  result ='/%s/apply/%s?organization=%s' % (
      params['url_name'], params['student_key'], entity.link_id)

  return result


def getShowDuplicatesRedirect(entity, params):
  """Returns the show duplicates redirect for the specified entity.
  """

  return'/%s/show_duplicates/%s' % (
      params['url_name'], entity.key().name())


def getSlotsRedirect(entity, params):
  """Returns the slots redirect for the specified entity.
  """

  return'/%s/slots/%s' % (
      params['url_name'], entity.key().id_or_name())


def getAssignSlotsRedirect(entity, params):
  """Returns the assign slots redirect for the specified entity.
  """

  return'/%s/assign_slots/%s' % (
      params['url_name'], entity.key().id_or_name())


def getCreateDocumentRedirect(entity, prefix):
  """Returns the redirect for new documents.
  """

  return '/document/create/%s/%s' % (prefix, entity.key().id_or_name())


def getListDocumentsRedirect(entity, prefix):
  """Returns the redirect for listing documents.
  """

  return '/document/list/%s/%s' % (prefix, entity.key().id_or_name())


def getCreateSurveyRedirect(entity, prefix, url_name):
  """Returns the redirect for new surveys.
  """

  return '/%s/create/%s/%s' % (url_name, prefix, entity.key().id_or_name())


def getListSurveysRedirect(entity, prefix, url_name):
  """Returns the redirect for listing surveys.
  """

  return '/%s/list/%s/%s' % (url_name, prefix, entity.key().id_or_name())


def getTakeProjectSurveyRedirect(entity, info):
  """Returns the redirect for taking a Survey for the given Student Project.

  Args:
      entity: a StudentProject entity
      info: a dictionary contain a survey and params entry
  """

  survey_entity = info['survey']
  params = info['params']

  return '/%s/take/%s?project=%s' %(params['url_name'],
                                    survey_entity.key().id_or_name(),
                                    entity.key().id_or_name())


def getToSRedirect(presence):
  """Returns link to 'show' the ToS Document if it exists, None otherwise.

  Args:
    presence: Presence entity that may or may not have a tos property
  """
  if not presence:
    return None

  try:
    tos_doc = presence.tos
  except db.Error:
    return None

  if not tos_doc:
    return None

  return getPublicRedirect(tos_doc, {'url_name': 'document'})
