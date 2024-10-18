import psycopg
import datetime

fileName = "/home/leungweyman/Revature/WeymanLeung/Project1/alert.log"

try:
	# Connection to the database
	with psycopg.connect(
		"dbname=project1 user=leungweyman password=pizza1 host=/var/run/postgresql port=5432"
	) as connection:
		with connection.cursor() as my_cursor:
			# Count number of rows where level is ERROR and time difference is within minute
			my_cursor.execute("SELECT COUNT(*) FROM log_entries WHERE level = 'ERROR' AND (timestamp >= NOW() - interval '1 minute')")
			error_count = my_cursor.fetchone()[0]

			# Count number of rows where level is FATAL and time difference is within minute
			my_cursor.execute("SELECT COUNT(*) FROM log_entries WHERE level = 'FATAL' AND (timestamp >= NOW() - interval '1 minute')")
			fatal_count = my_cursor.fetchone()[0]

		# Write to alert log file with timestamp if thresholds are hit
		with open(fileName, 'a') as file:
			# Timestamp for better logging purposes
			current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			# Error threshold is 5
			if error_count >= 5:
				file.write(f"Timestamp: {current_timestamp} Alert: Error Threshold Hit Count: {error_count} \n")
			# Fatal threshold is 1
			if fatal_count >= 1:
				file.write(f"Timestamp: {current_timestamp} Alert: Fatal Threshold Hit Count: {fatal_count} \n")

except Exception as e:
	print(f"Error connecting to db: " + e)