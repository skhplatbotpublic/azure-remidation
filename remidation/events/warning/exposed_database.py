from remidation.events.skeleton import Skeleton
from typing import Any, Dict
from loguru import logger

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.core.exceptions import (ResourceNotFoundError, AzureError)

from remidation.common.consts import SNSEventKeys
from remidation.common.utils import (validateDictKeys, convertDictToClassRecursion)

class ExposedDatabase(Skeleton):
	'''
	ExposedDatabase class
	handle events of type ExposedDatabase
	'''
	def __init__(self, event: Dict[str, Any]):
		super().__init__(event=event)
		
		if not self.validateMessage():
				raise AttributeError(f'message is not valid. event message: {event}')

		self.initializeMessage()


	def handleEvent(self):
		'''
		remove inbound from DB security group
		for each DB in the message
		'''
		for identity in self.metaDataList:
			self.findAndRemoveInboundFromDBSecurityGroup(subscriptionID=self.accountId, resourceGroupName=identity.coIdentityId.resourceGroups, ruleName=identity.coIdentityId.firewallRules)

	def validateMessage(self) -> bool:
		'''
		validate message from SNS
		'''
		involvedIdentities: list[Dict] = self.msgDict.get(SNSEventKeys.Message.INVOLVED_IDENTITIES_DEATIALS, None)

		if involvedIdentities and len(involvedIdentities):
			return True
		
		return False

	def initializeMessage(self):
		'''
		initialize message from SNS
		'''
		for item in self.msgDict[SNSEventKeys.Message.INVOLVED_IDENTITIES_DEATIALS]:
			self.metaDataList.append(convertDictToClassRecursion(item))

	@staticmethod
	def findAndRemoveInboundFromDBSecurityGroup(subscriptionID: str, resourceGroupName: str, ruleName: str) -> None:
		'''
		finds and removes an inbound rule from a database security group.

		Args:
			subscriptionID (str): The ID of the Azure subscription.
			resourceGroupName (str): The name of the resource group containing the database server.
			serverName (str): The name of the database server.
			ruleName (str): The name of the security rule to be removed.

		Returns:
			None

		Raises:
			ResourceNotFoundError: If the network security group or security rule is not found.
			AzureError: If an error occurs while removing the security rule.
		'''
		try:
			logger.info(f'finding and removing inbound from DB security group. {subscriptionID=}, {resourceGroupName=}, {ruleName=}')

			creds = DefaultAzureCredential()
			networkClient = NetworkManagementClient(creds, subscriptionID)

			for network in networkClient.network_security_groups.list(resourceGroupName):
				for rule in networkClient.security_rules.list(resourceGroupName, network.name):
					if rule.name == ruleName:
						logger.info(f'removing security rule: {rule.name}')
						networkClient.security_rules.begin_delete(resourceGroupName, network.name, rule.name)
						break

		except ResourceNotFoundError:
			logger.error(f'network security group or security rule not found: {ruleName}')
			raise ResourceNotFoundError(f'network security group or security rule not found: {ruleName}')
		
		except AzureError as ex:
			logger.error(f'an error occurred: {ex.message}')
			raise AzureError(f'an error occurred: {ex.message}')
