import psycopg
import datetime

fileName = "/home/leungweyman/Revature/WeymanLeung/Project1/alert.log"

try:
	# connect to db
	with psycopg.connect(
		"dbname=project1 user=leungweyman password=pizza1 host=/var/run/postgresql port=5432"
	) as connection:
		with connection.cursor() as my_cursor:
			# count number of rows where level is ERROR and time difference is within min
			my_cursor.execute("SELECT COUNT(*) FROM log_entries WHERE level = 'ERROR' AND (timestamp >= NOW() - interval '1 minute')")
			error_count = my_cursor.fetchone()[0]

			# count number of rows where level is FATAL and time difference is within minute
			my_cursor.execute("SELECT COUNT(*) FROM log_entries WHERE level = 'FATAL' AND (timestamp >= NOW() - interval '1 minute')")
			fatal_count = my_cursor.fetchone()[0]

		with open(fileName, 'a') as file:
			# write to alert log file with timestamp if thresholds are hit
			current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			if error_count >= 5:
				print(f"Timestamp: {current_timestamp} Alert: Error Threshold Hit Count: {error_count} \n")
				file.write(f"Timestamp: {current_timestamp} Alert: Error Threshold Hit Count: {error_count} \n")
			if fatal_count >= 1:
				print(f"Timestamp: {current_timestamp} Alert: Fatal Threshold Hit Count: {fatal_count} \n")
				file.write(f"Timestamp: {current_timestamp} Alert: Fatal Threshold Hit Count: {fatal_count} \n")

except Exception as e:
	print(f"Error connecting to db: " + e)