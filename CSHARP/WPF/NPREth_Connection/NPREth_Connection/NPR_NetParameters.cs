using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace NPREth_Connection
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

        public NPR_NetParameters(Socket _socket)
        {
            DEFAULT_IP = "192.168.0.253";
            DEFAULT_MAC = "00:11:55:AA:CC:FF";
            DEFAULT_SUBNET_MASK = "255.255.255.0";
            DEFAULT_GW = "192.168.0.1";
            DEFAULT_PORT = 27985;
            answerReceived = new byte[succString.Length];
            dataReceived = new byte[bytesToRead];
            socket = _socket;
        }


        /// <summary>
        /// Gets the apparatus type (0-65535)
        /// </summary>
        /// <returns>Returns a string</returns>
        private string GetDeviceType()
        {
            string deviceType = "N.A.";

            if (socket.Connected)
            {
                //GET COMMAND COMPOSING
                string stringCommand = "GET REV\r\n";
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
                    deviceType = Encoding.ASCII.GetString(netParam);
                }
                else
                    deviceType = "";
            }

            return deviceType;
        }


        /// <summary>
        /// Gets the hardware and software configuration status (0-65535)
        /// </summary>
        /// <returns>Returns a string</returns>
        private string GetHwFwConfiguration()
        {
            string configType = "N.A.";

            if (socket.Connected)
            {
                //GET COMMAND COMPOSING
                string stringCommand = "GET REV\r\n";
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
                    configType = Encoding.ASCII.GetString(netParam);
                }
                else
                    configType = "";
            }

            return configType;
        }


        /// <summary>
        /// Gets the physical address of the ethernet interface (aa:bb:cc:dd:ee:ff)
        /// </summary>
        /// <returns>Returns a string</returns>
        private string GetMacAddress()
        {
            string macAddress = "N.A.";

            if(socket.Connected)
            {
                //GET COMMAND COMPOSING
                string stringCommand = "GET MAC\r\n";
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
                    macAddress = Encoding.ASCII.GetString(netParam);
                }
                else
                    macAddress = "";
            }

            return macAddress;
        }


        /// <summary>
        /// Gets the IP address of the ethernet interface (w.x.y.z)
        /// </summary>
        /// <returns>Returns a string</returns>
        private string GetIpAddress()
        {
            string ipAddress = "N.A.";

            if (socket.Connected)
            {
                //GET COMMAND COMPOSING
                string stringCommand = "GET IP\r\n";
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
                    ipAddress = Encoding.ASCII.GetString(netParam);
                }
                else
                    ipAddress = "";
            }

            return ipAddress;
        }


        /// <summary>
        /// Gets the mask of the local subnet to the board (w.x.y.z)
        /// </summary>
        /// <returns>Returns a string</returns>
        private string GetSubnetMaskAddress()
        {
            string subMask = "N.A.";

            if (socket.Connected)
            {
                //GET COMMAND COMPOSING
                string stringCommand = "GET SM\r\n";
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
                    subMask = Encoding.ASCII.GetString(netParam);
                }
                else
                    subMask = "";
            }

            return subMask;
        }


        /// <summary>
        /// Gets the IP address of the gateway (w.x.y.z)
        /// </summary>
        /// <returns>Returns a string</returns>
        private string GetGwAddress()
        {
            string gwAddress = "N.A.";

            if (socket.Connected)
            {
                //GET COMMAND COMPOSING
                string stringCommand = "GET GW\r\n";
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
                    gwAddress = Encoding.ASCII.GetString(netParam);
                }
                else
                    gwAddress = "";
            }

            return gwAddress;
        }


        /// <summary>
        /// Get all net parameters (device type, hw&fw configuration, mac, ip, subnet mask, gateway address)
        /// </summary>
        /// <returns>Returns a 'NPR_NetParamenters.DeviceParameters' struct with corresponding fields</returns>
        public DeviceParameters GetNetParameters()
        {
            string deviceType = GetDeviceType();
            string hwFwConfig = GetHwFwConfiguration();
            string macAddress = GetMacAddress();
            string ipAddress = GetIpAddress();
            string subMask = GetSubnetMaskAddress();
            string gwAddress = GetGwAddress();

            deviceParameters = new DeviceParameters(deviceType, hwFwConfig, macAddress, ipAddress, subMask, gwAddress);
            return deviceParameters;
        }


        /// <summary>
        /// Sets the physical address of the ethernet interface
        /// </summary>
        /// <param name="macAddress">String representing the MAC address (aa:bb:cc:dd:ee:ff)</param>
        /// <returns>Returns a boolean isSet</returns>
        public bool SetMacAddress(string macAddress)
        {
            bool isSet = false;

            if (socket.Connected)
            {
                //GET COMMAND COMPOSING
                string stringCommand = "SET MAC " + macAddress + "\r\n";
                //SEND COMMAND
                int byteSend = socket.Send(Encoding.ASCII.GetBytes(stringCommand));
                //ANSWER RECEIVE ("SUCC\r\n", "ERR\r\n")
                socket.Receive(answerReceived, answerReceived.Length, SocketFlags.None);

                if (String.Equals(Encoding.ASCII.GetString(answerReceived), succString))
                {
                    isSet = true;
                }
            }

            return isSet;
        }


        /// <summary>
        /// Sets the IP address of the ethernet interface
        /// </summary>
        /// <param name="ipAddress">String representing the IP address (w.x.y.z)</param>
        /// <returns>Returns a boolean isSet</returns>
        public bool SetIpAddress(string ipAddress)
        {
            bool isSet = false;

            if (socket.Connected)
            {
                //GET COMMAND COMPOSING
                string stringCommand = "SET IP " + ipAddress + "\r\n";
                //SEND COMMAND
                int byteSend = socket.Send(Encoding.ASCII.GetBytes(stringCommand));
                //ANSWER RECEIVE ("SUCC\r\n", "ERR\r\n")
                socket.Receive(answerReceived, answerReceived.Length, SocketFlags.None);

                if (String.Equals(Encoding.ASCII.GetString(answerReceived), succString))
                {
                    isSet = true;
                }
            }

            return isSet;
        }


        /// <summary>
        /// Sets the mask of the local subnet to the board
        /// </summary>
        /// <param name="subMask">String representing the subnet mask (w.x.y.z)</param>
        /// <returns>Returns a boolean isSet</returns>
        public bool SetSubnetMaskAddress(string subMask)
        {
            bool isSet = false;

            if (socket.Connected)
            {
                //GET COMMAND COMPOSING
                string stringCommand = "SET SM " + subMask + "\r\n";
                //SEND COMMAND
                int byteSend = socket.Send(Encoding.ASCII.GetBytes(stringCommand));
                //ANSWER RECEIVE ("SUCC\r\n", "ERR\r\n")
                socket.Receive(answerReceived, answerReceived.Length, SocketFlags.None);

                if (String.Equals(Encoding.ASCII.GetString(answerReceived), succString))
                {
                    isSet = true;
                }
            }

            return isSet;
        }


        /// <summary>
        /// Sets the GW address of the ethernet interface
        /// </summary>
        /// <param name="gwAddress">String representing the GW address (w.x.y.z)</param>
        /// <returns>Returns a boolean isSet</returns>
        public bool SetGwAddress(string gwAddress)
        {
            bool isSet = false;

            if (socket.Connected)
            {
                //GET COMMAND COMPOSING
                string stringCommand = "SET GW " + gwAddress + "\r\n";
                //SEND COMMAND
                int byteSend = socket.Send(Encoding.ASCII.GetBytes(stringCommand));
                //ANSWER RECEIVE ("SUCC\r\n", "ERR\r\n")
                socket.Receive(answerReceived, answerReceived.Length, SocketFlags.None);

                if (String.Equals(Encoding.ASCII.GetString(answerReceived), succString))
                {
                    isSet = true;
                }
            }

            return isSet;
        }


    }





}
