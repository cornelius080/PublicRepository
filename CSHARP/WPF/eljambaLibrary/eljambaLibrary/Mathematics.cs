using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Media.Media3D;



namespace eljambaLibrary
{
    public class Mathematics
    {
        UsefulMethods myUsefulMethods = new UsefulMethods();


        /// <summary>
        /// This method calculates the mean value of an array
        /// </summary>
        /// <param name="myArray">an array of double elements</param>
        public double CalculateMean(double[] myArray)
        {
            double mean = 0.0;

            for (var i = 0; i < myArray.Length; i++)
                mean += myArray[i];

            mean = (mean / myArray.Length);

            return mean;

        }



        /// <summary>
        /// This method calculates the standard deviation of an array
        /// </summary>
        /// <param name="myArray">an array of double elements</param>
        /// <param name="correction">if true divides for N-1; if false divides for N</param>
        public double CalculateStd(double[] myArray, bool correction)
        {
            double std = 0.0;
            double somme = 0.0;
            double sommeQuad = 0.0;

            for (var i = 0; i < myArray.Length; i++)
            {
                sommeQuad += Math.Pow(myArray[i], 2);
                somme += myArray[i];
            }
            somme = Math.Pow(somme, 2);
            somme = (somme / myArray.Length);
            if (correction == false)
                std = (sommeQuad - somme) / (myArray.Length);
            else
                std = (sommeQuad - somme) / (myArray.Length - 1);

            return std;

        }



        /// <summary>
        /// This method calculates the mode value of an array
        /// </summary>
        /// <param name="myArray">an array of double elements</param>
        public double CalculateMode(double[] myArray)
        {
            int length = myArray.Length;
            double[] sortedArray;
            int index = 0;
            int jm = 1; //contains the higher current frequency
            int j = 0;
            double mode = new double();

            sortedArray = myUsefulMethods.SelectionSortAscendingOrder(myArray);
            mode = sortedArray[0];
            while (index <= length)
            {
                j = 0; //contains the number of comparisons between identical elements to the i_esim; so, j+1 is the number of the copies of sortedArray[i] that are in sortedArray
                while (((index + j + 1) < length) && (sortedArray[index + j] == sortedArray[index + j + 1]))
                {
                    j = j + 1;
                }
                if (jm < j + 1)
                {
                    jm = j + 1;
                    mode = sortedArray[index + j];
                }
                mode = sortedArray[index + j];
            }
            return mode;

        }
        


        /// <summary>
        /// Returns the specified column from the input matrix.
        /// </summary>
        /// <param name="myMat">input matrix 3 X 3</param>
        /// <param name="colNumber">number of the column in zero base</param>
        public Vector3D ExtractColumnsFromMatrix(Matrix3D myMat, int colNumber)
        {
            Vector3D col = new Vector3D();


            if (colNumber < 0 || colNumber > 2)
                MessageBox.Show("(Incorrect column number");

            else if (colNumber == 0)
            {
                col.X = myMat.M11;
                col.Y = myMat.M21;
                col.Z = myMat.M31;
            }
            else if (colNumber == 1)
            {
                col.X = myMat.M12;
                col.Y = myMat.M22;
                col.Z = myMat.M32;
            }
            else if (colNumber == 2)
            {
                col.X = myMat.M13;
                col.Y = myMat.M23;
                col.Z = myMat.M33;
            }            

            return col;
        }



        /// <summary>
        /// Returns a column vector (3 X nSamples) from the input matrix.
        /// </summary>
        /// <param name="myMat">input matrix (3 X 3 X nSamples)</param>
        /// <param name="colNumber">number of the column in zero base</param>
        public Vector3D[] ExtractColumnsFromMatrix(Matrix3D[] myMat, int colNumber)
        {
            int nSamples = myMat.Length;
            Vector3D[] col = new Vector3D[nSamples];


            for (var i = 0; i < nSamples; i++)
            {
                if (colNumber < 0 || colNumber > 2)
                    MessageBox.Show("(Incorrect column number");

                else if (colNumber == 0)
                {
                    col[i].X = myMat[i].M11;
                    col[i].Y = myMat[i].M21;
                    col[i].Z = myMat[i].M31;
                }
                else if (colNumber == 1)
                {
                    col[i].X = myMat[i].M12;
                    col[i].Y = myMat[i].M22;
                    col[i].Z = myMat[i].M32;
                }
                else if (colNumber == 2)
                {
                    col[i].X = myMat[i].M13;
                    col[i].Y = myMat[i].M23;
                    col[i].Z = myMat[i].M33;
                }

            }
            

            return col;
        }



        /// <summary>
        /// Returns the transpose of the input matrix (3 x 3).
        /// </summary>
        /// <param name="myMat">3 x 3 matrix</param>
        public Matrix3D TransposeMatrix(Matrix3D myMat)
        {
            Matrix3D transposed = new Matrix3D();

            transposed.M11 = myMat.M11;
            transposed.M12 = myMat.M21;
            transposed.M13 = myMat.M31;
            transposed.M21 = myMat.M12;
            transposed.M22 = myMat.M22;
            transposed.M23 = myMat.M32;
            transposed.M31 = myMat.M13;
            transposed.M32 = myMat.M23;
            transposed.M33 = myMat.M33;

            return transposed;
        }



        /// <summary>
        /// Returns the transpose of the input matrix (3 x 3 x nSamples).
        /// </summary>
        /// <param name="myMat">3 x 3 x nSamples matrix</param>
        public Matrix3D[] TransposeMatrix(Matrix3D[] myMat)
        {
            int nSamples = myMat.Length;
            Matrix3D[] transposed = new Matrix3D[nSamples];

            for(var i=0; i<nSamples; i++)
            {
                transposed[i].M11 = myMat[i].M11;
                transposed[i].M12 = myMat[i].M21;
                transposed[i].M13 = myMat[i].M31;
                transposed[i].M21 = myMat[i].M12;
                transposed[i].M22 = myMat[i].M22;
                transposed[i].M23 = myMat[i].M32;
                transposed[i].M31 = myMat[i].M13;
                transposed[i].M32 = myMat[i].M23;
                transposed[i].M33 = myMat[i].M33;
            }
            
            return transposed;
        }



        /// <summary>
        /// Returns the absolute value of each element of the input array (nSamples x 1).
        /// </summary>
        /// <param name="myArray">nSamples x 1 input array</param>
        public double[] ArrayAbs(double[] myArray)
        {
            double[] absArray = new double[myArray.Length];

            for (var i = 0; i < absArray.Length; i++)
                absArray[i] = Math.Abs(myArray[i]);

            return absArray;
        }



        /// <summary>
        /// Returns the maximum value of the array
        /// </summary>
        /// <param name="myArray">nSamples x 1 input array</param>
        public double ArrayMax(double[] myArray)
        {
            double max = Double.NegativeInfinity;

            for (var i=0; i<myArray.Length; i++)
            {
                if (myArray[i] > max)
                    max = myArray[i];
            }

            return max;
        }


    }
}
