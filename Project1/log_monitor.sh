#!/bin/bash

# Path to log file
LOGFILE="/home/leungweyman/Revature/WeymanLeung/Project1/app.log"
USERNAME="leungweyman"

# read last 60 logs in logfile
tail -n 60 $LOGFILE | while read line; do
	# grab first 2 columns date, time
	TIMESTAMP=$(echo $line | awk '{print $1, $2}')
	# search for error or fatal
	LEVEL=$(echo $line | grep -o 'ERROR\|FATAL')
	# grab everything after ] and escape quotes
	MESSAGE=$(echo $line | awk -F '] ' '{print $2}' | sed "s/'/''/g")

	# convert timestamp into seconds for comparison
	CURRENTTIME=$(date +%s)
	PREVIOUSTIME=$(date -d "$TIMESTAMP" +%s)
	DIFFERENCE=$((CURRENTTIME - PREVIOUSTIME))

	# if difference less than minute and if level non empty then its valid
	if [[ $DIFFERENCE -le 60 ]] && [[ -n $LEVEL ]]; then
		# echo "${TIMESTAMP} | ${LEVEL} | ${MESSAGE}"
		echo $line
		# added constraint in db for duplicate entries
		psql -U $USERNAME -d "project1" -c "INSERT INTO log_entries (timestamp, level, message) VALUES ('$TIMESTAMP', '$LEVEL', '$MESSAGE')";
		# echo "Inserted ${line} into database" 
	fi
done
