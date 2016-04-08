def main():
    lines = 0.0
    cnt = 0.0
    with open("log/log.csv") as f:
        for line in f:
	    lines += 1
	    if "ERR_RECUR" in line:
	        print line
	        cnt += 1

    print cnt/lines
main()
