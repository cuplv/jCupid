import java.lang.StringBuilder;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Scanner;

//import cute.Cute;

public class SumBytes
{
    //public static boolean isNumeric (String s)
    //{
        //try
        //{
            //double d= Double.parseDouble(s);
        //}
        //catch (NumberFormatException e)
        //{
            //return false;
        //}
        //return true;
    //}

    //public static String input(String [] args)
    //{
        //if (args.length == 0)
        //{
            //Object obj = Cute.input.Object("java.lang.String");
            //String s = obj.toString();
            //return s;
        //}
        //else
        //{
            
            //int ind = args[0].indexOf("(");
            //String input = args[0].substring(0,ind);

            //System.out.println("input = " + input);
            //if (input.equals("0"))
            //{
                //String s = null;
                //return s;
            //}
            //else if (isNumeric(input))
                //return new String();
            //else
                //return input;
        //}

    //}

    public static void main(String[] args)
    {
        Scanner sc = new Scanner(System.in);

        String s = sc.nextLine();
        
        
        //Object obj = Cute.input.Object("java.lang.String");
        //String s = obj.toString();
        //String s = input(args);
        byte[] bArray = s.getBytes();

        int sum = 0;
        for(int i= 0; i <  bArray.length;i++)
            sum += bArray[i];

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
        //if(bArray.length > 0 && bArray[0] == 10)
        //if(s.length() > 0)
        //{
            //System.out.println("s.substring(0,1) = " + s.substring(0,1));
            //System.out.println("s.substr == x? = " + s.substring(0,1).equals("x"));
        //}
        //if(s.length() > 0 && s.substring(0,1).equals("h"))
        {
            result = md.digest(bArray);
        }
        else
        {
            result = md.digest(md.digest(bArray));
        }
    }
}
