import random
#This simulation is used to find the average bleed DPS
#This is tricky with Aspect of the Cat and Farrul's Pounce since the bleed situations can vary widely

#Usage Note: This doesn't take into account any increased/more damage multipliers. Don't Spec Crimson Dance or ignore the 50% less in PoB when getting your damage #s
#Set up Path of Building and set all your configuration options and then take the min/max damage values
#Take the Min and Max Damage numbers from the "MH Source Physical" in PoB Calcs Tab in the Bleed Box

#TODO LIST
# - Instead of incrementally re-simulating longer lenghts updated dps each second, add in the new bleeds (would be MUCH more efficient)
# - Add rotating Stealth/Agility to simulation (changes in attk speed, bleed chance, crit chance, and Crimson Dance) - Big Addition
    #Each iteration could start at a random second within an Aspect phase
    
#==============SETUP AND VARIABLES==================
#If you want to print out some weighted DPS calculations based roughly on the rotating effects of Aspect of the Cat and Farrul's Pounce Gloves
farruls_pounce = True

# Current Values are my 6-Link Siege Balista Setup for Single Target Bleeds
use_skill_one = True
skill_one_min, skill_one_max = 34800, 88400

# Current Values are Puncture with GMP and Chain for Nice Bleed Spreading and duration
use_skill_two = True
skill_two_min, skill_two_max = 9600, 27200

skill_one_aps, skill_two_aps = 1.4, 3.2
#TODO
#skill_one_aps_cats_stealth=1.39
#skill_one_aps_cats_agility=1.45
#skill_two_aps_cats_stealth=3.08
#skill_two_aps_cats_agility=3.23


simulation_time=5 #In seconds, how long you continuously attack (DPS errors exist if longer than your bleed duration)
simulation_trials=10000

if int(simulation_time) < 1:
  print('Simulation time should be a time > 1 and preferably an integer. Given time: ' + str(simulation_time))
  exit()

skill_one_bleed_chance=100 # Siege Ballista - Chance to bleed gem + Tree Passives
skill_two_bleed_chance=100 # Puncture Has 100% anyways

crit_chance=34
#TODO
#cats_stealth_crit_chance=34
#cats_agility_crit_chance=27
crit_chance_lucky=True # Diamond Flask Active

crit_multiplier=1.5 #Can put your actual Crit Multi here, does nothing unless you have Perfect Agony (not worht usually)
crit_multiplier_for_ailments=1.5 #Don't Modify this base value

accuracy=94 # technically 91% chance - 94% chance if bleeding (Farrul's Pounce) #Todo consider hit chance after first bleed

#Perfect Agony Sucks unless you just happen to have a bunch of crit multi anyways
#Ailements always use your base crit multiplier 150%. Perfect Agony lets any crit over that be applied at 30% actual value
perfect_agony=False
if perfect_agony:
  crit_multiplier_for_ailments += ((crit_multiplier - 1.5) * .3)

ruthless=False #Only for Meele Attacks

ryslatha=True #Unique belt increases max/min hit range
ryslatha_min_roll=.6 #Change based on your belt roll (.6-.7)
ryslatha_max_roll=1.38 #Change based on your belt roll (1.3-1.4)

watchers_eye=True # Watcher's Eye Mod "Ailments you inflict deal damage faster while affected by Malevolence"
watchers_eye_roll = .15 # (10-15%) Mod Roll

synthesis_bleed_faster=True
synthesis_bleed_faster_val = .35 # (30-35%) Synthesis faster implicit on bow

enemy_maimed=True
maim_effect=15 #10-15 Value based on gem level (Only need in one skill, preferably not your single target skill)

war_banner=True
war_banner_effect=12 #8-12 based on Gem Level (Aura Effect?)

vuln_curse=True
vuln_effect=21 #Make sure this fits your gem level and also less effect for Shaper/Normal Boss. Increased Phys taken + Increased Phys taken over time * less effect

glad_passive_blood_in_the_eyes=True #10% increased physical dmg taken when maimed

