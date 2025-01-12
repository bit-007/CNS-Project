# GIF MALWARE DETECTION 
This Flask application is designed to analyze GIF files and determine their safety by validating the GIF’s structure against the GIF89a specification. Here’s a brief overview:
Key Features:
	1.	File Upload Functionality:
  	•	Users can upload GIF files via a web form.
  	•	Uploaded files are saved in the uploads directory.
	2.	GIF Validation:
  	•	Checks if the file is a valid GIF by analyzing its binary data.
  	•	Ensures the GIF conforms to the GIF89a standard.
  	•	Processes headers, logical screen descriptors, color tables, extension blocks, and image data blocks to confirm the file’s integrity.
	3.	Safety Check:
  	•	Determines if there is unexpected data after the GIF’s trailer (0x3b).
  	•	If there is, the GIF is flagged as “unsafe.”
  	•	Otherwise, it is deemed “safe.”
	4.	User Feedback:
  	•	Displays a success or warning message based on the file’s safety.



<img width="1439" alt="Screenshot 2025-01-12 at 11 36 27 AM" src="https://github.com/user-attachments/assets/1095dae8-040b-4f14-a08d-5939fc27eaae" />
<img width="1440" alt="Screenshot 2025-01-12 at 11 36 14 AM" src="https://github.com/user-attachments/assets/8e7d2fca-7ee4-47f8-b1dc-08a219aaf2c0" />
