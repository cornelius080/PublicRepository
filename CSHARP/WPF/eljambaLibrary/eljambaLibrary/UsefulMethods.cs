using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;



namespace eljambaLibrary
{
    public class UsefulMethods
    {
        /// <summary>
        /// This method returns the index with which the imu is stored in the data structure, starting from the imu number in zero base.
        /// </summary>
        /// <param name="arrayImu">array that contains the number of the imus</param>
        /// <param name="imuNumInZeroBase">number of the imu in zero base</param>
        public int findIndex(int[] arrayImu, int imuNumInZeroBase)
        {
            int index = -1;

            for (var i = 0; i < arrayImu.Length; i++)
            {
                if (arrayImu[i] == imuNumInZeroBase)
                    index = i;
            }

            return index;
        }



        /// <summary>
        /// This method sorts array elements in ascending order
        /// </summary>
        /// <param name="myArray">an array of double elements</param>
        public double[] SelectionSortAscendingOrder(double[] myArray)
        {
            int length = myArray.Length;
            int posmin;
            double tmp;

            for (var i = 0; i < (length - 1); i++)
            {
                posmin = i;
                for (var j = (i + 1); j < length; j++)
                {
                    if (myArray[j] < myArray[posmin])
                        posmin = j;
                }
                if (posmin != i)
                {
                    tmp = myArray[i];
                    myArray[i] = myArray[posmin];
                    myArray[posmin] = tmp;
                }
            }
            return myArray;
        }



        /// <summary>
        /// This method sorts array elements in ascending order
        /// </summary>
        /// <param name="myArray">an array of int elements</param>
        public int[] SelectionSortAscendingOrder(int[] myArray)
        {
            int length = myArray.Length;
            int posmin;
            int tmp;

            for (var i = 0; i < (length - 1); i++)
            {
                posmin = i;
                for (var j = (i + 1); j < length; j++)
                {
                    if (myArray[j] < myArray[posmin])
                        posmin = j;
                }
                if (posmin != i)
                {
                    tmp = myArray[i];
                    myArray[i] = myArray[posmin];
                    myArray[posmin] = tmp;
                }
            }
            return myArray;
        }



        /// <summary>
        /// Returns the sensors selected in a previous acquisition, and saved in a .csv file.
        /// </summary>
        /// <param name="_fullPathFilename"> String that contains the full path and the filename of the .csv</param>
        /// <returns> Array of int elements that contain the selected sensors number. If no selection were performed, an array of 16 zeros is returned.</returns>
        public int[] CheckSelectedSensorsFromCSVFile(string _fullPathFilename)
        {
            bool esiste = File.Exists(_fullPathFilename);
            int[] selectedSensors;
            selectedSensors = null;

            if (esiste == true)
            {
                String rigaSelectedSensors, rigaIntestazione;
                int lunghezza = 0, cont = 0, startIndex = 0;

                using (StreamReader sr = new StreamReader(_fullPathFilename))
                {
                    rigaIntestazione = sr.ReadLine();
                    rigaSelectedSensors = sr.ReadLine();
                }


                //creo un vettore della dimensione opportuna
                for (var car = 0; car < rigaSelectedSensors.Length; car++)
                    if (rigaSelectedSensors[car] == ';') lunghezza++;

                selectedSensors = new int[lunghezza];


                //immagazzino nel vettore i valori letti
                for (var myChar = 0; myChar < rigaSelectedSensors.Length; myChar++)
                {
                    if (rigaSelectedSensors[myChar] == ';')
                    {
                        selectedSensors[cont] = int.Parse(rigaSelectedSensors.Substring(startIndex, myChar - startIndex));
                        startIndex = myChar + 1;
                        cont++;
                    }
                }

            }
            else
            {
                selectedSensors = new int[16];
                for (var i = 0; i < selectedSensors.Length; i++)
                    selectedSensors[i] = 0;
            }



            return selectedSensors;
        }



        /// <summary>
        /// Creates a file in which a file header and the selected sensors are written.
        /// </summary>
        /// <param name="_fullPathFilename"> String composed by the path and the file name. </param>
        /// <param name="stringaIntestazione"> String with the file header, such as "EMG_UP" + ";" + "EMG_DOWN" + ";"</param>
        /// <param name="selectedSensors"> Array of int elements corrisponding to the selected sensors. </param>
        public void SaveSelectedSensorsInCSVFile(string _fullPathFilename, string stringaIntestazione, int[] selectedSensors)
        {
            using (StreamWriter sw = new StreamWriter(_fullPathFilename, false))  // True to append data to the file; false to overwrite the file
            {
                //SCRIVO L'INTESTAZIONE DEL FILE 
                sw.WriteLine(stringaIntestazione);

                for (var i = 0; i < selectedSensors.Length; i++)
                    sw.Write(selectedSensors[i].ToString() + ";");
            }
        }



        /// <summary>
        /// Removes the zeros in an array, if are present. 
        /// </summary>
        /// <param name="myArray"> Input array of int elements. </param>
        /// <returns></returns>
        public int[] RemoveZerosFromArray(int[] myArray)
        {
            int[] newArray;

            int contaZeri = 0;
            for (var i = 0; i < myArray.Length; i++)
            {
                if (myArray[i] == 0)
                    contaZeri++;
            }

            newArray = new int[myArray.Length - contaZeri];
            int index = 0;
            for (var i = 0; i < myArray.Length; i++)
            {
                if (myArray[i] != 0)
                {
                    newArray[index] = myArray[i];
                    index++;
                }
            }

            return newArray;
        }



        /// <summary>
        /// Removes the zeros in an array, if are present. 
        /// </summary>
        /// <param name="myArray"> Input array of double elements. </param>
        /// <returns></returns>
        public double[] RemoveZerosFromArray(double[] myArray)
        {
            double[] newArray;

            int contaZeri = 0;
            for (var i = 0; i < myArray.Length; i++)
            {
                if (myArray[i] == 0)
                    contaZeri++;
            }

            newArray = new double[myArray.Length - contaZeri];
            int index = 0;
            for (var i = 0; i < myArray.Length; i++)
            {
                if (myArray[i] != 0)
                {
                    newArray[index] = myArray[i];
                    index++;
                }
            }

            return newArray;
        }

    }
}
