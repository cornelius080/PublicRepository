using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Reflection;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;

namespace NPREth_Commands
{
    public class NPREth_Connect
    {
        Socket serverSocket = null;
        IPEndPoint ipEndPoint = null;
        readonly string succString = "SUCC\r\n";
        byte[] dataReceived = null;
        byte[] answerReceived = null;
        readonly int bytesToRead = 20;
        string saveDirectory, dataFileName;
        public bool isConnected;
        public Task connectionTask;
        CancellationTokenSource cancTokenSource; //object needed to the cancellation token
        CancellationToken cancToken; //CancellationToken object needed to cancel the connection task
        readonly string DEFAULT_IP = "192.168.0.253";
        readonly int DEFAULT_PORT = 27985;


        /// <summary>
        /// Constructor of the class.
        /// </summary>
        public NPREth_Connect()
        {
            try
            {
                ipEndPoint = new IPEndPoint(IPAddress.Parse(DEFAULT_IP), DEFAULT_PORT);
            }
            catch(FormatException fe)
            {
                MessageBox.Show(fe.ToString());
                Environment.Exit(1);
            }
            Init();
        }


        /// <summary>
        /// Constructor of the class.
        /// </summary>
        /// <param name="IpAddressString">Ip address in the string format "000.000.000.000"</param>
        public NPREth_Connect(string IpAddressString)
        {
            try
            {
                ipEndPoint = new IPEndPoint(IPAddress.Parse(IpAddressString), DEFAULT_PORT);
            }
            catch(FormatException fe)
            {
                MessageBox.Show(fe.ToString());
                Environment.Exit(1);
            }
            Init();
        }


        /// <summary>
        /// Method for class variables initialization, for socket definition and connection and preliminary saving operations.
        /// </summary>
        private void Init()
        {
            saveDirectory = DefineSaveDirectory();
            CreateFileHeader(saveDirectory);

            answerReceived = new byte[succString.Length];
            dataReceived = new byte[bytesToRead];

            cancTokenSource = new CancellationTokenSource();
            cancToken = cancTokenSource.Token;

            TcpConnect();
        }


        /// <summary>
        /// Method for starting the connection task and keeping the device connected.
        /// </summary>
        public void StartConnection()
        {
            isConnected = true;
            try
            {
                connectionTask = new Task(KeepConnectionAlive, cancToken);
                connectionTask.Start();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
                Environment.Exit(1);
            }
        }


        /// <summary>
        /// Method for stopping the connection, disposing the connection task and closing the socket.
        /// </summary>
        public void StopConnection()
        {
            isConnected = false;
            try
            {
                cancTokenSource.CancelAfter(500);
            }
            catch (AggregateException Aex)
            {
                if (Aex.InnerExceptions.Any(e => e is TaskCanceledException))
                    MessageBox.Show("Task cancelled");
                else
                    MessageBox.Show(Aex.ToString());
            }
            catch (OperationCanceledException oce)
            {
                MessageBox.Show(oce.ToString());
            }
            finally
            {
                cancTokenSource.Dispose();
            }

            Thread.Sleep(1000);
            connectionTask.Dispose();
            TcpDisconnect();


            answerReceived = new byte[succString.Length];
            dataReceived = new byte[bytesToRead];
        }


        /// <summary>
        /// Method used in the 'connection thread' used for keeping the device connected.
        /// </summary>
        private void KeepConnectionAlive()
        {      
            //DEVICE STATE REQUEST
            try
            {
                while (serverSocket.Connected && isConnected)
                {
                    ////////////////////////////
                    /// DEVICE STATE READING
                    ////////////////////////////
                    //REC accetta solo multipli di 4; in caso contrario, restituisce un numero di byte arrotondato ad un multiplo di 4
                    SendToNPR("REC 4");
                    Thread.Sleep(200);
                    ReadFromNPR();
                    SaveDataIntoFile(dataFileName, dataReceived);

                    //TOKEN OBSERVATION BY POLLING
                    if (cancToken.IsCancellationRequested)
                        cancToken.ThrowIfCancellationRequested();
                }
            }
            catch (Exception ex) //ObjectDisposedException oex
            {
                MessageBox.Show(ex.ToString());
            }
        }


