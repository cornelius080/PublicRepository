using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using Waveplus.DaqSys;
using Waveplus.DaqSys.Definitions;
using Waveplus.DaqSysInterface;
using WaveplusLab.Shared.Definitions;
using System.Diagnostics;
using System.Windows;

namespace pisaSindrome_cometa
{
    class myQuaternion
    {
        public float[] w, x, y, z;

        /// <summary>
        /// Structures builder
        /// </summary>
        public myQuaternion(int samplesNumber)
        {
            w = new float[samplesNumber];
            x = new float[samplesNumber];
            y = new float[samplesNumber];
            z = new float[samplesNumber];

        }
    }
    class myRotationMatrix
    {
        public float[][][] element;

        /// <summary>
        /// Structures builder
        /// </summary>
        public myRotationMatrix(int samplesNumber)
        {
            element = new float[3][][];
            for (var i=0; i<element.Length; i++)
            {
                element[i] = new float[3][];
                for(var j=0; j<element[i].Length; j++)
                {
                    element[i][j] = new float[samplesNumber];
                }
            }


        }
    }
    class myAngles
    {
        public float[][] flx;
        public float[][] add;
        public float[][] rot;
        public float[][] absFlx;
        public float[][] absAdd;
        public float[][] absRot;

        /// <summary>
        /// Structures builder
        /// </summary>
        public myAngles(int sensorsNumber, int samplesNumber)
        {
            flx = new float[sensorsNumber][];
            add = new float[sensorsNumber][];
            rot = new float[sensorsNumber][];
            for (var i = 0; i < flx.Length; i++)
            {
                flx[i]    = new float[samplesNumber];
                add[i]    = new float[samplesNumber];
                rot[i]    = new float[samplesNumber];
                absFlx[i] = new float[samplesNumber];
                absAdd[i] = new float[samplesNumber];
                absRot[i] = new float[samplesNumber];

            }
        }
    }
    class myBuffer
    {
        public float[][] AccX;
        public float[][] AccY;
        public float[][] AccZ;
        public float[][] QuatW;
        public float[][] QuatX;
        public float[][] QuatY;
        public float[][] QuatZ;
        public double[]  Time;

        /// <summary>
        /// Structures builder
        /// </summary>
        public myBuffer(int sensorsNumber, int samplesNumber)
        {
            Time  = new double[samplesNumber];
            AccX  = new float[sensorsNumber][];
            AccY  = new float[sensorsNumber][];
            AccZ  = new float[sensorsNumber][];
            QuatW = new float [sensorsNumber][];
            QuatX = new float [sensorsNumber][];
            QuatY = new float [sensorsNumber][];
            QuatZ = new float [sensorsNumber][];
            for (var i=0; i < QuatW.Length; i++)
            {
                AccX[i]  = new float[samplesNumber];
                AccY[i]  = new float[samplesNumber];
                AccZ[i]  = new float[samplesNumber];
                QuatW[i] = new float[samplesNumber];
                QuatX[i] = new float[samplesNumber];
                QuatY[i] = new float[samplesNumber];
                QuatZ[i] = new float[samplesNumber];
            }
        }
    }
    class DataCollection
    {
        public myBuffer fifoBuffers; //BUFFER DEI DATI RIEMPITO CON LOGICA FIFO
        public myBuffer finestraAttiva; //VETTORE CHE COTIENE GLI ULTIMI dimFinestraAttiva CAMPIONI DEI fifoBuffers
        public myAngles cometaAngles;
        public myRotationMatrix recalibrationMatrix; //STRUTTURA CHE CONTIENE LA MATRICE DI RICALIBRAZIONE DEI QUATERNIONI LETTI DALLE IMU
        int dimFinestraAttiva; //utilizzato per il riempimento della finestraAttiva sottocampionando i fifoBuffers 
        int dimBuffers; //lunghezza in campioni dei singoli buffers;   0,1s : (e.ScanNumber/14) campioni = durataBuffers in sec : dimBuffers; 
        double Tc;
        int sampleStep;
        int[] array_sonde; //deve contenere gli indici in base zero


        

