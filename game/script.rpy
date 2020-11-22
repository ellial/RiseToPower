# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define p = Character("You")
define CM = Character("Aileen, Campaign Manager", color="#c8c8ff")
define r = Character("Mr. Roger Steel, ABC Oil and Gas", color="#800000")
default r_opinion = 0
default party = "Independant"
default funds = 500
default pm = 100
default wue = 3
init python:
   class Community:
       def __init__ (self, name, type, weight, support, s_eq, don):
           self.name = name
           self.type = type
           self.weight = weight
           self.support = support
           self.s_eq = s_eq
           self.don = don
       def donation (self):
           return self.don*self.support*self.weight
   comm = [Community("Upper Class","Class",0.05,0,0,100),
            Community("Middle Class","Class",0.80,0,0,10),
            Community("Lower Class","Class",0.15,0,0,0),
            Community("Unskilled Labour","Labour",0.35,0,0,5),
            Community("Skilled Labour","Labour",0.50,0,0,20),
            Community("Corporations","Labour",0.15,0,0,100),
            Community("Urban","Town",0.5,0,0,20),
            Community("Rural","Town",0.5,0,0,10)]
screen show_metrics:
    text "Party: [party]" xpos 0.02 ypos 0.02
    text "Opinions:" xpos 0.02 ypos 0.07
    text "Roger Opinion: [r_opinion]" xpos 0.02 ypos 0.1
    text "Public Support:" xpos 0.02 ypos 0.15
    for i in range(8):
        $ weight = comm[i].weight*100
        $ support = comm[i].support
        $ name = comm[i].name
        text "[name]([weight]%): [support]" xpos 0.02 ypos (0.18+(i*0.03))
    text "Campaign Funds: [funds]" xpos 0.02 ypos 0.44
    text "Personal Motivation: [pm]" xpos 0.02 ypos 0.49
    text "Weeks until election: [wue]" xpos 0.02 ypos 0.55
#    text "Upper Class([(comm[0].weight)*100]%): [comm[0].support]"
label nextTurn:
    python:
        wue = wue-1
        tdonations = 0
        for i in comm:
            tdonations = i.donation()
            i.support = i.support + (i.s_eq - i.support)/2
        funds = funds + tdonations/3 - 300
        r_opinion = r_opinion - 0.1*r_opinion
        if party!="Independant":
            funds=funds+50
    if funds<=0:
        jump bankrupt
        return
    show screen show_metrics
    show metrics black at left
    return
label bankrupt:
    scene bg loss
    "You have run out of funds and are forced to drop out of the race.
    \nClick to restart"
    return
# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg office

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show protagonist base

    # These display lines of dialogue.

    "Welcome to Rise to Power!"
    "You are an ethusiastic citizen who wants to make the world a better place by entering into public office. The election is in 3 weeks and there are many hurdles you are yet to cross. There is only 1 goal: Get Elected!
    {p=2}Click anywhere to continue."

    hide protagonist base
    show campaignmanager base
    CM "Hey there! I am Aileen and I'll be your Campaign Manager."
    CM "Before we get started, we have to decide which political party you should, if any.
    \nJoining a political party increases public support from their core demographics."
    CM "You can either join the Conservatives or the Liberals, based on your idealogy. Both parties are marred by corruption scandals, but unfortunately, those are the only choices."
    CM "You can also choose to run as an independant. You wouldn't get much public support but at least you won't compromise on your values."


menu:

    CM "Which party would you like to join?"

    "I would like to join the Conservatives.":
        jump w1Conservatives
    "I would like to join the Liberals.":
        jump w1Liberals
    "I would like to remain independant":
        jump w1Independant

label w1Conservatives:
    python:
        party = "Conservatives"
        comm[0].s_eq = 50
        comm[0].support = 70
        comm[1].s_eq = 50
        comm[1].support = 50
        comm[2].s_eq = 0
        comm[2].support = 10
        comm[3].s_eq = 50
        comm[3].support = 60
        comm[4].s_eq = 40
        comm[4].support = 30
        comm[5].s_eq = 60
        comm[5].support = 50
        comm[6].s_eq = 0
        comm[6].support = 30
        comm[7].s_eq = 80
        comm[7].support = 60
        pm=pm-10
    CM "You have joined the Conservatives!"
    jump week2
label w1Liberals:
    python:
        party = "Liberals"
        comm[0].s_eq = 50
        comm[0].support = 30
        comm[1].s_eq = 50
        comm[1].support = 50
        comm[2].s_eq = 80
        comm[2].support = 90
        comm[3].s_eq = 50
        comm[3].support = 40
        comm[4].s_eq = 50
        comm[4].support = 70
        comm[5].s_eq = 40
        comm[5].support = 50
        comm[6].s_eq = 80
        comm[6].support = 60
        comm[7].s_eq = 0
        comm[7].support = 30
        pm=pm-10
    CM "You have joined the Liberals!"
    jump week2
label w1Independant:
    python:
        comm[0].support = 10
        comm[1].support = 10
        comm[2].support = 10
        comm[3].support = 10
        comm[4].support = 10
        comm[5].support = 10
        comm[6].support = 10
        comm[7].support = 10
    CM "I see you have decided to fight this battle alone. It's a tough road ahead."
    jump week2
label week2:
    call nextTurn from _call_nextTurn
