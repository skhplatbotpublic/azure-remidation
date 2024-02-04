from abc import ABC, abstractmethod
from typing import Any, Dict
from loguru import logger
from json import loads as jsonLoads

from remidation.common.consts import SNSEventKeys
from remidation.common.utils import validateDictKeys

class Skeleton(ABC):
	'''
	abstract class for all entities
	'''
	def __init__(self, event: Dict[str, Any]):
			'''
			constructor for Skeleton class
			Args:
					event (Dict[str, Any]): event from SNS
			
			Raises:
					AttributeError: if event is not valid
			'''
			self.event: dict = event
			self.metaDataList: list[dict] = []
			self.msgDict: dict = {}

			if not self.validateGeneralMessage(msg=event):
					raise AttributeError(f'message is not valid. event message: {event}')
					
			self.message = self.initializeGeneralMessage()

	@abstractmethod
	def handleEvent(self):
			pass

	@abstractmethod
	def validateMessage(self) -> bool:
			pass
	
	def validateGeneralMessage(self, msg: Dict[str, Any]) -> bool:
		'''
		validate message from SNS
		Args:
				msg (Dict[str, Any]): message from SNS
				Returns:
						bool: True if message is valid, False otherwise
		'''
		logger.info('validating message from SNS')
		if validateDictKeys(constsCls=SNSEventKeys.General, inputDict=msg):
				return True
		
		logger.error(f'message is not valid. {msg=}')
		return False

	def initializeGeneralMessage(self) -> None:
			'''
			initialize message from SNS
			Args:
					msg (Dict[str, Any]): message from SNS
					Returns:
							SNSMessage: SNSMessage object
			'''
			logger.info('initializing message from SNS')
			msgStr: dict = self.event[SNSEventKeys.General.MESSAGE]			
			self.msgDict: dict = jsonLoads(msgStr)

			self.eventType: str = self.msgDict[SNSEventKeys.Message.OBJECT]
			self.title = self.msgDict[SNSEventKeys.Message.TITLE]
			accountId = self.msgDict[SNSEventKeys.Message.ACCOUNT_IDS]
			if isinstance(accountId, list) and len(accountId) == 1:
					self.accountId = accountId[0]
			else:
					logger.error(f'key not found: {SNSEventKeys.Message.ACCOUNT_IDS} or value is not a list of length 1')
					raise AttributeError(f'key not found: {SNSEventKeys.Message.ACCOUNT_IDS} or value is not a list of length 1')

			logger.info(f'initialized message from SNS. {self.eventType=}, {self.title=}, {self.accountId=}')
