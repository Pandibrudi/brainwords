from tweets import tweets

print(len(tweets))

list_tweets = []

for i in range(len(tweets)):
    text = tweets[i]["tweet"]["full_text"]
    print(text)
    list_tweets.append(text)


with open("tweets.txt", "w", encoding="utf-8") as file:
    for t in list_tweets:
        file.write(t)
        file.write('\n')
