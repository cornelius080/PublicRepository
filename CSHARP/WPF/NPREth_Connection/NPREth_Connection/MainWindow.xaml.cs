using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Reflection;
using System.Security.Permissions;
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

namespace NPREth_Connection
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
            timer.Tick += timer_Tick;
            
        }


        /// <summary>
        /// Button click event
        /// </summary>
        private void ConnectButton_Click(object sender, RoutedEventArgs e)
        {            
            nprConnection = new NPREth_Connect();
            nprConnection.StartConnection();
            timer.Start();
            
        }                


        /// <summary>
        /// Event called by the timer tick every timerInterval milliseconds elapsed.
        /// </summary>
        private void timer_Tick(object sender, EventArgs e)
        {            
            //NPR STATUS
            NPRStateTextBox.Text = nprConnection.GetNPRStatus();

            //NET PARAMETERS
            ipTextBox.Text = nprConnection.deviceParameters.IP;
            macTextBox.Text = nprConnection.deviceParameters.MAC;
            gwTextBox.Text = nprConnection.deviceParameters.GW;
            subMaskTextBox.Text = nprConnection.deviceParameters.SUBNET_MASK;
            deviceTextBox.Text = nprConnection.deviceParameters.DEVICE_TYPE;
            hwFwTextBox.Text = nprConnection.deviceParameters.HW_FW_CONF;


            ///////////////////////////////////////
            ////ONLY FOR DEBUG PURPOSES
            myLabel1.Content = "STATUS: " + nprConnection.connectionTask.Status.ToString();
            myLabel2.Content = "IS CANCELED: " + nprConnection.connectionTask.IsCanceled.ToString();
            ///////////////////////////////////////            
        }


        /// <summary>
        /// Button click event
        /// </summary>
        private void DisconnectButton_Click(object sender, RoutedEventArgs e)
        {
            timer.Stop();
            ResetInterface();
            nprConnection.StopConnection();
            Thread.Sleep(1000);

            
            ///////////////////////////////////////
            ////ONLY FOR DEBUG PURPOSES
            myLabel1.Content = "STATUS: " + nprConnection.connectionTask.Status.ToString();
            myLabel2.Content = "IS CANCELED: " + nprConnection.connectionTask.IsCanceled.ToString();
            ///////////////////////////////////////
        }


        /// <summary>
        /// Method for reset the interface after disconnection
        /// </summary>
        private void ResetInterface()
        {
            NPRStateTextBox.Text = "";

            ipTextBox.Text = "";
            macTextBox.Text = "";
            gwTextBox.Text = "";
            subMaskTextBox.Text = "";
            deviceTextBox.Text = "";
            hwFwTextBox.Text = "";
        }





    }
}
