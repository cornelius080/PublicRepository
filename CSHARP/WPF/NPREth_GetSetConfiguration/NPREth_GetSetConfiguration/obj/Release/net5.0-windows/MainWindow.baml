   M S B A M L   `   `   `  ���� U  QNPREth_GetSetConfiguration, Version=1.0.0.0, Culture=neutral, PublicKeyToken=nullG(clr-namespace:NPREth_GetSetConfigurationNPREth_GetSetConfiguration  +    %NPREth_GetSetConfiguration.MainWindow   \ XPresentationFramework, Version=5.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35e aSystem.Windows.Controls.Ribbon, Version=5.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089W SPresentationCore, Version=5.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35R NWindowsBase, Version=5.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35F 9http://schemas.microsoft.com/winfx/2006/xaml/presentation     R NSystem.Xaml, Version=5.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     @d2http://schemas.microsoft.com/expression/blend/2008     Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     :local(clr-namespace:NPREth_GetSetConfiguration       � Title$  NPREth NET CONFIGURATION��$	��514��$	��882�� � WindowState$ 	Maximized=�.��� .+��� -    ��Name$ GetConfigurationGroupBox��$��GET CONFIGURATION��$��	301,0,0,0q�$��10q�$��20(�$
��Bold"�$
��Left=�$	��274��$	��452��$��Center=�.���� -    ��Name$  GetConfigurationStackPanel��.+��� $
��0,10q�$��16(�$��
IP Address���� -    ��Name$ ipAddressGetConfig���� $
��0,10q�$��16(�$��MAC Address���� -   $ macAddressGetConfig�� �� 
IsReadOnly$
 True��${�False���� $
��0,10q�$��16(�$��
GW Address���� -   $ gwAddressGetConfig��$
 True��${�False���� $
��0,10q�$��16(�$��Subnet Mask���� -   $ subMaskGetConfig��$
 True��${�False���� -    ��Name$ ConnectButton��$
��0,20q�$��CONNECT���� -   $ DisconnectButton��$��
DISCONNECT��${�False���� -	   $ SetConfigurationGroupBox��$��SET CONFIGURATION��$��	597,0,0,0q�$��10q�$��20(�$
��Bold"�$
��Left=�$	��274��$	��452��$��Center=�.���� -
   $  SetConfigurationStackPanel��.+��� $
��0,10q�$��16(�$��
IP Address���� -   $ ipAddressSetConfig��${�False���� $
��0,10q�$��16(�$��MAC Address���� -   $ macAddressSetConfig��${�False���� $
��0,10q�$��16(�$��
GW Address���� -   $ gwAddressSetConfig��${�False���� $
��0,10q�$��16(�$��Subnet Mask���� -   $ subMaskSetConfig��${�False���� -   $ SetConfigurationButton��$
��0,20q�$	��SET��${�False���� -   $# SetDefaultConfigurationButton��$��SET DEFAULT��${�False���� -   $ ExtraParametersGroupBox��$��HW FW PARAMETERS��$��15,0,0,0q�$��10q�$��20(�$
��Bold"�$
��Left=�$	��274��$	��452��$��Center=�.���� -   $ ExtraParametersStackPanel��.+��� $
��0,10q�$��16(�$
��Type���� -   $ typeTextBox��${�False��$
 True���� $
��0,10q�$��16(�$	��Rev���� -   $ 
revTextBox��$
 True��${�False��