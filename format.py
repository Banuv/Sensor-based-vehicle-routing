import csv
import numpy


def format():

	a = [[]]

	b = []

	f_array = []

	z = []


	c = 0
	d = 0
	l = 0

	#load csv values of the heat map to format
	a = numpy.loadtxt('heatmap.csv', dtype = 'int', delimiter=',', usecols=range(3))


	#removing colomn end buffers
	a = numpy.delete(a, list(range(-1, a.shape[0], 5)), axis = 0)


	c, d = a.shape

	#create a formatted (N X 4) matrix of heatmap elements
	for i in range (0, c):
		for j in (0, d-1):
			if j == 2:
				x = a[i][j]
				b.append(x)

	c = numpy.size(b)
	d = c / 4
	x = numpy.array(b)
	x.resize(int(d),4)



	#removing row buffer
	c = x.shape[0]
	x = numpy.delete(x, list(range(-1, a.shape[0], c)), axis = 0)

	c, d = x.shape

	for i in range (0, c):
		for j in range (0, d):
			l = x[i][j]
			f_array.append(l)

	#creating the final formatted array
	final_array = []
	start = 0
	endVar = 4
	end = endVar
	while len(final_array) is not c:
		final_array.append(f_array[start:end])
		start = end
		end = end + endVar


#	print(final_array)
	return final_array


def main():
	format()
	print('done formatting')


if __name__ == '__main__':
	main()


            
