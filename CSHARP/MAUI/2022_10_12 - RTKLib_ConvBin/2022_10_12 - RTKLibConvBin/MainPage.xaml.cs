namespace _2022_10_12___RTKLibConvBin;

public partial class MainPage : ContentPage
{
    private string _ubxFilename;
    private string _startTime1, _startTime2, _stopTime1, _stopTime2, _timeInterval;
    private bool _isTimeRounding;
    private string _rinexVersion, _markerName;
    private bool _isSatellitesGps, _isSatellitesGlonass, _isSatellitesGalileo, _isSatellitesBeiDou;
    private bool _isSatellitesSbas, _isSatellitesQzss, _isSatellitesIrnss;
    private ConvBin cb;


    public MainPage()
    {
        InitializeComponent();

        this.CheckBoxExt_StartTime.Label.Text = "FROM";
        this.CheckBoxExt_StopTime.Label.Text = "TO";
        this.CheckBoxExt_Interval.Label.Text = "INTERVAL (s)";
        this.CheckBoxExt_TimeRounding.Label.Text = "Time rounding (required for OPUS and other third-party services)";
        this.CheckBoxExt_StartTime.CheckBox.CheckedChanged += CheckBoxExt_StartTime_CheckedChanged;
        this.CheckBoxExt_StopTime.CheckBox.CheckedChanged += CheckBoxExt_StopTime_CheckedChanged;
        this.CheckBoxExt_Interval.CheckBox.CheckedChanged += CheckBoxExt_Interval_CheckedChanged;
        this.CheckBoxExt_TimeRounding.CheckBox.CheckedChanged += CheckBoxExt_TimeRounding_CheckedChanged;
        this.Picker_RinexVersion.SelectedIndex = 0;
        this.CheckBoxExt_Satellites_Gps.Label.Text = "GPS";
        this.CheckBoxExt_Satellites_Gps.CheckBox.IsChecked = true;
        this.CheckBoxExt_Satellites_Gps.CheckBox.CheckedChanged += CheckBoxExt_Satellites_Gps_CheckedChanged;
        this.CheckBoxExt_Satellites_Glonass.Label.Text = "GLONASS";
        this.CheckBoxExt_Satellites_Glonass.CheckBox.IsChecked = true;
        this.CheckBoxExt_Satellites_Glonass.CheckBox.CheckedChanged += CheckBoxExt_Satellites_Glonass_CheckedChanged;
        this.CheckBoxExt_Satellites_Galileo.Label.Text = "GALILEO";
        this.CheckBoxExt_Satellites_Galileo.CheckBox.IsChecked = true;
        this.CheckBoxExt_Satellites_Galileo.CheckBox.CheckedChanged += CheckBoxExt_Satellites_Galileo_CheckedChanged;
        this.CheckBoxExt_Satellites_BeiDou.Label.Text = "BEIDOU";
        this.CheckBoxExt_Satellites_BeiDou.CheckBox.IsChecked = true;
        this.CheckBoxExt_Satellites_BeiDou.CheckBox.CheckedChanged += CheckBoxExt_Satellites_BeiDou_CheckedChanged;
        this.CheckBoxExt_Satellites_Sbas.Label.Text = "SBAS";
        this.CheckBoxExt_Satellites_Sbas.CheckBox.IsChecked = false;
        this.CheckBoxExt_Satellites_Sbas.CheckBox.CheckedChanged += CheckBoxExt_Satellites_Sbas_CheckedChanged;
        this.CheckBoxExt_Satellites_Qzss.Label.Text = "QZSS";
        this.CheckBoxExt_Satellites_Qzss.CheckBox.IsChecked = false;
        this.CheckBoxExt_Satellites_Qzss.CheckBox.CheckedChanged += CheckBoxExt_Satellites_Qzss_CheckedChanged;
        this.CheckBoxExt_Satellites_Irnss.Label.Text = "IRNSS";
        this.CheckBoxExt_Satellites_Irnss.CheckBox.IsChecked = false;
        this.CheckBoxExt_Satellites_Irnss.CheckBox.CheckedChanged += CheckBoxExt_Satellites_Irnss_CheckedChanged;

        _isSatellitesBeiDou = this.CheckBoxExt_Satellites_BeiDou.CheckBox.IsChecked;
        _isSatellitesGalileo = this.CheckBoxExt_Satellites_Galileo.CheckBox.IsChecked;
        _isSatellitesGlonass = this.CheckBoxExt_Satellites_Glonass.CheckBox.IsChecked;
        _isSatellitesGps = this.CheckBoxExt_Satellites_Gps.CheckBox.IsChecked;
        _isSatellitesIrnss = this.CheckBoxExt_Satellites_Irnss.CheckBox.IsChecked;
        _isSatellitesQzss = this.CheckBoxExt_Satellites_Qzss.CheckBox.IsChecked;
        _isSatellitesSbas = this.CheckBoxExt_Satellites_Sbas.CheckBox.IsChecked;           

    }


