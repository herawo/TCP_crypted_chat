from Crypto.Cipher import AES
from Crypto import Random
import base64
import inspect

class CleverReceiver(object):
	def __init__(self, passphrase, allow_not_encoded):
		self.pseudo = None
		self.encoding = None
		self.message = None
		self.passphrase = passphrase
		self.allow_not_encoded = allow_not_encoded
		
	def decypher_and_decode(self, rcv_message):
		if rcv_message.find(b'> [') is -1:
			if self.allow_not_encoded :
				return rcv_message.decode()
			else:
				raise Exception("Can't communicate without encoding"
								"when using only encoded mode")
		index = rcv_message.find(b'> ')
		self.pseudo = rcv_message[:index]
		self.encoding = rcv_message[(index+3):(index+6)]
		self.message = rcv_message[(index+7):]           
		try:
			method = getattr(self, 'decrypt_' + self.encoding.decode())
			return method(self.message)
		except Exception:
			raise Exception("Unknown encryption type")
		
	def decrypt_AES(self, message):
		b64decoded = base64.b64decode(message)
		decryption_suite = AES.new(
			self.passphrase.encode('utf-8'),
			AES.MODE_CFB,
			'This is an IV456'.encode('utf-8'),
		)
		decrypted_text = decryption_suite.decrypt(b64decoded)
		decoded = decrypted_text.decode()
		return decoded
		
	def debug(self):
		attributes = inspect.getmembers(
			self,
			lambda a:not(inspect.isroutine(a))
		)
		attr_values = [a for a in attributes if not(
			a[0].startswith('__') and a[0].endswith('__')
		)]
		for attr_value in attr_values:
			print(attr_value[0] + " = " + str(attr_value[1]))
			
			
class CleverSender(object):
	
	def __init__(self, passphrase, allow_not_encoded):
		self.encoding = None
		self.passphrase = passphrase
		self.allow_not_encoded = allow_not_encoded
	
	def send_message(self, message):
		if  message[0] != '[' :
			return message.encode("utf-8")
		else:
			crypt_index_end = message.find(']')
			self.encoding = message[1:(crypt_index_end)]
			try:
				method = getattr(
					self,
					'encrypt_' + self.encoding
				)
				return method(message[(crypt_index_end+1):])
			except Exception:
				raise Exception("Unknown encryption type")
			
	
	def encrypt_AES(self, message):
		obj = AES.new(
			self.passphrase.encode('utf-8'),
			AES.MODE_CFB,
			'This is an IV456'.encode('utf-8'),
		)
		encoded = message.encode("utf-8")
		ciphertext = obj.encrypt(encoded)
		b64_encoded = base64.b64encode(ciphertext)
		
		return b'['+ self.encoding.encode('utf-8') + b']' + b64_encoded
			
		
