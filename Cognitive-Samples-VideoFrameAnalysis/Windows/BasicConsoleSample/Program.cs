// 
// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license.
// 
// Microsoft Cognitive Services: http://www.microsoft.com/cognitive
// 
// Microsoft Cognitive Services Github:
// https://github.com/Microsoft/Cognitive
// 
// Copyright (c) Microsoft Corporation
// All rights reserved.
// 
// MIT License:
// Permission is hereby granted, free of charge, to any person obtaining
// a copy of this software and associated documentation files (the
// "Software"), to deal in the Software without restriction, including
// without limitation the rights to use, copy, modify, merge, publish,
// distribute, sublicense, and/or sell copies of the Software, and to
// permit persons to whom the Software is furnished to do so, subject to
// the following conditions:
// 
// The above copyright notice and this permission notice shall be
// included in all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED ""AS IS"", WITHOUT WARRANTY OF ANY KIND,
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
// NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
// LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
// OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
// WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
// 

using System;
using VideoFrameAnalyzer;
using Microsoft.ProjectOxford.Face;
using Microsoft.ProjectOxford.Face.Contract;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using System.IO;

namespace BasicConsoleSample
{
    internal class Program
    {
        const int CallLimitPerSecond = 10;
        static Queue<DateTime> _timeStampQueue = new Queue<DateTime>(CallLimitPerSecond);

        private static void Main(string[] args)
        {
            // Step 1: Initialization
            const int PersonCount = 2;

            // Step 2: Authorize the API call
            FaceServiceClient faceServiceClient = new FaceServiceClient("1178ed738f7541c28ca797ab1b19f608", "https://westcentralus.api.cognitive.microsoft.com/face/v1.0");

            // Step 3: Create the PersonGroup
            const string personGroupId = "myfamily3";
            const string personGroupName = "MyFamily3";
            _timeStampQueue.Enqueue(DateTime.UtcNow);
            faceServiceClient.CreatePersonGroupAsync(personGroupId, personGroupName).Wait();

            // Step 4: Create the persons to the PersonGroup
            CreatePersonResult[] persons = new CreatePersonResult[PersonCount];
            Parallel.For(0, PersonCount, async i =>
            {
                await WaitCallLimitPerSecondAsync();

                string personName = $"PersonName#{i}";
                persons[i] = await faceServiceClient.CreatePersonAsync(personGroupId, personName);
            });

            // Step 5: Add faces to the persons
            Parallel.For(0, PersonCount, async i =>
            {
                Guid personId = persons[i].PersonId;
                //string personImageDir = @"/path/to/person/i/images";
                string personImageDir = @"E:/Projects/ms-cognitive-services/Cognitive-Samples-VideoFrameAnalysis/Windows/LiveCameraSample/Data/faces/i";


                foreach (string imagePath in Directory.GetFiles(personImageDir, "*.jpg"))
                {
                    await WaitCallLimitPerSecondAsync();

                    using (Stream stream = File.OpenRead(imagePath))
                    {
                        await faceServiceClient.AddPersonFaceAsync(personGroupId, personId, stream);
                    }
                }
            });
        }

        static async Task WaitCallLimitPerSecondAsync()
        {
            Monitor.Enter(_timeStampQueue);
            try
            {
                if (_timeStampQueue.Count >= CallLimitPerSecond)
                {
                    TimeSpan timeInterval = DateTime.UtcNow - _timeStampQueue.Peek();
                    if (timeInterval < TimeSpan.FromSeconds(1))
                    {
                        await Task.Delay(TimeSpan.FromSeconds(1) - timeInterval);
                    }
                    _timeStampQueue.Dequeue();
                }
                _timeStampQueue.Enqueue(DateTime.UtcNow);
            }
            finally
            {
                Monitor.Exit(_timeStampQueue);
            }
        }

        public static void RunBasicConsoleSample()
        {
            // Create grabber. 
            FrameGrabber<Face[]> grabber = new FrameGrabber<Face[]>();

            // Create Face API Client.
            FaceServiceClient faceClient = new FaceServiceClient("df7f34fe20094d87836b165c6adbce41");

            // Set up a listener for when we acquire a new frame.
            grabber.NewFrameProvided += (s, e) =>
            {
                Console.WriteLine("New frame acquired at {0}", e.Frame.Metadata.Timestamp);
            };

            // Set up Face API call.
            grabber.AnalysisFunction = async frame =>
            {
                Console.WriteLine("Submitting frame acquired at {0}", frame.Metadata.Timestamp);
                // Encode image and submit to Face API. 
                return await faceClient.DetectAsync(frame.Image.ToMemoryStream(".jpg"));
            };

            // Set up a listener for when we receive a new result from an API call. 
            grabber.NewResultAvailable += (s, e) =>
            {
                if (e.TimedOut)
                    Console.WriteLine("API call timed out.");
                else if (e.Exception != null)
                    Console.WriteLine("API call threw an exception.");
                else
                    Console.WriteLine("New result received for frame acquired at {0}. {1} faces detected", e.Frame.Metadata.Timestamp, e.Analysis.Length);
            };

            // Tell grabber when to call API.
            // See also TriggerAnalysisOnPredicate
            grabber.TriggerAnalysisOnInterval(TimeSpan.FromMilliseconds(3000));

            // Start running in the background.
            grabber.StartProcessingCameraAsync().Wait();

            // Wait for keypress to stop
            Console.WriteLine("Press any key to stop...");
            Console.ReadKey();

            // Stop, blocking until done.
            grabber.StopProcessingAsync().Wait();

        }
    }
}
