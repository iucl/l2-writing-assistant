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
public class BabelNetDemo
{
	/**
	 * A demo to see the senses of a word.
	 * 
	 * @param lemma
	 * @param languageToSearch
	 * @param includeRedirections
	 * @param languagesToPrint
	 * @throws IOException
	 */
	public static void testDictionary(String lemma, Language languageToSearch,
			  						  boolean includeRedirections,
			  						  Language... languagesToPrint) throws IOException
	{
		BabelNet bn = BabelNet.getInstance();
		System.out.println("SENSES FOR \"" + lemma + "\"");
		List<BabelSense> senses =
			bn.getSenses(languageToSearch, lemma, POS.NOUN, includeRedirections);
		Collections.sort(senses, new BabelSenseComparator());
		for (BabelSense sense : senses)
			System.out.println("\t=>"+sense.getSenseString());
		System.out.println();
		System.out.println("SYNSETS WITH \"" + lemma + "\"");
		List<BabelSynset> synsets =
			bn.getSynsets(languageToSearch, lemma, POS.NOUN, includeRedirections);
		Collections.sort(synsets, new BabelSynsetComparator(lemma));
		for (BabelSynset synset : synsets)
			System.out.println(
					"\t=>(" +synset.getId() + 
					") SOURCE: " + synset.getSynsetSource() +
					") TYPE: " + synset.getSynsetType() +
					"; WN SYNSET: " + synset.getWordNetOffsets() +
					"; MAIN SENSE: " + synset.getMainSense() +
					"; SENSES: "+ synset.toString(languagesToPrint));
		System.out.println();
	}

	/**
	 * A demo to see the senses of a word.
	 * 
	 * @param lemma
	 * @param languageToSearch
	 * @param includeRedirections
	 * @throws IOException
	 */
	public static void testDictionary(String lemma, Language languageToSearch,
			  						  boolean includeRedirections,
			  						  BabelSenseSource... allowedSources) throws IOException
	{
		BabelNet bn = BabelNet.getInstance();
		System.out.println("SENSES FOR \"" + lemma + "\"");
		List<BabelSense> senses =
			bn.getSenses(languageToSearch, lemma, POS.NOUN, includeRedirections,
						 allowedSources);
		Collections.sort(senses, new BabelSenseComparator());
		for (BabelSense sense : senses)
			System.out.println("\t=>"+sense.getSenseString());
		System.out.println();
		System.out.println("SYNSETS WITH \"" + lemma + "\"");
		List<BabelSynset> synsets =
			bn.getSynsets(languageToSearch, lemma, POS.NOUN,
						  includeRedirections, allowedSources);
		Collections.sort(synsets, new BabelSynsetComparator(lemma));
		for (BabelSynset synset : synsets)
			System.out.println(
					"\t=>(" +synset.getId() + 
					") SOURCE: " + synset.getSynsetSource() +
					") TYPE: " + synset.getSynsetType() +
					"; WN SYNSET: " + synset.getWordNetOffsets() +
					"; MAIN SENSE: " + synset.getMainSense() +
					"; SENSES: "+ synset.toString());
		System.out.println();
	}
	
	/**
	 * A demo to explore the BabelNet graph.
	 * 
	 * @param id
	 * @throws IOException
	 */
	public static void testGraph(String id) throws IOException
	{
		BabelNet bn = BabelNet.getInstance();
		BabelSynset synset = bn.getSynsetFromId(id);
		
		testGraph(synset);		
	}

	/**
	 * A demo to explore the BabelNet graph.
	 * 
	 * @param lemma
	 * @param language
	 * @throws IOException
	 */
	public static void testGraph(String lemma, Language language) throws IOException
	{
		BabelNet bn = BabelNet.getInstance();
		List<BabelSynset> synsets = bn.getSynsets(language, lemma);
		Collections.sort(synsets, new BabelSynsetComparator(lemma));
		
		for (BabelSynset synset : synsets) testGraph(synset);
	}
	
