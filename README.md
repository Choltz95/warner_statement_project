## Project
Identifying the number of spelling and/or grammar errors in a firm's financial statements. Statements are typically in HTML or XBRL format, and cleaning these documents in order to identify mistakes is quite difficult.

## Usage
python wraper.py <`data/>{mandatory} <-g>{optional} <-uc>{optional} <-c #cores>{optional}

**data**: directory containing forms <br />
**-g**: set flag if grammar checking is needed <br />
**-uc**: set flag if case sensitivity (caped words checked) <br />
**-c**: todo get #cores from command line

## Files & Directories
**readme.md**: This file
**simon\_school\_collab\_tr.pdf**: First technical report produced detailing approach <br />
**words**: The Unix words file composes the foundation for our wordlist.[3] <br />
**loughran_mcdonald.txt**: Form 10-K specific dictionary  compiled through research done by Bill McDonald and Tim Loughran.[1] <br />
**custom_dict.txt**: Set of custom words we update as we go through the data. <br />
**dict**: Complete dictionary used by the program. Combination of words, loughran_mcdonald.txt, and custom_dict.txt <br />
**cc.txt**: data file for cross_check.py <br />
**file_log**: A log of parsed files is kept on disk. <br />
**log.csv**: output of the program <br />
**old_log.csv**: output of the program prior to inclusion of the loughran_mcdonald.txt dictionary. <br />
**wraper.py**: Entry point and driver program for the project. The program takes a directory containing the Form 10-K documents and optional arguments including whether to look for grammar mistakes, parse upper-case words, and the number of cores to use. By default, the program will take advantage of the number of cores supported by your machine -1.  <br />
**count_errors.py**: For a given plaintext document, count and record instances of spelling and grammar mistakes using language_tool and pyEnchant.[0],[2] <br />
**cross_check.py**: comparison of output with loughran mcdonald dictionary. <br />
**html2text.py**: Takes an html or xbrl formatted document and returns flattened plaintext of any natural language description in the document. <br />
**merge_dicts.py**: program to merge multiple dictionaries <br />
**parse_lib.py**: Helper library for html2text. Contains methods to construct an explicit state machine, traverse the syntax tree, clean tags, and to extract document metadata. <br />
**stats.py**: program to gather some statistics from the log files. <br />
**update_log.py**: helper program for cross_check.py <br />
**word_freq.py**: grab current statistics of misspelled words. <br />
**depreciated/**: Directory containing depreciated tools and resources for this project

#Program

###Dictionary merge

    The dict file is produced by merge_dicts.py and is composed of words derived from three other dictionaries.
    +----------------+
    |     dict       |     
    | +------------+ |
    | |loughran-   | |
    | |mcdonald.txt| |
    | +------------+ |
    | +------------+ |
    | |  words     | |
    | +------------+ |
    | +------------+ |
    | |custom_dict | |
    | +------------+ |
    +----------------+

###Program process

    INPUT/LIBRARY     PROGRAM PROCESS        OUTPUT

    +--------+         +----------+
    |xbrl    +-------->+wraper.py |
    |document|         +-----+----+
    +--------+               |
                             |
                             |
                             v              +---------+
     +-------+         +-----+------+       | clean   |
     |parse_ +---------+html2text.py+------>+ txt     |
     |lib.py |         +-----+------+       | document|
     +-------+               |              +---------+
                             |
                             |
                             v
    +------+          +------+--------+     +--------+
    | dict +----------+count_errors.py+---->+log.csv |
    +------+          +---------------+     +--------+


##TODO and future topics
A large number words used in the Form 10-Ks include the names of corporations, the names of people, and the names of places. 
Currently, we manually add these names to our wordlist, but named-entity recognition is an area of natural language processing
which deas with extracting and classifying named entitities. There exist a number of approaches to implementing a system to do this,
and further research could be done on finding existing systems or implementing our own.

## References 
[depreciated]After the Deadline http://www.afterthedeadline.com/api.slp <br />
[0]language-tool <br />
[1]Loughran, McDonald Dictionary https://www3.nd.edu/~mcdonald/Word_Lists_files/Documentation/Documentation_LoughranMcDonald_MasterDictionary.pdf
[2]pyenchant(1.6.6) http://pythonhosted.org/pyenchant/tutorial.html<br />
[3]Unix Words https://en.wikipedia.org/wiki/Words_%28Unix%29 <br />