   M S B A M L   `   `   `  ����U  QNPREth_GetSetConfiguration, Version=1.0.0.0, Culture=neutral, PublicKeyToken=nullG(clr-namespace:NPREth_GetSetConfigurationNPREth_GetSetConfiguration  5   	   +    %NPREth_GetSetConfiguration.MainWindow   5   	   \ XPresentationFramework, Version=5.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35e aSystem.Windows.Controls.Ribbon, Version=5.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089W SPresentationCore, Version=5.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35R NWindowsBase, Version=5.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35F 9http://schemas.microsoft.com/winfx/2006/xaml/presentation     5   	   R NSystem.Xaml, Version=5.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   @d2http://schemas.microsoft.com/expression/blend/2008     5   	   Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5   	   :local(clr-namespace:NPREth_GetSetConfiguration     5   	     � Title$  NPREth NET CONFIGURATION��5   	   $	��514��6*   $	��882��67    � WindowState$ 	Maximized=�6C   .��5	      � .+�5
   
   �� -   5         ��Name$ GetConfigurationGroupBox��5
      $��GET CONFIGURATION��65   $��	301,0,0,0q�6P   $��10q�6c   $��20(�6p   $
��Bold"�6~   $
��Left=�6�   $	��274��6�   $	��452��6�   $��Center=�6�   .��5      �� -   5         ��Name$  GetConfigurationStackPanel��5      .+�5      �� $
��0,10q�6   $��16(�6*   $��
IP Address��68   �� 5      -   5         ��Name$ ipAddressGetConfig��5      �� 5      $
��0,10q�6   $��16(�6*   $��MAC Address��68   �� 5      -   5        $ macAddressGetConfig��5       �� 
IsReadOnly$
 True��67   ${�False��6I   �� 5      $
��0,10q�6   $��16(�6*   $��
GW Address��68   �� 5      -   5        $ gwAddressGetConfig��5      $
 True��66   ${�False��6H   �� 5      $
��0,10q�6   $��16(�6*   $��Subnet Mask��68   �� 5      -   5        $ subMaskGetConfig��5      $
 True��64   ${�False��6F   �� 5      -   5         ��Name$ ConnectButton��5      $
��0,20q�60   $��CONNECT��6>   6P   �� 5      -   5        $ DisconnectButton��5      $��
DISCONNECT��63   ${�False��6g   5      5      �� 5   
   -	   5        $ SetConfigurationGroupBox��5      $��SET CONFIGURATION��65   $��	597,0,0,0q�6P   $��10q�6c   $��20(�6p   $
��Bold"�6~   $
��Left=�6�   $	��274��6�   $	��452��6�   $��Center=�6�   .��5      �� -
   5        $  SetConfigurationStackPanel��5      .+�5      �� $
��0,10q�6   $��16(�6*   $��
IP Address��68   �� 5      -   5        $ ipAddressSetConfig��5      ${�False��66   �� 5      $
��0,10q�6   $��16(�6*   $��MAC Address��68   �� 5      -   5        $ macAddressSetConfig��5      ${�False��67   �� 5      $
��0,10q�6   $��16(�6*   $��
GW Address��68   �� 5      -   5        $ gwAddressSetConfig��5      ${�False��66   �� 5       $
��0,10q�6   $��16(�6*   $��Subnet Mask��68   �� 5!      -   5        $ subMaskSetConfig��5!      ${�False��64   �� 5"      -   5        $ SetConfigurationButton��5"      $
��0,20q�69   $	��SET��6G   ${�False��6z   �� 5#      -   5        $# SetDefaultConfigurationButton��5#      $��SET DEFAULT��6@   ${�False��6�   5$      5%      �� 5&   
   -   5        $ ExtraParametersGroupBox��5&      $��HW FW PARAMETERS��64   $��15,0,0,0q�6N   $��10q�6`   $��20(�6m   $
��Bold"�6{   $
��Left=�6�   $	��274��6�   $	��452��6�   $��Center=�6�   .��5'      �� -   5        $ ExtraParametersStackPanel��5'      .+�5(      �� $
��0,10q�6   $��16(�6*   $
��Type��68   �� 5)      -   5        $ typeTextBox��5)      ${�False��6/   $
 True��6A   �� 5*      $
��0,10q�6   $��16(�6*   $	��Rev��68   �� 5+      -   5        $ 
revTextBox��5+      $
 True��6.   ${�False��6@   5,      5-      5/      50      