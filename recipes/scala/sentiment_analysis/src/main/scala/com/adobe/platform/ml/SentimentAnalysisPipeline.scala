/*
 *  Copyright 2017 Adobe.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *          http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
package com.adobe.platform.ml

import com.adobe.platform.ml.config.ConfigProperties
import com.adobe.platform.ml.sdk.PipelineFactory
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.feature._
import org.apache.spark.ml.param.ParamMap
import org.apache.spark.sql.SparkSession

/**
  * Main Pipeline configuration class that outlines the logistic regression pipeline stages
  */
class SentimentAnalysisPipeline extends PipelineFactory {

 /*   val stopWords = Array("a", "able", "about", "above", "abst", "accordance", "according",
      "accordingly", "across", "act", "actually", "added", "adj", "affected", "affecting", "affects",
      "after", "afterwards", "again", "against", "ah", "all", "almost", "alone", "along", "already",
      "also", "although", "always", "am", "among", "amongst", "an", "and", "announce", "another",
      "any","anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere",
      "apparently", "approximately", "are", "aren", "arent", "arise", "around", "as", "aside",
      "ask", "asking", "at", "auth", "available", "away", "awfully", "b", "back", "be", "became",
      "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin",
      "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides",
      "between", "beyond", "biol", "both", "brief", "briefly", "but","by", "c", "ca", "came", "can",
      "cannot", "can't", "cause", "causes", "certain", "certainly", "co", "com", "come", "comes",
      "contain", "containing", "contains", "could", "couldnt", "d", "date", "did", "didn't",
      "different", "do", "does", "doesn't", "doing", "done", "don't", "down", "downwards","due",
      "during", "e", "each", "ed", "edu", "effect", "eg", "eight", "eighty", "either", "else",
      "elsewhere", "end", "ending", "enough", "especially", "et", "et-al", "etc", "even", "ever", "every",
      "everybody", "everyone", "everything", "everywhere", "ex", "except", "f", "far", "few", "ff",
      "fifth", "first", "five", "fix", "followed", "following", "follows", "for", "former", "formerly",
      "forth", "found", "four", "from", "further", "furthermore", "g", "gave", "get", "gets", "getting",
      "give", "given", "gives", "giving", "go", "goes", "gone", "got", "gotten", "h", "had", "happens",
      "hardly", "has", "hasn't", "have", "haven't", "having", "he", "hed", "hence", "her", "here", "hereafter",
      "hereby", "herein", "heres", "hereupon", "hers", "herself", "hes", "hi", "hid", "him", "himself", "his",
      "hither", "home", "how", "howbeit", "however", "hundred", "i", "id", "ie", "if", "i'll", "im", "immediate",
      "immediately", "importance", "important", "in", "inc", "indeed", "index", "information", "instead",
      "into", "invention", "inward", "is", "isn't", "it", "itd", "it'll", "its", "itself", "i've", "j",
      "just", "k", "keep", "keeps", "kept", "kg", "km", "know", "known", "knows", "l", "largely", "last",
      "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked",
      "likely", "line", "little", "'ll", "look", "looking", "looks", "ltd", "m", "made", "mainly",
      "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely",
      "mg", "might", "million", "miss", "ml", "more", "moreover", "most", "mostly", "mr", "mrs", "much",
      "mug", "must", "my", "myself", "n", "na", "name", "namely", "nay", "nd", "near", "nearly", "necessarily",
      "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine", "ninety", "no",
      "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing",
      "now", "nowhere", "o", "obtain", "obtained", "obviously", "of", "off", "often", "oh", "ok", "okay",
      "old", "omitted", "on", "once", "one", "ones", "only", "onto", "or", "ord", "other", "others",
      "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "owing",
      "own", "p", "page", "pages", "part", "particular", "particularly", "past", "per", "perhaps",
      "placed", "please", "plus", "poorly", "possible", "possibly", "potentially", "pp", "predominantly",
      "present", "previously", "primarily", "probably", "promptly", "proud", "provides", "put", "q", "que",
      "quickly", "quite", "qv", "r", "ran", "rather", "rd", "re", "readily", "really", "recent", "recently",
      "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "respectively",
      "resulted", "resulting", "results", "right", "run", "s", "said", "same", "saw", "say", "saying", "says",
      "sec", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves",
      "sent", "seven", "several", "shall", "she", "shed", "she'll", "shes", "should", "shouldn't", "show",
      "showed", "shown", "showns", "shows", "significant", "significantly", "similar", "similarly", "since",
      "six", "slightly", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime",
      "sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically", "specified", "specify", "specifying",
      "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest",
      "sup", "sure", "t's", "take", "taken", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that",
      "that's", "thats", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "there's",
      "thereafter", "thereby", "therefore", "therein", "theres", "thereupon", "these", "they", "they'd",
      "they'll", "they're", "they've", "think", "third", "this", "thorough", "thoroughly", "those", "though",
      "three", "through", "throughout", "thru", "thus", "to", "together", "too", "took", "toward", "towards",
      "tried", "tries", "truly", "try", "trying", "twice", "two", "un", "under", "unfortunately", "unless",
      "unlikely", "until", "unto", "up", "upon", "us", "use", "used", "useful", "uses", "using", "usually",
      "value", "various", "very", "via", "viz", "vs", "want", "wants", "was", "wasn't", "way", "we", "we'd",
      "we'll", "we're", "we've", "welcome", "well", "went", "were", "weren't", "what", "what's", "whatever",
      "when", "whence", "whenever", "where", "where's", "whereafter", "whereas", "whereby", "wherein",
      "whereupon", "wherever", "whether", "which", "while", "whither", "who", "who's", "whoever", "whole",
      "whom", "whose", "why", "will", "willing", "wish", "with", "within", "without", "won't", "wonder",
      "would", "wouldn't", "yes", "yet", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
      "yourself", "yourselves", "zero", "template", "align", "center", "cite", "style", "left", "web",
      "flagicon", "references", "rowspan", "width", "infobox", "colspan", "class", "time", "external",
      "links", "background", "reflist", "area", "bgcolor", "wikitable", "top", "http", "reflisttemplate",
      "including", "list", "main", "icon", "coord", "title", "webtemplate", "border", "website", "row",
      "include", "site", "col", "set", "large", "san", "valign", "color", "sort", "halign", "align",
      "dfdddf", "dfbbbf", "persondatadefaultsort", "rt"
    ) */

