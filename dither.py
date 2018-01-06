import cv2
import numpy as np
import ast
from time import sleep
from math import floor
import argparse

mid_point = 128

def one_dimensional_error_diffusion(img):
	rows,cols = img.shape

	for row in range(0,rows):
		error = 0
		for col in range(0,cols):

			current_pixel = img_pixel(img, row, col) + error
			if(current_pixel < mid_point):
				error = current_pixel
				img[row, col] = 0
			else:
				error = current_pixel - 255
				img[row, col] = 255

	return img

def two_dimensional_error_diffusion(img, matrix):
	width = len(matrix)
	height = len(matrix[1])

	if width != height:
		print("Matrix width does not equal height!")
		return

	mid = width - floor(width / 2)
	divider = nested_sum(matrix)

	if divider is 0:
		print("Divider equals zero!")
		return

	rows,cols = img.shape

	for col in range(0,cols):
		error = 0		
		for row in range(0,rows):
			current_pixel = img[row, col]

			if(current_pixel < mid_point):
				error = current_pixel
				img[row, col] = 0
			else:
				error = current_pixel - 255				
				img[row, col] = 255
				
			img = distribute_error(img, row, col, matrix, error)

	return img

def distribute_error(img, x, y, matrix, error):
	width = len(matrix)
	mid = width - floor(width / 2)
	matrix_range = 2
	divider = nested_sum(matrix)

	y_count = 0
	for error_y in range(-matrix_range, matrix_range + 1):
		x_count = 0
		for error_x in range(-matrix_range, matrix_range + 1):

			if matrix[y_count][x_count] is not 0:
				img_pixel_adjust(img, x, y, (error / divider) * matrix[y_count][x_count], offset_x=error_x, offset_y=error_y)

			x_count += 1
		y_count += 1

	return img

def nested_sum(L):
	total = 0
	for i in L:
		if isinstance(i, list):
			total += nested_sum(i)
		else:
			total += i
	return total

def set_to_zero(L):
	list = L
	for i in range(0,len(list)):
		for j in range(0,len(list[i])):
			list[i][j] = 0
	return list

def img_pixel(img, x, y, offset_x=0, offset_y=0):
	return img.item(x + offset_y, y + offset_y)

def img_pixel_set(img, x, y, new_value, offset_x=0, offset_y=0):
	rows, cols = img.shape
	if x + offset_x < rows and y + offset_y < cols:
		img.itemset((x + offset_x, y + offset_y), new_value)

def img_pixel_adjust(img, x, y, new_value, offset_x=0, offset_y=0):
	rows, cols = img.shape
	if x + offset_x < rows and y + offset_y < cols:
		img.itemset((x + offset_x, y + offset_y ), img.item(x + offset_x, y + offset_y) + new_value )


parser = argparse.ArgumentParser(description='Dither an image')
parser.add_argument("-f", help="Image Filepath")
args = vars(parser.parse_args())
img = cv2.imread(args['f'])
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

floyd_steinberg_matrix =	[[0,0,0],
							[0,0,7],
							[3,5,1]]

jarvis_judice_ninke_matrix =	[[0,0,0,0,0],
								[0,0,0,0,0],
								[0,0,0,7,5],
								[3,5,7,5,3],
								[1,3,5,3,1]]

atkinson_matrix =	[[0,0,0,0,0],
					[0,0,0,0,0],
					[0,0,0,1,1],
					[0,1,1,1,0],
					[0,0,1,0,10]]

print ("""
   1. Jarvis Judice Ninke
   2. Atkinson_matrix
   3. Custom...
   """)

use_custom = False

while True:
	sel = int(input("Make Selection...\n"));
	if sel == 1:
		two_dimensional_error_diffusion(img, jarvis_judice_ninke_matrix)
		break
	if sel == 2:
		two_dimensional_error_diffusion(img, atkinson_matrix)
		break
	if sel == 3:
		use_custom = True
		break

if use_custom:
	while True:
		custom = input("Enter matrix... [[0,0,0],[0,0,0... Dimensions must match\n")
		custom = ast.literal_eval(custom)
		two_dimensional_error_diffusion(img, custom)
		break

cv2.imwrite(args['f'][:-4] + '_output.png', img)

while True:

	cv2.imshow('window', img)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
