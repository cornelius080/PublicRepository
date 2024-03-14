namespace _2022_11_16___Xsens_File_Configuration;

public partial class MainPage : ContentPage
{
    private bool _isPacketCounter, _isSampleTimeFine, _isSampleTimeCoarse, _isUtcTime;
    private string _orientation, _orientationPrecision, _orientationFrequency;
    private bool _isRateTurn, _isAcceleration, _isFreeAcceleration, _isMagneticField;
    private string _inertialDataPrecision, _inertialDataFrequency, _magneticFieldPrecision, _magneticFieldFrequency;
    private bool _isAccelerationHR, _isRateTurnHR;
    private string _highRateDataPrecision, _highRateDataFrequency;
    private bool _isTemperature, _isPressure;
    private string _temperaturePrecision, _temperatureFrequency, _pressurePrecision, _pressureFrequency, _filterSettings, _coordinateFrame;


    public MainPage()
    {
        InitializeComponent();

        this.CheckBoxExt_PacketCounter.Label.Text = "Packet Counter";
        this.CheckBoxExt_PacketCounter.CheckBox.CheckedChanged += CheckBoxExt_PacketCounter_CheckedChanged;
        this.CheckBoxExt_SampleTimeCoarse.Label.Text = "Sample Time Coarse";
        this.CheckBoxExt_SampleTimeCoarse.CheckBox.CheckedChanged += CheckBoxExt_SampleTimeCoarse_CheckedChanged;
        this.CheckBoxExt_SampleTimeFine.Label.Text = "Sample Time Fine";
        this.CheckBoxExt_SampleTimeFine.CheckBox.CheckedChanged += CheckBoxExt_SampleTimeFine_CheckedChanged;
        this.CheckBoxExt_UTCTime.Label.Text = "UTC Time";
        this.CheckBoxExt_UTCTime.CheckBox.CheckedChanged += CheckBoxExt_UTCTime_CheckedChanged;
        this.CheckBoxExt_UTCTime.CheckBox.IsChecked = true;

        this._isPacketCounter = this.CheckBoxExt_PacketCounter.CheckBox.IsChecked;
        this._isSampleTimeCoarse = this.CheckBoxExt_SampleTimeCoarse.CheckBox.IsChecked;
        this._isSampleTimeFine = this.CheckBoxExt_SampleTimeFine.CheckBox.IsChecked;
        this._isUtcTime = this.CheckBoxExt_UTCTime.CheckBox.IsChecked;



        this.Picker_Orientation.SelectedIndex = 0;
        this.Picker_Orientation_Precision.SelectedIndex = 1;
        this.Picker_Orientation_Frequency.SelectedIndex = 0;



        this.CheckBoxExt_RateTurn.Label.Text = "Rate of Turn";
        this.CheckBoxExt_RateTurn.CheckBox.IsChecked = true;
        this.CheckBoxExt_RateTurn.CheckBox.CheckedChanged += CheckBoxExt_RateTurn_CheckedChanged;
        this.CheckBoxExt_Acceleration.Label.Text = "Acceleration";
        this.CheckBoxExt_Acceleration.CheckBox.IsChecked = true;
        this.CheckBoxExt_Acceleration.CheckBox.CheckedChanged += CheckBoxExt_Acceleration_CheckedChanged;
        this.CheckBoxExt_FreeAcceleration.Label.Text = "Free Acceleration";
        this.CheckBoxExt_FreeAcceleration.CheckBox.CheckedChanged += CheckBoxExt_FreeAcceleration_CheckedChanged;
        this.Picker_InertialData_Precision.SelectedIndex = 1;
        this.Picker_InertialData_Frequency.SelectedIndex = 0;

        this._isRateTurn = this.CheckBoxExt_RateTurn.CheckBox.IsChecked;
        this._isAcceleration = this.CheckBoxExt_Acceleration.CheckBox.IsChecked;
        this._isFreeAcceleration = this.CheckBoxExt_FreeAcceleration.CheckBox.IsChecked;




        this.CheckBoxExt_MagneticField.Label.Text = "Magnetic Field";
        this.CheckBoxExt_MagneticField.CheckBox.IsChecked = true;
        this.CheckBoxExt_MagneticField.CheckBox.CheckedChanged += CheckBoxExt_MagneticField_CheckedChanged;
        this.Picker_MagneticField_Precision.SelectedIndex = 1;
        this.Picker_MagneticField_Frequency.SelectedIndex = 0;

        this._isMagneticField = this.CheckBoxExt_MagneticField.CheckBox.IsChecked;





        this.CheckBoxExt_AccelerationHR.Label.Text = "Acceleration HR";
        this.CheckBoxExt_AccelerationHR.CheckBox.IsChecked = true;
        this.CheckBoxExt_AccelerationHR.CheckBox.CheckedChanged += CheckBoxExt_AccelerationHR_CheckedChanged;
        this.CheckBoxExt_RateTurnHR.Label.Text = "Rate of Turn HR";
        this.CheckBoxExt_RateTurnHR.CheckBox.IsChecked = true;
        this.CheckBoxExt_RateTurnHR.CheckBox.CheckedChanged += CheckBoxExt_RateTurnHR_CheckedChanged;
        this.Picker_HighRate_Frequency.SelectedIndex = 0;
        this.Picker_HighRate_Precision.SelectedIndex = 1;

        this._isAccelerationHR = this.CheckBoxExt_AccelerationHR.CheckBox.IsChecked;
        this._isRateTurnHR = this.CheckBoxExt_RateTurnHR.CheckBox.IsChecked;





        this.CheckBoxExt_Temperature.Label.Text = "Temperature";
        this.CheckBoxExt_Temperature.CheckBox.CheckedChanged += CheckBoxExt_Temperature_CheckedChanged;
        this.Picker_Temperature_Precision.SelectedIndex = 1;
        this.Picker_Temperature_Frequency.SelectedIndex = 0;

        this._isTemperature = this.CheckBoxExt_Temperature.CheckBox.IsChecked;




        this.CheckBoxExt_Pressure.Label.Text = "Pressure";
        this.CheckBoxExt_Pressure.CheckBox.CheckedChanged += CheckBoxExt_Pressure_CheckedChanged;
        this.Picker_Pressure_Precision.SelectedIndex = 1;
        this.Picker_Pressure_Frequency.SelectedIndex = 0;

        this._isPressure = this.CheckBoxExt_Pressure.CheckBox.IsChecked;



        this.Picker_FilterSettings.SelectedIndex = 0;
        this._filterSettings = (string)this.Picker_FilterSettings.ItemsSource[0];
        this.Picker_CoordinateFrame.SelectedIndex = 0;
        this._coordinateFrame = (string)this.Picker_CoordinateFrame.ItemsSource[0];

    }


