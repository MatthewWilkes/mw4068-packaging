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

"""Slot allocation logic.
"""

__authors__ = [
  '"Sverre Rabbelier" <sverre@rabbelier.nl>',
  ]


import itertools
import math


class Error(Exception):
  """Error class for the Allocation module.
  """

  pass


class Allocator(object):
  """A simple student slots allocator.

  The buildSets method is used to validate the allocation data as well as
  construct the sets that the algorithm then uses to distribute the slots.
  By separating these steps it is possible to write a different allocation
  algorithm but re-use the sets and validation logic.
  """

  # I tried to write explicit code that does not require any
  # additional comments (with the exception of the set notation for
  # the convenience of any mathematicians that happen to read this
  # piece of code ;).

  def __init__(self, orgs, popularity, mentors, slots,
               max_slots_per_org, min_slots_per_org, iterative):
    """Initializes the allocator.

    Args:
      orgs: a list of all the orgs that need to be allocated
      popularity: the amount of applications per org
      mentors: the amount of assigned mentors per org
      slots: the total amount of available slots
      max_slots_per_org: how many slots an org should get at most
      min_slots_per_org: how many slots an org should at least get
    """

    self.locked_slots = {}
    self.adjusted_slots = {}
    self.adjusted_orgs = []
    self.locked_orgs = []
    self.unlocked_applications = []
    self.slots = slots
    self.max_slots_per_org = max_slots_per_org
    self.min_slots_per_org = min_slots_per_org
    self.orgs = set(orgs)
    self.initial_popularity = popularity
    self.mentors = mentors
    self.iterative = iterative

  def allocate(self, locked_slots, adjusted_slots):
    """Allocates the slots and returns the result.

    Args:
      locked_slots: a dict with orgs and the number of slots they get
      adjusted_slots: a dict with orgs and the number of extra slots they get
    """

    self.locked_slots = locked_slots
    self.adjusted_slots = adjusted_slots

    self.buildSets()

    if not sum(self.popularity.values()) or not sum(self.mentors.values()):
      return self.popularity

    if self.iterative:
      return self.iterativeAllocation()
    else:
      return self.preprocessingAllocation()

  def buildSets(self):
    """Allocates slots with the specified constraints
    """

    popularity = self.initial_popularity.copy()

    # set s
    locked_slots = self.locked_slots
    adjusted_slots = self.adjusted_slots

    # set a and b
    locked_orgs = set(locked_slots.keys())
    adjusted_orgs = set(adjusted_slots.keys())

    # set a' and b'
    unlocked_orgs = self.orgs.difference(locked_orgs)

    # set a*b and a'*b'
    locked_and_adjusted_orgs = locked_orgs.intersection(adjusted_orgs)

    # a+o and b+o should be o
    locked_orgs_or_orgs = self.orgs.union(locked_orgs)
    adjusted_orgs_or_orgs = self.orgs.union(adjusted_orgs)

    total_popularity = sum(popularity.values())

    # an item can be only a or b, so a*b should be empty
    if locked_and_adjusted_orgs:
      raise Error("Cannot have an org locked and adjusted")

    # a+o should be o, testing length is enough though
    if len(locked_orgs_or_orgs) != len(self.orgs):
      raise Error("Unknown org as locked slot")

    # same for b+o
    if len(adjusted_orgs_or_orgs) != len(self.orgs):
      raise Error("Unknown org as adjusted slot")

    self.adjusted_orgs = adjusted_orgs
    self.unlocked_orgs = unlocked_orgs
    self.locked_orgs = locked_orgs
    self.popularity = popularity
    self.total_popularity = total_popularity

  def rangeSlots(self, slots, org):
    """Returns the amount of slots for the org within the required bounds.
    """

    slots = int(math.floor(float(slots)))
    slots = min(slots, self.max_slots_per_org)
    slots = max(slots, self.min_slots_per_org)
    slots = min(slots, self.mentors[org])

    return slots

  def iterativeAllocation(self):
    """A simple iterative algorithm.
    """

    adjusted_orgs = self.adjusted_orgs
    adjusted_slots = self.adjusted_slots
    locked_orgs = self.locked_orgs
    locked_slots = self.locked_slots

    unallocated_popularity = self.total_popularity - len(locked_slots)

    available_slots = self.slots
    allocations = {}

    for org in self.orgs:
      popularity = self.popularity[org]
      mentors = self.mentors[org]

      if org in locked_orgs:
        slots = locked_slots[org]
      elif unallocated_popularity:
        weight = float(popularity) / float(unallocated_popularity)
        slots = int(math.floor(weight*available_slots))

      if org in adjusted_orgs:
        slots += adjusted_slots[org]

      slots = min(slots, self.max_slots_per_org)
      slots = min(slots, mentors)
      slots = min(slots, available_slots)

      allocations[org] = slots
      available_slots -= slots
      unallocated_popularity -= popularity

    return allocations

  def preprocessingAllocation(self):
    """An algorithm that pre-processes the input before running as normal.
    """

    adjusted_orgs = self.adjusted_orgs
    adjusted_slots = self.adjusted_slots
    locked_orgs = self.locked_orgs
    locked_slots = self.locked_slots
    unlocked_orgs = self.unlocked_orgs
    total_popularity = self.total_popularity

    available_slots = self.slots
    allocations = {}
    slack = {}

    for org in locked_orgs:
      popularity = self.popularity[org]
      slots = locked_slots[org]
      slots = self.rangeSlots(slots, org)

      total_popularity -= popularity
      available_slots -= slots
      allocations[org] = slots
      del self.popularity[org]

    # adjust the orgs in need of adjusting
    for org in adjusted_orgs:
      slots = float(adjusted_slots[org])

      adjustment = (float(total_popularity)/float(available_slots))*slots
      adjustment = int(math.ceil(adjustment))
      self.popularity[org] += adjustment
      total_popularity += adjustment

    # adjust the popularity so that the invariants are always met
    for org in unlocked_orgs:
      popularity = self.popularity[org]
      mentors = self.mentors[org]

      slots = (float(popularity)/float(total_popularity))*available_slots
      slots = self.rangeSlots(slots, org)

      popularity = (float(total_popularity)/float(available_slots))*slots

      self.popularity[org] = popularity

    total_popularity = sum(self.popularity.values())

    # do the actual calculation
    for org in unlocked_orgs:
      popularity = self.popularity[org]
      raw_slots = (float(popularity)/float(total_popularity))*available_slots
      slots = int(math.floor(raw_slots))

      slack[org] = raw_slots - slots
      allocations[org] = slots

    slots_left = available_slots - sum(allocations.values())

    # add leftover slots, sorted by slack, decending
    for org, slack in sorted(slack.iteritems(), key=lambda (k,v): v, reverse=True):
      if slots_left < 1:
        break

      current = allocations[org]
      slots = self.rangeSlots(current + 1, org)

      slots_left += slots - current
      allocations[org] = slots

    return allocations
