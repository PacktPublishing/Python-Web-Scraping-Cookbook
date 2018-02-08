""" Defines the interface for writing a blob of data to storage """

from interface import Interface

class IBlobWriter(Interface):
	def write(self, filename, contents):
		pass 