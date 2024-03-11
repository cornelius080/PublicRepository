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

namespace pisaSindrome_cometa
{
    /// <summary>
    /// Logica di interazione per MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        internal readonly IDaqSystem _daqSystem;
        imuPlacementWindow subWindow;
        DataCollection dc;        
        imuPlacement[] imuIndexesInZeroBase;
        DispatcherTimer reverseCountdown;
        long startTimeReverseCounter;
        int durataActiveWindow;
        bool _isSettingReferences;
        RotateTransform frontaleTransform, sagittaleTransform, trasversaleTransform;


        public MainWindow()
        {
            InitializeComponent();
            try
            {
                // Create _daqSystem object and assign the event handlers
                _daqSystem = new DaqSystem();
                _daqSystem.StateChanged += Device_StateChanged;
                _daqSystem.DataAvailable += Capture_DataAvailable;


                subWindow = new imuPlacementWindow();
                durataActiveWindow = 5;
                reverseCountdown = new DispatcherTimer();
                _isSettingReferences = true;

                frontaleTransform    = new RotateTransform();
                sagittaleTransform   = new RotateTransform();
                trasversaleTransform = new RotateTransform();

            }
            catch (Exception _exception)
            {
                // Show exceptiton message
                MessageBox.Show(_exception.ToString());
            }
            finally
            {
                // Show device state
                ShowDeviceState(_daqSystem.State);
                DisplayErrorOccurred(_daqSystem.InitialError);
            }

        }


        /// <summary>
        /// This method opens the imuPlacementWindow
        /// </summary>
        private void imuSelectionButton_Click(object sender, RoutedEventArgs e)
        {
            subWindow.Show();
        }


        /// <summary>
        /// This method sets imu references during standing, calculating the rotation matrix for recalibration
        /// </summary>
        private void setReferencesButton_Click(object sender, RoutedEventArgs e)
        {
            double samplingFrequency;
            int[] imuindexes;

            ////////////////////////////////////////////////////////////////////
            //  IMU CONFIGURATION SETTINGS
            ////////////////////////////////////////////////////////////////////
            ISensorConfiguration sensorConfiguration = new SensorConfiguration
            {
                SensorType = SensorType.INERTIAL_SENSOR,
                AccelerometerFullScale = AccelerometerFullScale.g_16,
                GyroscopeFullScale = GyroscopeFullScale.dps_2000
            };

            ICaptureConfiguration captureConf = new CaptureConfiguration();
            captureConf.IMU_AcqType = ImuAcqType.Mixed6xData_142Hz;
            _daqSystem.ConfigureCapture(captureConf);

            _daqSystem.DetectAccelerometerOffset(0);

            
            ////////////////////////////////////////////////////////////////////
            //  DATA COLLECTION DECLARATION
            ////////////////////////////////////////////////////////////////////
            samplingFrequency = 142.0;
            imuIndexesInZeroBase = subWindow.selectedSensorsInZeroBase;
            imuindexes = new int[imuIndexesInZeroBase.Length];
            for (var i = 0; i < imuindexes.Length; i++)
            {
                imuindexes[i] = imuIndexesInZeroBase[i].sensorNumber;
            }
            dc = new DataCollection(imuindexes, durataActiveWindow, samplingFrequency);


            ///////////////////////////////////////////////////////////////////
            // SETTING REFERENCES -> TIMER START
            ///////////////////////////////////////////////////////////////////
            //countdown start
            reverseCountdown.Interval = TimeSpan.FromMilliseconds(100);
            reverseCountdown.Start();
            //system time registration
            startTimeReverseCounter = Environment.TickCount;
            //imu data transmission for recalibration matrix calculus
            _daqSystem.StartCapturing(DataAvailableEventPeriod.ms_100);


        }


        /// <summary>
        /// This method sets imu references during standing, calculating the rotation matrix for recalibration
        /// </summary>
        private void reverseCounter_Tick(object sender, EventArgs e, DataAvailableEventArgs de)
        {
            var elapsed = TimeSpan.FromMilliseconds(Environment.TickCount - startTimeReverseCounter);

            if (elapsed.Seconds <= 0)
            {
                reverseCountdown.Stop();
                _daqSystem.StopCapturing();
                dc.SetImuReferences((subWindow.pelvisComboBox.SelectedIndex - 1), de);
                _isSettingReferences = false;
            }

        }


