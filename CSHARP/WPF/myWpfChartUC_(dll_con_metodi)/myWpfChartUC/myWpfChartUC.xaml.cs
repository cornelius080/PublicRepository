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
using System.Windows.Forms.DataVisualization.Charting;
using System.Drawing;

namespace myWpfChartUC
{
    /// <summary>
    /// Logica di interazione per UserControl1.xaml
    /// </summary>
    public partial class myWpfChartUC : UserControl
    {
        public myWpfChartUC()
        {
            InitializeComponent();
        }

        //public void ChangeRectangleProperties(Brushes myFillColour, Brushes myStrokeColour, double myStrokeThickness)
        //{
        //    myRect.Fill = myFillColour;
        //    myRect.Stroke = myStrokeColour;
        //    myRect.StrokeThickness = myStrokeThickness;
        //}


        public void InizializzaGrafico(string xAxisTitle, string yAxisTitle, float xAxisTitleFontSize, float yAxisTitleFontSize)
        {
            myChart.Series.Clear();
            myChart.ChartAreas.Clear();
            myChart.Legends.Clear();
            myChart.Titles.Clear();
            myChart.ChartAreas.Add("area");
            myChart.ChartAreas["area"].AxisX.Minimum = 0;
            myChart.ChartAreas["area"].AxisX.Maximum = 10;
            myChart.ChartAreas["area"].AxisX.Interval = 1;
            myChart.ChartAreas["area"].AxisX.Title = xAxisTitle;
            myChart.ChartAreas["area"].AxisX.TitleFont = new System.Drawing.Font("Microsoft Sans Serif", xAxisTitleFontSize);
            //myChart.Chart.ChartAreas["area"].AxisY.Minimum = -1;
            //myChart.Chart.ChartAreas["area"].AxisY.Maximum = 1;
            //myChart.Chart.ChartAreas["area"].AxisY.Interval = 1;
            myChart.ChartAreas["area"].AxisY.Title = yAxisTitle;
            myChart.ChartAreas["area"].AxisY.TitleFont = new System.Drawing.Font("Microsoft Sans Serif", yAxisTitleFontSize);
            myChart.AntiAliasing = AntiAliasingStyles.All;
            myChart.TextAntiAliasingQuality = TextAntiAliasingQuality.High;
            myChart.Customize += chart_Customize;            
        }


        private void chart_Customize(object sender, EventArgs e)
        {
            //make the X-axis show up with days, hours, minutes, seconds properly.

            CustomLabelsCollection xAxisLabels = ((Chart)sender).ChartAreas["area"].AxisX.CustomLabels;

            for (int cnt = 0; cnt < xAxisLabels.Count; cnt++)
            {
                TimeSpan ts = TimeSpan.FromSeconds(double.Parse(xAxisLabels[cnt].Text));

                if (ts.Days > 0)
                    xAxisLabels[cnt].Text = ts.Days.ToString("00") + ":" + ts.Hours.ToString("00") + ":" + ts.Minutes.ToString("00") + ":" + ts.Seconds.ToString("00");
                else
                {
                    if (ts.Hours > 0)
                        xAxisLabels[cnt].Text = ts.Hours.ToString("00") + ":" + ts.Minutes.ToString("00") + ":" + ts.Seconds.ToString("00");
                    else
                        xAxisLabels[cnt].Text = ts.Minutes.ToString("00") + ":" + ts.Seconds.ToString("00");
                }
            }
        }


        public void CreaSerie(string nomeSerie)
        {
            myChart.Series.Add(nomeSerie);
            myChart.Series[nomeSerie].ChartType = SeriesChartType.FastLine;
            myChart.Series[nomeSerie].BorderWidth = 3;
            myChart.Legends.Add(nomeSerie);
            myChart.Legends[nomeSerie].Docking = Docking.Right;
            myChart.Legends[nomeSerie].Alignment = StringAlignment.Center;
            myChart.Legends[nomeSerie].BorderColor = System.Drawing.Color.Tomato;
            myChart.Series[nomeSerie].IsVisibleInLegend = false;
        }


        public void CreaSerie(string[] nomeSerie)
        {
            for (var i = 0; i < nomeSerie.Length; i++)
                CreaSerie(nomeSerie[i]);
        }


        public void AggiornaContenutoSerie(string nomeSerie, double[] xValues, double[] yValues)
        {
            myChart.Series[nomeSerie].Points.SuspendUpdates();
            myChart.Series[nomeSerie].Points.Clear();
            for (var i = 0; i < xValues.Length; i++)
                myChart.Series[nomeSerie].Points.AddXY(xValues[i], yValues[i]);

            myChart.Series[nomeSerie].Points.ResumeUpdates();
            myChart.Series[nomeSerie].IsVisibleInLegend = true;
        }


        public void UpdateAxisX(double[] myTime)
        {
            myChart.ChartAreas["area"].AxisX.Minimum = (double)myTime[0];
            myChart.ChartAreas["area"].AxisX.Maximum = (double)myTime[(-1 + myTime.Length)];
            myChart.ChartAreas["area"].AxisX.Interval = 1;
        }


        public Chart Chart => myChart;      //è equivalente a      public Chart Chart { get { return myChart; } }



    }
}
