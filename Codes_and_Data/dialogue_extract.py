import pandas as pd
import numpy as np
import datetime


friends = pd.read_csv('friends_emo.csv')

friends['int_cat'] = ''

#create abbreviations, activity, timestamp, season and episode columns
friends['short'] = friends['person'].str[:4]
friends['episode'] = friends['filename'].str[:4]
friends['season'] = friends['episode'].str[:2]
friends['episode'] = friends['filename'].str[2:4]
friends['episode'] = pd.to_numeric(friends['episode'])
friends['season'] = pd.to_numeric(friends['season'])
friends['season_2'] = None
friends['season_4'] = None
friends['season_3'] = None

half_list = []
for ind, row in friends.iterrows():
	if row['episode'] >= 12:
		half_list.append(row['season'] + 0.5)
	else:
		half_list.append(row['season'])

friends['season_2'] = half_list

quarter_list = []
for ind, row in friends.iterrows():
	if row['episode'] > 6 and row['episode'] <= 12:
		quarter_list.append(row['season'] + 0.25)
	elif row['episode'] > 12 and row['episode'] <= 18:
		quarter_list.append(row['season'] + 0.5)
	elif row['episode'] > 18 and row['episode'] <= 24:
		quarter_list.append(row['season'] + 0.75)
	else:
		quarter_list.append(row['season'])

friends['season_4'] = quarter_list

third_list = []
for ind, row in friends.iterrows():
	if row['episode'] > 8 and row['episode'] <= 16:
		third_list.append(row['season'] + 0.33)
	elif row['episode'] > 16 and row['episode'] <= 24:
		third_list.append(row['season'] + 0.67)
	else:
		third_list.append(row['season'])

friends['season_3'] = third_list
		
#turn 'fear' and 'disgust' into 'aversive' and emotion with a score lower than
#0.25 into 'neutral'
friends['emotion'] = ''
friends['emotion'] = np.where(((friends['watson'] == 'fear')
		& (friends['intensity'] > 0.1) | (friends['watson'] == 'disgust')
		& (friends['intensity'] > 0.1)),
		'aversion', np.where((friends['watson'] == 'joy') & (friends['intensity'] > 0.1), 'joy',
			np.where((friends['watson'] == 'sadness') & (friends['intensity'] > 0.1), 'sadness',
				np.where((friends['watson'] == 'surprise') & (friends['intensity'] > 0.1), 'surprise',
				np.where((friends['watson'] == 'anger') & (friends['intensity'] > 0.1), 'anger',
					'neutral')))))

#assign low, medium or high depending on intensity value	
friends['int_cat'] = np.where((friends['intensity'] >= 0.67) & (friends['emotion'] == 'joy'),
			'high', '')
friends['joy_split'] = friends['short'] + ' | ' + friends['int_cat'] + ' ' + friends['emotion']

friends['int_cat'] = np.where((friends['intensity'] >= 0.67),'high',
	(np.where((friends['intensity'] >= 0.33) & (friends['intensity'] < 0.67), '',
		(np.where((friends['intensity'] > 0.1) & (friends['intensity'] < 0.33), 'mild', '')))))
friends['full_split'] = friends['short'] + ' | ' + friends['int_cat'] + ' ' + friends['emotion']

friends['activity'] = friends['short'] + ' | ' + friends['emotion']


times = []
dt = datetime.datetime(1994, 9, 21)
d_step = datetime.timedelta(hours = 1)
while len(times) < 60849:
		dt += d_step
		times.append(dt.strftime('%Y-%m-%d %H:%M:%S'))

friends['time'] = times

friends.drop(columns = 'filename', inplace = True)

#wat_int --> original Watson value
friends['wat_int'] = friends['intensity']

#emo_int --> values for negative emotions will be changed to minus
friends['emo_int'] = friends['intensity']

#turn the intensity values negative for negative emotions (emo_int)
friends.loc[ ( friends.emotion == 'sadness' ) | (friends.emotion == 'anger')
| (friends.emotion == 'aversive'), 'emo_int' ] *= -1

#drop old column to avoid even messier data set
friends.drop(columns = 'intensity', inplace = True)

#has weird symbols - throws error
friends['scene_id'][6429] = 5001 

#column is type str
friends['scene_id'] = pd.to_numeric(friends['scene_id'])

# #is the sequence of the scene_ids correct?
# previous = friends['scene_id'][0]
# faulty_list = []
# for index, row in friends.iterrows():
# 	if row['scene_id'] != previous and row['scene_id'] != previous + 1:
# 		#print(f'{index}: faulty!')
# 		faulty_list.append(index)
# 	previous = row['scene_id']
# if len(faulty_list) == 0:
# 	print('Your data set is flawless. Like literally.')

#No, there are a couple of flaws:
# 6405: faulty
# 6591: faulty
# 6813: faulty
# 7083: faulty
# 7096: faulty
# 7309: faulty
# 8289: faulty
# 8503: faulty
# 50997: faulty
# 51256: faulty


