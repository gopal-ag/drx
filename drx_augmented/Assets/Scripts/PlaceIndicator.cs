using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;

public class PlaceIndicator : MonoBehaviour
{
    public ARRaycastManager raycastManager;
    public GameObject indicator;
    public List<ARRaycastHit> hits = new List<ARRaycastHit>();
    public bool showIndicator = true;
    void Start()
    {
        raycastManager = FindObjectOfType<ARRaycastManager>();
        indicator = transform.GetChild(0).gameObject;
        indicator.SetActive(false);
    }

    void Update()
    {
        var ray = new Vector2(Screen.width / 2, Screen.height / 2);

        if(raycastManager.Raycast(ray, hits, TrackableType.PlaneWithinPolygon))
        {
            var hitPose = hits[0].pose;
            transform.position = hitPose.position;
            transform.rotation = hitPose.rotation;
            if (!indicator.activeInHierarchy && showIndicator)
            {
                indicator.SetActive(true);
            }
        }
        else if (indicator.activeInHierarchy || !showIndicator)
        {
            indicator.SetActive(false);
        }
    }
}
