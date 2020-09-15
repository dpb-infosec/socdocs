import xml.etree.ElementTree as ET
import re
import base64
from jinja2 import Environment, FileSystemLoader
import os


RES_PATH = "./res"


class QRadarRule:

    def __init__(self):
        self.last_modified = ''
        self.origin = ''
        self.owner = ''
        self.name = ''
        self.notes = ''
        self.ruleText = ''
        self.buildingBlock = None
        self.enabled = None
        self.id = None

    def __str__(self):
        return """QRadarRule with state: \n - id=%s \n 
        - enabled=%s \n 
        - buildingBlock=%s \n 
        - owner=%s \n 
        - name=%s \n 
        - notes=%s \n 
        - ruleText=%s""" % (self.id, self.enabled, self.buildingBlock, self.owner, self.name, self.notes, self.ruleText)


filelist = [f for f in os.listdir(RES_PATH + "/rules") if f.endswith(".md")]
for f in filelist:
    os.remove(os.path.join(RES_PATH + "/rules", f))

filelist = [f for f in os.listdir(
    RES_PATH + "/building_blocks") if f.endswith(".md")]
for f in filelist:
    os.remove(os.path.join(RES_PATH + "/building_blocks", f))


tree = ET.parse('export.xml')
root = tree.getroot()
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

ruletemplate = env.get_template('rule.template')
buildingtemplate = env.get_template('buildingblock.template')

b64_rules = root.findall(".//custom_rule[origin='USER']") + \
    root.findall(".//custom_rule[origin='OVERRIDE']")

for b64_rule in b64_rules:

    rule = QRadarRule()
    rule.origin = b64_rule.findtext("origin")
    rule.last_modified = b64_rule.findtext("mod_date")

    rule_string = re.sub('&lt;.*?&gt;', '',
                         base64.b64decode(b64_rule.findtext('rule_data')).decode("utf-8"))                        
    rule_tree = ET.fromstring(rule_string)

    rule.name = rule_tree.find(".//name").text
    rule.owner = rule_tree.attrib.get("owner")
    rule.notes = rule_tree.find(".//notes").text
    rule.id = rule_tree.attrib.get("id")
    rule.buildingBlock = rule_tree.attrib.get("buildingBlock")
    rule.enabled = rule_tree.attrib.get("enabled")

    ruletext = ''
    tests = rule_tree.findall(".//test")

    for i, test in enumerate(tests):
        if i == 0:
            if test.attrib.get("negate") == "true":
                ruletext += "NOT "
            ruletext += test.findtext("text")

        else:
            if test.attrib.get("negate") == "true":
                ruletext += "\nAND NOT " + test.findtext("text")
            else:
                ruletext += "\nAND " + test.findtext("text")
    rule.ruleText = re.sub('&quot;','"',ruletext)  

    if rule.buildingBlock == "false":
        output = ruletemplate.render(rule=rule)
        rule_doc = open(RES_PATH + "/rules/" +
                        re.sub('/', '_', rule.name) + ".md", 'w')
        rule_doc.write(output)
        rule_doc.close()
    else:
        output = buildingtemplate.render(rule=rule)
        rule_doc = open(RES_PATH + "/building_blocks/" +
                        re.sub('/', '_', rule.name) + ".md", 'w')
        rule_doc.write(output)
        rule_doc.close()
