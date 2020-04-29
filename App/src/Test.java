import java.util.ArrayList;
import java.util.Scanner;

public class Test {
    public static void main(String[] args) {
        Main m = new Main();
//        String result = m.translate("3.1415927");
        Scanner in = new Scanner(System.in);
        while(true) {
            System.out.println("Enter the number: ");
            String input = in.nextLine();
            m.translate(input);
            String result = m.getResult();
            System.out.println("The split number is: " + m.getNumbers().toString());
            System.out.println("The word list is: " +  m.getWords().toString());
            ArrayList<ArrayList<String>> wordSet = m.getWords();
//            System.out.println(wordSet.size());
            System.out.println();
//            System.out.println(wordSet.get(0).getClass());
//            System.out.println(wordSet.get(0));
            System.out.println("Get result once: " + result);
            String r1 = m.getResult();
            System.out.println("Get result again: " + r1);
        }

    }
}
