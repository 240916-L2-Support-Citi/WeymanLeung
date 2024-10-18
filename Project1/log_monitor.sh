#!/bin/bash

# Path to log file
LOGFILE="/home/leungweyman/Revature/WeymanLeung/Project1/app.log"
USERNAME="leungweyman"

# Read last 60 logs in LOGFILE
tail -n 60 $LOGFILE | while read line; do
	# Collect first 2 columns of line using awk
	TIMESTAMP=$(echo $line | awk '{print $1, $2}')
	# Search for Error/Fatal using grep
	LEVEL=$(echo $line | grep -o 'ERROR\|FATAL')
	# Collect everything after ']' and escape quotes
	MESSAGE=$(echo $line | awk -F '] ' '{print $2}' | sed "s/'/''/g")

	# Convert timestamps into seconds for comparison
	CURRENTTIME=$(date +%s)
	PREVIOUSTIME=$(date -d "$TIMESTAMP" +%s)
	DIFFERENCE=$((CURRENTTIME - PREVIOUSTIME))

	# Check difference between two timestamps (1 min), Check if non zero value, if non zero, it is valid
	if [[ $DIFFERENCE -le 60 ]] && [[ -n $LEVEL ]]; then
		# echo "${TIMESTAMP} | ${LEVEL} | ${MESSAGE}"
		echo $line
		# Insert log into database
		# Added unique constraint on timestamp on table
		psql -U $USERNAME -d "project1" -c "INSERT INTO log_entries (timestamp, level, message) VALUES ('$TIMESTAMP', '$LEVEL', '$MESSAGE')";
		# echo "Inserted ${line} into database" 
	fi
done
