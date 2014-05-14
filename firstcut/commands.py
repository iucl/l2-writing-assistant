import os

EN_MODE = "google"
#EN_MODE = "wiki"

here = os.path.dirname(os.path.realpath(__file__))
en_cmd_google = """
java -Xmx6G -Xms600M -cp HERE/../stanford/stanford-parser.jar edu.stanford.nlp.parser.lexparser.LexicalizedParser -writeOutputFiles -outputFilesExtension penn -tokenized -sentences newline -escaper edu.stanford.nlp.process.PTBEscapingProcessor -outputFormat penn -outputFormatOptions basicDependencies HERE/../stanford/models/englishPCFG.ser.gz {0}
java -Xmx6G -Xms600M -cp HERE/../stanford/stanford-parser.jar edu.stanford.nlp.trees.EnglishGrammaticalStructure -conllx -basic -treeFile {1}{2}.penn > {3}{4}.conll
"""
en_cmd_google = en_cmd_google.replace("HERE", here)


en_cmd_wiki = """
        java -Xmx6G -Xms600M -cp HERE/../stanford/stanford-parser.jar edu.stanford.nlp.parser.lexparser.LexicalizedParser -writeOutputFiles -outputFilesExtension penn -tokenized -sentences newline -escaper edu.stanford.nlp.process.PTBEscapingProcessor -outputFormat penn -outputFormatOptions CCPropagatedDependencies -maxLength 35 HERE/../stanford/models/englishPCFG.ser.gz {0}
        java -Xmx6G -Xms600M -cp HERE/../stanford/stanford-parser.jar edu.stanford.nlp.trees.EnglishGrammaticalStructure -conllx -CCprocessed -treeFile {1}{2}.penn > {3}{4}.conll"""
en_cmd_wiki = en_cmd_wiki.replace("HERE", here)

de_cmd = """
java -cp HERE/../mate/anna-3.3.jar is2.util.Split {0} > {1}.split

java -Xmx7G -Xms1G -cp HERE/../mate/anna-3.3.jar is2.lemmatizer.Lemmatizer -model HERE/../mate/german/lemma-ger-3.6.model -test {2}.split -out {3}.lema

java -Xmx7G -Xms1G -cp HERE/../mate/anna-3.3.jar is2.tag.Tagger -model HERE/../mate/german/tag-ger-3.6.model -test {4}.lema -out {5}.tag

java -classpath HERE/../mate/anna-3.3.jar is2.parser.Parser -model HERE/../mate/german/parser-ger-3.6.model -test {6}.tag -out {7}.conll
"""
de_cmd = de_cmd.replace("HERE", here)

#.format(PARPATH + filename,PARPATH + filename,\
# PARPATH + filename,PARPATH + filename, \
#PARPATH + filename,PARPATH + filename,\
#PARPATH + filename,PARPATH + filename,)

es_cmd = """
java -cp HERE/../mate/anna-3.3.jar is2.util.Split {0} > {1}.split

java -Xmx7G -Xms1G -cp HERE/../mate/anna-3.3.jar is2.lemmatizer.Lemmatizer -model HERE/../mate/spanish/lemma-spanish.model -test {2}.split -out {3}.lema

java -Xmx7G -Xms1G -cp HERE/../mate/anna-3.3.jar is2.tag.Tagger -model HERE/../mate/spanish/postag-spanish.model -test {4}.lema -out {5}.tag

java -Xmx7G -Xms1G -classpath HERE/../mate/anna-3.3.jar is2.parser.Parser -model HERE/../mate/spanish/parser-spanish.model -test {6}.tag -out {7}.conll

"""
es_cmd = es_cmd.replace("HERE", here)
