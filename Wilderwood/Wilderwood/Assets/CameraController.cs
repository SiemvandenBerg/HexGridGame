using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    public float moveSpeed = 5f;
    public float rotateSpeed = 50f;
    public float zoomSpeed = 5f;

    void Update()
    {
        // Move camera with WASD keys
        if (Input.GetKey(KeyCode.W))
            transform.position += new Vector3(0, 0, moveSpeed * Time.deltaTime);
        if (Input.GetKey(KeyCode.S))
            transform.position -= new Vector3(0, 0, moveSpeed * Time.deltaTime);
        if (Input.GetKey(KeyCode.A))
            transform.position -= new Vector3(moveSpeed * Time.deltaTime, 0, 0);
        if (Input.GetKey(KeyCode.D))
            transform.position += new Vector3(moveSpeed * Time.deltaTime, 0, 0);

        // Rotate camera with Q and E keys
        if (Input.GetKey(KeyCode.Q))
            transform.RotateAround(transform.position + transform.forward, Vector3.up, -rotateSpeed * Time.deltaTime);
        if (Input.GetKey(KeyCode.E))
            transform.RotateAround(transform.position + transform.forward, Vector3.up, rotateSpeed * Time.deltaTime);

        // Zoom camera with mouse scroll wheel
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        transform.position += transform.forward * scroll * zoomSpeed * Time.deltaTime;
    }
}

// using System.Collections;
// using System.Collections.Generic;
// using UnityEngine;

// public class CameraController : MonoBehaviour
// {
//     public float movementSpeed = 10f;
//     public float rotationSpeed = 100f;

//     void Update()
//     {
//         // Camera movement controls
//         float horizontalInput = Input.GetAxis("Horizontal");
//         float verticalInput = Input.GetAxis("Vertical");
//         float depthInput = Input.GetAxis("Depth");

//         transform.Translate(new Vector3(horizontalInput, depthInput, verticalInput) * Time.deltaTime * movementSpeed);

//         // Camera rotation controls
//         float rotateHorizontalInput = Input.GetAxis("RotateHorizontal");
//         float rotateVerticalInput = Input.GetAxis("RotateVertical");

//         transform.RotateAround(transform.position, Vector3.up, rotateHorizontalInput * Time.deltaTime * rotationSpeed);
//         transform.RotateAround(transform.position, transform.right, -rotateVerticalInput * Time.deltaTime * rotationSpeed);
//     }
// }
