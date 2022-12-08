using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;

public class HandTracking : MonoBehaviour
{
    // Start is called before the first frame update
    public UDPReceive udpReceive;
    public GameObject[] handLeft;
    public GameObject[] handRight;

    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        string data = udpReceive.data;

        print(data);
        string[] hands = data.Split(';');
        print(hands[0]);

        //0        1*3      2*3
        //x1,y1,z1,x2,y2,z2,x3,y3,z3

        if (hands[0].Trim().Length > 0)
        {
            string[] landmarks = hands[0].Split('/');
            for (int i = 0; i < landmarks.Length; i++)
            {
                string[] landmark = landmarks[i].Split(',');
                float x = float.Parse(landmark[0], CultureInfo.InvariantCulture.NumberFormat) / 100;
                float y = float.Parse(landmark[1], CultureInfo.InvariantCulture.NumberFormat) / 100 * -1;
                float z = float.Parse(landmark[2], CultureInfo.InvariantCulture.NumberFormat) / 100 * -1;

                handLeft[i].transform.localPosition = new Vector3(x, y + 7, z);
            }
        }

        if (hands[1].Trim().Length > 0)
        {
            string[] landmarks = hands[1].Split('/');
            for (int i = 0; i < landmarks.Length; i++)
            {
                string[] landmark = landmarks[i].Split(',');
                float x = float.Parse(landmark[0], CultureInfo.InvariantCulture.NumberFormat) / 100;
                float y = float.Parse(landmark[1], CultureInfo.InvariantCulture.NumberFormat) / 100 * -1;
                float z = float.Parse(landmark[2], CultureInfo.InvariantCulture.NumberFormat) / 100 * -1;

                handRight[i].transform.localPosition = new Vector3(x, y + 7, z);
            }
        }
    }
}