    #region UBX FILE SELECTION
    async void Button_OpenFile_Clicked(object sender, EventArgs e)
    {
        var customFileType = new FilePickerFileType(
                new Dictionary<DevicePlatform, IEnumerable<string>>
                {
                    { DevicePlatform.WinUI, new[] { ".ubx" } }
                });

        try
        {
            var pickResult = await FilePicker.Default.PickAsync(new PickOptions
            {
                PickerTitle = "SELECT UBLOX FILE",
                FileTypes = customFileType
            });

            if (pickResult != null)
            {
                //await DisplayAlert("FILENAME", pickResult.FileName, "CANCEL");
                //await DisplayAlert("FULLPATH", pickResult.FullPath, "CANCEL");
                _ubxFilename = pickResult.FullPath;
            }
        }
        catch (Exception ex)
        {
            await DisplayAlert("EXCEPTION DURING FILE PICKING", ex.ToString(), "CANCEL");
        }

        this.Button_Convert.IsEnabled = true;
    }
    #endregion


    #region RESULTS FOLDER LOCATION
    private void RadioButton_InputFolder_CheckedChanged(object sender, EventArgs e)
    {
        if (Button_Browse != null && RadioButton_InputFolder != null && RadioButton_InputFolder.IsChecked == true)
            //if (RadioButton_InputFolder.IsChecked == true)
            Button_Browse.IsEnabled = false;
    }

    private void RadioButton_SelectedFolder_CheckedChanged(object sender, EventArgs e)
    {
        if (RadioButton_SelectedFolder != null && RadioButton_SelectedFolder.IsChecked == true)
            //if (RadioButton_SelectedFolder.IsChecked == true)
            Button_Browse.IsEnabled = true;
    }

    private void Button_Browse_Click(object sender, EventArgs e)
    {
        DisplayAlert("FOLDER FILE DIALOG", "SELECT OUTPUT FOLDER", "CANCEL");
    }
    #endregion


