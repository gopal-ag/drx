using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class PlaceManager : MonoBehaviour
{
    private PlaceIndicator placeIndicator;
    public GameObject ballHitIndicator;
    public GameObject cricketStump;
    public GameObject ball;
    private GameObject[] newPlacedObject = new GameObject[2];
    private GameObject newBall;
    private GameObject newBallHitIndicator;
    public TextMeshProUGUI placeButtonText;

    private int stumps_placed = 0;
    private int ball_placed = 0;

    // Parameters for the ball throw
    private Vector3 intermediateTargetPosition;
    private Vector3 midAirTargetPosition;
    private Vector3 finalTargetPosition;
    private bool isMovingToIntermediate = false;
    private bool isMovingToMidAir = false;
    private bool isMovingToFinal = false;
    public float throwSpeed = 5f;

    void Start()
    {
        placeIndicator = FindObjectOfType<PlaceIndicator>();
    }

    public void ClickToPlace()
    {
        // Instantiate the object to place at the position of the place indicator and confirm its rotation
        if (placeButtonText.text == "Place Stumps")
        {
            newPlacedObject[stumps_placed] = Instantiate(cricketStump, placeIndicator.transform.position, placeIndicator.transform.rotation, placeIndicator.transform);
            placeButtonText.text = "Confirm";
        }
        else if (placeButtonText.text == "Confirm")
        {
            // Detach the object from the place indicator and set its parent to null
            newPlacedObject[stumps_placed].transform.parent = null;
            placeButtonText.text = "Place Stumps";
            stumps_placed++;
            if (stumps_placed >= 2)
            {
                placeButtonText.text = "Throw Ball!";
                return;
            }
        }
        else if (placeButtonText.text == "Throw Ball!")
        {
            // Calculate target positions
            intermediateTargetPosition = newPlacedObject[0].transform.position + (newPlacedObject[1].transform.position - newPlacedObject[0].transform.position) * 0.33f;
            finalTargetPosition = newPlacedObject[0].transform.GetChild(2).transform.position;
            midAirTargetPosition = (intermediateTargetPosition + finalTargetPosition) / 2;
            newBallHitIndicator = Instantiate(ballHitIndicator, intermediateTargetPosition, Quaternion.identity);

            // Set movement flags
            isMovingToIntermediate = true;
            isMovingToMidAir = false;
            isMovingToFinal = false;

            // Update button text
            placeButtonText.text = "";

            // Initialize ball throw parameters
            if (newBall != null)
            {
                Destroy(newBall);
            }
            Vector3 ball_pos = newPlacedObject[1].transform.Find("BallPos").position;
            newBall = Instantiate(ball, ball_pos, newPlacedObject[1].transform.rotation);
            ball_placed++;
        }
    }

    void Update()
    {
        if (isMovingToIntermediate || isMovingToMidAir || isMovingToFinal)
        {
            MoveBall();
        }
    }

    private void MoveBall()
    {
        float step = throwSpeed * Time.deltaTime;

        if (isMovingToIntermediate)
        {
            newBall.transform.position = Vector3.MoveTowards(newBall.transform.position, intermediateTargetPosition, step);
            if (Vector3.Distance(newBall.transform.position, intermediateTargetPosition) < 0.001f)
            {
                isMovingToIntermediate = false;
                isMovingToMidAir = true;
            }
        }
        else if (isMovingToMidAir)
        {
            newBall.transform.position = Vector3.MoveTowards(newBall.transform.position, midAirTargetPosition, step);
            if (Vector3.Distance(newBall.transform.position, midAirTargetPosition) < 0.001f)
            {
                isMovingToMidAir = false;
                isMovingToFinal = true;
            }
        }
        else if (isMovingToFinal)
        {
            newBall.transform.position = Vector3.MoveTowards(newBall.transform.position, finalTargetPosition, step);
            if (Vector3.Distance(newBall.transform.position, finalTargetPosition) < 0.001f)
            {
                newBall.transform.position = finalTargetPosition;
                isMovingToFinal = false;
            }
        }
    }
}
