using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace pisaSindrome_cometa
{
    public struct imuPlacement
    {
        public int sensorNumber;        
        public int sensorIndexInDataStructure;
        public string anatomicalLandmark;

        public imuPlacement(int numeroSensore, int indiceSensoreNellaStrutturaDati, string puntoAnatomico)
        {
            sensorNumber = numeroSensore;
            sensorIndexInDataStructure = indiceSensoreNellaStrutturaDati;
            anatomicalLandmark = puntoAnatomico;
        }
    }

    /// <summary>
    /// Logica di interazione per imuPlacementWindow.xaml
    /// </summary>
    public partial class imuPlacementWindow : Window
    {
        public imuPlacement[] selectedSensorsInZeroBase; //i numeri delle imu vengono indicizzate in base zero



        public imuPlacementWindow()
        {
            InitializeComponent();
        }



        private void confirmButton_Click(object sender, RoutedEventArgs e)
        {
            if (pelvisComboBox.SelectedIndex != 0 || pelvisComboBox.SelectedIndex != -1)
            {
                MessageBox.Show("PLEASE SELECT THE IMU ON PELVIS AND CONFIRM");
                return;
            }
            else
            {
                int contaZeri = 0;
                imuPlacement[] temp       = new imuPlacement[4];
                selectedSensorsInZeroBase = new imuPlacement[4];
                int[] temp1;


                //per l'imu 13 il selected index vale 13 (successivamente, in selectedSensorsInZeroBase, viene indicizzato in base zero, ovvero 12)
                //se l'imu non viene selezionata il selected index vale -1
                //se viene selezionato NONE il selected index vale 0
                temp[0].sensorNumber = trunkComboBox.SelectedIndex;   temp[0].anatomicalLandmark = "TRUNK";    temp[0].sensorIndexInDataStructure = -1;
                temp[1].sensorNumber = pelvisComboBox.SelectedIndex;  temp[1].anatomicalLandmark = "PELVIS";   temp[1].sensorIndexInDataStructure = -1;
                temp[2].sensorNumber = shankComboBox.SelectedIndex;   temp[2].anatomicalLandmark = "SHANK";    temp[2].sensorIndexInDataStructure = -1;
                temp[3].sensorNumber = thighComboBox.SelectedIndex;   temp[3].anatomicalLandmark = "THIGH";    temp[3].sensorIndexInDataStructure = -1;
                

                //conto il numero di 0 ('NONE') e di -1 ('')
                for (var i = 0; i < temp.Length; i++)
                {
                    if (temp[i].sensorNumber == 0 || temp[i].sensorNumber == -1)
                    {
                        contaZeri++;
                    }
                }

                //copio i numeri e le etichette dei soli sensori selezionati
                selectedSensorsInZeroBase = new imuPlacement[temp.Length - contaZeri];
                int j = 0;
                for (var i = 0; i < temp.Length; i++)
                {
                    if (temp[i].sensorNumber != 0 && temp[i].sensorNumber != -1)
                    {
                        selectedSensorsInZeroBase[j].sensorNumber = temp[i].sensorNumber - 1;
                        selectedSensorsInZeroBase[j].anatomicalLandmark = temp[i].anatomicalLandmark;
                        j++;
                    }
                }

                //copio i numeri dei sensori selezionati in un vettore ausiliario, e ordino i suoi elementi in ordine crescente
                temp1 = new int[selectedSensorsInZeroBase.Length];
                for(var i=0; i<temp1.Length; i++)
                {
                    temp1[i] = selectedSensorsInZeroBase[i].sensorNumber;
                }
                temp1 = SelectionSortAscendingOrder(temp1);

                //assegno gli indici con cui le imu sono state e verranno immagazzinate nelle strutture dati
                for (var i=0; i<temp1.Length; i++)
                {
                    selectedSensorsInZeroBase[i].sensorIndexInDataStructure = trovaIndice(temp1[i], temp1);
                }
            }            

            //getSelectedSensors();
            
        }


        /// <summary>
        /// Saves an .adf file in the folder bin\Debug\ImuPlacements
        /// </summary>
        private void createAdfFile()
        {
            string data = DateTime.Now.ToString("dd-MM-yyyy hh.mm.ss-");
            string path = System.AppDomain.CurrentDomain.BaseDirectory;
            var filePath = path + @"\ImuPlacements";
            if (!Directory.Exists(filePath))
            {
                System.IO.DirectoryInfo di = System.IO.Directory.CreateDirectory(filePath);
            }

            string emptyString = "";
            imuPlacement[] myStruct = new imuPlacement[4];
            myStruct[0].sensorNumber = -10;     myStruct[0].anatomicalLandmark = "TRUNK";
            myStruct[1].sensorNumber = -10;     myStruct[1].anatomicalLandmark = "PELVIS";
            myStruct[2].sensorNumber = -10;     myStruct[2].anatomicalLandmark = "SHANK";
            myStruct[3].sensorNumber = -10;     myStruct[3].anatomicalLandmark = "THIGH";
            for(var i = 0; i < selectedSensorsInZeroBase.Length; i++)
            {
                for (var j = 0; j < myStruct.Length; j++)
                {
                    if(string.Compare(selectedSensorsInZeroBase[i].anatomicalLandmark, myStruct[j].anatomicalLandmark) == 1)
                    {
                        myStruct[j].sensorNumber = selectedSensorsInZeroBase[i].sensorNumber;
                    }
                }
            }


            using (StreamWriter sw = new StreamWriter(filePath + @"\" + data + "ImuPlacements.adf"))  // True to append data to the file; false to overwrite the file
            {
                for (var i = 0; i < myStruct.Length; i++)
                {
                    if(myStruct[i].sensorNumber == -10)
                    {
                        sw.WriteLine(myStruct[i].anatomicalLandmark);
                        sw.WriteLine(emptyString);
                    }
                    else
                    {
                        sw.WriteLine(myStruct[i].anatomicalLandmark);
                        sw.WriteLine(myStruct[i].sensorNumber);
                    }
                }
                sw.WriteLine("[End]");
            }

        }


        private void createAdfFileButton_Click(object sender, RoutedEventArgs e)
        {
            createAdfFile();
            string path = System.AppDomain.CurrentDomain.BaseDirectory;
            var filePath = path + @"\ImuPlacements";
            string stringa = "Adf file saved in " + filePath;
            MessageBox.Show(stringa);
        }


        /// <summary>
        /// Returns the struct with the selected sensors in base zero and respective anatomical landmarks
        /// </summary>
        public imuPlacement[] getSelectedSensors()
        {
            return selectedSensorsInZeroBase;
        }


        /// <summary>
        /// This method sorts array elements in ascending order
        /// </summary>
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
        /// Starting from Imu number in base zero, this method renstitutes the index with which the Imu is stored in data structures
        /// </summary>
        public int trovaIndice(int numSondaInBaseZero, int[] sensorNumberInAscendingOrder)
        {
            int indice = -1;

            for (var i = 0; i < sensorNumberInAscendingOrder.Length; i++)
            {
                if (sensorNumberInAscendingOrder[i] == numSondaInBaseZero)
                {
                    indice = i;
                }
            }

            return indice;
        }







    }
}