    #region LOGS DURATION
    private void CheckBoxExt_StartTime_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_StartTime.CheckBox.IsChecked)
        {
            this.Entry_StartTime1.IsEnabled = true;
            this.Entry_StartTime2.IsEnabled = true;
        }
        else
        {
            this.Entry_StartTime1.IsEnabled = false;
            this.Entry_StartTime2.IsEnabled = false;
            this.Entry_StartTime1.Text = "";
            this.Entry_StartTime2.Text = "";
            this.Entry_StartTime1.Placeholder = "YYYY/MM/DD";
            this.Entry_StartTime2.Placeholder = "hh:mm:ss";
        }
    }

    private void CheckBoxExt_StopTime_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_StopTime.CheckBox.IsChecked)
        {
            this.Entry_StopTime1.IsEnabled = true;
            this.Entry_StopTime2.IsEnabled = true;
        }
        else
        {
            this.Entry_StopTime1.IsEnabled = false;
            this.Entry_StopTime2.IsEnabled = false;
            this.Entry_StopTime1.Text = "";
            this.Entry_StopTime2.Text = "";
            this.Entry_StopTime1.Placeholder = "YYYY/MM/DD";
            this.Entry_StopTime2.Placeholder = "hh:mm:ss";
        }
    }

    private void CheckBoxExt_Interval_CheckedChanged(object sender, EventArgs e)
    {
        this.Picker_Interval.SelectedIndex = 6;

        if (this.CheckBoxExt_Interval.CheckBox.IsChecked)
            this.Picker_Interval.IsEnabled = true;
        else
            this.Picker_Interval.IsEnabled = false;
    }

    private void Entry_StartTime1_TextChanged(object sender, EventArgs e)
    {
        _startTime1 = this.Entry_StartTime1.Text;
    }

    private void Entry_StartTime2_TextChanged(object sender, EventArgs e)
    {
        _startTime2 = this.Entry_StartTime2.Text;
    }

    private void Entry_StopTime1_TextChanged(object sender, EventArgs e)
    {
        _stopTime1 = this.Entry_StopTime1.Text;
    }

    private void Entry_StopTime2_TextChanged(object sender, EventArgs e)
    {
        _stopTime2 = this.Entry_StopTime2.Text;
    }

    void Picker_Interval_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("INTERVAL SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            _timeInterval = (string)picker.ItemsSource[selectedIndex];
        }
    }

    private void CheckBoxExt_TimeRounding_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_TimeRounding.CheckBox.IsChecked)
            _isTimeRounding = true;
        else
            _isTimeRounding = false;
    }
    #endregion


    #region RINEX VERSION
    void Picker_RinexVersion_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            _rinexVersion = (string)picker.ItemsSource[selectedIndex];
        }
    }
    #endregion


    #region MARKER NAME
    private void Entry_MarkerName_TextChanged(object sender, EventArgs e)
    {
        _markerName = this.Entry_MarkerName.Text;
    }
    #endregion


    #region SATELLITES
    private void CheckBoxExt_Satellites_Gps_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_Satellites_Gps.CheckBox.IsChecked)
            _isSatellitesGps = true;
        else
            _isSatellitesGps = false;
    }

    private void CheckBoxExt_Satellites_Glonass_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_Satellites_Glonass.CheckBox.IsChecked)
            _isSatellitesGlonass = true;
        else
            _isSatellitesGlonass = false;
    }

    private void CheckBoxExt_Satellites_Galileo_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_Satellites_Galileo.CheckBox.IsChecked)
            _isSatellitesGalileo = true;
        else
            _isSatellitesGalileo = false;
    }

    private void CheckBoxExt_Satellites_BeiDou_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_Satellites_BeiDou.CheckBox.IsChecked)
            _isSatellitesBeiDou = true;
        else 
            _isSatellitesBeiDou = false;
    }

    private void CheckBoxExt_Satellites_Sbas_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_Satellites_Sbas.CheckBox.IsChecked)
            _isSatellitesSbas = true;
        else
            _isSatellitesSbas = false;
    }

    private void CheckBoxExt_Satellites_Qzss_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_Satellites_Qzss.CheckBox.IsChecked)
            _isSatellitesQzss = true;
        else
            _isSatellitesQzss = false;
    }

    private void CheckBoxExt_Satellites_Irnss_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_Satellites_Irnss.CheckBox.IsChecked)
            _isSatellitesIrnss = true;
    }
    #endregion


    #region CONVERSION
    private void Button_Convert_Clicked(object sender, EventArgs e)
    {
        string startTime = _startTime1 + " " + _startTime2;
        string stopTime = _stopTime1 + " " + _stopTime2;

        cb = new ConvBin();
        cb.ConvertUbxIntoRinex(_ubxFilename, startTime, stopTime, _timeInterval, _rinexVersion, _markerName, _isSatellitesGps, _isSatellitesGlonass, _isSatellitesGalileo, _isSatellitesBeiDou, _isSatellitesQzss, _isSatellitesSbas);
    }
    #endregion

}

