# This is the Server.py file containing source code about Server
# being developed to provide services to clients
# About Author: Pushkar Bhattarai

from socket import *

messageToSend = "" # a container to send message to client

serverName = gethostname() # getting hostname of local host
serverPort = 5000 # using port in the local host
serverSocket = socket(AF_INET, SOCK_STREAM) # creating a socket
serverSocket.bind((serverName, serverPort)) # binding it to server and port
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # reusing server and port
serverSocket.listen(5) # Listening to maximum 5 connections
print("Server is ready for connections...")

while True:
	connectionSocket, address = serverSocket.accept() # initiating a connection
	#print("\n Client connected from: ", address)
	
	messageReceived = connectionSocket.recv(1024) # message is received in messageReceived varialble
	receivedMsg = messageReceived.decode("utf-8") # decoded message is stored in receivedMsg
	
	# For initial connection where Authentication is done
	if receivedMsg[0] == "0": # 0 is used to identify the type of received message to denote the task
		receivedMsg = receivedMsg.strip('0') # stripping off 0 
		print("\nVerifying Username and Password\n")
		try:
			infile = open("users.txt",'r') # accessing user.txt file to tally username and passwords
			line1 = ""
			isTrue = False
			for line in infile: # using for loop to find username and password
				line1 = line
				line1 = line1.rstrip('\n')
				if line1 == receivedMsg:
					isTrue = True # if username/password is found isTrue boolean is set to true
					break				
			infile.close()	
			if isTrue:
				print("Authenticated\n")
				messageToSend = "Authenticated" # sends "Authenticated" as message to client
			else:
				messageToSend = "failed"			
		except IOError:
			print("\n<---Users.txt File Not Found--->\n")

	# If Option 1 is selected the option detail will be send to this server for which it will
	# send the acknowledgement
	elif receivedMsg == "1":
		print("\nAcknowledgement Sent For Service No.1\n")
		messageToSend = '1'
	
	# After receiveing ack client will again request company details by sending name of company
	# For that below is required
	elif receivedMsg[0] == "1": # using 1 to denote the option used to show company details
		print("----Finding Company Details-----")
		receivedMsg = receivedMsg.strip('1') # stripping off 1
		try:
			infile = open("organisations.txt",'r') # opening organisations.txt file to check for company details
			line1 = ""
			istrue = True # to detect unavailability of company info
			for line in infile:
				line1 = line
				line1 = line1.rstrip('\n') # storing data of each line into line1
				infoList = line1.split() # splitting data using spaces
				
				if infoList[0] == receivedMsg: # checking whether company name is present that is stored in index 0
					print("----COMPANY FOUND-----")
					msgToSend = "1"+infoList[1]+"\t"+infoList[2] # storing comapny details
					messageToSend = msgToSend
					istrue = False
					break
				if istrue: # if information is not present
					messageToSend = "1Company Information Not in Database"
			infile.close()		
		except IOError:
			print("\n<---Organisation.txt File Not Found--->\n")
	
	# If option 2 is selected
	# min, max and mean is calculated here
	elif receivedMsg == "2":
		print("----Calculating Please Wait...-----")	
		try:
			infile = open("organisations.txt",'r')
			line1 = ""
			infoList2 = []
			
			for line in infile:
				line1 = line
				line1 = line1.rstrip('\n') # storing data of each line
				infoList = line1.split() # splitting according to spaces
				infoList2 += [infoList[3]] # storing data in index 3 in new infoList2

			minimum = min(infoList2) # finding minimum value from the list
			maximum = max(infoList2) # finding maximum value from the list
			# to find mean value
			total = 0.0
			for value in infoList2:
				total += float(value)
			mean = total/len(infoList2)
			# sending all min max and mean value at once
			messageToSend = "2"+str(minimum)+"\t"+str(maximum)+"\t"+str(mean)
			infile.close()	
			
		except IOError:
			print("\n<---Organisations.txt File Not Found--->\n")
	
	# Sending message back to client
	connectionSocket.send(messageToSend.encode("utf-8"))
	connectionSocket.close()
	