inc_dmg_taken_multi = 100 #Track effective DPS from increased damage taken modifiers
if enemy_maimed:
  inc_dmg_taken_multi += maim_effect
  if glad_passive_blood_in_the_eyes:
    inc_dmg_taken_multi += 10
if vuln_curse:
  inc_dmg_taken_multi += vuln_effect
if war_banner:
  inc_dmg_taken_multi += war_banner_effect
inc_dmg_taken_multi /= 100 #for percent value
  
if ryslatha:
  #Calculating the max and min damage from unique belt "Ryslatha"
  skill_one_min = int(skill_one_min * ryslatha_min_roll)
  skill_two_min = int(skill_two_min * ryslatha_min_roll)
  skill_one_max = int(skill_one_max * ryslatha_max_roll)
  skill_two_max = int(skill_two_max * ryslatha_max_roll)
  
# =============END SETUP/VARIABLES===================


# =============START FUNCTIONS=======================
def CalculateBleeds(aps, attk_time, min_dmg, max_dmg, bleed_chance):
  return_bleeds = []
  for t in range(0, int(aps * attk_time)):
    #Hit and Bleed Check
    if random.randint(0,99) < accuracy and random.randint(0, 99) < bleed_chance:
      #Bleed Based on random value between min and max damage
      bleed = float(random.randint(min_dmg, max_dmg))
        
      #Fossil Mod Chance to double damage with bleeding
      if random.randint(0, 99) < 60:
        bleed *= 2

      #DO NOT LINK TO RANGED ATTACKS EVEN THOUGH THE GAME SAYS IT WORKS
      if ruthless:#Important, PoB gives Ruthess a 37% more multi, so ware of that if you use this
        if t % 3 == 2: #Every third hit
          bleed = bleed * 2.13 #113 More damage with bleeding
        
      #Crimson Dance bleed is 35% This is doubled later if we are simulating at 70% solo bleed
      bleed = bleed * .35
        
      #Bleeds Faster from watcher's eye 15% faster and Sythesis Implicit 35% faster
      bleed_faster_multi = 1
      if watchers_eye:
        bleed_faster_multi += watchers_eye_roll
      if synthesis_bleed_faster:
        bleed_faster_multi += synthesis_bleed_faster_val
      
      bleed *= bleed_faster_multi

      #Effective DPS calc for all increased damage taken modifiers added together
      bleed *= inc_dmg_taken_multi
         
      # Crit Chance, with Diamond Flask support
      if (random.randint(0,99) < crit_chance) or (crit_chance_lucky and random.randint(0,99) < crit_chance):
        bleed *= crit_multiplier_for_ailments
        
      return_bleeds.append(int(bleed))
  #print(return_bleeds) #Had to debug some issues
  return return_bleeds
  

# =============START MAIN SIMULATION=======================
print('\n\n\nThis simulation is trying to show an average Bleed DPS after attacking for a given time with up to two skills. You plus a totem or mirage archer')
print('This simulation runs '+ str(simulation_trials) + ' trials to get average top bleeds.')
  
