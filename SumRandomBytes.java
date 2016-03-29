import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Scanner;

public class SumRandomBytes
{
    public static int sumString(String s)
    {
        byte[] bArray = s.getBytes();
        int sum = 0;
        for (int i: bArray)
            sum += i;

        return sum;
    }

    public static byte[] readBytes(int n) throws FileNotFoundException, IOException
    {
        FileInputStream in = new FileInputStream("/dev/random");
        byte[] d = new byte[n];
        in.read(d);

        return d;
    }

    public static void main(String[] args)
    {
        Scanner sc = new Scanner(System.in);

        String s = sc.nextLine();
        
        int sumOfBytes = sumString(s);

        byte[] data = new byte[sumOfBytes];
        try
        {
            data = readBytes(sumOfBytes);
        }
        catch (FileNotFoundException e)
        {
            System.out.println(e);
            System.exit(1);
        }
        catch(IOException e)
        {
            System.out.println(e);
            System.exit(2);
        }
        // at this point data is full of random stuff, so now hash it!
        
        try 
        {
            MessageDigest md = MessageDigest.getInstance("SHA-1");
            md.digest(data);
        }
        catch(NoSuchAlgorithmException e)
        {
            System.out.println(e);
            System.exit(3);
        }
        
    }
}
