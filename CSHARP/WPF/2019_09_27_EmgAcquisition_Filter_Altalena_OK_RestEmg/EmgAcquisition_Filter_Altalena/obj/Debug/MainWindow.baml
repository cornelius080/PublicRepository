   M S B A M L   `   `   `  ����Y  UEmgAcquisition_Filter_Altalena, Version=1.0.0.0, Culture=neutral, PublicKeyToken=nullO,clr-namespace:EmgAcquisition_Filter_AltalenaEmgAcquisition_Filter_Altalena  5   	   G CmyWpfChartUC, Version=1.0.0.0, Culture=neutral, PublicKeyToken=nullA0clr-namespace:myWpfChartUC;assembly=myWpfChartUCmyWpfChartUC 5   	   /    )EmgAcquisition_Filter_Altalena.MainWindow   5   	   R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35^ ZWindowsFormsIntegration, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35F 9http://schemas.microsoft.com/winfx/2006/xaml/presentation     R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   @d2http://schemas.microsoft.com/expression/blend/2008     5   	   Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5   	   >local,clr-namespace:EmgAcquisition_Filter_Altalena     5   	   ImyWpfChartUC0clr-namespace:myWpfChartUC;assembly=myWpfChartUC     5   	   -   5          �Name$  myWindow��5   O    � Title$ EmgAcquisition @ 500Hz��5	   	   $��651.893��6(   $��678.2��69    � WindowState$ 	Maximized=�6G   .��5
      � .+�5   
   �� -   5         ��Name$ myLabel��5      $�� ��6!   $
��Left=�6,   $��58��6G   $��4,8,0,0q�6S   $	��Top=�6d   $	��164��6|   $��16(�6�   $
��Bold"�6�   
���   �$��1q�6�   �� 5   
   -   5         ��Name$ emgUpComboBox��5      $��	4,114,0,0q�6*   $
��Left=�6[   $	��164��6v   $��30��6�   $	��Top=�6�   $��16(�6�   $
��Bold"�6�   �� 5   
   -   5        $ emgDownComboBox��5      $��	4,173,0,0q�6,   $
��Left=�6_   $	��164��6z   $��30��6�   $	��Top=�6�   $��16(�6�   $
��Bold"�6�   �� 5   
   -   5         ��Name$ ConfigurationButton��5      $��	CONFIGURE��6.   $
��Left=�6B   $��	4,236,0,0q�6]   $	��164��6p   $��30��6�   $	��Top=�6�   $
��Bold"�6�   $��16(�6�   �� 5   
   -   5        $ StartCaptureButton��5      $��START��6-   $��	4,290,0,0q�6=   $
��Left=�6q   $	��164��6�   $��30��6�   $	��Top=�6�   $��16(�6�   $
��Bold"�6�   �� 5   
   -   5        $ StopCaptureButton��5      $
��STOP��6,   $��	4,401,0,0q�6;   $
��Left=�6N   $	��164��6i   $��30��6u   $	��Top=�6�   $��16(�6�   $
��Bold"�6�   6�   �� 5   
   -   5        $ RestartCaptureButton��5      $��RESTART��6/   $��	4,455,0,0q�6A   $
��Left=�6T   $	��164��6o   $��30��6{   $	��Top=�6�   $��16(�6�   $
��Bold"�6�   6�   �� 5   
   $��199,10,10,10.4q�6   .@�5      �� -	   5         ��Name$ AnimationTimeItem��5      $��	ANIMATION��61   $
��Bold"�6D   .��5      � ���#c3c3c3.+�5      �� -
   5         ��Name$ baseAltalenaImg��5      $��152,266,152.4,20.6q�65   $	��154��6Q   $	��287��6]   $��BaseAltalena.png��6j   �� 5      -   5        $ barraAltalenaImg��5      $��49,244,49.4,279.6q�66   $	��360��6Q   $��50��6]   $��BarraAltalena.png��6i    J� RenderTransformOrigin$ 0.5,0.5&�6�   �� 5      -   5        	 ��Name$	 upRmsTextBox_Copy��5      $��0,10,10.6,0q�69   
 �� TextWrapping$

 Wrap=�6N   $��UpRms��6b   $
��Bold"�6o   $��16(�6�    �� 
IsReadOnly . $��60��6�   $	��Top=�6�   $��Right=�6�   $	��100��6�   ��6�   Z� 6�   �� 5      -   5        $	 downRmsTextBox_Copy��5      $��	10,10,0,0q�6;   $

 Wrap=�6N   $��DownRms��6b   $
��Bold"�6q   $��16(�6�    . $
��Left=�6�   $	��100��6�   $��60��6�   $	��Top=�6�   ��6�   Z� 6�   5      5      �� 5      -   5        $ plotTabItem��5      $
��PLOT��6+   $
��Bold"�69   .��5      � ���	#FFE5E5E5.+�5        myWpfChartUC.myWpfChartUC  -   5          Name$ graficoEmgUp��5   0   $��10,10,10.4,383.6q�6F   $��1q�6`   
���   �6t     5      -   5        $ graficoEmgDown��5   0   $��10,384,10.2,9.6q�6H   $��1q�6a   
���   �6u   5      5       5!      �� 5"   
   -   5        $ RestEmgButton��5"      $��REST EMG��6(   $��	4,345,0,0q�6;   $
��Left=�6j   $	��164��6�   $��30��6�   $	��Top=�6�   $��16(�6�   $
��Bold"�6�   5$      5%      