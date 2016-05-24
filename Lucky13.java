/*
 * Lucky13.java
 * 2016 ian <ian@ian-HP-Mini-210-2000>
 *
 * 
 */
import javax.crypto.*;
import javax.crypto.spec.IvParameterSpec;
import java.io.UnsupportedEncodingException;
import java.lang.Integer;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.Random;
import java.util.Scanner;

public class Lucky13
{
    public static byte[] encrypt(String message, SecretKey MACKey, SecretKey AESKey, IvParameterSpec IV)
    {
        byte[] cText = {};
        try
        {
            Mac mac = Mac.getInstance(MACKey.getAlgorithm());
            mac.init(MACKey);

            byte[] utf8 = message.getBytes("UTF8");
            byte[] digest = mac.doFinal(utf8);

            // Now we combine these together, first we must make a new byte[]
            // of length a multiple of 128 bits (16 bytes).
            int size = utf8.length + digest.length;
            int over = size % 16;
            size += (16-over);

            // Now for the byte array of the correct length:
            byte[] full = new byte[size];
            // First copy the utf8 array into full, at position 0
            System.arraycopy(utf8,0,full,0,utf8.length);
            // Second copy the digest array into full after utf8
            System.arraycopy(digest,0,full,utf8.length,digest.length);
            // (16-over) representes how many bytes of padding we need to
            // write so we subtract one from this and write it to the last
            // (16-over) bytes of full
            
            byte val = (byte)(16 - over - 1);
            for (int i = utf8.length+digest.length; i < size; i++)
                full[i] = val;

            Cipher AesCipherEnc = Cipher.getInstance("AES/CBC/NoPadding");

            AesCipherEnc.init(Cipher.ENCRYPT_MODE,AESKey,IV);
            cText = AesCipherEnc.doFinal(full);

            return cText;

        } catch (InvalidKeyException e) {
            System.out.println("InvalidKeyException raised as: "+e);
            return cText;
        } catch (NoSuchAlgorithmException e) {
            System.out.println("NoSuchAlgorithmException raised as: "+e);
            return cText;
        } catch (UnsupportedEncodingException e) {  
            System.out.println("UnsupportedEncodingException raised as: "+e);
            return cText;
        } catch (NoSuchPaddingException e){
            System.out.println("NoSuchPaddingException raised as: "+e);
            return cText;
        } catch (IllegalBlockSizeException e){
            System.out.println("IllegalBlockSizeException raised as: "+e);
            return cText;
        } catch (BadPaddingException e){
            System.out.println("BadPaddingException raised as: "+e);
            return cText;
        } catch (InvalidAlgorithmParameterException e){
            System.out.println("InvalidAlgorithmParameterException raised as: "+e);
            return cText;
        }
    }

    public static String decrypt(byte[] cText, SecretKey MACKey, SecretKey AESKey, IvParameterSpec IV)
    {
        try
        {
            Cipher AesCipherDec = Cipher.getInstance("AES/CBC/NoPadding");
            AesCipherDec.init(Cipher.DECRYPT_MODE,AESKey,IV);
            byte[] pText = AesCipherDec.doFinal(cText);
            int pTextSize = pText.length;
            boolean goodPadding = true;

            int numEntries = (int)(pText[pTextSize - 1] + 1) & 0xFF; 
            //System.out.println("numEntries = " + numEntries);
            boolean validNumEntries;
            if (numEntries < 1 || numEntries > 16)
            {
                validNumEntries = false;
                goodPadding = false;
            }
            else 
            {
                validNumEntries = true;
                goodPadding = true;
            }

            int subTerm;

            if (validNumEntries)
                subTerm = numEntries;
            else
                subTerm = 0;

            for(int i = pTextSize - numEntries; i < pTextSize; i++)
            {
                if(!validNumEntries || pText[i] != numEntries -1)
                {
                    goodPadding = false;
                }
            }

            // now we figure out what to check the MAC of!
            boolean goodMAC;
            Mac mac2 = Mac.getInstance(MACKey.getAlgorithm());
            mac2.init(MACKey);
            System.out.println("goodPadding = " + goodPadding);
            byte[] supposedDigest = Arrays.copyOfRange(pText,
                    pTextSize-subTerm-20,pTextSize-subTerm);
            byte[] message = Arrays.copyOfRange(pText,0,
                    pTextSize-subTerm-20);
            byte[] actualDigest = mac2.doFinal(message);
            goodMAC = Arrays.equals(supposedDigest,actualDigest);
            System.out.println("goodMAC = " + goodMAC);

            if (goodMAC)
                return new String(message,"UTF-8");
            else
                return "Something went wrong in MAC/Padding";

        } catch (InvalidKeyException e) {
            System.out.println("InvalidKeyException raised as: "+e);
            return "";
        } catch (NoSuchAlgorithmException e) {
            System.out.println("NoSuchAlgorithmException raised as: "+e);
            return "";
        } catch (UnsupportedEncodingException e) {  
            System.out.println("UnsupportedEncodingException raised as: "+e);
            return "";
        } catch (NoSuchPaddingException e){
            System.out.println("NoSuchPaddingException raised as: "+e);
            return "";
        } catch (IllegalBlockSizeException e){
            System.out.println("IllegalBlockSizeException raised as: "+e);
            return "";
        } catch (BadPaddingException e){
            System.out.println("BadPaddingException raised as: "+e);
            return "";
        } catch (InvalidAlgorithmParameterException e){
            System.out.println("InvalidAlgorithmParameterException raised as: "+e);
            return "";
        }
    }

    public static void main(String [] args) 
    {
        try 
        {
            // Generate a key for the HMAC-MD5 keyed-hashing algorithm; see RFC 2104
            // In practice, you would save this key.
            KeyGenerator keyGen = KeyGenerator.getInstance("HmacSHA1");
            SecretKey key = keyGen.generateKey();

            String str = "This message will be digested";

            KeyGenerator KeyGen = KeyGenerator.getInstance("AES");
            KeyGen.init(128);

            SecretKey SecKey = KeyGen.generateKey();
            // Need an IV: 
            byte[] iv = new byte[16];
            new Random().nextBytes(iv);
            IvParameterSpec IV = new IvParameterSpec(iv);

            byte[] ct = encrypt(str, key,SecKey,IV);

            // Now the Decrypt stage!
            Scanner sc = new Scanner(System.in);
            //System.out.println("Would you like to interject some ciphertext " 
                    //+ "of your own? ");
            String userInput = sc.next();
            ct = userInput.getBytes("UTF8");

            //if (userInput.equals("y") || userInput.equals("Y"))
            //{
                //System.out.println("Enter your Ciphertext now: ");
                //String rogueCipherText = sc.next();
                //ct = rogueCipherText.getBytes("UTF8");
                //System.out.println("length of cText = " + ct.length);
            //}
            
            String pt = decrypt(ct, key,SecKey,IV);
            System.out.println("Plaintext is: " + pt);
            
            

        } catch (NoSuchAlgorithmException e) {
            System.out.println("NoSuchAlgorithmException raised as: "+e);
        } catch (UnsupportedEncodingException e) {  
            System.out.println("UnsupportedEncodingException raised as: "+e);
        }
    }
}