    /**
      * Implementation of pipeline factory to configure the pipeline with
      * three stages - tokenizer, stop words remover, countvectorizer, LogisticRegression
      * @param configProperties Properties map from the pipeline.json
      * @return
      */
    override def apply(configProperties: ConfigProperties) = {
      // Configure an ML pipeline, which consists of three stages: tokenizer, hashingTf, LogisticRegression
      val maxIter: Int = configProperties.get("maxIter").get.toInt
      val regParam: Double = configProperties.get("regParam").get.toDouble
      val numFeatures: Int  = configProperties.get("numFeatures").get.toInt


      val tokenizer = new RegexTokenizer()
        .setGaps(false)
        .setPattern("\\p{L}+")
        .setInputCol("text")
        .setOutputCol("words")

     // Leaving the filterer and countVectorizer intact as commented if someone wants to enable it later
     /* val filterer = new StopWordsRemover()
        .setStopWords(stopWords)
        .setCaseSensitive(false)
        .setInputCol("words")
        .setOutputCol("filtered")*/

      val tf = new HashingTF()
        .setInputCol("words")
        .setOutputCol("features")

     /* val countVectorizer = new CountVectorizer()
        .setInputCol("filtered")
        .setOutputCol("features")*/

      val lr = new LogisticRegression()
        .setMaxIter(maxIter)
        .setRegParam(regParam)
        .setElasticNetParam(0.0)

      val pipeline = new Pipeline()
        .setStages(Array(tokenizer, tf, lr))

      pipeline
    }

  /***
    * Ability to add paramMap just before calling transform for your pipeline
    * @param configProperties
    * @param sparkSession
    * @return
    */
    override def getParamMap(configProperties: ConfigProperties, sparkSession: SparkSession) = {
      val map = new ParamMap()
      map
    }
}
