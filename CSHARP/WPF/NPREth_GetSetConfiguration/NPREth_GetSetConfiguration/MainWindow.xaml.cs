using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
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


namespace NPREth_GetSetConfiguration
{    
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        NPREth_Connect nprConnection = null;
        DispatcherTimer timer = null; //il timer crea un evento per l'aggiornamento dell'interfaccia
        readonly int timerInterval; //periodo di aggiornamento dell'interfaccia (ms)

        public MainWindow()
        {
            InitializeComponent();

            timerInterval = 500;
            timer = new DispatcherTimer();
            timer.Interval = TimeSpan.FromMilliseconds(timerInterval);
            //timer.Tick += timer_Tick;
        }

        private void ConnectButton_Click(object sender, RoutedEventArgs e)
        {
            if (String.Equals(ipAddressGetConfig.Text, ""))
                nprConnection = new NPREth_Connect();
            else
                nprConnection = new NPREth_Connect(ipAddressGetConfig.Text);


            nprConnection.StartConnection();
            //timer.Start();

            SetInterface();
            Thread.Sleep(500);
            //GET DEVICE PARAMETERS
            ipAddressGetConfig.Text = nprConnection.deviceParameters.IP;
            macAddressGetConfig.Text = nprConnection.deviceParameters.MAC;
            gwAddressGetConfig.Text = nprConnection.deviceParameters.GW;
            subMaskGetConfig.Text = nprConnection.deviceParameters.SUBNET_MASK;
            typeTextBox.Text = nprConnection.deviceParameters.DEVICE_TYPE;
            revTextBox.Text = nprConnection.deviceParameters.HW_FW_CONF;

            //COPY CONFIGURATION FROM GET TO SET SECTION
            ipAddressSetConfig.Text = ipAddressGetConfig.Text;
            macAddressSetConfig.Text = macAddressGetConfig.Text;
            gwAddressSetConfig.Text = gwAddressGetConfig.Text;
            subMaskSetConfig.Text = subMaskGetConfig.Text;

        }

        ///// <summary>
        ///// Event called by the timer tick every timerInterval milliseconds elapsed.
        ///// </summary>
        //private void timer_Tick(object sender, EventArgs e)
        //{
        //    //ipAddressGetConfig.Text = nprConnection.deviceParameters.IP;
        //    //macAddressGetConfig.Text = nprConnection.deviceParameters.MAC;
        //    //gwAddressGetConfig.Text = nprConnection.deviceParameters.GW;
        //    //subMaskGetConfig.Text = nprConnection.deviceParameters.SUBNET_MASK;
        //    //typeTextBox.Text = nprConnection.deviceParameters.DEVICE_TYPE;
        //    //revTextBox.Text = nprConnection.deviceParameters.HW_FW_CONF;

        //    ////COPY CONFIGURATION FROM GET TO SET SECTION
        //    //ipAddressSetConfig.Text = ipAddressGetConfig.Text;
        //    //macAddressSetConfig.Text = macAddressGetConfig.Text;
        //    //gwAddressSetConfig.Text = gwAddressGetConfig.Text;
        //    //subMaskSetConfig.Text = subMaskGetConfig.Text;
        //}

        private void SetConfigurationButton_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Appying changes...", "WAIT");

            nprConnection.netParameters.SetNetParameters(macAddressSetConfig.Text, ipAddressSetConfig.Text, subMaskSetConfig.Text, gwAddressSetConfig.Text);

            MessageBox.Show("To apply the changes, shutdown and restart the device.", "REMINDER");
        }

        private void SetDefaultConfigurationButton_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Appying changes...", "WAIT");

            nprConnection.netParameters.SetNetParameters(nprConnection.netParameters.DEFAULT_MAC, nprConnection.netParameters.DEFAULT_IP, nprConnection.netParameters.DEFAULT_SUBNET_MASK, nprConnection.netParameters.DEFAULT_GW);

            MessageBox.Show("To apply the changes, shutdown and restart the device.", "REMINDER");
        }

        private void DisconnectButton_Click(object sender, RoutedEventArgs e)
        {
            //timer.Stop();
            ResetInterface();
            nprConnection.StopConnection();

        }

        private void SetInterface()
        {
            //ENABLING WINDOWS CONTROLS
            typeTextBox.IsEnabled = true;
            revTextBox.IsEnabled = true;
            ipAddressGetConfig.IsEnabled = true;
            macAddressGetConfig.IsEnabled = true;
            gwAddressGetConfig.IsEnabled = true;
            subMaskGetConfig.IsEnabled = true;
            ipAddressSetConfig.IsEnabled = true;
            macAddressSetConfig.IsEnabled = true;
            gwAddressSetConfig.IsEnabled = true;
            subMaskSetConfig.IsEnabled = true;
            ConnectButton.IsEnabled = false;
            DisconnectButton.IsEnabled = true;
            SetConfigurationButton.IsEnabled = true;
            SetDefaultConfigurationButton.IsEnabled = true;

        }

        private void ResetInterface()
        {
            //DELETING TEXTBOX CONTENT
            typeTextBox.Text = "";
            revTextBox.Text = "";
            ipAddressGetConfig.Text = ipAddressSetConfig.Text;
            macAddressGetConfig.Text = "";
            gwAddressGetConfig.Text = "";
            subMaskGetConfig.Text = "";
            ipAddressSetConfig.Text = "";
            macAddressSetConfig.Text = "";
            gwAddressSetConfig.Text = "";
            subMaskSetConfig.Text = "";

            //DISABLING WINDOW CONTROLS
            typeTextBox.IsEnabled = false;
            revTextBox.IsEnabled = false;
            //ipAddressGetConfig.IsEnabled = false;
            macAddressGetConfig.IsEnabled = false;
            gwAddressGetConfig.IsEnabled = false;
            subMaskGetConfig.IsEnabled = false;
            ipAddressSetConfig.IsEnabled = false;
            macAddressSetConfig.IsEnabled = false;
            gwAddressSetConfig.IsEnabled = false;
            subMaskSetConfig.IsEnabled = false;
            ConnectButton.IsEnabled = true;
            DisconnectButton.IsEnabled = false;
            SetConfigurationButton.IsEnabled = false;
            SetDefaultConfigurationButton.IsEnabled = false;
        }

    }
}
