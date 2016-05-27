import java.lang.Integer;
import java.lang.Long;
import java.lang.Math;
import java.math.BigInteger;
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

    public static BigInteger stringToBigInt(String str,int base)
    {
        BigInteger ans = new BigInteger("0");

        for(int i = 0; i < str.length(); i++)
        {
            BigInteger ch = new BigInteger(Integer.toString((int)(str.charAt(i)-32)));
            BigInteger power = new BigInteger(Integer.toString(base));
            power = power.pow(i);
            ans = ans.add(ch.multiply(power));
        }

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

    public static BigInteger BigRepeatedSquare(BigInteger base, BigInteger power, BigInteger mod)
    {
        BigInteger R = new BigInteger("1");
        BigInteger two = new BigInteger("2");

        //System.out.println("intial power = " + power);
        if (power.compareTo(BigInteger.ZERO) == 0)
            return BigInteger.ONE;
        else if (power.compareTo(BigInteger.ONE) == 0)
            return base;

        while (power.compareTo(BigInteger.ZERO) > 0) // this means power > 0
        {
            BigInteger powerMod = power.mod(two);
            //System.out.println("power = " + power);
            if (powerMod.compareTo(BigInteger.ONE) == 0)
                R = R.multiply(base).mod(mod);

            base = base.multiply(base).mod(mod);
            power = power.divide(two);
        }

        return R;
    }

    public static long montLadder(int base, long power, int mod)
    {
        long x1 = base;
        long x2 = base*base;
        int started = 0;
        int i;
        for (i=63; i>=0; i--) {

            int bit_set = ((int)(power >> i) & 0x01);

            long t_x1 = ((1-bit_set)*(x1*x1)) + (bit_set)*(x1*x2);
            long t_x2 = ((1-bit_set)*(x1*x2)) + (bit_set)*(x2*x2);

            x1 = (1-started)*x1 + started*(t_x1 % mod);
            x2 = (1-started)*x2 + started*(t_x2 % mod);

            started |= (bit_set);
        }
        return x1;
    }

    public static void main(String [] args)
    {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine();

        long num = stringToLong(s,96);
        BigInteger BigNum = stringToBigInt(s,96);

        int prime = 2357;
        BigInteger BigPrime = new BigInteger("2357");
        //int prime = 5;
        int g = 1415;
        BigInteger BigG = new BigInteger("1415");
        //int g = 2;

        int res = repeatedSquare(g,num,prime);
        BigInteger BigRes = BigRepeatedSquare(BigG,BigNum,BigPrime);
        long res2 = montLadder(g, num, prime);

        System.out.println("num = " + num);
        //System.out.println("res = " + res);
        //System.out.println("BigRes = " + BigRes);
        //System.out.println("res2= " + res2);
    }
}
