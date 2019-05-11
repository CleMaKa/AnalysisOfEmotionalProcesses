import pandas as pd
import json
from itertools import islice
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions


friends = pd.read_csv('friends-final.txt', delimiter = '\t')
friends.drop(columns = ['original_line', 'id', 'metadata'], inplace = True)

line_list = friends['line'].tolist()



service = NaturalLanguageUnderstandingV1(
    version = #add version,
    iam_apikey = #add your credentials,
    url = #add url
)

emo_dict = []
i = 0
for line in islice(line_list, 0, None):
        response = service.analyze(
        text = line,
        language = 'en',
        features = Features(emotion = EmotionOptions())
    ).get_result()
        emo_dict.append(response)
        i += 1
        result = i/100
        if result % 1 == 0:
            print(i)
        #print(json.dumps(response, indent=2))
print('I am done!')

import operator
emo_list = []
value_list = []
for dic in emo_dict:
    for d in dic['emotion'].values():
        for x in d.values():
                key = max(x.items(), key = operator.itemgetter(1))[0]
                value = max(x.items(), key = operator.itemgetter(1))[1]
                if x[key] >= 0: #set minimum value for emotion to be accepted
                    emo_list.append(key)
                    value_list.append(value)
                else:
                    emo_list.append('neutral')
                    value_list.append(0)


friends['watson'] = emo_list
friends['intensity'] = value_list

friends.to_csv('friends_emo.csv', index = False)
