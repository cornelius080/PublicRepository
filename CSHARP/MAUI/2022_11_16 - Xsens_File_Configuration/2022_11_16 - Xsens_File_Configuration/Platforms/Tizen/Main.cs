using System;
using Microsoft.Maui;
using Microsoft.Maui.Hosting;

namespace _2022_11_16___Xsens_File_Configuration;

class Program : MauiApplication
{
	protected override MauiApp CreateMauiApp() => MauiProgram.CreateMauiApp();

	static void Main(string[] args)
	{
		var app = new Program();
		app.Run(args);
	}
}
