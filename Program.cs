using System;
using System.Numerics;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RSA
{
    public class Program
    {
        static readonly int[] primes = {3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
          109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
          233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
          367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
          499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
          643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
          797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
          947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063,
          1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201,
          1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319,
          1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471,
          1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597,
          1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723,
          1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873,
          1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999};
        static Random rnd = new Random();
        static void Main(string[] args)
        {
            int[] res = GetKeys();
            string[] r = EncodeFunction("Hello!", res[0], res[1]);
            foreach (string s in r)
            {
                Console.WriteLine(s);
            }
            Console.WriteLine("--------");
            string ans = DecodeFunction(r, res[2], res[3]);
            Console.WriteLine(ans);
            Console.ReadKey();
        }
        static int[] GetKeys()
        {
            int p = 7;
            int q = 11;
            int n = p * q;
            int f = (p - 1) * (q - 1);
            int i = Convert.ToInt32(Math.Pow(2, 16)) + 1;
            if (Check(i, f) == 0)
            {
                for (int j = 2; j < f; j++)
                {
                    if (Check(i, f) == 1)
                        break;
                }
            }
            int e = i;
            int d = get(e, f);
            int[] arr = new int[4];
            arr[0] = e;
            arr[1] = n;
            arr[2] = d;
            arr[3] = n;
            return arr;
        }

        static int Check (int x, int y)
        {
            while (true)
            {
                if (y == 0)
                    return x;
                x %= y;
                if (x == 0)
                    return y;
                y %= x;
            }
        }
        static int get(int a, int m)
        {
            int b, c, i, j, x, y;
            b = m;
            c = a;
            i = 0;
            j = 1;
            while (c != 0)
            {
                x = Convert.ToInt32(b / c);
                y = b % c;
                b = c;
                c = y;
                y = j;
                j = i - j * x;
                i = y;
            }
            if (i < 0)
                i += m;
            return i;
        }
        static string ToBinary(int n)
        {
            return Convert.ToString(n, 2);
        }

        static bool MillerRabin(int n, int s)
        {
            for (int j = 1; j <= s; j++)
            {
                int a = rnd.Next(1, n - 1);
                string b = ToBinary(n - 1);
                int d = 1;
                for (int i = b.Length - 1; i > -1; i--)
                {
                    int x = d;
                    d = (d * d) % n;
                    if (d == 1 && x != 1 && x != n - 1)
                        return true;  // составное
                    if (b[i] == '1')
                    {
                        d = (d * a) % n;
                        if (d != 1)
                            return true;  // составное
                        return false;  // простое
                    }
                }
            }
            return true;  // эта ветвь никогда не выполняется
        }
        static bool Ferma(int n, int a)
        {
            return (BigInteger.ModPow(a, n - 1, n) == 1);
        }
        static bool Prime(int n)
        {
            if (n % 2 == 0)
                return false;
            foreach (int prime_ in primes)
            {
                if (n % prime_ == 0 && n != prime_)
                    return false;
            }
            for (int i = 0; i < 50; i++)
            {
                int a = rnd.Next(0, Convert.ToInt32(Math.Pow(10, 5)));
                if (!MillerRabin(n, a) || !Ferma(n, a))
                    return false;
            }
            return true;
        }
        static string[] EncodeFunction(string a, int e, int n)
        {
            string[] a_array = new string[a.Length + 1];
            string[] encode_array = new string[a.Length + 1];
            a_array[0] = Convert.ToString(rnd.Next(0, Convert.ToInt32(Math.Pow(10, 5))));
            for (int i = 1; i < a.Length; i++)
                a_array[i] = Convert.ToString(Convert.ToByte(a[i - 1]));
            for (int i = 1; i <= a.Length; i++)
                a_array[i] = Convert.ToString((Convert.ToInt32(a_array[i - 1]) + Convert.ToInt32(a_array[i])) % n);
            for (int i = 0; i <= a.Length; i++)
                encode_array[i] = Convert.ToString((int)BigInteger.ModPow(Convert.ToInt32(a_array[i]), e, n), 16);
            return encode_array;
        }
        static string DecodeFunction(string[] a, int d, int n)
        {
            int[] decode_array = new int[a.Length];
            for (int i = 0; i < a.Length; i++)
                decode_array[i] = (int)BigInteger.ModPow(Convert.ToInt32(a[i], 16), d, n);
            char[] new_array = new char[a.Length];
            for (int i = 1; i < decode_array.Length; i++)
            {
                new_array[i - 1] = (char)((decode_array[i] - decode_array[i - 1]) % n);
                Console.WriteLine(((decode_array[i] - decode_array[i - 1]) % n));
            }
            return new string(new_array);
        }
    }
}
