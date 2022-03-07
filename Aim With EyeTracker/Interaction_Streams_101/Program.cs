using System;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using System.Threading;
using System.Diagnostics;

namespace Interaction_Streams_101
{
    public class SharedThreadData {

        public int xValue = 0;
        public int yValue = 0;

        public SharedThreadData()
        {
            xValue = 0;
        }
        public void UpdateEyeCoordinates(int xValue, int yValue)
        {
            this.xValue = xValue;
            this.yValue = yValue;
        }
    }

    public class ThreadManager
    {
        public static SharedThreadData state;

        public static void ReadKeyboard(object data)
        {
            ThreadManager.state = (SharedThreadData)data;
            InterceptKeys.BeginLoop();
        }

        public static void TrackEyeMovement(object data)
        {
            MouseController.TrackEyeMovement((SharedThreadData)data);
        }
    }

    class InterceptKeys
    {
        private const int WH_KEYBOARD_LL = 13;
        private const int WM_KEYDOWN = 0x0100;
        private static LowLevelKeyboardProc _proc = HookCallback;
        private static IntPtr _hookID = IntPtr.Zero;

        public static bool MouseToggleMode = true;
        public static bool isOn = false;

        public static bool FollowMouseGame = true;

        public static void Main()
        {

            if (false)
            {

            }
            else
            {
                //MouseController.ControlArduinoMotor();
                //PredeterminedMovements();
                ShootyMode();
                //MouseController.MoveMouseToWhereEyeTrackerIs();
            }

        }

        public static void PredeterminedMovements()
        {
            MouseController.PredeterminedMovements_UP_DOWN();
            //MouseController.PredeterminedMovements_LOOK_AT_ME();
            //MouseController.PredeterminedMovements_HIT_DRUM();

        }

        public static void ShootyMode()
        {
            SharedThreadData variable = new SharedThreadData();

            // Start a thread that calls a parameterized static method.
            Thread newThread = new Thread(ThreadManager.ReadKeyboard);
            newThread.IsBackground = false;
            newThread.Start(variable);

            Thread newThread2 = new Thread(ThreadManager.TrackEyeMovement);
            newThread2.IsBackground = false;
            newThread2.Start(variable);

            new Thread(() =>
            {
                while (true)
                {
                    //Console.WriteLine(MousePosition.GetCursorPosition().X + " " + MousePosition.GetCursorPosition().Y);
                }
            }).Start();

        }

        public static void BeginLoop()
        {
            _hookID = SetHook(_proc);
            Application.Run();
            UnhookWindowsHookEx(_hookID);
        }

        public static void ButtonControls(string key)
        {
            if (!InterceptKeys.FollowMouseGame)
            {
                if (key == "T" && MouseController.Enabled)
                {
                    int a = 0;
                    while (true)
                    {
                        MouseController.MoveToLocationFromCenter(ThreadManager.state.xValue, ThreadManager.state.yValue);
                        a = a + 1;
                        //Console.WriteLine(a);
                        if (a == 200)
                        {
                            break;
                        }
                    }
                }
            }
            else if (InterceptKeys.MouseToggleMode)
            {
                if (key == "T" && MouseController.Enabled && InterceptKeys.isOn == false)
                {
                    Console.WriteLine("TOGGLE ON");
                    Console.WriteLine("x: " + ThreadManager.state.xValue + ", y: " + ThreadManager.state.yValue);
                    MouseController.MoveToLocationFromCenter(ThreadManager.state.xValue, ThreadManager.state.yValue);
                    MouseOperations.MouseEvent(MouseOperations.MouseEventFlags.LeftDown);
                    InterceptKeys.isOn = true;
                    Thread.Sleep(300);

                }
                else if(key == "T" && MouseController.Enabled && InterceptKeys.isOn == true)
                {
                    Console.WriteLine("TOGGLE ON");
                    MouseOperations.MouseEvent(MouseOperations.MouseEventFlags.LeftUp);
                    InterceptKeys.isOn = false;
                    Thread.Sleep(300);
                }
                else if (key == "J" && MouseController.Enabled)
                {
                    MouseController.AdjustYValue(5);
                    Console.WriteLine("x: " + MouseController.centerPositionCrossHairX.ToString() + ", y: " + MouseController.centerPositionCrossHairY.ToString());
                    Console.WriteLine("N Pressed");
                }
                else if (key == "K" && MouseController.Enabled)
                {
                    MouseController.AdjustYValue(-5);
                    Console.WriteLine("x: " + MouseController.centerPositionCrossHairX.ToString() + ", y: " + MouseController.centerPositionCrossHairY.ToString());
                    Console.WriteLine("N Pressed");
                }
                else if (key == "Y" && MouseController.Enabled)
                {
                    MouseController.AdjustXValue(5);
                    Console.WriteLine("x: " + MouseController.centerPositionCrossHairX.ToString() + ", y: " + MouseController.centerPositionCrossHairY.ToString());
                    Console.WriteLine("N Pressed");
                }
                else if (key == "U" && MouseController.Enabled)
                {
                    MouseController.AdjustXValue(-5);
                    Console.WriteLine("x: " + MouseController.centerPositionCrossHairX.ToString() + ", y: " + MouseController.centerPositionCrossHairY.ToString());
                    Console.WriteLine("N Pressed");
                }
            }
            else{
                //Console.WriteLine(key);
                if (key == "B" && MouseController.Enabled)
                {
                    Console.WriteLine("going to center");
                    MouseController.MoveToCenter();
                }
                // Simply move to a location
                else if (key == "P" && MouseController.Enabled)
                {
                    MouseController.MoveToLocationFromCenter(ThreadManager.state.xValue, ThreadManager.state.yValue);
                    Console.WriteLine("V Pressed");
                }
                // Move to a locationa and SHOOT
                else if (key == "T" && MouseController.Enabled)
                {
                    Console.WriteLine("x: " + ThreadManager.state.xValue + ", y: " + ThreadManager.state.yValue);
                    MouseController.MoveToLocationFromCenter(ThreadManager.state.xValue, ThreadManager.state.yValue);
                    MouseOperations.MouseEvent(MouseOperations.MouseEventFlags.LeftDown);
                    Thread.Sleep(200);
                    MouseOperations.MouseEvent(MouseOperations.MouseEventFlags.LeftUp);
                }
                else if (key == "J" && MouseController.Enabled)
                {
                    MouseController.AdjustYValue(5);
                    Console.WriteLine("x: " + MouseController.centerPositionCrossHairX.ToString() + ", y: " + MouseController.centerPositionCrossHairY.ToString());
                    Console.WriteLine("N Pressed");
                }
                else if (key == "K" && MouseController.Enabled)
                {
                    MouseController.AdjustYValue(-5);
                    Console.WriteLine("x: " + MouseController.centerPositionCrossHairX.ToString() + ", y: " + MouseController.centerPositionCrossHairY.ToString());
                    Console.WriteLine("N Pressed");
                }
                else if (key == "Y" && MouseController.Enabled)
                {
                    MouseController.AdjustXValue(5);
                    Console.WriteLine("x: " + MouseController.centerPositionCrossHairX.ToString() + ", y: " + MouseController.centerPositionCrossHairY.ToString());
                    Console.WriteLine("N Pressed");
                }
                else if (key == "U" && MouseController.Enabled)
                {
                    MouseController.AdjustXValue(-5);
                    Console.WriteLine("x: " + MouseController.centerPositionCrossHairX.ToString() + ", y: " + MouseController.centerPositionCrossHairY.ToString());
                    Console.WriteLine("N Pressed");
                }
                else if (key == "D1")
                {
                    if (MouseController.Enabled)
                    {
                        Console.WriteLine("Mouse Controls Disabled");
                        MouseController.Enabled = false;
                    }
                    else
                    {
                        Console.WriteLine("Mouse Controls Enabled");
                        MouseController.Enabled = true;
                    }
                    Thread.Sleep(100);
                }
            }




        }

