using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace _2022_10_12___RTKLibConvBin
{
    internal class ConvBin : Page
    {
        private string command, workingDirectory, projectDirectory;
        private Process winShell;


        /// <summary>
        /// Class Constructor for the ubx file conversion into rinex using the RTKLib ConvBin
        /// </summary>
        public ConvBin()
        {
            command = "convbin.exe";
            workingDirectory = AppContext.BaseDirectory;
            projectDirectory = Directory.GetParent(workingDirectory).Parent.Parent.Parent.Parent.Parent.FullName;
            winShell = new Process();
        }


        /// <summary>
        /// Converts the ubx file into Rinex according to the selected options.
        /// </summary>
        /// <param name="fileName">Ubx file to be converted</param>
        /// <param name="startTime">Start time for the conversion</param>
        /// <param name="stopTime">End time for the conversion</param>
        /// <param name="timeInterval">Observation data interval (s)</param>
        /// <param name="rinexVersion">Version of Rinex output</param>
        /// <param name="markerName">Marker name</param>
        /// <param name="gps">If false, GPS is excluded</param>
        /// <param name="glonass">If false, GLONASS is excluded</param>
        /// <param name="galileo">If false, GALILEO is excluded</param>
        /// <param name="beidou">If false, BEIDOU is excluded</param>
        /// <param name="qzss">If false, QZSS is excluded</param>
        /// <param name="sbas">If false, SBAS is excluded</param>
        public void ConvertUbxIntoRinex(string fileName, string startTime, string stopTime, string timeInterval, string rinexVersion, string markerName, bool gps, bool glonass, bool galileo, bool beidou, bool qzss, bool sbas)
        {
            RunWinShell();

            if (!string.IsNullOrEmpty(fileName))
            {
                command = command + " "  + fileName;
                if (!string.IsNullOrEmpty(startTime))
                    if (!string.IsNullOrWhiteSpace(startTime))
                        command = command + " -ts " + startTime;
                if (!string.IsNullOrEmpty(stopTime))
                    if (!string.IsNullOrWhiteSpace(stopTime))
                        command = command + " -te " + stopTime;
                if (!string.IsNullOrEmpty(timeInterval))
                    command = command + " -ti " + timeInterval;
                if (!string.IsNullOrEmpty(rinexVersion))
                    command = command + " -v " + rinexVersion;
                if (!string.IsNullOrEmpty(markerName))
                    command = command + " -hm " + markerName;

                //NOTA: L'opzione -y esclude le costellazioni. Quando l'utente spunta una costellazione questa deve essere inclusa.
                if (!gps)
                    command = command + " -y G";
                if (!glonass)
                    command = command + " -y R";
                if (!galileo)
                    command = command + " -y E";
                if (!beidou)
                    command = command + " -y C";
                if (!qzss)
                    command = command + " -y J";
                if (!sbas)
                    command = command + " -y S";

                winShell.StandardInput.WriteLine(command);
                //QuitWinShell();
            }
            else 
                return;
                    
        }


        /// <summary>
        /// Runs a Windows command line and moves into the folder that contains the ConvBin.exe
        /// </summary>
        private void RunWinShell()
        {
            try
            {
                winShell.StartInfo.FileName = "cmd.exe";
                winShell.StartInfo.RedirectStandardInput = true;
                ////winShell.StartInfo.RedirectStandardOutput = true;
                ////winShell.StartInfo.CreateNoWindow = true;
                ////winShell.StartInfo.UseShellExecute = false;
                winShell.Start();
                winShell.StandardInput.WriteLine("cd " + projectDirectory + "\\myDependencies");
            }
            catch(Exception ex)
            {
                DisplayAlert("RUN SHELL EXCEPTION", ex.ToString(), "CANCEL");
            }
        }


        /// <summary>
        /// Waits indefinitely for the associated process and closes the shell.
        /// </summary>
        private void QuitWinShell()
        {
            try
            {
                winShell.StandardInput.Flush();
                winShell.StandardInput.Close();
                winShell.WaitForExit();
            }
            catch (Exception ex)
            {
                DisplayAlert("QUIT SHELL EXCEPTION", ex.ToString(), "CANCEL");
            }            
        }



    }
}
