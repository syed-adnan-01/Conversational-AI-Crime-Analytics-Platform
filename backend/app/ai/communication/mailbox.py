class Mailbox:
    def __init__(self): self.messages = []
    def push(self, message): self.messages.append(message)
    def drain(self): result, self.messages = self.messages, []; return result
