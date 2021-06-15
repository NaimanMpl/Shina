images_list = ['https://media.discordapp.net/attachments/572843920187326465/634315089360584706/2.gif',
               'https://media.discordapp.net/attachments/572843920187326465/634313555859996672/7.gif',
               'https://media.discordapp.net/attachments/634328175991586816/634328214105489423/1.gif',
               'https://media.discordapp.net/attachments/634328175991586816/634328229829935104/3.gif',
               'https://media.discordapp.net/attachments/634328175991586816/634328233353150464/4.gif',
               'https://cdn.discordapp.com/attachments/634328175991586816/634328235156570132/5.gif',
               'https://media.discordapp.net/attachments/634328175991586816/634328251153645568/6.gif'
               ]

def get_imagees_list():
    return images_list

def append(args):
    images_list.append(args)

def remove(args):
    images_list.remove(args)


