using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace NPREth_GetSetConfiguration
{
    public readonly struct DeviceParameters
    {
        public string DEVICE_TYPE { get; }
        public string HW_FW_CONF { get; }
        public string MAC { get; }
        public string IP { get; }
        public string SUBNET_MASK { get; }
        public string GW { get; }

        public DeviceParameters(string deviceType, string hwFwConf, string macAddress, string ipAddress, string subnetMask, string gateWay)
        {
            this.DEVICE_TYPE = deviceType;
            this.HW_FW_CONF = hwFwConf;
            this.MAC = macAddress;
            this.IP = ipAddress;
            this.SUBNET_MASK = subnetMask;
            this.GW = gateWay;
        }
    }


    public class NPR_NetParameters
    {
        DeviceParameters deviceParameters;
        public readonly string DEFAULT_IP;
        public readonly string DEFAULT_MAC;
        public readonly string DEFAULT_SUBNET_MASK;
        public readonly string DEFAULT_GW;
        public readonly int DEFAULT_PORT;
        readonly string succString = "SUCC\r\n";
        readonly int bytesToRead = 50;
        byte[] answerReceived, dataReceived;
        Socket socket;



        /// <summary>
        /// Class contructor which contains methods for get and set net parameters.
        /// </summary>
        /// <param name="_socket">Socket object used for the device connection.</param>
        public NPR_NetParameters(Socket _socket)
        {
            DEFAULT_IP = "192.168.0.253";
            DEFAULT_MAC = "00:11:55:AA:CC:FF";
            DEFAULT_SUBNET_MASK = "255.255.0.0";
            DEFAULT_GW = "192.168.0.1";
            DEFAULT_PORT = 27985;
            answerReceived = new byte[succString.Length];
            dataReceived = new byte[bytesToRead];
            socket = _socket;
        }


        #region GET NET PARAMETERS

        /// <summary>
        /// Generic method for net parameter retrieving.
        /// </summary>
        /// <param name="stringCommand">Command in the format "GET <parameter>\r\n"</param>
        /// <returns>Returns a string</returns>
        private string GetParameter(string stringCommand)
        {
            string parameter = "N.A.";

            if (socket.Connected)
            {                
                //SEND BYTES REQUEST
                int byteSend = socket.Send(Encoding.ASCII.GetBytes(stringCommand));

                byte[] temp = new byte[50];
                //RECEIVE ANSWER
                socket.Receive(temp, temp.Length, SocketFlags.None);
                //la risposta è del tipo SUCC<space><param>\r\n (SUCC (4byte) + <spazio> (1byte) + param (Nbyte) + \r\n (2byte))
                //cerco l'indice corrispondente all'elemento spazio
                int spaceIndex = System.Array.FindIndex(temp, x => x.Equals(32));
                //cerco l'indice corrispondente all'elemento carriageReturn
                int carrReturnIndex = System.Array.FindIndex(temp, x => x.Equals(13));
                if (spaceIndex != -1 && carrReturnIndex != -1)
                {
                    byte[] netParam = new byte[carrReturnIndex - spaceIndex - 1];
                    System.Array.Copy(temp, spaceIndex + 1, netParam, 0, netParam.Length);
                    parameter = Encoding.ASCII.GetString(netParam);
                }
                else
                    parameter = "";
            }

            return parameter;
        }
        

        /// <summary>
        /// Gets the apparatus type PLD TYPE (0-65535)
        /// </summary>
        /// <returns>Returns a string</returns>
        private string GetPldType()
        {
            string type = GetParameter("GET TYPE\r\n");
            return type;
        }


        /// <summary>
        /// Gets the hardware and firmware configuration status PLD REV(0-65535) 
        /// </summary>
        /// <returns>Returns a string</returns>
        private string GetPldRev()
        {
            string rev = GetParameter("GET REV\r\n");
            return rev;
        }


        /// <summary>
        /// Gets the physical address of the ethernet interface (aa:bb:cc:dd:ee:ff)
        /// </summary>
        /// <returns>Returns a string</returns>
        private string GetMacAddress()
        {
            string mac = GetParameter("GET MAC\r\n");
            return mac;
        }


        /// <summary>
        /// Gets the IP address of the ethernet interface (0.0.0.0)
        /// </summary>
        /// <returns>Returns a string</returns>
        private string GetIpAddress()
        {
            string ip = GetParameter("GET IP\r\n");
            return ip;
        }


        /// <summary>
        /// Gets the mask of the local subnet to the board (0.0.0.0)
        /// </summary>
        /// <returns>Returns a string</returns>
        private string GetSubnetMaskAddress()
        {
            string sm = GetParameter("GET SM\r\n");
            return sm;
        }


        /// <summary>
        /// Gets the IP address of the gateway (0.0.0.0)
        /// </summary>
        /// <returns>Returns a string</returns>
        private string GetGwAddress()
        {
            string gw = GetParameter("GET GW\r\n");
            return gw;
        }


        /// <summary>
        /// Get all net parameters (device type PLD TYPE, hw&fw configuration PLD REV, mac, ip, subnet mask, gateway address)
        /// </summary>
        /// <returns>Returns a 'NPR_NetParamenters.DeviceParameters' struct with corresponding fields</returns>
        public DeviceParameters GetNetParameters()
        {
            string deviceType = GetPldType();
            string hwFwConfig = GetPldRev();
            string macAddress = GetMacAddress();
            string ipAddress = GetIpAddress();
            string subMask = GetSubnetMaskAddress();
            string gwAddress = GetGwAddress();

            deviceParameters = new DeviceParameters(deviceType, hwFwConfig, macAddress, ipAddress, subMask, gwAddress);
            return deviceParameters;
        }
        
        #endregion


        #region SET NET PARAMETERS

        private bool SetParameter(string stringCommand)
        {
            bool isSet = false;

            if (socket.Connected)
            {
                string answer = "";
                //SEND COMMAND
                int byteSend = socket.Send(Encoding.ASCII.GetBytes(stringCommand));
                //ANSWER RECEIVE ("SUCC\r\n", "ERR\r\n")
                byte[] temp = new byte[50];
                socket.Receive(temp, temp.Length, SocketFlags.None);
                //cerco l'indice corrispondente all'elemento line feed
                int lineFeedIndex = System.Array.FindIndex(temp, x => x.Equals(10));
                if (lineFeedIndex != -1)
                {
                    byte[] ans = new byte[lineFeedIndex + 1];
                    System.Array.Copy(temp, 0, ans, 0, ans.Length);
                    answer = Encoding.ASCII.GetString(ans);
                }

                if (String.Equals(answer, succString))
                {
                    isSet = true;
                }
            }

            return isSet;
        }


        /// <summary>
        /// Sets the physical address of the ethernet interface
        /// </summary>
        /// <param name="macAddress">String representing the MAC address (aa:bb:cc:dd:ee:ff)</param>
        /// <returns>Returns a boolean isSet</returns>
        private bool SetMacAddress(string macAddress)
        {
            bool isSet = SetParameter("SET MAC " + macAddress + "\r\n");
            return isSet;
        }


        /// <summary>
        /// Sets the IP address of the ethernet interface
        /// </summary>
        /// <param name="ipAddress">String representing the IP address (0.0.0.0)</param>
        /// <returns>Returns a boolean isSet</returns>
        private bool SetIpAddress(string ipAddress)
        {
            bool isSet = SetParameter("SET IP " + ipAddress + "\r\n");
            return isSet;
        }


        /// <summary>
        /// Sets the mask of the local subnet to the board
        /// </summary>
        /// <param name="subMask">String representing the subnet mask (0.0.0.0)</param>
        /// <returns>Returns a boolean isSet</returns>
        private bool SetSubnetMaskAddress(string subMask)
        {
            bool isSet = SetParameter("SET SM " + subMask + "\r\n");
            return isSet;
        }


        /// <summary>
        /// Sets the GW address of the ethernet interface
        /// </summary>
        /// <param name="gwAddress">String representing the GW address (0.0.0.0)</param>
        /// <returns>Returns a boolean isSet</returns>
        private bool SetGwAddress(string gwAddress)
        {
            bool isSet = SetParameter("SET GW " + gwAddress + "\r\n");
            return isSet;
        }


        /// <summary>
        /// Set all net parameters (device type PLD TYPE, hw&fw configuration PLD REV, mac, ip, subnet mask, gateway address)
        /// </summary>
        public void SetNetParameters(string macAddress, string ipAddress, string subMask, string gwAddress)
        {
            bool setMac = SetMacAddress(macAddress);
            bool setSM = SetSubnetMaskAddress(subMask);
            bool setGW = SetGwAddress(gwAddress);
            //string pippo = ipAddress;
            bool setIP = SetIpAddress(ipAddress);


            string msg = "SET IP = " + setIP.ToString() + "\n" + "SET MAC = " + setMac.ToString() + "\n" + "SET SM = " + setSM.ToString() + "\n" + "SET GW = " + setGW.ToString() + "\n";
            MessageBox.Show(msg, "SET NET PARAMETERS");
        }

        #endregion





    }





}
