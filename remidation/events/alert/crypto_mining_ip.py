from remidation.events.skeleton import Skeleton
from typing import Any, Dict
from loguru import logger

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import SecurityRule
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import (ResourceNotFoundError, AzureError)

from remidation.common.consts import SNSEventKeys
from remidation.common.utils import (validateDictKeys, convertDictToClassRecursion)

class CryptoMiningIP(Skeleton):
		'''
		CryptoMiningIP class
		handle events of type CryptoMiningIP
		'''
		def __init__(self, event: Dict[str, Any]):
			super().__init__(event=event)
			
			if not self.validateMessage():
				raise AttributeError(f'message is not valid. event message: {event}')
			
			self.initializeMessage()
		

		def handleEvent(self):
			'''
			block IP in the firewall
			for each IP in the message
			'''
			for resource in self.metaDataList:
				self.blockIPFireWall(subscriptionID=self.accountId, resourceGroupName=resource.identity.resourceGroups, vmName=resource.identity.virtualMachines, ip=resource.affectedResources.targetIp)

		def validateMessage(self) -> bool:
			'''
			validate message from SNS
			'''
			activities: list[Dict] = self.msgDict.get(SNSEventKeys.Message.ACTIVITIES, None)
			if activities and len(activities):
				return True
			
			return False

		def initializeMessage(self):
			'''
			initialize message from SNS
			'''
			for item in self.msgDict[SNSEventKeys.Message.ACTIVITIES]:
				self.metaDataList.append(convertDictToClassRecursion(item)) 

		@staticmethod
		def blockIPFireWall(subscriptionID: str, resourceGroupName: str, vmName: str, ip: str) -> None:
				'''
				block IP in the firewall
				Args:
						subscriptionID (str): subscription ID
						resourceGroupName (str): resource group name
						vmName (str): vm name
						ip (str): ip to block
				
				Returns:
						None
				
				Raises:
					ResourceNotFoundError: if resource not found
					AzureError: if Azure error occurred
					Exception: if unexpected error occurred
				'''
				try:
						logger.info(f'blocking IP in the firewall. {subscriptionID=}, {resourceGroupName=}, {vmName=}, {ip=}')
						credentials = DefaultAzureCredential()
						networkClient = NetworkManagementClient(credentials, subscriptionID)
						computeClient = ComputeManagementClient(credentials, subscriptionID)

						logger.info('getting network interface and network security group')
						vm = computeClient.virtual_machines.get(resourceGroupName, vmName)
						networkInterfaceId = vm.network_profile.network_interfaces[0].id
						networkInterfaceName = networkInterfaceId.split('/')[-1]

						logger.info('creating security rule in network security group')
						networkInterface = networkClient.network_interfaces.get(resourceGroupName, networkInterfaceName)
						nsgId = networkInterface.network_security_group.id
						nsgName = nsgId.split('/')[-1]

						params = SecurityRule(
								protocol='*',
								source_address_prefix=ip,
								destination_address_prefix='*',
								access='Deny',
								direction='Inbound',
								source_port_range='*',
								destination_port_range='*',
								priority=100,
								description=f'Block IP {ip}'
						)
					
						for rule in networkClient.security_rules.list(resourceGroupName, nsgName):
								if rule.source_address_prefix == ip:
										logger.info(f'find rule: {rule.name}, block IP: {ip}')
										networkClient.security_rules.begin_create_or_update(
												resourceGroupName,
												nsgName,
												'block_' + ip.replace('.', '_'),
												params
										)
										break
								
				except ResourceNotFoundError as err:
						logger.error(f"resource not found: {err}")
						raise ResourceNotFoundError(f"resource not found: {err}")
				
				except AzureError as err:
						logger.error(f"an Azure error occurred: {err}")
						raise AzureError(f"an Azure error occurred: {err}")
				
				except Exception as err:
						logger.error(f"an unexpected error occurred: {err}")
						raise Exception(f"an unexpected error occurred: {err}")
				
