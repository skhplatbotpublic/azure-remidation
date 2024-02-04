from json import load as jsonLoad
from json import loads as jsonLoads
from typing import Any, Dict
from remidation.events.alert import CryptoMiningIP
from remidation.events.warning import EnforceDataBaseEncryption, ExposedDatabase

CRYPTO_MINING_IP: str = 'remidation/sns_events/communication_to_crypto_mining_ip.json'
SECURE_TRANSFER_REQUIRED: str = 'remidation/sns_events/secure_transfer_required.json'
EXPOSED_DATABASE: str = 'remidation/sns_events/exposed_database.json'

TITLE_CRYPTO_MINING_IP: str = 'Communication to crypto-mining IP'
TITLE_SECURE_TRANSFER_REQUIRED: str = 'Storage account does not enforce encryption of data in-transit'
TITLE_EXPOSED_DATABASE: str = 'exposed by Firewall rule'

class ExampleImplementation:
	'''
	implements the remidation of the events
	'''
	def __init__(self):
		self.run()

	def run(self):
		'''
		run the remidation of the events
		'''
		for jsonFile in [EXPOSED_DATABASE, SECURE_TRANSFER_REQUIRED, CRYPTO_MINING_IP]:
			with open(jsonFile) as file:
				msg: Dict[str, Any] = jsonLoad(file)
				msgDict: dict = jsonLoads(msg['Message'])
				eventTitle: str = msgDict['title']

				if TITLE_CRYPTO_MINING_IP == eventTitle:
					CryptoMiningIP(event=msg).handleEvent()

				elif TITLE_SECURE_TRANSFER_REQUIRED == eventTitle:
					EnforceDataBaseEncryption(event=msg).handleEvent()

				elif TITLE_EXPOSED_DATABASE in eventTitle:
					ExposedDatabase(event=msg).handleEvent()


if __name__ == '__main__':
	ExampleImplementation().run()
