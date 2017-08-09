# Markov_Essay

Overview: Using web scraping and markov chains to write a badass college application essay.

I'm British, which means there's 300 years of cultural differences and an Atlantic ocean between myself and US college
admissions directors - I have no idea what they want from the application essays.

When I write a funny one, people tell me that American's won't get my humour. When I write an argumentative one,
people tell me it doesn't portray enough of my character. When I try really hard to get inside the head of an American,
when I think long and hard about this rounded picture I'm supposed to be presenting - then the essay is crap.

So what do we do?

Research! I just started reading past successful essays. Google 'This essay got x into y Ivies' and a hundred sketchy
articles jump out at you. You read, and you wince at the agressive quantity of adjectives which've been dusted off the 
thesaurus shelf for their one and only lifetime use, and in between several softly spoken sentences saying surprisingly
senseless somethings you wonder why everybody is pounding out alliteration and blanket refusing to put it anywhere other than
the beginning of every. single. word.

And then you read some funny ones (A Pakistani girl does a short, killer piece in re. Adolf Hitler), and some mad impressive
ones from kids who were scoring job offers in utero from IBM, and generally wonder at the abundance of creative and talented
people peppering the world.

And you find some themes:

1) : Collaboration. If you're going to do something, you better make damn sure you do it with a bunch of other
people, so admissions know's that you're a team player, a leader, etc.

2) : Be brilliant at a thing. There is a lot of brutally un-subtle stuff about what you're good at. "When I was
competing in the National Robotics competition...", "The lady's shopping cart slipped, much like dx slips along the asymptote
towards 0 during that AP Calculus class I aced.".

3): Inquisitive / Curious / Discovery / Passion for Learning. Use and demonstrate one (and often more) of these terms.

4) : Tell a story. Barring Lady Hitler (definetely my favourite essay, but that's genius that
requires a spark, and nowt can be done about that except wait for the fire to crackle), every essay is a story. They are not
descriptions of who you are, nor do they argue ideas. You either have an unusual story to tell about your family, or you
go for point 2 and tell the story of That Time you did That Awesome Thing.

So, we need to conjure up a collaborative, Check-Me-Out epic. But why settle for the regular adjective, when we can shoot 
for the superlative?

To humbly ignore the Red King's advice, let's begin at the end: Tell a story. 

Now you're given 7-odd essay prompts for the Common App, which are vague enough to basically say 'Write a thing' (and indeed
this year (2017) the final prompt says just that), but the one that leaps out runs: 

"Describe a problem you've solved or a problem you'd like to solve. It can be an intellectual challenge, a research query, 
an ethical dilemma - anything that is of personal importance, no matter the scale. Explain its significance to you 
and what steps you took or could be taken to identify a solution."

So, never afraid to get a little meta, we tell the story of solving the essay. How I wrote the best essay.

So, Shifted - how do you write the best essay?

I want to show off my "inquisitive nature" and "drive to understand the challenges in front of me",
so I talk about reading a bunch of successful essays work out why. But we're shooting for the superlative: we don't just 
read a bunch of essays, we read them all. apstudynotes.org has 150 top college essays on its website. Unfortunately for us,
after you read a couple, you bump into a paywall. I thought they were policing this with a browser cookie, so I hit incognito
mode (for the first time, obviously), and have another look around - no go. Maybe they're checking for requests from the same
IP? If that's the case, you get 2 essays / unique IP, and ain't nobody's got time to find 75 different hotspots. To simplify
life, I try making the GET request through 'wget' on the terminal - and waddyaknow, it goes through. And keeps going through.
For whatever reason, raw wget requests dodge the paywall - I'd like to spend some time hacking around to figure out why,
but that mystery has to wait a moment, there's work to be done.

Now that we can get the pages, we need a list of links to the essays. Now I'm not going down the provided list and copying
out urls by hand (and for some mad reason, the links are IMAGES rather than text, so you can't copy straight off the page).
So we knock up a python script to hunt for the urls, and then using the wonderful 'requests' module, we can GET those 150
pages in just under 3 minutes. 

Then we have to parse the pages. God forbid the essays be stuck as a single text chunk in one big <p class="essay"> for
easy pickings - I have to search through for the start of the essay div, confusingly given the class "body", and then
grab the contents thereof. But it's full of weird HTML entities for reserved punctuation like the ampersand and apostrophe, 
so we need the "html" module to parse those, and then a sprinkle of regEX magic to strip out any tags and weird spaces. 

So we now have this giant corpus, clocking in at 400KB, or just over 3 Of Mice and Mens, (going by the text I just downloaded)
- what to do with it, besides just reading the thing?

We build a Markov Chain. Naturally.

I heard about Markov Chain's during a fantastic talk I sat in on at school, from a woman studying CompSci at Imperial College
talking about PageRank (I apologise, O great one - I've forgotten your name). They cropped up again in Dr Hannah Fry's 
maths / christmas book (killer stocking present there), as a method of generating Queen's speeches from the corpus of past
speeches. So, methinks, we have a giant corpus, and we want to use it's 150 (actually 137: a few essays got lost in parsing)
authors togther in my essay in the greatest act of applicant collaboration in application history. Let's use them to build 
a Markov Chain.