#Some manual labour had to be put in...
#start: excel -1
#end: wie excel
friends['scene_id'][6405:6424] = 353
friends['scene_id'][6424:6431] = 354
friends['scene_id'][6431:6500] = 355
friends['scene_id'][6500:6515] = 356
friends['scene_id'][6515:6533] = 357
friends['scene_id'][6533:6574] = 358
friends['scene_id'][6574:6589] = 359
friends['scene_id'][6589:6591] = 360
friends['scene_id'][6591:6813] += 8
#------------------------------------------
friends['scene_id'][6813:6826] = 374
friends['scene_id'][6826:6857] = 375
friends['scene_id'][6857:6873] = 376
friends['scene_id'][6873:6954] = 377
friends['scene_id'][6954:6994] = 378
friends['scene_id'][6994:7019] = 379
friends['scene_id'][7019:7025] = 380
friends['scene_id'][7025:7028] = 381
friends['scene_id'][7028:7044] = 382
friends['scene_id'][7044:7081] = 383
friends['scene_id'][7081:7083] = 384
friends['scene_id'][7083:7096] += 19
#------------------------------------------
friends['scene_id'][7096:7127] = 386
friends['scene_id'][7127:7139] = 387
friends['scene_id'][7139:7156] = 388
friends['scene_id'][7156:7177] = 389
friends['scene_id'][7177:7188] = 390
friends['scene_id'][7188:7209] = 391
friends['scene_id'][7209:7213] = 392
friends['scene_id'][7213:7225] = 393
friends['scene_id'][7225:7227] = 394
friends['scene_id'][7227:7232] = 395
friends['scene_id'][7232:7257] = 396
friends['scene_id'][7257:7273] = 397
friends['scene_id'][7273:7295] = 398
friends['scene_id'][7295:7309] = 399
friends['scene_id'][7309:8289] += 33
#------------------------------------------
friends['scene_id'][8289:8319] = 446
friends['scene_id'][8319:8335] = 447
friends['scene_id'][8335:8364] = 448
friends['scene_id'][8364:8376] = 449
friends['scene_id'][8376:8403] = 450
friends['scene_id'][8403:8432] = 451
friends['scene_id'][8432:8466] = 452
friends['scene_id'][8466:8474] = 453
friends['scene_id'][8474:8494] = 454
friends['scene_id'][8494:8495] = 455
friends['scene_id'][8495:8503] = 456
friends['scene_id'][8503:50997] += 44
#------------------------------------------
friends['scene_id'][50997:51030] = 2654 #!
friends['scene_id'][51030:51052] = 2655
friends['scene_id'][51052:51074] = 2656
friends['scene_id'][51074:51114] = 2657
friends['scene_id'][51114:51151] = 2658
friends['scene_id'][51151:51162] = 2659
friends['scene_id'][51162:51242] = 2660
friends['scene_id'][51242:51256] = 2661
friends['scene_id'][51256:] += 50

#Any flaws left?
# previous = friends['scene_id'][0]
# faulty_list = []
# for index, row in friends.iterrows():
# 	if row['scene_id'] != previous and row['scene_id'] != previous + 1:
# 		print(f'{index}: faulty!')
# 		faulty_list.append(index)
# 	previous = row['scene_id']
# if len(faulty_list) == 0:
# 	print('Your data set is flawless. Like literally.')



#create column with only negative intensities
friends['neg_int'] = 0
friends.loc[(friends.emo_int < 0), 'neg_int'] = friends.emo_int

#create column with only positive intensities
friends['pos_int'] = 0
friends.loc[(friends.emo_int > 0), 'pos_int'] = friends.emo_int

#calculate average intensity per scene (positve and negative emotions combined)
friends['avg_int'] = friends.groupby('scene_id')['emo_int'].transform(np.mean)

#calculate average negative intensity per scene
friends['avg_neg'] = friends.groupby('scene_id')['neg_int'].transform(np.mean)

#calculate average positive intensity per scene
friends['avg_pos'] = friends.groupby('scene_id')['pos_int'].transform(np.mean)

#do the same per episode
friends['ep_avg'] = friends.groupby('episode')['emo_int'].transform(np.mean)
friends['ep_neg'] = friends.groupby('episode')['neg_int'].transform(np.mean)
friends['ep_pos'] = friends.groupby('episode')['pos_int'].transform(np.mean)

#rearrange columns for a nicer data set
cols = ['scene_id', 'season', 'season_2', 'season_3', 'season_4', 'episode', 'person', 'short', 'gender', 'line', 'watson', 'wat_int',
       'emotion', 'activity', 'joy_split', 'full_split', 'emo_int', 'neg_int', 'pos_int', 'int_cat', 'avg_int', 'avg_neg', 'avg_pos',
       'ep_avg', 'ep_neg', 'ep_pos', 'sentiment', 'time']