for i in range(0, int(simulation_time)): #Huge outer for loop to show ramping dps every second
  crimson_dance = []     #A list of the sum of the top 8 bleeds from each trial
  non_crimson_dance = [] #A list of the top bleeds (X2 to simulate it not being a Crimson Dance Hit)
  
  for j in range(0, simulation_trials):
    bleeds = []
    time_attacking = i+1
    #Skill One (Siege Ballista)
    if use_skill_one:
      list_one = CalculateBleeds(skill_one_aps, time_attacking, skill_one_min, skill_one_max, skill_one_bleed_chance)
      bleeds.extend(list_one) if list_one is not None else None
      
    #Skill Two (Puncture)
    if use_skill_two:
      list_two = bleeds.extend(CalculateBleeds(skill_two_aps, time_attacking, skill_two_min, skill_two_max, skill_two_bleed_chance))
      bleeds.extend(list_two) if list_two is not None else None
   
    #After each trial, sort and pull top 8 bleeds, and double top bleed for Solo Bleed Simulation      
    bleeds.sort(reverse=True)
    top_eight_bleeds = sum(bleeds[:8])
    crimson_dance.append(top_eight_bleeds)
    non_crimson_dance.append(sum(bleeds[:1]) * 2) # Farrul's Pounce when only dealing 1 bleed will be non-crimson dance value @ 70%, hence the x2

  #Now Get averages over all trials
  avg_crimson_dance = sum(crimson_dance) / simulation_trials
  avg_non_crimson_dance = sum(non_crimson_dance) / simulation_trials
  avg_non_crimson_dance_with_movement= avg_non_crimson_dance * 3

  print('\n\nAttacking non stop for ' + str(i+1) + ' seconds')
  #print('I\'m using a 6-link siege ballista for single target damage (slower aps, very hard hitting bleed) and puncture to fill out lots of long bleeds to always take advantage of Crimson dance when it is up. Also GMP+Chain for Map clear\n')

  print('Crimson Dance:                    ' + str("{:,}".format(int(avg_crimson_dance))) + ' DPS')
  print('VS')
  print('Non-Crimson Dance Top Bleed:      ' + str("{:,}".format(int(avg_non_crimson_dance))) + ' DPS')
  print('    With Movement Bonus:          ' + str("{:,}".format(int(avg_non_crimson_dance_with_movement))) + ' DPS')
  if farruls_pounce:
    print('\nNow lets look at Farrul\'s Pounce and Aspect of the Cat')
    print('6 seconds of Crimson Dance during Cat\'s Stealth (using Farrul\'s Fur). Inflicts 35% bleeds, top 8 bleeds damage at a time, no movement bonus')
    print('6 seconds of non CD bleed during Cat\'s Agility. Inflict 70% bleed, x3 damage when moving.\n')

    print('Crimson Dance and Non-Crimson Dance are separate debuffs allowing up to 9 bleeds. Ideally we could link Aspect of the Cat to Less Duration,')
    print('but lets do some rough weighted calculations for both Aspect Phases:\n')

    weighted_average = (avg_crimson_dance * .5) + (avg_non_crimson_dance * .5)
    weighted_average_with_movement = (avg_crimson_dance * .5) + (avg_non_crimson_dance_with_movement * .5)
    weighted_nine_bleeds = (avg_crimson_dance) + (avg_non_crimson_dance)
    weighted_nine_bleeds_and_movement = (avg_crimson_dance) + (avg_non_crimson_dance_with_movement)

    print('50% of the time Crimson Dance + 50% of the time Single bleed:')
    print(str("{:,}".format(int(weighted_average))) + ' DPS -- or ' + str(int(int(weighted_average) / int(avg_crimson_dance) * 100)) + '% damage compared to straight crimson dance')
    print(str("{:,}".format(int(weighted_average_with_movement))) + ' DPS if movement bonus during Cat\'s Agility -- or ' + str(int(int(weighted_average_with_movement) / int(avg_crimson_dance) * 100)) + '% damage compared to straight crimson dance\n')

    print('DPS with 9 Bleeds.(8 Stacked during CD + 1 During no CD)')
    print(str("{:,}".format(int(weighted_nine_bleeds))) + ' DPS -- ' + str(int(int(weighted_nine_bleeds) / int(avg_crimson_dance) * 100)) + '% damage compared to straight crimson dance')
    print(str("{:,}".format(int(weighted_nine_bleeds_and_movement))) + ' DPS if movement bonus during Cat\'s Agility -- or ' + str(int(int(weighted_nine_bleeds_and_movement) / int(avg_crimson_dance) * 100)) + '% damage compared to straight crimson dance\n')

    print('9 Bleed damage looks great but you can\'t achieve it until you\'ve been attacking through both phases and your bleed duration needs to be long enouhg or your aspect phase needs to be short enough to make it work consistently and not take forever to achieve.')
