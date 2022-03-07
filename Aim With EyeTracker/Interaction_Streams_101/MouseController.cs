using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System;
using Tobii.Interaction;
using Solid.Arduino;
using Solid.Arduino.Firmata;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using System.Threading;
using Point = System.Drawing.Point;

namespace Interaction_Streams_101
{
    
    public static class MouseController
    {

        static bool DebugMode = false;
        public static bool Enabled = true;

        static int MovementSpeed = 10;

        //This is when I self define what the center position is, for calibration purposes
        static int centerX = 0;
        static int centerY = 0;

        // This is the position that I use for reference of where I'm shooting at
        // I want to be able to change this on the fly                              sda
        //static int centerPositionCrossHairX = 1280;
        public static int centerPositionCrossHairX = 965;
        //static int centerPositionCrossHairY = 718;
        public static int centerPositionCrossHairY = 490;

        public static double MouseAccelerationLeft = .55;

        public static double MouseAccelerationRight = .65;

        public static void TrackEyeMovement(SharedThreadData threadSafeVariable)
        {
            var host = new Host();
            var myCursor = new Cursor(Cursor.Current.Handle);
            Cursor.Position = new Point(1300, 720);
            var gazePointDataStream = host.Streams.CreateGazePointDataStream();
            gazePointDataStream.GazePoint((x, y, ts) => MoveMouseToCursor(x, y, threadSafeVariable));
            Console.ReadKey();
            host.DisableConnection();
        }
        public static void MoveMouseToWhereEyeTrackerIs()
        {
            var host = new Host();
            var myCursor = new Cursor(Cursor.Current.Handle);
            Cursor.Position = new Point(1300, 720);
            var gazePointDataStream = host.Streams.CreateGazePointDataStream();
            gazePointDataStream.GazePoint((x, y, ts) => MoveMouseToLocation((int)x, (int)y));
            Console.ReadKey();
            host.DisableConnection();
        }
        public static void MoveMouseToLocation(int destX, int destY)
        {
            int x = MousePosition.GetCursorPosition().X;
            int y = MousePosition.GetCursorPosition().Y;

            Console.WriteLine(x + " : " + destX);
            Console.WriteLine(y + " : " + destY);
            int xMovemnet = destX - x;
            int yMovement = destY - y;

            RelativeMove(xMovemnet, yMovement);

        }

        [DllImport("User32.dll")]
        static extern void mouse_event(int dwFlags, int dx, int dy, int dwData, int dwExtraInfo);
        public static void RelativeMove(int relx, int rely)
        {
            mouse_event(0x0001, relx, rely, 0, 0);
        }
        public static void GetCurrentMousePosition()
        {
            
        }

        public static void MoveToLocationFromCenter(int destX, int destY)
        {
             Console.WriteLine(centerPositionCrossHairX + " : " + destX);
             Console.WriteLine(centerPositionCrossHairY + " : " + destY);

            int xMovement = 0;

            if(destX - MouseController.centerPositionCrossHairX > 0)
            {
                xMovement = (int)((destX - MouseController.centerPositionCrossHairX) * MouseController.MouseAccelerationRight);
            }
            else
            {
                xMovement = (int)((destX - MouseController.centerPositionCrossHairX) * MouseController.MouseAccelerationLeft);
            }

            int yMovement = (int)((destY - MouseController.centerPositionCrossHairY) * .45);

            if (false)
            {
                RelativeMove(xMovement, yMovement);
            }
            else
            {

                int relativemovementX = (xMovement / 5);
                int relativemovementY = (yMovement / 5);

                for (int i = 0; i < 5; i++)
                {
                    Thread.Sleep(5);
                    RelativeMove(relativemovementX, relativemovementY);
                }
            }

        }

        public static void AdjustXValue(int value)
        {
            MouseController.centerPositionCrossHairX += value;
            Console.WriteLine("center position x: " + MouseController.centerPositionCrossHairX);
        }

        public static void AdjustYValue(int value)
        {
            MouseController.centerPositionCrossHairY += value;
            //Console.WriteLine("center position y: " + MouseController.centerPositionCrossHairY);
        }



        public static void Calibrate()
        {
            int x = MousePosition.GetCursorPosition().X;
            int y = MousePosition.GetCursorPosition().Y;
            centerX = x;
            centerY = y;
            Debug("new center: " + centerX + "," + centerY);
        }

        public static void MoveToCenter()
        {
            int x = MousePosition.GetCursorPosition().X;
            int y = MousePosition.GetCursorPosition().Y;

            //Console.WriteLine(x + " : " + centerX);
            //Console.WriteLine(y + " : " + centerY);

            int xMovemnet = centerX - x;
            int yMovement = centerY - y;

            RelativeMove(xMovemnet, yMovement);
        }

        // Moves to the x,y assuming that the mouse is currently at the centerpoint
        public static void MoveRelativeToCenterDot(int x, int y)
        {
            int xMovemnet = x - centerPositionCrossHairX;
            int yMovement = y - centerPositionCrossHairY;

            RelativeMove(xMovemnet, yMovement);
        }


        static int arduinoMode = 0;
        public static void Main2(string[] args)
        {

            if (arduinoMode == 1)
            {
                ControlArduinoMotor();
            }
            else
            {
                //DebugPosition();
                //MoveCursor();
            }
        }