        /// <summary>
        /// This method starts imu data transmission
        /// </summary>
        private void startCaptureButton_Click(object sender, EventArgs e)
        {
            try
            {
                //#################################
                //START DATA ACQUISITION
                //#################################
                //Represents the time interval between two consecutive DataAvailableEvents events
                _daqSystem.StartCapturing(DataAvailableEventPeriod.ms_100);
            }
            catch (Exception _exception)
            {
                // Show exception message
                MessageBox.Show(_exception.ToString());
            }

        }


        /// <summary>
        /// Method automatically recalled by the imu when new data are available
        /// </summary>
        void Capture_DataAvailable(object sender, DataAvailableEventArgs e)
        {
            //if (InvokeRequired)
            //{
            //    MethodInvoker invoke = () => Capture_DataAvailable(sender, e);
            //    Invoke(invoke);
            //    return;
            //}
            if (Dispatcher.CheckAccess())
            {
                Action invoke = () => Capture_DataAvailable(sender, e);
                invoke();
                return;
            }

            //se non è un'acquisizione per calcolare la matrice di ricalibrazione
            if (_isSettingReferences == false)
            {
                //RIEMPIO I BUFFERS
                dc.RiempiFifoBuffers(e);
                //////if (saveCheckBox.IsChecked == true)
                //////{
                //////    dc.CsvSavingInRealTime(startTime, e);
                //////}
            }


        }

        
        /// <summary>
        /// This method stops data acquisition
        /// </summary>
        private void stopCaptureButton_Click(object sender, EventArgs e)
        {
            try
            {
                // Stop data capture process
                _daqSystem.StopCapturing();

            }
            catch (Exception _exception)
            {
                // Show exception message
                MessageBox.Show(_exception.ToString());
            }         
        }
        

        /// <summary>
        /// This method reveals the imu state change
        /// </summary>
        void Device_StateChanged(object sender, DeviceStateChangedEventArgs e)
        {
            //if (InvokeRequired)
            //{
            //    MethodInvoker invoke = () => Device_StateChanged(sender, e);
            //    Invoke(invoke);
            //    return;
            //}

            if (Dispatcher.CheckAccess())
            {
                Action invoke = () => Device_StateChanged(sender, e);
                invoke();
                return;
            }
            // Show the new device state
            ShowDeviceState(e.State);

        }
        

        /// <summary>
        /// This method shows the imu state
        /// </summary>
        protected void ShowDeviceState(DeviceState newState)
        {
            switch (newState)
            {
                case DeviceState.Idle:
                    //Capture controls
                    startCaptureButton.IsEnabled = true;
                    stopCaptureButton.IsEnabled = false;
                    break;
                case DeviceState.Capturing:
                    //Capture controls
                    startCaptureButton.IsEnabled = false;
                    stopCaptureButton.IsEnabled = true;
                    break;
                case DeviceState.NotConnected:
                    startCaptureButton.IsEnabled = false;
                    stopCaptureButton.IsEnabled = false;
                    string s1 = "DeviceState.NotConnected";
                    MessageBox.Show(s1.ToString());
                    break;
                case DeviceState.CommunicationError:
                    startCaptureButton.IsEnabled = false;
                    stopCaptureButton.IsEnabled = false;
                    string s2 = "DeviceState.CommunicationError";
                    MessageBox.Show(s2.ToString());
                    break;
                case DeviceState.InitializingError:
                    startCaptureButton.IsEnabled = false;
                    stopCaptureButton.IsEnabled = false;
                    string s3 = "DeviceState.InitializingError";
                    MessageBox.Show(s3.ToString());
                    break;
                case DeviceState.UpdatingFirmware:
                    string s4 = "DeviceState.UpdatingFirmware";
                    MessageBox.Show(s4.ToString());
                    break;
                case DeviceState.Initializing:
                    string s5 = "DeviceState.Initializing";
                    MessageBox.Show(s5.ToString());
                    break;
            }
        }


        /// <summary>
        /// This method shows the device error
        /// </summary>
        private void DisplayErrorOccurred(DeviceError error)
        {
            // Display device error code
            MessageBox.Show(error.ToString());
        }






    }
}
