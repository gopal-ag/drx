using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UIElements;

public class Stumps : MonoBehaviour
{
    public MeshRenderer meshRenderer;
    // Start is called before the first frame update
    void OnEnable()
    {  
    }

    void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.tag == "Ball")
        {
            meshRenderer.material.color = Color.green;
        }
    }
}
