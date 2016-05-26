import java.util.Scanner;

public class PasswordCheckerFix2
{
    static String pass = "mySecretPassword";

    public static String getInput()
    {
        Scanner sc = new Scanner(System.in);

        String inp = sc.nextLine();

        return inp;

    }

    public static boolean checkPass(byte[] passBytes, byte[] inpBytes)
    {
        byte diff = 0;
        for (int i = 0; i < passBytes.length && i < inpBytes.length; i++)
        {
            diff |= (passBytes[i] ^ inpBytes[i]);
        }

        return diff==0;
    }

    public static void main(String [] args)
    {
        String inp = getInput();

        byte[] passBytes = pass.getBytes();
        byte[] inpBytes = inp.getBytes();

        boolean result = checkPass(passBytes,inpBytes);
        //boolean result = checkPass(pass,inp);

        System.out.println("result is: " + result);

    }
}
