## Project
Identifying the number of spelling and/or grammar errors in a firm's financial statements. Statements are typically in HTML or XBRL format, and cleaning these documents in order to identify mistakes is quite difficult.

## Usage
python wraper.py <`data/>{mandatory} <-g>{optional} <-uc>{optional} <-c #cores>{optional}

data: directory containing forms <br />
-g: set flag if grammar checking is needed <br />
-uc: set flag if case sensitivity (caped words checked) <br />
-c: todo get #cores from command line

## References 
After the Deadline (http://www.afterthedeadline.com/api.slp)
pyenchant(1.6.6) (http://pythonhosted.org/pyenchant/tutorial.html)
