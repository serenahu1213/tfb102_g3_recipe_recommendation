from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from recomm_recipes import *


def Carousel_Template(recommRecipes):               
    message = TemplateSendMessage(
        alt_text='Carousel template',  
        template=CarouselTemplate(columns=[
            CarouselColumn(
                thumbnail_image_url=recommRecipes[0][2],
                title=recommRecipes[0][1],
                text='預估花費: $ '+str(recommRecipes[0][4])+'\n預估熱量: '+str(recommRecipes[0][5])+' cal',
                actions=[MessageTemplateAction(label='所需食材', text=str(recommRecipes[0][1])+'所需食材'),
                         URITemplateAction(label='查看愛料理詳細食譜', uri='https://icook.tw/recipes/'+str(recommRecipes[0][0])),
                         MessageTemplateAction(label='我要煮!', text='我要煮'+str(recommRecipes[0][1])+'!')
                        ]
            ),
            CarouselColumn(
                thumbnail_image_url=recommRecipes[1][2],
                title=recommRecipes[1][1],
                text='預估花費: $ '+str(recommRecipes[1][4])+'\n預估熱量: '+str(recommRecipes[1][5])+' cal',
                actions=[MessageTemplateAction(label='所需食材', text=str(recommRecipes[1][1])+'所需食材'),
                         URITemplateAction(label='查看愛料理詳細食譜', uri='https://icook.tw/recipes/'+str(recommRecipes[1][0])),
                         MessageTemplateAction(label='我要煮!', text='我要煮'+str(recommRecipes[1][1])+'!')
                        ]
            ),
            CarouselColumn(
                thumbnail_image_url=recommRecipes[2][2],
                title=recommRecipes[2][1],
                text='預估花費: $ '+str(recommRecipes[2][4])+'\n預估熱量: '+str(recommRecipes[2][5])+' cal',
                actions=[MessageTemplateAction(label='所需食材', text=str(recommRecipes[2][1])+'所需食材'),
                         URITemplateAction(label='查看愛料理詳細食譜', uri='https://icook.tw/recipes/'+str(recommRecipes[2][0])),
                         MessageTemplateAction(label='我要煮!', text='我要煮'+str(recommRecipes[2][1])+'!')
                        ]
            ),
            CarouselColumn(
                thumbnail_image_url=recommRecipes[3][2],
                title=recommRecipes[3][1],
                text='預估花費: $ '+str(recommRecipes[3][4])+'\n預估熱量: '+str(recommRecipes[3][5])+' cal',
                actions=[MessageTemplateAction(label='所需食材', text=str(recommRecipes[3][1])+'所需食材'),
                         URITemplateAction(label='查看愛料理詳細食譜', uri='https://icook.tw/recipes/'+str(recommRecipes[3][0])),
                         MessageTemplateAction(label='我要煮!', text='我要煮'+str(recommRecipes[3][1])+'!')
                        ]
            ),
            CarouselColumn(
                thumbnail_image_url=recommRecipes[4][2],
                title=recommRecipes[4][1],
                text='預估花費: $ '+str(recommRecipes[4][4])+'\n預估熱量: '+str(recommRecipes[4][5])+' cal',
                actions=[MessageTemplateAction(label='所需食材', text=str(recommRecipes[4][1])+'所需食材'),
                         URITemplateAction(label='查看愛料理詳細食譜', uri='https://icook.tw/recipes/'+str(recommRecipes[4][0])),
                         MessageTemplateAction(label='我要煮!', text='我要煮'+str(recommRecipes[4][1])+'!')
                        ]
            )
        ]
                                 )
    )
    
    
    return message

