

public class Cmp
{
    public static byte gt(int a, int b)
    {
        return (a > b) ? (byte)0xFF : (byte)0x00;
    }

    public static byte gt_constant(int a, int b)
    {
        return (byte)(((((b - a)) >> 31)&0x01)*0xFF);
    }

    public static void main(String[] args) {
        System.out.println(gt_constant(5, 8));
        System.out.println(gt_constant(8, 5));
        System.out.println(gt_constant(5000000, 8));
        System.out.println(gt_constant(5000000, 500000000));
        System.out.println(gt_constant(-1, -3));
        System.out.println(gt_constant(-3, -1));
        System.out.println(gt_constant(3, -8));
        System.out.println(gt_constant(-8, 3));
        System.out.println(gt_constant(3, 3));



    }


}
