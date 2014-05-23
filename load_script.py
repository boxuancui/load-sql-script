import csv
import sys

scriptName = sys.argv[0]
fileName = sys.argv[1]
hasHeader = sys.argv[2]
dlm = sys.argv[3]

if dlm == "\\t":
	file = csv.reader(open(fileName, "r"), delimiter = "\t")
else:
	file = csv.reader(open(fileName, "r"), delimiter = dlm)
firstLine = file.next()
nCol = len(firstLine)
header = []

if __name__ == "__main__":
	if hasHeader.lower()[0] == "y":
		header = firstLine
	elif hasHeader.lower()[0] == "n":
		for i in range(nCol):
			header.append("V" + str(i))
	else:
		print "Please specify if the data has a header: yes or no?"
	
	
	
	print header