        /// <summary>
        /// Structures builder
        /// </summary>
        public DataCollection(int[] _array_sonde, int secondiFinestraAttiva, double frequenzaCampionamento)
        {
            array_sonde = _array_sonde;
            sampleStep = new int();
            sampleStep = (int)Math.Floor((2000 / frequenzaCampionamento));

            Tc = Math.Pow(frequenzaCampionamento, -1);
            //0,1s: (e.ScanNumber / 14) campioni = durataBuffers in sec: dimBuffers;
            dimFinestraAttiva = (10 * sampleStep * secondiFinestraAttiva);  
            dimBuffers = 2 * dimFinestraAttiva;  //impostata al doppio della lunghezza della finestra attiva

            //primo indice=sonda, secondo indice=campione
            fifoBuffers = new myBuffer(array_sonde.Length, dimBuffers);

            //primo indice=sonda, secondo indice=campione
            finestraAttiva = new myBuffer(array_sonde.Length, dimFinestraAttiva);

            //primo indice=angolo, secondo indice=campione
            cometaAngles = new myAngles(array_sonde.Length, dimFinestraAttiva);            
        }


        /// <summary>
        /// This method populates buffers with Fifo logic
        /// </summary>
        public void RiempiFifoBuffers(DataAvailableEventArgs e)
        {
            //ciclo sulle sonde
            for (var i = 0; i < fifoBuffers.QuatW.Length; i++)
            {
                //CICLI SUI CAMPIONI
                //ciclo per lo shift
                for (var k = 0; k < (fifoBuffers.QuatW[0].Length - sampleStep); k++)
                {
                    fifoBuffers.AccX[i][k]  = fifoBuffers.AccX[i][k + sampleStep];
                    fifoBuffers.AccY[i][k]  = fifoBuffers.AccX[i][k + sampleStep];
                    fifoBuffers.AccZ[i][k]  = fifoBuffers.AccX[i][k + sampleStep];
                    fifoBuffers.QuatW[i][k] = fifoBuffers.QuatW[i][k + sampleStep];
                    fifoBuffers.QuatX[i][k] = fifoBuffers.QuatX[i][k + sampleStep];
                    fifoBuffers.QuatY[i][k] = fifoBuffers.QuatY[i][k + sampleStep];
                    fifoBuffers.QuatZ[i][k] = fifoBuffers.QuatZ[i][k + sampleStep];
                    fifoBuffers.Time[k]     = fifoBuffers.Time[k + sampleStep];
                }
                //ciclo per copiare i dati
                for (var k = (fifoBuffers.QuatW[0].Length - sampleStep); k < fifoBuffers.QuatW[0].Length; k++)
                {
                    //IN e.ImuSamples I SENSORI SONO INDICIZZATI IN BASE ZERO; LO STESSO AVVIENE IN array_sonde, OVVERO IN vettore_sonde
                    //200 campioni circa a pacchetto diviso sampleStep, fa circa 14
                    fifoBuffers.AccX[i][k]  = e.AccelerometerSamples[array_sonde[i], 0, (k - fifoBuffers.QuatW[0].Length + sampleStep) * 14];
                    fifoBuffers.AccY[i][k]  = e.AccelerometerSamples[array_sonde[i], 1, (k - fifoBuffers.QuatW[0].Length + sampleStep) * 14];
                    fifoBuffers.AccZ[i][k]  = e.AccelerometerSamples[array_sonde[i], 2, (k - fifoBuffers.QuatW[0].Length + sampleStep) * 14];
                    fifoBuffers.QuatW[i][k] = e.ImuSamples          [array_sonde[i], 0, (k - fifoBuffers.QuatW[0].Length + sampleStep) * 14];
                    fifoBuffers.QuatX[i][k] = e.ImuSamples          [array_sonde[i], 1, (k - fifoBuffers.QuatW[0].Length + sampleStep) * 14];
                    fifoBuffers.QuatY[i][k] = e.ImuSamples          [array_sonde[i], 2, (k - fifoBuffers.QuatW[0].Length + sampleStep) * 14];
                    fifoBuffers.QuatZ[i][k] = e.ImuSamples          [array_sonde[i], 3, (k - fifoBuffers.QuatW[0].Length + sampleStep) * 14];
                    fifoBuffers.Time[k]     = fifoBuffers.Time[k - 1] + (float)Tc;
                }
            }

        }


