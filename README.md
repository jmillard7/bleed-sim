# bleed-sim
Path of Exile Bleeding Simulator

This simulator will tell you your average Bleed DPS by simulating the scenario many times (10,000 by default). You need to input your attack time, aps, damage min/max and other gearing options. There is also support for your main skill and a secondary skill (totem, mirage archer, etc)

Note: you should take your damage numbers from Path of Building(PoB) in the calculate tab in the bleed box. We are letting PoB take care of all the "increased" and all the "more" modifiers that apply to bleed. You should unspec Crimson Dance in the builder before looking up this number since it is accounted already in this simulator. All the "Effective DPS Mod" calculations are also in the simulator, but require your input, alternatively take this PoB value and assign it to the "inc_dmg_taken_multi" variable after ln.94. EG 150% effective dps mod set the variable to 1.5

Other options include: Ruthless(Melee only), Ryslatha's Coil (Yes it works with bleed), crit/accuracy, bleed chance, diamond flask, Perfect Agony(kinda not worth), and Synthesis or Watcher's Eye "Bleeding you inflict deals damage faster"

The nice thing about this simulator is that I've separated each 10,000 simulations into 1 second intervals (while tracking/correcting for the aps multiplied by 1second rounding error) so that you can see your bleed dps for each second leading up to your input simulation time (Shouldn't be higher than your bleed duration). Also if desired you can select that you have Farrul's Pounce (allowing 9 bleeds) and get some nice weighted numbers in addition to and in contrast to only crimson dance damage or only non-crimson dance DPS.

# Example Output:
>This simulation shows an average Bleed DPS after attacking for a given time with up to two skills. You plus a totem or mirage archer
>This simulation runs 10000 trials to get average top bleeds.
>
>Attacking non stop for 1 seconds
>Crimson Dance:                    160,214 DPS
>VS
>Non-Crimson Dance Top Bleed:      265,928 DPS
>    With Movement Bonus:          797,786 DPS
>
>Attacking non stop for 2 seconds
>Crimson Dance:                    210,395 DPS
>VS
>Non-Crimson Dance Top Bleed:      342,790 DPS
>    With Movement Bonus:          1,028,370 DPS
>
>Attacking non stop for 3 seconds
>Crimson Dance:                    323,232 DPS
>VS
>Non-Crimson Dance Top Bleed:      387,389 DPS
>    With Movement Bonus:          1,162,167 DPS
v
>Attacking non stop for 4 seconds
vCrimson Dance:                    471,238 DPS
>VS
>Non-Crimson Dance Top Bleed:      418,238 DPS
>    With Movement Bonus:          1,254,715 DPS
>
>Attacking non stop for 5 seconds
>Crimson Dance:                    700,086 DPS
>VS
>Non-Crimson Dance Top Bleed:      441,257 DPS
>    With Movement Bonus:          1,323,772 DPS
>
>Now lets look at Farrul's Pounce and Aspect of the Cat
>6 seconds of Crimson Dance during Cat's Stealth (using Farrul's Fur). Inflicts 35% bleeds, top 8 bleeds damage at a time, no movement >bonus
>6 seconds of non CD bleed during Cat's Agility. Inflict 70% bleed, x3 damage when moving.
>
>Crimson Dance and Non-Crimson Dance are separate debuffs allowing up to 9 bleeds. Ideally we could link Aspect of the Cat to Less vDuration, but lets do some rough weighted calculations for both Aspect Phases:
>
>Never overlapping bleeds: 50% of the time Crimson Dance + 50% of the time Single bleed:
>570,671 DPS -- or 81% damage compared to straight crimson dance
>1,011,929 DPS if movement bonus only during Cat's Agility -- or 144% damage compared to straight crimson dance
>
>DPS with 9 Bleeds.(8 Stacked during CD + 1 During no CD)
>1,141,343 DPS -- 163% damage compared to straight crimson dance
>2,023,858 DPS if movement bonus during Cat's Agility -- or 289% damage compared to straight crimson dance
>
>9 Bleed damage looks great but you can't achieve it until you've been attacking through both phases and your bleed duration needs to be >long enouhg or your aspect phase needs to be short enough to make it work consistently and not take forever to achieve.

