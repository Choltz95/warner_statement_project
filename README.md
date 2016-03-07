## Project
Identifying the number of spelling and/or grammar errors in a firm's financial statements. Statements are typically in HTML or XBRL format, and cleaning these documents in order to identify mistakes is quite difficult.

## Usage
python wraper.py <data/>{mandatory} <-g>{optional} <-uc>{optional} <-c #cores>{optional}

data: directory containing forms
-g: set flag if grammar checking is needed
-uc: set flag if case sensitivity (caped words checked)
-c: todo get #cores from command line

## References 
After the Deadline (http://www.afterthedeadline.com/api.slp)
PyEnchant (http://pythonhosted.org/pyenchant/tutorial.html)
