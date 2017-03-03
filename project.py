#!/usr/bin/python

"""
Inventory allocator
Usage: project.py [-h] [--inv <inventory filename>] [--inp <input filename>] [--out <Output filename>]
Default inventory filename: inventory.txt
Default input filename: input.txt
Default output filename: output.txt
"""

import sys
import json
import argparse

def inventoryAlloctor():
	class openFile:
		def __init__ ( self, fileName, mode ):
			try:
				self.fl = open ( fileName, mode )
			except IOError, e:
				print "Error : " + str(e)
				sys.exit()
		def readJson ( self ):
			return json.loads( self.fl.read() )
		
		def writeJson ( self, jsonList ):
			json.dump( jsonList, self.fl, indent=4 )

		def __del__ ( self ):
			self.fl.close()

	parser = argparse.ArgumentParser( description="Inventory allocator" )
	parser.add_argument( "--inv", default="inventory.txt", help="Inventory filename" )
	parser.add_argument( "--inp", default="input.txt", help="Input filename" )
	parser.add_argument( "--out", default="output.txt", help="Output filename" )
	invFlnm = parser.parse_args().inv
	inpFlnm = parser.parse_args().inp
	outFlnm = parser.parse_args().out

	inventory = openFile( invFlnm, "r" ).readJson()
	input = openFile( inpFlnm, "r" ).readJson()

	invProdList = [ item.keys()[0] for item in inventory ]
	invQuanList = [ item.values()[0] for item in inventory ]

	outJson = []
	for order in input:
		if all( item == 0 for item in invQuanList ):
			break
		header = order[ "Header" ]
		lines = order[ "Lines" ]
		quanOrderList, quanAllocList, quanBackList = [], [], []
		idxLine = 0
		invalidOrder = False
		for idxInv in range( len( invProdList )):
			if idxLine >= len( lines ):
				quanOrder, quanAlloc, quanBack = 0, 0, 0
			else:
				if invProdList[ idxInv ]  == lines[ idxLine ][ "Product" ]:
					quanOrder = lines[ idxLine ][ "Quantity" ]
					if quanOrder >= 6:
						invalidOrder = True
						continue
					elif invQuanList[ idxInv ] >= quanOrder:
						quanAlloc, quanBack = quanOrder, 0
						invQuanList[ idxInv ] -= quanOrder
					else:
						quanBack = quanOrder
					idxLine += 1
				else:
					quanOrder, quanAlloc, quanBack = 0, 0, 0
			quanOrderList.append( quanOrder )
			quanAllocList.append( quanAlloc )
			quanBackList.append( quanBack )

		if all( item == 0 for item in quanOrderList ):
			invalidOrder = True

		if invalidOrder:
			outJson.append({ "Header": header, "Invalid order": quanOrderList })
		else:
			outJson.append({ "Header": header, "Order": quanOrderList, "Allocated":  quanAllocList, "Back Ordered": quanBackList })

	openFile( outFlnm, "w" ).writeJson( outJson )

if __name__ == "__main__":
	inventoryAlloctor()