        private static IntPtr SetHook(LowLevelKeyboardProc proc)
        {
            using (Process curProcess = Process.GetCurrentProcess())
            using (ProcessModule curModule = curProcess.MainModule)
            {
                return SetWindowsHookEx(WH_KEYBOARD_LL, proc,
                    GetModuleHandle(curModule.ModuleName), 0);
            }
        }

        private delegate IntPtr LowLevelKeyboardProc(
            int nCode, IntPtr wParam, IntPtr lParam);

        private static IntPtr HookCallback(
            int nCode, IntPtr wParam, IntPtr lParam)
        {
            if (nCode >= 0 && wParam == (IntPtr)WM_KEYDOWN)
            {
                int vkCode = Marshal.ReadInt32(lParam);
                ButtonControls(((Keys)vkCode).ToString());

            }
            return CallNextHookEx(_hookID, nCode, wParam, lParam);
        }

        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern IntPtr SetWindowsHookEx(int idHook,
            LowLevelKeyboardProc lpfn, IntPtr hMod, uint dwThreadId);

        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool UnhookWindowsHookEx(IntPtr hhk);

        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern IntPtr CallNextHookEx(IntPtr hhk, int nCode,
            IntPtr wParam, IntPtr lParam);

        [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern IntPtr GetModuleHandle(string lpModuleName);
    }

    public class SafeSpaceCoordinates
    {
        int lowerX;
        int upperX;
        int lowerY;
        int upperY;

        public static SafeSpaceCoordinates Instance = new SafeSpaceCoordinates(2400, 1440);
        int squareDiameter = 200;
        public SafeSpaceCoordinates(int screenWidth, int screenHeight)
        {
            this.lowerX = (screenWidth / 2) - squareDiameter;
            this.upperX = (screenWidth / 2) + squareDiameter;
            this.lowerY = (screenHeight / 2) - squareDiameter;
            this.upperY = (screenHeight / 2) + squareDiameter;
            //Console.WriteLine(lowerX);
            //Console.WriteLine(upperX);
            //Console.WriteLine(lowerY);
            //Console.WriteLine(upperY);
        }
        public bool CheckIfCoordinatesInCenterPoint(double x, double y)
        {
            x = (int)x;
            y = (int)y;

            bool debug = false;
            if (debug)
            {
                Console.WriteLine("begin");
                Console.WriteLine(x + " " + this.lowerX + " " + this.upperX);
                Console.WriteLine(y + " " + this.lowerY + " " + this.upperY);
            }

            if (x > this.upperX ||
                x < this.lowerX
                 || y > this.upperY
                 || y < this.lowerY
                )
            {
                return false;
            }
            return true;
        }

    }
}