	/**
	 * A demo to explore the BabelNet graph.
	 * 
	 * 
	 * @param synset
	 * @throws IOException
	 */
	public static void testGraph(BabelSynset synset) throws IOException
	{
		BabelNet bn = BabelNet.getInstance();
		List<BabelNetGraphEdge> successorsEdges = bn.getSuccessorEdges(synset.getId());

		System.out.println("SYNSET ID:" + synset.getId());
		System.out.println("# OUTGOING EDGES: " + successorsEdges.size());
		
		for (BabelNetGraphEdge edge : successorsEdges)
		{
			System.out.println("\tEDGE " + edge);
			System.out.println("\t" + bn.getSynsetFromId(edge.getTarget()).toString(Language.EN));
			System.out.println();
		}
	}
	
	/**
	 * A demo to see the translations of a word.
	 * 
	 * @param lemma
	 * @param languageToSearch
	 * @param languagesToPrint
	 * @throws IOException
	 */
	public static void testTranslations(String lemma, Language languageToSearch,
			  							Language... languagesToPrint) throws IOException
	{
		BabelNet bn = BabelNet.getInstance();
		
		List<Language> allowedLanguages = Arrays.asList(languagesToPrint);
		Multimap<Language, ScoredItem<String>> translations =
			bn.getTranslations(languageToSearch, lemma);
		
		System.out.println("TRANSLATIONS FOR " + lemma);
		for (Language language : translations.keySet())
		{
			if (allowedLanguages.contains(language))
				System.out.println("\t"+language+"=>"+translations.get(language)); 
		}
	}
	
	/**
	 * A demo to see the glosses of a {@link BabelSynset} given its id.
	 * 
	 * @param id
	 * @throws IOException
	 */
	public static void testGloss(String id) throws IOException
	{
		BabelNet bn = BabelNet.getInstance();
		BabelSynset synset = bn.getSynsetFromId(id);
		
		testGloss(synset);
	}
	
	/**
	 * 
	 * A demo to see the glosses of a word in a certain language
	 * 
	 * @param lemma
	 * @param language
	 * @throws IOException
	 */
	public static void testGloss(String lemma, Language language) throws IOException
	{
		BabelNet bn = BabelNet.getInstance();
		List<BabelSynset> synsets = bn.getSynsets(language, lemma);
		Collections.sort(synsets, new BabelSynsetComparator(lemma));
		
		for (BabelSynset synset : synsets) testGloss(synset);
	}

	/**
	 * A demo to see the glosses of a {@link BabelSynset}
	 * 
	 * @param synset
	 * @throws IOException
	 */
	public static void testGloss(BabelSynset synset) throws IOException
	{
		String id = synset.getId();
		BabelNet bn = BabelNet.getInstance();
		List<BabelGloss> glosses = bn.getGlosses(id);
		
		System.out.println("GLOSSES FOR SYNSET " + synset + " -- ID: " + id);
		for (BabelGloss gloss : glosses)
		{
			System.out.println(" * "+gloss.getLanguage()+" "+gloss.getSource()+" "+
							        gloss.getSourceSense()+"\n\t"+gloss.getGloss());
		}
		System.out.println();
	}
	
	public static void testImages(String lemma, Language language) throws IOException
	{
		BabelNet bn = BabelNet.getInstance();
		System.out.println("SYNSETS WITH word: \""+ lemma + "\"");
		List<BabelSynset> synsets = bn.getSynsets(language, lemma);
		Collections.sort(synsets, new BabelSynsetComparator(lemma));
		for (BabelSynset synset : synsets)
		{
			System.out.println("  =>(" + synset.getId() + ")" +
							 "  MAIN LEMMA: " + synset.getMainSense());
			for (BabelImage img : synset.getImages())
			{
				System.out.println("\tIMAGE URL:" + img.getURL());
				System.out.println("\tIMAGE VALIDATED URL:" + img.getValidatedURL());
				System.out.println("\t==");
			}
			System.out.println("  -----");
		}
	}
	
