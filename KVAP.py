##import ConfigParser
import sys
import os

##NOTE: Files must have an empty line at the end
endline = '}\n\n'

targets = {}
targets['_'] = 'DOTA_ABILITY_BEHAVIOR_NO_TARGET' #Behavior POINT or NO_TARGET

targets['ground'] = 'DOTA_UNIT_TARGET_BASIC' #Will also have  if nonhero isnt on the list
targets['structure'] = 'DOTA_UNIT_TARGET_BUILDING'
targets['tree'] = 'DOTA_UNIT_TARGET_TREE'
targets['hero'] = 'DOTA_UNIT_TARGET_HERO'
targets['mechanical'] = 'DOTA_UNIT_TARGET_MECHANICAL'

targets['enemy'] = 'DOTA_UNIT_TARGET_TEAM_ENEMY'
targets['ally'] = 'DOTA_UNIT_TARGET_TEAM_FRIENDLY'
targets['friend'] = 'DOTA_UNIT_TARGET_TEAM_FRIENDLY'

targets['nonancient'] = 'DOTA_UNIT_TARGET_FLAG_NOT_ANCIENTS'
targets['invu'] = 'DOTA_UNIT_TARGET_FLAG_INVULNERABLE'

targets['nonhero'] = 'NOT_HERO'
targets['air'] = 'AIR' #custom
targets['notself'] = 'NOTSELF' #custom
targets['dead'] = 'DEAD' #custom

targets['neutral'] = ''
targets['organic'] = ''
targets['vuln'] = ''
targets['self'] = ''
targets['player'] = ''
targets['debris'] = ''
targets['ward'] = ''
targets['item'] = ''
targets['ancient'] = ''
targets['alive'] = ''
targets['nonsapper'] = ''
targets['wall'] = ''
targets['bridge'] = ''


