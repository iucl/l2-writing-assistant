EN_MODE = "google"
#EN_MODE = "wiki"

en_cmd_google = """
java -Xmx6G -Xms600M -cp ../stanford/stanford-parser.jar edu.stanford.nlp.parser.lexparser.LexicalizedParser -writeOutputFiles -outputFilesExtension penn -tokenized -sentences newline -escaper edu.stanford.nlp.process.PTBEscapingProcessor -outputFormat penn -outputFormatOptions basicDependencies ../stanford/models/englishPCFG.ser.gz {0}
java -Xmx6G -Xms600M -cp ../stanford/stanford-parser.jar edu.stanford.nlp.trees.EnglishGrammaticalStructure -conllx -basic -treeFile {1}{2}.penn > {3}{4}.conll
"""


en_cmd_wiki = """
        java -Xmx6G -Xms600M -cp ../stanford/stanford-parser.jar edu.stanford.nlp.parser.lexparser.LexicalizedParser -writeOutputFiles -outputFilesExtension penn -tokenized -sentences newline -escaper edu.stanford.nlp.process.PTBEscapingProcessor -outputFormat penn -outputFormatOptions CCPropagatedDependencies -maxLength 35 ../stanford/models/englishPCFG.ser.gz {0}
        java -Xmx6G -Xms600M -cp ../stanford/stanford-parser.jar edu.stanford.nlp.trees.EnglishGrammaticalStructure -conllx -CCprocessed -treeFile {1}{2}.penn > {3}{4}.conll"""

de_cmd = """
java -cp ../mate/anna-3.3.jar is2.util.Split {0} > {1}.split

java -Xmx7G -Xms1G -cp ../mate/anna-3.3.jar is2.lemmatizer.Lemmatizer -model ../mate/german/lemma-ger-3.6.model -test {2}.split -out {3}.lema

java -Xmx7G -Xms1G -cp ../mate/anna-3.3.jar is2.tag.Tagger -model ../mate/german/tag-ger-3.6.model -test {4}.lema -out {5}.tag

java -classpath ../mate/anna-3.3.jar is2.parser.Parser -model ../mate/german/parser-ger-3.6.model -test {6}.tag -out {7}.conll
"""

#.format(PARPATH + filename,PARPATH + filename,\
# PARPATH + filename,PARPATH + filename, \
#PARPATH + filename,PARPATH + filename,\
#PARPATH + filename,PARPATH + filename,)

es_cmd = """
java -cp ../mate/anna-3.3.jar is2.util.Split {0} > {1}.split

java -Xmx7G -Xms1G -cp ../mate/anna-3.3.jar is2.lemmatizer.Lemmatizer -model ../mate/spanish/lemma-spanish.model -test {2}.split -out {3}.lema

java -Xmx7G -Xms1G -cp ../mate/anna-3.3.jar is2.tag.Tagger -model ../mate/spanish/postag-spanish.model -test {4}.lema -out {5}.tag

java -Xmx7G -Xms1G -classpath ../mate/anna-3.3.jar is2.parser.Parser -model ../mate/spanish/parser-spanish.model -test {6}.tag -out {7}.conll

"""