        /// <summary>
        /// This method populates active window downsampling buffers
        /// </summary>
        public void RiempiFinestraAttiva()
        {
            //COPIO I DATI DAI fifoBuffers ALLA finestraAttiva   
            //ciclo sulle sonde             
            for (var i = 0; i < fifoBuffers.QuatW.Length; i++)
            {                
                //alternativa al successivo ciclo for
                //public static void Copy(Array sourceArray, int sourceIndex, Array destinationArray, int destinationIndex, int length)
                //Array.Copy(fifoBuffers[i][j], (fifoBuffers[i][j].Length - 1 - finestraAttiva[i][j].Length), finestraAttiva[i][j], 0, 
                //finestraAttiva[i][j].Length);

                //ciclo sui campioni
                for (var k = 0; k < finestraAttiva.QuatW[i].Length; k++)
                {
                    finestraAttiva.AccX[i][k]  = fifoBuffers.AccX [i][fifoBuffers.QuatW[i].Length - (finestraAttiva.QuatW[i].Length * 2) + (k * 2)];
                    finestraAttiva.AccY[i][k]  = fifoBuffers.AccY [i][fifoBuffers.QuatW[i].Length - (finestraAttiva.QuatW[i].Length * 2) + (k * 2)];
                    finestraAttiva.AccZ[i][k]  = fifoBuffers.AccZ [i][fifoBuffers.QuatW[i].Length - (finestraAttiva.QuatW[i].Length * 2) + (k * 2)];
                    finestraAttiva.QuatW[i][k] = fifoBuffers.QuatW[i][fifoBuffers.QuatW[i].Length - (finestraAttiva.QuatW[i].Length * 2) + (k * 2)];
                    finestraAttiva.QuatX[i][k] = fifoBuffers.QuatX[i][fifoBuffers.QuatX[i].Length - (finestraAttiva.QuatX[i].Length * 2) + (k * 2)];
                    finestraAttiva.QuatY[i][k] = fifoBuffers.QuatY[i][fifoBuffers.QuatY[i].Length - (finestraAttiva.QuatY[i].Length * 2) + (k * 2)];
                    finestraAttiva.QuatZ[i][k] = fifoBuffers.QuatZ[i][fifoBuffers.QuatZ[i].Length - (finestraAttiva.QuatZ[i].Length * 2) + (k * 2)];
                    finestraAttiva.Time[k]     = fifoBuffers.Time[fifoBuffers.Time.Length - (finestraAttiva.Time.Length * 2) + (k * 2)];
                    //finestraAttiva[i][j][k]  = fifoBuffers[i][j][k + fifoBuffers[i][j].Length - finestraAttiva[i][j].Length];
                }         
            }                

        }