class wc3pars:
    def __init__(self, section):
        self.name = ''
        if 'Name' in section:
            self.name = section['Name']
        else:
            self.name = section['comments']

        if 'race' in section:
            self.race = section['race']

        self.code = None
        if 'code' in section:
            self.code = section['code']
        
        # BaseClass
        self.baseclass = 'ability_datadriven'

        # MaxLevel
        self.max_level = 1
        if 'levels' in section:
            if section['levels'] is not '-':
                self.max_level = section['levels']

        # AbilityBehavior, AbilityUnitTargetTeam and AbilityUnitTargetType
        self.behavior = ''
        self.unit_target_team = ''
        self.unit_target_type = ''
        if 'targs1' in section:
            targs1 = section['targs1']
            target_key = targs1.split(',')
            if 'ground' in target_key:
                if 'nonhero' not in target_key:
                    self.unit_target_type += 'DOTA_UNIT_TARGET_BASIC | DOTA_UNIT_TARGET_HERO'
                else:
                    self.unit_target_type += 'DOTA_UNIT_TARGET_BASIC'
            if 'structure' in target_key:
                if len(self.unit_target_type) > 0:
                    self.unit_target_type += ' | DOTA_UNIT_TARGET_BUILDING'
                else:
                    self.unit_target_type += 'DOTA_UNIT_TARGET_BUILDING'

            if 'tree' in target_key:
                if len(self.unit_target_type) > 0:
                    self.unit_target_type += ' | DOTA_UNIT_TARGET_TREE'
                else:
                    self.unit_target_type += 'DOTA_UNIT_TARGET_TREE'

            if 'mechanical' in target_key:
                if len(self.unit_target_type) > 0:
                    self.unit_target_type += ' | DOTA_UNIT_TARGET_MECHANICAL'
                else:
                    self.unit_target_type += 'DOTA_UNIT_TARGET_MECHANICAL'

            if '_' in target_key:
                self.behavior = targets['_']

            if 'Rng1' in section:
                if section['Rng1'] is '-':
                    if 'Cool1' in section:
                        if section['Cool1'] is '0' or section['Cool1'] is '-':
                            if 'Cost1' in section:
                                if section['Cost1'] is '' or section['Cost1'] is '0':
                                    self.behavior = 'DOTA_ABILITY_BEHAVIOR_PASSIVE'

            if 'enemy' in target_key:
                if 'ally' in target_key or 'friend' in target_key:
                    self.unit_target_team = 'DOTA_UNIT_TARGET_TEAM_BOTH'
                else:
                    self.unit_target_team = 'DOTA_UNIT_TARGET_TEAM_ENEMY'
            else:
                if 'ally' in target_key or 'friend' in target_key:
                    self.unit_target_team = 'DOTA_UNIT_TARGET_TEAM_FRIENDLY'

        #Defaults if nothing could be associated properly
        if self.behavior is '':
            self.behavior = 'DOTA_ABILITY_BEHAVIOR_UNIT_TARGET'
        if self.unit_target_team is '':
            self.unit_target_team = 'DOTA_UNIT_TARGET_TEAM_ENEMY'
        if self.unit_target_type is '':
            self.unit_target_type = 'DOTA_UNIT_TARGET_HERO | DOTA_UNIT_TARGET_BASIC'

        # AbilityUnitDamageType and AbilityCastAnimation are placeholders to change later
        self.unit_damage_type = 'DAMAGE_TYPE_MAGICAL'
        self.cast_animation = 'ACT_DOTA_CAST_ABILITY_2'

        # AbilityCastRange = Rng1
        self.cast_range = self.make4Loop(section, 'Rng')

        # AbilityCastPoint = Cast1
        self.cast_point = self.make4Loop(section, 'Cast')

        # AbilityCooldown = Cool1
        self.cooldown = self.make4Loop(section, 'Cool')

        # AbilityManaCost = Cost1
        self.mana_cost = self.make4Loop(section, 'Cost')

        # AbilityDuration = Dur1
        self.duration = self.make4Loop(section, 'Dur')

        # AOERadius = Area1
        self.aoe_radius = self.make4Loop(section, 'Area')

        # Ability Specials: A to I, from 1 to 4
        self.data = {}
        for l in 'ABCDEFGHI':
            self.data[l] = self.make4Loop(section, 'Data'+l)

        self.description = None
        if 'Ubertip' in section:
            self.description = section['Ubertip']

        self.comments = ''
        if 'comments' in section:
            self.comments = section['comments']

    def make4Loop(self, section, Keyword):
        string = ''
        for num in range(1,int(self.max_level)+1):
            if Keyword+str(num) in section:
                if section[Keyword+str(num)] is not '-':
                    if len(string)>0:
                        string = string+" "+section[Keyword+str(num)]
                    else:
                        string = section[Keyword+str(num)]
        return string        

    def check(self):
        print(self.npc_name)
        print(self.statushealthregen)
        print(self.statusmanaregen)

    def writetofile(self, nfile, write):
        newfile = open(nfile, write)
        lines = []
        section = ''
        lines.append(self.abilitycomment(self.name))
        lines.append(self.kline((self.race+"_"+self.name.replace(' ', '_').lower())))
        lines.append(self.kvline('BaseClass', self.baseclass,None))
        lines.append(self.kvline('AbilityTextureName', self.race+"_"+self.name.replace(' ', '_').lower(),None))
        lines.append(self.kvline('MaxLevel', self.max_level, None))

        lines.append(self.kvcomment(None))

        lines.append(self.kvline('AbilityBehavior', self.behavior,None))
        lines.append(self.kvline('AbilityUnitTargetTeam', self.unit_target_team,None))
        lines.append(self.kvline('AbilityUnitTargetType', self.unit_target_type,None))
        lines.append(self.kvline('AbilityUnitDamageType', self.unit_damage_type,None))
        lines.append(self.kvline('AbilityCastAnimation', self.cast_animation,None))

        lines.append(self.kvcomment(None))

        if self.cast_range is not '':
            lines.append(self.kvline('AbilityCastRange', self.cast_range,None))
        lines.append(self.kvline('AbilityCastPoint', self.cast_point,None))
        lines.append(self.kvline('AbilityCooldown', self.cooldown,None))
        if self.mana_cost is not '':
            lines.append(self.kvline('AbilityManaCost', self.mana_cost,None))

        lines.append(self.kvcomment(None))

        if self.aoe_radius is not '':
            lines.append(self.kvline('AOERadius', self.aoe_radius,None))

        abcounter = 0
        lines.append('\t'+'"AbilitySpecial"\n\t{\n')
        if self.duration is not '' and self.duration is not '0':
            abcounter += 1
            lines.append(self.kvspecial(abcounter, '', self.duration, 'duration'))
        if self.aoe_radius is not '' and self.aoe_radius is not '0':
            abcounter += 1
            lines.append(self.kvspecial(abcounter, '', self.aoe_radius, 'radius'))
        for i in self.data:
            if self.data[i] is not '' and self.data[i] is not '0' and self.data[i] is not '0 0 0':
                abcounter += 1
                lines.append(self.kvspecial(abcounter, i, self.data[i]))
        lines.append('\t}')

        lines.append('\n\n\t'+"//ToDo"+'\n\n')

        lines.append(endline)
        for line in lines:
            section += line
        newfile.write(section)

    def kvspecial(self, counter, letter, val, name='', ):
        line = ''
        field = '"FIELD_'
        hasDecimal = val.find('.')
        if val is not None:
            if hasDecimal is not -1:
                field += 'FLOAT"'
            else:
                field += 'INTEGER"'
            line += '\t\t'+'"0'+str(counter)+'"\n'
            line += '\t\t{\n'
            line += '\t\t\t'+'"var_type"'+'\t\t'+field+'\n'
            if name is not '':
                line += '\t\t\t"'+name+'"'+'\t\t"'+val+'"\n'
            elif letter is not '':
                line += '\t\t\t'+'"data'+letter+'"'+'\t\t\t"'+val+'"\n'
            line += '\t\t}\n'

        return line

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

    def kvcomment(self, comment):
        line =  '\t\t'
        if comment is not None:
            line += '//' + comment
        line += '\n'
        return line

    def abilitycomment(self, comment):
        line = '//=================================================================================\n'
        line += '// Ability: ' + comment +'\n'
        if self.description is not None:
            line += '// Description: ' + self.description + '\n'
        if self.code is not None:
            line += '// Code Reference: ' + self.code + '\n'
        line += '//=================================================================================\n'
        return line

    def kline(self, unit_name):
        line = '"'+ unit_name +'"\n' + '{\n'
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
    fullfile = sectionoff('abilities.txt')
    f = open('kv_abilities.txt','w')
    f.write('')
    for key in fullfile:
        if key is not '':
            afile = parse_text_section(fullfile[key])
            work = wc3pars(afile)
            work.writetofile('kv_abilities.txt', 'a')
    print('Finished Ability Parsing')
