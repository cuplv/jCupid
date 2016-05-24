

public class Mux
{

    /* This one has a side channel in it */
    public static char select_side_channel(char a, char b, boolean select)
    {
        if (select == true) {
            return a;
        } else {
            return b;
        }
    }

    public static char select_constant_time(char a, char b, int select)
    {
        int res = 0;
        int mask_a = (0xFF)*select;
        int mask_b = (0xFF)*(1-select);
        res = ((int)a & mask_a) | ((int)b & mask_b);

        return (char)res;
    }


    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Error: requires an argument");
        }

        System.out.println(args[0]);
        char a = args[0].charAt(0);
        char b = args[0].charAt(1);
        char s_chr = args[0].charAt(2);
        boolean s = (((int)s_chr & 1) == 1);

        System.out.println(Mux.select_side_channel(a, b, s));
        System.out.println(Mux.select_constant_time(a, b, s?1:0));

    }


}
