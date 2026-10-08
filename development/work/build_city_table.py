from pathlib import Path
import xml.etree.ElementTree as ET
from luaparser import ast

ROOT=Path(__file__).resolve().parents[1]
runtime=(ROOT/'work/arkham_city_runtime.lua').read_text(encoding='utf-8')
ast.parse(runtime)
table=ET.Element('CheatTable',CheatEngineTableVersion='45')
entries=ET.SubElement(table,'CheatEntries')
def node(parent,id,title,script=None,group=False,key=None):
    e=ET.SubElement(parent,'CheatEntry');ET.SubElement(e,'ID').text=str(id);ET.SubElement(e,'Description').text='"'+title+'"'
    if group:ET.SubElement(e,'Options',moHideChildren='1');ET.SubElement(e,'GroupHeader').text='1'
    if script:
        ET.SubElement(e,'VariableType').text='Auto Assembler Script';ET.SubElement(e,'AssemblerScript').text=script
    if key:
        hot=ET.SubElement(ET.SubElement(e,'Hotkeys'),'Hotkey');ET.SubElement(hot,'Action').text='Toggle Activation';ET.SubElement(ET.SubElement(hot,'Keys'),'Key').text=str(key);ET.SubElement(hot,'ID').text='0'
    return e
def flag(parent,id,title,name,key=None,other=None):
    extra=''
    if other:extra=f"local m=getAddressList().getMemoryRecordByID({other});if m and m.Active then m.Active=false end\n"
    enable="if not AC then error('Enable Initialize Arkham City Table first.') end\n"+extra+f"AC.setFlag('{name}',true)"
    disable=f"if AC then AC.setFlag('{name}',false) end"
    script=f'[ENABLE]\n{{$lua}}\nif syntaxcheck then return end\n{enable}\n{{$asm}}\n[DISABLE]\n{{$lua}}\nif syntaxcheck then return end\n{disable}\n{{$asm}}'
    return node(parent,id,title,script,key=key)
def action(parent,id,title,fn,key=None):
    script=f"[ENABLE]\n{{$lua}}\nif syntaxcheck then return end\nif not AC then error('Enable Initialize Arkham City Table first.') end\nAC.action(memrec,function() {fn} end)\n{{$asm}}\n[DISABLE]"
    return node(parent,id,title,script,key=key)
root=node(entries,1,'[Required] Initialize Arkham City GOTY Table',f'[ENABLE]\n{{$lua}}\nif syntaxcheck then return end\n{runtime}\n{{$asm}}\n[DISABLE]\n{{$lua}}\nif syntaxcheck then return end\nif AC and AC.shutdown then AC.shutdown() end\nAC=nil\n{{$asm}}')
ET.SubElement(root,'Options',moHideChildren='1',moDeactivateChildrenAsWell='1');ET.SubElement(root,'Color').text='008000'
children=ET.SubElement(root,'CheatEntries')
status=node(children,2,'Runtime Status (read-only; no popup)')
ET.SubElement(status,'VariableType').text='String';ET.SubElement(status,'Length').text='500';ET.SubElement(status,'Unicode').text='0';ET.SubElement(status,'Address').text='AC_RuntimeStatus'
def group(id,title):return ET.SubElement(node(children,id,title,group=True),'CheatEntries')
survival=group(10,'Player / Survival (Batman and DLC Characters)')
flag(survival,11,'Infinite Health','health')
combat=group(20,'Enemies / Combat')
flag(combat,21,'Freeze Enemies (AI / Movement; animations preserved) [Test]','freeze')
flag(combat,22,'Super Damage (10x-equivalent + Batarang KO) [-] [Test]','superDamage',189,23)
flag(combat,23,'One-Hit Knockout (Melee + Batarangs) [=] [Test]','oneHit',187,22)
reach=group(30,'Gadgets / Reach')
flag(reach,31,'Extra-Long Grapple Distance [Test]','grappleRange')
flag(reach,32,'Extra-Long Batarang Distance [Test]','batarangRange')
missions=group(70,'Side Missions / Phone Races')
flag(missions,71,'Zsasz Phone Race Countdown = 59 Seconds [Test]','phoneTimer')
challenge=group(50,'Challenge Modes [Require Gameplay Testing]')
flag(challenge,51,'Combat Challenge HUD Score = Target [Test]','score')
target=node(challenge,52,'Challenge Score Target');ET.SubElement(target,'VariableType').text='4 Bytes';ET.SubElement(target,'Address').text='AC_ChallengeScoreTarget'
flag(challenge,53,'Pause Challenge / Modifier Countdown Timer [Test]','challengeTimer')
action(challenge,54,'Reset Challenge Timer (countdown refills; count-up resets) [Test]','AC.resetChallenge()')
flag(challenge,55,'Freeze Predator Challenge Timer [Test]','predatorTimer')
action(challenge,56,'Reset Predator Challenge Timer to 0 [Test]','AC.resetPredator()')
teleport=group(60,'Positions / Teleport (same character session only)')
action(teleport,61,'Save Position [J]','AC.save()',74)
action(teleport,62,'Teleport to Saved Position [K]','AC.teleport()',75)
action(teleport,63,'Undo / Redo Last Teleport [L]','AC.undoTeleport()',76)
for i,n in enumerate([1,2,5,10]):action(teleport,64+i,f'Teleport Up {n} Body Height(s) [F{i+1}]',f'AC.up({n})',112+i)
ET.SubElement(table,'UserdefinedSymbols')
ET.SubElement(table,'Comments').text='Original v6 release for Steam Batman Arkham City GOTY. Removes Gameplay / Time, story play-time freeze, 1.5x speed, and 0.5x slow motion, including their runtime logic. Retains the dedicated Zsasz phone-race countdown hold at 59 seconds and separate challenge-mode scripts. User reports v5 phone timer at 58-59 seconds and one-shot Batarang results; independent timer-disable and gadget-variant tests remain. Phone offsets/masks are validated on activation; only the active race-linked countdown is held. Damage KO bit restores when both damage modes are off. Core health/combat/range/position behavior unchanged. Armor Full remains removed. No output popups or console edits. Disable old initializer before loading so any old speed modification is restored. Back up saves. Disable combat modifiers for scripted bosses/interrogations. Teleports do not stream maps or check walls; L undoes, J resaves. Challenge score remains an unverified HUD-field test. Applied HP reductions persist until enemies respawn. Other gadgets are not claimed supported. Hotkeys J/K/L; F1-F4; main keyboard -/=. No armor, fly, combo, XP, upgrade-point, waypoint or scan/story-flag cheats.'
ET.indent(table,space='  ')
out=ROOT/'outputs/Batman Arkham City GOTY - Original v6.CT'
ET.ElementTree(table).write(out,encoding='utf-8',xml_declaration=True)
parsed=ET.parse(out)
ids=[e.text for e in parsed.findall('.//CheatEntry/ID')];assert len(ids)==len(set(ids))
assert not {'40','41','42','43'} & set(ids), 'Removed Gameplay / Time entries must stay absent'
assert {'53','54','55','56','71'} <= set(ids), 'Keep challenge timers and the separate phone-race toggle'
assert all(text not in runtime for text in ['C.flags.storyTimer','C.flags.fast','C.flags.slow',"C.remember('speed'"]), 'Removed time/speed runtime must stay absent'
for e in parsed.findall('.//AssemblerScript'):
    for block in e.text.split('{$lua}')[1:]:ast.parse(block.split('{$asm}')[0])
print(out);print('Unique records:',len(ids),'Lua syntax valid')
