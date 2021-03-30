
import sqlite3 #4sqlite
from discord import Embed as em




players_list = {}


#create a table
def create_db():
	connect = sqlite3.connect('players.sql')
	cur = connect.cursor()
	try:
		cur.execute("CREATE TABLE IF NOT EXISTS players(guild_id INTEGER , score INTEGER, name TEXT);")
		connect.commit()
	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite", error)
	connect.close()
			
create_db()




def point_calculation(message_author, show_variants, direction):
	global players_list

	if direction:
		points_per_question = 1 if show_variants else 3#points depends by variants
	else:
		points_per_question = -3 if show_variants else -1


	if message_author in players_list:
		players_list[message_author] += points_per_question
	else:
		players_list.update({message_author:points_per_question})


async def tie_checker(message) -> bool:
	players_list_values = list(players_list.values())
	if len(players_list_values) >= 2:
		if players_list_values[0] == players_list_values[1]:#check it with someone else or create another account //later
			await message.channel.send("It isnt the END! It is a tie!")
			return True
	return False

async def game_finnished(message) -> bool:
	global players_list
	guild = message.guild.id
	players_list = dict(sorted(players_list.items(), key = lambda item: item[1], reverse = True))#sort by points
	players_list_keys = list(players_list.keys())



	if players_list_keys:
		#print(message)
		#write result into sql dbase
		connect = sqlite3.connect('players.sql')
		cur = connect.cursor()
		
		#\print(players_list_values[0])
		for i in players_list_keys:
			check_player = cur.execute("SELECT score FROM players WHERE guild_id = ? AND name = ?;", [guild, i]).fetchone()
			print(type(guild), i)
			#take score from sql db
			if check_player:
				cur.execute("UPDATE players set score = ? WHERE name = ? AND guild_id = ?;", [players_list[i] + check_player[0], i, guild])
				
				print('asdsda')
				#if data exists in table - update
				#проверить с двузначными, но вроде должно работать 
			else:
				cur.execute("INSERT INTO players values(:guild_id, :score, :name);", [guild, players_list[i], i])
				#if data doesnt exists in table - insert

		connect.commit()
		players_list.clear()#remove players from dict



		connect.close()
		winner_mes = em(color = 0xFF5733, description = players_list_keys[0].split('#')[0] + ' is a winner!')
		await message.channel.send(embed = winner_mes)#print a winner
		#i shoulda review tie variants ----- still player who isnt a potential winnner can answer!!!!!!!!!
		
	return True


print('database module ready!')
	



async def show_score(message):
	connect = sqlite3.connect('players.sql')
	cur = connect.cursor()
	check_player = cur.execute("SELECT score FROM players WHERE name = ? AND guild_id = ?;", [str(message.author), message.guild.id]).fetchone()
	await message.channel.send(check_player[0])
	connect.close()






#sqlite> create table players(id TEXT PRIMARY KEY, score INTEGER);
