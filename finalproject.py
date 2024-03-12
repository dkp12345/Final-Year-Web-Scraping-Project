import logging
import json
from aiogram import *
import asyncio
import time
from aiogram.types import chat_permissions, inline_keyboard
import requests
from bs4 import BeautifulSoup
import random
import pymongo
from pymongo import MongoClient
import urllib.parse
from datetime import datetime, timedelta
import string

Admin = '@trade4u'
BotName = 'Chegg unblur by Trade4u'
mainGroupId = -100847392380

adminId = 1703027575


botLink = "https://t.me/cheggcheapunblurbot"

# API_TOKEN = '1834750087:AAFfudHVQ5vb-ZyiJr0errhBmUWanleTpo8'
API_TOKEN = '5773392136:AAH2Dr-RbV7-lf29yp0i2KjlcbB4gbQp1cc'

# Configure loggingṇ
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
client = Dispatcher(bot)


all_genid = []


lock_permissions = {
    'can_send_messages': False,
    'can_send_media_messages': None,
    'can_send_polls': None,
    'can_send_other_messages': None,
    'can_add_web_page_previews': None,
    'can_change_info': None,
    'can_invite_users': None,
    'can_pin_messages': None
}
unlock_permissions = {
    'can_send_messages': True,
    'can_send_media_messages': None,
    'can_send_polls': None,
    'can_send_other_messages': None,
    'can_add_web_page_previews': None,
    'can_change_info': None,
    'can_invite_users': None,
    'can_pin_messages': None
}

s = requests.Session()

