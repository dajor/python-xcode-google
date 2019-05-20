import re
import requests
import os
from google.cloud import translate


translate_client = translate.Client()

translateAPI = "https://www.googleapis.com/language/translate/v2?key=ya29.c.EloOB_lJCN5tAneAm4meLkB-zLLMTcK9Oeen31lo3DeOnoVmf_wjfF0MwDtTYutNoQpOgEU3b-Ri8hbsMoeGyOP6Cipvg9VoRkqb8sWNqOtu7QyWaPNG518JSMQ"

def createDirectoryIfNotExists(fileName):
    if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))

def writeToFile(sourceText, translatedText, target):
    fileName = "output/" + target + ".lproj/Localizable.strings"
    with open(fileName, "a") as myfile:
       createDirectoryIfNotExists(fileName)
       contentToWrite = "\"" + sourceText + "\" = \"" + translatedText + "\";\n"
       myfile.write(contentToWrite)

def translateSourceText(sourceText, target):
    translation = translate_client.translate(sourceText,target_language=target)
    return translation['translatedText']
    #url = translateAPI + "&q=" + sourceText + "&source=en&target=" + target
    #r = requests.get(url)
    #jsonObject = jsonObject = r.json()
    #return jsonObject['data']['translations'][0]['translatedText'].encode('utf-8')

def translateLineInFile(line, target, outputTarget):
    matchSource = re.search(r'\"(.*)\"(.*)\"(.*)\"', line)
    if matchSource:
        stringName = matchSource.group(1)
        sourceText = matchSource.group(3)
        translation = translateSourceText(sourceText, target)
        writeToFile(stringName, translation, outputTarget)

def clearContentsOfFile(target):
    fileName = "output/" + target + ".lproj/Localizable.strings"
    createDirectoryIfNotExists(fileName)
    open(fileName, 'w').close()

def translateFile(translateName, target, outputTarget):

    print("Translating for: " + translateName)

    clearContentsOfFile(outputTarget)

    with open('Localizable.strings', 'r') as stringsFile:
        for line in stringsFile:
            translateLineInFile(line, translateTarget, outputTarget)


with open('Google_IOS_Country_Codes.txt', 'r') as targetsFile:
    for targetLine in targetsFile:

        if "#" in targetLine:
            continue

        targetArray = targetLine.split()

        translateName = targetArray[0]
        translateTarget = targetArray[1]
        outputTarget = targetArray[2]

        translateFile(translateName, translateTarget, outputTarget)


