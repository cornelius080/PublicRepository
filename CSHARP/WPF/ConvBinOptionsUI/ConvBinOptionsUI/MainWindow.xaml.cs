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

namespace ConvBinOptionsUI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            ComboBox_RinexVersion.SelectedIndex = 0;
        }

        private void RadioButton_InputFolder_Checked(object sender, RoutedEventArgs e)
        {
            if(Button_Browse != null && RadioButton_InputFolder != null && RadioButton_InputFolder.IsChecked == true)
                Button_Browse.IsEnabled = false;
        }

        private void RadioButton_SelectedFolder_Checked(object sender, RoutedEventArgs e)
        {
            Button_Browse.IsEnabled = true;
        }

        private void Button_Browse_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("OPEN FILE DIALOG -> SELECT UBX INPUT FILE");
        }

        private void CheckBox_StartTime_Checked(object sender, RoutedEventArgs e)
        {
            TextBox_StartTime1.IsEnabled = true;
            TextBox_StartTime2.IsEnabled = true;
            TextBox_StartTime1.Text = "          ";
            TextBox_StartTime2.Text = "          ";
        }

        private void CheckBox_StartTime_Unchecked(object sender, RoutedEventArgs e)
        {
            TextBox_StartTime1.IsEnabled = false;
            TextBox_StartTime2.IsEnabled = false;
            TextBox_StartTime1.Text = "YYYY.MM.DD";
            TextBox_StartTime2.Text = "hh:mm:ss";
        }

        private void CheckBox_StopTime_Checked(object sender, RoutedEventArgs e)
        {
            TextBox_StopTime1.IsEnabled = true;
            TextBox_StopTime2.IsEnabled = true;
            TextBox_StopTime1.Text = "";
            TextBox_StopTime2.Text = "";
        }

        private void CheckBox_StopTime_Unchecked(object sender, RoutedEventArgs e)
        {
            TextBox_StopTime1.IsEnabled = false;
            TextBox_StopTime2.IsEnabled = false;
            TextBox_StopTime1.Text = "YYYY.MM.DD";
            TextBox_StopTime2.Text = "hh:mm:ss";
        }

        private void CheckBox_Interval_Checked(object sender, RoutedEventArgs e)
        {
            ComboBox_Interval.IsEnabled = true;
        }

        private void CheckBox_Interval_Unchecked(object sender, RoutedEventArgs e)
        {
            ComboBox_Interval.IsEnabled = false;
        }

        private void ComboBox_Interval_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            MessageBox.Show(ComboBox_Interval.SelectedIndex.ToString());
            MessageBox.Show(ComboBox_Interval.SelectedItem.ToString());
        }

        private void ComboBox_RinexVersion_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            MessageBox.Show(ComboBox_RinexVersion.SelectedIndex.ToString());
            MessageBox.Show(ComboBox_RinexVersion.SelectedItem.ToString());
        }

        
    }




}