    #region TIMESTAMP
    private void CheckBoxExt_PacketCounter_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_PacketCounter.CheckBox.IsChecked)
            this._isPacketCounter = true;
        else
            this._isPacketCounter = false;
    }

    private void CheckBoxExt_SampleTimeFine_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_SampleTimeFine.CheckBox.IsChecked)
            this._isSampleTimeFine = true;
        else
            this._isSampleTimeFine = false;
    }

    private void CheckBoxExt_SampleTimeCoarse_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_SampleTimeCoarse.CheckBox.IsChecked)
            this._isSampleTimeCoarse = true;
        else
            this._isSampleTimeCoarse = false;
    }

    private void CheckBoxExt_UTCTime_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_UTCTime.CheckBox.IsChecked)
            this._isUtcTime = true;
        else
            this._isUtcTime = false;
    }
    #endregion


    #region ORIENTATION
    void Picker_Orientation_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._orientation = (string)picker.ItemsSource[selectedIndex];
        }
    }

    void Picker_Orientation_Precision_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._orientationPrecision = (string)picker.ItemsSource[selectedIndex];
        }
    }

    void Picker_Orientation_Frequency_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._orientationFrequency = (string)picker.ItemsSource[selectedIndex];
        }
    }
    #endregion


    #region INERTIAL DATA
    private void CheckBoxExt_RateTurn_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_RateTurn.CheckBox.IsChecked)
            this._isRateTurn = true;
        else
            this._isRateTurn = false;
    }

    private void CheckBoxExt_Acceleration_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_Acceleration.CheckBox.IsChecked)
            this._isAcceleration = true;
        else
            this._isAcceleration = false;
    }

    private void CheckBoxExt_FreeAcceleration_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_FreeAcceleration.CheckBox.IsChecked)
            this._isFreeAcceleration = true;
        else
            this._isFreeAcceleration = false;
    }

    void Picker_InertialData_Precision_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._inertialDataPrecision = (string)picker.ItemsSource[selectedIndex];
        }
    }

    void Picker_InertialData_Frequency_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._inertialDataFrequency = (string)picker.ItemsSource[selectedIndex];
        }
    }
    #endregion


    #region MAGNETIC FIELD
    private void CheckBoxExt_MagneticField_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_MagneticField.CheckBox.IsChecked)
            this._isMagneticField = true;
        else
            this._isMagneticField = false;
    }

    void Picker_MagneticField_Precision_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._magneticFieldPrecision = (string)picker.ItemsSource[selectedIndex];
        }
    }

    void Picker_MagneticField_Frequency_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._magneticFieldFrequency = (string)picker.ItemsSource[selectedIndex];
        }
    }
    #endregion


    #region HIGH-RATE DATA
    private void CheckBoxExt_AccelerationHR_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_AccelerationHR.CheckBox.IsChecked)
            this._isAccelerationHR = true;
        else
            this._isAccelerationHR = false;
    }

    private void CheckBoxExt_RateTurnHR_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_RateTurnHR.CheckBox.IsChecked)
            this._isRateTurnHR = true;
        else
            this._isRateTurnHR = false;
    }

    void Picker_HighRate_Precision_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._highRateDataPrecision = (string)picker.ItemsSource[selectedIndex];
        }
    }

    void Picker_HighRate_Frequency_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._highRateDataFrequency = (string)picker.ItemsSource[selectedIndex];
        }
    }
    #endregion


    #region TEMPERATURE
    private void CheckBoxExt_Temperature_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_Temperature.CheckBox.IsChecked)
            this._isTemperature = true;
        else
            this._isTemperature = false;
    }

    void Picker_Temperature_Precision_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._temperaturePrecision = (string)picker.ItemsSource[selectedIndex];
        }
    }

    void Picker_Temperature_Frequency_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._temperatureFrequency = (string)picker.ItemsSource[selectedIndex];
        }
    }
    #endregion


    #region PRESSURE
    private void CheckBoxExt_Pressure_CheckedChanged(object sender, EventArgs e)
    {
        if (this.CheckBoxExt_Pressure.CheckBox.IsChecked)
            this._isPressure = true;
        else
            this._isPressure = false;
    }

    void Picker_Pressure_Precision_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._pressurePrecision = (string)picker.ItemsSource[selectedIndex];
        }
    }

    void Picker_Pressure_Frequency_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._pressureFrequency = (string)picker.ItemsSource[selectedIndex];
        }
    }
    #endregion


    #region FILTER SETTINGS
    void Picker_FilterSettings_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._filterSettings = (string)picker.ItemsSource[selectedIndex];
        }
    }
    #endregion


    #region COORDINATE FRAME
    void Picker_CoordinateFrame_SelectedIndexChanged(object sender, EventArgs e)
    {
        var picker = (Picker)sender;
        int selectedIndex = picker.SelectedIndex;

        if (selectedIndex != -1)
        {
            //DisplayAlert("RINEX VERSION SELECTED ITEM", (string)picker.ItemsSource[selectedIndex], "cancel");
            this._coordinateFrame = (string)picker.ItemsSource[selectedIndex];
        }
    }
    #endregion




    private void ButtonDebug_Clicked(object sender, EventArgs e)
    {
        //DisplayAlert("DEBUG", "PACKET COUNTER: " + _isPacketCounter + "\n" + "SAMPLE TIME FINE: " + _isSampleTimeFine + "\n" + "SAMPLE TIME COARSE: " + _isSampleTimeCoarse + "\n" + "UTC TIME: " + _isUtcTime + "\n", "cancel");

        //DisplayAlert("DEBUG", "ORIENTATION: " + _orientation + "\n" + "PRECISION: " + _orientationPrecision + "\n" + "FREQUENCY: " + _orientationFrequency + "\n", "cancel");

        //DisplayAlert("DEBUG", "RATE TURN: " + _isRateTurn + "\n" + "ACCELERATION: " + _isAcceleration + "\n" + "FREE ACCELERATION: " + _isFreeAcceleration + "\n" + "PRECISION: " + _inertialDataPrecision + "\n" + "FREQUENCY: " + _inertialDataFrequency + "\n", "cancel");

        //DisplayAlert("DEBUG", "MAGNETIC FIELD: " + _isMagneticField + "\n" + "PRECISION: " + _magneticFieldPrecision + "\n" + "FREQUENCY: " + _magneticFieldFrequency + "\n", "cancel");

        //DisplayAlert("DEBUG", "RATE TURN HR: " + _isRateTurnHR + "\n" + "ACCELERATION HR: " + _isAccelerationHR + "\n" + "PRECISION: " + _highRateDataPrecision + "\n" + "FREQUENCY: " + _highRateDataFrequency + "\n", "cancel");

        //DisplayAlert("DEBUG", "TEMPERATURE: " + _isTemperature + "\n" + "PRECISION: " + _temperaturePrecision + "\n" + "FREQUENCY: " + _temperatureFrequency + "\n", "cancel");

        DisplayAlert("DEBUG", "PRESSURE: " + _isPressure + "\n" + "PRECISION: " + _pressurePrecision + "\n" + "FREQUENCY: " + _pressureFrequency + "\n", "cancel");



    }
}

