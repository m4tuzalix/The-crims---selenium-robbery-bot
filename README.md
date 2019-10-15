# The-crims---selenium-robbery-bot

The crims is web in-page game. You are a gangster and you manage your criminal imperium. Robberies are the most famous way to earn money
in this game. It is a bit monotonous and time consuming. Bot does it for us ;)

15.10.2019 UPDATE

- sequence for normal robberies: 
    #Always picks the most profitable jump with 100% of success
    #Restories stamina by taking drugs in the club - always picks the strongest drug (more stamina to get) and counts amount required to 
      acquire 100% stamina. If overdosed you die and go to hospital for 30 minutes. Bot never mistakes in calculation ;)
    #Reudces toxication if higver than 10% - The higher toxiacation, the worse effect of drugs (less stamina, more money to spend)
      
- sequence for gang robbersies:
   #Almost the same as above with small improvments. To rob in gang other people must agree the jump. Sometimes it takes the ages so bot        has proper timeouts to recheck if clicked :)
      
- sequence for killing people in clubs:
   #If man's respect range or proffession is different than the one in seettings - bot exits the club (More powerful opponenents)
   #Kills people in set range of respect for instance 10k-100k
   #Avoids particular proffesions and ranks - exits the club
   #Restores stamina - one assault takes 50%
    
