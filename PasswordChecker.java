import java.util.Scanner;

public class PasswordChecker
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
        for (int i = 0; i < passBytes.length && i < inpBytes.length; i++)
        {
            if (passBytes[i] != inpBytes[i])
            {
                System.out.println("Passwords don't match!");
                return false;
            }
            else
            {
                System.out.println("byte is: " + passBytes[i]);
            }
        }

        return true;
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
