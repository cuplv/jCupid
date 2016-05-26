import java.util.Scanner;

public class PasswordCheckerFix3
{
    static String pass = "mySecretPassword";

    public static String getInput()
    {
        Scanner sc = new Scanner(System.in);

        String inp = sc.nextLine();

        return inp;

    }

    public static boolean checkPass(String pass, String inp)
    {
        boolean diff = true;
        diff &= pass.equals(inp);
        return diff;
    }

    public static void main(String [] args)
    {
        String inp = getInput();

        byte[] passBytes = pass.getBytes();
        byte[] inpBytes = inp.getBytes();

        boolean result = checkPass(pass,inp);

        System.out.println("result is: " + result);

    }
}
