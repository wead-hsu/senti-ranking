import java.io.BufferedInputStream;
import java.io.InputStreamReader;
import java.io.*;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map.Entry;
import java.util.Set;
import java.util.TreeSet;

public class ExtendSentiWords{
	
	public static void maini(String[] args) throws IOException {
		Word2VEC vec = new Word2VEC();
		vec.loadModel("/Users/wdxu/git/qa-demo/data/word2vec/lookup.bin");
		/*
		System.out.println("One word analysis");
	
		System.out.println("*******************************");
		System.out.println("Three word analysis");
		result = vec.analogy("中华民国", "中华人民共和国", "毛泽东");
		iter = result.iterator();
		while (iter.hasNext()) {
			Word2VEC.WordEntry word = (Word2VEC.WordEntry) iter.next();
			System.out.println(word.name + " " + word.score);
		}
		*/
	}

	public static void main(String[] args) throws IOException{
		
		Word2VEC vec = new Word2VEC();
		vec.loadModel("/Users/wdxu/git/qa-demo/data/word2vec/lookup.bin");
		System.out.println("One word analysis");
        try {
                String encoding="UTF-8";
                File infile = new File("../data/senti-words/mutals-and-adj");
				File outfile = new File("../data/senti-words/extend-mutals-and-adj");
				BufferedWriter output = new BufferedWriter(new FileWriter(outfile));
			
				InputStreamReader read = new InputStreamReader(new FileInputStream(infile),encoding);
                BufferedReader bufferedReader = new BufferedReader(read);
                String lineTxt = null;
                while((lineTxt = bufferedReader.readLine()) != null){
					String[] words = lineTxt.split("\t");
					System.out.print(words[0] + " ");
					output.write(words[0] + ' ');
					Set<Word2VEC.WordEntry> result = find_near(vec, words[0]);
					if( result != null){
						Iterator iter = result.iterator();
						while (iter.hasNext()) {
							Word2VEC.WordEntry word = (Word2VEC.WordEntry) iter.next();
							output.write(word.name + " " + word.score + "\t");
						}
					}
					output.write("\n");
				}
                read.close();

		} catch (Exception e) {
            System.out.println("读取文件内容出错");
            e.printStackTrace();
        }
		
	}

	public static Set<Word2VEC.WordEntry> find_near(Word2VEC vec, String org){
		Set<Word2VEC.WordEntry> result = new TreeSet<Word2VEC.WordEntry>();
		try{
			result = vec.distance(org);
			Iterator iter = result.iterator();
			if (iter.hasNext()) {
				Word2VEC.WordEntry word = (Word2VEC.WordEntry) iter.next();
				System.out.println(word.name + " " + word.score);
			}
			return result;
		} catch( Exception e){
			System.out.println("Not found");
			return null;
		}
	}

}
