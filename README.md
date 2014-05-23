load-sql-script
===============

Create SQL load script automatically

The script does not require setup or installation. It can be moved to the desired directory and used directly. It scans the data file line by line, instead of reading the enter file. "csv" and "datetime" module is used for parsing data.

Syntax:
python load_script.py fileName hasHeader dlm tableName

•	fileName: Name of data file. 
•	hasHeader: Column names: "yes" or "no"?
•	dlm: Delimiter: Any 1-character delimiter and "\t" for tab
•	tableName: Name of the table to be created on database