cookie_list = [{
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'cookie': 'chegg_web_cbr_id=a; V=fc8df6e1933cb0e8785f5ef4ea25b01a6138d6d2a3b7d9.55028078; userData=%7B%22authStatus%22%3A%22Logged%20Out%22%2C%22attributes%22%3A%7B%22uvn%22%3A%22fc8df6e1933cb0e8785f5ef4ea25b01a6138d6d2a3b7d9.55028078%22%7D%7D; local_fallback_mcid=92178412797534659639217238785843533219; PHPSESSID=r50v05rogtg67btckaj9nftodj; user_geo_location=%7B%22country_iso_code%22%3A%22IN%22%2C%22country_name%22%3A%22India%22%2C%22region%22%3A%22UP%22%2C%22region_full%22%3A%22Uttar+Pradesh%22%2C%22city_name%22%3A%22Fatehpur+Chaurasi%22%2C%22postal_code%22%3A%22209871%22%2C%22locale%22%3A%7B%22localeCode%22%3A%5B%22en-IN%22%2C%22hi-IN%22%2C%22gu-IN%22%2C%22kn-IN%22%2C%22kok-IN%22%2C%22mr-IN%22%2C%22sa-IN%22%2C%22ta-IN%22%2C%22te-IN%22%2C%22pa-IN%22%5D%7D%7D; C=0; O=0; optimizelyEndUserId=oeu1631114968807r0.0684335019862421; _pxvid=8f310efc-10b9-11ec-ac27-41495664734c; __gads=ID=71fdb067d5b0ee9e-225e6e5691cb0010:T=1631114969:S=ALNI_MYrthbrfzrOadNIOBl4M3_O2-QgPw; usprivacy=1YNY; _omappvp=6m4fHr6vHEaGCvZJ8389sM6AfOLh6ZpxPBASSPsg1mlSYW97x9ZtPLBlm4zb2b9UUrYKO1ynvoaDVnvk9kdjPLr3f3e1r9GE; forterToken=288c73c867c449aa9ee284b78bef4b0e_1631114969525__UDF43b_13ck; adobeujs-optin=%7B%22aam%22%3Atrue%2C%22adcloud%22%3Atrue%2C%22aa%22%3Atrue%2C%22campaign%22%3Atrue%2C%22ecid%22%3Atrue%2C%22livefyre%22%3Atrue%2C%22target%22%3Atrue%2C%22mediaaa%22%3Atrue%7D; s_ecid=MCMID%7C92178412797534659639217238785843533219; AMCVS_3FE7CBC1556605A77F000101%40AdobeOrg=1; _rdt_uuid=1631114971070.98f99dfd-e173-49cf-9be1-0f3bde20a47a; _ga=GA1.2.617502122.1631114970; _gid=GA1.2.1989534726.1631114971; _gcl_au=1.1.76699181.1631114971; _fbp=fb.1.1631114971567.1552694451; mcid=92178412797534659639217238785843533219; id_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImphbWlyY2hlZ2dAb3V0bG9vay5jb20iLCJpc3MiOiJodWIuY2hlZ2cuY29tIiwic3ViIjoiZjFlZTU3NzUtYTdjNC00ZDE5LWI2MDEtZDY4YjI5Yzg1YzAxIiwiYXVkIjoiQ0hHRyIsImlhdCI6MTYzMTExNDk4MiwiZXhwIjoxNjM5MDE0NzE5LCJyZXBhY2tlcl9pZCI6ImFwdyJ9.Y8FNMCBuvcrsBQOtkwrNfOHHXxE7Y8JUWjzP-dcnD-TOExkNs5Hif6hsHDmbDw1uqrXVkTI1bjYXqVVHySlmt9GNcSOr88EWIU3CgkiaGxgUOxbdt5DFOuVXjD2tEpBb7sBUUOOjliT2NAwy1jbeJjeOgLvgl4o_XFVaOsX4fz8HF5AImEQJPwfNAkqFVkyYUJPIGyQIneuHpPaPCPCSvTAxslQXMd5jwqNKr5kN0KQX9vZ5gy1EBVEE9mkl1mClUREzdl7uI8qLMlPhx3oEx6rIoymZEiGyvpnp4t-EgGxHs7v8iBlM0Ujm7sWPVU2M7kImbrkdaCG6fRxPlq6c3g; SU=Eg5hPwjllJg-s4TsJiZtT28TA0kvj7YXJplwxRI1LRZ8b6Xd6uFE-mw0t_Vgy2wAfpopDmY1J9Wan8NUZVhQOrvy0cPlG1kLPwWC1T752HhHRh7Afo6MNNnlj92AVfuk; U=bcbdd2ed4077d323768938559c65371e; _sdsat_cheggUserUUID=f1ee5775-a7c4-4d19-b601-d68b29c85c01; _ym_uid=1631114987712911147; _ym_d=1631114987; _ym_isad=2; _cs_c=1; AMCV_3FE7CBC1556605A77F000101%40AdobeOrg=-408604571%7CMCMID%7C92178412797534659639217238785843533219%7CMCIDTS%7C18879%7CMCAID%7CNONE%7CMCOPTOUT-1631122193s%7CNONE%7CMCAAMLH-1631719793%7C12%7CMCAAMB-1631719793%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCSYNCSOP%7C411-18886%7CvVersion%7C4.6.0%7CMCCIDH%7C-2104721531; intlPaQExitIntentModal=hide; exp=A311C%7CA803B%7CC024A%7CA209A%7CA212A%7CA560B%7CA448A%7CA270C%7CA278C%7CA966F%7CA890H; expkey=6F7150F8D3893927CF4C7D76E8E64CE0; _scid=7f4ef356-4fae-4b88-88e5-875b4d3bf7fa; _sctr=1|1631039400000; _vid_t=he9/2E8PSeFUg/6CZnefEWq9LtcOQHwwRmR0v0e2nbFfMgWZ6qygrRcuo456CDrfmFKvTySZ2VdEUg==; DFID=web|AO1rVlHf6QzNETl6Zj5C; CVID=482ce327-77ce-47dd-9663-6271eb244bda; _sdsat_authState=Hard%20Logged%20In; _cs_cvars=%7B%221%22%3A%5B%22Page%20Name%22%2C%22home%20page%22%5D%7D; _pxff_tm=1; CSID=1631121682957; ab.storage.deviceId.b283d3f6-78a7-451c-8b93-d98cdb32f9f1=%7B%22g%22%3A%22f9378df4-3360-3192-44d1-af1d8cf06ff4%22%2C%22c%22%3A1631114970243%2C%22l%22%3A1631121685136%7D; ab.storage.userId.b283d3f6-78a7-451c-8b93-d98cdb32f9f1=%7B%22g%22%3A%22f1ee5775-a7c4-4d19-b601-d68b29c85c01%22%2C%22c%22%3A1631114986333%2C%22l%22%3A1631121685138%7D; schoolapi=null; _gat=1; s_pers=%20buFirstVisit%3Dcore%252Ccs%7C1788882188808%3B%20gpv_v6%3Dchegg%257Cweb%257Ccore%257Chome%2520page%7C1631123498031%3B; _px3=923ee04d26af25fb018c104062e26d8aa409a2291734bd8390a968008c5bece1:wrn6I6klvHWwaca/TYTtLXgixTPAVk+K8Zn9sAjA2uZ/rbf2h/7U4/yYutelcqM8djjnaKJFvL7KyoQECI6nBA==:1000:gFx5PP1LtVeCETWZMsQgR0++rdPg2GE6FjGxLeCLw73XWxByqH0GmRvWAU1CzXi/gxxR5nzLWUCzuJsJX61lyXR8LGhvErNeH0iWRsOab0ah6U0v5gX2CfXJ9LhesmdySurunQQheXbeSW3UfzQs9BPBJ8yCSbHU8SJbojsqJmrCF+Bgykzqvwa63YL+zItjW2Sej7b3BNKBJPYAVcK31w==; _px=wrn6I6klvHWwaca/TYTtLXgixTPAVk+K8Zn9sAjA2uZ/rbf2h/7U4/yYutelcqM8djjnaKJFvL7KyoQECI6nBA==:1000:/+YnG+w2ALEieeIc4fWJoZGMWsYVqL8aeVh+Mch8HtMtCuygsBtE5INwYbb3udwY6ESwOW7vbjfGbGh4GQRFSrG7Gw/elxERjmut5O0yQaKUTzJgDskAPJ8YWDtlfjEBlkjgczslII4GnMaFBTXKV465VFvPR72EnILGaW7jWW29kIyzbNUincf2P0+ej6/HrfO9Eh6KO97ZOczNR6Ercg+kFrOgXiwKR726DcgrxCTK4LSjMfN8Fw4KomH2UEqOOQs9NUN8gtZaNE4ediVSng==; OptanonConsent=isIABGlobal=false&datestamp=Wed+Sep+08+2021+22%3A51%3A39+GMT%2B0530+(India+Standard+Time)&version=6.18.0&hosts=&consentId=45ed9953-ce59-408a-a556-fe4049be96b5&interactionCount=1&landingPath=NotLandingPage&groups=snc%3A1%2Cfnc%3A1%2Cprf%3A1%2CSPD_BG%3A1%2Ctrg%3A1&AwaitingReconsent=false; s_sess=%20buVisited%3Dcore%252Ccs%3B%20s_sq%3Dcheggincriovalidation%253D%252526pid%25253Dchegg%2525257Cweb%2525257Ccore%2525257Cmyaccount%2525257Coverview%252526pidt%25253D1%252526oid%25253Dhttps%2525253A%2525252F%2525252Fwww.chegg.com%2525252F%252526ot%25253DA%3B%20cheggCTALink%3Dfalse%3B%20SDID%3D2863C992E764161C-1D33532F80091E4E%3B%20s_ptc%3D0.00%255E%255E0.00%255E%255E0.00%255E%255E0.62%255E%255E0.56%255E%255E0.21%255E%255E2.85%255E%255E0.05%255E%255E4.09%3B; _uetsid=8fef0d4010b911ec800c9335677de6f3; _uetvid=8fef6ac010b911ecba1d27a1716895c0; wcs_bt=s_4544d378d9e5:1631121699; ab.storage.sessionId.b283d3f6-78a7-451c-8b93-d98cdb32f9f1=%7B%22g%22%3A%2253fdd4e8-ed76-bb1f-a573-dc370c003688%22%2C%22e%22%3A1631123499679%2C%22c%22%3A1631121685133%2C%22l%22%3A1631121699679%7D; _tq_id.TV-8145726354-1.ad8a=b1dfc79303c9a9d4.1631114973.0.1631121702..; _cs_id=38f48a27-2c90-a652-8700-fad242d0c161.1631114989.3.1631121705.1631121705.1.1665278989499; _cs_s=1.1.0.1631123505964; __CT_Data=gpv=7&ckp=tld&dm=chegg.com&apv_79_www33=7&cpv_79_www33=7',
    'origin': 'https://www.chegg.com',
    'accept': 'application/json',
    'content-type': 'application/json',
    "cache-control": "max-age=0",
    "deviceFingerPrintId": "web|A0oUFYO50M5NYadliOz5"
}]



