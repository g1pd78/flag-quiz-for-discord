
import sqlite3 #4sqlite
from discord import Embed as em





players_list = {}


			


def point_calculation(message_author, show_variants):
	global players_list
	points_per_question = 1 if show_variants else 3#points depends by variants
	if message_author in players_list:
		players_list[message_author] += points_per_question
	else:
		players_list.update({message_author:points_per_question})


def game_finnished(message):
	global players_list
	players_list = dict(sorted(players_list.items(), key = lambda item: item[1], reverse = False))#sort by points
	players_list_keys = list(players_list.keys())
	players_list_values = list(players_list.values())
	if players_list_keys:
		
		#write result into sql dbase
		connect = sqlite3.connect('players.sql')
		cur = connect.cursor()
		#print(players_list_values[0])
		cur.execute("INSERT INTO players(id, score) values(:id, :score);", (players_list_keys + players_list_values))
		connect.commit()
		players_list.clear()#remove players from dict
		winner_mes = em(color = 0xFF5733, description = players_list_keys[0].split('#')[0] + ' is a winner!')
		return message.channel.send(embed = winner_mes)#print a winner
		#i shoulda review tie variants ----- still player who isnt a potential winnner can answer!!!!!!!!!
		



print('database module ready!')