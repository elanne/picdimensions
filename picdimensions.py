#!/usr/bin/python
import sys
import argparse
from PIL import Image
from decimal import Decimal

def main():
	check_and_process_arguments()

def check_and_process_arguments():
		
	parser = argparse.ArgumentParser(description="This program calculates the dimensions when cropping images.")
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-i', '--interactive', action='store_true')
	group.add_argument('-l', '--long', type=int, 
		help='Lenght of the long edge in pixels')
	group.add_argument('-s', '--short', type=int,
		help='Lenght of the short edge in pixels')
	parser.add_argument('-f', '--file', type=file,
		help='Image file for preserving dimensions')
	args = parser.parse_args()
	
	is_imagefile = None
	# if file was provided, check that it is an image file
	if args.file:
		is_imagefile, width, height = is_image(args.file)
		
		if is_imagefile = False:
			print "File is not an image file!"
			sys.exit(2)

	# if --interactive / -i given
	if args.interactive:
		if is_imagefile:
			interactive_shell(width, height)
		else:
			interactive_shell()

	# if --long / -l given
	elif args.long:
		if is_imagefile:
			calculate("L", args.long, width, height)
		else:
			calculate("L", args.long)
	
	# if --short / -s given
	elif args.short:
		if is_imagefile:
			calculate("S", args.short, width, height)
		else:
			calculate("S", args.short)

def is_image(file):
	try:
		imfile = Image.open(file)
		width, height = imfile.size
		return True, width, height
	except IOError:
		return False, 0, 0

def interactive_shell(img_width=None, img_height=None):
	while True:
		edge = raw_input("Long edge (L) or short edge (S)? ").upper()
		if edge in ["L","S"]:
			# ask for lenght
			while True:
				try:
					edge_length = int(raw_input("Input length of fixed edge: "))
					calculate(edge, edge_length, img_width, img_height)
					break
				except ValueError:
					print "Please input a number"
		else:
			print "Please choose L for long edge or S for short edge"
         
def calculate(edgeType, edge_length, img_width=None, img_height=None):
	shortfactor = None
	longfactor = None
	# calculate dimension factor if width and length provided
	if img_width and img_height:
		shorfactor, longfactor = calculate_factor(img_width, img_height)
		
	# edgeType is long:
	if edgeType in ["L"]:
		calculate_short_edge(edge_length, shortfactor)
	
	# edgeType is short:
	if edgeType in ["S"]:
		calculate_long_edge(edge_length, longfactor)
	

def calculate_factor(img_width, img_height):
	if img_width <= img_height:
		shortfactor = Decimal(img_width)/Decimal(img_height)
		longfactor = Decimal(img_height)/Decimal(img_width)
	else:
		longfactor = Decimal(img_width)/Decimal(img_height)
		shortfactor = Decimal(img_height)/Decimal(img_width)
	return shortfactor, longfactor


def calculate_short_edge(edge_length, factor=None):
	dimensions = [(50,70), (30,40), (10,15), (10,13)]
	for x,y in dimensions:
		short_edge = int(x*edge_length/y)
		print "%sx%s cm image: short edge is %s px. New dimensions are %sx%s px." \
		% (x, y, short_edge, short_edge, edge_length)
	if factor:
		short_edge = int(factor*edge_length)
		print "To preserve dimensions, short edge is %s px. New dimensions are %sx%s px." \
		% (short_edge, edge_length, short_edge)

def calculate_long_edge(edge_length, factor=None):
	dimensions = [(50,70), (30,40), (10,15), (10,13)]
	for x,y in dimensions:
		long_edge = int(y*edge_length/x)
		print "%sx%s cm image: long edge is %s px. New dimensions are %sx%s px." \
		% (x, y, long_edge, edge_length, long_edge)
	if factor:
		long_edge = int(factor*edge_length)
		print "To preserve dimensions, long edge is %s px. New dimensions are %sx%s px." \
		% (long_edge, edge_length, long_edge)

   
if __name__ == "__main__":
   main()
