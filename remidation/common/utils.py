from types import SimpleNamespace

def validateDictKeys(constsCls: type, inputDict: dict):
	'''
	validate dict keys
	Args:
		constsCls (type): class of consts
		inputDict (dict): dict to validate
		Returns:
				bool: True if dict is valid, False otherwise
	'''
	constValues = [value for name, value in vars(constsCls).items() if not name.startswith('__')]

	for const in constValues:
		if const not in inputDict.keys():
			return False

		if 	not inputDict[const]:
			return False
	
	return True

		

def convertDictToClassRecursion(inputDict: dict) -> SimpleNamespace:
		'''
		convert dict to class
		Args:
				inputDict (dict): dict to convert
				Returns:
						SimpleNamespace: converted dict
		'''
		for key in inputDict:
			if isinstance(inputDict[key], dict):
				inputDict[key] = convertDictToClassRecursion(inputDict[key])
			elif isinstance(inputDict[key], str) and '/' in inputDict[key]:
				parts = inputDict[key].lstrip('/').split('/')
				if len(parts) % 2 == 0:  # Ensure there are pairs of values
						inputDict[key] = SimpleNamespace(**dict(zip(parts[::2], parts[1::2])))
		return SimpleNamespace(**inputDict)
