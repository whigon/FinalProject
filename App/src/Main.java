import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Set;

public class Main {
    // Set of numbers
    private Set<String> keySet;
    // Map of the number and words
    private JSONObject map;
    // This array is used to store the numbers that are split from a digit
    private ArrayList<String> numbers;
    // This array is used to store words corresponding to the number
    private ArrayList<JSONArray> words;

    /**
     * Constructor: load the data file.
     */
    public Main() {
        loadFile();
    }

    /**
     * Translate digits into a set of words.
     *
     * @param digits input
     * @return a set of words
     */
    public String translate(String digits) {
        // New a space
        numbers = new ArrayList<>();
        words = new ArrayList<>();

        splitNumber(digits);

        return getResult();
    }

    /**
     * Randomly generate a set of words according to numbers.
     *
     * @return a set of words
     */
    public String getResult() {
        String str = " ";

        for (int i = 0; i < words.size(); i++) {
            str += randomlyPick(words.get(i)) + " ";
        }

        return str;
    }

    /**
     * Split digits into numbers and store the corresponding words.
     *
     * @param input digits
     */
    private void splitNumber(String input) {
        int length = input.length();
        String subNumber;

        if (length != 0) {
            // Check from the longest substring
            for (int i = length; i > 0; i--) {
                subNumber = input.substring(0, i);

                if (isExist(subNumber)) {
                    // Store split-number
                    numbers.add(subNumber);
                    // Store corresponding words
                    words.add((JSONArray) (map.get(subNumber)));
                    // Find next
                    splitNumber(input.substring(i));

                    break;
                }
            }
        }
    }


    /**
     * Randomly pick a word from a set of words.
     * Some numbers can be represented by more than one word.
     *
     * @param array A set of words that can represent a number
     * @return A randomly-picked word
     */
    public String randomlyPick(JSONArray array) {
        int random = (int) (Math.random() * array.size());
//        System.out.println(array);
//        System.out.println(random);

        return array.getString(random);
    }

    /**
     * Check whether a number can be represented by a word.
     *
     * @param number A sub-string of digits
     * @return True or False
     */
    private boolean isExist(String number) {
        return keySet.contains(number);
    }

    /**
     * Return the set of numbers.
     * Each number is the longest substring of the input digits, which can be represented by at least one word
     *
     * @return A set of numbers
     */
    public ArrayList<String> getNumbers() {
        return numbers;
    }

    /**
     * Return the set of words that can be used to represented numbers
     *
     * @return A set of JsonArray which contains the words
     */
    public ArrayList<JSONArray> getWords() {
        return words;
    }

    /**
     * Load the data file.
     */
    private void loadFile() {
        // Get file path
        File file = new File(System.getProperty("user.dir"));
        String parent = file.getParent();
        System.out.println(file);

        try {
            // Read from file
            BufferedReader reader = new BufferedReader(new FileReader(new File(parent + "/Resources/test_data.json")));

            String data = "";
            String str;
            while ((str = reader.readLine()) != null) {
                data += str;
            }

            // Store the map
            map = (JSONObject) JSON.parse(data);
            // Store the key set
            keySet = map.keySet();
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}
