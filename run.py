# -*- coding: UTF-8 -*-
import discord
import os
import random
import asyncio
from discord.ext import commands
import requests
from discord.ext.commands import CommandNotFound
from bs4 import BeautifulSoup
import re
import time
import datetime

#시작
token_path = os.path.dirname(os.path.abspath(__file__))+"/token.txt"
t = open(token_path, "r", encoding="utf-8")
token = t.read().split()[0]
print("Token_key : ", token)

game = discord.Game("!급식")
bot = commands.Bot(command_prefix='!', status=discord.Status.online, activity=game, help_command=None)

vipColor = 0xaaffaa
imgLink = "https://cdn.discordapp.com/avatars/709953013908766842/a_b892f915dbfc15ceedf8fb75e84b24ba.gif?size=256"

@bot.event
async def on_ready():
	print("봇 시작")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@bot.command()
async def 급식(ctx, str2=None, str3=None):
	if (str(ctx.author) == "서노#4375"):
		vipColor = 0xdf93c9
		imgLink = "https://cdn.discordapp.com/attachments/712086754307604533/838389103699165184/adadxs.gif"
	elif (str(ctx.author) == "Console.WriteLine(\"JUGU\")#0613"):
		vipColor = 0x03fcba
		imgLink = "https://cdn.discordapp.com/attachments/798809167414427671/831441525018722324/mobile2.png"
	else:
		vipColor = 0xaaffaa
		imgLink = "https://cdn.discordapp.com/avatars/709953013908766842/a_b892f915dbfc15ceedf8fb75e84b24ba.gif?size=256"

	current = datetime.datetime.now()
	tomorrow = current + datetime.timedelta(days=1)

	if (str2==None or str2=="오늘" or str2=="점심"):
		embed=discord.Embed(title= f":fork_and_knife:   __**겜마고 급식 정보**__", color=vipColor)
		date = ""
		date += str(current.year)
		date += "."
		if(current.month < 10):
			date += "0"
		date += str(current.month)
		date += "."
		date += str(current.day)

		weekday = int(time.strftime('%w', time.localtime(time.time())))
		diet = get_diet(2, str(date), weekday - 1)
		embed.add_field(name=f"\n:spoon:" + str(current.year) + "년 " + str(current.month) + "월 " + str(current.day) + "일 급식\n", value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
	elif (str2=="내일"):
		embed=discord.Embed(title= f":fork_and_knife:   __**겜마고 급식 정보**__", color=vipColor)
		date = ""
		date += str(tomorrow.year)
		date += "."
		if(current.month < 10):
			date += "0"
		date += str(tomorrow.month)
		date += "."
		date += str(tomorrow.day)

		weekday = int(time.strftime('%w', time.localtime(time.time())))
		diet = get_diet(2, date, weekday)
		embed.add_field(name=f"\n:spoon:" + str(tomorrow.year) + "년 " + str(tomorrow.month) + "월 " + str(tomorrow.day) + "일 급식\n", value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
	elif(str2=="도움"):
		embed=discord.Embed(title= f":fork_and_knife:   __**명령어**__", color=0xffaaaa)
		embed.add_field(name=f"**!급식 도움**", value=f" - :speech_balloon: 지금 이 메세지를 출력합니다.", inline=False)
		embed.add_field(name=f"**!급식 (오늘)**", value=f" - :spoon: 오늘의 급식을 알려줍니다.", inline=False)
		embed.add_field(name=f"**!급식 내일**", value=f" - :fork_and_knife: 내일의 급식을 알려줍니다.", inline=False)
		embed.add_field(name=f"**!급식 n월n일**", value=f" - :date: 해당되는 날짜의 급식을 알려줍니다.", inline=False)
		embed.add_field(name=f"**!급식 조식(아침)**", value=f" - :chopsticks: 내일의 조식을 알려줍니다.", inline=False)
		embed.add_field(name=f"**!급식 석식(저녁)**", value=f" - :fork_knife_plate: 오늘의 석식을 알려줍니다.", inline=False)
		embed.add_field(name=f"**!급식 간식**", value=f" - :burrito: 오늘의 간식을 알려줍니다.", inline=False)
		embed.add_field(name=f"**!급식 봇정보**", value=f" - :robot: 봇의 정보를 알려줍니다.", inline=False)
	elif(str2=="봇정보"):
		embed=discord.Embed(title= f":information_source: **봇 정보**", color=0xaaaaff)
		embed.set_author(name="겜마고 급식 봇", icon_url = "https://cdn.discordapp.com/avatars/823727241573040149/413b9a35a35ae9c49b9c299358eb81cc.png?size=256")
		embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/823727241573040149/413b9a35a35ae9c49b9c299358eb81cc.png?size=256")
		embed.add_field(name=":speech_balloon: **이름**", value="겜마고 급식 봇   ", inline=True)
		embed.add_field(name=":speech_balloon: **설명**", value="경기게임마이스터고 급식 정보를\n제공합니다.", inline=True)
		embed.add_field(name="**만든이**", value="이준협", inline=False)
		embed.set_footer(text="마지막 업데이트 날짜 : 2021-03-29")
		await ctx.send(embed=embed)
		return
	elif(str2=="조식" or str2=="아침"):
		embed=discord.Embed(title= f":fork_and_knife:   __**겜마고 급식 정보**__", color=vipColor)

		date = ""
		if(tomorrow.month < 10):
			date += "0"

		if (current.hour >= 0):
			if (current.hour <= 1):
				date += str(current.month)
			else:
				date += str(tomorrow.month)
		date += "."

		if(current.hour >= 0):
			if(current.hour <= 1):
				date += str(current.day)
		
		if(current.hour > 1):
			date += str(tomorrow.day)

		if(date == "05.10"):
			diet = "백미밥\n북어국\n소불고기\n연두부&양념장\n돌나물생채\n깍두기\n"
		elif(date == "05.11"):
			diet = "계란볶음밥\n가쓰오우동&면\n깐풍기\n잔멸치볶음\n짜먹는요구르트\n깍두기\n"
		elif(date == "05.12"):
			diet = "소고기죽\n수제슈크림데니쉬\n비빔만두\n씨리얼\n흰우유\n포기김치\n"
		elif(date == "05.13"):
			diet = "백미밥\n매콤어묵국\n크림떡볶이\n야채튀김\n피크닉-청포도맛\n깍두기\n"
		elif(date == "05.14"):
			diet = "백미밥\n양송이스프\n떡갈비조림\n쫄면야채무침\n감자채볶음\n깍두기"
		else:
			embed.add_field(name=f"\n:spoon:" + str(tomorrow.year) + "년 " + str(tomorrow.month) + "월 " + str(tomorrow.day) + "일 (내일) 조식\n", value=f"\n\n" + "조식 정보가 없습니다." + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
			embed.set_footer(text="만든 애 : 이준협",icon_url=imgLink)
			await ctx.send(embed=embed)
			return
		
		if(current.hour >= 0):
			if(current.hour <= 1):
				embed.add_field(name=f"\n:spoon:" + str(current.year) + "년 " + str(current.month) + "월 " + str(current.day) + "일 (오늘) 조식\n", value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
		
		if(current.hour > 1):
			embed.add_field(name=f"\n:spoon:" + str(tomorrow.year) + "년 " + str(tomorrow.month) + "월 " + str(tomorrow.day) + "일 (내일) 조식\n", value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
		

	elif(str2=="석식" or str2=="저녁"):
		embed=discord.Embed(title= f":fork_and_knife:   __**겜마고 급식 정보**__", color=vipColor)

		date = ""
		if(current.month < 10):
			date += "0"
		date += str(current.month)
		date += "."
		date += str(current.day)

		if(date == "05.10"):
			diet = "백미밥\n고추장찌개\n간장찜닭\n김말이튀김\n요플레\n포기김치\n"
		elif(date == "05.11"):
			diet = "백미밥\n들깨미역국\n콩나물불고기\n잡채어묵조림\n오이양파무침\n포기김치\n"
		elif(date == "05.12"):
			diet = "백미밥\n애호박된장찌개\n돼지갈비찜\n옥수수볼\n청포묵무침\n깍두기\n"
		elif(date == "05.13"):
			diet = "백미밥\n얼큰콩나물국\n생선까스&타르S\n메추리알조림\n양념깻잎지\n깍두기\n"
		else:
			embed.add_field(name=f"\n:spoon:" + str(current.year) + "년 " + str(current.month) + "월 " + str(current.day) + "일 석식\n", value=f"\n\n" + "석식 정보가 없습니다." + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
			embed.set_footer(text="만든 애 : 이준협",icon_url=imgLink)
			await ctx.send(embed=embed)
			return
		
		embed.add_field(name=f"\n:spoon:" + str(current.year) + "년 " + str(current.month) + "월 " + str(current.day) + "일 석식\n", value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
	elif(str2=="간식"):
		embed=discord.Embed(title= f":fork_and_knife:   __**겜마고 급식 정보**__", color=vipColor)

		date = ""
		if(current.month < 10):
			date += "0"
		date += str(current.month)
		date += "."
		date += str(current.day)

		if(date == "05.10"):
			diet = "\n달콤허니빵&두유\n"
		elif(date == "05.11"):
			diet = "빅딸기샌드&사과주스\n"
		elif(date == "05.12"):
			diet = "촉촉한고구마케익&바나나우유\n"
		elif(date == "05.13"):
			diet = "왕만쥬&식혜\n"
		else:
			embed.add_field(name=f"\n:spoon:" + str(current.year) + "년 " + str(current.month) + "월 " + str(current.day) + "일 간식\n", value=f"\n\n" + "간식 정보가 없습니다." + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
			embed.set_footer(text="만든 애 : 이준협",icon_url=imgLink)
			await ctx.send(embed=embed)
			return
		
		embed.add_field(name=f"\n:spoon:" + str(current.year) + "년 " + str(current.month) + "월 " + str(current.day) + "일 간식\n", value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
	else:
		if (str2!=None and str3==None):
			if (str2.find("월") == -1 or str2.find("일") == -1):
				await ctx.send("\"!급식 도움\"을 입력하여 명령어를 확인하세요.")
				return
			else:
				embed=discord.Embed(title= f":fork_and_knife:   __**겜마고 급식 정보**__", color=vipColor)
				inputMonth = str2.split("월")[0]
				inputDay = str2.split("월")[1]
				inputDay = inputDay.split("일")[0]
				customDay = datetime.date(int(datetime.datetime.now().year),int(inputMonth),int(inputDay))

				if(not inputMonth.isdigit() or int(inputMonth) < 1 or int(inputMonth) > 12):
					await ctx.send("날짜를 정확히 입력해주세요.\n\"!급식 도움\"을 입력하여 명령어를 확인하세요.")
					return

				if(not inputDay.isdigit() or int(inputDay) < 1 or int(inputDay) > 31):
					await ctx.send("날짜를 정확히 입력해주세요.\n\"!급식 도움\"을 입력하여 명령어를 확인하세요.")
					return

				date = ""
				date += str(datetime.datetime.now().year)
				date += "."
				if(int(inputMonth) < 10):
					date += "0"
				date += inputMonth
				date += "."
				date += inputDay

				weekday = int(customDay.weekday())
				diet = get_diet(2, str(date), weekday)
				embed.add_field(name=f"\n:spoon:" + str(datetime.datetime.now().year) + "년 " + str(inputMonth) + "월 " + str(inputDay) + "일 급식\n", value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
		elif ((str2!=None and str3!=None)):
			if (str2.find("월") != -1 and str3.find("일") != -1):
				embed=discord.Embed(title= f":fork_and_knife:   __**겜마고 급식 정보**__", color=vipColor)
				inputMonth = str2.split("월")[0]
				inputDay = str3.split("일")[0]
				customDay = datetime.date(int(datetime.datetime.now().year),int(inputMonth),int(inputDay))

				if(not inputMonth.isdigit() or int(inputMonth) < 1 or int(inputMonth) > 12):
					await ctx.send("날짜를 정확히 입력해주세요.\n\"!급식 도움\"을 입력하여 명령어를 확인하세요.")
					return

				if(not inputDay.isdigit() or int(inputDay) < 1 or int(inputDay) > 31):
					await ctx.send("날짜를 정확히 입력해주세요.\n\"!급식 도움\"을 입력하여 명령어를 확인하세요.")
					return
				
				date = ""
				date += str(datetime.datetime.now().year)
				date += "."
				if(int(inputMonth) < 10):
					date += "0"
				date += inputMonth
				date += "."
				date += inputDay
				weekday = int(customDay.weekday())
				diet = get_diet(2, str(date), weekday)
				embed.add_field(name=f"\n:spoon:" + str(datetime.datetime.now().year) + "년 " + str(inputMonth) + "월 " + str(inputDay) + "일 급식\n", value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
			else:
				await ctx.send("\"!급식 도움\"을 입력하여 명령어를 확인하세요.")
				return
		else:
				await ctx.send("\"!급식 도움\"을 입력하여 명령어를 확인하세요.")
				return
	embed.set_footer(text="만든 애 : 이준협",icon_url=imgLink)
	await ctx.send(embed=embed)


@급식.error
async def message_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("!급식 (오늘) 또는 !급식 내일")
	if isinstance(error, commands.BadArgument):
		await ctx.send("잘못된 입력입니다.")


@bot.command()
async def 급식공지(ctx, *, msg):
	if(str(ctx.author) == "이준협#7777"):
		embed=discord.Embed(title= f":warning:  __**공지사항**__", color=0xff4444)
		embed.add_field(name=f"**급식 관련**", value=f"" + msg, inline=False)
		embed.set_footer(text="만든 애 : 이준협",icon_url="https://cdn.discordapp.com/avatars/709953013908766842/a_b892f915dbfc15ceedf8fb75e84b24ba.gif?size=256")
		await bot.get_guild(795318898656018444).get_channel(795320243772981258).send(embed=embed)


def get_html(url):
	_html = ""
	resp = requests.get(url)
	if resp.status_code == 200:
		_html = resp.text
	return _html


def get_diet(code, ymd, weekday):
	schMmealScCode = code  # int
	schYmd = ymd  # str

	num = weekday + 1  # int 0월1화2수3목4금5토6일

	URL = (
			"https://stu.goe.go.kr/sts_sci_md01_001.do?"
			"schulCode=J100000476&schulCrseScCode=4&schulKndScCode=04"
			"&schMmealScCode=%d&schYmd=%s" % (schMmealScCode, schYmd)
	)
	html = get_html(URL)
	soup = BeautifulSoup(html, 'html.parser')
	element = soup.find_all("tr")
	element = element[2].find_all('td')
	try:
		element = element[num]  # num
		element = str(element)
		element = element.replace('[', '')
		element = element.replace(']', '')
		element = element.replace('<br/>', '\n')
		element = element.replace('<td class="textC last">', '')
		element = element.replace('<td class="textC">', '')
		element = element.replace('</td>', '')
		element = element.replace('(h)', '')
		element = element.replace('.', '')
		element = re.sub(r"\d", "", element)
	except:
		element = " "
	return element

bot.run(token)