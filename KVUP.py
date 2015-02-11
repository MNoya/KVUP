##import ConfigParser


##NOTE: Files must have an empty line at the end
endline = '}\n\n'

#Armor Types: - "CombatClassDefend"
#------------
armortypes = {}
armortypes['Flesh'] = 'DOTA_COMBAT_CLASS_DEFEND_SOFT'
armortypes['small'] = 'DOTA_COMBAT_CLASS_DEFEND_WEAK'
armortypes['medium'] = 'DOTA_COMBAT_CLASS_DEFEND_BASIC'
armortypes['large'] = 'DOTA_COMBAT_CLASS_DEFEND_STRONG'
armortypes['fort'] = 'DOTA_COMBAT_CLASS_DEFEND_STRUCTURE'
armortypes['hero'] = 'DOTA_COMBAT_CLASS_DEFEND_HERO'
armortypes['none'] = 'NONE' # Ignored
armortypes['divine'] = 'DIVINE' # Needs custom mechanic


#Attack Types: - "CombatClassAttack"
#--------------
attacktypes = {}
attacktypes['normal'] = 'DOTA_COMBAT_CLASS_ATTACK_BASIC'
attacktypes['pierce'] = 'DOTA_COMBAT_CLASS_ATTACK_PIERCE'
attacktypes['siege'] = 'DOTA_COMBAT_CLASS_ATTACK_SIEGE'
attacktypes['chaos'] = 'DOTA_COMBAT_CLASS_ATTACK_LIGHT'
attacktypes['hero'] = 'DOTA_COMBAT_CLASS_ATTACK_HERO'
attacktypes['magic'] = 'MAGIC' # Needs custom mechanic
attacktypes['spells'] = 'SPELLS' # Needs custom mechanic

#Movement Types: - ""
#--------------
movementtypes = {}
movementtypes['foot'] = 'DOTA_UNIT_CAP_MOVE_GROUND'
movementtypes['fly'] = 'DOTA_UNIT_CAP_MOVE_FLY'
movementtypes['float'] = 'DOTA_UNIT_CAP_MOVE_GROUND'
movementtypes['hover'] = 'DOTA_UNIT_CAP_MOVE_GROUND'
movementtypes['_'] = 'DOTA_UNIT_CAP_MOVE_NONE'
movementtypes[''] = 'DOTA_UNIT_CAP_MOVE_NONE'
movementtypes['amph'] = 'DOTA_UNIT_CAP_MOVE_GROUND'
movementtypes['horse'] = 'DOTA_UNIT_CAP_MOVE_GROUND'

#Attribute Primary 
attributeprimary = {}
attributeprimary['STR'] = 'DOTA_ATTRIBUTE_STRENGTH'
attributeprimary['INT'] = 'DOTA_ATTRIBUTE_INTELLECT'
attributeprimary['AGI'] = 'DOTA_ATTRIBUTE_AGILITY'

#Collision Hull
boundshullnames = {}
boundshullnames['144'] = 'DOTA_HULL_SIZE_BARRACKS'
boundshullnames['96'] = 'DOTA_HULL_SIZE_FILLER'
boundshullnames['81'] = 'DOTA_HULL_SIZE_BUILDING'
boundshullnames['80'] = 'DOTA_HULL_SIZE_HUGE'
boundshullnames['24'] = 'DOTA_HULL_SIZE_HERO'
boundshullnames['16'] = 'DOTA_HULL_SIZE_REGULAR'
boundshullnames['8'] = 'DOTA_HULL_SIZE_SMALL'