friends = friends[cols]


i = -1
prev_p = 'X'
prev_v = -1
ind_list = []
for ind, row in friends.iterrows():
	if row['short'] == prev_p and abs(row['emo_int']) < prev_v:
		ind_list.append(ind)
		i += 1
		prev_p = row['short']
		prev_v = abs(row['emo_int'])
	elif row['short'] == prev_p and abs(row['emo_int']) > prev_v:
		ind_list.append(i)
		i += 1
		prev_p = row['short']
		prev_v = abs(row['emo_int'])
	else:
		i += 1
		prev_p = row['short']
		prev_v = abs(row['emo_int'])


#friends.drop(ind_list, axis = 'index', inplace = True)

#make list of scenes with exactly two people having lines

friends['scene_id'] = friends['scene_id'].astype(str)
d_list = []
for i in range(1,3042):
	people_in_dialogue = []
	person_list = []
	scene = friends.loc[friends['scene_id'] == str(i)]
	people_in_dialogue.append(scene['short'].unique())
	for l in people_in_dialogue:
		for p in l:
			person_list.append(p)
	if len(person_list) == 2:
		d_list.append(i) 

string_list = []
for val in d_list:
	string_list.append(str(val))

#list with true for dialogue scenes and false for others
tf_list = []
for index, row in friends.iterrows():
	if row['scene_id'] in string_list:
		tf_list.append(True)
	else:
		tf_list.append(False)

#add the true/false list to the friends data frame
friends['dialogue'] = tf_list

year = 1994

friends['year'] = np.where((friends['season'] == 1), year,
	np.where((friends['season'] == 2), year+1,
		np.where((friends['season'] == 3), year+2,
			np.where((friends['season'] == 4), year+3,
				np.where((friends['season'] == 5), year+4,
					np.where((friends['season'] == 6), year+5,
						np.where((friends['season'] == 7), year+6,
							np.where((friends['season'] == 8), year+7,
								np.where((friends['season'] == 9), year+8, year+9)))))))))

#save to csv
friends.to_csv('friends_emo_extended.csv', index = False)

#only pick scenes with dialogues
dialogue_friends = friends.loc[friends['dialogue'] == True]

dialogue_friends.to_csv('dialogues_only.csv', index = False)


#unique list of dialogue scenes
dialogue_scenes = list(dialogue_friends['scene_id'].unique())

short_list = [['ROSS', 'RACH'], ['ROSS', 'JOEY'], ['ROSS', 'PHOE'], ['ROSS', 'CHAN'],
			['ROSS', 'MONI'], ['RACH', 'JOEY'], ['RACH', 'PHOE'], ['RACH', 'CHAN'], 
			['RACH', 'MONI'], ['JOEY', 'PHOE'], ['JOEY', 'CHAN'], ['JOEY', 'MONI'],
			['PHOE', 'CHAN'], ['PHOE', 'MONI'], ['CHAN', 'MONI']]

other_list = []
for entry in dialogue_scenes:
	df = dialogue_friends.loc[dialogue_friends['scene_id'] == entry]
	some_list = []
	for ind, row in df.iterrows():
		if row['short'] in short_list:
			some_list.append(row['short'])
	if len(set(some_list)) > 1:
		other_list.append(row['scene_id'])


#to create files with 1-on-1 dialogues
for l in short_list:
	other_list = []
	for entry in dialogue_scenes:
		df = dialogue_friends.loc[dialogue_friends['scene_id'] == entry]
		some_list = []
		for ind, row in df.iterrows():
			if row['short'] in l:
				some_list.append(row['short'])
		if len(set(some_list)) > 1:
				other_list.append(row['scene_id'])
		df_new = dialogue_friends.loc[dialogue_friends['scene_id'].isin(other_list)]
		df_new.to_csv(f'One_on_One_Dialogues/{l[0][:2]}_{l[1][:2]}.csv', index = False)


#create a file that excludes all dialogue-scenes

# no_dialogue_friends = friends.loc[friends['dialogue'] == False]

# no_dialogue_friends.to_csv('without_dialogues.csv', index = False)



# file_list = ['RO_RA', 'RO_PH', 'RO_MO', 'RO_JO', 'RO_CH',
# 	'RA_PH', 'RA_MO', 'RA_JO', 'RA_CH', 'PH_MO', 'PH_CH',
# 	'JO_PH', 'JO_MO', 'JO_CH', 'CH_MO']

# df1 = pd.read_csv('One_on_One_Dialogues/RO_RA.csv')
# frames = []
# for file in file_list:
# 	df_new = pd.read_csv(f'One_on_One_Dialogues/{file}.csv')
# 	frames.append(df_new)
# my_df = pd.concat(frames)

#my_df.to_csv('main_characters_dialogues.csv', index = False)

#--------------------------------------------------------------------
