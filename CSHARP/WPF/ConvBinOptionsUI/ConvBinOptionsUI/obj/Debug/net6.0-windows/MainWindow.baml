   M S B A M L   `   `   `  ����K  GConvBinOptionsUI, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null3clr-namespace:ConvBinOptionsUIConvBinOptionsUI  5   	   !    ConvBinOptionsUI.MainWindow   5   	   W SPresentationCore, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35e aSystem.Windows.Controls.Ribbon, Version=6.0.2.0, Culture=neutral, PublicKeyToken=b77a5c561934e089R NWindowsBase, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35F 9http://schemas.microsoft.com/winfx/2006/xaml/presentation     5   	   R NSystem.Xaml, Version=6.0.2.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   @d2http://schemas.microsoft.com/expression/blend/2008     5   	   Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5   	   0localclr-namespace:ConvBinOptionsUI     5   	     � Title$  ConvBinOptionsUI��5   	   $	��768��6"   $
��1012��6/   .��5	      � .+�5
   
   �� -   5         ��Name$ GroupBox_ResultsFolder��5
      $��Results Folder Location��63   $��10,10,10,452q�6T   $��14(�6j   .��5      �� .+�5      ��  �� Orientation$ 
Horizontal=�6   .+�5      	� -   5         	�Name$ RadioButton_InputFolder��5   "   $��Input File Folder��6C    d� 	IsChecked$
 TrueY�6_   6p   	� 5      -   5        $  RadioButton_SelectedFolder��5   "   $��Selected Folder��6F   6`   5      �� 5      $ 
Horizontal=�6   .+�5      �� -   5         ��Name$ TextBox_SelectedFolder��5      ${�False��6>   $	��600��6P   �� 5      -   5         ��Name$ Button_Browse��5      $	��...��64   ${�False��6B   $��30��6T   $��20,0,0,0q�6_   6q   5      5      5      �� 5   
   -   5        $ GroupBox_LogsDuration��5      $��Logs Duration��62   $��10,120,10,245q�6I   $��14(�6`   .��5      �� .+�5      �� $ 
Horizontal=�6   .+�5      �� .+�5      �� -   5         ��Name$ CheckBox_StartTime��5   #   $
��From��6?   6s   �� 5      $ 
Horizontal=�6%   .+�5      �� -   5        $ TextBox_StartTime1��5   &   ${�False��6B   $��
YYYY.MM.DD��6T   $��90��6f   $��21��6q    � ToolTip$ 
YYYY.MM.DD��6}   �� 5      -	   5        $ TextBox_StartTime2��5   &   ${�False��6B   $��hh:mm:ss��6T   $��90��6d   $��21��6o   $ hh:mm:ss��6{   5      5      �� 5       .+�5!      �� -
   5        $ CheckBox_StopTime��5!   #   $��To��6>   6s   �� 5"      $ 
Horizontal=�6%   .+�5#      �� -   5        $ TextBox_StopTime1��5#   &   ${�False��6A   $��
YYYY.MM.DD��6S   $��90��6e   $��21��6p   $ 
YYYY.MM.DD��6|   �� 5$      -   5        $ TextBox_StopTime2��5$   &   ${�False��6A   $��hh:mm:ss��6S   $��90��6c   $��21��6n   $ hh:mm:ss��6z   5%      5&      �� 5'      .+�5(      �� -   5        $ CheckBox_Interval��5(   #   $��Interval��6>   6u   �� 5)      -   5        	 ��Name$	 ComboBox_Interval��5)   #   ${�False��6>   .@�5*      �� $
��10 s��6+   �� 5+      $
��20 s��6+   �� 5,      $
��30 s��6+   5-      5.      5/      �� 50      .+�51      �� -   5        $ CheckBox_TimeRounding��51      $F��@Time rounding (required for OPUS and other third-party services)��6>   52      53      54      �� 55   
   -   5        $ GroupBox_RinexVersion��55      $��RINEX Version��62   $��10,323,10,182q�6I   $��14(�6`   .��56      �� .+�57      �� -   5        $	 ComboBox_RinexVersion��57      $��25��6:   .@�58      �� $��
RINEX 3.02��6#   �� 59      $��
RINEX 2.10��6#   5:      5;      5<      �� 5=   
   -   5        $ GroupBox_MarkerName��5=      $��Marker Name��60   $��10,403,10,237q�6E   $��14(�6\   .��5>      �� .+�5?      �� -   5        $ TextBox_MarkerName��5?      ${�False��66   $��For static data��6H   5@      5A      �� 5B   
   -   5        $ GroupBox_Satellites��5B      $��
Satellites��60   $��10,533,10,-17q�6D   $��14(�6[   .��5C      �� .+�5D      �� $ 
Horizontal=�6   .+�5E      �� -   5        $ CheckBox_Satellites_Gps��5E      $	��GPS��6@   $
 TrueY�6N   �� 5F      -   5        $ CheckBox_Satellites_Sbas��5F      $
��SBAS��6A   $ FalseY�6P   �� 5G      -   5        $! CheckBox_Satellites_Glonass��5G      $��GLONASS��6D   $
 TrueY�6V   �� 5H      -   5        $! CheckBox_Satellites_Galileo��5H      $��Galileo��6D   $
 TrueY�6V   5I      �� 5J      $ 
Horizontal=�6   .+�5K      �� -   5        $ CheckBox_Satellites_Qzss��5K      $
��QZSS��6A   $ FalseY�6P   �� 5L      -   5        $  CheckBox_Satellites_Beidou��5L      $��BeiDou��6C   $
 TrueY�6T   �� 5M      -   5        $ CheckBox_Satellites_Irnss��5M      $��IRNSS��6B   $ FalseY�6R   5N      5O      5P      5S      5T      