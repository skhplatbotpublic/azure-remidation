from remidation.events.skeleton import Skeleton
from typing import Any, Dict
from loguru import logger

from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccount
from azure.core.exceptions import (ResourceNotFoundError, AzureError)

from remidation.common.consts import SNSEventKeys
from remidation.common.utils import (validateDictKeys, convertDictToClassRecursion)

class EnforceDataBaseEncryption(Skeleton):
	'''
	EnforceDataBaseEncryption class
	handle events of type EnforceDataBaseEncryption
	'''
	def __init__(self, event: Dict[str, Any]):
		super().__init__(event=event)
		self.initializeMessage()
		
		if not self.validateMessage():
				raise AttributeError(f'message is not valid. event message: {event}')

	def handleEvent(self):
		'''
		enable secure transfer for storage accounts
		for each storage account in the message
		'''
		for resource in self.metaDataList:
			self.enableSecureTransfer(subscriptionID=self.accountId, resourceGroupName=resource.id.resourceGroups, storageAccountName=resource.id.storageAccounts)

	def validateMessage(self) -> bool:
		'''
		validate message from SNS
		'''
		failedResources: list[Dict] = self.msgDict.get(SNSEventKeys.Message.FAILED_RESOURCES, None)
		if failedResources and len(failedResources):
			return True
		
		return False

	def initializeMessage(self):
		'''
		initialize message from SNS
		'''
		for item in self.msgDict[SNSEventKeys.Message.FAILED_RESOURCES]:
			self.metaDataList.append(convertDictToClassRecursion(item))


	@staticmethod
	def enableSecureTransfer(subscriptionID: str, resourceGroupName: str, storageAccountName: str) -> None:
			'''
			enable secure transfer for storage account
			Args:
				subscriptionID (str): subscription ID
				resourceGroupName (str): resource group name
				storageAccountName (str): storage account name
			
			Returns:
				None

			Raises:
				ResourceNotFoundError: If the storage account is not found.
				AzureError: If an error occurs while updating the storage account.
			'''
			try:
					logger.info(f'enable secure transfer for storage account {storageAccountName} in resource group {resourceGroupName}')
					creds: DefaultAzureCredential = DefaultAzureCredential()
					storageClient: StorageManagementClient = StorageManagementClient(credential=creds, subscription_id=subscriptionID)
					storageAccount = storageClient.storage_accounts.get_properties(resourceGroupName, storageAccountName)
					storageAccount.enable_https_traffic_only = True

					storageAccount: StorageAccount = storageClient.storage_accounts.update(
							resourceGroupName,
							storageAccountName,
							storageAccount
					)

					logger.info(f'secure transfer enabled for storage account {storageAccountName} in resource group {resourceGroupName}')
			except ResourceNotFoundError:
					logger.error(f'storage account {storageAccountName} not found in resource group {resourceGroupName}')
					raise ResourceNotFoundError(f'storage account {storageAccountName} not found in resource group {resourceGroupName}')
			
			except AzureError as ex:
					logger.error(f'an error occurred: {ex.message}')
					raise AzureError(f'an error occurred: {ex.message}')
