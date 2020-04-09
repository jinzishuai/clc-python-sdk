"""
Anti-affinity related functions.

These Anti-affinity related functions generally align one-for-one with published API calls categorized in the account category

API v2 - https://t3n.zendesk.com/forums/21645944-Account

Antiaffinity object variables:

	antiaffinity.id
	antiaffinity.name
	antiaffinity.location
	antiaffinity.servers

"""
from __future__ import print_function, absolute_import, unicode_literals

# TODO - Update Anti-Affinity Policy - returning 500 error
# TODO - Create Anti-Affinity Policy - returning 400 error
# TODO - Return servers object


import json
import clc

class AntiAffinity(object):

	@staticmethod
	def GetAll(alias=None,location=None,session=None):
		"""Gets a list of anti-affinity policies within a given account.

		https://t3n.zendesk.com/entries/44657214-Get-Anti-Affinity-Policies

		>>> clc.v2.AntiAffinity.GetAll()
		[<clc.APIv2.anti_affinity.AntiAffinity object at 0x10c65e910>, <clc.APIv2.anti_affinity.AntiAffinity object at 0x10c65ec90>]

		"""
		if not alias:  alias = clc.v2.Account.GetAlias(session=session)

		policies = []
		policy_resp = clc.v2.API.Call('GET','antiAffinityPolicies/%s' % alias,{},session=session)
		for k in policy_resp:
			r_val = policy_resp[k]
			for r in r_val:
				if r.get('location'):
					if location and r['location'].lower()!=location.lower():  continue
					servers = [obj['id'] for obj in r['links'] if obj['rel'] == "server"]
					policies.append(AntiAffinity(id=r['id'],name=r['name'],location=r['location'],servers=servers,session=session))

		return(policies)


	@staticmethod
	def GetLocation(location=None,alias=None,session=None):
		"""Returns a list of anti-affinity policies within a specific location.

		>>> clc.v2.AntiAffinity.GetLocation("VA1")
		[<clc.APIv2.anti_affinity.AntiAffinity object at 0x105eeded0>]

		"""
		if not location:  location = clc.v2.Account.GetLocation(session=session)

		return(AntiAffinity.GetAll(alias=alias,location=location,session=session))


	@staticmethod
	def Create(name,alias=None,location=None,session=None):
		"""Creates a new anti-affinity policy within a given account.

		https://t3n.zendesk.com/entries/45042770-Create-Anti-Affinity-Policy

		*TODO* Currently returning 400 error:
		clc.APIFailedResponse: Response code 400. . POST https://api.tier3.com/v2/antiAffinityPolicies/BTDI

		"""

		if not alias:  alias = clc.v2.Account.GetAlias(session=session)
		if not location:  location = clc.v2.Account.GetLocation(session=session)

		r = clc.v2.API.Call('POST','antiAffinityPolicies/%s' % alias,
							json.dumps({'name': name, 'location': location}),
							session=session)
		return(AntiAffinity(id=r['id'],name=r['name'],location=r['location'],servers=[],session=session))


	def __init__(self,id,alias=None,name=None,location=None,servers=None,session=None):
		"""Create AntiAffinity object.

		If parameters are populated then create object location.
		Else if only id is supplied issue a Get Policy call

		https://t3n.zendesk.com/entries/44658344-Get-Anti-Affinity-Policy

		>>> clc.v2.AntiAffinity(id="f5b5e523ed8e4604842ec417d5502510")
		<clc.APIv2.anti_affinity.AntiAffinity object at 0x104753690>

		"""

		self.id = id
		self.session = session

		if alias:  self.alias = alias
		else:  self.alias = clc.v2.Account.GetAlias(session=self.session)

		if name:
			self.name = name
			self.location = location
			self.servers = servers
		else:
			r = clc.v2.API.Call('GET','antiAffinityPolicies/%s/%s' % (self.alias,self.id),{},session=self.session)
			self.name = r['name']
			self.location = r['location']
			self.servers = [obj['id'] for obj in r['links'] if obj['rel'] == "server"]


	def Update(self,name):
		"""Change the policy's name.

		https://t3n.zendesk.com/entries/45066480-Update-Anti-Affinity-Policy

		*TODO* - currently returning 500 error

		"""

		_ = clc.v2.API.Call('PUT','antiAffinityPolicies/%s/%s' % (self.alias,self.id),{'name': name},session=self.session)
		self.name = name


	def Delete(self):
		"""Delete policy

		https://t3n.zendesk.com/entries/45044330-Delete-Anti-Affinity-Policy

		>>> a = clc.v2.AntiAffinity.GetLocation("WA1")[0]
		>>> a.Delete()
		"""
		_ = clc.v2.API.Call('DELETE','antiAffinityPolicies/%s/%s' % (self.alias,self.id),{},session=self.session)


	def __str__(self):
		pass