def remove_tags(html):

    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    soup.find("h2", {"class": "guidance-header"}).decompose()
    soup.find("section", {"id": "general-guidance"}).decompose()
    soup.find("div", {"id": "select-view"}).decompose()
    # return data by retrieving the tag content
    return soup


@client.message_handler()
async def chegg(message: types.Message, amount=1):
    if message.chat.id == mainGroupId:

        if "https://www.chegg.com" in message.text:
            print("getting")
            user = str(message.from_user.id)
            u = 1
            if u == None:
               print(u)
            else:

                c_headers = random.choice(cookie_list)
                try:
                    if 'https://www.chegg.com' in message.text:
                        await bot.set_chat_permissions(mainGroupId, permissions=lock_permissions)
                        # await bot.send_message(-1001468490071,f"@{message.from_user.username or message.from_user.first_name} ask me the solution now please wait until the below timer complets..")
                        try:
                            if "questions-and-answers" in message.text:
                                req = requests.get(
                                    message.text, headers=c_headers)
                                soup = BeautifulSoup(
                                    req.content, 'html.parser')
                                qution = soup.find(
                                    "div", {"class": "ugc-base question-body-text"}, 'html.parser')
                                answer = soup.find(
                                    "div", {"class": "answer-given-body ugc-base"}, 'html.parser')
                                answer_by = soup.find_all(
                                    "span", {"class": "answerer-name"}, 'html.parser')
                                for tag in soup.select(".answer-given-body.ugc-base img"):
                                    if 'd2vlcm61l7u1fs.cloudfront.net' in tag['src']:
                                        tag["src"] = "https:" + tag["src"]
                                aid = str(req.content).split(
                                    'answerId="')[1].split('" >')[0]
                                like_dislike = requests.post(
                                    'https://www.chegg.com/study/_ajax/contentfeedback/getreview?entityType=ANSWER&entityId=+{}'.format(aid), headers=c_headers)
                                like_soup = like_dislike.json()
                                l1 = (like_soup['review_count'])
                                l2 = (l1['result'])
                                if "0" in l2:
                                    like = (l2['0'])
                                    like_number = (like['count'])
                                else:
                                    like_number = 0
                                if "1" in l2:
                                    dislike = (l2['1'])
                                    dislike_number = (dislike['count'])
                                else:
                                    dislike_number = 0
                                main_html = '''
                                                            <!DOCTYPE html>
                                                            <html lang="en">
                                                            <head>
                                                                <meta charset="UTF-8" />
                                                                <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                                                                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                                                                    <!-- CSS only -->
                                                                    <link
                                                                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"
                                                                    rel="stylesheet"
                                                                    integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6"
                                                                    crossorigin="anonymous"
                                                                    />
                                                                    <title>Powered by Homework Hub server</title>
                                                                </head>
                                                                <style>
                                                                    .body {
                                                                    width: 100px;
                                                                    }
                                                                    .alert {
                                                                    text-align: center;
                                                                    }
                                                                    .qution_header{
                                                                    text-align: center;
                                                                    color: rgb(
                                                                        37, 70, 175);

                                                                    }
                                                                    img {

                                                                max-width: 100%;

                                                                }
                                                                .question{
                                                                    padding: 30px;
                                                                }
                                                                .answer{
                                                                    padding: 30px;
                                                                }
                                                                </style>
                                                                <body>
                                                                    <div class="alert alert-success" role="alert">
                                                                    Powered by Homework Hub server | | join for chegg answers : https://discord.gg/HfYBKVWM9y
                                                                    </div>
                                                                </body>
                                                                <body>
                                                                    <div class="alert alert-danger" role="alert">
                                                                    THIS ANSWER LINK WILL EXPIRE IN 10 MIN
                                                                    </div>
                                                                </body>
                                                                </html>
                                                                '''
                                like_dislike_html = '''
                                                                <section >
                                                                    <div class="container my-3 bg-light">
                                                                    <div class="col-md-12 text-center">
                                                                    <button type="button" class="btn btn-primary">
                                                                        likes <span class="badge bg-secondary">{}</span>
                                                                    </button>
                                                                    <button type="button" class="btn btn-primary">
                                                                        dislikes <span class="badge bg-danger">{}</span>
                                                                    </button>
                                                                    </div>
                                                                </div>
                                                                </section>
                                                                '''
                                answer_given = '''
                                                                <section>
                                                                    <div class="card text-center">
                                                                        <div class="card-header">
                                                                        ANSWER GIVEN BY
                                                                        </div>
                                                                        <div class="card-body">
                                                                        <h5 class="card-title">{}</h5>
                                                                        </div>
                                                                        <div class="card-footer text-muted">
                                                                        Powered by Homework Hub server
                                                                        </div>
                                                                    </div>
                                                                </section>
                                                                '''
                                qution_html = '''
                                                                <section>
                                                                <div class="container my-5">
                                                                    <div
                                                                    class="row p-4 pb-0 pe-lg-0 pt-lg-5 align-items-center rounded-3 border shadow-lg"
                                                                    >
                                                                    <h1 class="qution_header">QUESTION</h1>
                                                                    <div class="question">
                                                                        {}
                                                                    </div>
                                                                    </div>
                                                                    </div>
                                                                </div>
                                                                </section>
                                                                '''
                                answer_html = '''
                                                                <section>
                                                                <div class="container my-5">
                                                                    <div
                                                                    class="row p-4 pb-0 pe-lg-0 pt-lg-5 align-items-center rounded-3 border shadow-lg"
                                                                    >
                                                                    <h1 class="qution_header">ANSWER</h1>
                                                                    <div class="answer">
                                                                        {}
                                                                    </div>
                                                                    </div>
                                                                    </div>
                                                                </div>
                                                                </section>
                                                                '''
                                file = open('Answer.html', 'w',
                                            encoding='utf-8')
                                file.write(str(main_html))
                                file.write(
                                    str(answer_given).format(answer_by))
                                file.write(str(like_dislike_html).format(
                                    like_number, dislike_number))
                                file.write(str(qution_html).format(qution))
                                file.write(str(answer_html).format(answer))
                                file.close()
                                # try:
                                #     url = "https://siasky.net/skynet/skyfile"
                                #     link_files = [
                                #         ('file', ("Answer.html", open(
                                #             './Answer.html', 'rb'), 'text/html'))
                                #     ]
                                #     headers7 = {
                                #         'referrer': 'https://siasky.net/'
                                #     }
                                #     response = requests.request(
                                #         "POST", url, headers=headers7, files=link_files)
                                #     limb = "https://siasky.net/" + \
                                #         response.json()["skylink"]
                                #     keyboard = inline_keyboard.InlineKeyboardMarkup(
                                #         row_width=3)
                                #     button = inline_keyboard.InlineKeyboardButton(
                                #         'Answer', url=limb)
                                #     keyboard.add(button)
                                #     await message.reply(f"✅🟢✅🟢✅🟢✅🟢✅🟢✅🟢\n\n @{message.from_user.username or message.from_user.first_name} please click the below link and download \n\n ✅🟢✅🟢✅🟢✅🟢✅🟢✅🟢", reply_markup=keyboard)
                                # except Exception as e:
                                #     print(e)
                                #     doc = open('Answer.html', 'rb')
                                #     # try:
                                #     #   await bot.send_document(message.from_user.id, doc)
                                #     # except:
                                #     #   await bot.send_document(message.chat.id, doc)
                                #     # await message.reply('dont send another question immediately check @freejaffawarrior ')
                                #     await bot.send_document(message.chat.id, doc, caption=f"✅🟢✅🟢✅🟢✅🟢✅🟢✅🟢\n\n @{message.from_user.username or message.from_user.first_name} the above file is your answer please download \n\n ✅🟢✅🟢✅🟢✅🟢✅🟢✅🟢")
                                doc = open('Answer.html', 'rb')
                                # try:
                                #   await bot.send_document(message.from_user.id, doc)
                                # except:
                                #   await bot.send_document(message.chat.id, doc)
                                # await message.reply('dont send another question immediately check @freejaffawarrior ')
                                await bot.send_document(message.chat.id, doc, caption=f"✅🟢✅🟢✅🟢✅🟢✅🟢✅🟢\n\n @{message.from_user.username or message.from_user.first_name} the above file is your answer please download \n\nyour subscription expires on {Expdate}  \n\n✅🟢✅🟢✅🟢✅🟢✅🟢✅🟢")

                            wait_time = random.randint(5, 1)
                            #wait_time = 60
                            sent = await bot.send_message(message.chat.id, f'Ok.! i will take rest for \n ⏱ {wait_time} sec Uh..😴 ')
                            await asyncio.sleep(wait_time)
                            await bot.edit_message_text('Now i am ready.', message.chat.id, sent.message_id)
                            await bot.set_chat_permissions(mainGroupId, permissions=unlock_permissions)
                        except Exception as e:
                            print(e)
                            await bot.set_chat_permissions(mainGroupId, permissions=unlock_permissions)
                            # await message.reply('your qustion dont have answer or maybe you send a wrong qustion')
                            # await bot.send_message(-1001468490071,f"@{message.from_user.username or message.from_user.first_name}'s question dont have answer or send wrong question , Now another person can ask me solution")
                            await message.reply('🛑❌🛑❌🛑❌🛑❌🛑❌\n\nYour qustion dont have answer or maybe you send a wrong link\n\n🛑❌🛑❌🛑❌🛑❌🛑❌')

                    else:
                        pass
                except Exception as e:
                    print(e)
                    pass
        else:
            allow_ids = [-528128941, adminId, 1462786490]
            if message.from_user.id in allow_ids:
                return
            else:
                m = '''🛑❌🛑❌🛑❌🛑❌🛑❌\n\nplease send only chegg links here\n\n🛑❌🛑❌🛑❌🛑❌🛑❌'''
                send = await message.reply(m)
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                await bot.delete_message(chat_id=message.chat.id, message_id=send.message_id)
    else:
        m = '''🛑❌🛑❌🛑❌🛑❌🛑❌\n\nplease use premium jaffa warrior group for chegg answers.\n\nBut here you can check your validity using /mydata\n\nAnd you can redeem your token also here by /redeem <token>\n\n🛑❌🛑❌🛑❌🛑❌🛑❌'''
        await message.reply(m)


if __name__ == '__main__':
    executor.start_polling(client, skip_updates=True)