#    $ nextTurn()
#    show screen show_metrics
    scene bg roger
    with fade
    show roger base
    show metrics black at left
    r "Good aftertoon candidate! I am Roger Steel from ABC Oil and Gas and I have a proposition for you."
    r "We were hoping you could endorse ABC Oil and Gas’s new pipeline through the town and condemn those “environmental protestors”. The Oil and Gas lobby will be more than happy to financially and publically support your campaign."
menu:
    r "What do you say, candidate?"

    "I would be happy to accept your generous contribution and endorse the pipeline!":
        jump w2Endorse
    "Thank you for the offer but I would not like to get involved in this issue.":
        jump w2Neutral
    "That pipeline is a threat to the safety of the people and the environment! I support the protests.":
        jump w2Protest

label w2Endorse:
    python:
        comm[0].support = comm[0].support+10
        comm[1].support = comm[1].support-10
        comm[2].support = comm[2].support
        comm[3].support = comm[3].support+20
        comm[4].support = comm[4].support
        comm[5].support = comm[5].support+30
        comm[6].support = comm[6].support
        comm[7].support = comm[7].support-10
        r_opinion = r_opinion+50
        funds = funds+400
        pm=pm-20
    r "Smart decision candidate! The Oil and Gas lobby shall be extremely pleased. Expect significant campaign contributions soon ;)"
    jump week3
label w2Neutral:
    python:
        comm[0].support = comm[0].support
        comm[1].support = comm[1].support-5
        comm[2].support = comm[2].support
        comm[3].support = comm[3].support-5
        comm[4].support = comm[4].support
        comm[5].support = comm[5].support-15
        comm[6].support = comm[6].support
        comm[7].support = comm[7].support-5
        r_opinion = r_opinion-15
        pm=pm-10
    r "This is politics candidate, you will have to get involved at some point. You won't get anywhere if you don't keep the right people happy."
    jump week3
label w2Protest:
    python:
        comm[0].support = comm[0].support-5
        comm[1].support = comm[1].support+10
        comm[2].support = comm[2].support
        comm[3].support = comm[3].support-25
        comm[4].support = comm[4].support
        comm[5].support = comm[5].support-30
        comm[6].support = comm[6].support
        comm[7].support = comm[7].support+10
        r_opinion = r_opinion-50
        pm=pm+10
    r "Wrong answer! The loss of potential jobs will be your fault candidate. I'm sure your opponent will choose wisely."
    jump week3

label week3:
    call nextTurn from _call_nextTurn_1
    scene bg office
    with fade
    show campaignmanager base
    show metrics black at left
    CM "There have been increasing demands by the public to expand social security benefits for the homeless and unemployed. However this may mean increasing taxes and may anger some of our supporters."

menu:
    CM "How would you like to frame your tax policy?"

    "We should expand social security by raising corporate and marginal taxes.":
        jump w3Corporate
    "We should expand social security by raising taxes for the middle class.":
        jump w3Middle
    "Social security is too big anyways. We should in fact reduce welfare benefits and lower taxes for everyone.":
        jump w3Welfare
    "Social security and taxes are good as it is. There is no need for change.":
        jump w3Neutral

label w3Corporate:
    python:
        comm[0].support = comm[0].support-40
        comm[1].support = comm[1].support+5
        comm[2].support = comm[2].support+30
        comm[3].support = comm[3].support+15
        comm[4].support = comm[4].support+15
        comm[5].support = comm[5].support-60
        comm[6].support = comm[6].support+10
        comm[7].support = comm[7].support+10
        r_opinion = r_opinion-40
    CM "This is sure to make our more generous supporters very unhappy. Let's hope they don't withdraw their support."
    jump Election
label w3Middle:
    python:
        comm[0].support = comm[0].support
        comm[1].support = comm[1].support-45
        comm[2].support = comm[2].support+25
        comm[3].support = comm[3].support-5
        comm[4].support = comm[4].support
        comm[5].support = comm[5].support
        comm[6].support = comm[6].support-5
        comm[7].support = comm[7].support+5
    CM "The people will not like that! Hopefully the idea of expanded social security would balance it out."
    jump Election
label w3Welfare:
    python:
        comm[0].support = comm[0].support+30
        comm[1].support = comm[1].support+25
        comm[2].support = comm[2].support-40
        comm[3].support = comm[3].support
        comm[4].support = comm[4].support+5
        comm[5].support = comm[5].support+60
        comm[6].support = comm[6].support+5
        comm[7].support = comm[7].support-5
        pm=pm-10
    CM "Some of our key supporters will be really pleased. However, it will really hurt those in need."
    jump Election
label w3Neutral:
    python:
        comm[0].support = comm[0].support
        comm[1].support = comm[1].support-5
        comm[2].support = comm[2].support-10
        comm[3].support = comm[3].support-5
        comm[4].support = comm[4].support
        comm[5].support = comm[5].support
        comm[6].support = comm[6].support
        comm[7].support = comm[7].support
        r_opinion = r_opinion-40
    CM "This may make people slightly unhappy but nothing they can't forgive."
    jump Election
label Election:
    hide screen show_metrics
    scene bg office
    with fade
    show campaignmanager base
    CM "The election has been called! Are you ready for the results?"
    python:
        ps=0
        for i in comm:
            ps=ps+(i.support*i.weight)
        ps=ps/3
    if ps<=50:
        scene bg loss
        "The results are in and it seems only [ps]\% of the citizens voted for you. You have lost the election.
        \nClick to return to the main menu."
    else:
        scene bg win
        "Congratulations! [ps]\% of the citizens have chosen you as their next representative.
        \nClick to return to the main menu."
    # This ends the game.

    return
