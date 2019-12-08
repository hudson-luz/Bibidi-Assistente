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
using System.Diagnostics;
using System.IO;
using System.Data.SQLite;
using Microsoft.Win32;

namespace Bibidi
{
    /// <summary>
    /// Interação lógica para MainWindow.xam
    /// </summary>
    public partial class MainWindow : Window
    {
        string dbPath = string.Empty;
        public MainWindow()
        {
            InitializeComponent();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {

            rtbOutput.AppendText("[" + DateTime.Now + "] Result ID: " + GetCommandID(tbCommand.Text));
            rtbOutput.AppendText("[" + DateTime.Now + "] Result Path: " + GetCommandPathByID(GetCommandID(tbCommand.Text)));
            RunCommand(GetCommandPathByID(GetCommandID(tbCommand.Text)));
        } 

        private string GetCommandID(string sentence)
        {
            string output = "";

            if (!string.IsNullOrEmpty(dbPath))
            {
                Process cmd = new Process();
                ProcessStartInfo startInfo = new ProcessStartInfo();
                startInfo.FileName = "cmd.exe";
                startInfo.RedirectStandardOutput = true;
                startInfo.Arguments = "/c python BibidiClassifier.py " + dbPath + " \"" + sentence + "\"";
                startInfo.UseShellExecute = false;
                startInfo.WorkingDirectory = Directory.GetCurrentDirectory();
                startInfo.CreateNoWindow = true;
                cmd.StartInfo = startInfo;
                cmd.Start();
                output = cmd.StandardOutput.ReadToEnd();
                cmd.Close();
            }
            else
            {
                output = "GetCommandID Error: No database loaded";
            }

            return output;
        }

        private string GetCommandPathByID(string id)
        {
            string r = "";
            if (!string.IsNullOrEmpty(dbPath))
            {
                SQLiteConnection conn = new SQLiteConnection("Data Source=" + dbPath + "; Version=3");
                conn.Open();
                SQLiteCommand cmd = new SQLiteCommand($"select path from commands where id_command = '{id}'", conn);
                r = cmd.ExecuteScalar().ToString();
                
            }
            else
            {
                r = "GetCommandPathByID Error: No database loaded.";
            }

            return r;
        }

        private void btnLoadDatabase_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog dialogue = new OpenFileDialog();
            dialogue.Filter = "SQLite Database Files (*.db) | *.db";
            bool? result = dialogue.ShowDialog();
            if(result == true)
            {
                dbPath = dialogue.FileName;
            }
        }

        private void RunCommand(string path)
        {
            Process.Start(path);
        }
    }

}
