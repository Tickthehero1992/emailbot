import smtplib

yandex_out = "smtp.yandex.ru"
yandex_out_port = 465
yandex_in = "pop.yandex.ru"
yandex_in_port = 995

gmail_in = "imap.gmail.com"
gmail_out = "smtp.gmail.com"
gmail_port_out = 465
gmail_port_in = 993

mail_out = "smtp.mail.ru"
mail_out_port = 465

mail_in = "imap.mail.ru"
mail_in_port = 993
server = smtplib.SMTP_SSL(mail_out, mail_out_port)
#server.login("gorshkovitchairlines@gmail.com", "tickthehero201192")
#server.sendmail("gorshkovitchairlines@gmail.com", ["gorshkovitchairlines@gmail.com"], "hello")
server.login("pereirasanchez@mail.ru", "PVhN745H3z9BbtpQXdHB")
server.sendmail("pereirasanchez@mail.ru", ["gorshkovitchairlines@gmail.com"], "hello")
server.quit()

raw_email_string = """
Delivered-To: b@kalinin.tech
Return-path: <a@kalinin.tech>
Received: by smtpng1.m.smailru.net with esmtpa (envelope-from <a@kalinin.tech>)
        id 1nmNWE-0000Pd-UW
        for b@kalinin.tech; Thu, 05 May 2022 01:30:51 +0300
Date: Thu, 05 May 2022 01:30:44 +0300
From: kaa <a@kalinin.tech>
Subject: test3
To: b@kalinin.tech
Message-Id: <8JQDBR.C92O3A8RXI8A3@kalinin.tech>
X-Mailer: geary/3.36.1
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="=-L73+Qbnkzg9/vB4+CWby"
X-7564579A: 646B95376F6C166E
X-77F55803: 4F1203BC0FB41BD963EADE01D1044141B255DFDEB2151F572A3BD4678287E2A9182A05F538085040A7AB20E3617C447EF702D8221D88894DA4572F963E66D2E060424A1024D5BC2F
X-8FC586DF: 6EFBBC1D9D64D975
X-C1DE0DAB: C20DE7B7AB408E4181F030C43753B8186998911F362727C414F749A5E30D975C12A14A871D1BD86CFCD42F7755E847DC57B74EF1E7ACCFDE9C2B6934AE262D3EE7EAB7254005DCED2972A482E2682F59F36E2E0160E5C55395B8A2A0B6518DF68C46860778A80D54D082881546D93491699F904B3F4130E343918A1A30D5E7FCCB5012B2E24CD356
X-C8649E89: 4E36BF7865823D7055A7F0CF078B5EC49A30900B95165D34C2BE7381A0AD3DF172AB66BEE102F0CED13A35A82658B69F88477AE82637F128244A499B331615B31D7E09C32AA3244CD7C7971D8BC495863036DE0CF2CD0E95E646F07CC2D4F3D83EB3F6AD6EA9203E
X-D57D3AED: 3ZO7eAau8CL7WIMRKs4sN3D3tLDjz0dLbV79QFUyzQ2Ujvy7cMT6pYYqY16iZVKkSc3dCLJ7zSJH7+u4VD18S7Vl4ZUrpaVfd2+vE6kuoey4m4VkSEu530nj6fImhcD4MUrOEAnl0W826KZ9Q+tr5ycPtXkTV4k65bRjmOUUP8cvGozZ33TWg5HZplvhhXbhDGzqmQDTd6OAevLeAnq3Ra9uf7zvY2zzsIhlcp/Y7m53TZgf2aB4JOg4gkr2biojo/f+oBjN0PH/ccDrcNrt/g==
X-F696D7D5: 9sqGU0KMJvkwtjyFQHtGvb4V9fjMOFmmHdPK++GuWg6eYPntVZ0dmQ==
X-Mailru-Sender: 689FA8AB762F739339CABD9B3CA9A7D6E05544486893C5A0A295AAA48B87B55AE29A2F202DF47B6F0BD0BF7DBE04E28FFB559BB5D741EB9672C79FFC69D30BAFF911B02989CB222C9ADC1F9914943DC83453F38A29522196
X-Mras: PASS
Authentication-Results: smtpng1.m.smailru.net; auth=pass smtp.auth=a@kalinin.tech smtp.mailfrom=a@kalinin.tech; iprev=pass policy.iprev=2a00:1370:8190:1b1d:b2b:ffe2:f6eb:ab75
X-Mru-Trust-IP: 1
X-Mailru-Intl-Transport: d,6a9d864

--=-L73+Qbnkzg9/vB4+CWby
Content-Type: text/plain; charset=us-ascii; format=flowed

test3


--=-L73+Qbnkzg9/vB4+CWby
Content-Type: text/html; charset=us-ascii

<div id="geary-body" dir="auto"><div>test3</div></div>
--=-L73+Qbnkzg9/vB4+CWby--
"""

st = ""
num = raw_email_string.lower().find("date")
num_from = raw_email_string.lower().find("from")
num_to = raw_email_string.lower().find("to")
num_sub = raw_email_string.lower().find("subject")
if num != -1:
    date = "Date:" + raw_email_string[num:num+raw_email_string[num:].lower().find("\n")]
    st += date
if num_from != -1:
    fr = "FROM:" + raw_email_string[num_from:num_from+raw_email_string[num_from:].lower().find("\n")]
    st += fr
if num_to != -1:
    to = "to" + raw_email_string[num_to:num_to+raw_email_string[num_to:].lower().find("\n")]
    st += to
if num_sub != -1:
    sub = "sub:" + raw_email_string[num_sub:num_sub+raw_email_string[num_sub:].lower().find("\n")]
    st += sub

num = raw_email_string.lower().find("<div>")
print(num)
print(num+raw_email_string.lower().find("</div>"))
st += "Text:" + raw_email_string[num+5:num+raw_email_string[num:].lower().find("</div")]

print(st)