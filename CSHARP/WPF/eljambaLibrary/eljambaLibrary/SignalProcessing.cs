using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;



namespace eljambaLibrary
{
    public class SignalProcessing
    {
        Mathematics myMathClass = new Mathematics();


        /// <summary>
        /// Returns a filtered array using a moving average window.
        /// </summary>
        /// <param name="myArray"> Input array of double elements </param>
        /// <param name="windowLength"> Length of window. Min is set to 3. Max is set to (2*l)-1. </param>
        /// <returns> Output array of double elements. </returns>
        public double[] MovingAverageFilter(double[] myArray, int windowLength)
        {
            int l = myArray.Length;
            int minWindowLength = 3;
            int maxWindowLength = (2 * l) - 1;
            double[] filteredArray = new double[l];

            // se la lunghezza della finestra è pari, diventa dispari 
            if (windowLength % 2 == 0)
                windowLength = windowLength - 1;


            if (windowLength < minWindowLength)
                windowLength = minWindowLength;
            else if (windowLength > maxWindowLength)
                windowLength = maxWindowLength;

            ////////IMPLEMENTAZIONE RICORSIVA 
            ////////Steven Smith - Moving Average Filters (NON FUNZIONA!)
            ////////y[i] = y[i-1] + x[i+p] - x[i-q];
            //////int p = (int)((windowLength - 1) / 2);
            //////int q = (int)((windowLength + 1) / 2);

            //////double[] temp = new double[3];
            //////for (var i = 0; i < q; i++)
            //////{
            //////    for (var j = i; j < i + 3; j++)
            //////        temp[j - i] = myArray[i];

            //////    filteredArray[i] = CalculateMean(temp);
            //////}
            //////for (var i = q; i < l - p; i++)
            //////    filteredArray[i] = filteredArray[i - 1] + myArray[i + p] - myArray[i - q];
            //////for (var i = l - p; i < l; i++)
            //////    filteredArray[i] = myArray[i];


            //IMPLEMENTAZIONE NON RICORSIVA
            double[] window = new double[windowLength];
            for (var i = 0; i < l - windowLength; i++)
            {
                for (var j = i; j < i + windowLength; j++)
                    window[j - i] = myArray[j];

                filteredArray[i] = myMathClass.CalculateMean(window);
            }



            return filteredArray;
        }


        /// <summary>
        /// Returns the Root Mean Square of the signal.
        /// </summary>
        /// <param name="myArray"> Input array of double elements. </param>
        /// <returns> Output array of double elements. </returns>
        public double SignalRMS(double[] myArray)
        {
            double rms;
            double[] arrayQuadro = new double[myArray.Length];
            for (var i = 0; i < arrayQuadro.Length; i++)
                arrayQuadro[i] = Math.Pow(myArray[i], 2);

            double media = myMathClass.CalculateMean(arrayQuadro);
            rms = Math.Pow(media, 0.5);

            return rms;
        }



        /// <summary>
        /// Returns the envelope sequence of the input array. 
        /// </summary>
        /// <param name="myArray">nSamples x 1 input array</param>
        /// <param name="windowSize">Dimensione della finestra utilizzata per segmentare (senza overlap) il segnale </param>
        /// <returns> Output array of double elements. </returns>
        public double[] SignalEnvelope(double[] myArray, int windowSize)
        {
            double[] myArrayAbs = new double[myArray.Length];
            double[] myArrayAbsMax = new double[myArray.Length];
            double[] myArrayEnvelope = new double[myArray.Length];
            double[] window = new double[windowSize];
            double myMax;
            int stopSample;


            // Calcolo il valore assoluto dell'array
            myArrayAbs = myMathClass.ArrayAbs(myArray);


            // Divido la sequenza raddrizzata in finestre senza overlap; per ciascuna finestra calcolo il massimo
            // Ogni campione della finestra considerata viene sostituito dal suo massimo
            stopSample = windowSize * (int) Math.Floor((double) myArray.Length / windowSize);
            stopSample = stopSample - windowSize + 1;
            for(int startSample = 0; startSample < stopSample; startSample += windowSize)
            {
                Array.Copy(myArrayAbs, startSample, window, 0, window.Length);
                myMax = myMathClass.ArrayMax(window);
                //window = Enumerable.Repeat(myMax, windowSize).ToArray();
                //Array.Copy(window, 0, myArrayAbsMax, startSample, windowSize);
                for (var i = startSample; i < startSample + windowSize; i++)
                    myArrayAbsMax[i] = myMax;
            }
            window = new double[myArrayAbs.Length - stopSample];
            Array.Copy(myArrayAbs, stopSample, window, 0, window.Length);
            myMax = myMathClass.ArrayMax(window);
            for (var i = stopSample; i < myArrayAbsMax.Length; i++)
                myArrayAbsMax[i] = myMax;


            // Filtraggio passa basso del segnale scalettato
            myArrayEnvelope = MovingAverageFilter(myArrayAbsMax, windowSize);

            return myArrayEnvelope;
        }


    }
}