        /// <summary>
        /// Method for socket stream definition using the default or the user-defined IP address.
        /// </summary>
        private void TcpConnect()
        {
            try
            {
                serverSocket = new Socket(ipEndPoint.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
                serverSocket.Connect(ipEndPoint);
            }
            catch (SocketException se)
            {
                MessageBox.Show(se.ToString());
                MessageBox.Show("VERIFY THAT THE DEVICE IS SWITCHED ON", "ERROR", MessageBoxButton.OK, MessageBoxImage.Error);
                Environment.Exit(1);
            }
        }


        /// <summary>
        /// Method for socket shutdown, both for reading and writing, and socket closing.
        /// </summary>
        private void TcpDisconnect()
        {
            try
            {
                serverSocket.Shutdown(SocketShutdown.Both);
                serverSocket.Close();
            }
            catch (SocketException se)
            {
                MessageBox.Show(se.ToString());
            }
        }


        private void SendToNPR(string stringCommand)
        {
            //COMMAND COMPOSING
            stringCommand += "\r\n";
            //SEND REQUEST
            int byteSend = serverSocket.Send(Encoding.ASCII.GetBytes(stringCommand));
        }


        private void ReadFromNPR()
        {
            //VERIFY IF COMMAND SENT TO NPR IS RECOGNIZED
            //ANSWER RECEIVE ("SUCC\r\n", "ERR\r\n")
            serverSocket.Receive(answerReceived, answerReceived.Length, SocketFlags.None);
            //DATA RECEIVE IF SUCC
            if (String.Equals(Encoding.ASCII.GetString(answerReceived), succString))
                serverSocket.Receive(dataReceived, dataReceived.Length, SocketFlags.None);

        }


        public bool GetConnectionStatus()
        {
            return serverSocket.Connected;
        }


        /// <summary>
        /// Gets the status of the NPR converting a single byte received into a string.
        /// </summary>
        /// <returns>Returns a string representing the status number of the device</returns>
        public string GetNPRStatus()
        {
            //se c'è una sola chiamata socket.Receive, nel buffer è contenuto SUCC/ERR
            //return Convert.ToInt32(dataReceived[7]).ToString(); 


            //se ci sono due chiamate socket.Receive, nella prima cè la risposta SUCC/ERR mentre nella seconda ci sono i dati
            return Convert.ToInt32(dataReceived[1]).ToString();
        }




        


        /// <summary>
        /// Method for retrieving the project name.
        /// </summary>
        /// <returns></returns>
        private string GetProjectName()
        {
            string namespaceName = Assembly.GetExecutingAssembly().FullName.Split(',')[0];
            return namespaceName;
        }

        /// <summary>
        /// Method for the creation of a folder, with the name of the project, in the Documents and Settings folder.
        /// </summary>
        /// <returns></returns>
        private string DefineSaveDirectory()
        {
            string saveDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            saveDirectory = saveDirectory + @"\" + GetProjectName();

            if (!Directory.Exists(saveDirectory))
            {
                Directory.CreateDirectory(saveDirectory);
            }

            return saveDirectory;
        }

        private void CreateFileHeader(string _saveDirectory)
        {
            //FILE HEADER WRITING
            try
            {
                /*fileName = saveDirectory + @"\\" + DateTime.Now.ToString("yyyy'-'MM'-'dd'___'HH':'mm':'ss") + @" - " + GetProjectName() + @".csv";*/
                dataFileName = _saveDirectory + @"\\ALL_DATA_RECEIVED.csv";
                using (StreamWriter sw = new StreamWriter(dataFileName, false))
                {
                    sw.WriteLine("DATETIME" + ";" + "BYTE" + ";" + "ASCII" + ";");
                }
            }
            catch (IOException ioe)
            {
                MessageBox.Show(ioe.ToString());
            }
        }

        private void SaveDataIntoFile(string fileData, byte[] dataArray)
        {
            //DATA ARRAY WRITING
            using (StreamWriter sw = new StreamWriter(fileData, true))
            {
                string stringa = Encoding.ASCII.GetString(dataArray);
                for (int i = 0; i < dataArray.Length; i++)
                {
                    sw.WriteLine(DateTime.Now.ToString("HH':'mm':'ss.fff") + ";" + dataArray[i].ToString() + ";" + stringa[i] + ";");
                }
            }
        }

        




    }
}
