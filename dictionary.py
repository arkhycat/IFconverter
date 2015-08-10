import urllib.request
import json

class Dictionary:
	def __init__(self):
		yandex_key = "dict.1.1.20150809T173135Z.b71bc26c3704375e.4644f2de59215c34b7c5e69899bda4db8527dc2a"
		self.request = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key="+yandex_key+"&lang=en-ru&text="

	def request_json_translation(self, word):
		full_request = self.request+word
		translation = urllib.request.urlopen(full_request).read()
		return translation.decode('utf-8')

	def extract_translation_from_json(self, json_data):
		data = json.loads(json_data)
		result = []
		for tr_def in data['def']:
			for tr in tr_def['tr']:
				translation = tr['text']
				result.append(translation)
				if 'syn' in tr:
					for syn in tr['syn']:
						result.append(syn['text'])
		return result

	def get_translation(self, word):
		json_data = self.request_json_translation(word)
		return self.extract_translation_from_json(json_data)

