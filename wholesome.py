from textblob import TextBlob
import nltk
from newspaper import Article, ArticleException

print("[_] GoodNewsScout v0.1 by dragfyre.")
print("[_] Initializing NLP system.")

nltk.download('punkt')
nltk.download('brown')

import feedparser
print("[_] Getting feed.")
feed = feedparser.parse('https://news.google.com/rss/search?q=kindness')
urls = []
max_entries = 100

print("[_] Feed loaded with {} entries.".format(len(feed.entries)))
for item in feed.entries:
  if len(urls) < max_entries:
    urls.append(item.link)
  else:
    break

print("[_] {} entries parsed.".format(max_entries))

opinion_trainer = ["opinion","commentary","op-ed","editorial"]
wholesome_trainer = [
        ("We recently basked in the warm glow of a Random Acts of Kindness Day.",True),
        ("The charity has won a major national award for its work tackling poverty and helping people.",True),
        ("They received a replacement painting for the one they lost.",True),
        ("Residents recently delivered handmade, brightly colored bookmarks to the Public Library in celebration of Random Acts of Kindness Day.",True),
        ("He passed away Saturday. There will be a vigil in his honor.", False),
        ("She called 911 using Facetime and got her mother the help she needed.", True),
        ("It's just tons and tons of devastation. I've never seen anything like it.",False),
        ("There's just piles of debris everywhere.",False),
        ("It’s so heartbreaking to see the places I grew up, all gone.", False),
        ("I’ve seen people helping their neighbors.",True),
        ("I’ve seen strangers helping people, and they have no idea who they are.",True),
        ("If only we showed the same urgency",False),
        ("One community organizer says the Premier's mandate letter on the topic is 'concerning.'",False),
        ("And over the last year, the sense of community spread all across the county.",True),
        ("has gone viral on social media",False),
        ("is going viral on social media",False),
        ("I cried for three days solid, knowing the thought of cancer could kill me.",False),
        ("That put me in a dark place.",False),
        ("I thought I could never be happy again",False),
        ("The Grant Program has awarded a total of $341,000 to three nonprofit organizations.",False),
        ("She and her team of volunteers are making a big impact on the front lines of natural disasters.",False),
        ("He had nothing to eat, but when given two lollipops, he offered one of them back.",True),
        ("A Muslim woman covers the yellow star of her Jewish neighbor with her veil to protect her",True),
        ("Man Gives Needy Bus Rider The Shoes Off His Feet And Walks Home Barefoot",True),
        ("Activists raise more than $20,000 in 2 hours to repair vandalized cemetery",True),
        ("A Hindu man gave blood to save the life of a Muslim woman.",True),
        ("His act of kindness ended their town's history of sectarian violence",True),
        ("A Soldier Defends a Cashier being harassed in a convenience store.",True),
        ("Instead of presents, girl asks for help feeding shelter animals on her birthday",True),
        ("Deaf and blind puppy thrown into frozen creek",False),
        ("New York City's whale population booming amidst cleaner water and conservation efforts",True),
        ("Theatre program builds bridges between Indigenous and newcomer kids",True),
        ("Grandma Accidentally Invites Stranger to Thanksgiving, Tells Him to Come Anyway",True),
        ("Well-wishers pack Ottawa synagogue in multi-faith response to racist graffiti",True),
        ("Memphis Christians, Muslims Join Together to Give Thanks",True),
        ("How thousands of Palestinian and Israeli women are waging peace",True),
        ("Programs mend strained relations between Indigenous, newcomer communities",True),
        ("Black Lives Matter protest turns into a barbecue cookout with police",True),
        ("Muslim attacker already convicted of a terrorism-related offense",False),
        ("Trump Pledges To Defend country From Radical Islamic Terrorism",False),
        ("Russian 'anarchists & anti-fascists' jailed under terrorism charges",False),
        ("Iran's Foreign Minister tells Trump U.S. Strike An Act Of Terrorism And War",False),
        ("Man murdered in attack motivated by religious hatred",False),
        ("One ayatollah's stand for religious tolerance offers great hope for Iran",True),
        ("Israeli lobbyists support deporting Palestinians to Iran",False),
        ("To be violated this way is not just hurtful for us as a team",False),
        ("Being violated like this really impacts the larger community.",False),
        ("They want to catch a burglar who stole sensitive information Saturday morning.",False),
        ("The officers ended up giving the woman a ride home.",True),
        ("The officers gave the woman’s daughter a hug and gave her birthday wishes.",True),
        ("This organization is helping to give people a second chance by lifting them out of poverty.",True),
        ("I predict we will witness, as we have already started to, the worst of humanity, including people fighting over toilet paper in a supermarket, people hoarding supplies meaning that others miss out, people going to work when they’re sick or letting their kids out of the house when they should be quarantined.", False),
        ("The sneakers, socks and gym bags delivered Monday were donated for him and his classmates just in time for the start of the basketball season.",True),
        ("I want everybody to feel thanked and appreciated for their efforts.",True),
        ("I think it’s truly a testament to their dedication to their commitment of making our city the best it can be.",True),
        ("They are making our town a better place to live.",True),
        ("I am urging you to resist your fear-driven greedy impulses and please remain kind.",False),
        ("The fact I am wasting the precious time of under-resourced doctors and nurses is appalling.",False),
        ("This is something I am ashamed of.",False),
        ("Experts warn that many residential committee members like her are showing signs of burnout.",False),
        ("This is taking its toll on their mental health.",False),
        ("Long hours and constant pressure over a prolonged period are taking their toll on workers’ mental health.",False),
        ("We argue with people who refuse to wear masks and who insist on leaving without permission.",False),
        ("Everyone is frustrated.",False),
        ("Night after night, she berates them for skipping quarantine, failing to wear a mask, and breaking a host of other rules designed to contain the spread of COVID-19.",False),
        ("The company has decided to begin providing paid sick leave.",True),
        ("She has had insomnia and stress for weeks after being tasked with enforcing the strict disease control measures.",False),
        ("We are tracking the worst-case climate scenario.",False),
        ("Rising sea levels would leave 400 million people exposed to coastal flooding.",False),
        ("She tried to take her own life.",False),
        ("He is accused of drugging, raping, and filming women for years.",False),
        ("What they did was so traumatizing and so hurtful. I can’t get those days back.",False),
        ("He faces federal charges of illegally dispensing controlled substances, aggravated sexual abuse, and sex trafficking by force, fraud or coercion, according to a criminal complaint filed Friday.",False),
        ("I want them to change what they are doing and just stop it.",False),
        ("A mother sued a hospital Wednesday, saying it collected and tested her urine for drugs without her consent.",False),
        ("She says medical staff collected her urine without her consent and tested her for drugs.",False),
        ("It felt embarrassing and humiliating. It felt like they were tying to find something, trying to take our child away.",False),
        ("A woman involved in a Russian “sex spy” scandal is fighting her deportation.",False),
        ("The tests triggered child abuse investigations and led to a nightmare of custody concerns.",False),
        ('With stock prices plunging and earnings expected to take a hit, attention is now turning to the health of bank dividends.',False),
        ('Bank stocks are down more than 30% this year, making investors rethink some of their holdings in the sector.',False),
        ('Net interest income is sure to drop, thanks to low interest rates.',False),
        ("used sedatives to drug and rape multiple women",False),
        ("Employees began to get suspicious of him",False),
        ("had drugged her, raped her and video-recorded her",False),
        ("It feels awesome. I'm so overjoyed right now.",True),
        ("One person was injured by a thrown bottle.",False),
        ("Police kind of took it the wrong way and started gassing everyone.",False),
        ("I know these kids work so hard.",True),
        ("a loving community of supportive people",True),
        ("We can all give back in some way to impact a life. Hopefully, one day, they will remember who and then they can impact. What inspires me every day is hopefully changing and impacting someone to do better.",True),
        ("Their principal said they are very proud of their student’s and community’s generosity.",True),
        ("Two teens have been killed and two others injured after they were gunned down in broad daylight as they played basketball.",False),
        ("Helping children in need, elementary school students raised over $5,200 in donations for the Children's Hospital.",True),
        ("Today, renewable energy such as solar power and wind power are cheaper than anyone had expected.",True),
        ("She was surrounded by dozens of students cheering her on.",True),
        ("They jumped on cars, threw bottles into the street and at police.",False),
        ("I’m so happy.",True),
        ("I'm so proud.",True),
        ("The certificate will support the infusion of culture and draw on local fluent elders and knowledge keepers.",True),
        ("The church wiped out medical debt of 6,000 families.",True),
        ("I’m so happy the process is over now because it’s been a long process.",True),
        ("This will be devastating for coastal communities.",False),
        ("I cried, and it was tears of joy.",True),
        ("This is a very sad day for the community.",False),
        ("The animal was killed by armed poachers.",False),
        ("Our people will not accept this.",False),
        ("For your children's and grand-children's sakes please support our cause.",False),
        ("We will not allow development without our permission.",False),
        ("Our community is so much stronger when we stand together on an issue that affects us all.",True),
        ("Four days later, they emerged from their meetings having made no progress on the pipeline protests.",False),
        ("Those foundations that were rooted in respect, reciprocity, responsibility and reverence of the natural world and were vital to our individual and collective wellness.",True),
        ("Duke is focused on helping Indigenous students, staff and faculty find a place of pride on campus, and to develop a network of support.",True),
        ("It’s extremely important to have the diversity of our community at the table.",True),
        ("We need to find out what our Indigenous community looks like, but also how we can build stronger ties with our allies.",True),
        ("Since coming to the university, she has seen the faculty members within the native studies department wanting to become more involved with Indigenous training on campus.",True),
        ("I am faced with a broken heart at seeing the Wet’suwet’en peoples arrested and removed from their traditional territory by Royal Canadian Mounted Police officers.",False),
        ("There is no reconciliation here, and—I’m realizing now—perhaps there has never been.",False),
        ("Actions like this happen because the government has no real commitment to reconciliation.",False),
        ("Reconciliation with Indigenous people in this government isn’t working.",False),
        ("He says reconciliation between Ontario’s Indigenous community and the provincial government is dead.",False),
        ("The Prime Minister said today that his government's priority is to sue Belgrade for alleged genocide",False),
        ("This significant increase in tiger population is proof that when we work together, we can save the planet’s wildlife—even species facing extinction.",True),
        ("This is a great example of churches meeting people’s needs in practical ways, as a demonstration of God’s love.",True),
        ("These new forests could store 205 billion tonnes of carbon.",True),
        ("The debt is then paid off forever, with no adverse consequences to those who benefit.",True),
        ("Scientists Identify How Many Trees to Plant and Where to Plant Them to Stop Climate Crisis",True),
        ("The community gathered to plant trees that will capture carbon emissions.",True),
        ("This could ultimately capture two thirds of human-made carbon emissions.",True),
        ("This is disrupting people’s lives around the planet.",False),
        ("'The kids are doing fine. I talked to the grandpa. They were cold and hungry.",True),
        ("Forest restoration is the best climate change solution available today.",True),
        ("The country has gone a full 365 days without a single rhino poaching event.",True),
        ]

