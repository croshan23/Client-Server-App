# This is Client.py file containing source codes for client
# Which will interact with Server.py file to provide services
# Seeking by user running it
# About Author: Pushkar Bhattarai

from socket import *

serverResponse = "" # container to receive responses from server
messageToSend = "" # container to send message to server
counter = 1 # counter to check the number of failed attempts of user credentials
print("Client is ready...")
# function for welcome screen
def welcomeScreen():
	print("\n -------Welcom To Swinburne Server-----\n")
	print("\n ----------------------------------------")
	print("\t\t MENU")
	print("----------------------------------------")
	print("(1) Get Server Name and IP ")
	print("(2) Get Statistics Mean, Min and Max")
	print("(3) Quit Program")
	print("Enter your choice (1,2 or 3)")	


while counter < 3: # if failed attemps is 3, client system stops
	serverName = gethostname() # getting local host name
	serverPort = 5000 # using port in the local host
	clientSocket = socket(AF_INET, SOCK_STREAM) # creating a socket
	clientSocket.connect((serverName, serverPort)) # binding it to server and port
	#print("\n Connected to "+ serverName + " at " + gethostbyname(serverName))

	if serverResponse == "": # denoting the initial state where username/password should be asked
		messageToSend1 = input("Enter Username: ")
		messageToSend2 = input("Enter Password: ")
		messageToSend = "0"+messageToSend1+" "+messageToSend2 # appending 0 with the message to signify that user credential checking is to be done
	
	# if user credential checking is successfull, following will be performed
	elif serverResponse == "Authenticated": 
		print("\n<----------Congratulation!!! Your Credentials Are Verified------------>\n")
		welcomeScreen() # showing menu screen
		# Asking for user to enter their option to use services provided
		userInput = input("Enter YOUR OPTION: ")
		if userInput == '1':
			messageToSend = userInput # server will be asked to perform service designated by option 1
		elif userInput == '2':
			messageToSend = userInput # server will be asked to perform service designated by option 2
		elif userInput == '3': # closing the client system exploiting counter 
			counter = 3
			print("\n<----------Thank You! for using the service------------>\n")

	elif serverResponse == "failed": # if authentication is failed
		print("<----------Authentication Failed------------>")
		print("<------Please Enter Valid Credentials------->")
		print("<------Only Three attempts is Allowed------->")
		counter = counter+1 # tracking number of failed attempts
		messageToSend1 = input("Enter Username: ")
		messageToSend2 = input("Enter Password: ")
		messageToSend = "0"+messageToSend1+" "+messageToSend2 # appending 0 with the message to signify that user credential checking is to be done
			
	elif serverResponse == "1": # getting acknowledgement from server to run service required by option 1
		print("\n Acknowledgement Received From Server ")
		userInput = input("Enter the Company Name: ") # asking user to enter company name for which they want information
		messageToSend = "1"+userInput # using 1 to denote option 1 service
	
	elif serverResponse[0] == "1":
		# displaying server response that contains company information, to clients
		serverResponse = serverResponse.strip('1')
		print("<----------SERVER DETAILS ARE------------>")
		print(serverResponse)
		
		welcomeScreen()
		userInput = input("Enter YOUR OPTION: ")		
		if userInput == '1':
			messageToSend = userInput # server will be asked to perform service designated by option 1
		elif userInput == '2':
			messageToSend = userInput # server will be asked to perform service designated by option 2
		elif userInput == '3': # closing the client system exploiting counter
			counter = 3
			print("\n<----------Thank You! for using the service------------>\n")			
		
	elif serverResponse[0] == "2":
		serverResponse = serverResponse.strip('2') # using 2 in index 0 to denote the server response containg min, max and mean value
		# splitting server response and printing it separately
		infoList = serverResponse.split() 
		print("\nMINIMUM \t"+infoList[0])
		print("MAXIMUM \t"+infoList[1])
		print("MEAN \t\t"+infoList[2]+"\n")
		
		welcomeScreen()
		userInput = input("Enter YOUR OPTION: ")
		if userInput == '1':
			messageToSend = userInput # server will be asked to perform service designated by option 1
		elif userInput == '2':
			messageToSend = userInput # server will be asked to perform service designated by option 2
		elif userInput == '3': # closing the client system exploiting counter
			counter = 3
			print("\n<----------Thank You! for using the service------------>\n")
			
	# sending message to server
	clientSocket.send(messageToSend.encode("utf-8"))
	
	# receiving server message and decoding it
	messageReceived = clientSocket.recv(1024)
	serverResponse = messageReceived.decode("utf-8")

# closing client application	
print("closing connection")
clientSocket.close()


		