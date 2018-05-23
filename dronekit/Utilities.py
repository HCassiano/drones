def safe_input(message, typeInput)
	try:
		input_raw = raw_input (message)
		if typeInput == "INT":
			input_processed = int(input_raw)
		elif typeInput == "FLOAT":
			input_processed = float(input_raw)
		else:
			input_processed = str(input_raw)
		return input_processed
	except Exception as e:
		raise e
