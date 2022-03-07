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
using System.Drawing;
using Rectangle = System.Drawing.Rectangle;
using System;
using System.Threading;
using System.Windows;
using Point = System.Drawing.Point;
using Gma.System.MouseKeyHook;
using System;
using System.Diagnostics;
using System.Windows.Forms;
using System.Runtime.InteropServices;

namespace Interaction_Streams_101
{
    public class MousePosition
    {
        // <summary>
        /// Struct representing a point.
        /// </summary>
        [StructLayout(LayoutKind.Sequential)]
        public struct POINT
        {
            public int X;
            public int Y;

            public static implicit operator Point(POINT point)
            {
                return new Point(point.X, point.Y);
            }
        }

        /// <summary>
        /// Retrieves the cursor's position, in screen coordinates.
        /// </summary>
        /// <see>See MSDN documentation for further information.</see>
        [DllImport("user32.dll")]
        public static extern bool GetCursorPos(out POINT lpPoint);

        public static Point GetCursorPosition()
        {
            POINT lpPoint;
            GetCursorPos(out lpPoint);
            // NOTE: If you need error handling
            // bool success = GetCursorPos(out lpPoint);
            // if (!success)

            return lpPoint;
        }

        public static void GetCurserPointRelative()
        {
            Point p = GetCursorPosition();
        }
    }
}
