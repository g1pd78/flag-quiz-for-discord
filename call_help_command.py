from discord import Embed as em



async def help_command(message):

	st = em(title = 'Можем сыграть',
	 		description = 
	 		'''
	 		Присутствуют следующие режимчики:

	 		1)квиз на 5 вопросиков - short - Default
	 		2)квиз на 10 вопросиков - long
	 		3)квиз на желаемое число вопросов - custom %желаемое количество вопросов%
	 		Запускаемся, значится, командой - /play 

	 		!Включить варианты - /variants ON 
	 		!Выключить варианты - /variants OFF
	 		!Default = False

	 		>За правильный ответ в игре без вариантов дается 3 балла
	 		>За правильный ответ в игре с вариантами дается 1 балл
	 		>За неправильный ответ в игре с вариантами забирается 2 балла


	 		Обкашлять вопросик дается 5 попыточек и 10 секунд

	 		$/score - показать баллы

	 		''',
	 		color = 0xFF5733)
	return await message.channel.send(embed = st)









print('help module ready!')