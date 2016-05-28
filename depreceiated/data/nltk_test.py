import nltk   

html = open('0000004904-06-000034.txt')    
raw = nltk.clean_html(html)  
print(raw)
