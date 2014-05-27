load-sql-script
===============

Create SQL load script automatically

The script does not require setup or installation. It can be moved to the desired directory and used directly. It scans the data file line by line, instead of reading the enter file. "csv" and "datetime" module is used for parsing data.

Syntax: <br/>
<b>python load_script.py</b> [<i>fileName</i>] [<i>hasHeader</i>] [<i>dlm</i>] [<i>tableName</i>]

<ul>
<li><i>fileName</i>: Name of data file</li>
<li><i>hasHeader</i>: Has column names? "yes" or "no"?</li>
<li><i>dlm</i>: Delimiter. Any 1-character delimiter and "\t" for tab</li>
<li><i>tableName</i>: Name of the table to be created on database</li>
</ul>