class wc3pars:
    def __init__(self, section):
        self.npc_name = ''
        if 'Name' in section:
            self.npc_name = section['Name']
        
        # BaseClass
        self.baseclass = 'npc_dota_creature'
        if 'isbldg' in section:
            if section['isbldg'] is '1':
                self.baseclass = 'npc_dota_building'
        self.level = 0
        if 'level' in section:
            if section['level'] is not '-':
                self.level = section['level']

        # Abilities
        self.abilitycounter = 1
        self.abilitylist = None
        if 'abilList' in section:
            if section['abilList'] is not '_':
                self.abilitylist = section['abilList']
                self.abilitylist = self.abilitylist.split(',')
        self.heroabilitylist = None
        if 'heroAbilList' in section:
            if section['heroAbilList'] is not '':
                self.heroabilitylist = section['heroAbilList']
                self.heroabilitylist = self.heroabilitylist.split(',')

        self.combatclassdefend = 'DOTA_COMBAT_CLASS_DEFEND_BASIC'
        if 'defType' in section:
            self.combatclassdefend = armortypes[section['defType']]
        self.armorphys = None
        if 'def' in section:
            self.armorphys = section['def']
        self.armormagic = 0

        self.attackcapabilities = 'DOTA_UNIT_CAP_MELEE_ATTACK'
        if 'weapsOn' in section:
            if section['weapsOn'] is '0':
                self.attackcapabilities = 'DOTA_UNIT_CAP_NO_ATTACK'

        self.attackdamagemin = '0'
        self.attackdamagemax = '0'
        if (('dice1' and 'sides1') in section):
            if section['dice1'] is not '-' and section['sides1'] is not '-':
                self.attackdamagemin = str(float(section['dice1']) + float(section['dmgplus1']))
                self.attackdamagemax = str(float(section['dice1']) * float(section['sides1']) + float(section['dmgplus1']))
        self.attackdamagetype = 'DAMAGE_TYPE_ArmorPhysical'
        self.attackrate = None
        if 'cool1' in section:
            self.attackrate = section['cool1']
        self.attackanimationpoint = None
        if 'dmgpt1' in section:
            self.attackanimationpoint = section['dmgpt1']
        self.attackacqurange = None
        if 'acquire' in section:
            self.attackacqurange = section['acquire']
        self.attackrange = None
        if 'rangeN1' in section:
            self.attackrange = section['rangeN1']

        self.projectilemodel = None
        self.projectilespeed = None
        if self.attackrange.find('-') == -1:
            if float(self.attackrange) > 128:
                if 'Missilespeed' in section:
                    if section['Missilespeed'] is not '':
                        self.projectilemodel = ''
                        self.projectilespeed = section['Missilespeed']
                        self.attackcapabilities = 'DOTA_UNIT_CAP_RANGED_ATTACK'
        
        self.combatclassattack = 'DOTA_COMBAT_CLASS_ATTACK_BASIC'
        if 'atkType1' in section:
            if section['atkType1'] is not 'none':
                self.combatclassattack = attacktypes[section['atkType1']]
            else:
                self.combatclassattack = None
                self.attackcapabilities = 'DOTA_UNIT_CAP_NO_ATTACK'

        # Add Hero Attributes
        self.attributeprimary = None
        if 'Primary' in section:
            if section['Primary'] is not '_':
                self.attributeprimary = attributeprimary[section['Primary']]
                self.attributebasestrength = section['STR']
                self.attributestrengthgain = section['STRplus']
                self.attributebaseintelligence = section['INT']
                self.attributeintelligencegain = section['INTplus']
                self.attributebaseagility = section['AGI']
                self.attributeagilitygain = section['AGIplus']

        # Add Gold, Lumber and Food Cost
        self.goldcost = 0
        if 'goldcost' in section:
            self.goldcost = section['goldcost']

        self.lumbercost = 0
        if 'lumbercost' in section:
            self.lumbercost = section['lumbercost']

        self.foodcost = 0
        if 'foodcost' in section:
            self.foodcost = section['foodcost']

        # Add Formation Rank, for custom pathing on units
        self.formation = None
        if 'formation' in section and self.baseclass is not 'npc_dota_building':
            self.formation = section['formation']

        # Add Build Time
        self.buildtime = None
        if 'bldtm' in section:
            self.buildtime = section['bldtm']

        self.bountygoldmin = None
        self.bountygoldmax = None
        if 'bountydice' in section:
            self.bountygoldmin = str(float(section['bountydice']) + float(section['bountyplus']))
            self.bountygoldmax = str(float(section['bountydice']) * float(section['bountysides']) + float(section['bountyplus']))

        self.statushealth= '1'
        if 'HP' in section:
            self.statushealth = section['HP']
        self.statushealthregen = '0'
        if 'regenHP' in section:
            if section['regenHP'] is not '-':
                self.statushealthregen = section['regenHP']
        self.statusmana = '0'
        if 'manaN' in section:
        	if section['manaN'] not in '-':
        		self.statusmana = section['manaN']              
        self.statusmanaregen = '0'
        if 'regenMana' in section:
            if section['regenMana'] is not ' - ' and section['regenMana'] is not '-':
                self.statusmanaregen = section['regenMana']
        self.visiondaytimerange = 10
        if 'sight' in section:
            self.visiondaytimerange = section['sight']
        self.visionnighttimerange = 10
        if 'nsight' in section:
            self.visionnighttimerange = section['nsight']

        self.movementcapabilities = 'DOTA_UNIT_CAP_MOVE_NONE'
        self.movementspeed = '0'
        if 'spd' in section:
            self.movementspeed = section['spd']
            if 'movetp' in section:
                self.movementcapabilities = movementtypes[section['movetp']]
        self.movementturnrate = '0.5'
        if 'turnRate' in section:
            self.movementturnrate = section['turnRate']

        # Defaults
        self.boundshullname = 'DOTA_HULL_SIZE_HERO'
        self.healthbaroffset = 140

        # Proper collision, to SetHullRadius and adjust bounds later
        self.collision = None
        if 'collision' in section:
            self.collision = section['collision']

        self.team = 'DOTA_TEAM_NEUTRALS'
        if self.baseclass is 'npc_dota_building':
            self.unitrelationshipclass = 'DOTA_NPC_UNIT_RELATIONSHIP_TYPE_BUILDING'
        else:
            self.unitrelationshipclass = 'DOTA_NPC_UNIT_RELATIONSHIP_TYPE_DEFAULT'      

        self.comments = ''
        
        self.description = None
        if 'Ubertip' in section:
            self.description = section['Ubertip']

    def check(self):
        print(self.npc_name)
        print(self.statushealthregen)
        print(self.statusmanaregen)

    def writetofile(self, nfile, write):  ##if you need to edit the format or spelling or whatever, do it here
        newfile = open(nfile, write)
        lines = []
        section = ''
        lines.append('\n')
        lines.append(self.unitcomment(self.npc_name))
        lines.append(self.kline(self.npc_name.replace(' ', '_')))
        lines.append(self.kvcomment(' General'))
        lines.append(self.kvcomment('----------------------------------------------------------------'))
        if self.attributeprimary is not None:
            self.baseclass = ''
            lines.append(self.kvline('override_hero', self.baseclass, "Add npc_dota_hero internal name"))
        else:
            lines.append(self.kvline('BaseClass', self.baseclass,None))
            lines.append(self.kvline('Model', '', 'Add model'))
            lines.append(self.kvline('ModelScale', '1', None))
            lines.append(self.kvline('Level', self.level, None))
            lines.append(self.kvline('HealthBarOffset', self.healthbaroffset, None))

        lines.append(self.kvcomment(None))
        
        lines.append(self.kvcomment(' Abilities'))
        lines.append(self.kvcomment('----------------------------------------------------------------'))

        if self.abilitylist is not None:
            for abil in self.abilitylist:
                lines.append(self.kvline('Ability' + str(self.abilitycounter), '', 'Reference: ' + abil))
                self.abilitycounter += 1
        if self.heroabilitylist is not None:
            for abil in self.heroabilitylist:
                lines.append(self.kvline('Ability' + str(self.abilitycounter), '', 'Reference: ' + abil))
                self.abilitycounter += 1
        lines.append(self.kvcomment(None))

        lines.append(self.kvcomment(' Armor'))
        lines.append(self.kvcomment('----------------------------------------------------------------'))
        lines.append(self.kvline('ArmorPhysical', self.armorphys, None))
        lines.append(self.kvline('MagicalResistance', self.armormagic, None))
        lines.append(self.kvcomment(None))

        lines.append(self.kvcomment(' Attack'))
        lines.append(self.kvcomment('----------------------------------------------------------------'))
        lines.append(self.kvline('AttackCapabilities',self.attackcapabilities, None))
        lines.append(self.kvline('AttackDamageType', self.attackdamagetype, None))
        lines.append(self.kvline('AttackDamageMin', self.attackdamagemin, None))
        lines.append(self.kvline('AttackDamageMax', self.attackdamagemax, None))

        if not self.attackrate.find('-') != -1:
        	lines.append(self.kvline('AttackRate', self.attackrate, None))

        if not self.attackanimationpoint.find('-') != -1:
        	lines.append(self.kvline('AttackAnimationPoint',self.attackanimationpoint, None))

        if not self.attackacqurange.find('-') != -1:
        	lines.append(self.kvline('AttackAcquisitionRange', self.attackacqurange, None))
        if not self.attackrange.find('-') != -1:
        	lines.append(self.kvline('AttackRange',self.attackrange, None))

        lines.append(self.kvline('ProjectileModel', self.projectilemodel, 'Add projectile'))
        lines.append(self.kvline('ProjectileSpeed', self.projectilespeed, None))
        lines.append(self.kvcomment(None))

        # Only for heroes
        if self.attributeprimary is not None:
            lines.append(self.kvcomment(' Attributes'))
            lines.append(self.kvcomment('----------------------------------------------------------------'))
            lines.append(self.kvline('AttributePrimary',self.attributeprimary, None))
            lines.append(self.kvline('AttributeBaseStrength', self.attributebasestrength, None))
            lines.append(self.kvline('AttributeStrengthGain', self.attributestrengthgain, None))
            lines.append(self.kvline('AttributeBaseIntelligence', self.attributebaseintelligence, None))
            lines.append(self.kvline('AttributeIntelligenceGain', self.attributeintelligencegain, None))
            lines.append(self.kvline('AttributeBaseAgility',self.attributebaseagility, None))
            lines.append(self.kvline('AttributeAgilityGain', self.attributeagilitygain, None))
            lines.append(self.kvcomment(None))

        lines.append(self.kvcomment(' Bounty'))
        lines.append(self.kvcomment('----------------------------------------------------------------'))
        lines.append(self.kvline('BountyGoldMin', self.bountygoldmin, None))
        lines.append(self.kvline('BountyGoldMax', self.bountygoldmax, None))
        lines.append(self.kvcomment(None))

        lines.append(self.kvcomment(' Bounds'))
        lines.append(self.kvcomment('----------------------------------------------------------------'))
        
        # Attempt to write the best hull and radius possible
        if float(self.collision) <= 8: 
            self.boundshullname = 'DOTA_HULL_SIZE_SMALL'
            self.ringradius = 40
        elif float(self.collision) <= 16:
            self.boundshullname = 'DOTA_HULL_SIZE_REGULAR'
            self.ringradius = 70
        elif float(self.collision) <= 24:
            self.boundshullname = 'DOTA_HULL_SIZE_HERO'
            self.ringradius = 100
        # Cut the 24-81 interval in half
        elif float(self.collision) <= 54:
            self.boundshullname = 'DOTA_HULL_SIZE_HERO'
            self.ringradius = 130
        elif float(self.collision) <= 81:
            self.boundshullname = 'DOTA_HULL_SIZE_BUILDING'
            self.ringradius = 160
        # Cut the 96-144 interval in half
        elif float(self.collision) <= 120:
            self.boundshullname = 'DOTA_HULL_SIZE_FILLER'
            self.ringradius = 190
        else:
            self.boundshullname = 'DOTA_HULL_SIZE_BARRACKS'
            self.ringradius = 220

        lines.append(self.kvline('BoundsHullName', self.boundshullname, None))
        lines.append(self.kvline('RingRadius', self.ringradius, None))
        lines.append(self.kvline('CollisionSize', self.collision, None))
        lines.append(self.kvline('FormationRank', self.formation, None))

        lines.append(self.kvcomment(None))

        lines.append(self.kvcomment(' Building Cost Stats'))
        lines.append(self.kvcomment('----------------------------------------------------------------'))
        lines.append(self.kvline('GoldCost', self.goldcost, None))
        lines.append(self.kvline('LumberCost', self.lumbercost, None))
        if self.baseclass is not 'npc_dota_building':
            lines.append(self.kvline('FoodCost', self.foodcost, None))
        lines.append(self.kvline('BuildTime', self.buildtime, None))

        lines.append(self.kvcomment(None))

        lines.append(self.kvcomment(' Movement'))
        lines.append(self.kvcomment('----------------------------------------------------------------'))
        lines.append(self.kvline('MovementCapabilities', self.movementcapabilities, None))
        if self.movementspeed is not '-':
	        lines.append(self.kvline('MovementSpeed', self.movementspeed, None))
        else:
            lines.append(self.kvline('MovementSpeed', '0', None))
        if self.movementturnrate is not '-':
	        lines.append(self.kvline('MovementTurnRate', self.movementturnrate, None))
        lines.append(self.kvcomment(None))

        lines.append(self.kvcomment(' Status'))
        lines.append(self.kvcomment('----------------------------------------------------------------'))
        lines.append(self.kvline('StatusHealth', self.statushealth, None))
        lines.append(self.kvline('StatusHealthRegen', self.statushealthregen, None))

		# Careful with negative mana regen 
        if not self.statusmana.find('-') != -1:
            lines.append(self.kvline('StatusMana', self.statusmana, None))
        else:
           lines.append(self.kvline('StatusMana', '0', None)) 

        if not self.statusmanaregen.find('-') != -1:
            lines.append(self.kvline('StatusManaRegen', self.statusmana, None))
        else:
           lines.append(self.kvline('StatusManaRegen', '0', None))

        lines.append(self.kvcomment(None))

        lines.append(self.kvcomment(' Vision'))
        lines.append(self.kvcomment('----------------------------------------------------------------'))
        lines.append(self.kvline('VisionDaytimeRange', self.visiondaytimerange, None))
        lines.append(self.kvline('VisionNighttimeRange', self.visionnighttimerange, None))
        lines.append(self.kvcomment(None))
        
        lines.append(self.kvcomment(' Team'))
        lines.append(self.kvcomment('----------------------------------------------------------------'))
        lines.append(self.kvline('TeamName', self.team, None))

        if self.combatclassattack is 'MAGIC':
            self.combatclassattack = 'DOTA_COMBAT_CLASS_ATTACK_HERO'
            lines.append(self.kvline('CombatClassAttack', self.combatclassattack, "MAGIC - Attacks deal magic damage, ignores physical armor"))
        elif self.combatclassattack is 'SPELLS':
            self.combatclassattack = 'DOTA_COMBAT_CLASS_ATTACK_HERO'
            lines.append(self.kvline('CombatClassAttack', self.combatclassattack, "SPELLS - Attacks only through spells"))
        else:
            lines.append(self.kvline('CombatClassAttack', self.combatclassattack, None))
        
        if self.combatclassdefend is 'DIVINE':
            self.combatclassdefend = 'DOTA_COMBAT_CLASS_DEFEND_HERO'
            lines.append(self.kvline('CombatClassDefend', self.combatclassdefend, "DIVINE - Takes only 1/10 dmg from all types of atacks."))
        elif self.combatclassdefend is not 'NONE':
            lines.append(self.kvline('CombatClassDefend', self.combatclassdefend, None))
        lines.append(self.kvline('UnitRelationShipClass', self.unitrelationshipclass, None))
        lines.append(self.kvcomment(None))
    
        if self.baseclass is 'npc_dota_creature' and self.attributeprimary is None:
            lines.append(self.kvcomment(' Creature Data'))
            lines.append(self.kvcomment('----------------------------------------------------------------'))
            lines.append(self.kvblock('Creature'))
            lines.append(self.kvline2('DisableClumpingBehavior', '1', None))
            lines.append('\n\t}\n')
        lines.append(endline)
        for line in lines:
            section += line
        newfile.write(section)

    def kvline(self, key, val, comment):
        line = ''
        if val is not None:
            key = str(key)
            val = str(val)
            line = '\t"' + key + '"\t'
            # At least 1 tab, desired is align to the equivalent of 5 tabs
            # Need to account for the extra 2 "" characters
            if len(key) < 2:
                line += '\t'
            if len(key) < 6:
                line += '\t'
            if len(key) < 10:
                line += '\t'
            if len(key) < 14:
                line += '\t'
            if len(key) < 18:
                line += '\t'
            if len(key) < 22:
                line += '\t'
            line += '"' + val +'"'
            if comment is not None:
                line += '\t //' + comment
            line += '\n'
        return line

    def kvline2(self, key, val, comment):
        line = ''
        if val is not None:
            key = str(key)
            val = str(val)
            line = '\t\t"' + key + '"\t'
            # At least 1 tab, desired is align to the equivalent of 5 tabs
            # Need to account for the extra 2 "" characters
            if len(key) < 2:
                line += '\t'
            if len(key) < 6:
                line += '\t'
            if len(key) < 10:
                line += '\t'
            if len(key) < 14:
                line += '\t'
            if len(key) < 18:
                line += '\t'
            if len(key) < 22:
                line += '\t'
            line += '"' + val +'"'
            if comment is not None:
                line += '\t //' + comment
            #line += '\n'
        return line

    def kvcomment(self, comment):
        line =  '\t'
        if comment is not None:
            line += '//' + comment
        line += '\n'
        return line

    def unitcomment(self, comment):
        line = '//=================================================================================\n'
        line += '// Creature: ' + comment +'\n'
        if self.description is not None:
            line += '// Description: ' + self.description + '\n'
        line += '//=================================================================================\n'
        return line

    def kline(self, unit_name):
        line = '"'+ unit_name +'"\n' + '{\n'
        return line

    # 2nd level
    def kvblock(self, block_name):
        line = '\t"'+ block_name +'"\n' + '\t{\n'
        return line
        

def parse_file_section(textsec):
    lines = {}
    counter = 0
    with open(textsec) as f:
        for line in f:
            pair = line[0:-1].split('=')
            if len(pair) == 2:
                lines[pair[0]] = pair[1]
    return lines
    
def parse_text_section(textsec):
    textsec = textsec.split('\n')
    lines = {}
    counter = 0
    for line in textsec:
        pair = line.split('=')
        if len(pair) == 2:
            lines[pair[0]] = pair[1]
    return lines

def sectionoff(textfile):
    sections = {}
    with open(textfile, 'r') as f:
        secname = ''
        sec = ''
        for line in f:
            if line[0:1] == '[':
                sections[secname] = sec
                secname = line
                secname = secname[1:-2]
                sec = ''
            else:
                sec += line
    return sections


if __name__ == '__main__':
    fullfile = sectionoff('units.txt')
    print(fullfile[''])
    f = open('kv_units.txt','w')
    f.write('')
    for key in fullfile:
        if key is not '':
            afile = parse_text_section(fullfile[key])
            work = wc3pars(afile)
            work.writetofile('kv_units.txt', 'a')
    print('Finished Unit Parsing')
