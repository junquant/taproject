from JiakBot import JiakBot

jiakbot = JiakBot()
sentence = "I don't know where to find good prawn noodles"

run = True
while run:
    sentence = input('User: ')
    if(sentence!='quit'):
        print('Bot: ',jiakbot.respond(sentence))
    else:
        print('bye bye')
        run=False
