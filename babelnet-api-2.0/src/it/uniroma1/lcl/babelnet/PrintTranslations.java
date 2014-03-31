package it.uniroma1.lcl.babelnet;

import it.uniroma1.lcl.babelnet.iterators.*;
import it.uniroma1.lcl.jlt.util.Language;
import it.uniroma1.lcl.jlt.util.ScoredItem;

import java.io.IOException;
import java.util.*;

import com.google.common.collect.Multimap;

import edu.mit.jwi.item.IPointer;
import edu.mit.jwi.item.POS;

/**
 * A demo class to test {@link BabelNet}'s various features.
 * 
 * @author ponzetto
 */
public class PrintTranslations {
    /**
     * A demo to see the translations of a word.
     * 
     * @param lemma
     * @param languageToSearch
     * @param languagesToPrint
     * @throws IOException
     */
    public static void testTranslations(String lemma, Language languageToSearch,
                                        Language... languagesToPrint) throws IOException {
        BabelNet bn = BabelNet.getInstance();
        
        List<Language> allowedLanguages = Arrays.asList(languagesToPrint);
        Multimap<Language, ScoredItem<String>> translations =
            bn.getTranslations(languageToSearch, lemma);
        
        for (Language language : translations.keySet()) {
            if (allowedLanguages.contains(language)) {
                System.out.print(""+language);
                for (ScoredItem<String> item : translations.get(language)) {
                    System.out.print("\t"+item);
                }
                System.out.println();
            }
        }
    }
    
    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Please specify a word to look up on the command line.");
            return;
        }
        try
        {
            String word = args[1];
            Set<Language> languages = new HashSet<Language>();
            // = BabelNetConfiguration.getInstance().getBabelLanguages();

            languages.add(Language.ES);
            languages.add(Language.DE);
            languages.add(Language.EN);

            Language source;
            if (args[0].equals("en")) {
                source = Language.EN;
            } else if (args[0].equals("fr")) {
                source = Language.FR;
            } else if (args[0].equals("nl")) {
                source = Language.NL;
            } else {
                throw new Exception();
            }
            testTranslations(word, source, languages.toArray(new Language[languages.size()]));
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }
}