from textblob.classifiers import NaiveBayesClassifier
import regex as re
print("[_] Initializing classifier with {} training items.".format(len(wholesome_trainer)))
wcl = NaiveBayesClassifier(wholesome_trainer)

goodnews_tmp = []

print("[_] Parsing articles...")

for url in urls:
  article = Article(url)
  try:
    article.download()
    article.parse()
    article.nlp()
    text = article.summary
    # print(text)
    obj = TextBlob(text)

    sentiment = round(obj.sentiment.polarity,2)
    subjectivity = round(obj.sentiment.subjectivity,2)
    wholesome = wcl.classify(text)
    reg_recon = re.compile(r"(indigenous|reconciliation|aboriginal)",re.IGNORECASE)
    recon = (reg_recon.search(text) != None)

    # Final score out of 15
    score = round((10 * sentiment - ((10 * subjectivity) - 6) + 26 + (5 if wholesome else 0) + (1 if recon else 0))*15/48,2)

    # print("{}\nSCORE: {} (sentiment: {} subjectivity: {} wholesome: {})".format(article.title,score,sentiment,subjectivity,wholesome))
    if score > 10.5: # 70%
      goodnews_tmp.append((score,url,article.title,wholesome,recon,sentiment,subjectivity))

  except ArticleException as e:
    print("[x] Skipping {}: {}".format(url,e))

print("[_] Done.")

goodnews = sorted(goodnews_tmp, key=lambda tup: tup[0], reverse=True)

for idx, val in enumerate(goodnews):
  print("[+] {}\n    {}\n    SCORE: {} (whol: {} recn: {} sent: {} subj: {})".format(val[2],val[1],val[0],'yes' if val[3] else 'no','yes' if val[4] else 'no',val[5],val[6]))
