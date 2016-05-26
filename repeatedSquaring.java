import java.lang.Long;
import java.lang.Math;
import java.util.Scanner;

public class repeatedSquaring
{
    public static long stringToLong(String str,int base)
    {
        long ans = 0;

        for(int i = 0; i < str.length(); i++)
            ans += (long) ((int)(str.charAt(i)-32))*Math.pow(base,i);

        return ans;
    }

    public static int repeatedSquare(int base, long power, int mod)
    {
        int R = 1;

        if (power == 0)
            return 0;
        else if (power == 1)
            return base;

        while (power != 0)
        {
            if (power %2 == 1)
                R = R*base % mod;

            base = base*base % mod;
            power/= 2;
        }

        return R;
    }

    public static void main(String [] args)
    {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine();

        long num = stringToLong(s,100);

        int prime = 2357;
        //int prime = 5;
        int g = 1415;
        //int g = 2;

        int res = repeatedSquare(g,num,prime);

        System.out.println("res = " + res);
    }
}
