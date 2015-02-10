# Warcraft 3 -> Dota 2 KV-Unit Parser

KVUP takes a file containing Warcraft III unit data and converts it to Dota 2 custom unit KeyValues.

## Usage

Step 1. Create a units.txt file by running the included [RMPQEx](http://www.rivsoft.net/projects/other/rmpqex/) over any Warcraft 3 map, using the Dump object data to [select the Unit data]. A default units file is included.

![img](http://puu.sh/fInYj/11d9d3b2c9.png)

Step 2. Go into a console and while in the same folder as the script and units file, run `python kvup.py`. [Get Python 3.3+ if you don't have it](https://www.python.org/downloads/)

![img](http://puu.sh/fIpm7/0a2c4e13fe.png)

Step 3. Open the generated kv_units.txt, search and copy any unit definitions necessary. In this file you will find both heroes and units with all their convertable values.

Step 4. Add Model, Ranged Projectile and change BaseClass if needed.
