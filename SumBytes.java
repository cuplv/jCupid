import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Scanner;

public class SumBytes
{
    public static void main(String[] args)
    {
        Scanner sc = new Scanner(System.in);

        String s = sc.nextLine();

        byte[] bArray = s.getBytes();

        int sum = 0;
        for(int i: bArray)
            sum += i;

        MessageDigest md = null;

        try
        {
            md = MessageDigest.getInstance("SHA-1");
        }
        catch(NoSuchAlgorithmException e)
        {
            System.out.println(e);
        }

        byte[] result;
        if (sum < 500)
        {
            result = md.digest(bArray);
        }
        else
        {
            result = md.digest(md.digest(bArray));
        }
    }
}
