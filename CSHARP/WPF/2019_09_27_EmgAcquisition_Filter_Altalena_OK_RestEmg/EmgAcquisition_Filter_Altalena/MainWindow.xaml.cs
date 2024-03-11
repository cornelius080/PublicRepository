using System;
using System.Collections.Generic;
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
using System.Windows.Threading;
using Waveplus.DaqSys;
using Waveplus.DaqSys.Definitions;
using Waveplus.DaqSysInterface;
using WaveplusLab.Shared.Definitions;
using System.Windows.Forms.DataVisualization;
using System.Windows.Forms.DataVisualization.Charting;
using System.Drawing;
using System.IO;
using eljambaLibrary;
using System.Diagnostics;



namespace EmgAcquisition_Filter_Altalena
{
    /// <summary>
    /// Logica di interazione per MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        internal readonly IDaqSystem _daqSystem;
        RotateTransform myRotation;
        DateTime restPeriod;
        Stopwatch crono;
        DispatcherTimer restEmgTimer, rmsTimer;
        int emgUpNumber, emgDownNumber, envelopeWinSize;
        double upRms, downRms, inclinazione, outcomeIndex, meanRestEmgUp, meanRestEmgDown;
        double[] timeEmg, emgUpSignal, emgDownSignal, emgUpEnvelope, emgDownEnvelope;
        string[] emgString;
        string fullPathFilename;
        UsefulMethods usefulMethods;
        SignalProcessing signalProcessing;
        Mathematics myMathClass;
        List<double> restEmgUp, restEmgDown;


        
        public MainWindow()
        {
            InitializeComponent();
            try
            {
                /////////////////////////////////////////////////////////
                // DAQ AND PROCESSING
                /////////////////////////////////////////////////////////
                // Create _daqSystem object and assign the event handlers
                _daqSystem = new DaqSystem();
                _daqSystem.StateChanged += Device_StateChanged;
                _daqSystem.DataAvailable += Capture_DataAvailable;
                //i buffer devono contenere 500 nuovi campioni ogni 1s
                timeEmg = new double[1500];
                emgUpSignal = new double[timeEmg.Length];
                emgDownSignal = new double[timeEmg.Length];
                emgUpEnvelope = new double[timeEmg.Length];
                emgDownEnvelope = new double[timeEmg.Length];
                restEmgUp = new List<double>();
                restEmgDown = new List<double>();
                meanRestEmgUp = 0.0;
                meanRestEmgDown = 0.0;
                envelopeWinSize = 10;



                ///////////////////////////////////////////////
                // OPERATION ON TIME
                ///////////////////////////////////////////////
                restEmgTimer = new DispatcherTimer();
                restEmgTimer.Interval = TimeSpan.FromMilliseconds(100);
                restEmgTimer.Tick += new EventHandler(RestEmgTimer_Tick);

                rmsTimer = new DispatcherTimer();
                rmsTimer.Interval = TimeSpan.FromMilliseconds(100);
                rmsTimer.Tick += new EventHandler(RmsTimer_Tick);

                crono = new Stopwatch();



                ///////////////////////////////////////////////
                // GRAPHICS
                ///////////////////////////////////////////////
                StartCaptureButton.IsEnabled = false;
                StopCaptureButton.IsEnabled = false;
                RestartCaptureButton.IsEnabled = false;
                RestEmgButton.IsEnabled = false;

                int xAxisFontSize, yAxisFontSize;
                xAxisFontSize = 14;
                yAxisFontSize = 14;
                graficoEmgUp.InizializzaGrafico("TIME (S)", "EMG (uV)", xAxisFontSize, yAxisFontSize);
                graficoEmgDown.InizializzaGrafico("TIME (S)", "EMG (uV)", xAxisFontSize, yAxisFontSize);

                myRotation = new RotateTransform();
                barraAltalenaImg.RenderTransform = myRotation;



                ///////////////////////////////////////////////
                // DLL EXTERNAL CLASS
                ///////////////////////////////////////////////
                usefulMethods = new UsefulMethods();
                signalProcessing = new SignalProcessing();
                myMathClass = new Mathematics();



                ///////////////////////////////////////////////
                // FILE INPUT / OUTPUT
                ///////////////////////////////////////////////
                fullPathFilename = Environment.CurrentDirectory + @"\" + myWindow.Title + "_SelectedSensors.csv";
                
            }
            catch (Exception _exception)
            {
                // Show exceptiton message
                MessageBox.Show(_exception.ToString());
            }

        }

        
        private void MainWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            // Remove the event handlers from _daqSystem object and dispose it
            _daqSystem.StateChanged -= Device_StateChanged;
            _daqSystem.DataAvailable -= Capture_DataAvailable;
            _daqSystem.Dispose();
        }

                
        private void ConfigurationButton_Click(object sender, RoutedEventArgs e)
        {
            emgString = new string[]
            {
                (string)emgUpComboBox.SelectedItem,
                (string)emgUpComboBox.SelectedItem + "_ENVELOPE",
                (string)emgDownComboBox.SelectedItem,
                (string)emgDownComboBox.SelectedItem + "_ENVELOPE"
            };

            if (_daqSystem.State == DeviceState.NotConnected)
            {
                MessageBox.Show("DEVICE NOT CONNECTED");
                RestartCaptureButton.IsEnabled = true;
                RestartCaptureButton.Click += RestartCaptureButton_Click;
                return;
            }

            ISensorConfiguration sensorConfiguration = new SensorConfiguration
            {
                SensorType = SensorType.EMG_SENSOR,
                AccelerometerFullScale = AccelerometerFullScale.g_16
            };

            if (emgUpNumber != 0 && emgDownNumber != 0)
            {
                _daqSystem.ConfigureSensor(sensorConfiguration, emgUpNumber);
                _daqSystem.ConfigureSensor(sensorConfiguration, emgDownNumber);
                _daqSystem.DetectAccelerometerOffset(0);
                myLabel.Content = "EMG CONFIGURED";

                // CREA SERIE
                string[] tempVar1;
                tempVar1 = new string[] { emgString[0], emgString[1] };
                graficoEmgUp.CreaSerie(tempVar1);

                string[] tempVar2;
                tempVar2 = new string[] { emgString[2], emgString[3] };
                graficoEmgDown.CreaSerie(tempVar2);

                RestartCaptureButton.IsEnabled = true;
                StartCaptureButton.IsEnabled = true;

                upRmsTextBox_Copy.Text = "EMG_" + emgUpNumber.ToString();
                downRmsTextBox_Copy.Text = "EMG_" + emgDownNumber.ToString();
            }
            else if (emgUpNumber != 0 && emgDownNumber == 0)
            {
                _daqSystem.ConfigureSensor(sensorConfiguration, emgUpNumber);
                _daqSystem.DetectAccelerometerOffset(0);
                myLabel.Content = "EMG UP CONFIGURED";

                // CREATE THE SERIE
                string[] tempVar1;
                tempVar1 = new string[] { emgString[0], emgString[1] };
                graficoEmgUp.CreaSerie(tempVar1);

                RestartCaptureButton.IsEnabled = true;
                StartCaptureButton.IsEnabled = true;

                upRmsTextBox_Copy.Text = "EMG_" + emgUpNumber.ToString();
            }
            else if (emgDownNumber != 0 && emgUpNumber == 0)
            {
                _daqSystem.ConfigureSensor(sensorConfiguration, emgDownNumber);
                _daqSystem.DetectAccelerometerOffset(0);
                myLabel.Content = "EMG DOWN CONFIGURED";

                //CREA SERIE
                string[] tempVar2;
                tempVar2 = new string[] { emgString[2], emgString[3] };
                graficoEmgDown.CreaSerie(tempVar2);

                RestartCaptureButton.IsEnabled = true;
                StartCaptureButton.IsEnabled = true;

                downRmsTextBox_Copy.Text = "EMG_" + emgDownNumber.ToString();
            }
            else if (emgUpNumber == 0 && emgDownNumber == 0)
                myLabel.Content = "SELECT EMG";


        }

                
        private void StartCaptureButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                int[] selectedEmg = new int[] { emgUpNumber, emgDownNumber };

                DisableDaqSensors(usefulMethods.RemoveZerosFromArray(selectedEmg));                
                usefulMethods.SaveSelectedSensorsInCSVFile(fullPathFilename, "EMG_UP" + ";" + "EMG_DOWN" + ";", selectedEmg);

                _daqSystem.StartCapturing(DataAvailableEventPeriod.ms_100);
                //rmsTimer.Start();
                //crono.Restart();

                emgUpComboBox.IsEnabled = false;
                emgDownComboBox.IsEnabled = false;
                ConfigurationButton.IsEnabled = false;
                StartCaptureButton.IsEnabled = false;
                StopCaptureButton.IsEnabled = true;
                RestEmgButton.IsEnabled = true;
                RestartCaptureButton.IsEnabled = true;
                myLabel.Content = "START";
            }
            catch (Exception _exception)
            {
                // Show exception message
                MessageBox.Show(_exception.ToString());
            }

        }

                        
        void Capture_DataAvailable(object sender, DataAvailableEventArgs e)
        {
            if (Dispatcher.CheckAccess())
            {
                void Invoke() => Capture_DataAvailable(sender, e);

                Invoke();
                return;
            }

            FillFifoBuffers(e);
        }
        
       
        private void RmsTimer_Tick(object sender, EventArgs e)
        {
            if (emgUpNumber != 0 && emgDownNumber != 0)
            {
                /////////////////////////////////////////////////////////////////////////////
                // 'PLOT' TAB UPDATE
                /////////////////////////////////////////////////////////////////////////////
                graficoEmgUp.AggiornaContenutoSerie(emgString[0], timeEmg, emgUpSignal);
                graficoEmgUp.AggiornaContenutoSerie(emgString[1], timeEmg, emgUpEnvelope);
                graficoEmgUp.UpdateAxisX(timeEmg);
                myLabel.Content = "CAPTURING";

                graficoEmgDown.AggiornaContenutoSerie(emgString[2], timeEmg, emgDownSignal);
                graficoEmgDown.AggiornaContenutoSerie(emgString[3], timeEmg, emgDownEnvelope);
                graficoEmgDown.UpdateAxisX(timeEmg);
                myLabel.Content = "CAPTURING";


                /////////////////////////////////////////////////////////////////////////////
                // 'ANIMATION' TAB UPDATE
                /////////////////////////////////////////////////////////////////////////////
                upRms = Math.Round(signalProcessing.SignalRMS(emgUpEnvelope), 1);
                downRms = Math.Round(signalProcessing.SignalRMS(emgDownEnvelope), 1);
                
                //outcomeIndex = 0;
                //if (crono.ElapsedMilliseconds >= 1000)
                //    outcomeIndex = -1 + (downRms / upRms);

                outcomeIndex = -1 + (downRms / upRms);
                inclinazione = (180.0 / Math.PI) * Math.Atan(outcomeIndex);
                if (inclinazione > 50 || inclinazione < -50)
                    inclinazione = 50;

                //qui è un valore puntuale assunto da myRotation.Angle
                myRotation.Angle = -1 * inclinazione; //il meno è per le rotazioni antiorarie

                upRmsTextBox_Copy.Text = "EMG_" + emgUpNumber.ToString() + Environment.NewLine + upRms.ToString();
                downRmsTextBox_Copy.Text = "EMG_" + emgDownNumber.ToString() + Environment.NewLine + downRms.ToString();
            }
            else if (emgUpNumber != 0 && emgDownNumber == 0)
            {
                /////////////////////////////////////////////////////////////////////////////
                // 'PLOT' TAB UPDATE
                /////////////////////////////////////////////////////////////////////////////
                graficoEmgUp.AggiornaContenutoSerie(emgString[0], timeEmg, emgUpSignal);
                graficoEmgUp.AggiornaContenutoSerie(emgString[1], timeEmg, emgUpEnvelope);
                graficoEmgUp.UpdateAxisX(timeEmg);
                myLabel.Content = "CAPTURING";


                /////////////////////////////////////////////////////////////////////////////
                // 'ANIMATION' TAB UPDATE
                /////////////////////////////////////////////////////////////////////////////
                upRms = Math.Round(signalProcessing.SignalRMS(emgUpEnvelope), 1);
                upRmsTextBox_Copy.Text = "EMG_" + emgUpNumber.ToString() + Environment.NewLine + upRms.ToString();
            }
            else if (emgUpNumber == 0 && emgDownNumber != 0)
            {
                /////////////////////////////////////////////////////////////////////////////
                // 'PLOT' TAB UPDATE
                /////////////////////////////////////////////////////////////////////////////
                graficoEmgDown.AggiornaContenutoSerie(emgString[2], timeEmg, emgDownSignal);
                graficoEmgDown.AggiornaContenutoSerie(emgString[3], timeEmg, emgDownEnvelope);
                graficoEmgDown.UpdateAxisX(timeEmg);
                myLabel.Content = "CAPTURING";


                /////////////////////////////////////////////////////////////////////////////
                // 'ANIMATION' TAB UPDATE
                /////////////////////////////////////////////////////////////////////////////
                downRms = Math.Round(signalProcessing.SignalRMS(emgDownEnvelope), 1);
                downRmsTextBox_Copy.Text = "EMG_" + emgDownNumber.ToString() + Environment.NewLine + downRms.ToString();
            }

            
        }

                
        private void FillFifoBuffers(DataAvailableEventArgs e)
        {
            double emgTc = Math.Pow(500, -1); // frequenza di campionamento 500Hz
            int stepEmg = 4;


            if (emgUpNumber != 0)
            {
                for (var i = 0; i < emgUpSignal.Length - 40; i++)
                    emgUpSignal[i] = emgUpSignal[i + 40];

                int passo = 0;
                for (var i = emgUpSignal.Length - 40; i < emgUpSignal.Length; i++)
                {
                    emgUpSignal[i] = e.Samples[emgUpNumber - 1, passo] - meanRestEmgUp;
                    passo += stepEmg;
                }

                // ENVELOPE
                emgUpEnvelope = signalProcessing.SignalEnvelope(emgUpSignal, envelopeWinSize);
            }
            

            if (emgDownNumber != 0)
            {
                for (var i = 0; i < emgDownSignal.Length - 40; i++)
                    emgDownSignal[i] = emgDownSignal[i + 40];

                int passo = 0;
                for (var i = emgDownSignal.Length - 40; i < emgDownSignal.Length; i++)
                {
                    emgDownSignal[i] = e.Samples[emgDownNumber - 1, passo] - meanRestEmgDown;
                    passo += stepEmg;
                }
                
                // ENVELOPE
                emgDownEnvelope = signalProcessing.SignalEnvelope(emgDownSignal, envelopeWinSize);
            }


            //////////////////////////////////////
            // TIMESTAMPS
            //////////////////////////////////////
            for (var i = 0; i < timeEmg.Length - 40; i++)
                timeEmg[i] = timeEmg[i + 40];

            for (var i = timeEmg.Length - 40; i < timeEmg.Length; i++)
                timeEmg[i] = timeEmg[i - 1] + emgTc;


        }


        private void RestEmgButton_Click(object sender, RoutedEventArgs e)
        {
            RestEmgButton.IsEnabled = false;
            restPeriod = DateTime.Now.AddSeconds(3);

            restEmgTimer.Start();            
        }


        private void RestEmgTimer_Tick(object sender, EventArgs e)
        {
            TimeSpan elapsedTime = restPeriod - DateTime.Now;

            if (elapsedTime.TotalSeconds <= 0)
            {
                restEmgTimer.Stop();
                rmsTimer.Start();

                meanRestEmgUp = myMathClass.CalculateMean(restEmgUp.ToArray());
                meanRestEmgDown = myMathClass.CalculateMean(restEmgDown.ToArray());
            }
            else
            {
                // calcola la media dei campioni letti dagli emgSignal
                for(var i=0; i<emgUpSignal.Length; i++)
                {
                    restEmgUp.Add(emgUpSignal[i]);
                    restEmgDown.Add(emgDownSignal[i]);
                }
            }
            
        }


        private void StopCaptureButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // Stop data capture process
                _daqSystem.StopCapturing();
                rmsTimer.Stop();
                //crono.Stop();
                myLabel.Content = "STOP";


                emgUpComboBox.IsEnabled = true;
                emgDownComboBox.IsEnabled = true;
                ConfigurationButton.IsEnabled = true;

                
                StartCaptureButton.IsEnabled = true;


                StopCaptureButton.IsEnabled = false;
                RestartCaptureButton.IsEnabled = true;
            }
            catch (Exception _exception)
            {
                // Show exception message
                MessageBox.Show(_exception.ToString());
            }
        }

        
        private void RestartCaptureButton_Click(object sender, RoutedEventArgs e)
        {
            System.Diagnostics.Process.Start(Application.ResourceAssembly.Location);
            Application.Current.Shutdown();
        }





       
        private void emgUpComboBox_Loaded(object sender, RoutedEventArgs e)
        {
            int[] vettore = usefulMethods.CheckSelectedSensorsFromCSVFile(fullPathFilename);

            List<string> data = new List<string>();
            data.Add("SELECT EMG 1");
            data.Add("EMG_1"); data.Add("EMG_2"); data.Add("EMG_3"); data.Add("EMG_4");
            data.Add("EMG_5"); data.Add("EMG_6"); data.Add("EMG_7"); data.Add("EMG_8");
            data.Add("EMG_9"); data.Add("EMG_10"); data.Add("EMG_11"); data.Add("EMG_12");
            data.Add("EMG_13"); data.Add("EMG_14"); data.Add("EMG_15"); data.Add("EMG_16");

            var emgUpComboBox = sender as ComboBox;
            emgUpComboBox.ItemsSource = data;
            emgUpComboBox.SelectedIndex = vettore[0];
            emgUpNumber = emgUpComboBox.SelectedIndex;
        }


        private void emgDownComboBox_Loaded(object sender, RoutedEventArgs e)
        {
            int[] vettore = usefulMethods.CheckSelectedSensorsFromCSVFile(fullPathFilename);

            List<string> data = new List<string>();
            data.Add("SELECT EMG 2");
            data.Add("EMG_1"); data.Add("EMG_2"); data.Add("EMG_3"); data.Add("EMG_4");
            data.Add("EMG_5"); data.Add("EMG_6"); data.Add("EMG_7"); data.Add("EMG_8");
            data.Add("EMG_9"); data.Add("EMG_10"); data.Add("EMG_11"); data.Add("EMG_12");
            data.Add("EMG_13"); data.Add("EMG_14"); data.Add("EMG_15"); data.Add("EMG_16");


            var emgDownComboBox = sender as ComboBox;
            emgDownComboBox.ItemsSource = data;
            emgDownComboBox.SelectedIndex = vettore[1];
            emgDownNumber = emgDownComboBox.SelectedIndex;

        }


        private void emgUpComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            emgUpNumber = emgUpComboBox.SelectedIndex;
        }


        private void emgDownComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            emgDownNumber = emgDownComboBox.SelectedIndex;
        }


        private void DisableDaqSensors(int[] notToBeDisabledSensors)
        {
            int[] array = new int[32]; // vettore che contiene gli indici di tutte i sensori, selezionati e non 
            for (var i = 0; i < array.Length; i++)
                array[i] = i + 1;

            int[] newSelectedSensors; //uguale al notToBeDisabledSensors, ma ordinato in ordine crescente
            int[] disabledSensors = new int[array.Length - notToBeDisabledSensors.Length];

            newSelectedSensors = usefulMethods.SelectionSortAscendingOrder(notToBeDisabledSensors);

            int start = 0;
            for (var i = 0; i < array.Length; i++)
            {
                int cont = 0;
                for (var j = 0; j < newSelectedSensors.Length; j++)
                {
                    if (array[i] != newSelectedSensors[j])
                        cont++;
                }

                if (cont == newSelectedSensors.Length)
                {
                    disabledSensors[start] = array[i];
                    start++;
                }
            }

            for (var i = 0; i < disabledSensors.Length; i++)
                _daqSystem.DisableSensor(disabledSensors[i]);

        }


        void Device_StateChanged(object sender, DeviceStateChangedEventArgs e)
        {
            if (Dispatcher.CheckAccess())
            {
                void Invoke() => Device_StateChanged(sender, e);
                Invoke();
                return;
            }
        }




    }
}
