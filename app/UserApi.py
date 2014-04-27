class ConversationContainer:
        def __init__(self):
            #for now the container is a dictionary
            self.container = {}
        def buildKey(recipients):
            return ".".join(recipients.sort)
        def add(self, recipients, message):
            recipientsKey = buildKey(recipients)
            if recipientsKey in self.container:
                self.container[recipientsKey].append(message)
            else:
                self.container[recipientsKey] = [message]
        def getConversation(self, recipients):
            return self.container.get(tuple(recipients))
            
class User:
    def __init__(self, userID, conversationContainer=None):
        self.userID = userID
        if conversationContainer:
            self.conversationContainer = conversationContainer
        else:
            self.conversationContainer = ConversationContainer()
    def receiveMessageCallback(self, recipients, message):
        self.conversationContainer.add(recipients, message)
    def getConversation(self, recipients):    
        return self.conversationContainer.getConversation(recipients)

        #author is a User object, recipients is a list of strings (userIDs), message is any type

class UserHandler:
    
def sendMessage(author, recipients, message):
    #TODO authenticate author
    if not author.userID in recipients:
        recipients.append(author)
    for recipient in recipients:
        #find User objects from the userIDs provided in recipients list
        UserHandler.deliverMessage(recipient,recipients, message)


sendingUser = User("sendingUser")
userA = User("userA")
userB = User("userB")

recipientList = [sendingUser, "userA", "userB"]
sendMessage("blah", ["userA","userB"], "asdf")
print(userA.getConversation([userA,userB]))
print(userB.getConversation([userA,userB]))