	/**
	 * The snippet contained in our WWW-12 demo paper
	 * 
	 */
	public static void www12Test() throws IOException
	{
		BabelNet bn = BabelNet.getInstance();
		System.out.println("SYNSETS WITH English word: \"bank\"");
		List<BabelSynset> synsets = bn.getSynsets(Language.EN, "bank");
		Collections.sort(synsets, new BabelSynsetComparator("bank"));
		for (BabelSynset synset : synsets)
		{
			System.out.print("  =>(" + synset.getId() + ") SOURCE: " + synset.getSynsetSource() +
							 "; TYPE: " + synset.getSynsetType() + 
							 "; WN SYNSET: " + synset.getWordNetOffsets() + ";\n" +
							 "  MAIN LEMMA: " + synset.getMainSense() + 
							 ";\n  IMAGES: " + synset.getImages() + 
							 ";\n  CATEGORIES: " + synset.getCategories() + 
							 ";\n  SENSES (German): { ");
			for (BabelSense sense : synset.getSenses(Language.DE))
				System.out.print(sense.toString()+" ");
			System.out.println("}\n  -----");
			Map<IPointer, List<BabelSynset>> relatedSynsets = synset.getRelatedMap(); 
			for (IPointer relationType : relatedSynsets.keySet())
			{
				List<BabelSynset> relationSynsets = relatedSynsets.get(relationType);
				for (BabelSynset relationSynset : relationSynsets)
				{
					System.out.println("    EDGE " + relationType.getSymbol() +
									   " " + relationSynset.getId() +
									   " " + relationSynset.toString(Language.EN));
				}
			}
			System.out.println("  -----");
		}
	}
	
	/**
	 * A demo to test iterators.
	 * 
	 * @param iterator
	 */
	public static <T> void testIterator(BabelIterator<T> iterator)
	{
		int counter = 0;
		while (iterator.hasNext())
		{
			System.out.println(counter+". "+iterator.next().toString());
			counter++;
		}
	}
	
	/**
	 * Just for testing
	 * 
	 * @param args
	 * 
	 */
	static public void main(String[] args)
	{
		try
		{
			// UNCOMMENT TO TEST THE WWW-12 SNIPPET
			www12Test();
			
			// UNCOMMENT TO TEST THE IMAGES
//			testImages("balloon", Language.EN);
			
			// UNCOMMENT TO TEST THE ITERATORS
//			BabelNet bn = BabelNet.getInstance();
//			testIterator(bn.getOffsetIterator());
//			testIterator(bn.getSynsetIterator());
//			testIterator(bn.getLexiconIterator());
			
			// UNCOMMENT TO TEST THE LEXICON
//			System.out.println("===============TESTING BABELNET DICT===============\n");
//			for (String test : new String[] {
//					"bank",
//					"house",
//					"car",
//					"account"
//			}) testDictionary(test, Language.EN, false, Language.IT);
//			System.out.println("=====================DONE=====================");

			// UNCOMMENT TO TEST THE GRAPH
//			System.out.println("===============TESTING BABELNET GRAPH===============\n");
//			testGraph("bank", Language.EN);
//			testGraph("bn:00000010n");
//			System.out.println("=====================DONE=====================");

			// UNCOMMENT TO TEST THE TRANSLATIONS
//			System.out.println("===============TESTING BABELNET TRANSLATIONS===============\n");
//			Set<Language> languages = BabelNetConfiguration.getInstance().getBabelLanguages();
//			languages.add(Language.EN);
//			testTranslations("apple", Language.EN, languages.toArray(new Language[languages.size()]));
//			System.out.println("=====================DONE=====================");
			
			// UNCOMMENT TO TEST THE GLOSSES
//			System.out.println("===============TESTING BABELNET GLOSSES===============\n");
//			testGloss("play", Language.EN);
//			testGloss("bn:00000010n");
//			System.out.println("=====================DONE=====================");
			
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}
}