        public static void MoveMouseToCursor(double x, double y, SharedThreadData threadSafeVariable)
        {

            // X : 0-2600
            // Y : 0-1440
            // bool IsCenter = SafeSpaceCoordinates.Instance.CheckIfCoordinatesInCenterPoint(x, y);

            if (true)
            {
                threadSafeVariable.UpdateEyeCoordinates((int)x, (int)y);
            }
            else
            {
                if (x > 1300)
                {
                    RelativeMove(MovementSpeed, 0);
                }
                else
                {
                    RelativeMove(-1 * MovementSpeed, 0);
                }

                if (y > 720)
                {
                    RelativeMove(0, MovementSpeed);
                }
                else
                {
                    RelativeMove(0, -1 * MovementSpeed);
                }
            }
        }

        public static void moveRelative()
        {
            while (true)
            {
                Thread.Sleep(50);
                RelativeMove(0, 2);
            }
        }

        public static void DebugPosition()
        {
            var host = new Host();
            var gazePointDataStream = host.Streams.CreateGazePointDataStream();
            gazePointDataStream.GazePoint((x, y, ts) => Console.WriteLine((int)x + " : " + (int)y));
            Console.ReadKey();
            host.DisableConnection();
        }
        public static void ControlArduinoMotor()
        {
            ISerialConnection connection = GetConnection();
            var session = (connection != null) ? new ArduinoSession(connection) : null;
            session.SetDigitalPinMode(9, PinMode.ServoControl);
            session.SetDigitalPinMode(8, PinMode.ServoControl);
            var host = new Host();
            var gazePointDataStream = host.Streams.CreateGazePointDataStream();
            gazePointDataStream.GazePoint((x, y, ts) => DoActionOnEyeMovement(x, y, session));
            Console.ReadKey();
            host.DisableConnection();
        }

        public static void PredeterminedMovements_HIT_DRUM()
        {
            ISerialConnection connection = GetConnection();
            var session = (connection != null) ? new ArduinoSession(connection) : null;

            session.SetDigitalPin(8, 110);
            Thread.Sleep(4000);

            session.SetDigitalPin(8, 40);
            Thread.Sleep(3000);

            session.SetDigitalPin(8, 110);
            Thread.Sleep(4000);
        }

        public static void PredeterminedMovements_UP_DOWN()
        {
            ISerialConnection connection = GetConnection();
            var session = (connection != null) ? new ArduinoSession(connection) : null;

            session.SetDigitalPinMode(9, PinMode.ServoControl);
            session.SetDigitalPinMode(8, PinMode.ServoControl);

            Thread.Sleep(2000);

            session.SetDigitalPin(8, 70);
            Thread.Sleep(100);

            session.SetDigitalPin(8, 110);
            Thread.Sleep(200);

            session.SetDigitalPin(8, 70);
            Thread.Sleep(100);

        }

        public static void PredeterminedMovements_LOOK_AT_ME()
        {
            ISerialConnection connection = GetConnection();
            var session = (connection != null) ? new ArduinoSession(connection) : null;

            session.SetDigitalPin(8, 80); // UP
            session.SetDigitalPin(9, 100); // LEFT

            Thread.Sleep(4000);

            // Home location
            session.SetDigitalPin(8, 100);
            session.SetDigitalPin(9, 0);

            Thread.Sleep(6000);

        }



        // x value ranges from 0-2400
        // y value ranges from 0-1300
        public static void DoActionOnEyeMovement(double x, double y, ArduinoSession session)
        {
            // this is straight forward
            //session.SetDigitalPin(9, 30); // yValue
            //session.SetDigitalPin(8, 85); // yValue

            bool motormode = true;

            int lowerboundX = 0;
            int upperboundX = 60;

            int lowerBoundY = 60;
            int upperBoundY = 135;

            //session.SetDigitalPin(9, 60); // yValue

            // get the percentage across the screen you're looking

            int xValueNoralized = (int)(Math.Abs(upperboundX - (x / 2400) * 60));
            Console.WriteLine(xValueNoralized);

            int yValueNoralized = Math.Abs((upperBoundY + lowerBoundY) - (lowerBoundY + (int)((y / 1400) * (upperBoundY - lowerBoundY)))) + 15;
            Console.WriteLine(xValueNoralized + " : " + yValueNoralized);

            //Console.WriteLine((int)x + " " + (int)y);

            if (motormode == true)
            {
                session.SetDigitalPin(9, xValueNoralized); // yValue

                session.SetDigitalPin(8, yValueNoralized); // yValue

            }

        }

        private static ISerialConnection GetConnection()
        {
            Console.WriteLine("Searching Arduino connection...");
            ISerialConnection connection = EnhancedSerialConnection.Find();

            if (connection == null)
                Console.WriteLine("No connection found. Make shure your Arduino board is attached to a USB port.");
            else
                Console.WriteLine($"Connected to port {connection.PortName} at {connection.BaudRate} baud.");

            return connection;
        }

        public static void Debug(string debugValue)
        {
            if (DebugMode)
            {
                Console.WriteLine(debugValue);
            }
        }
    }
}