        /// <summary>
        /// This method calculates the rotation matrix used for recalibration
        /// </summary>
        public void SetImuReferences(int pelvisImuIndexInZeroBase, DataAvailableEventArgs e)
        {
            int index;
            myQuaternion auxQuat, modeQuat;
            myRotationMatrix modeRotMat; 

            index = trovaIndice(pelvisImuIndexInZeroBase);

            //quaternion copy from imu structures into auxiliary quaternion
            auxQuat = new myQuaternion(e.ScanNumber);
            for (var i = 0; i < e.ScanNumber; i++)
            {
                auxQuat.w[i] = e.ImuSamples[index, 0, i];
                auxQuat.x[i] = e.ImuSamples[index, 0, i];
                auxQuat.y[i] = e.ImuSamples[index, 0, i];
                auxQuat.z[i] = e.ImuSamples[index, 0, i];
            }

            //Mode calculus
            modeQuat = new myQuaternion(1);
            modeQuat.w = CalculateMode(auxQuat.w);
            modeQuat.x = CalculateMode(auxQuat.x);
            modeQuat.y = CalculateMode(auxQuat.y);
            modeQuat.z = CalculateMode(auxQuat.z);

            //quaternion conversion into rotation matrix
            modeRotMat = new myRotationMatrix(modeQuat.w.Length);
            modeRotMat = FromQuaternionToRotationMatrix(modeQuat);


        }

        
        /// <summary>
        /// This method converts a quaternion into a rotation matrix of the same length
        /// </summary>
        public myRotationMatrix FromQuaternionToRotationMatrix(myQuaternion myQuat)
        {
            myRotationMatrix rotMat = new myRotationMatrix(myQuat.w.Length);

            for(var i=0; i< myQuat.w.Length; i++)
            {
                rotMat.element[0][0][i] = (float)(Math.Pow(myQuat.w[i], 2)) + (float)(Math.Pow(myQuat.x[i], 2)) - (float)(Math.Pow(myQuat.y[i], 2)) - (float)(Math.Pow(myQuat.z[i], 2));

                rotMat.element[0][1][i] = 2 * ( (myQuat.x[i] * myQuat.y[i]) - (myQuat.w[i] * myQuat.z[i]));
                rotMat.element[0][2][i] = 2 * ( (myQuat.x[i] * myQuat.z[i]) + (myQuat.w[i] * myQuat.y[i]) );
                rotMat.element[1][0][i] = 2 * ( (myQuat.x[i] * myQuat.y[i]) + (myQuat.w[i] * myQuat.z[i]) );

                rotMat.element[1][1][i] = (float)(Math.Pow(myQuat.w[i], 2)) - (float)(Math.Pow(myQuat.x[i], 2)) + (float)(Math.Pow(myQuat.y[i], 2)) - (float)(Math.Pow(myQuat.z[i], 2));

                rotMat.element[1][2][i] = 2 * ((myQuat.y[i] * myQuat.z[i]) - (myQuat.w[i] * myQuat.x[i]));
                rotMat.element[2][0][i] = 2 * ((myQuat.x[i] * myQuat.z[i]) - (myQuat.w[i] * myQuat.y[i]));
                rotMat.element[2][1][i] = 2 * ((myQuat.y[i] * myQuat.z[i]) + (myQuat.w[i] * myQuat.x[i]));

                rotMat.element[2][2][i] = (float)(Math.Pow(myQuat.w[i], 2)) - (float)(Math.Pow(myQuat.x[i], 2)) - (float)(Math.Pow(myQuat.y[i], 2)) + (float)(Math.Pow(myQuat.z[i], 2));

            }

            return rotMat;

        }
        

        /// <summary>
        /// This method calculates the mean value of an array
        /// </summary>
        public float CalculateMean(float[] myArray)
        {
            float mean = 0.0f;

            for (var i = 0; i < myArray.Length; i++)
            {
                mean += myArray[i];
            }
            mean = (float)(mean / myArray.Length);

            return mean;

        }


        /// <summary>
        /// This method calculates the mode value of an array
        /// </summary>
        public float[] CalculateMode(float[] myArray)
        {
            int length = myArray.Length;
            float[] sortedArray;
            int index = 0;
            int jm = 1; //contains the higher current frequency
            int j = 0;
            float[] mode = new float[1];

            sortedArray = SelectionSortAscendingOrder(myArray);
            mode[0] = sortedArray[0];
            while (index <= length)
            {
                j = 0; //contains the number of comparisons between identical elements to the i_esim; so, j+1 is the number of the copies of sortedArray[i] that are in sortedArray
                while (((index + j + 1) < length) && (sortedArray[index + j] == sortedArray[index + j + 1]))
                {
                    j = j + 1;
                }
                if(jm < j + 1)
                {
                    jm = j + 1;
                    mode[0] = sortedArray[index + j];
                }
                mode[0] = sortedArray[index + j];
            }
            return mode;
            
        }


        /// <summary>
        /// This method calculates the standard deviation of an array
        /// </summary>
        public float CalculateStd(float[] myArray)
        {
            float std = 0.0f;
            float somme = 0.0f;
            float sommequad = 0.0f;

            for (var i = 0; i < myArray.Length; i++)
            {
                sommequad += (float)Math.Pow(myArray[i], 2);
                somme += myArray[i];
            }
            somme = (float) (Math.Pow(somme, 2));
            somme = (float) (somme / myArray.Length);
            std = (sommequad - somme) / (myArray.Length);

            return std;

        }


