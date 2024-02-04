############## REMEDIATION CONSTS  #####################

# ENTITIES TYPES
class ObjectType:
	ALERT_ENTITY: str = 'Alert'
	WARNING_ENTITY: str = 'WarningEntity'

# HARDENING TYPES
class HardeningType:
	EXPOSED_DATABASE: str = 'ExposedDatabase'
	MISCONFIGURATION :str = 'Misconfiguration'

# SNS MESSAGE KEYS
class SNSEventKeys:
	class General:
		TYPE: str = 'Type'
		MESSAGE: str = 'Message'
		MESSAGE_ID: str = 'MessageId'
		TOPIC_ARN: str = 'TopicArn'

	class Message:	
		ACCOUNT_IDS: str = 'accountIds'
		ACCOUNT_NAME: str = 'accountName'
		ACTIVITIES: str = 'activities'
		AFFECTED_RSOURCES: str = 'affectedResources'
		FAILED_RESOURCES: str = 'failedResources'
		HARDENING_TYPE: str = 'hardeningType'
		INVOLVED_IDENTITIES_DEATIALS: str = 'involvedIdentitiesDetails'
		MESSAGE: str = 'Message'
		MESSAGE_ID: str = 'MessageId'
		OBJECT: str = 'objectType'
		RESOURCE_GROUP: str = 'resourceGroup'
		RESOURCE_NAME: str = 'name'
		TITLE: str = 'title'