        /// <summary>
        /// This method calculates the matrix product NOT COMMUTATIVE between two matrix
        /// </summary>
        public myRotationMatrix MatrixProduct(myRotationMatrix A, myRotationMatrix B)
        {
            myRotationMatrix product = new myRotationMatrix(A.element[0][0].Length);

            for (var sample = 0; sample < product.element[0][0].Length; sample++)
            {
                for (var row = 0; row < product.element.Length; row++)
                {
                    for (var col = 0; col < product.element[0].Length; col++)
                    {
                        product.element[row][col][sample] = 0.0f;
                        for (var k = 0; k < A.element[0].Length; k++)  //OR k < B.element.length;
                        {
                            product.element[row][col][sample] = product.element[row][col][sample] + (A.element[row][k][sample] * B.element[k][col][sample]);
                        }
                    }
                }
            }             
            
            return product;

        }


        /// <summary>
        /// This method creates a .bin file in which data read from imu were saved
        /// </summary>
        public void CreaFileCsv(string data)
        {
            string w = "QUAT_W_";
            string x = "QUAT_X_";
            string y = "QUAT_Y_";
            string z = "QUAT_Z_";
            string path = System.AppDomain.CurrentDomain.BaseDirectory;
            string filePath = path + @"\" + data + "ImuData.csv";

            using (StreamWriter sw = new StreamWriter(filePath))  // True to append data to the file; false to overwrite the file
            {
                //SCRIVO L'INTESTAZIONE DELLE COLONNE DEL FILE
                for (int i = 0; i < array_sonde.Length; i++)
                {
                    sw.Write(w + (1 + array_sonde[i]) + ";" + x + (1 + array_sonde[i]) + ";" + y + (1 + array_sonde[i]) + ";" +
                        z + (1 + array_sonde[i]) + ";" + "" + ";");
                }
                sw.Write("\n");
                sw.Close();
            }      
            
        }


        /// <summary>
        /// This method writes in real-time imu data in a preliminary created file 
        /// </summary>
        public void CsvSavingInRealTime(string data, DataAvailableEventArgs e)
        {
            //#######################################################################################################################################
            //STRUTTURA DEL FILE 
            //(W1[i])      X1[i]        Y1[i]        Z1[i]           (W2[i])      X2[i]        Y2[i]        Z2[i]   ....... 
            //#######################################################################################################################################

            string path = System.AppDomain.CurrentDomain.BaseDirectory;
            string filePath = path + @"\" + data + "ImuData.csv";

            using (StreamWriter sw = new StreamWriter(filePath, true))  // True to append data to the file; false to overwrite the file
            {
                //ciclo sui campioni
                for (var k = 0; k < e.ScanNumber; k++)
                {
                    //ciclo sulle sonde
                    for (var i = 0; i < array_sonde.Length; i++)
                    {
                        //ciclo sulle componenti
                        for (var j = 0; j < 4; j++)
                        {
                            sw.Write(e.ImuSamples[array_sonde[i], j, k] + ";");
                        }
                        sw.Write("" + ";");
                    }
                    sw.Write("\n");
                }

                ////ciclo sui campioni
                //for (var k = 0; k < e.ScanNumber; k++)
                //{
                //    //SCRIVO LA BASE TEMPI SOLO PER LA PRIMA SONDA....LE ALTRE SONDE HANNO LA STESSA BASE TEMPI
                //    bw.Write(fifoTimeBuffers[k + fifoTimeBuffers.Length - e.ScanNumber]);
                //    //ciclo sulle sonde
                //    for (var i = 0; i < array_sonde.Length; i++)
                //    {
                //        //ciclo sulle componenti
                //        for (var j = 0; j < 4; j++)
                //        {
                //            bw.Write(e.ImuSamples[array_sonde[i], j, k]);
                //        }
                //    }
                //}                        
            }          
                        
        }


        /// <summary>
        /// Starting from Imu number in base zero, this method renstitutes the index with which the Imu is stored in data structures
        /// </summary>
        public int trovaIndice(int numSondaInBaseZero)
        {
            int indice = -1;

            for (var i = 0; i < array_sonde.Length; i++)
            {
                if (array_sonde[i] == numSondaInBaseZero)
                {
                    indice = i;
                }
            }

            return indice;
        }


        /// <summary>
        /// This method sorts array elements in ascending order
        /// </summary>
        public float[] SelectionSortAscendingOrder(float[] myArray)
        {
            int length = myArray.Length;
            int posmin;
            float tmp;

            for(var i = 0; i < (length-1); i++)
            {
                posmin = i;
                for(var j = (i+1); j < length; j++)
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

    }
}
